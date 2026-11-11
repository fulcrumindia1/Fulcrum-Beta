# Legal Agreements, Master NDA & Role Activation E2E

**Test Cases:** `FUL-32-E2E-0060` – `0064` (`Batch A1`, `Batch A2`, `Batch B EXP-M2/M7/M8`, `Batch D1 Tab 8`)  
**Evidence Files:** `scratch/run_04_roles_a2/a2_report.json`, `scratch/run_08_batch_d/d1_report.json`, `scratch/final_live_snapshot.json`

---

## 1. Personal Terms & Master Dual NDA Coverage (`61` Total Rows; `55` QA32 Rows)

| Legal Document Type | QA32 Rows | SHA-256 `doc_hash` Non-Null | Key Verified Behaviors |
|---|---:|---:|---|
| **`terms_and_conditions`** (`v1.0.0`) | `32` | `100%` (`True`) | Every QA user (`A..AF`, `26` Aspirants + `6` Mentors) accepted personally during first UI session before entering dashboards. |
| **`nda_dual`** (Master Dual NDA) | `23` | `100%` (`True`) | All `14` QA Guides + `14` QA SMEs signed personally (`roles_covered` list with `>=2` entries on `23` rows, `"I ACCEPT"` signature text verified in `d1_report.json`). |

---

## 2. Multi-Role & Lifecycle NDA Enforcement Scenarios Tested Live

1. **Admin Non-Fabrication Guard (`NEG-PRE-NDA-LOCK`, `Batch A2`):**
   - After Admin granted `guide` to `A` in Tab 7 (`pending_nda`), Admin Tab 7 displayed **`"🔒 Awaiting User Signature"`** (button `disabled = True`). Admin could not activate `A`'s Guide role on `A`'s behalf (`tab7_A_awaiting_signature`).
2. **Pre-NDA Assignment Exclusion (`EXP-M7`, `Batch B`):**
   - Admin granted temporary `guide` (`pending_nda`) to solo Aspirant `AA`. `AA` remained **excluded** from Admin Tab 4 Guide assignment dropdown (`asg_guide`), confirming NDA-pending mentors cannot receive Aspirants prematurely. Admin then cancelled via `Cancel Grant`.
3. **Simultaneous Dual-Role NDA Activation (`G, W`, `Batch A2`):**
   - Users granted **both** `guide` and `sme` (`pending_nda`) prior to first NDA acceptance (`G`, `W`) unlocked **both** `guide` and `sme` roles immediately upon completing one personal `nda_dual` signature.
4. **Second-Role Master NDA Reaffirmation (`H, K, AB` & Re-grants `A, B`, `Batch A2`, `EXP-M2`, `EXP-M8`):**
   - Users already holding an active mentor role (`guide` or `sme`) who later received a 2nd mentor role grant (or re-grant after global revocation of `A`'s Guide and `B`'s SME) were gated by **`REAFFIRM NDA & ACTIVATE`** (`views/legal_ui.py`) before the second/re-granted role transitioned from `pending_nda -> active`.
5. **Admin Tab 8 (`📜 Legal & NDA Records`) UI Audit (`d1_report.json`):**
   - Filter dropdown switched cleanly across `"nda_dual"` (`ui_nda_shows_qa32 = True`) and `"terms_and_conditions"` (`ui_tc_shows_qa32 = True`), displaying `QA32` signatures, `roles_covered`, phrases, timestamps, and truncated SHA-256 `doc_hash`.
6. **Baseline Real Accounts Untouched:**
   - Pre-existing `pending_nda` baseline accounts `VaniSri` (`vanisrisjvl@gmail.com`) and `Manick` (`manicksjvl@gmail.com`) remained untouched in `pending_nda` (`d2_report.json`).

