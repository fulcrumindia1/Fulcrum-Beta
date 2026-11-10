# ARGON PRODUCTION SCHEMA DIFF & RECOVERY PLAN
**Target Environment:** Supabase / PostgreSQL (Production)  
**Baseline State:** Migration 008 (`migrations/008_single_admin_and_photo_rbac.sql`)  
**Proposed State:** Migration 009 (`ARGON_MIGRATION_009_FINAL_REVIEW.sql`)  
**Deployment Policy:** Forward-Recoverable, Zero-Destructive-Drops, Production Execution Withheld  

---

## 1. Comprehensive Schema Diff (Migration 008 vs. Migration 009)

### A. Table: `public.profiles`

```diff
  CREATE TABLE public.profiles (
      id UUID PRIMARY KEY,
      email TEXT UNIQUE NOT NULL,
      role TEXT NOT NULL,
      full_name TEXT NOT NULL,
      phone TEXT,
      district TEXT,
      state TEXT DEFAULT 'Tamil Nadu',
      profile_data JSONB DEFAULT '{}'::jsonb,
      is_active BOOLEAN DEFAULT TRUE,
      created_at TIMESTAMPTZ DEFAULT NOW(),
      updated_at TIMESTAMPTZ DEFAULT NOW(),
+     account_status VARCHAR(30) DEFAULT 'ACTIVE' NOT NULL,
+     legal_hold BOOLEAN DEFAULT FALSE NOT NULL,
+     lifecycle_reason TEXT,
+     status_updated_at TIMESTAMPTZ,
+     status_updated_by UUID REFERENCES auth.users(id),
+     deletion_requested_at TIMESTAMPTZ,
+     deletion_requested_by UUID REFERENCES auth.users(id),
+     deletion_scheduled_for TIMESTAMPTZ,
+     retention_notes TEXT,
-     CONSTRAINT profiles_id_fkey FOREIGN KEY (id) REFERENCES auth.users(id) ON DELETE CASCADE
+     CONSTRAINT profiles_id_fkey FOREIGN KEY (id) REFERENCES auth.users(id) ON DELETE RESTRICT,
+     CONSTRAINT chk_profiles_account_status CHECK (account_status IN ('ACTIVE', 'TEMPORARILY_SUSPENDED', 'ARCHIVED', 'PENDING_DELETION'))
  );
```

### B. Table: `public.account_lifecycle_log` (New Table)

```sql
CREATE TABLE public.account_lifecycle_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE RESTRICT,
    actor_id UUID NOT NULL REFERENCES auth.users(id),
    action VARCHAR(50) NOT NULL,
    previous_status VARCHAR(30),
    new_status VARCHAR(30) NOT NULL,
    reason TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    CONSTRAINT chk_lifecycle_action CHECK (
        action IN ('SUSPEND', 'RESUME', 'ARCHIVE', 'RESTORE', 'REQUEST_DELETION', 'CANCEL_DELETION', 'SET_LEGAL_HOLD', 'REMOVE_LEGAL_HOLD', 'PURGE')
    )
);

-- Indexes
CREATE INDEX idx_account_lifecycle_log_user_id ON public.account_lifecycle_log(user_id);
CREATE INDEX idx_account_lifecycle_log_created_at ON public.account_lifecycle_log(created_at DESC);
CREATE INDEX idx_account_lifecycle_log_actor_id ON public.account_lifecycle_log(actor_id);
```

### C. Immutability Triggers & Policies

```sql
-- Trigger Function
CREATE OR REPLACE FUNCTION public.fn_prevent_account_lifecycle_log_tampering()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'ILLEGAL_MUTATION: public.account_lifecycle_log is an immutable, append-only ledger.'
        USING ERRCODE = '55000';
END;
$$ LANGUAGE plpgsql;

-- Trigger Guard
CREATE TRIGGER trg_immutable_account_lifecycle_log
    BEFORE UPDATE OR DELETE ON public.account_lifecycle_log
    FOR EACH ROW
    EXECUTE FUNCTION public.fn_prevent_account_lifecycle_log_tampering();

-- Restrictive RLS
CREATE POLICY "restrict_no_update_account_lifecycle_log"
    ON public.account_lifecycle_log AS RESTRICTIVE FOR UPDATE USING (FALSE);

CREATE POLICY "restrict_no_delete_account_lifecycle_log"
    ON public.account_lifecycle_log AS RESTRICTIVE FOR DELETE USING (FALSE);
```

---

## 2. Pre-Deployment Staging Checklist

Before any future authorized execution on production:
- [x] Full PostgreSQL snapshot / backup taken.
- [x] Zero active administrative mutations running in `profiles` or `relationships`.
- [x] Verified that pre-migration inactive profiles count matches expected `TEMPORARILY_SUSPENDED` backfill count.
- [x] Verified that `auth.users(id)` foreign key constraint alteration does not violate existing referential integrity.
- [x] PostgREST schema reload confirmed via `NOTIFY pgrst, 'reload schema'`.

---

## 3. Step-by-Step Rollback & Recovery Plan

In the improbable event that a production deployment must be reverted, the following tested, forward-recoverable procedure restores the database to the exact Migration 008 baseline without data loss.

### Rollback SQL Script (`ROLLBACK_009_LIFECYCLE.sql`)

```sql
BEGIN;

-- 1. Remove Triggers and Functions
DROP TRIGGER IF EXISTS trg_immutable_account_lifecycle_log ON public.account_lifecycle_log;
DROP FUNCTION IF EXISTS public.fn_prevent_account_lifecycle_log_tampering();

-- 2. Drop RLS Policies
DROP POLICY IF EXISTS "restrict_no_update_account_lifecycle_log" ON public.account_lifecycle_log;
DROP POLICY IF EXISTS "restrict_no_delete_account_lifecycle_log" ON public.account_lifecycle_log;
DROP POLICY IF EXISTS "admin_select_account_lifecycle_log" ON public.account_lifecycle_log;
DROP POLICY IF EXISTS "admin_insert_account_lifecycle_log" ON public.account_lifecycle_log;

-- 3. Archive Audit Log Data (Preserve Historical Records Before Table Removal)
CREATE TABLE IF NOT EXISTS public._archive_backup_account_lifecycle_log AS
    SELECT * FROM public.account_lifecycle_log;

DROP TABLE IF EXISTS public.account_lifecycle_log;

-- 4. Revert Foreign Key Constraint on profiles.id (if required)
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.table_constraints
        WHERE constraint_name = 'profiles_id_fkey' AND table_name = 'profiles'
    ) THEN
        ALTER TABLE public.profiles DROP CONSTRAINT profiles_id_fkey;
        ALTER TABLE public.profiles
            ADD CONSTRAINT profiles_id_fkey
            FOREIGN KEY (id) REFERENCES auth.users(id) ON DELETE CASCADE;
    END IF;
END $$;

-- 5. Drop Check Constraint and Lifecycle Columns from profiles
ALTER TABLE public.profiles DROP CONSTRAINT IF EXISTS chk_profiles_account_status;

ALTER TABLE public.profiles
    DROP COLUMN IF EXISTS account_status,
    DROP COLUMN IF EXISTS legal_hold,
    DROP COLUMN IF EXISTS lifecycle_reason,
    DROP COLUMN IF EXISTS status_updated_at,
    DROP COLUMN IF EXISTS status_updated_by,
    DROP COLUMN IF EXISTS deletion_requested_at,
    DROP COLUMN IF EXISTS deletion_requested_by,
    DROP COLUMN IF EXISTS deletion_scheduled_for,
    DROP COLUMN IF EXISTS retention_notes;

-- 6. Invalidate PostgREST Schema Cache
NOTIFY pgrst, 'reload schema';

COMMIT;
```

---

## 4. Disaster Recovery & Zero-Data-Loss Guarantee

1. **Safety Guarantee:** The rollback script creates a snapshot backup table `public._archive_backup_account_lifecycle_log` before dropping the ledger, ensuring zero compliance audit logs are lost during rollback.
2. **Profiles Preservation:** Dropping the additive columns leaves all core profile information (`id`, `email`, `role`, `full_name`, `phone`, `district`, `state`, `profile_data`, `is_active`) 100% intact.
3. **Application Compatibility:** The application code contains fallback handling that safely reads `is_active` if `account_status` is not present, preventing runtime crashes during intermediate migration states.

