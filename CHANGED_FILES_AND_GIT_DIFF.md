# FULCRUM-BETA — CHANGED FILES & GIT DIFF AUDIT

**Author:** Fulcrum Systems Engineering Team  
**Date:** November 2026  
**Branch:** `dev/account-lifecycle-and-archive`  
**Target:** Sole Platform Administrator (`fulcrumindia1@gmail.com`)

---

## 1. Summary of Changes

To implement the **Account Lifecycle & Archive** engine, repair mentor revocation defects, eliminate silent fallbacks, and quarantine destructive cleanup scripts, a targeted set of files was created and updated:

| Category | File Path | Status | Key Purpose |
| :--- | :--- | :---: | :--- |
| **New Core Service** | `services/account_lifecycle.py` | **NEW** | Account lifecycle state machine, status resolver, impact preview, archival, restoration, 30-day deletion grace, legal hold, and audit logging. |
| **New Admin UI** | `views/admin_account_lifecycle.py` | **NEW** | 4-subtab Admin UI: Active Accounts, Archived Accounts, Pending Deletion, Account Action History. |
| **New Migration** | `migrations/009_account_lifecycle_and_archive.sql` | **NEW** | 100% additive SQL migration: 7 profile lifecycle columns, `account_lifecycle_log` table, `ON DELETE RESTRICT` constraint. |
| **New Migration Root**| `MIGRATION_009_REVISED.sql` | **NEW** | Root copy for convenient inspection and staging review. |
| **New Chaos Tests** | `tests/test_account_lifecycle_and_handover_chaos.py` | **NEW** | 9 chaos and edge-case tests validating handovers, cascades, promotions, and grace cancellations. |
| **App Entrypoint** | `app.py` | **MODIFIED** | Active session locked banner for suspended/archived users; 30-day grace cancellation banner; mounted Tab 13. |
| **Core Relationships**| `services/relationships.py` | **MODIFIED** | Co-mentor promotion on unassignment, `replace_target_id` single replacement, consultation transfer/queuing, Sole Admin check. |
| **Roles & Permissions**| `services/roles.py` | **MODIFIED** | `is_assignable_mentor()` validator, `guide_ids`/`sme_ids` cleanup in `revoke_role()`, fail-closed error reporting. |
| **Photo Security** | `services/aspirant_photos.py` | **MODIFIED** | Removed silent SQLite fallback on cloud storage upload errors; fail-closed error returns. |
| **Authentication** | `services/auth.py` | **MODIFIED** | Login status gate blocking `TEMPORARILY_SUSPENDED` and `ARCHIVED` logins in both SQLite and Supabase paths. |
| **Local Database** | `services/local_db.py` | **MODIFIED** | Dynamic schema auto-migration for 9 lifecycle columns, `account_lifecycle_log` table, status helpers. |
| **Profile Queries** | `services/profiles.py` | **MODIFIED** | `list_profiles_by_role()` excludes accounts where `account_status != 'ACTIVE'`. |
| **Journey Workflow** | `services/journey.py` | **MODIFIED** | Added `mark_journey_completed()` for Case Completed / Alumni workflow without disabling user accounts. |
| **Inactivity Monitor**| `services/inactivity.py` | **MODIFIED** | Excluded archived and suspended founders and completed journeys from SLA escalations. |
| **Admin Views** | `views/admin.py` | **MODIFIED** | Added 13th tab `"🗄️ Account Lifecycle & Archive"`. |
| **Admin Governance**| `views/admin_governance.py` | **MODIFIED** | Cleaned up role checks to support multi-role mentors. |
| **Quarantined Script**| `scripts/remove_requested_accounts.py` | **MODIFIED** | Quarantined; removed hardcoded email deletion list; fatal exit on execution. |
| **Git Configuration** | `.gitignore` | **MODIFIED** | Added `brain/` to prevent screenshot and scratch artifact leaks. |

---

## 2. Key Git Diff Excerpts

### A. Quarantining Destructive Account Deletion Script
`scripts/remove_requested_accounts.py`:
```diff
- EMAILS_TO_REMOVE = [
-     "test_user1@example.com",
-     "mentor_old@example.com",
-     ...
- ]
+ # Hardcoded operational deletion lists are strictly cleared
+ EMAILS_TO_REMOVE = []
+ 
+ def main():
+     print("FATAL ERROR: Direct account deletion script is QUARANTINED and disabled.")
+     print("Direct execution of account purging is prohibited by institutional policy.")
+     print("Refer to services/account_lifecycle.py for audited account lifecycle management.")
+     sys.exit(1)
```

### B. Co-Guide & SME Revocation Fix
`services/roles.py`:
```diff
  # Inspect both raw keys (guide_ids, sme_ids) and expanded keys (guides, smes)
- if role == "guide" and mentor_id in [g.get("id") for g in rel.get("guides", [])]:
+ raw_gids = rel.get("guide_ids") or []
+ if isinstance(raw_gids, str):
+     try: raw_gids = json.loads(raw_gids)
+     except Exception: raw_gids = []
+ if mentor_id in raw_gids or (rel.get("guide_id") == mentor_id):
+     unassign_guide(rel["aspirant_id"], mentor_id, admin_id=admin_id)
```

### C. Eliminating Silent SQLite Fallback on Cloud Storage Failure
`services/aspirant_photos.py`:
```diff
      except Exception as e:
-         print(f"Cloud upload failed: {e}. Falling back to SQLite.")
-         get_local_db().save_photo(user_id, photo_bytes)
-         return True, None
+         print(f"[AspirantPhotos] Cloud storage upload failed: {e}")
+         return False, f"Failed to persist profile photo to cloud storage: {e}"
```

### D. Safe Foreign Key Constraint (`ON DELETE RESTRICT`)
`migrations/009_account_lifecycle_and_archive.sql`:
```diff
+ ALTER TABLE public.profiles
+     DROP CONSTRAINT IF EXISTS profiles_id_fkey,
+     ADD CONSTRAINT profiles_id_fkey 
+     FOREIGN KEY (id) REFERENCES auth.users(id) ON DELETE RESTRICT;
```

### E. Account Lifecycle Session Gate
`app.py`:
```diff
+ # Check Account Lifecycle Gate for Active Sessions
+ from services.account_lifecycle import get_account_status
+ acc_details = get_account_status(user["id"])
+ acc_st = acc_details.get("account_status", "ACTIVE")
+ 
+ if acc_st in ("TEMPORARILY_SUSPENDED", "ARCHIVED"):
+     # Display institutional locked banner and HALT view rendering
+     st.markdown(render_account_locked_banner(acc_details))
+     if st.button("Sign Out"):
+         st.session_state.clear()
+         st.rerun()
+     st.stop()
```

