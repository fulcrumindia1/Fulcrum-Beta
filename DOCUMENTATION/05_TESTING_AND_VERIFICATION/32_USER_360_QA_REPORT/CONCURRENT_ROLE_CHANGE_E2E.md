# Concurrent Actions, Stale Sessions, Reciprocal Roles & Edge-Case E2E

**Test Cases:** `FUL-32-E2E-0010` – `0018`, `0038`, `0105` – `0108` (`Batch B`, `Batch C2`, `Batch D2`)  
**Evidence Files:** `scratch/run_05_batch_b/batch_b_part4_report.json`, `scratch/run_07_batch_c2/batch_c2_report.json`, `scratch/run_08_batch_d/d2_report.json`, `scratch/final_live_snapshot.json`

---

## 1. Concurrency & Race Condition Tests Executed Live (`d2_report.json`, `batch_c2_report.json`)

| Concurrent / Reciprocal Test | Method & Actors | Expected Integrity Rule | Actual Verified Result | Verdict |
|---|---|---|---|---|
| **Simultaneous Multi-Actor Journey Writes (`F` & `D`)** | 2 parallel Chromium browser threads (`ThreadPoolExecutor(2)` + `threading.Barrier(2)`) submitting simultaneously to `F`'s Journey (`F` Aspirant vs `D` Guide). | Zero lost updates; both `journey_events` rows commit cleanly. | `F` submit `3.01s` (`ok=True`), `D` submit `3.06s` (`ok=True`); **`both_concurrent_milestones_persisted = True`**. | **PASS** |
| **Mid-Session Guide Unassignment (`AC -> J`)** | Guide `J` opened `AC` ticket response form (`AC->J Stale Session ...`); Admin concurrently clicked `Unassign Guide` on `J -> AC` in Tab 4; stale `J` clicked submit. | Stale Guide write rejected; ticket remains unmodified (`OPEN`). | DB `stale_db_status = "OPEN"`, `guide_response = null`; unassign cleared `assigned_guide_id` cleanly. Restored `J -> AC` (`j_restored_ok = True`). | **PASS** |
| **Rapid Triple-Role Switching (`G`)** | Logged into triple-role `G` (`aspirant+guide+sme`) and executed 6 consecutive sidebar workspace switches (`guide -> sme -> aspirant -> guide -> sme -> aspirant`). | All 6 portal renders succeed cleanly without session bleed or crashes. | `rapid_switch_all_ok = True`; latencies: `2.9s, 2.74s, 1.43s, 3.08s, 3.55s, 1.41s`. | **PASS** |
| **Reciprocal Mentoring (`A <-> B`, `G <-> K <-> N`)** | `A` Guides `B` while `B` serves as SME to `A`; `K` Guides `N` & `G` mentors `N` while `M/G/K` overlap. | Overlapping reciprocal roles do not conflict across workspaces. | `15/15` perspective caseload checks had `missing=[]`, `leaked=[]` (`Batch B`). Note switched-role consultation reply hits `DEF-32-002`. | **PASS (Caseloads) / PARTIAL (`DEF-32-002`)** |
| **Same Triple-Role Person as BOTH Guide & SME (`O<-K,K`, `AE<-AB,AB`)** | Assigned triple-role `K` as both Guide & SME to `O`, and `AB` as both Guide & SME to `AE` in Tab 4. | Permitted when mentor holds active `guide` & `sme` roles; self-assignment blocked (`O->O`). | Both `O<-K,K` and `AE<-AB,AB` saved cleanly; self-mentorship rejected (`"An entrepreneur cannot be assigned as their own Guide/SME."`). | **PASS** |
| **Dual Concurrent `Archive Q` vs `Q`'s Active Caseload** | Clicked `Archive` on `Q` (`G, Z` active mentees). | Atomic rollback if archive fails; OR full transfer/notification if succeeds. | **`archive_account` un-assigned `Q` (`"2 case(s) have no remaining co-guide!"`) BEFORE failing `PGRST204`**, leaving `Q` active yet detached until restored (`DEF-32-001` non-atomic side effect). | **FAIL (`DEF-32-001`)** |

*Note:* High-volume destructive stress tests and simultaneous dual-Admin database lock chaos were explicitly excluded from live production per Section 1 & Section 12 safety boundaries.

