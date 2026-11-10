# FULCRUM-BETA 2.1 — SCHEMA CONTRACT AUDIT REPORT

**Document Status:** Schema and DDL Verification Attestation  
**Date:** November 10, 2026  
**Auditor:** Independent Principal Systems Forensic Engineer & Release Architect  

---

## 1. Canonical Table Definitions

### 1.1 `public.profiles`
The consolidated schema defines the following columns for account lifecycle governance and user profiles:
- `id` (UUID, Primary Key, Foreign Key -> `auth.users(id)` ON DELETE RESTRICT)
- `email` (TEXT, Unique, NOT NULL)
- `role` (TEXT, Default `'aspirant'`)
- `full_name` (TEXT, NOT NULL)
- `phone` (TEXT)
- `district` (TEXT)
- `state` (TEXT, Default `'Tamil Nadu'`)
- `profile_data` (JSONB / TEXT, Default `'{}'`)
- `is_active` (BOOLEAN, Default `TRUE`)
- `account_status` (VARCHAR(30), Default `'ACTIVE'`, CHECK IN `('ACTIVE', 'TEMPORARILY_SUSPENDED', 'ARCHIVED', 'PENDING_DELETION')`)
- `legal_hold` (BOOLEAN, Default `FALSE`)
- `lifecycle_reason` (TEXT)
- `status_updated_at` (TIMESTAMPTZ, Default `NOW()`)
- `status_updated_by` (UUID, Foreign Key -> `auth.users(id)` ON DELETE SET NULL)
- `deletion_requested_at` (TIMESTAMPTZ)
- `deletion_requested_by` (UUID, Foreign Key -> `auth.users(id)` ON DELETE SET NULL)
- `deletion_scheduled_for` (TIMESTAMPTZ)
- `retention_notes` (TEXT)
- `created_at` (TIMESTAMPTZ, Default `NOW()`)
- `updated_at` (TIMESTAMPTZ, Default `NOW()`)

> **Contract Rule:** No fictitious columns (e.g. `status_reason`, `archived_at`, `restored_at`, `reactivated_at`, `grace_period_days`) may be queried or updated. All status transitions record their timestamp in `status_updated_at` and explanation in `lifecycle_reason`.

---

### 1.2 `public.account_lifecycle_log`
The immutable audit log table possesses the following canonical schema:
- `id` (UUID, Primary Key, Default `gen_random_uuid()`)
- `user_id` (UUID, NOT NULL)
- `actor_id` (UUID, NOT NULL)
- `action` (VARCHAR(50), NOT NULL, CHECK IN `('SUSPEND', 'RESUME', 'ARCHIVE', 'RESTORE', 'REQUEST_DELETION', 'CANCEL_DELETION', 'APPLY_LEGAL_HOLD', 'RELEASE_LEGAL_HOLD')`)
- `previous_status` (VARCHAR(30))
- `new_status` (VARCHAR(30))
- `reason` (TEXT, NOT NULL)
- `metadata` (JSONB, Default `'{}'::jsonb`)
- `created_at` (TIMESTAMPTZ, Default `NOW()`)

> **Contract Rule:** Column names are strictly `previous_status` (NOT `old_status`) and `metadata` (NOT `details`).
> **Security Rule:** Triple-layer immutability enforced:
> 1. Table DAC: `REVOKE UPDATE, DELETE, TRUNCATE ON public.account_lifecycle_log FROM authenticated, anon, public;`
> 2. RLS AS RESTRICTIVE policies for UPDATE and DELETE evaluating to `FALSE`.
> 3. PostgreSQL trigger `trg_immutable_account_lifecycle_log` aborting any mutation attempts.

---

## 2. Dynamic Sole Admin SQL DDL

### 2.1 Function: `public.is_admin()`
Eliminated hardcoded old UUID. Resolved dynamically against the Sole Admin email:
```sql
CREATE OR REPLACE FUNCTION public.is_admin()
RETURNS BOOLEAN AS $$
    SELECT EXISTS (
        SELECT 1 FROM public.profiles
        WHERE id = auth.uid()
          AND lower(email) = 'fulcrumindia1@gmail.com'
          AND role = 'admin'
    );
$$ LANGUAGE sql SECURITY DEFINER STABLE;
```

### 2.2 Trigger Function: `public.handle_new_user()`
```sql
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
```

### 2.3 Single Admin Role Locks
- In `public.enforce_single_admin_profile_guard()`: Only `lower(email) = 'fulcrumindia1@gmail.com'` can receive role `'admin'`. Any other email is demoted to `'aspirant'`.
- In `public.enforce_single_admin_user_roles_guard()`: Any insert or update to `public.user_roles` with role `'admin'` requires that the corresponding profile belongs to `fulcrumindia1@gmail.com`.
- In `public.account_lifecycle_log` RLS policies:
  ```sql
  USING (
      auth.jwt() ->> 'email' = 'fulcrumindia1@gmail.com'
      OR public.is_admin()
  );
  ```

---

## 3. Reconciliation Diff Matrix

| Location | Old Defective Code | Canonical Remediated Code |
| :--- | :--- | :--- |
| `services/account_lifecycle.py:114` | `select("... status_reason, archived_at, restored_at ...")` | `select("... lifecycle_reason, status_updated_at, status_updated_by ...")` |
| `services/account_lifecycle.py:342` | `update({"status_reason": ...})` | `update({"lifecycle_reason": ..., "status_updated_at": ...})` |
| `services/account_lifecycle.py:351` | `insert({"old_status": ..., "details": ...})` | `insert({"previous_status": ..., "metadata": ...})` |
| `services/account_lifecycle.py:446` | `update({"reactivated_at": ...})` | Removed `reactivated_at`, set `status_updated_at` |
| `services/account_lifecycle.py:718` | `update({"archived_at": ...})` | Removed `archived_at`, set `status_updated_at` |
| `services/account_lifecycle.py:825` | `update({"restored_at": ...})` | Removed `restored_at`, set `status_updated_at` |
| `services/account_lifecycle.py:948` | `update({"grace_period_days": ...})` | Removed `grace_period_days`, set `status_updated_at` |
| `migrations/008_...sql:23, 41, 55` | Hardcoded `616304b5-aef5-4cd0-88be-2fda7ddf7f88` | Dynamic lookup on `lower(email) = 'fulcrumindia1@gmail.com'` |
| `migrations/009_...sql:227, 246` | Hardcoded `auth.uid() = '616304b5...'::uuid` | `auth.jwt() ->> 'email' = 'fulcrumindia1@gmail.com' OR public.is_admin()` |

