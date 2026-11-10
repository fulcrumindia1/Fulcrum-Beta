# FULCRUM-INDIA: AGY ARGON — GATE 0 SUPABASE RLS VERIFICATION

## 1. Table-Level RLS Policy Verification

| Table Name | RLS Status | Verified Policy Names | Access Rules & Invariant Enforcement |
| :--- | :---: | :--- | :--- |
| **`public.profiles`** | **ENABLED** | `Admin full access`, `Users read all active profiles`, `Users update own profile` | Only Platform Admin (`fulcrumindia1@gmail.com`) or self-user can modify profile records. |
| **`public.user_roles`** | **ENABLED** | `Admin manages user roles`, `Users view own roles` | Non-admin users can view only their own role grants. Only Admin can insert/update/delete. |
| **`public.legal_acceptances`** | **ENABLED** | `Admin view all legal records`, `Users insert own acceptance`, `Users view own acceptances` | Tamper-proof audit log. Non-admin can only insert own acceptance; cannot update or delete past records. |
| **`public.aspirant_photos`** | **ENABLED** | `Admin full control aspirant photos`, `Aspirants manage own photo`, `Mentors view assigned aspirant photo` | Metadata is visible ONLY to owner, Admin, and assigned mentors who hold an active role and accepted NDA. |
| **`public.relationships`** | **ENABLED** | `Admin manages relationships`, `Assigned mentors view relationships`, `Aspirants view own relationship` | Caseload allocations are exclusive to Admin. Mentors see only relationships where their UUID is assigned. |
| **`public.case_discussions`**| **ENABLED** | `Participants view case discussions`, `Mentors view private notes`, `Authors create messages` | Aspirants cannot query records where `is_private_mentor_note = true`. |
| **`public.journeys`** | **ENABLED** | `Admin manages journeys`, `Aspirant views own journey`, `Assigned mentors view journey` | Isolated to the entrepreneur, Admin, and assigned mentors. |

---

## 2. Storage Bucket Policy Verification

### A. Bucket: `aspirant-profile-photos` (Existing, Inactive Anon Upload Fixed)

- **Access Level**: `public = false` (Strictly Private Bucket).
- **Hard Cap**: 5 MB upload limit, 150 KB stored WebP target.
- **Signed URL Expiry**: 300 seconds (short-lived HMAC signed tokens).
- **RLS Policies in `storage.objects`**:
  1. **Owner Access**: `(storage.foldername(name))[1] = auth.uid()::text` (Permitted to insert, select, delete own headshot).
  2. **Admin Access**: Verified `auth.jwt() ->> 'email' = 'fulcrumindia1@gmail.com'` (Full SELECT, INSERT, DELETE).
  3. **Assigned Mentor Access**:
     ```sql
     EXISTS (
         SELECT 1 FROM public.relationships r
         WHERE r.aspirant_id::text = (storage.foldername(name))[1]
           AND r.status = 'active'
           AND (r.guide_id = auth.uid() OR r.sme_id = auth.uid()
                OR r.guide_ids ? auth.uid()::text OR r.sme_ids ? auth.uid()::text)
           AND EXISTS (SELECT 1 FROM public.user_roles ur WHERE ur.user_id = auth.uid() AND ur.status = 'active')
           AND EXISTS (SELECT 1 FROM public.legal_acceptances la WHERE la.user_id = auth.uid() AND la.status = 'ACCEPTED')
     )
     ```

### B. Bucket: `professional-profile-photos` (Proposed in Migration 008)

- **Access Level**: `public = false` (Private Bucket).
- **Hard Stored Cap**: `file_size_limit = 153600` (150 KB strictly enforced by storage engine).
- **Allowed MIME Types**: `image/webp`, `image/png`, `image/jpeg`.
- **Status**: Proposed in `ARGON_MIGRATION_008_REVISED_PROPOSAL.sql`. Awaiting explicit owner approval.
