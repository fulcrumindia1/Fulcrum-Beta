# Photo Upload and Storage Privacy Audit

**Test Cases:** `FUL-32-E2E-0095` – `0102` (`Batch C1` & `Final Snapshot`)  
**Evidence Files:** `scratch/run_06_batch_c1/batch_c1_report.json`, `scratch/synthetic_photos/`, `scratch/final_live_snapshot.json`

---

## 1. Upload Coverage & Bucket Counts (`final_live_snapshot.json`)

- **Supabase Storage Buckets (Preflight Verified):** Both `aspirant-profile-photos` and `professional-headshots` are strictly **private (`public = False`)**.
- **Aspirant Founder Photos (`aspirant-profile-photos`):** `10` total rows (`2` untouched baseline + `8` QA32: `A, B, F, G, L, T, U, AE`).
  - Verified on `A..AE` (lines `378-426` of `batch_c1_report.json`): each uploaded cleanly as `<uuid>/avatar_<hash>.webp` (`zero_journey_impact = True`, `journey_events` unaffected).
  - Delete & Re-upload verified on **`F`** (`avatar_ab898fb8.webp` after removal/re-upload; zero impact on `F`'s journey timeline).
- **Mentor Professional Headshots (`professional-headshots`):** `9` total rows (`1` untouched baseline + `8` QA32: `D, P, A, B, H, G, T, U`), stored cleanly as `<uuid>/headshot_<hash>.webp`.

---

## 2. Privacy, Ownership, Cross-Tenant & Storage Authorization Matrix (`Batch C1`)

| Probe Case | Target Photo | Viewer / Attempt | Expected Result | Observed HTTP / Service / UI Outcome | Verdict |
|---|---|---|---|---|---|
| **Raw Unauthenticated URL** | Private Storage object URL | Anonymous GET | HTTP `400`/`403` blocked | `raw_public_url_status = 400` | **PASS** |
| **Signed URL Retrieval** | Authorized founder photo | Signed time-limited URL | HTTP `200` image bytes | `signed_url_status = 200` | **PASS** |
| **Hybrid Bucket Separation** | Dual-role **`A`** | Own founder photo vs own Guide headshot | Stored separately across 2 private buckets | `A_bucket_separation = True` (`avatar_*.webp` in `aspirant-profile-photos` vs `headshot_*.webp` in `professional-headshots`) | **PASS** |
| **Shared Dual-Mentor Headshot** | Guide+SME **`H`** | `H` Guide Portal vs `H` SME Portal | Uses shared `professional-headshots` record cleanly | `H-SME-SHARED-CHECK renders_shared_headshot = True` | **PASS** |
| **Co-Guide #2 Photo Access** | `B`'s founder photo | Assigned Co-Guide `#2` **`E`** | Authorized read via `guide_ids` | `Co-Guide E allowed B = True` | **PASS** |
| **Unassigned Mentor Denied** | `F`'s & `A`'s founder photos | Unassigned Guides `Q -> F`, `X -> A` | Denied; no leakage | Both `Q->F` & `X->A` denied cleanly | **PASS** |
| **Professional Headshot Isolation** | SME `P`'s headshot | Aspirant `F` & peer Guide `D` vs Self & Admin | Aspirants & peers denied; self & Admin allowed | Denied with `"Unauthorized: Professional photographs are private..."`; Self & Admin allowed | **PASS** |

*Note on Archived Accounts:* Live archived-account photo cutoff could not complete through live UI because `archive_account` failed with Supabase schema error `PGRST204` (`DEF-32-001` — see `ARCHIVE_RESTORE_AND_CLOSURE_E2E.md`).

