-- ============================================================================
-- MIGRATION 008: SINGLE-ADMIN IDENTITY LOCK, PRIVATE PROFESSIONAL PHOTOGRAPHS,
--                POST-RELEASE SCHEME TRACKING & COMPOSITE PERFORMANCE INDEXES
-- ============================================================================
-- Safe to run multiple times (100% idempotent, zero destructive drops).
-- ============================================================================

BEGIN;

-- ----------------------------------------------------------------------------
-- PART 1: RECONCILE & LOCK SINGLE ADMIN IDENTITY (fulcrumindia1@gmail.com)
-- ----------------------------------------------------------------------------

UPDATE public.profiles
SET role = 'aspirant',
    updated_at = NOW()
WHERE lower(email) <> 'fulcrumindia1@gmail.com'
  AND lower(role) IN ('admin', 'district_admin', 'operational_admin');

UPDATE public.profiles
SET role = 'admin',
    updated_at = NOW()
WHERE lower(email) = 'fulcrumindia1@gmail.com';

DELETE FROM public.user_roles
WHERE lower(role) IN ('admin', 'district_admin', 'operational_admin')
  AND user_id NOT IN (SELECT id FROM public.profiles WHERE lower(email) = 'fulcrumindia1@gmail.com');

INSERT INTO public.user_roles (user_id, role, status)
SELECT id, 'aspirant', 'active'
FROM public.profiles
WHERE id = '2970a3ee-46fc-483c-b276-aa2a955ba123'::uuid
ON CONFLICT (user_id, role) DO UPDATE SET status = 'active';

CREATE OR REPLACE FUNCTION public.is_admin()
RETURNS BOOLEAN AS $$
    SELECT EXISTS (
        SELECT 1 FROM public.profiles
        WHERE id = auth.uid()
          AND lower(email) = 'fulcrumindia1@gmail.com'
          AND role = 'admin'
    );
$$ LANGUAGE sql SECURITY DEFINER STABLE;

CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
DECLARE
    v_req_role TEXT;
    v_safe_role TEXT;
BEGIN
    v_req_role := lower(COALESCE(NEW.raw_user_meta_data->>'role', 'aspirant'));
    IF lower(NEW.email) = 'fulcrumindia1@gmail.com' THEN
        v_safe_role := 'admin';
    ELSIF v_req_role IN ('guide', 'sme', 'aspirant') THEN
        v_safe_role := v_req_role;
    ELSE
        v_safe_role := 'aspirant';
    END IF;

    INSERT INTO public.profiles (id, email, full_name, role)
    VALUES (
        NEW.id,
        NEW.email,
        COALESCE(NEW.raw_user_meta_data->>'full_name', split_part(NEW.email, '@', 1)),
        v_safe_role
    )
    ON CONFLICT (id) DO NOTHING;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION public.enforce_single_admin_profile_guard()
RETURNS TRIGGER AS $$
BEGIN
    IF lower(COALESCE(NEW.role, '')) IN ('admin', 'district_admin', 'operational_admin') THEN
        IF lower(COALESCE(NEW.email, '')) <> 'fulcrumindia1@gmail.com' THEN
            NEW.role := 'aspirant';
        ELSE
            NEW.role := 'admin';
        END IF;
    END IF;

    IF TG_OP = 'UPDATE' AND NEW.role IS DISTINCT FROM OLD.role THEN
        IF auth.uid() IS NOT NULL AND NOT public.is_admin() THEN
            NEW.role := OLD.role;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS trg_enforce_single_admin_profile ON public.profiles;
CREATE TRIGGER trg_enforce_single_admin_profile
    BEFORE INSERT OR UPDATE ON public.profiles
    FOR EACH ROW EXECUTE FUNCTION public.enforce_single_admin_profile_guard();

CREATE OR REPLACE FUNCTION public.enforce_single_admin_user_roles_guard()
RETURNS TRIGGER AS $$
BEGIN
    IF lower(COALESCE(NEW.role, '')) IN ('admin', 'district_admin', 'operational_admin') THEN
        IF NOT EXISTS (
            SELECT 1 FROM public.profiles
            WHERE id = NEW.user_id AND lower(email) = 'fulcrumindia1@gmail.com'
        ) THEN
            RAISE EXCEPTION 'Security Violation: Only fulcrumindia1@gmail.com may hold the admin role.';
        END IF;
        NEW.role := 'admin';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS trg_enforce_single_admin_user_roles ON public.user_roles;
CREATE TRIGGER trg_enforce_single_admin_user_roles
    BEFORE INSERT OR UPDATE ON public.user_roles
    FOR EACH ROW EXECUTE FUNCTION public.enforce_single_admin_user_roles_guard();

-- ----------------------------------------------------------------------------
-- PART 2: PRIVATE PROFESSIONAL PHOTOGRAPHS FOR GUIDES & SMES
-- ----------------------------------------------------------------------------

INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
    'professional-headshots',
    'professional-headshots',
    FALSE,
    5242880,
    ARRAY['image/jpeg', 'image/png', 'image/webp']
)
ON CONFLICT (id) DO UPDATE
SET public = FALSE,
    file_size_limit = 5242880,
    allowed_mime_types = ARRAY['image/jpeg', 'image/png', 'image/webp'];

CREATE TABLE IF NOT EXISTS public.professional_photos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE REFERENCES public.profiles(id) ON DELETE CASCADE,
    storage_bucket TEXT NOT NULL DEFAULT 'professional-headshots',
    storage_path TEXT NOT NULL,
    mime_type TEXT NOT NULL DEFAULT 'image/webp',
    byte_size INTEGER NOT NULL CHECK (byte_size > 0 AND byte_size <= 153600),
    width INTEGER NOT NULL DEFAULT 320 CHECK (width = 320),
    height INTEGER NOT NULL DEFAULT 320 CHECK (height = 320),
    sha256_hash TEXT NOT NULL,
    uploaded_by UUID NOT NULL REFERENCES public.profiles(id),
    uploaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_professional_photos_user_id
    ON public.professional_photos(user_id);

ALTER TABLE public.professional_photos ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Admin full access professional_photos" ON public.professional_photos;
CREATE POLICY "Admin full access professional_photos"
    ON public.professional_photos FOR ALL
    USING (public.is_admin())
    WITH CHECK (public.is_admin());

DROP POLICY IF EXISTS "Guide or SME self access professional_photos" ON public.professional_photos;
CREATE POLICY "Guide or SME self access professional_photos"
    ON public.professional_photos FOR ALL
    USING (
        user_id = auth.uid()
        AND (
            EXISTS (SELECT 1 FROM public.profiles p WHERE p.id = auth.uid() AND p.role IN ('guide', 'sme'))
            OR EXISTS (SELECT 1 FROM public.user_roles ur WHERE ur.user_id = auth.uid() AND ur.role IN ('guide', 'sme') AND ur.status = 'active')
        )
    )
    WITH CHECK (
        user_id = auth.uid()
        AND (
            EXISTS (SELECT 1 FROM public.profiles p WHERE p.id = auth.uid() AND p.role IN ('guide', 'sme'))
            OR EXISTS (SELECT 1 FROM public.user_roles ur WHERE ur.user_id = auth.uid() AND ur.role IN ('guide', 'sme') AND ur.status = 'active')
        )
    );

DROP POLICY IF EXISTS "Admin full access professional headshots storage" ON storage.objects;
CREATE POLICY "Admin full access professional headshots storage"
    ON storage.objects FOR ALL
    USING (bucket_id = 'professional-headshots' AND public.is_admin())
    WITH CHECK (bucket_id = 'professional-headshots' AND public.is_admin());

DROP POLICY IF EXISTS "Guide SME own folder access professional headshots storage" ON storage.objects;
CREATE POLICY "Guide SME own folder access professional headshots storage"
    ON storage.objects FOR ALL
    USING (
        bucket_id = 'professional-headshots'
        AND (storage.foldername(name))[1] = auth.uid()::text
    )
    WITH CHECK (
        bucket_id = 'professional-headshots'
        AND (storage.foldername(name))[1] = auth.uid()::text
    );

-- ----------------------------------------------------------------------------
-- PART 3: POST-RELEASE SCHEME APPLICATION STAGE TRACKING COLUMNS
-- ----------------------------------------------------------------------------

ALTER TABLE public.scheme_releases
    ADD COLUMN IF NOT EXISTS application_stage TEXT NOT NULL DEFAULT 'Recommended',
    ADD COLUMN IF NOT EXISTS application_note TEXT DEFAULT '',
    ADD COLUMN IF NOT EXISTS stage_updated_at TIMESTAMPTZ DEFAULT NOW(),
    ADD COLUMN IF NOT EXISTS stage_updated_by UUID REFERENCES public.profiles(id);

DROP POLICY IF EXISTS "Aspirants and assigned Guides update scheme stage" ON public.scheme_releases;
CREATE POLICY "Aspirants and assigned Guides update scheme stage"
    ON public.scheme_releases FOR UPDATE
    USING (
        public.is_admin()
        OR aspirant_id = auth.uid()
        OR EXISTS (
            SELECT 1 FROM public.relationships r
            WHERE r.aspirant_id = public.scheme_releases.aspirant_id
              AND r.guide_id = auth.uid()
              AND r.status = 'active'
        )
    )
    WITH CHECK (
        public.is_admin()
        OR aspirant_id = auth.uid()
        OR EXISTS (
            SELECT 1 FROM public.relationships r
            WHERE r.aspirant_id = public.scheme_releases.aspirant_id
              AND r.guide_id = auth.uid()
              AND r.status = 'active'
        )
    );

-- ----------------------------------------------------------------------------
-- PART 4 (CR-03): SCHEMA-VERIFIED COMPOSITE POSTGRESQL INDEXES FOR SCALE
-- ----------------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_profiles_role_active
    ON public.profiles (role, is_active);

CREATE INDEX IF NOT EXISTS idx_relationships_status_aspirant
    ON public.relationships (status, aspirant_id, guide_id, sme_id);

CREATE INDEX IF NOT EXISTS idx_help_requests_status_created_desc
    ON public.help_requests (status, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_help_requests_guide_status
    ON public.help_requests (assigned_guide_id, status, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_help_requests_sme_status
    ON public.help_requests (assigned_sme_id, status, created_at DESC);

COMMIT;

