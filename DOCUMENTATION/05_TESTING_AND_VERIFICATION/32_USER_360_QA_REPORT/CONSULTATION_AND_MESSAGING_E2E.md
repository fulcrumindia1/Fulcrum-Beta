# Consultation, Case Collaboration, and Admin Directives E2E

**Test Cases:** `FUL-32-E2E-0030` – `0039` (`Batch C2 Part 1 & Part 2`)  
**Evidence Files:** `scratch/run_07_batch_c2/batch_c2_report.json`, `steps/900/output.txt`, `steps/934/output.txt`, `task-941`

---

## 1. Bidirectional Consultations & Proactive Mentor Communication

| Scenario | Actors | Expected Behavior | Observed Browser & DB Outcome | Verdict |
|---|---|---|---|---|
| **Unassigned Mentor Block** | `X` -> `Dedicated Guide` | Rejected; no ticket created. | Alert: `"A Dedicated Guide is not currently available or assigned. Please select an active Domain S..."`; `tid = None`. | **PASS** |
| **Bidirectional Guide Ticket + Proactive Directive** | `F <-> D` (`a469e6a4-...`) | `F` submits -> `D` replies (`Awaiting Founder`) + sends Proactive Directive -> `F` sees Directive & replies -> `D` resolves. | `sees_directive = True`; DB `status = "RESOLVED"`, `has_guide_resp = True`. | **PASS** |
| **Bidirectional SME Ticket + Proactive Notice** | `F <-> P` (`213303a0-...`) | `F` submits -> `P` replies (`Awaiting Founder`) + sends Proactive SME Notice -> `P` resolves. | DB `status = "RESOLVED"`, `has_sme_resp = True`. | **PASS** |
| **Mentor-Base Hybrids (`T` Guide, `U` SME)** | `R <-> T`, `R <-> U` | `T` and `U` reply inside matching base-role workspaces. | Both moved `OPEN -> IN_PROGRESS` cleanly (`06278356-...`, `1ed5c28a-...`). | **PASS** |
| **Guide-Base Hybrid `H` in Guide Workspace** | `S -> H` (`1fcd9fc8-...`) | `H` replies inside Guide workspace. | Moved `OPEN -> IN_PROGRESS` cleanly (`has_guide_resp = True`). | **PASS** |
| **Co-Guide #2 Direct Consultation** | `B -> Co-Guide #2 E` (`f30931c9-...`) | `B` selects `Co-Guide #2 — QA32 E`; ticket appears on `E`'s Guide Console. | `coguide_e_sees = True`; DB ticket persisted (`OPEN`). | **PASS** |

---

## 2. CRITICAL LIVE DEFECT: Hybrid Switched-Workspace Consultation Replies (`DEF-32-002`)

| Actor | Base Role | Switched Portal | Ticket | Observed UI Error Alert & DB State | Status |
|---|---|---|---|---|---|
| **`A`** | `aspirant` | Guide Portal | `B -> A` (`60e0a3e3-...`) | **Alert:** `"Unauthorized: Only assigned Guides or Admins may respond to this consultation."` DB remained `OPEN`, `guide_response = null`. | **FAIL** |
| **`B`** | `aspirant` | SME Advisory Portal | `A -> B` (`e3855d0b-...`) | **Alert:** `Unauthorized...`; DB remained `OPEN`, `sme_response = null`. | **FAIL** |
| **`H`** | `guide` | SME Advisory Portal | `L -> H` (`b1fdfadc-...`) | **Alert:** `Unauthorized...`; DB remained `OPEN`, `sme_response = null`. | **FAIL** |

- **Verified Root Cause (`services/help_requests.py:454-458` & Pytest Reproducer `test_repro_def_002`):** `guide_respond_request()` and `sme_respond_request()` authorize callers via `st.session_state.get("role")`, which holds static `profiles.role` rather than `active_workspace` or `user_roles` membership. Any promoted Aspirant acting as Guide/SME, or promoted Guide acting as SME, cannot reply to consultations in live production.

---

## 3. Security, Stale-Session Revocation, Private Notes, and Directive Concealment

- **Cross-User & Spoofed-Target Protection (`task-941` & `batch_c2_report.json`):**
  - Calling `create_request(F_id, "Cross Spoof", ..., target_role="guide", target_mentor_id=Q_id)` **ignored/overrode** spoofed unassigned `Q_id` server-side and routed `assigned_guide_id` strictly to `F`'s active assigned Guide `D` (`de1d163e-...`).
  - Calling `guide_respond_request(fd_tid, Q_id, ...)` from unassigned `Q` failed (`cross_reply_blocked = True`, `"You are not authorized to respond to this request."`).
- **Mid-Session Unassignment Stale-Form Guard (`AC -> J`):**
  - Guide `J` opened `AC`'s active ticket (`AC->J Stale Session ...`) and typed a response. Admin simultaneously clicked `Unassign Guide` on `J` for `AC` in Tab 4. When stale `J` clicked submit: ticket **remained `OPEN`** (`stale_db_status = "OPEN"`, `guide_response = null`). Restoring `J -> AC` (`ensure_j_on_ac`) succeeded cleanly (`j_restored_ok = True`). (Note: prior unassignment nulled `assigned_guide_id` on pre-existing open `AC->J` tickets so former mentor `J` lost access).
- **Private vs Open `case_discussions` (`batch_c2_report.json`):**
  - Guide `D` posted `F-PRIVATE-CREDIT-NOTE` (`is_private=True`) and `F-OPEN-BOARD` (`is_private=False`) on `F`.
  - SME `P` saw **both** (`p_sees_private = True`, `p_sees_open = True`).
  - Aspirant `F` saw `F-OPEN-BOARD` (`f_sees_open = True`) and **never saw** `F-PRIVATE-CREDIT-NOTE` (`f_leaked_private = False`).
- **Admin Directives Concealment (`Tab 5`):**
  - Guide `D` raised `D->Admin F DIC Policy Query`; Admin issued `ADMIN-SECRET-DIRECTIVE: Approve DIC fast-track liaison for F.`.
  - Checked Aspirant `F` Tabs 3 (`Journey`) & 6 (`Consultations`): `f_leaked_directive = False`, `f_leaked_admin_word_in_journey = False`.

