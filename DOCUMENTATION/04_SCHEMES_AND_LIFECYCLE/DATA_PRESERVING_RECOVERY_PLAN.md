# FULCRUM-BETA — DATA-PRESERVING RECOVERY & ROLLBACK PLAN

**Author:** Fulcrum Database Engineering & Governance Team  
**Date:** November 2026  
**Status:** ARCHITECTURAL SPECIFICATION & STAGING RECOVERY RUNBOOK  
**Target:** Sole Platform Administrator (`fulcrumindia1@gmail.com`)

---

## 1. Executive Summary & Core Principles

A fundamental requirement of enterprise data governance is that **rolling back an application release or schema change must never destroy historical data, operational audit logs, or legal acceptances**.

Naive database rollbacks often contain destructive statements such as:
```sql
-- DANGEROUS / REJECTED ANTI-PATTERN:
DROP TABLE public.account_lifecycle_log;
ALTER TABLE public.profiles DROP COLUMN account_status;
```
If an application is rolled back after running in staging or production for even a single week, executing the naive script above would permanently erase every suspension, archival, restoration, and deletion audit record created during that period.

To eliminate this risk, Fulcrum employs an **Expand-and-Contract Migration Strategy with Forward Recovery**.

---

## 2. The Expand-and-Contract Pattern for Migration 009

Migration 009 is engineered to be **100% additive, non-breaking, and backwards-compatible**:

```
+---------------------------------------------------------------------------------+
| PHASE 1: EXPAND (Migration 009 Applied)                                         |
| - New columns added with safe defaults (account_status = 'ACTIVE', hold = FALSE)|
| - account_lifecycle_log created with append-only RLS                            |
| - ON DELETE CASCADE replaced with ON DELETE RESTRICT on profiles.id             |
| - OLD APPLICATION CODE CONTINUES WORKING WITHOUT ERROR                          |
+---------------------------------------------------------------------------------+
                                       |
                                       v
+---------------------------------------------------------------------------------+
| PHASE 2: RUNTIME ENFORCEMENT                                                    |
| - New application version enforces account lifecycle gates                      |
| - Admin uses the new Tab 13 (Account Lifecycle & Archive)                        |
| - Audit logs record all lifecycle events                                        |
+---------------------------------------------------------------------------------+
                                       |
         +-----------------------------+-----------------------------+
         | (Normal Operations Continue)|                             | (Application Rollback Required)
         v                             v                             v
[ Next Milestone: Contract ]                                [ INERT FORWARD RECOVERY ]
- Deprecate legacy profiles.is_active                        - Revert git release to prior commit
  after 90 days of stability.                               - LEAVE DATABASE SCHEMA INTACT
                                                             - Older app ignores new columns
                                                             - Audit logs remain 100% preserved
```

---

## 3. Forward Recovery Runbook: Application Rollback Without Data Loss

If an application defect requires rolling back the Streamlit codebase from `dev/account-lifecycle-and-archive` to a prior release:

### Step 1: Revert Application Code Only
- Revert the Git deployment to the previous stable release commit.
- **DO NOT execute any `DROP TABLE` or `DROP COLUMN` SQL statements.**

### Step 2: Database Remains in Expand State
- The additions from Migration 009 are strictly additive:
  - `profiles.account_status` defaults to `'ACTIVE'`
  - `profiles.legal_hold` defaults to `FALSE`
  - `account_lifecycle_log` is an isolated table
- The prior application code does not read or write these columns; it continues reading `profiles.is_active` and `user_roles`. Because all new columns are nullable or have valid defaults, prior application code functions without any SQL errors or schema conflicts.

### Step 3: Audit Trail Preservation
- Every action taken while Migration 009 was active remains safely stored in `public.account_lifecycle_log`.
- When the application is redeployed after fixes, all historical lifecycle records are instantly available without data reconstruction or manual re-entry.

---

## 4. Auth User Cascade Disaster Recovery & Protection

### The Cascade Threat (Mitigated by Migration 009)
In legacy schemas:
```sql
ALTER TABLE public.profiles ADD CONSTRAINT profiles_id_fkey 
FOREIGN KEY (id) REFERENCES auth.users(id) ON DELETE CASCADE;
```
If an operator deletes an identity in the Supabase Auth dashboard, PostgreSQL triggers a recursive cascade that deletes:
1. `public.profiles`
2. `public.journeys`
3. `public.relationships`
4. `public.scheme_releases`
5. `public.help_requests`

### Migration 009 Protection (`ON DELETE RESTRICT`)
Migration 009 executes:
```sql
ALTER TABLE public.profiles
    DROP CONSTRAINT IF EXISTS profiles_id_fkey,
    ADD CONSTRAINT profiles_id_fkey 
    FOREIGN KEY (id) REFERENCES auth.users(id) ON DELETE RESTRICT;
```
Now, if an administrator or script attempts to delete a Supabase Auth user who has associated operational records, PostgreSQL **aborts the transaction immediately** with a foreign key violation:
`ERROR: update or delete on table "users" violates foreign key constraint "profiles_id_fkey" on table "profiles"`.

### Data Recovery Runbook: Recovering an Accidental Auth Deletion
If an Auth user is deleted in an unmigrated environment:
1. The profile record retains its original UUID in historical logs.
2. The user is recreated in Supabase Auth with the exact same UUID:
   ```python
   # Re-create Auth User under preserved UUID
   admin_client.auth.admin.create_user({
       "uid": preserved_uuid,
       "email": original_email,
       "email_confirm": True
   })
   ```
3. All foreign key relationships reconnect seamlessly because PostgreSQL references the UUID, restoring full account integrity without data loss.

---

## 5. Schema Drift Verification & Health Check Procedure

Before and after applying any migration in staging or production, execute this read-only diagnostic query to confirm zero drift:

```sql
-- Read-Only Schema Health Check
SELECT 
    column_name, 
    data_type, 
    column_default, 
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'public' 
  AND table_name = 'profiles'
  AND column_name IN (
      'account_status', 
      'legal_hold', 
      'lifecycle_reason', 
      'status_updated_at', 
      'status_updated_by', 
      'deletion_requested_at', 
      'deletion_scheduled_for'
  )
ORDER BY column_name;
```

Expected result: 7 rows returned, all matching specification defaults.

