# Inactivity Monitoring, Directorate Escalation, and External Contact E2E

**Test Cases:** `FUL-32-E2E-0070` – `0077` (`Batch B`, `Batch C2`, `Batch D1`)  
**Evidence Files:** `scratch/run_08_batch_d/d1_report.json`, `scratch/run_07_batch_c2/batch_c2_report.json`, `scratch/run_05_batch_b/batch_b_part4_report.json`

---

## 1. Admin Tab 10 — Dual-Lens Caseload Inactivity Monitor (`d1_report.json`)

- **Dual Monitoring Lenses Switched Live:**
  1. `🧭 Mentor SLA Monitor (7 / 10 / 14 Days)`
  2. `🌱 Founder Engagement & Blocker Monitor (14 / 30 / 60 Days)`
  - Both lens panels rendered cleanly (`lens2_rendered = True`) across active filters (`Status`, `Mentor Role`).
- **Live Scan Execution (`🚀 Run Caseload Inactivity Scan Now`):**
  - Executed cleanly in **`3.09s`** against live production data with zero crashes (`logs: 0 -> 0`).
  - As all QA32 consultations and caseloads were created within the active test window (`< 7 days` old), `inactivity_logs` rightly remained `0` (`"No inactivity escalation records logged yet. Run a scan to check all active caseloads."`).
- **Staging-Only Scope Note (Per Section 1 & Section 5 Tab 10):** Artificial `7/10/14/30/60`-day clock jumps and broken notification delivery injection were **not** performed in production to protect real timestamps (`inactivity_logs = 0`).

---

## 2. Admin Tab 5 — Mentor Inquiries, Co-Guide Escalation & Scheme Support Reviews

1. **Guide -> Admin Co-Guide Assignment Escalation (`Batch B`):**
   - Guide `A` raised Directorate inquiry (`6dc6beb5-ffea-44f4-8f2d-cab8f31249d1`) on `B` -> Admin Tab 5 selected `Co-Guide #2 = E` and issued Directive -> `B` gained `guide_ids = ['A', 'E']`.
2. **Guide -> Admin Policy Directive (`D -> Admin -> F`, `Batch C2`):**
   - Guide `D` raised `"D->Admin F DIC Policy Query"` on `F` -> Admin issued `"ADMIN-SECRET-DIRECTIVE: Approve DIC fast-track liaison for F."`.
   - Verified `Admin` / directive strings were completely invisible on `F`'s Journey and Consultations tabs (`f_leaked_directive = False`, `f_leaked_admin_word_in_journey = False`).
3. **Scheme Support Review Escalation (`D -> Admin Tab 5 Subtab 2 -> APPROVED`, `Batch C2`):**
   - Guide `D` submitted SSR exception on `F`'s 3rd match -> Admin approved (`a2a95b8a-...` -> `status = "APPROVED"`).

---

## 3. Admin Tab 11 — Manual External Outreach (`Contact Aspirants`, `d1_report.json`)

- **Search & Multi-Role Coverage:** Found **`QA32 T`** (`qa32_T_visible = True`), **`QA32 U`** (`qa32_U_visible = True`), and **`QA32 F`** (`qa32_F_visible = True`).
- **Manual Compose Links:** Rendered verified `https://wa.me/...` and `https://mail.google.com/...` URLs without automated outbound transmission.
- **Confirmed Outreach Audit Trail:** Clicking `✅ Mark as Sent` on `F` logged to `external_contact_logs` (`ext_logs_before = 1`, `ext_logs_after = 2`, `mark_sent_logged = True`).

