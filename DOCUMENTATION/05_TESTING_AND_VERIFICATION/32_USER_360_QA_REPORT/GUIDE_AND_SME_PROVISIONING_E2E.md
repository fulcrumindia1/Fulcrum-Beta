# Guide and SME Provisioning E2E Audit (`FUL-32-E2E-0002` – `0007`)

**Deployed Code:** Commit `988127b` (`services/auth.py`, `services/roles.py`, `views/admin.py`, `views/legal_ui.py`)  
**Provisioned Synthetic Accounts:** Guides `D, H, Q, T` (Tab 2); SMEs `P, U` (Tab 3); Existing-Aspirant Role Grants (`22` professional grants via Tab 7)

---

## 1. What Was Fixed in `988127b` vs What Still Fails Live

1. **`user_roles` Creation Fix Confirmed Deployed:** Prior bug (Auth/profile created without `user_roles`) is fixed in `admin_create_mentor()` (`988127b`):
   - Admin Tab 2 (`D, H, Q, T`) created exactly `1` Auth UUID, `1` `profiles` row, and `1` `user_roles` row (`role='guide'`, `status='pending_nda'`).
   - Admin Tab 3 (`P, U`) created exactly `1` Auth UUID, `1` `profiles` row, and `1` `user_roles` row (`role='sme'`, `status='pending_nda'`).
   - Immediately after provisioning, mentors appeared as `PENDING NDA` in Tab 2/3 rosters and **remained excluded** from Admin Tab 4 Mentor Assignments (`EXP-M7` confirmed `AA` in `pending_nda` could not be assigned).
2. **`DEF-32-003` (P0 Live Blocker — Rerun Temp Password Regeneration):**
   - **Location:** `views/admin.py:532-533` (Guide provisioning) and `views/admin.py:676-677` (SME provisioning).
   - **Root Cause:** `secrets.token_urlsafe(12)` runs bare on every Streamlit script rerun without `st.session_state` caching before `st.form` submission. When the Admin clicks `Provision Guide` / `Provision SME`, Streamlit reruns the script and displays/generates a different password than the Auth user received (or vice versa).
   - **Observed Browser Proof (`run_02_pilot`, `Batch A1`):** Provisioned accounts `D`, `P`, and `H` all failed first browser login with `"Invalid login credentials"` using the displayed password until QA synchronized Supabase Auth passwords to unblock personal browser onboarding of `D, P, H, Q, T, U`.
3. **SME District Default Quirk (`Tab 3`):**
   - `views/admin.py` Tab 3 `Provision New SME Account` defaults `Location / District` to `"Madurai"`, causing `U` to initially save `"Madurai"` until manually updated to `"Chennai"` in `U`'s `My Profile` Tab 3 (`batch_c1_part2_report.json`).
4. **Admin Edit & Audit Limitations (`Tab 2 & Tab 3`):**
   - Admin Tabs 2 and 3 allow uploading/deleting private mentor headshots, **but provide no Admin edit form** to update an existing Guide or SME's bio, district, specialization, or phone (`DEF-32-008`).

---

## 2. Step-by-Step Mentor Onboarding Verification (After Temp PW Sync)

1. **First-Login Password Gate (`D, P, H, Q, T, U`):**
   - Logged into `https://app.fulcrumindia.online/` -> Forced into first-login password change gate (`temp_password_issued: true` -> `false`).
   - **Observed Mismatch (`DEF-32-009`):** Gate accepted 6-character password on UI (`app.py:1189`, `len(np1) < 6`), then rejected submission in backend (`services/auth.py:889`: `"Password must be at least 8 characters long."`). Cleanly accepted a compliant 12-character synthetic test password.
2. **Terms & Master Dual NDA Acceptance:**
   - Every mentor personally accepted Platform Terms & Conditions and Master Dual NDA (`nda_dual`, phrase `"I ACCEPT"`).
   - **Pre-NDA Assignment Block (`Batch A2`):** Before `A` signed NDA, Admin Tab 7 showed `"🔒 Awaiting User Signature"` (disabled), preventing Admin bypass (`tab7_A_awaiting_signature`).
3. **Role Activation & Cross-Dashboard Visibility (`pilot_finish_results.json`):**
   - Role status transitioned `pending_nda -> active`; `D` and `P` appeared in Admin Tab 4 and were assigned to `F` (`D` Guide, `P` SME).
   - `F` (`My Mentors`) immediately displayed `D` and `P`; `D` (`My Aspirants`) and `P` (`My Assigned Cases`) immediately displayed `F`; notifications delivered (`F: 2`, `D: 1`, `P: 1`).
4. **Negative Checks & Existing-Aspirant Promotion:**
   - Duplicate email rejection, empty required field guards, and non-Admin exclusion (`fulcrumindia1@gmail.com` omitted from Tab 7: `ug=0, um=0`) passed.
   - Promoting existing Aspirants (`A, B, C, E, G, I, J, K, M, N, S, W, Y, Z, AB, AD, AE`) via Admin Tab 7 granted new `user_roles` rows **reusing existing Auth UUIDs** (`37` total DB profiles = `5` real + `32` QA, zero duplicate Auth users).
5. **Dual-Side Cross-Role `profile_data` Observation (`U`):**
   - Admin-provisioned mentor keys (`expertise`, `bio`, `industry`) on `T` and `U` were **wiped** when `T` and `U` subsequently saved their Aspirant 5-section Venture Profile (`DEF-32-006`). When `U` opened SME Tab 3 (`My Profile`) to fix district to `Chennai`, submission failed with `"Please fill in your name and specialization domain."` until `expertise` was re-entered; afterward, saving SME Tab 3 preserved all 8 keys (`assistance_need`, `bio`, `business`, `demographics`, `expertise`, `industry`, `personal`, `professional`).
