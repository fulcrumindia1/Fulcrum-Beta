# Scheme Matching, Release, Stage Tracking, SSR & Catalogue E2E

**Test Cases:** `FUL-32-E2E-0040` – `0048` (`Batch C2` & `Batch D1`)  
**Evidence Files:** `scratch/run_07_batch_c2/batch_c2_report.json`, `scratch/run_08_batch_d/d1_report.json`, `scratch/run_08_batch_d/d2_report.json`

---

## 1. Scheme Catalogue Integrity & Read-Only Operations (`Tab 6`)

- **Catalogue Unchanged:** `schemes` count remained **`179`** (`canonical_179_schemes_untouched.exact_179_id_and_active_match = True` vs `seed/canonical_179_schemes.json`).
- **Production Read-Only Browser Tests (`Admin Tab 6`):**
  - Header displayed `179 Records in Intelligence Database` (`shows_179 = True`).
  - Clicked `Next Page ▶`: rendered **`Page 2 of 6 (179 Total Schemes)`** (`d1_report.json`).
  - Searched `"PMEGP"`: filtered catalogue cleanly (`search_pmegp = True`).
- **Isolated Local Staging CRUD (`LocalDatabase(tmpd/qa32_iso.db)`):**
  - Verified synthetic scheme `SCH-QA32-ISO-1` create (`created = True`), update + archive (`updated_and_archived = True`), and delete (`deleted = True`) offline without touching production Supabase.
- **Missing Feature Reported (`Section 5 Tab 6`):** **Admin-to-Guide scheme delegation does not exist** (`DEF-32-008`). Guides independently view and release curated scheme matches (`match_schemes_for_aspirant`) to their assigned Aspirants; Admins cannot push/delegate a specific scheme into a Guide's queue.

---

## 2. Profile-Driven Scheme Matching Comparison (`match_schemes_for_aspirant`)

| QA Aspirant | Profile Characteristics | Match Count | Top Recommendation / Scope Verification |
|---|---|---:|---|
| **`F`** | `Madurai`, `Tamil Nadu`, `Food Processing & Agribusiness`, `Pre-Seed / Seed` | **`85`** | Top #1: **`Tamil Nadu Startup Policy - Seed Funding`** (`SCH-TN-1`). |
| **`AF`** | `Theni`, `Tamil Nadu`, minimal concept (`Ideation / R&D`) | **`80`** | Lower match set reflecting minimal eligibility profile (`AF_minimal_matches = 80`). |
| **`AE`** | `Bengaluru (Karnataka)`, `Other State`, `Technology & SaaS`, `Pre-Seed / Seed` | **`79`** | **`0` Tamil Nadu-exclusive scheme leaks** (`AE_tn_exclusive_leaks = []`). |

---

## 3. Guide Release, Withdrawal, Private Note Privacy, Stage Tracking & SSR

| Workflow Step | Actors | Observed Browser & DB Verification | Verdict |
|---|---|---|---|
| **1. Guide Releases Top #1 & #2** | Guide `D` -> `F` | Released `SCH-TN-1` with public note `"F-PUBLIC-REC: Apply early for Q1 tranche."` & private note `"F-HIDDEN-GUIDE-NOTE: Branch manager contact."`; released #2 `PRIV-ANGELSTN-2026-DUP-146`. | **PASS** |
| **2. Guide Withdraws #2** | Guide `D` -> `F` | Clicked withdraw -> DB `PRIV-ANGELSTN-2026-DUP-146` transitioned `status = "WITHDRAWN"`; vanished from `F`'s Tab 5 (`f_withdrawn_s1_gone = True`). | **PASS** |
| **3. Private Note Isolation** | Aspirant `F` Tab 5 | `F` saw `SCH-TN-1` (`f_sees_s0 = True`) and `F-PUBLIC-REC` (`f_sees_public_rec = True`), and **never saw** `F-HIDDEN-GUIDE-NOTE` (`f_leaked_private_guide_note = False`). | **PASS** |
| **4. Application Stage Update** | `F` -> Guide `D` | `F` updated stage to `Applied` with note `"QA32 DIC Ref #2026-F1"`. DB `scheme_releases` recorded `application_stage = "Applied on Portal"`. Guide `D` saw **`Applied on Portal`** (`guide_d_sees_applied_on_portal = True`; note `QA32 DIC Ref #2026-F1` note string itself is not displayed on Guide's summary card: `guide_d_sees_app_note = False`). | **PASS** |
| **5. Scheme Support Review (SSR)** | Guide `D` -> Admin Tab 5 Subtab 2 | Guide `D` escalated #3 `m_f[2]`; Admin opened Tab 5 `Scheme Support Reviews`, entered `"Approved via QA32 Admin exception audit."`, clicked `Record Decision` -> DB `status = "APPROVED"` (`a2a95b8a-...`). | **PASS** |
| **6. Co-Guide #2 Scheme Access** | Co-Guide `E` on `B` | `E` opened `B`'s `Scheme Matches` subtab -> saw `"Top Curated Matches"` and `RELEASE TO ASPIRANT` action buttons (`coguide_e_sees_b_matches = True`, `coguide_e_has_release_btn = True`). | **PASS** |

