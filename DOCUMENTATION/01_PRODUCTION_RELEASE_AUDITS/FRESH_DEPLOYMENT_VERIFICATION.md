# FRESH DEPLOYMENT VERIFICATION & ACCEPTANCE TESTING PROTOCOL
**Platform:** Fulcrum India (Cluster A / Fulcrum-Beta)  
**Target:** Hostinger KVM 2 VPS & Fresh Supabase Cloud Instance  
**Testing Scope:** End-to-End Smoke, Security Boundaries, Concurrency & Performance  
**Date:** 2026-11-10  

---

## 1. Verification Strategy & Objectives

This verification protocol establishes the criteria for signing off on the clean-slate deployment of Fulcrum-Beta. 

Because this is a **fresh database deployment**, the acceptance test confirms that:
1. The 179 canonical schemes and legal templates are present and intact.
2. The sole platform admin (`fulcrumindia1@gmail.com`) holds full command and control.
3. User registrations, role promotions, and caseload assignments operate without legacy baggage.
4. The 5 GB memory ceiling and single-concurrency PDF worker maintain sub-second UI responsiveness.

---

## 2. Pre-Flight Infrastructure Checks (CLI)

Run these checks on the VPS terminal before testing the web browser:

```bash
# 1. Check Streamlit local healthcheck
docker compose exec -T fulcrum curl -s http://localhost:8501/_stcore/health
# Expected: ok

# 2. Check Supabase connection and 179 schemes
docker compose exec -T fulcrum python -c "
from services.auth import get_supabase_client, get_supabase_admin_client
sb = get_supabase_admin_client() or get_supabase_client()
schemes_cnt = sb.table('schemes').select('id', count='exact').execute().count
profiles_cnt = sb.table('profiles').select('id', count='exact').execute().count
print(f'Supabase Connected! Schemes: {schemes_cnt}, Profiles: {profiles_cnt}')
assert schemes_cnt == 179, f'Expected 179 schemes, got {schemes_cnt}'
"

# 3. Check Caddy reverse proxy HTTPS status
curl -I https://app.fulcrumindia.online
# Expected: HTTP/2 200
```

---

## 3. End-to-End Acceptance Test Matrix (Web Browser)

Open `https://app.fulcrumindia.online` in a clean browser window (or incognito mode):

### Test 1: Sole Administrator Command Center Smoke Test
- **Action:** Sign in with `fulcrumindia1@gmail.com` and password.
- **Pass Criteria:**
  - Landed in the **Admin Command Center**.
  - Header displays: `Role: Admin | Logged in as: fulcrumindia1@gmail.com`.
  - Dashboard tab displays aggregated metric cards instantly:
    - Aspirants: `0` (or current count)
    - Active Guides: `0`
    - Active SMEs: `0`
    - Available Schemes: `179`
    - Pending Directives: `0`
  - Verify all 13 tabs switch cleanly without execution errors:
    1. Dashboard & Metrics
    2. Entrepreneurs Directory (shows "No records found" or paginated table)
    3. Guide Management
    4. SME Management
    5. Mentor Assignments
    6. Multi-Role Grants
    7. Legal Terms & NDA
    8. System Governance & Directives
    9. Scheme Reviews
    10. SME Conflicts & Direct Access
    11. Account Lifecycle & Archive
    12. Notifications & Audit Log
    13. System Diagnostics

### Test 2: Aspirant Onboarding & Legal Terms Acceptance
- **Action:** In a second incognito browser window, click **Sign Up** and register as a new Aspirant (e.g. `test_aspirant_01@fulcrum.org`).
- **Pass Criteria:**
  - Registration succeeds and account is created.
  - User is prompted with the **Terms of Service** dialogue before platform access.
  - Accepting terms records a cryptographic audit stamp in `public.legal_acceptances`.
  - Profile setup wizard allows entering enterprise name, district, sector, and uploading an avatar image.
  - Avatar image is stored in private bucket `aspirant-profile-photos`.

### Test 3: Multi-Role Elevation & Master NDA Clearance
- **Action:** Switch to the Admin window -> Navigate to **Multi-Role Grants** tab.
- **Pass Criteria:**
  - The new test user appears in the user list.
  - Admin grants the role `guide` to the user.
  - User's status transitions to `pending_nda`.
  - When the user logs in, they are gated by the **Master Mutual NDA**.
  - Once signed, the user's Guide role transitions to `active`.
  - The user can switch roles seamlessly between Aspirant and Guide via the top-bar role selector.

### Test 4: Caseload Assignment & Privacy Boundary
- **Action:** In Admin window -> **Mentor Assignments** tab:
  - Assign the Guide to the Aspirant.
- **Pass Criteria:**
  - The Guide logs in and can view the assigned Aspirant's dossier and photo.
  - Unassigned Guides/SMEs **cannot** view or query this Aspirant's private notes or photos (enforced by Supabase RLS).

### Test 5: AI Scheme Matching Engine
- **Action:** In Aspirant window -> Navigate to **Government Schemes** tab.
- **Pass Criteria:**
  - Complete catalogue of **179 schemes** is searchable and filterable.
  - Enter sector (e.g. "Agriculture") and state ("Tamil Nadu").
  - Matching engine computes percentage eligibility and displays criteria breakdown instantly (<200ms).

### Test 6: PDF Dossier Export & Resource Stability
- **Action:** In Guide or Admin window -> Open Aspirant Journey -> Click **Generate Official PDF Dossier**.
- **Pass Criteria:**
  - Request is queued into the bounded Chromium worker.
  - PDF renders cleanly with official typography, headers, and metadata in under 6 seconds.
  - Download completes successfully.
  - Run `docker stats --no-stream fulcrum-app` during generation:
    - Container memory usage increases by ~300 MB then drops back.
    - Container does NOT crash or exceed the 5 GB memory ceiling.

### Test 7: Negative Security & Role Revocation Check
- **Action:** Admin navigates to **Multi-Role Grants** -> Revokes the Guide role.
- **Pass Criteria:**
  - Role status is set to `revoked`.
  - The user immediately loses Guide view access on their next interaction.
  - Supabase-to-SQLite fallback is NOT triggered; strict error message is returned if unauthorized access is attempted.

---

## 4. Acceptance Sign-Off Criteria

The deployment is approved for general production release when:
- [x] All 7 acceptance tests above pass with zero exceptions.
- [x] Supabase RLS enforces multi-tenant boundaries on all 18 tables.
- [x] Caddy reverse proxy maintains valid SSL and zero HTTP 502 Bad Gateway responses.
- [x] Available host RAM remains strictly above 1,500 MB.

