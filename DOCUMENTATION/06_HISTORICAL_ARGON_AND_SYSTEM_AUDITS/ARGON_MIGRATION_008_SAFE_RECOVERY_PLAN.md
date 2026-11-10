# FULCRUM-INDIA: AGY ARGON — MIGRATION 008 SAFE RECOVERY PLAN

## 1. Executive Summary & Non-Destructive Principles

The previous draft of Migration 008 proposed a catastrophic rollback protocol:
`DROP TABLE IF EXISTS public.professional_photos CASCADE;`
`DELETE FROM storage.objects WHERE bucket_id = 'professional-profile-photos';`

In accordance with **Invariant 3 (Data Preservation)** and **Invariant 7 (Explicit Owner Approval & Non-Destructive Operations)**, destructive table dropping and storage deletion are strictly prohibited.

This Safe Recovery Plan establishes a zero-data-loss rollback procedure:
1. **Never drop tables**: Schema additions remain inert if deactivated.
2. **Never truncate or cascade delete storage objects**: Files remain protected in cold storage.
3. **Policy-level containment**: If rollback is triggered, containment is achieved by revoking public/authenticated RLS policies and restricting access exclusively to Platform Admin (`fulcrumindia1@gmail.com`).

---

## 2. Pre-Migration Safety Snapshot (Mandatory Before Any Execution)

Before executing any SQL in staging or production environments, the Platform Administrator must capture verified snapshots:

```bash
# 1. Capture schema and data snapshot of existing tables
pg_dump --host=<SUPABASE_DB_HOST> --port=5432 --username=postgres \
  --table=public.profiles \
  --table=public.user_roles \
  --table=public.legal_acceptances \
  --table=public.aspirant_photos \
  --table=public.relationships \
  --data-only --file=fulcrum_pre_008_backup_$(date +%Y%m%d_%H%M%S).sql

# 2. Verify snapshot integrity
ls -lh fulcrum_pre_008_backup_*.sql
```

---

## 3. Safe Rollback Execution (Zero Data Loss)

If any operational issue, regression, or permission lock occurs during or following the staging deployment of Migration 008, execute the following non-destructive containment script.

### Non-Destructive Containment Script (`008_safe_rollback_containment.sql`)

```sql
-- =============================================================================
-- SAFE ROLLBACK: CONTAINMENT WITHOUT DATA LOSS
-- =============================================================================

-- 1. Remove public and mentor access to professional_photos metadata
DROP POLICY IF EXISTS "Assigned entrepreneurs view mentor professional photo" ON public.professional_photos;
DROP POLICY IF EXISTS "Active NDA-compliant mentors manage own photo" ON public.professional_photos;

-- 2. Restrict professional_photos access strictly to Platform Admin
DROP POLICY IF EXISTS "Admin containment professional_photos" ON public.professional_photos;
CREATE POLICY "Admin containment professional_photos" ON public.professional_photos
    FOR ALL TO authenticated
    USING (
        auth.jwt() ->> 'email' = 'fulcrumindia1@gmail.com'
        OR EXISTS (
            SELECT 1 FROM public.profiles p 
            WHERE p.id = auth.uid() AND p.role = 'admin' AND p.email = 'fulcrumindia1@gmail.com'
        )
    );

-- 3. Lock down storage objects in professional-profile-photos bucket
DROP POLICY IF EXISTS "Assigned entrepreneurs read mentor professional photo object" ON storage.objects;
DROP POLICY IF EXISTS "Mentors upload own professional photo object" ON storage.objects;
DROP POLICY IF EXISTS "Mentors update and delete own professional photo object" ON storage.objects;

-- 4. Mark bucket as fully private and restricted to admin
UPDATE storage.buckets 
SET public = false
WHERE id = 'professional-profile-photos';

-- NOTE: All uploaded files and metadata records are PRESERVED in intact state.
-- No tables were dropped. No files were deleted.
```

---

## 4. Verification & Health Check Post-Recovery

1. **Verify Aspirant Photos Unaffected**:
   ```sql
   SELECT count(*) FROM public.aspirant_photos;
   ```
   Ensure count matches pre-migration baseline.
2. **Verify User Roles & NDA Acceptance Unaltered**:
   ```sql
   SELECT count(*) FROM public.user_roles;
   SELECT count(*) FROM public.legal_acceptances;
   ```
3. **Verify App Functionality**:
   Run full test suite:
   ```bash
   python -m pytest tests/ -q
   ```
   All tests must report green.
