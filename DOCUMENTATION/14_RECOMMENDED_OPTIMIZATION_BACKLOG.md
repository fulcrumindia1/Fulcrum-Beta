# 14 — RECOMMENDED OPTIMIZATION BACKLOG
**Phase L Deliverable | P0–P3 Prioritized Product & Infrastructure Backlog**

---

## Priority P0: Critical Usability & Performance Remediation (**COMPLETED & VERIFIED**)

| Backlog ID | Area | File Location | Fix Description | Impact | Risk |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **`BKL-04`** | Performance | [`views/admin.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/admin.py), [`views/aspirant.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/aspirant.py) | Lazy Tab Evaluation (`if is_tab_active()`) | `7.2s` $\rightarrow$ `0.77s` | Low |
| **`BKL-05`** | Performance | [`services/roles.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/roles.py), [`services/profiles.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/profiles.py) | Batch N+1 query elimination in `list_users_with_multi_roles` | `21.5s` $\rightarrow$ `0.34s` | Low |
| **`BKL-01`** | Workflows | [`views/sme.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/sme.py), [`services/help_requests.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/help_requests.py) | SME consultation reply lockout repair | Unlocks SME replies | Low |
| **`BKL-02`** | Security | [`views/aspirant.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/aspirant.py), [`views/admin.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/admin.py) | Pass explicit `viewer_id` & `viewer_role` to photo fetcher | Restores headshots | Very Low |
| **`BKL-03`** | UI/UX | [`views/admin.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/admin.py) | Indent subtabs inside `with subtab_inq:` | Fixes layout bleed | Very Low |

---

## Priority P1: Capacity & Container Optimization (**APPROVED FOR DEPLOYMENT**)

| Backlog ID | Area | File Location | Proposed Optimization | Expected Benefit | Risk |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **`BKL-20`** | Infrastructure | `docker-compose.yml` | Increase `fulcrum-app` RAM from `1800M` to `3072M` | Eliminates OOM risk during concurrent PDF export | Very Low |
| **`BKL-21`** | Infrastructure | `docker-compose.yml` | Adjust CPU quota from `1.5` to `1.75` | Reduces p95 latency under 75+ user load | Very Low |
| **`BKL-22`** | Database | `supabase_setup.sql` | Add composite indexes on `relationships` and `help_requests` | Speeds up triage queries by 30% | Low |

---

## Priority P2: Medium-Term Scale Enhancements (Pre-Scale Beyond 2,000 Users)

| Backlog ID | Area | File Location | Proposed Optimization | Expected Benefit | Risk |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **`BKL-23`** | Database | [`services/profiles.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/profiles.py), [`views/admin.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/admin.py) | Server-side PostgREST range pagination (`limit 50 offset X`) | Caps memory usage at 10,000 users | Low |
| **`BKL-24`** | Performance | [`services/dossier_pdf.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/dossier_pdf.py) | Bounded asynchronous queue for PDF generation | Prevents CPU contention during batch export | Medium |
