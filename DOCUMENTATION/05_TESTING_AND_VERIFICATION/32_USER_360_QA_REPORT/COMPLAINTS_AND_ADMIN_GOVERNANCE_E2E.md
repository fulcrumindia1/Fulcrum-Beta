# Confidential Complaints and Admin Governance E2E (Tabs 9, 11, 12)

**Test Cases:** `FUL-32-E2E-0065` – `0082` (`Batch D1`)  
**Evidence Files:** `scratch/run_08_batch_d/d1_report.json`, `scratch/restore_p_to_c.py`, `task-1005`, `task-1038`, `reproducers/test_qa32_discovered_defects.py`

---

## 1. Tab 9 — Confidential Complaints & Fulcrum Support Isolation

| Check | Workflow Tested | Observed Result & DB Evidence | Verdict |
|---|---|---|---|
| **Assigned Founder Complaint (`B` vs Primary Guide `A`)** | `B` opened Aspirant Tab 4 -> `🛡️ Contact Fulcrum Support` -> submitted grievance (`reason='inactivity'`). | `guide_complaints` row `5e95cde7-...` persisted with `guide_id = A` (`677a856d-...`), `status = 'PENDING'`. | **PASS** |
| **Strict Confidentiality Before & After Resolution** | Logged into accused Guide `A` (Guide Portal -> `B`) & assigned SME `C` (SME Portal -> `B`). | `hidden_from_a_before = True`, `hidden_from_c_before = True`; zero leakage anywhere in `stMain`. | **PASS** |
| **Admin Resolution (`Tab 9`)** | Admin expanded `B`'s complaint in Tab 9 (`res_stat`), set `RESOLVED`, saved resolution notes (`res_note`), clicked `Submit Administrative Decision`. | DB updated `status = "RESOLVED"`. When `B` opened `Contact Fulcrum Support` expander, `"RESOLVED"` status appeared cleanly (`b_sees_resolved = True`). *UX Note:* Complaint history lives inside collapsed `Contact Fulcrum Support` expander on `B`'s Tab 4 (`views/aspirant.py:746`), easy to overlook unless expanded. | **PASS** |
| **Unassigned Founder Routing (`X`)** | Solo unassigned `X` opened Tab 4 -> `Contact Fulcrum Support` (saw info `"No Dedicated Guide assigned yet... routed directly to Fulcrum Support"`) and submitted request. | `guide_complaints` row `685a138d-...` routed with `guide_id = SOLE_ADMIN_UUID` (`616304b5-...`), appearing cleanly in Admin Tab 9 queue without errors. | **PASS** |

---

## 2. Tab 11 — Contact Aspirants (WhatsApp & Gmail Manual Outreach)

- **Search Visibility Contrast (`T` & `U`):**
  - Searched `"QA32 T"` and `"QA32 U"` inside Tab 11 (`adm_contact_asp_search`): **`qa32_T_visible = True`, `qa32_U_visible = True`** — confirming Tab 11 resolves multi-role Aspirants whereas Tabs 1 & 4 do not (`DEF-32-004`).
- **Link Construction & Manual Dispatch Audit (`QA32 F`):**
  - Inspected `F`'s contact card: verified live `https://wa.me/...` and `https://mail.google.com/...` compose links (`has_whatsapp_link = True`, `has_gmail_link = True`; no auto-send triggered).
  - Clicked `✅ Mark as Sent` (`btn_mark_asp_sent_{fid}`): `external_contact_logs` incremented `1 -> 2` (`mark_sent_logged = True`).

---

## 3. Tab 12 — SME Conflict of Interest Governance (`DEF-32-005`)

1. **Pre-Conflict History Check:** `C` submitted `C->P Pre-Recusal GST History Check` consultation so prior history existence could be audited post-recusal. `C` initially held `guide_id = D`, `sme_id = P`.
2. **Conflict Declaration (`SME P`):** `P` switched to `QA32 C` -> `Consultations` -> `⚖️ Declare Conflict of Interest`, selected `⚠️ Conflict of Interest Identified (Request Reassignment)`, submitted details. Persisted in `sme_conflict_declarations` (`status = 'DECLARED'`, `has_conflict = True`).
3. **Admin Approval (`Tab 12 -> ⚠️ Conflict Declarations`):** Clicked `🔄 Approve Recusal & Unassign`:
   - `P` cleanly removed from `C` (`sme_id = None`, `sme_ids = []`, `p_unassigned_cleanly = True`).
   - Guide `D` stayed assigned and untouched (`guide_d_untouched_during_recusal = True`).
   - `assignment_history` logged the COI recusal (`assignment_history_logged = True`).
   - Prior `C->P` consultation stayed intact in DB (`c_prior_consultations_preserved = True`).
4. **CRITICAL DEFECT DISCOVERED (`DEF-32-005`):**
   - Inspecting `sme_conflict_declarations` (`task-1038`) and attempting to restore/assign `P` in Admin Tab 4 (`restore_p_to_c.py`): **Both COI rows remained `'status': 'DECLARED'`, `'reviewed_by': null`, `'reviewed_at': null`!**
   - **Code Verification (`views/admin_governance.py:748-761`):** Clicking `btn_resolve_coi_` calls `unassign_sme(...)` but **never updates `sme_conflict_declarations.status`**.
   - **Downstream Impact:** Conflict card stays active in Tab 12 forever, Control Tower `open_conflicts_count` (`services/admin_metrics.py:109`) stays stuck `>0`, and Tab 4 blocks re-assigning `P` with **`"Conflict of Interest: Selected SME has declared an active recusal on this case."`** with zero UI clear/dismiss path (`test_repro_def_005` verified offline).

