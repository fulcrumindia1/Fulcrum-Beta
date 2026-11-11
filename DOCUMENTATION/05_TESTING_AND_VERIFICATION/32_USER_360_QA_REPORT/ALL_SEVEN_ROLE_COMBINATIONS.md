# All Seven Permitted Non-Admin Role Combinations E2E

**Campaign Verification:** Executed across all `32` QA accounts in live browser sessions (`Batch A2`, `Batch B`, `Batch C1`, `Batch C2`, `Batch D1/D2`)

---

## 1. Live Coverage Matrix Across the 7 Non-Admin Combinations

| # | Role Combination | QA Synthetic Account(s) | Count | Workspaces Available in Sidebar | Verified Live Behavior | Observed Defects Affecting Combination |
|---|---|---|---|---|---|---|
| **1** | **Aspirant only** | `F, L, O, R, V, X, AA, AC, AF` | `9` | Aspirant only (no switcher) | All 6 Aspirant tabs, 5-section profile, photo upload/delete, Journey edit/toggle/delete, Scheme Matches, Consultations, Complaints. | None blocking (`AF` sparse eligibility matched `80` schemes). |
| **2** | **Guide only** | `D, Q` | `2` | Guide only | All 3 Guide tabs, mentee selection, Journey contribute, Scheme release/withdraw/SSR, Consultation reply, Admin inquiry, Private headshot. | Initial Temp PW regeneration (`DEF-32-003`). |
| **3** | **SME only** | `P` | `1` | SME only | All 3 SME tabs, technical Journey note, Consultations reply, Proactive Advisory Notice, Case Discussion Board, Conflict Declaration, Private headshot. | COI approval stays `'DECLARED'` (`DEF-32-005`); Temp PW bug (`DEF-32-003`). |
| **4** | **Aspirant + Guide** | `A, E, J, M, T, Z, AE` | `7` | Aspirant <-> Guide switcher | Can switch cleanly between Founder and Guide workspaces; **Aspirant-base (`A`) fails Guide consultation replies; Guide-base (`T`) omitted from Admin Tabs 1/4 & blocked from roadmap toggle when Guide role passed**. | **CRITICAL:** `A` cannot reply in Guide Consultations (`DEF-32-002`); `T` invisible in Tabs 1 & 4 (`DEF-32-004`), loses `bio/expertise` on Aspirant save (`DEF-32-006`). |
| **5** | **Aspirant + SME** | `B, C, I, N, S, U, Y, AD` | `8` | Aspirant <-> SME switcher | Can switch cleanly between Founder and SME workspaces; **Aspirant-base (`B`) fails SME consultation replies; SME-base (`U`) omitted from Admin Tabs 1/4 & lost `expertise` on Aspirant save**. | **CRITICAL:** `B` cannot reply in SME Consultations (`DEF-32-002`); `U` invisible in Tabs 1 & 4 (`DEF-32-004`), lost `expertise` (`DEF-32-006`). |
| **6** | **Guide + SME** | `H` | `1` | Guide <-> SME switcher | Replied cleanly as Guide (`S->H` -> `IN_PROGRESS`), kept caseloads separate, shared private headshot in `professional-headshots`; **Blocked when switched to SME (`L->H` stayed `OPEN` + `"Unauthorized..."`)**. | `H` fails SME replies (`DEF-32-002`); sidebar badge stays pinned `"VERIFIED GUIDE"` in SME Portal (`DEF-32-010`). |
| **7** | **Aspirant + Guide + SME** | `G, K, W, AB` | `4` | Aspirant <-> Guide <-> SME switcher | Dual `pending_nda` (`G, W`) activated both roles in one NDA; 2nd mentor role (`K`) triggered `REAFFIRM_NDA`; `G` completed 6 rapid workspace switches (`1.41s–3.55s`); **Same consultation reply failure on non-base mentor workspaces**. | Non-base workspace consultation reply rejection (`DEF-32-002`); cross-role notification mix in sidebar (`DEF-32-010`). |

---

## 2. Live Workspace Consultation Reply Matrix (`batch_c2_report.json` & `task-900`)

| Actor | Base `profiles.role` | Active Workspace | Target Ticket | Actual DB Status After Click | Exact UI Outcome | Verdict |
|---|---|---|---|---|---|---|
| `D` | `guide` | Guide Portal | `F -> D` (`a469e6a4-...`) | `RESOLVED` (`guide_resp=True`) | Guidance recorded & bidirectional follow-up completed. | **PASS** |
| `P` | `sme` | SME Advisory Portal | `F -> P` (`213303a0-...`) | `RESOLVED` (`sme_resp=True`) | Advisory response recorded & resolved. | **PASS** |
| `T` | `guide` | Guide Portal | `R -> T` (`06278356-...`) | `IN_PROGRESS` (`guide_resp=True`) | Reply accepted (workspace matches `profiles.role`). | **PASS** |
| `U` | `sme` | SME Advisory Portal | `R -> U` (`1ed5c28a-...`) | `IN_PROGRESS` (`sme_resp=True`) | Reply accepted (workspace matches `profiles.role`). | **PASS** |
| `H` | `guide` | Guide Portal | `S -> H` (`1fcd9fc8-...`) | `IN_PROGRESS` (`guide_resp=True`) | Reply accepted (workspace matches `profiles.role`). | **PASS** |
| **`A`** | **`aspirant`** | **Guide Portal** | `B -> A` (`60e0a3e3-...`) | **`OPEN`** (`guide_resp=False`) | **`"Unauthorized: Only assigned Guides or Admins may respond to this consultation."`** | **FAIL (`DEF-32-002`)** |
| **`B`** | **`aspirant`** | **SME Advisory Portal** | `A -> B` (`e3855d0b-...`) | **`OPEN`** (`sme_resp=False`) | **`Unauthorized...`** alert, ticket remained `OPEN` (`sme_resp=False`). | **FAIL (`DEF-32-002`)** |
| **`H`** | **`guide`** | **SME Advisory Portal** | `L -> H` (`b1fdfadc-...`) | **`OPEN`** (`sme_resp=False`) | **`Unauthorized...`** alert, ticket remained `OPEN` (`sme_resp=False`). | **FAIL (`DEF-32-002`)** |

---

## 3. Root-Cause Diagnosis & Workspace Isolation Observations

- **Stale `st.session_state["role"]` (`DEF-32-002`):** Workspace switching updates active portal selection cleanly in UI, so `stMain` displays the exact authorized cases for that role (`15/15` perspectives `missing=[], leaked=[]`). However, `guide_respond_request` (`services/help_requests.py:455-458`), `sme_respond_request`, and `toggle_event_roadmap_inclusion` (`services/journey.py:270-282`) authorize against `st.session_state.get("role")`, which remains static as the user's base `profiles.role`.
- **Sidebar & Notifications (`DEF-32-010`):** On `H` switched into `SME Advisory Portal`, the sidebar badge remained `"VERIFIED GUIDE"`, and unread notification counts (`A`: `41`, `B`: `32`, `H`: `9`) aggregated notifications across all roles held by the identity.
- **Storage Separation (`Batch C1`):** Hybrid users maintained distinct buckets cleanly (`A`: `aspirant-profile-photos` vs `professional-headshots`, `A_bucket_separation=True`). Guide+SME `H` deliberately shared one professional headshot across both mentor identities (`H-SME-SHARED-CHECK=True`).

