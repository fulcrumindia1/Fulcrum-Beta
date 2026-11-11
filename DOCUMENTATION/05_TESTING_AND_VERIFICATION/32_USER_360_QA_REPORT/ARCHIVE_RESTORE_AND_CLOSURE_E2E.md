# Account Lifecycle, Archive, Restore, and Closure E2E (Tab 13)

**Test Cases:** `FUL-32-E2E-0085` – `0092` (`Batch D2`)  
**Evidence Files:** `scratch/run_08_batch_d/d2_report.json`, `task-1077`, `task-982`, `reproducers/test_qa32_discovered_defects.py::test_repro_def_001_lifecycle_supabase_column_mismatch`

---

## 1. CRITICAL PRODUCTION BLOCKER (`DEF-32-001` — Live Supabase Schema Mismatch `PGRST204`)

Every administrative mutation in **Admin Tab 13 (`🗄️ Account Lifecycle & Archive`)** failed in live production (`https://app.fulcrumindia.online/`, commit `988127b`) due to an unapplied/divergent Supabase schema (`Migration 009` vs live DB):

| Tab 13 Workflow | Target Test Account | Expected Behavior | Actual Observed UI Alert & DB State (`d2_report.json`) | Verdict |
|---|---|---|---|---|
| **Sole Admin Safeguard** | `fulcrumindia1@gmail.com` | Zero suspend/archive/delete/hold controls rendered. | **`no_pause_btn=True`, `no_archive_btn=True`, `no_delete_btn=True`, `no_hold_btn=True`** (`admin_listed_or_protected=True`). | **PASS** |
| **Account Action History Subtab** | Platform-wide log (`17` baseline rows) | Displays chronological tamper-evident table. | `subtab4_history_rendered = True`, `lifecycle_log_recent_actions` rendered 12 visible recent actions. | **PASS** |
| **Pause & Resume (`TEMPORARILY_SUSPENDED`)** | `V` | `V` paused -> login blocked -> resumed -> `V` logs in. | **Alert:** `"Failed to suspend account in Supabase: {'message': \"Could not find the 'lifecycle_reason' column of 'profiles' in the schema cache\", 'code': 'PGRST204'}"`; `V` stayed `ACTIVE` & `blocked_when_paused = False`. | **FAIL (`DEF-32-001`)** |
| **Archive Founder & Mentor (`ARCHIVED`)** | `AC` (`J/S`) & `Q` (`G/Z`) | Both enter `ARCHIVED`, logins blocked, excluded from Tab 4/caseloads, then restored with original UUIDs & zero auto-reclaim. | **Alert (`AC`):** `PGRST204 ('lifecycle_reason' missing)`. **Alert (`Q`):** `"2 case(s) have no remaining co-guide!"` + **`PGRST204`**, **causing un-rolled-back unassignment of `Q` from `G & Z` despite failed archival!** (`AC & Q` stayed `ACTIVE`; QA re-assigned `Q -> G, Z` cleanly). | **FAIL (`DEF-32-001`)** |
| **Apply Legal Hold** | `AF` | `AF` marked `legal_hold = True`; closure blocked under hold. | **Alert:** `"Failed to update legal hold in Supabase: {'message': \"Could not find the 'lifecycle_reason' column of 'profiles' in the schema cache\", 'code': 'PGRST204'}"`; `legal_hold` remained `False`. | **FAIL (`DEF-32-001`)** |
| **Schedule Closure (30d) & Cancel Deletion** | `AF` | `AF` moves to `PENDING_DELETION`, appears in Subtab 3, then cancelled back to `ACTIVE`. | **Alert:** `"Failed to schedule account deletion in Supabase: {'message': \"Could not find the 'deletion_requested_by' column of 'profiles' in the schema cache\", 'code': 'PGRST204'}"`; `account_status` stayed `ACTIVE`. | **FAIL (`DEF-32-001`)** |

---

## 2. Exact Verified Schema Divergence (`task-982`, `task-1077`, `migrations/009_account_lifecycle_and_archive.sql`)

| Layer | Columns Used by Live Code (`services/account_lifecycle.py`) | Actual Columns in Live Production Supabase (`task-982`) |
|---|---|---|
| **`profiles`** | `lifecycle_reason`, `deletion_requested_by`, `status_updated_at`, `status_updated_by`, `retention_notes` (`read/write`) | **`status_reason`**, `grace_period_days`, `deleted_at`, `archived_at`, `restored_at`, `reactivated_at`, `legal_hold`, `deletion_requested_at`, `deletion_scheduled_for` (NO `lifecycle_reason`, NO `deletion_requested_by`, NO `retention_notes`, NO `status_updated_at/by`) |
| **`account_lifecycle_log`** | `previous_status`, `metadata` | **`old_status`**, **`details`**, `reason`, `action`, `new_status` (NO `previous_status`, NO `metadata`) |

- **Why Automated SQLite Tests & Static Pre-Deploy Checks Missed This:** SQLite `LocalDatabase` mirrors `009`'s column names, and `FULCRUM_PREDEPLOY_CONTRACT_CHECK.py` passed `0 blockers` because it validates against expected/local contracts rather than introspecting the live Supabase REST schema cache on `profiles` / `account_lifecycle_log`.
- **Reproducer:** `DOCUMENTATION/05_TESTING_AND_VERIFICATION/32_USER_360_QA_REPORT/reproducers/test_qa32_discovered_defects.py::test_repro_def_001_lifecycle_supabase_column_mismatch` (`PASSED`).
- **Final Clean State Verification (`d2_report.json`):** `qa_status_issues_count = 0`; **all `32/32` QA accounts are `ACTIVE` (`legal_hold = False`, `deletion_scheduled_for = None`, `0` pending deletions)**.

