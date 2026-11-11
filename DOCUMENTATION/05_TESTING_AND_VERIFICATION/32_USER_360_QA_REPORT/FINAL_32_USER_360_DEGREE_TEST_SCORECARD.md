# Final 32-User 360° Live Institutional QA Scorecard & Release Decision

**Campaign Target:** `https://app.fulcrumindia.online/` (VPS `187.126.114.81`, Supabase `bhaqaawsufwtjeqfifbv`)  
**Deployed Revision:** Commit `988127b` (`988127bfd0ec016ad8fde7ea099ad38216262de5`)  
**Live App Container:** `fulcrum-app` (`sha256:6c212f0dc623b7d783534f71767dd950b063f522b9d0c982b4950a400c2627d1`)  
**Caddy Container:** `fulcrum-caddy` (`sha256:6aeddd44c3078b0f9a35206472a11420648a79c184603ef95957d0a20044cb2b`)  
**Pre-Test Backup:** `backups/supabase_backup_2026-11-11_00-03-17.zip` (`5` Auth users, `296` DB rows, `4` Storage files)

---

## 1. Executive Release Decision

> **RECOMMENDATION: CONDITIONAL HOLD / NO-GO FOR FULL INSTITUTIONAL LAUNCH UNTIL P0 DEFECTS ARE PATCHED ON STAGING & VERIFIED.**  
> Core single-role workflows (public signup, matching `179` schemes, bidirectional non-hybrid consultations, private storage photo isolation, private `case_discussions`, confidential complaints, PDF dossiers, and concurrent journey saves) operate smoothly and reliably under load (`0` uncaught JS/console errors, `p50 = 3.08s`, `15/15` caseload perspectives clean).  
> **However, three `P0` production blockers** (`DEF-32-001` complete Tab 13 Account Lifecycle outage via Supabase `PGRST204` + un-rolled-back mentor unassignment, `DEF-32-002` hybrid switched-workspace consultation reply lockouts, and `DEF-32-003` Admin Tab 2/3 mentor temp password mismatch on rerun) plus five `P1` defects (`DEF-32-004..008`) prevent safe promotion of multi-role institutional governance and account lifecycle workflows without targeted fixes.

---

## 2. Scorecard Summary by Functional Domain

| Domain | Scope Exercised (`FUL-32-E2E-*`) | Result | Blocking Defects / Key Findings |
|---|---|---|---|
| **Preflight & Upgrade Verification** | Deployed `988127b` vs VPS, pre-backup, RLS anon checks | **PASS** | `67/67` checksums verified; `fulcrum-app` healthy (`0.25% CPU`, `62.57 MiB RAM`). |
| **32-User Signup, Provisioning & Onboarding** | `26` Aspirant signups (`A..AF`), `6` Admin Tab 2/3 mentors (`D, P, H, Q, T, U`) | **PARTIAL FAIL** | `user_roles` creation fix verified (`988127b`), **FAIL:** Tab 2/3 temp PW regenerates across reruns (`DEF-32-003`), UI `6`-char vs backend `8`-char gate (`DEF-32-009`), Tab 3 defaults to Madurai. |
| **Multi-Role Grants & Dual NDA (`Tab 7`, `Tab 8`)** | `24` Tab 7 grants, all `7` non-Admin combos, `55` QA legal acceptances (`100%` hashed) | **PASS** | Sole Admin excluded; `"🔒 Awaiting User Signature"` enforced; `REAFFIRM_NDA` & dual activation work; NDA `pending_nda` exclusion (`EXP-M7`) works. |
| **Mentor Graph & 9 Mutation Experiments (`Tab 4`)** | `22` active pairs (`44+` assignments incl. Co-Guide `E` & multi-SME), `EXP-M1..M8` | **PARTIAL FAIL** | `9/9` mutations + `15/15` caseloads passed. **FAIL:** `T` & `U` omitted from Tabs 1, 4 & KPI (`DEF-32-004`), Tab 4 lacks Co-Guide add radio (`DEF-32-008`), Co-Guide `E` drops SME `C` view (`DEF-32-007`). |
| **Profiles, Journeys, Toggles, Edits & Dossiers** | `28/28` Venture Profiles & Journeys, `5` edits, `F` soft-delete, `2` PDF dossiers | **PARTIAL FAIL** | Concurrent Journey writes (`F & D`), edits, toggles (`A, F`), soft-delete, & PDFs passed. **FAIL:** `T`/`U` Aspirant save wiped mentor `expertise/bio/industry` (`DEF-32-006`). |
| **Consultations, Case Notes & Admin Directives** | Bidirectional `F<->D`, `F<->P`, `R<->T/U`, `B->E`, stale session `AC->J`, `case_discussions`, Tab 5 Directives | **PARTIAL FAIL** | Private notes & Admin Directives concealed from `F`; stale-session & spoofed target blocked. **FAIL:** Switched-workspace hybrids (`A, B, H`) rejected on consultation reply (`DEF-32-002`). |
| **Schemes Matching, Release, Withdraw, Stage & SSR** | `179` canonical schemes untouched, `F(85)/AF(80)/AE(79)` (`0` TN leaks), Guide release/withdraw/SSR | **PASS (with Missing Delegation Feature)** | Stage tracking (`Applied on Portal`), private note isolation, Co-Guide scheme access, Tab 5 SSR `APPROVED`, Tab 6 pagination & isolated local CRUD passed; Admin->Guide delegation not implemented (`DEF-32-008`). |
| **Photographs & Storage Privacy** | `8` QA founder avatars + `8` QA mentor headshots (`2` private buckets) | **PASS** | Raw URL `400`, signed `200`, cross-tenant/peer denials & hybrid bucket separation `100%` enforced; archived photo cutoff untested due to `DEF-32-001`. |
| **Complaints, Inactivity & Contact Aspirants (`Tabs 9–11`)** | `B` vs `A`, unassigned `X -> Admin`, dual-lens Inactivity scan, Tab 11 WhatsApp/Gmail + Mark Sent | **PASS** | Confidential complaints invisible to `A` & SME `C`; Tab 11 uniquely showed `T` & `U`; `external_contact_logs` recorded cleanly; `0` inactivity breaches (`<7d` cohort). |
| **SME Conflict Governance (`Tab 12`)** | `P` Conflict on `C` -> Tab 12 `Approve Recusal & Unassign` | **PARTIAL FAIL** | Removed `P`, preserved `D` & `C` consultations, logged history; **FAIL:** `sme_conflict_declarations.status` stayed `'DECLARED'` forever, blocking re-assignment (`DEF-32-005`). |
| **Account Lifecycle & Archive (`Tab 13`)** | Sole Admin guard, Action History, Pause `V`, Archive `AC & Q`, Legal Hold & 30d Deletion `AF` | **FAIL (OUTAGE)** | Sole Admin protected & History table loaded, **ALL live Supabase writes failed with `PGRST204` (`DEF-32-001`)** + non-atomic `Q` unassignment before error. |
| **Safety Invariants & Post-Test Cleanliness** | Preserved 32 QA users, 5 real baseline users, & 179 schemes | **PASS** | `32/32` QA accounts active (`0` status issues, `0` holds, `0` pending deletions); `5/5` real baseline (`0` relationships) & `179/179` canonical schemes **`100%` untouched**. |

---

## 3. Staging-Tested Offline Defect Reproducers

All `7` newly automated regression reproducers in [`test_qa32_discovered_defects.py`](file:///C:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/DOCUMENTATION/05_TESTING_AND_VERIFICATION/32_USER_360_QA_REPORT/reproducers/test_qa32_discovered_defects.py) ran against isolated temporary SQLite storage (`python -m pytest -v`) and passed (`7 passed, 2 warnings in 15.77s`), confirming exact root causes without altering production code or data.

## 4. Untested / Staging-Only Items Explicitly Flagged

- **Artificial `7/10/14/30/60`-Day Inactivity Aging & Failed Notification Injection:** Not executed in production (Section 1 / Section 10 staging-only rule).
- **Permanent Purge Execution & Archived-Account Storage Cutoff End-to-End:** Blocked in production by `DEF-32-001` (`PGRST204`) and safety prohibition against permanent deletion in production.
- **Resend Live SMTP Rate Burst (`26` real emails):** Verified `signup_aspirant` UI confirmation prompt while bypassing bulk email confirmations via Supabase Admin API to avoid Resend quota exhaustion/bounces.
- **Post-Batch-D2 SSH Container Log Check:** Verified public `/healthz` (`200 ok`), `/_stcore/health` (`200 ok`), and `0` Playwright console/page errors; VPS SSH `docker logs` ran at Preflight/Upgrade (`988127b`) and was not re-opened post-Batch-D2.

## 5. Complete Deliverable Package (`32_USER_360_QA_REPORT/`)

All `20` Section 16 deliverables + `reproducers/test_qa32_discovered_defects.py` reside under `DOCUMENTATION/05_TESTING_AND_VERIFICATION/32_USER_360_QA_REPORT/` with zero edits to production source code (`app.py`, `views/`, `services/`, `migrations/`) or VPS configuration.

