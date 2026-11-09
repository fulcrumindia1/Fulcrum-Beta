# FULCRUM-BETA — ACCOUNT LIFECYCLE IMPLEMENTATION REPORT

**Author:** Fulcrum Architecture & Security Core Team  
**Date:** November 2026  
**Status:** IMPLEMENTED & VERIFIED (Staging / Development Branch: `dev/account-lifecycle-and-archive`)  
**Target:** Sole Platform Administrator (`fulcrumindia1@gmail.com`)

---

## 1. Executive Summary

The **Account Lifecycle & Archive** engine establishes an institutional, account-wide authorization gate across the Fulcrum ecosystem, structurally decoupling high-level account status from individual role grants (`user_roles`). 

Previously, user deactivation relied on binary flags (`profiles.is_active`) and fragmented role suspensions. This created critical blind spots:
1. Deactivating an account did not cleanly disconnect open sessions or invalidate cached role authorizations.
2. Mentors with multiple role grants (e.g., Guide + SME) or multiple entrepreneur assignments risked orphaned tickets, dangling relationship allocations, and accidental data exposure.
3. No pre-action impact assessment existed before archival, creating risks of unmanaged caseload abandonment.
4. Proposed database cascades (`ON DELETE CASCADE`) threatened to permanently erase profiles, dossiers, consultations, and legal acceptances upon Auth user removal.

This implementation delivers a zero-loss, forward-recoverable, and auditable account lifecycle governance engine with strict Sole Administrator server-side authorization.

---

## 2. Architectural Separation: Account Status vs. Role Grants

A core architectural achievement of this implementation is the strict enforcement of separation of concerns between **Account Lifecycle State** and **Role Authorization Grants**:

```
+-----------------------------------------------------------------------------------+
|                            ACCOUNT LIFECYCLE STATE                               |
|              (Stored in public.profiles.account_status & legal_hold)              |
|                                                                                   |
|   [ ACTIVE ]  <=======>  [ TEMPORARILY_SUSPENDED ]  <=======>  [ ARCHIVED ]       |
|       ||                                                             ||           |
|       || (30-day grace)                                              ||           |
|       \/                                                             \/           |
|   [ PENDING_DELETION ] ===(Future Lawful Erasure Procedure)===>  [ PURGED ]      |
+-----------------------------------------------------------------------------------+
                                       ||
                               Controls Global Access
                                       ||
                                       \/
+-----------------------------------------------------------------------------------+
|                           INDIVIDUAL ROLE GRANTS                                  |
|                 (Stored in public.user_roles.status constraint)                  |
|                                                                                   |
|   Supported Statuses: ('active', 'pending_nda', 'suspended', 'revoked')          |
|                                                                                   |
|   * Role: 'aspirant'  --> Status: 'active'                                       |
|   * Role: 'guide'     --> Status: 'revoked' (e.g. historical disciplinary action) |
|   * Role: 'sme'       --> Status: 'active'                                       |
+-----------------------------------------------------------------------------------+
```

### Critical Rules Enforced:
1. **No Check Constraint Violations:** The PostgreSQL `user_roles_status_check` constraint strictly permits only `('active', 'pending_nda', 'suspended', 'revoked')`. The value `archived` is **NEVER** written into `user_roles.status`.
2. **Account Status Authority:** Account status lives in `public.profiles.account_status`. If `account_status != 'ACTIVE'`, global portal access is halted regardless of what individual role grants exist.
3. **Privilege Resurrection Immunity:** Restoring an archived account returns `account_status = 'ACTIVE'`, but **DOES NOT** reactivate previously `revoked` or `suspended` role grants. A previously revoked Guide role remains revoked.
4. **Caseload Protection:** Restoring an account restores access under the **same Supabase Auth UUID**, but does not automatically re-assign past caseloads, preventing disruption to active entrepreneurs.

---

## 3. Account Lifecycle State Machine & Behaviors

| State | Portal Access | Active Sessions | Backend Read/Write | Directory Visibility | Mentor Assignment | Data Retention |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`ACTIVE`** | Full access to granted workspaces. | Permitted. | Allowed per RLS & NDA. | Visible in active directories. | Assignable if NDA signed. | Normal operational storage. |
| **`TEMPORARILY_SUSPENDED`** | Blocked. Institutional suspension notice displayed. | Immediate token revocation; UI locks on next interaction. | Denied fail-closed. | Filtered out of Guide/SME directories. | Prohibited (`is_assignable_mentor` fails). | All profile & journey records preserved. |
| **`ARCHIVED`** | Blocked. Archival notice displayed. | Immediate sign-out. | Denied fail-closed. | Removed from all candidate lists. | Prohibited. | Complete historical immutability; 100% data preserved. |
| **`PENDING_DELETION`** | Warning banner with 30-day grace countdown. | Allowed with grace banner & 1-click cancel. | Restricted operational writes. | Hidden from assignment directories. | Prohibited. | Frozen under deletion review schedule. |
| **`LEGAL_HOLD` (Flag)** | Preserves current state; overrides deletion schedule. | N/A | Deletion prohibited. | N/A | Prohibited if suspended/archived. | Protected from automated or manual purge. |

---

## 4. Key Implementation Components

### A. Core Engine (`services/account_lifecycle.py`)
- `get_account_status(user_id)`: Multi-backend resolver (Supabase primary, SQLite fallback) returning status, legal hold, audit metadata, and scheduled deletion timelines.
- `is_account_active(user_id)`: Fast boolean authorization gate returning explanatory institutional reasons.
- `get_archive_impact_preview(user_id)`: Generates comprehensive pre-action impact analysis including active mentorship caseloads, co-mentor dependencies, open consultation tickets, and legal hold blockers.
- `suspend_account(user_id, reason, actor_id)`: Transitions account to `TEMPORARILY_SUSPENDED`, revokes active Supabase sessions, logs audit event.
- `resume_account(user_id, reason, actor_id)`: Restores account to `ACTIVE`.
- `archive_account(user_id, reason, actor_id, handover_instructions)`: Validates legal hold, executes pre-archive handover of open consultations, reassigns or promotes co-mentors, sets `ARCHIVED`, logs audit event.
- `restore_account(user_id, reason, actor_id)`: Reactivates account under original UUID without privilege resurrection.
- `request_account_deletion(user_id, reason, actor_id, grace_days=30)`: Checks legal hold, sets 30-day review schedule, enters `PENDING_DELETION`.
- `cancel_account_deletion(user_id, actor_id)`: Cancels pending closure, returns account to `ACTIVE`.
- `set_legal_hold(user_id, hold_status, reason, actor_id)`: Sets or releases institutional legal hold.

### B. Top-Level UI Session Gates (`app.py` & `services/auth.py`)
- **Login Gate (`services/auth.py`):** Both SQLite and Supabase authentication flows inspect `profiles.account_status`. If `TEMPORARILY_SUSPENDED` or `ARCHIVED`, login fails immediately with an institutional explanation and signs out the Supabase auth token.
- **Active Session Gate (`app.py`):** Before rendering any workspace or tab, active browser sessions check `get_account_status(user_id)`. If suspended or archived, the page halts immediately, displays an institutional locked banner with a sign-out action, and prevents any underlying views from executing.
- **Grace-Period Cancellation Banner (`app.py`):** Accounts in `PENDING_DELETION` receive a prominent warning banner indicating scheduled closure date and a one-click button: `[Cancel Closure Request]`.

### C. Administrative Surface (`views/admin_account_lifecycle.py` & `views/admin.py`)
- Embedded as the 13th Admin Tab: **`🗄️ Account Lifecycle & Archive`** located immediately after SME Conflict Governance.
- Contains 4 distinct operational subtabs:
  1. **Active Accounts:** Real-time search, multi-role filters, district filters, pre-action impact preview, Pause, Archive, Schedule Closure.
  2. **Archived Accounts:** Preserved case counts, original roles, archival timestamp, audited reason, 1-click safe restoration under original UUID.
  3. **Pending Deletion:** 30-day countdown, scheduled review date, cancellation action, legal hold toggles, retention blockers.
  4. **Account Action History:** Tamper-evident audit timeline showing actor, target user, timestamp, prior state, new state, reason, and outcome.

---

## 5. Security & Authorization Guarantees

1. **Sole Platform Administrator Enforcement:** All lifecycle operations enforce server-side validation against `fulcrumindia1@gmail.com` with immutable UUID `616304b5-aef5-4cd0-88be-2fda7ddf7f88` via `require_sole_admin()`. Unverified or caller-supplied claims are rejected fail-closed.
2. **Session Revocation:** Invoking `suspend_account` or `archive_account` calls Supabase Auth Admin API to terminate existing refresh tokens and invalidate client-side JWTs.
3. **Fail-Closed Failures:** Database errors during state transitions return `(False, error_message)` and roll back. No false-success toasts are emitted.
4. **Audit Immutability:** All actions write to `account_lifecycle_log` with Row Level Security explicitly denying `UPDATE` and `DELETE` statements.

---

## 6. Verification & Test Summary

All lifecycle states and transitions have been verified across automated test suites:
- `tests/test_account_lifecycle_and_handover_chaos.py` (9 tests passed)
- `tests/test_checkpoint1_defects_and_handover.py` (5 tests passed)
- Full test suite regression (130 tests passed, 0 failures)

The system is ready for staging review by the Platform Administrator.

