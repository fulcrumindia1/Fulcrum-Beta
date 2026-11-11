# Admin Counts and Global Role Consistency Audit

**Verification Scope:** Authoritative Supabase tables (`profiles`, `user_roles`, `relationships`, `legal_acceptances`) vs Admin Control Tower KPIs, Tabs 1–4 rosters, Tab 7 grants, and Tab 11 (`Contact Aspirants`)

---

## 1. Baseline vs. Final Database Population Counts (`final_live_snapshot.json` & `baseline_report.json`)

| Entity / Table | Pre-Test Real Baseline | Post-32-User Campaign Total | Delta (Synthetic QA Records) | Notes / Production Impact |
|---|---:|---:|---:|---|
| `profiles` (`auth.users`) | `5` | `37` | `+32` | `5` baseline real accounts untouched; `32` QA (`A..AF`) active. |
| `user_roles` | `6` | `36` | `+30` | `6` QA Tab 2/3 mentor grants + `24` QA Tab 7 grants (solely active). |
| `relationships` | `0` | `22` | `+22` | `22` active QA pairs (`5` baseline real remain at `0` relationships). |
| `journeys` / `journey_events` | `2` / `52` | `30` / `209` | `+28` / `+157` | All `28` QA Aspirants + `1` QA base journey per active Aspirant (`F` has `1` soft-deleted draft). |
| `journey_event_revisions` | `0` | `5` | `+5` | Verified on `A, B, F, T, U` edit dialogs (`batch_c1_part2_report.json`). |
| `help_requests` | `6` | `56` | `+50` | Consultations, proactive directives/notices, & Directorate inquiries. |
| `case_discussions` | `0` | `2` | `+2` | Private (`F-PRIVATE-CREDIT-NOTE`) & Open (`F-OPEN-BOARD`) on `F`. |
| `schemes` | `179` | `179` | `0` | **`100%` unchanged** (`exact_179_id_and_active_match = true`). |
| `scheme_releases` / `scheme_support_reviews` | `0` / `0` | `3` / `1` | `+3` / `+1` | Guide `D` releases (`SCH-TN-1`, withdrawn `PRIV-ANGELSTN-2026-DUP-146`) & `APPROVED` SSR. |
| `legal_acceptances` | `6` | `61` | `+55` | `23` `nda_dual` QA rows + `32` Terms rows; all `doc_hash` verified. |
| `guide_complaints` | `0` | `4` | `+4` | `B -> A` (`RESOLVED`), `X -> Fulcrum Support` (`PENDING`). |
| `sme_conflict_declarations` | `0` | `2` | `+2` | `P` on `C` (stuck `'DECLARED'` after Tab 12 recusal — `DEF-32-005`). |
| `external_contact_logs` | `0` | `2` | `+2` | Admin Tab 11 WhatsApp/Gmail `Mark as Sent` verification on `F`. |
| `inactivity_logs` | `0` | `0` | `0` | Scan executed (`3.09s`); `0` breaches (test cohort active `< 7` days). |
| `account_lifecycle_log` | `17` | `17` | `0` | Live Tab 13 writes blocked by `PGRST204` (`DEF-32-001`). |
| `assignment_history` | — | `73` | — | All assign/replace/unassign/COI transitions logged. |
| `aspirant_photos` / `professional_photos` | `2` / `1` | `10` / `9` | `+8` / `+8` | `8` QA founder photos + `8` QA mentor headshots (`H` shares 1). |
| `notifications` | `18` | `296` | `+278` | Assignment, milestone, consultation & complaint notifications. |

---

## 2. Admin UI Counter & Roster Parity Verification (`Batch A2`, `Batch B`, `Batch D1`)

| Metric / View | Expected (True Role Membership) | Observed Live UI | Discrepancy / Explanation |
|---|---:|---:|---|
| **Control Tower `ASPIRANTS` KPI** | `30` (`2` real + `28` QA incl. `T, U`) | **`28`** | **MINUS 2 (`DEF-32-004`):** KPI & `paginate_profiles(role="aspirant")` filter `profiles.role == 'aspirant'`, omitting Guide-base `T` & SME-base `U` who hold active `'aspirant'` grants in `user_roles`. |
| **Control Tower `ACTIVE GUIDES` KPI** | `15` (`1` real active + `14` QA active) | **`15`** | **EXACT MATCH.** `paginate_guides` checks active `'guide'` grants in `user_roles`; rightly excludes `VaniSri` (`pending_nda`) and temp `pending_nda` `AA` (`EXP-M7`). |
| **Control Tower `ACTIVE SMES` KPI** | `15` (`1` real active + `14` QA active) | **`15`** | **EXACT MATCH.** `paginate_smes` checks active `'sme'` grants in `user_roles`; rightly excludes `Manick` (`pending_nda`). |
| **Admin Tab 1 (`Aspirants & Journeys`)** | Shows all `28` QA Aspirants | Omits **`T` and `U`** | `QA32 T: visible=False`, `QA32 U: visible=False` (vs `Z/AF: True`). Admin cannot inspect `T`/`U`'s Venture Profiles, Journeys, or Dossier PDFs in Tab 1! |
| **Admin Tab 4 (`Assign Mentors`)** | Assignable Aspirants include `T, U` | Omits **`T` and `U`** | `QA32 T: False`, `QA32 U: False` in `asg_asp_g` / `asg_asp_s`, preventing Admin from assigning mentors to `T` and `U` (`DEF-32-004`). |
| **Admin Tab 11 (`Contact Aspirants`)** | Shows all Aspirants | **Shows `T` & `U`** | `d1_report.json`: `qa32_T_visible=True`, `qa32_U_visible=True`! Architectural inconsistency between Tab 11 (`user_roles`-aware / full list) vs Tabs 1 & 4 (`paginate_profiles(role="aspirant")`). |
| **Multi-Role Roster Uniqueness** | Triple-role user (`G, K, W, AB`) appears once in Tab 7, once in Tab 2, once in Tab 3 | **Verified `1x`** | Each triple-role person has 1 Auth UUID (`profiles` unique) and appears 1x in Tab 7 roster + 1x each in Tab 2 & Tab 3 (`EXP-M2` / `EXP-M6` / `EXP-M8` reduce only the revoked/suspended role KPI cleanly). |

**Note on Synthetic Cohort Visibility in Operational Metrics (Section 10 & 15):** Fulcrum does not implement an `is_test_account` flag in production metrics; per safety rules ("Do not invent or modify database columns"), all 32 retained `QA32` accounts contribute `+26` (`base_role='aspirant'`) / `+28` (`active aspirant`) Aspirants, `+14` Active Guides, and `+14` Active SMEs to production KPIs unless explicitly filtered by email prefix (`fulcrumindia1+qa32_*`).

