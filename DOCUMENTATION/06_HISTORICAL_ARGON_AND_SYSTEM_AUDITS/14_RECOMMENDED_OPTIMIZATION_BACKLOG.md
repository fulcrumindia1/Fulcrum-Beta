# 14 — RECOMMENDED OPTIMIZATION BACKLOG
**Phase L Deliverable | P0–P3 Prioritized Product & Infrastructure Backlog**

---

## Priority P0: Critical Usability, Security & Performance Remediation (**IMPLEMENTED ON STAGING BRANCH & VERIFIED**)

*These items were previously approved in [`ARGON_OWNER_DECISION_AND_APPROVAL_REGISTER.md`](file:///C:/Users/hp/.gemini/antigravity/brain/22e605d7-a862-4d23-bd2d-9491575ffa3a/ARGON_OWNER_DECISION_AND_APPROVAL_REGISTER.md) (`DEC-01` through `DEC-06`) and verified on `security/phase0-containment`:*

| Backlog ID | Area | File Location | Fix Description | Verified Impact | Risk | Approval Status |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| **`BKL-04`** | Performance | [`views/admin.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/admin.py), [`views/aspirant.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/aspirant.py), [`views/guide.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/guide.py), [`views/sme.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/sme.py) | Lazy Tab Evaluation (`if is_tab_active()`) | Warm tab switch `7.2s` $\rightarrow$ `0.4–0.8s` | Low | **Approved & Verified (`DEC-02`)** |
| **`BKL-05`** | Performance | [`services/roles.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/roles.py), [`services/profiles.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/profiles.py) | Batch N+1 query elimination in `list_users_with_multi_roles` | `21.5s` $\rightarrow$ `0.34s` (**62.4× faster**) | Low | **Approved & Verified (`DEC-02`)** |
| **`BKL-01`** | Workflows | [`views/sme.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/sme.py), [`services/help_requests.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/help_requests.py) | SME consultation reply lockout repair | Unlocks SME replies | Low | **Approved & Verified (`DEC-01`)** |
| **`BKL-02`** | Security | [`views/aspirant.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/aspirant.py), [`views/admin.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/admin.py) | Pass explicit `viewer_id` & `viewer_role` to photo fetcher | Restores headshots safely | Very Low | **Approved & Verified (`DEC-01`)** |
| **`BKL-03`** | UI/UX | [`views/admin.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/admin.py) | Indent subtabs inside `with subtab_inq:` | Fixes layout bleed | Very Low | **Approved & Verified (`DEC-01`)** |
| **`BKL-06`** | Security | [`services/cache.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/cache.py), [`views/guide.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/guide.py), [`views/sme.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/sme.py) | Cross-session role cache invalidation & active-role portal guard | Immediate mid-session role eviction | Very Low | **Approved & Verified (`DEC-02`)** |

---

## Priority P1: Container Capacity & Production Merge (**NOT APPROVED — AWAITING OWNER DECISION**)

| Backlog ID | Change Request ID | File Location | Proposed Optimization | Expected Benefit | Risk | Approval Status |
| :--- | :---: | :--- | :--- | :---: | :---: | :---: |
| **`BKL-20`** | **`CR-01`** | [`docker-compose.yml`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/docker-compose.yml) | Increase `fulcrum` container memory limit from `1800M` to `3072M` (`3.0 GiB`) and CPU limit from `1.5` to `1.75` | Adds `1.2 GiB` extra safety buffer for concurrent Chromium PDF exports while leaving `> 2.6 GiB` free host RAM | Very Low | **NOT APPROVED (Awaiting Owner Decision in `15`)** |
| **`BKL-21`** | **`CR-02`** | Branch `security/phase0-containment` $\rightarrow$ `main` | Merge verified security & performance remediation branch into production deployment branch | Deploys all 94/94 verified fixes to production | Low | **NOT APPROVED (Awaiting Owner Decision in `15`)** |

---

## Priority P2: Database Composite & GIN Indexing (**NOT APPROVED — AWAITING OWNER DECISION**)

| Backlog ID | Change Request ID | Target | Proposed Optimization | Expected Benefit | Risk | Approval Status |
| :--- | :---: | :--- | :--- | :---: | :---: | :---: |
| **`BKL-22`** | **`CR-03`** | Supabase PostgreSQL ([`10_DATABASE_QUERY_AND_INDEX_AUDIT.md`](file:///C:/Users/hp/.gemini/antigravity/brain/22e605d7-a862-4d23-bd2d-9491575ffa3a/10_DATABASE_QUERY_AND_INDEX_AUDIT.md)) | Apply idempotent composite & GIN indexes (`idx_profiles_role_is_active`, `idx_user_roles_user_id_status`, `idx_relationships_guide_ids_gin`, `idx_relationships_sme_ids_gin`, `idx_help_requests_guide_status_updated`, `idx_help_requests_sme_status_updated`) | Keeps multi-mentor JSONB and triage queries `< 10 ms` as database scales to `10,000+` rows | Low | **NOT APPROVED (Awaiting Owner Decision in `15`)** |

---

## Priority P3: Future High-Scale Enhancements (`> 2,000` Registered Users) (**NOT APPROVED — AWAITING OWNER DECISION**)

| Backlog ID | Area | File Location | Proposed Optimization | Expected Benefit | Risk | Approval Status |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| **`BKL-23`** | Database / UI | [`services/profiles.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/profiles.py), [`views/admin.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/admin.py) | PostgREST `.range(offset, offset + limit - 1)` server-side directory pagination | Caps Admin directory payload at `< 50 KB` even at `50,000` users | Low | **NOT APPROVED (Future Roadmap)** |
| **`BKL-24`** | Process Model | [`Dockerfile`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/Dockerfile) | Offload PDF generation to a dedicated worker queue if concurrent active users exceed `75` | Isolates main Streamlit event loop from subprocess spawning | Medium | **NOT APPROVED (Future Roadmap)** |
