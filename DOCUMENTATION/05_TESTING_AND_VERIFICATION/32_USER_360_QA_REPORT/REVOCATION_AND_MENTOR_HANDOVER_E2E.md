# Revocation, Role Suspension, Replacement, and Mentor Handover E2E

**Test Cases:** `FUL-32-E2E-0050` – `0059`, `FUL-32-E2E-0080` (`Batch B`, `Batch C2`, `Batch D1`, `Batch D2`)  
**Evidence Files:** `scratch/run_05_batch_b/batch_b_part4_report.json`, `scratch/run_07_batch_c2/batch_c2_report.json`, `scratch/run_08_batch_d/d1_report.json`

---

## 1. Resettable Relationship & Role Mutation Matrix (`9/9` Passed in Batch B)

| Experiment ID | Operation Executed | Affected Relationship / User | Unrelated Caseloads Preserved | Final Verification / Restore | Verdict |
|---|---|---|---|---|---|
| **`EXP-M1`** | Unassign `A` from `B` only | `B` lost `A`; Co-Guide `E` stayed active on `B` | `A -> E` remained active | Restored `A` on `B` (`guide_ids=[A, E]`). | **PASS** |
| **`EXP-M1b`** | Remove Guide `D` from `C` only | `C` lost `D`; `C`'s SME `P` stayed active | `D -> A` and `D -> F` untouched | Restored `D -> C`. | **PASS** |
| **`EXP-M2`** | Globally revoke `A`'s `guide` role (Tab 7) | `A` lost all Guide access (`B`, `E`) | `B` kept Co-Guide `E`; `D -> C` & `A` Aspirant untouched | Re-granted `A` Guide -> `A` reaffirmed NDA -> restored `A -> B, E`. | **PASS** |
| **`EXP-M3`** | Suspend `A`'s `guide` role only (Tab 7) | `A` excluded from Tab 4 Guide dropdown; `E` saw `"Temporarily Unavailable"` | `A` Aspirant dashboard & assignments stayed active | Reinstated `A`'s Guide role. | **PASS** |
| **`EXP-M5`** | Replace `L`'s Primary Guide (`E -> Q -> E`) | `L` handed over from `E` to `Q` | `L`'s SME `H` untouched | Restored `E -> L`. | **PASS** |
| **`EXP-M5b`** | Replace `A`'s 2nd SME (`C -> AD -> C`) | `A`'s secondary SME updated | `A`'s Primary SME `B` & Guide `D` untouched | Restored `C` onto `A`. | **PASS** |
| **`EXP-M6`** | Suspend triple-role `G`'s `sme` role only (Tab 7) | `N` saw `"Temporarily Unavailable"` for SME `G` | `G`'s Aspirant (`Q/I`) & Guide (`M`) roles & cases stayed active | Reinstated `G`'s SME role. | **PASS** |
| **`EXP-M7`** | Grant temporary `PENDING_NDA` mentor role to `AA` -> check Tab 4 -> `Cancel Grant` | `AA` excluded from Tab 4 Guide/SME assignment dropdowns | `AA` Solo Aspirant account stayed cleanly `ACTIVE` | Cancelled temporary grant (`Cancel Grant`). | **PASS** |
| **`EXP-M8`** | Globally revoke `B`'s `sme` role (Tab 7) | `B` lost SME cases (`A, E`) | `B` Aspirant (`[A, E]` Guides, `C` SME) stayed active | Re-granted `B` SME -> `B` reaffirmed NDA -> restored `B -> A, E`. | **PASS** |

---

## 2. Handover Edge Cases, Stale Sessions, COI & Lifecycle Side-Effects

- **Stale-Session Guide Unassignment (`AC -> J`, `Batch C2`):**
  - While Guide `J` had `AC`'s consultation form open (`tid_acj`), Admin unassigned `J` from `AC` in Tab 4.
  - Prior open `AC->J` tickets had `assigned_guide_id` cleared server-side; stale submit left `status = "OPEN"` with `guide_response = null` (`batch_c2_report.json`). Re-assigned `J -> AC` (`j_restored_ok = True`).
- **Tab 12 Conflict-of-Interest Handover (`P` on `C`, `Batch D1`):**
  - Approving COI recusal unassigned `P` from `C`, kept Guide `D` intact, kept `C`'s prior consultations (`C->P Pre-Recusal GST History Check`) intact, and logged `assignment_history`.
  - **Defect Found (`DEF-32-005`):** Re-assigning `P` to `C` later is blocked by `"Conflict of Interest: Selected SME has declared an active recusal on this case."` because Tab 12 never updates `sme_conflict_declarations.status` from `'DECLARED'`.
- **Non-Atomic Archive Unassignment Side-Effect (`Q` on `G & Z`, `Batch D2`):**
  - When Admin clicked `🗄️ Archive Account` on Mentor `Q`, `archive_account()` executed relationship removal (`"2 case(s) have no remaining co-guide!"`, clearing `Q` from `G` and `Z`) **before** failing with `PGRST204` on `profiles.update({"lifecycle_reason": ...})` (`d2_report.json`), leaving `Q` active while orphaned from `G` & `Z` until QA deliberately re-assigned `Q -> G, Z` in Tab 4.

