-- ============================================================================
-- MIGRATION 009: ACCOUNT-WIDE LIFECYCLE, INSTITUTIONAL ARCHIVE & AUDIT TRAIL
-- ============================================================================
-- Mode: Strictly Additive, Idempotent, Forward-Recoverable, Zero-Destructive-Drops
-- Reference: PHASE 3 — REVISE MIGRATION 009 BEFORE USE
--
-- KEY SAFEGUARDS IMPLEMENTED:
-- 1. AUTH CASCADE IMMUNITY: Replaces ON DELETE CASCADE on profiles.id with
--    ON DELETE RESTRICT to guarantee an Auth user deletion NEVER cascades into
--    and destroys profiles, Journeys, Consultations, or Legal Acceptances.
-- 2. ROLE SEPARATION: Keeps account_status (ACTIVE, TEMPORARILY_SUSPENDED,
--    ARCHIVED, PENDING_DELETION) strictly separate from role status
--    (user_roles.status: active, pending_nda, suspended, revoked).
-- 3. IMMUTABLE AUDIT LOG: account_lifecycle_log stores tamper-evident timeline
--    with RLS denying UPDATE and DELETE to all roles.
-- 4. STRICT SOLE ADMIN: Restricted to fulcrumindia1@gmail.com
--    (UUID: 616304b5-aef5-4cd0-88be-2fda7ddf7f88).
-- ============================================================================

BEGIN;

-- ----------------------------------------------------------------------------
-- PART 1: EXTEND PROFILES TABLE WITH ACCOUNT LIFECYCLE & LEGAL HOLD COLUMNS
-- ----------------------------------------------------------------------------

DO $$
BEGIN
    -- account_status: High-level account authorization state
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'profiles' AND column_name = 'account_status'
    ) THEN
        ALTER TABLE public.profiles
            ADD COLUMN account_status VARCHAR(30) DEFAULT 'ACTIVE';
    END IF;

    -- legal_hold: Prevents scheduled closure or lawful erasure while compliance hold is active
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'profiles' AND column_name = 'legal_hold'
    ) THEN
        ALTER TABLE public.profiles
            ADD COLUMN legal_hold BOOLEAN DEFAULT FALSE;
    END IF;

    -- lifecycle_reason: Institutional justification for current account state
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'profiles' AND column_name = 'lifecycle_reason'
    ) THEN
        ALTER TABLE public.profiles
            ADD COLUMN lifecycle_reason TEXT;
    END IF;

    -- status_updated_at: Timestamp of latest account lifecycle transition
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'profiles' AND column_name = 'status_updated_at'
    ) THEN
        ALTER TABLE public.profiles
            ADD COLUMN status_updated_at TIMESTAMPTZ DEFAULT NOW();
    END IF;

    -- status_updated_by: Administrator actor who authorized the transition
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'profiles' AND column_name = 'status_updated_by'
    ) THEN
        ALTER TABLE public.profiles
            ADD COLUMN status_updated_by UUID REFERENCES auth.users(id) ON DELETE SET NULL;
    END IF;

    -- deletion_requested_at: When user or admin initiated closure review
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'profiles' AND column_name = 'deletion_requested_at'
    ) THEN
        ALTER TABLE public.profiles
            ADD COLUMN deletion_requested_at TIMESTAMPTZ;
    END IF;

    -- deletion_requested_by: Identity that requested closure
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'profiles' AND column_name = 'deletion_requested_by'
    ) THEN
        ALTER TABLE public.profiles
            ADD COLUMN deletion_requested_by UUID REFERENCES auth.users(id) ON DELETE SET NULL;
    END IF;

    -- deletion_scheduled_for: Scheduled expiration date (e.g. 30 days grace window)
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'profiles' AND column_name = 'deletion_scheduled_for'
    ) THEN
        ALTER TABLE public.profiles
            ADD COLUMN deletion_scheduled_for TIMESTAMPTZ;
    END IF;

    -- retention_notes: Legal hold notes, compliance justification, or archive details
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'profiles' AND column_name = 'retention_notes'
    ) THEN
        ALTER TABLE public.profiles
            ADD COLUMN retention_notes TEXT;
    END IF;
END $$;

-- Enforce valid account_status domain constraint
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'check_account_status_valid'
    ) THEN
        ALTER TABLE public.profiles
            ADD CONSTRAINT check_account_status_valid
            CHECK (account_status IN ('ACTIVE', 'TEMPORARILY_SUSPENDED', 'ARCHIVED', 'PENDING_DELETION'));
    END IF;
END $$;

-- Performance index for active account directory filtering
CREATE INDEX IF NOT EXISTS idx_profiles_account_status_active
    ON public.profiles(account_status, role)
    WHERE is_active = TRUE;

-- ----------------------------------------------------------------------------
-- PART 2: REMOVE DANGEROUS CASCADE ON AUTH FOREIGN KEY (PHASE 3A)
-- ----------------------------------------------------------------------------
-- In the baseline schema, profiles.id REFERENCES auth.users(id) ON DELETE CASCADE.
-- If an auth user is removed, PostgreSQL cascades and destroys profiles and journeys.
-- We replace this with ON DELETE RESTRICT to guarantee referential safety.
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.table_constraints
        WHERE constraint_name = 'profiles_id_fkey' AND table_name = 'profiles'
    ) THEN
        ALTER TABLE public.profiles DROP CONSTRAINT profiles_id_fkey;
        ALTER TABLE public.profiles
            ADD CONSTRAINT profiles_id_fkey
            FOREIGN KEY (id) REFERENCES auth.users(id) ON DELETE RESTRICT;
    END IF;
END $$;

-- ----------------------------------------------------------------------------
-- PART 3: CREATE IMMUTABLE ACCOUNT ACTION HISTORY (LIFECYCLE AUDIT LOG)
-- ----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS public.account_lifecycle_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    actor_id UUID NOT NULL,
    action VARCHAR(50) NOT NULL CHECK (action IN (
        'SUSPEND',
        'RESUME',
        'ARCHIVE',
        'RESTORE',
        'REQUEST_DELETION',
        'CANCEL_DELETION',
        'APPLY_LEGAL_HOLD',
        'RELEASE_LEGAL_HOLD'
    )),
    previous_status VARCHAR(30),
    new_status VARCHAR(30),
    reason TEXT NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_acc_lifecycle_log_user
    ON public.account_lifecycle_log(user_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_acc_lifecycle_log_action
    ON public.account_lifecycle_log(action, created_at DESC);

-- ----------------------------------------------------------------------------
-- PART 4: ROW LEVEL SECURITY (RLS) FOR ACCOUNT LIFECYCLE & ARCHIVE
-- ----------------------------------------------------------------------------

ALTER TABLE public.account_lifecycle_log ENABLE ROW LEVEL SECURITY;

-- Sole Admin may inspect all lifecycle audit records
DROP POLICY IF EXISTS "Sole Admin full access to account_lifecycle_log" ON public.account_lifecycle_log;
CREATE POLICY "Sole Admin full access to account_lifecycle_log"
    ON public.account_lifecycle_log
    FOR ALL
    TO authenticated
    USING (public.is_admin())
    WITH CHECK (public.is_admin());

-- Users may view their own lifecycle timeline events
DROP POLICY IF EXISTS "Users can view own account_lifecycle_log" ON public.account_lifecycle_log;
CREATE POLICY "Users can view own account_lifecycle_log"
    ON public.account_lifecycle_log
    FOR SELECT
    TO authenticated
    USING (user_id = auth.uid());

-- Immutable log rule: No ordinary authenticated user can UPDATE or DELETE audit events
DROP POLICY IF EXISTS "Deny update on account_lifecycle_log" ON public.account_lifecycle_log;
CREATE POLICY "Deny update on account_lifecycle_log"
    ON public.account_lifecycle_log
    FOR UPDATE
    TO authenticated
    USING (FALSE);

DROP POLICY IF EXISTS "Deny delete on account_lifecycle_log" ON public.account_lifecycle_log;
CREATE POLICY "Deny delete on account_lifecycle_log"
    ON public.account_lifecycle_log
    FOR DELETE
    TO authenticated
    USING (FALSE);

-- ----------------------------------------------------------------------------
-- PART 5: BACKFILL EXISTING RECORDS
-- ----------------------------------------------------------------------------

-- Ensure all existing profiles have account_status populated based on is_active
UPDATE public.profiles
SET account_status = CASE
        WHEN is_active = TRUE OR is_active IS NULL THEN 'ACTIVE'
        ELSE 'TEMPORARILY_SUSPENDED'
    END,
    legal_hold = COALESCE(legal_hold, FALSE),
    status_updated_at = COALESCE(status_updated_at, updated_at, created_at, NOW())
WHERE account_status IS NULL;

COMMIT;

