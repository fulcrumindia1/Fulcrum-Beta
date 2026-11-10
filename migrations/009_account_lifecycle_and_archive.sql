-- ============================================================================
-- MIGRATION 009 (HARDENED): ACCOUNT-WIDE LIFECYCLE, ARCHIVE & AUDIT TRAIL
-- ============================================================================
-- Mode: Strictly Additive, Idempotent, Forward-Recoverable, Zero-Destructive-Drops
-- References:
--   - P0 — Fix fail-open account authorization
--   - P0 — Audit logs must really be immutable
--   - P0 — Correct Migration 009's existing-user backfill
--
-- CRITICAL REFERENTIAL MODIFICATION ACKNOWLEDGEMENT:
-- This migration explicitly alters the foreign key constraint on public.profiles.id
-- from 'ON DELETE CASCADE' to 'ON DELETE RESTRICT'. This is an intentional security
-- modification designed to guarantee that an Auth user deletion NEVER cascades into
-- and destroys profiles, Journeys, Consultations, Scheme Releases, or Legal Acceptances.
--
-- KEY SAFEGUARDS IMPLEMENTED:
-- 1. AUTH CASCADE IMMUNITY: Replaces ON DELETE CASCADE on profiles.id with
--    ON DELETE RESTRICT.
-- 2. IMMUTABLE AUDIT LOG (TRIPLE-LAYER DEFENSE):
--    a. Table Privileges: REVOKE UPDATE, DELETE, TRUNCATE from authenticated, anon, public.
--    b. Restrictive RLS: AS RESTRICTIVE policies FOR UPDATE and FOR DELETE USING (FALSE).
--    c. Database Trigger: trg_immutable_account_lifecycle_log aborts any UPDATE or DELETE.
-- 3. SAFE EXISTING-USER BACKFILL:
--    Correctly classifies pre-migration inactive profiles (is_active = FALSE) as
--    'TEMPORARILY_SUSPENDED', preventing them from being mistakenly marked 'ACTIVE'.
-- 4. ROLE STATUS SEPARATION: Keeps account_status (ACTIVE, TEMPORARILY_SUSPENDED,
--    ARCHIVED, PENDING_DELETION) strictly separate from role status
--    (user_roles.status: active, pending_nda, suspended, revoked).
-- ============================================================================

BEGIN;

-- ----------------------------------------------------------------------------
-- PART 1: EXTEND PROFILES TABLE WITH ACCOUNT LIFECYCLE & LEGAL HOLD COLUMNS
-- ----------------------------------------------------------------------------

DO $$
BEGIN
    -- account_status: High-level account authorization state
    -- Added without immediate default to avoid masking legacy is_active states during initial backfill
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'profiles' AND column_name = 'account_status'
    ) THEN
        ALTER TABLE public.profiles
            ADD COLUMN account_status VARCHAR(30);
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

-- ----------------------------------------------------------------------------
-- PART 2: SAFE EXISTING-USER BACKFILL (P0)
-- ----------------------------------------------------------------------------
-- Ensures that pre-migration inactive profiles (is_active = FALSE) are classified
-- as 'TEMPORARILY_SUSPENDED' and NEVER accidentally elevated to 'ACTIVE'.
UPDATE public.profiles
SET account_status = CASE
        WHEN is_active = FALSE THEN 'TEMPORARILY_SUSPENDED'
        ELSE 'ACTIVE'
    END,
    legal_hold = COALESCE(legal_hold, FALSE),
    status_updated_at = COALESCE(status_updated_at, updated_at, created_at, NOW())
WHERE account_status IS NULL
   OR (account_status = 'ACTIVE' AND is_active = FALSE);

-- Now set future default to 'ACTIVE' for newly registered profiles
ALTER TABLE public.profiles
    ALTER COLUMN account_status SET DEFAULT 'ACTIVE';

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
-- PART 3: REMOVE DANGEROUS CASCADE ON AUTH FOREIGN KEY (P0)
-- ----------------------------------------------------------------------------
-- Replaces ON DELETE CASCADE with ON DELETE RESTRICT on profiles.id.
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
-- PART 4: CREATE IMMUTABLE ACCOUNT ACTION HISTORY (LIFECYCLE AUDIT LOG)
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
-- PART 5: TRIPLE-LAYER IMMUTABLE AUDIT LOG ENFORCEMENT (P0)
-- ----------------------------------------------------------------------------

-- Layer A: Table Privileges (DAC)
-- Explicitly revoke UPDATE, DELETE, and TRUNCATE from all roles
REVOKE UPDATE, DELETE, TRUNCATE ON public.account_lifecycle_log FROM authenticated, anon, public;
GRANT SELECT, INSERT ON public.account_lifecycle_log TO authenticated;

-- Layer B: Row Level Security (RLS)
ALTER TABLE public.account_lifecycle_log ENABLE ROW LEVEL SECURITY;

-- Sole Admin SELECT Policy (Read-Only)
DROP POLICY IF EXISTS "Sole Admin select account_lifecycle_log" ON public.account_lifecycle_log;
CREATE POLICY "Sole Admin select account_lifecycle_log"
    ON public.account_lifecycle_log
    FOR SELECT
    TO authenticated
    USING (
        auth.jwt() ->> 'email' = 'fulcrumindia1@gmail.com'
        OR public.is_admin()
    );

-- User SELECT Policy (View own audit trail)
DROP POLICY IF EXISTS "Users view own account_lifecycle_log" ON public.account_lifecycle_log;
CREATE POLICY "Users view own account_lifecycle_log"
    ON public.account_lifecycle_log
    FOR SELECT
    TO authenticated
    USING (user_id = auth.uid());

-- Authenticated INSERT Policy (Append-Only)
-- Strict Defense: Only Sole Admin or self-service deletion actions can insert
DROP POLICY IF EXISTS "Authenticated insert account_lifecycle_log" ON public.account_lifecycle_log;
CREATE POLICY "Authenticated insert account_lifecycle_log"
    ON public.account_lifecycle_log
    FOR INSERT
    TO authenticated
    WITH CHECK (
        (auth.jwt() ->> 'email' = 'fulcrumindia1@gmail.com' OR public.is_admin())
        OR (
            auth.uid() = actor_id
            AND auth.uid() = user_id
            AND action IN ('REQUEST_DELETION', 'CANCEL_DELETION')
        )
    );

-- RESTRICTIVE Policies: In PostgreSQL, AS RESTRICTIVE policies are combined with AND!
-- They absolutely override any permissive policies and block all UPDATE/DELETE attempts.
DROP POLICY IF EXISTS "Restrictive deny update on account_lifecycle_log" ON public.account_lifecycle_log;
CREATE POLICY "Restrictive deny update on account_lifecycle_log"
    ON public.account_lifecycle_log
    AS RESTRICTIVE
    FOR UPDATE
    TO authenticated, anon, public
    USING (FALSE);

DROP POLICY IF EXISTS "Restrictive deny delete on account_lifecycle_log" ON public.account_lifecycle_log;
CREATE POLICY "Restrictive deny delete on account_lifecycle_log"
    ON public.account_lifecycle_log
    AS RESTRICTIVE
    FOR DELETE
    TO authenticated, anon, public
    USING (FALSE);

-- Layer C: Database Trigger Guard
-- Even if executed by superuser or service role, the trigger aborts UPDATE or DELETE
CREATE OR REPLACE FUNCTION public.enforce_account_lifecycle_log_immutability()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'ACCOUNT_LIFECYCLE_LOG IS STRICTLY APPEND-ONLY: UPDATE and DELETE operations are prohibited by institutional security policy.'
        USING ERRCODE = 'integrity_constraint_violation';
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_immutable_account_lifecycle_log ON public.account_lifecycle_log;
CREATE TRIGGER trg_immutable_account_lifecycle_log
BEFORE UPDATE OR DELETE ON public.account_lifecycle_log
FOR EACH ROW
EXECUTE FUNCTION public.enforce_account_lifecycle_log_immutability();

-- ----------------------------------------------------------------------------
-- PART 6: POSTGREST SCHEMA CACHE REFRESH
-- ----------------------------------------------------------------------------
NOTIFY pgrst, 'reload schema';

COMMIT;
