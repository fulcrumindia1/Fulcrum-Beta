# NEW SUPABASE INSTANCE SETUP & CONFIGURATION CHECKLIST
**Platform:** Fulcrum India (Cluster A / Fulcrum-Beta)  
**Target Architecture:** Fresh Supabase Project (Clean Slate, Zero Legacy Records)  
**Server Target:** Hostinger KVM 2 VPS (Ubuntu 24.04.5 LTS, 8 GB RAM)  
**Authoritative Production Admin:** `fulcrumindia1@gmail.com`  
**Date:** 2026-11-10  

---

## 1. Executive Summary & Objective

This checklist provides the exact, end-to-end procedure for initializing a **completely fresh Supabase cloud project** for Fulcrum-Beta. 

Because this is a **clean-slate deployment**, no historical user accounts or legacy database records will be imported. The only data seeded into this fresh database is the **canonical catalogue of 179 government schemes** and the mandatory **legal templates** (Terms of Service and Master Mutual NDA).

---

## 2. Project Provisioning & Region Settings

1. **Log in to Supabase Management Console:**  
   Navigate to [https://supabase.com/dashboard](https://supabase.com/dashboard) and log in.
2. **Create New Project:**
   - **Organization:** Select your production organization.
   - **Name:** `fulcrum-production` (or your preferred name).
   - **Database Password:** Generate a secure, 32+ character random password. Store this in your secure password manager.
   - **Region:** **South Asia (Mumbai) - `ap-south-1`** *(Crucial for sub-40ms latency to Tamil Nadu users).*
   - **Pricing Plan:** Pro tier recommended for production connection pooling and backup retention.
3. **Database Timezone Configuration:**
   - Open **Settings -> Database**.
   - Ensure timezone is set to `Asia/Kolkata` (UTC+05:30) or UTC (Fulcrum stores all timestamps in UTC with ISO 8601).

---

## 3. Authentication & Security Configuration

Navigate to **Authentication -> URL Configuration**:

| Setting | Value | Purpose |
| :--- | :--- | :--- |
| **Site URL** | `https://app.fulcrumindia.online` | Canonical redirect target for email auth links. |
| **Redirect URLs** | `https://app.fulcrumindia.online/**`<br>`http://localhost:8501/**` *(optional staging)* | Whitelisted callback destinations. |

Navigate to **Authentication -> Providers -> Email**:
- **Enable Email provider:** `ON`
- **Confirm email:** Recommended `ON` for production security.
- **Secure password requirements:** Minimum 8 characters.

---

## 4. Database Schema Migration Sequence (SQL Editor)

Open the **SQL Editor** in the Supabase Dashboard and execute the SQL migration scripts located in `FULCRUM_FRESH_DEPLOYMENT/migrations/` and `FULCRUM_FRESH_DEPLOYMENT/seed/` in the exact chronological order below.

> [!IMPORTANT]
> Each script is 100% idempotent and transactional. Run each script in a separate SQL Editor query tab.

### Step 4.1: Master Base Schema (`migrations/000_complete_beta_setup.sql`)
- **Action:** Open `migrations/000_complete_beta_setup.sql`, copy all contents into the SQL Editor, and click **Run**.
- **What this creates:**
  - Extensions: `uuid-ossp`, `pgcrypto`.
  - Core Tables: `profiles`, `user_roles`, `legal_documents`, `legal_acceptances`, `relationships`, `journeys`, `journey_events`, `schemes`, `help_requests`, `complaints`, `sme_conflicts`, `case_discussions`, `notifications`, `mentor_inactivity`, `aspirant_photos`.
  - Functions: `public.is_admin()`, `public.handle_new_user()`, `public.record_account_audit_event()`.
  - Auth Trigger: Automatically registers new Auth signups into `public.profiles` as `aspirant`.
  - Storage Buckets: Initializes `aspirant-profile-photos`.
  - Row Level Security: Enables RLS on all tables and installs strict multi-tenant policies.

### Step 4.2: Photo Security & Performance Indexes (`migrations/008_single_admin_lock_professional_photos_and_workflow_columns.sql`)
- **Action:** Open `migrations/008_single_admin_lock_professional_photos_and_workflow_columns.sql`, copy contents into SQL Editor, and click **Run**.
- **What this creates:**
  - Table: `public.professional_photos` with private RLS policies.
  - Storage Bucket: Initializes `professional-profile-photos`.
  - Columns: Adds `release_status`, `released_at`, `released_by` to schemes table for formal release tracking.
  - Composite Indexes: Adds high-performance lookup indexes for journeys, consultations, and photo signed URL queries.

### Step 4.3: Account Lifecycle, Immutable Audit & Cascade Immunity (`migrations/009_account_lifecycle_and_archive.sql`)
- **Action:** Open `migrations/009_account_lifecycle_and_archive.sql`, copy contents into SQL Editor, and click **Run**.
- **What this creates:**
  - **Auth Cascade Immunity:** Replaces `ON DELETE CASCADE` on `profiles.id` with `ON DELETE RESTRICT`. Auth deletions can never wipe historical journeys or legal acceptances.
  - **Account Lifecycle States:** `account_status` (`ACTIVE`, `TEMPORARILY_SUSPENDED`, `ARCHIVED`, `PENDING_DELETION`), `lifecycle_stage`, `legal_hold`.
  - **Triple-Layer Immutable Audit Log:** Table `account_lifecycle_audit_log` with SQL triggers and restrictive RLS forbidding `UPDATE`, `DELETE`, or `TRUNCATE`.

### Step 4.4: Canonical 179 Government Schemes (`seed/seed_179_schemes_idempotent.sql`)
- **Action:** Open `seed/seed_179_schemes_idempotent.sql`, copy contents into SQL Editor, and click **Run**.
- **What this creates:**
  - Inserts all **179 canonical government schemes** with complete eligibility rules, sector tags, budget ranges, and application URLs.
  - Uses `ON CONFLICT (id) DO UPDATE SET ...` to guarantee exact idempotency.

---

## 5. Storage Buckets Verification

Navigate to **Storage -> Buckets** in the Supabase Dashboard:

| Bucket Name | Privacy | Size Limit | Allowed MIME Types | Required Policies |
| :--- | :--- | :--- | :--- | :--- |
| `aspirant-profile-photos` | **Private** | 5 MB | `image/png`, `image/jpeg`, `image/webp` | Aspirant manage own folder; Admin/Mentors read |
| `professional-profile-photos` | **Private** | 5 MB | `image/png`, `image/jpeg`, `image/webp` | Owner manage own; Authenticated read |

*(If not automatically created by migration scripts, click **New Bucket**, name exactly as above, toggle **Public Bucket = OFF**, and save).*

---

## 6. Pre-Flight SQL Verification Queries

Run the following verification script in the SQL Editor to confirm that the fresh database is 100% operational:

```sql
-- 1. Verify Scheme Catalogue count (MUST be exactly 179)
SELECT 
    COUNT(*) AS total_schemes,
    COUNT(*) FILTER (WHERE category IS NOT NULL) AS categorized_schemes
FROM public.schemes;

-- 2. Verify Legal Documents are seeded
SELECT id, title, version, is_active FROM public.legal_documents;

-- 3. Verify RLS is enabled on all public tables (should return 0 rows with rowsecurity = false)
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public' AND rowsecurity = FALSE;

-- 4. Verify Storage Buckets exist
SELECT id, name, public, file_size_limit FROM storage.buckets;
```

**Expected Results:**
- `total_schemes`: **179**
- `legal_documents`: 2 rows (`terms_and_conditions`, `master_mutual_nda`)
- Unprotected tables: **0**
- Storage Buckets: 2 rows (`aspirant-profile-photos`, `professional-profile-photos`)

---

## 7. Extracting API Keys for VPS `.env`

Navigate to **Project Settings -> API**:
1. Copy **Project URL**: (e.g., `https://xxxxxxxxxxxxxxxxxxxx.supabase.co`)
2. Copy **Project API Keys**:
   - `anon` / `public`: (Publishable key)
   - `service_role` / `secret`: (Secret service key — Keep strictly confidential!)

These keys will be configured directly in `/opt/fulcrum/.env` on the VPS as described in `WINSCP_FRESH_DEPLOYMENT_GUIDE.md`.

