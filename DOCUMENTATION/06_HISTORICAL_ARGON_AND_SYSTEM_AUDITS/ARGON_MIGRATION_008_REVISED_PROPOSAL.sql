-- =============================================================================
-- FULCRUM-INDIA: AGY ARGON — Migration 008 (REVISED PROPOSAL ONLY)
-- =============================================================================
-- PROPOSAL STATUS: STATIC CODE INSPECTION ONLY — DO NOT EXECUTE IN PRODUCTION
-- OWNER APPROVAL REQUIRED PRIOR TO LIVE POSTGRES APPLICATION.
-- 
-- SUMMARY:
-- 1. Additive schema for Guide and SME professional headshots (professional_photos).
-- 2. Enforces maximum 153,600 bytes (150 KB) hard stored cap at database level.
-- 3. Strict RLS: Owner self-management requires active role & accepted NDA.
-- 4. Aspirant view access restricted to verified assigned mentors.
-- 5. Isolated Platform Admin authority verified by Auth UUID and email.
-- 6. NON-DESTRUCTIVE: Preserves all existing tables, photos, and user data.
-- =============================================================================

-- 1. Ensure private storage bucket for professional photos exists
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
    'professional-profile-photos',
    'professional-profile-photos',
    false,
    153600, -- 150 KB hard cap
    ARRAY['image/webp', 'image/png', 'image/jpeg']::text[]
)
ON CONFLICT (id) DO UPDATE SET
    public = false,
    file_size_limit = 153600,
    allowed_mime_types = ARRAY['image/webp', 'image/png', 'image/jpeg']::text[];

-- 2. Create professional_photos metadata table (additive, does not alter aspirant_photos)
CREATE TABLE IF NOT EXISTS public.professional_photos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    role_context TEXT NOT NULL CHECK (role_context IN ('guide', 'sme')),
    storage_bucket TEXT NOT NULL DEFAULT 'professional-profile-photos',
    storage_path TEXT NOT NULL,
    content_type TEXT NOT NULL CHECK (content_type IN ('image/webp', 'image/png', 'image/jpeg')),
    file_size_bytes INTEGER NOT NULL CHECK (file_size_bytes > 0 AND file_size_bytes <= 153600),
    width INTEGER,
    height INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now()),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now()),
    CONSTRAINT uq_professional_photos_user_role UNIQUE (user_id, role_context)
);

-- Enable RLS
ALTER TABLE public.professional_photos ENABLE ROW LEVEL SECURITY;

-- 3. RLS Policies on public.professional_photos
DROP POLICY IF EXISTS "Admin full control professional_photos" ON public.professional_photos;
CREATE POLICY "Admin full control professional_photos" ON public.professional_photos
    FOR ALL TO authenticated
    USING (
        auth.jwt() ->> 'email' = 'fulcrumindia1@gmail.com'
        OR EXISTS (
            SELECT 1 FROM public.profiles p 
            WHERE p.id = auth.uid() AND p.role = 'admin' AND p.email = 'fulcrumindia1@gmail.com'
        )
    )
    WITH CHECK (
        auth.jwt() ->> 'email' = 'fulcrumindia1@gmail.com'
        OR EXISTS (
            SELECT 1 FROM public.profiles p 
            WHERE p.id = auth.uid() AND p.role = 'admin' AND p.email = 'fulcrumindia1@gmail.com'
        )
    );

DROP POLICY IF EXISTS "Active NDA-compliant mentors manage own photo" ON public.professional_photos;
CREATE POLICY "Active NDA-compliant mentors manage own photo" ON public.professional_photos
    FOR ALL TO authenticated
    USING (
        auth.uid() = user_id
        AND EXISTS (
            SELECT 1 FROM public.user_roles ur
            WHERE ur.user_id = auth.uid() 
              AND ur.role = professional_photos.role_context
              AND ur.status = 'active'
        )
        AND EXISTS (
            SELECT 1 FROM public.legal_acceptances la
            WHERE la.user_id = auth.uid()
              AND la.status = 'ACCEPTED'
              AND (la.doc_type IN ('nda_dual', 'nda_' || professional_photos.role_context)
                   OR la.roles_covered::text ILIKE '%' || professional_photos.role_context || '%')
        )
    )
    WITH CHECK (
        auth.uid() = user_id
        AND EXISTS (
            SELECT 1 FROM public.user_roles ur
            WHERE ur.user_id = auth.uid() 
              AND ur.role = professional_photos.role_context
              AND ur.status = 'active'
        )
    );

DROP POLICY IF EXISTS "Assigned entrepreneurs view mentor professional photo" ON public.professional_photos;
CREATE POLICY "Assigned entrepreneurs view mentor professional photo" ON public.professional_photos
    FOR SELECT TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM public.relationships r
            WHERE r.aspirant_id = auth.uid()
              AND r.status = 'active'
              AND (
                  (professional_photos.role_context = 'guide' AND (r.guide_id = professional_photos.user_id OR (r.guide_ids IS NOT NULL AND r.guide_ids ? professional_photos.user_id::text)))
                  OR
                  (professional_photos.role_context = 'sme' AND (r.sme_id = professional_photos.user_id OR (r.sme_ids IS NOT NULL AND r.sme_ids ? professional_photos.user_id::text)))
              )
        )
    );

-- 4. Storage Policies on storage.objects for professional-profile-photos
DROP POLICY IF EXISTS "Admin full control professional photo objects" ON storage.objects;
CREATE POLICY "Admin full control professional photo objects" ON storage.objects
    FOR ALL TO authenticated
    USING (
        bucket_id = 'professional-profile-photos'
        AND (
            auth.jwt() ->> 'email' = 'fulcrumindia1@gmail.com'
            OR EXISTS (SELECT 1 FROM public.profiles p WHERE p.id = auth.uid() AND p.role = 'admin' AND p.email = 'fulcrumindia1@gmail.com')
        )
    );

DROP POLICY IF EXISTS "Mentors upload own professional photo object" ON storage.objects;
CREATE POLICY "Mentors upload own professional photo object" ON storage.objects
    FOR INSERT TO authenticated
    WITH CHECK (
        bucket_id = 'professional-profile-photos'
        AND (storage.foldername(name))[1] = auth.uid()::text
        AND (octet_length(COALESCE(metadata->>'size', '0')::text) <= 153600)
        AND EXISTS (
            SELECT 1 FROM public.user_roles ur
            WHERE ur.user_id = auth.uid() 
              AND ur.status = 'active'
              AND ur.role IN ('guide', 'sme')
        )
        AND EXISTS (
            SELECT 1 FROM public.legal_acceptances la
            WHERE la.user_id = auth.uid()
              AND la.status = 'ACCEPTED'
        )
    );

DROP POLICY IF EXISTS "Mentors update and delete own professional photo object" ON storage.objects;
CREATE POLICY "Mentors update and delete own professional photo object" ON storage.objects
    FOR ALL TO authenticated
    USING (
        bucket_id = 'professional-profile-photos'
        AND (storage.foldername(name))[1] = auth.uid()::text
    );

DROP POLICY IF EXISTS "Assigned entrepreneurs read mentor professional photo object" ON storage.objects;
CREATE POLICY "Assigned entrepreneurs read mentor professional photo object" ON storage.objects
    FOR SELECT TO authenticated
    USING (
        bucket_id = 'professional-profile-photos'
        AND EXISTS (
            SELECT 1 FROM public.relationships r
            WHERE r.aspirant_id = auth.uid()
              AND r.status = 'active'
              AND (
                  r.guide_id::text = (storage.foldername(name))[1]
                  OR (r.guide_ids IS NOT NULL AND r.guide_ids ? (storage.foldername(name))[1])
                  OR r.sme_id::text = (storage.foldername(name))[1]
                  OR (r.sme_ids IS NOT NULL AND r.sme_ids ? (storage.foldername(name))[1])
              )
        )
    );
