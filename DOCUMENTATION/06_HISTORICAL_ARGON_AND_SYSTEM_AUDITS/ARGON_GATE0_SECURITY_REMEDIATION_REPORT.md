# FULCRUM-INDIA: AGY ARGON — GATE 0 SECURITY REMEDIATION REPORT

## 1. Executive Summary

- **Remediation Phase**: Phase 0 (Security Containment & Code Hardening — Development & Staging Only).
- **Target Branch**: `security/phase0-containment` (branched from `main`).
- **Production Status**: **ZERO live production changes.** No live production SQL executed, zero live accounts modified or deleted, and no code pushed to production auto-deployment.
- **Test Evidence**: **94 of 94 tests passing (100% green)**, including all 79 baseline regression tests and 15 dedicated negative security tests (SEC-01 through SEC-16).

---

## 2. Security Vulnerabilities Remediated

### Priority 0.1: Unauthenticated Account Takeover (CWE-640 / CWE-287) — RESOLVED
- **Vulnerability**: `services/auth.py:complete_password_reset` previously allowed unauthenticated password overrides by calling `admin_client.auth.admin.update_user_by_id()` with only a target email address. A bypass button in `views/login.py` allowed rendering the password reset form without an email verification token.
- **Remediation**:
  1. Completely eliminated the unauthenticated Admin API backdoor in `services/auth.py`.
  2. Enforced that Supabase mode strictly requires a verified recovery session token from an authentic Supabase Auth password reset email.
  3. Enforced minimum password length of 8 characters.
  4. Added explicit protection for the single Platform Administrator (`fulcrumindia1@gmail.com`), rejecting all public self-serve reset attempts.
  5. Enforced caller session verification in `complete_first_login_password_change`.
  6. Hardened `views/login.py` to prevent opening the recovery form without a valid recovery token.

### Priority 0.2: Credential Exposure & Secret Containment — RESOLVED
- **Vulnerability**: The deployment archive `fulcrum_deploy.tar.gz` contained historical environment settings and was tracked in git.
- **Remediation**:
  1. Purged `fulcrum_deploy.tar.gz` from git tracking and deleted it from disk.
  2. Updated `.gitignore` to prevent any archives (`*.tar.gz`, `*.tgz`, `*.zip`, `*.dump`) or `.env*` files from being staged or committed.
  3. Created `ARGON_GATE0_SECRET_ROTATION_OWNER_CHECKLIST.md` providing step-by-step instructions for the owner to rotate credentials in the Supabase Dashboard and Streamlit Cloud settings without exposing secrets.

### Priority 0.3: Protection of Single Admin Invariant & Role Separation — RESOLVED
- **Vulnerability**: Invariant 1 dictates exactly ONE Platform Administrator (`fulcrumindia1@gmail.com`). Prior code contained references to legacy roles (`district_admin`, `operational_admin`) and lacked strict exclusion of the Admin from ordinary mentor/aspirant candidate dropdowns.
- **Remediation**:
  1. Purged references to `district_admin` and `operational_admin` in `services/external_contact.py` and `services/collaboration.py`.
  2. Hardened `services/roles.py:grant_role` to enforce that only `aspirant`, `guide`, and `sme` are grantable (`VALID_GRANTABLE_ROLES`). Attempting to grant `admin` is strictly rejected.
  3. Hardened `services/roles.py:list_active_profiles_for_role` to guarantee that the Platform Administrator is never returned in ordinary candidate lists.

### Priority 0.4: Private Case Discussions & Fail-Open Elimination — RESOLVED
- **Vulnerability**: `services/collaboration.py` previously accepted caller-supplied `requesting_role: str = "aspirant"` to filter private advisory notes, allowing parameter tampering to view confidential notes.
- **Remediation**:
  1. Added `viewer_id` resolution from verified session context in `list_case_messages`.
  2. Verified active case assignment: only Platform Admin or mentors actively assigned to the entrepreneur with an accepted NDA can view private notes (`is_private_mentor_note = True`).
  3. Defense-in-depth: if unauthorized, private notes are filtered out at the Supabase query level, local DB query level, and via post-processing list filtering.
  4. In `services/profiles.py:update_aspirant_profile`: caller identity is strictly validated, and cross-user updates by unauthorized actors are rejected.

### Priority 0.5: Fail-Closed Photo Operations & Access Control — RESOLVED
- **Vulnerability**: `services/aspirant_photos.py:upload_aspirant_photo` previously masked Supabase storage upload failures by writing to local SQLite and returning `True` with a warning. Streamlit Cloud's ephemeral filesystem caused uploaded photos to vanish on container reboot. Furthermore, `get_aspirant_photo` skipped authorization when `viewer_id` was `None`.
- **Remediation**:
  1. In `get_aspirant_photo`: strictly fail closed if `viewer_id` is missing in Supabase mode (SEC-05).
  2. In `upload_aspirant_photo`: when `DATA_BACKEND=supabase`, if cloud storage fails, the routine returns `False, "Failed to persist profile photo to cloud storage"`. Silent fallback to local SQLite is completely eliminated.
  3. Retained 150 KB compressed WebP cap and EXIF sanitization.

### Priority 0.6: Elimination of Silent Production Fallbacks — RESOLVED
- **Vulnerability**: When running in Supabase mode, failures in `services/roles.py` (`grant_role`, `activate_role`, `revoke_role`) and `services/legal.py` (`record_legal_acceptance`) previously caught exceptions and fell back to local SQLite while reporting success.
- **Remediation**:
  1. When `DATA_BACKEND=supabase`, any failure in Supabase returns `False, error_message`.
  2. Local SQLite is active only when `DATA_BACKEND=sqlite` is explicitly configured.

### Priority 0.7: Secure Mentor Provisioning — RESOLVED
- **Vulnerability**: Admin account provisioning forms in `views/admin.py` used hardcoded passwords (`"Guide@123"`, `"Sme@123"`), and success banners exposed plaintext credentials in persistent UI toasts.
- **Remediation**:
  1. Replaced hardcoded default passwords with cryptographically secure random passwords generated via `secrets.token_urlsafe(12)`.
  2. Default temporary password in `services/auth.py:admin_create_mentor` now generates secure random tokens.
  3. Suppressed credential exposure in persistent toasts.

---

## 3. Issue Classification Matrix

| Issue ID | Description | Severity | Status | Verification |
| :--- | :--- | :---: | :---: | :--- |
| **P0-ATO** | Unauthenticated password override via Admin API | P0 | **RESOLVED & TESTED** | `test_sec_01`, `test_sec_02`, `test_sec_03` |
| **P0-ARCH** | Tracked deployment archive with secrets | P0 | **RESOLVED & TESTED** | Purged from git; `.gitignore` updated |
| **P0-ADMIN**| Admin account protection & single admin invariant | P0 | **RESOLVED & TESTED** | `test_sec_12_13`, `test_sec_14` |
| **P0-NOTE** | Private case notes parameter tampering | P0 | **RESOLVED & TESTED** | `test_sec_08`, `test_sec_09`, `test_sec_10`, `test_sec_11` |
| **P0-PHOTO**| Photo upload false success & unauthenticated view | P0 | **RESOLVED & TESTED** | `test_sec_05`, `test_sec_06`, `test_sec_07`, `test_sec_16` |
| **P1-SQL** | Proposed Migration 008 destructive rollback | P1 | **PROPOSAL REVISED** | `ARGON_MIGRATION_008_REVISED_PROPOSAL.sql` |
| **P1-SECR** | Live credential rotation in Supabase / Streamlit | P1 | **AWAITING OWNER ACTION** | `ARGON_GATE0_SECRET_ROTATION_OWNER_CHECKLIST.md` |
| **P2-UX** | Guide/SME headshots in 360° dashboard views | P2 | **PHASE 1 SCOPE** | Awaiting Gate 1 approval |
