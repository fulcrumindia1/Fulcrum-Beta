-- =============================================================================
-- FULCRUM-BETA: MIGRATION 007 — MULTI-ROLE ARCHITECTURE & USER ROLES TABLE
-- =============================================================================
-- Fixes: PGRST205 "Could not find the table 'public.user_roles' in the schema cache"
-- 1. Creates public.user_roles table with idempotent check constraint.
-- 2. Sets up performance indexes and Row Level Security (RLS).
-- 3. Automatically seeds user_roles with existing profiles.
-- 4. Reloads the PostgREST schema cache so Streamlit Cloud detects it immediately.
-- =============================================================================

-- 1. USER ROLES TABLE
CREATE TABLE IF NOT EXISTS public.user_roles (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id           UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    role              TEXT NOT NULL CHECK (role IN ('aspirant', 'guide', 'sme', 'admin', 'district_admin', 'operational_admin')),
    status            TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'pending_nda', 'suspended', 'revoked')),
    granted_by        UUID REFERENCES public.profiles(id),
    granted_at        TIMESTAMPTZ DEFAULT NOW(),
    activated_at      TIMESTAMPTZ,
    suspended_at      TIMESTAMPTZ,
    revoked_at        TIMESTAMPTZ,
    revocation_reason TEXT,
    created_at        TIMESTAMPTZ DEFAULT NOW(),
    updated_at        TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT uq_user_role UNIQUE (user_id, role)
);

-- Performance Indexes
CREATE INDEX IF NOT EXISTS idx_user_roles_user_id ON public.user_roles(user_id);
CREATE INDEX IF NOT EXISTS idx_user_roles_role_status ON public.user_roles(role, status);

-- 2. ROW LEVEL SECURITY (RLS)
ALTER TABLE public.user_roles ENABLE ROW LEVEL SECURITY;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE tablename = 'user_roles' 
        AND policyname = 'Admin full access user_roles'
    ) THEN
        CREATE POLICY "Admin full access user_roles" 
        ON public.user_roles
        FOR ALL TO authenticated 
        USING (public.is_admin());
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE tablename = 'user_roles' 
        AND policyname = 'Users read own user_roles'
    ) THEN
        CREATE POLICY "Users read own user_roles" 
        ON public.user_roles
        FOR SELECT TO authenticated 
        USING (user_id = auth.uid());
    END IF;
END $$;

-- 3. SEED USER ROLES FROM PROFILES (Non-destructive initial backfill)
INSERT INTO public.user_roles (user_id, role, status, granted_at, activated_at)
SELECT id, role, 'active', created_at, created_at
FROM public.profiles
WHERE role IN ('aspirant', 'guide', 'sme', 'admin')
ON CONFLICT (user_id, role) DO NOTHING;

-- 4. RELOAD SCHEMA CACHE
NOTIFY pgrst, 'reload schema';

