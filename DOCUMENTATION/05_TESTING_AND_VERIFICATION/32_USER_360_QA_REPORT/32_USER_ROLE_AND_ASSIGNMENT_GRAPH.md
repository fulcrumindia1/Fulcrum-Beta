# 32-User Role and Assignment Graph (Live Institutional Simulation)

**Campaign Target:** `https://app.fulcrumindia.online/` (Hostinger KVM 2 `187.126.114.81`)  
**Deployed Revision:** Commit `988127b` (`988127bfd0ec016ad8fde7ea099ad38216262de5`)  
**Live App Container:** `fulcrum-app` (`sha256:6c212f0dc623b7d783534f71767dd950b063f522b9d0c982b4950a400c2627d1`)  
**Verification Sources:** `scratch/final_live_snapshot.json`, `scratch/run_05_batch_b/batch_b_part4_report.json`, `scratch/run_08_batch_d/d1_report.json`, `scratch/run_08_batch_d/d2_report.json`

---

## 1. Synthetic Population Summary (32 Unique Users + 1 Sole Admin)

- **Total Profiles in Supabase:** `37` (`5` untouched baseline real users including Sole Admin `fulcrumindia1@gmail.com` + `32` QA32 synthetic accounts `QA32 A` through `QA32 AF`).
- **Role Totals Across the 32 Synthetic Identities:**
  - **Aspirants (`28`):** `A, B, C, E, F, G, I, J, K, L, M, N, O, R, S, T, U, V, W, X, Y, Z, AA, AB, AC, AD, AE, AF` (`26` base `aspirant` signups + `2` mentor-base hybrids `T` and `U`).
  - **Active Guides (`14`):** `A, D, E, G, H, J, K, M, Q, T, W, Z, AB, AE` (`3` via Admin Tab 2 base role [`D, Q, T`], `1` Admin Tab 2 dual [`H`], `10` via Admin Tab 7 grants + personal NDA).
  - **Active SMEs (`14`):** `B, C, G, H, I, K, N, P, S, U, W, Y, AB, AD` (`2` via Admin Tab 3 base role [`P, U`], `12` via Admin Tab 7 grants + personal NDA).
- **Non-Admin Role Combinations Covered:** `7/7` (`9` Aspirant-only, `2` Guide-only, `1` SME-only, `7` Aspirant+Guide, `8` Aspirant+SME, `1` Guide+SME, `4` Aspirant+Guide+SME).
- **Final Account Status:** All `32/32` QA accounts finished `ACTIVE`, `is_active = True`, `legal_hold = False`, `deletion_scheduled_for = None`, with `0` pending purges.

---

## 2. Authoritative Final Relationship Graph (`relationships` Table — 22 Active Links)

| Aspirant | Primary Guide | Co-Guide(s) (`guide_ids`) | Primary SME | Advisory Panel SME(s) (`sme_ids`) | Notes / Observed Platform Behavior |
|---|---|---|---|---|---|
| `A` | `D` | `[D]` | `B` | `[C, B]` | Reciprocal `A -> B` (Guide) & `B -> A` (SME); multi-SME panel verified (`C, B`). |
| `B` | `A` | `[A, E]` | `C` | `[C]` | Primary `A` + Co-Guide `#2` `E` added via Guide -> Admin Tab 5 Directive escalation (`6dc6beb5-ffea-4f44-8f2d-cab8f31249d1`). |
| `C` | `D` | `[D]` | `None` *(COI recused `P`)* | `[]` | Prior SME `P` unassigned after Tab 12 COI approval; re-assigning `P` blocked live by `"Conflict of Interest: Selected SME has declared an active recusal on this case."` (`DEF-32-005`). |
| `E` | `A` | `[A]` | `B` | `[B]` | Standard active pair; `A` and `B` independently preserved during `EXP-M1` / `EXP-M8`. |
| `F` | `D` | `[D]` | `P` | `[P]` | Pilot primary pair (`D` Guide-only, `P` SME-only, `F` Aspirant-only). |
| `G` | `Q` | `[Q]` | `I` | `[I]` | Triple-role `G` mentored by Guide-only `Q` and Aspirant+SME `I`. |
| `I` | `J` | `[J]` | `N` | `[N]` | Mentored by Aspirant+Guide `J` and Aspirant+SME `N`. |
| `J` | `M` | `[M]` | `S` | `[S]` | Standard active mentorship pair. |
| `K` | `Z` | `[Z]` | `Y` | `[Y]` | Triple-role `K` receiving external Guide/SME support. |
| `L` | `E` | `[E]` | `H` | `[H]` | Guide `E` + Guide+SME hybrid `H` (as SME). |
| `M` | `G` | `[G]` | `K` | `[K]` | Triple-role mentors `G` (Guide) and `K` (SME). |
| `N` | `K` | `[K]` | `G` | `[G]` | Triple-role mentors `K` (Guide) and `G` (SME). |
| `O` | `K` | `[K]` | `K` | `[K]` | Same triple-role mentor `K` verified allowed as both Guide and SME in Tab 4. |
| `R` | `T` | `[T]` | `U` | `[U]` | Mentor-base hybrids `T` (Guide) and `U` (SME) mentoring Aspirant-only `R`. |
| `S` | `H` | `[H]` | `W` | `[W]` | Dual `H` (Guide) + Triple `W` (SME). |
| `V` | `W` | `[W]` | `AB` | `[AB]` | Triple `W` (Guide) + Triple `AB` (SME). |
| `W` | `AB` | `[AB]` | `AD` | `[AD]` | Triple `AB` (Guide) + Hybrid `AD` (SME). |
| `Y` | `AE` | `[AE]` | `I` | `[I]` | Non-TN `AE` (Guide) + `I` (SME). |
| `Z` | `Q` | `[Q]` | `N` | `[N]` | Guide-only `Q` + Hybrid `N` (SME). |
| `AC` | `J` | `[J]` | `S` | `[S]` | Stale-session handover & archive-blocker test target. |
| `AD` | `M` | `[M]` | `C` | `[C]` | Hybrid `M` (Guide) + `C` (SME). |
| `AE` | `AB` | `[AB]` | `AB` | `[AB]` | Non-TN `"Bengaluru (Karnataka)"` / `"Other State"` founder mentored by same triple-role `AB`. |
| `AB`, `T`, `U`, `X`, `AA`, `AF` | *Unassigned* | `[]` | *Unassigned* | `[]` | `X, AA, AF` intentionally unassigned solo controls; `T, U` blocked from receiving mentors via Admin Tab 4 (`DEF-32-004`). |

---

## 3. Graph & Perspective Verification Results

- **Pre-Graph Negative Rules (`Batch B`):**
  - `FUL-32-E2E-0010`: Self-mentorship blocked cleanly (`"An entrepreneur cannot be assigned as their own Guide."` / `"...SME."`).
  - `FUL-32-E2E-0011`: Admin Tab 4 `Assign Dedicated Guide` has **no** Co-Guide additive mode (always replaces primary Guide -> `REPLACED`); only `Assign Specialized Domain SME` exposes `➕ Add Specialist to Advisory Panel (Concurrent Multi-SME)`. Co-Guide `#2` (`E` on `B`) required escalation through Guide -> Admin Tab 5 Directive (`DEF-32-008`).
- **15-Perspective Caseload Isolation (`Batch B`):**
  - Across `15/15` checked authenticated browser perspectives (`stMain` caseload verification), `missing = []` and `leaked = []` (`PASS`).
  - **Known Co-Guide Profile Read Defect (`DEF-32-007`):** When Co-Guide `#2` `E` opened `B`'s `🤝 Guidance Team` pill, UI displayed `QA32 A [Primary]` and `QA32 E [Co-Guide #2]`, but displayed **`No Domain SME assigned yet`** even though `B` holds `sme_id = C` (`services/profiles.py:126, 337` scalar `guide_id.eq.{actor_id}` omits `guide_ids`).
- **Untouched Baseline Real Users:** All `5` real baseline user IDs (`fulcrumindia1@gmail.com`, `pravindev666@gmail.com`, `mathew60666@gmail.com`, `vanisrisjvl@gmail.com`, `manicksjvl@gmail.com`) remained `ACTIVE` with `0` relationships throughout (`d2_report.json`).

