# 32-User Venture Profiles, Journey Timelines, Edits, Toggles, and Dossiers

**Test Cases:** `FUL-32-E2E-0020` – `0028` (`Batch C1`, `Batch C1 Part 2`, `Batch D2 Concurrency`)  
**Evidence Files:** `scratch/run_06_batch_c1/batch_c1_report.json`, `scratch/run_06_batch_c1/batch_c1_part2_report.json`, `scratch/run_08_batch_d/d2_report.json`, `scratch/run_06_batch_c1/dossier_F.pdf`, `dossier_B.pdf`

---

## 1. Venture Profile Completion Across All 28 QA Aspirants

- **Coverage:** `28/28` QA Aspirants (`A`..`AF` excluding non-Aspirants `D, H, P, Q`) saved complete 5-section Venture Profiles via real Chromium UI (`missing_biz = []`):
  - **Standard TN Districts (`27/28`):** Diverse `MASTER_DISTRICTS_TN` & `MASTER_SECTORS` / `MASTER_STAGES` coverage (`Madurai`, `Coimbatore`, `Chennai`, `Salem`, `Tiruchirappalli`, `Thanjavur`, `Erode`, `Tirunelveli`, `Kanyakumari`, `Vellore`, `Thoothukudi`, `Namakkal`, `Karur`, `Dindigul`, `Krishnagiri`, `Dharmapuri`, `Cuddalore`, `Nagapattinam`, `Viluppuram`, `Virudhunagar`, `Ramanathapuram`, `Sivaganga`, `Pudukkottai`, `Theni`).
  - **Custom Sector Edge Case (`AB`):** Entered custom sector `"Marine Aquaculture Export"` (`batch_c1_part2_report.json`).
  - **Non-TN Custom Location (`AE`):** Saved `district = "Bengaluru (Karnataka)"`, `state = "Other State"`.
  - **Minimal / Sparse Profile (`AF`):** Saved `"QA32 AF Minimal Concept"` (`Ideation / R&D`, `100%` completion UI).
- **Cross-Role Profile Clobber Defect (`DEF-32-006`):**
  - When Mentor-base hybrids **`T`** (`guide` + `aspirant`) and **`U`** (`sme` + `aspirant`) saved their Aspirant 5-section Venture Profiles in Batch C1, top-level mentor keys **`expertise`, `bio`, and `industry` were wiped** from `profiles.profile_data` (while pure mentors `P` & `Q` retained all three).
  - Subsequently, when `U` attempted to update district `Madurai -> Chennai` in SME Tab 3 (`My Profile`), validation blocked save (`"Please fill in your name and specialization domain."`) until `expertise` (`"Technology Commercialization & SaaS Scale-up"`) was re-entered. Saving SME Tab 3 afterward **preserved** all 8 keys (`assistance_need`, `bio`, `business`, `demographics`, `expertise`, `industry`, `personal`, `professional`).

---

## 2. Journey Creation, Mentor Contributions, Edits & Soft-Delete (`batch_c1_part2_report.json`)

| Workflow | Scope Tested | Outcome & DB Evidence | Verdict |
|---|---|---|---|
| **Aspirant Manual Milestones** | All `28/28` Aspirants | `missing_je = []`; every Aspirant added at least 1 manual milestone via `"Add Journey Milestone"`. | **PASS** |
| **Guide & SME Contributions** | `8/8` pairs (`D->F`, `P->F`, `A->B`, `E->B`, `C->B`, `H->S`, `G->N`, `T->R`, `U->R`, etc.) | All mentor Journey contributions saved with correct author role tags (`GUIDE`, `SME`). | **PASS** |
| **Journey Entry Edits & Revisions** | `A, B, F, T, U` via `@st.dialog("Edit Journey Entry")` | `5/5` saved edited titles (`"... (Edited)"`) and persisted `1` revision each in `journey_event_revisions` (`journey_event_id` FK). | **PASS** |
| **Soft-Delete (`QA32 F Temporary Draft Entry`)** | `F` | `del_ev_{id}` -> `yes_del_ev_{id}` set `deleted_at` & `deleted_by` (`soft_deleted_count = 1`), removing entry cleanly from active timeline while preserving audit row. | **PASS** |
| **Not Needed / Needed Roadmap Toggle (`A`, `F`)** | Non-aspirant events (`A`: `91bd6a6c`, `F`: `ce775c61`) | UI button `.st-key-excl_{id}` only renders on non-aspirant (`guide`/`sme`/`system`) items; clicking set `included_in_roadmap = False`, restoring via `.st-key-incl_{id}` set `True`. | **PASS** |
| **Not Needed Toggle on `T` & `U`** | Mentor-base hybrids `T`, `U` | **`ui_excl_count = 0`** (Admin Tab 4 cannot assign mentors to `T`/`U`, leaving 0 mentor events); calling `toggle_event_roadmap_inclusion` with `actor_role='guide'`/`'sme'` rejected (`"Permission denied: Guides/Smes cannot alter..."`, `DEF-32-002` pattern). | **BLOCKED (UI) / REPRODUCED (`DEF-32-002`)** |
| **Concurrent Multi-Actor Writes (`F` & `D`)** | Simultaneous browser threads on `F` (`task-1088`) | Thread 1 (`F`, Aspirant, `3.01s`) & Thread 2 (`D`, Guide, `3.06s`) hit barrier simultaneously -> **both milestones saved cleanly** (`both_concurrent_milestones_persisted = True`). | **PASS** |
| **Admin Journey Sanitization & Dossiers** | Admin Tab 1 on `F`, `B` | `f_leaked_admin_word_in_journey = False`; Dossier PDFs downloaded for `F` (`367,822` B, `%PDF-`) and `B` (`396,646` B, `%PDF-`). Note Admin Tab 1 cannot open `T`/`U` (`DEF-32-004`). | **PASS (for base Aspirants); PARTIAL (`DEF-32-004`)** |

