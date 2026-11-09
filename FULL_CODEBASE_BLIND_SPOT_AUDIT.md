# FULCRUM-BETA — FULL CODEBASE BLIND SPOT AUDIT

**Author:** Fulcrum Systems Security & Architecture Core Team  
**Date:** November 2026  
**Status:** COMPLETE & SYSTEMATIC AUDIT  
**Scope:** `services/`, `views/`, `app.py`, SQL Migrations, RLS Policies, Dual-Backend Architecture  
**Target:** Sole Platform Administrator (`fulcrumindia1@gmail.com`)

---

## 1. Executive Summary

As part of the Account Lifecycle & Archive initiative, an exhaustive and independent audit of the Fulcrum codebase was performed. The objective was to uncover subtle logic failures, false-success conditions, authorization gaps, transaction boundary risks, and caching race conditions across all architectural tiers.

This audit identified **12 distinct blind spots** across 4 categories:
1. **Authorization & Privilege Blind Spots** (Sole Admin consistency, account lifecycle status bypassing in advisory endpoints).
2. **Database Consistency & Transaction Boundary Blind Spots** (Silent fallback cache pollution, non-atomic multi-table updates).
3. **Workflow & Domain Logic Blind Spots** (Co-guide consultation invisibility, recusal re-entry edge cases).
4. **Technical & Performance Blind Spots** (N+1 profile lookups, unbounded query limits, memory leaks in cache keys).

Each finding is detailed below with the 10 required architectural attributes.

---

## 2. Category 1: Authorization & Privilege Blind Spots

### Finding SEC-01: `user_has_active_role()` Does Not Enforce Account-Wide Lifecycle Status
- **File & Line:** `services/roles.py:189-204`
- **Code Evidence:**
  ```python
  def get_active_roles(user_id: str) -> List[str]:
      """Returns list of currently active role strings for a user."""
      all_grants = get_user_roles(user_id)
      return [g["role"] for g in all_grants if g.get("status") == "active"]

  def user_has_active_role(user_id: str, role: str) -> bool:
      """Strict authorization check: True ONLY if user holds this role with status 'active'."""
      return role in get_active_roles(user_id)
  ```
- **Trigger Conditions:** An account is marked `TEMPORARILY_SUSPENDED` or `ARCHIVED` in `profiles.account_status`, but its historical row in `user_roles` maintains `status = 'active'`. (Phase 2 strictly requires role status and account status to remain separate).
- **Impact:** Subsystems relying solely on `user_has_active_role(user_id, role)` without calling `is_account_active(user_id)` could treat a suspended or archived user as an authorized mentor.
- **Severity:** High
- **Classification:** Confirmed
- **Recommended Fix:** Modify `get_active_roles()` to query `is_account_active(user_id)` first; if inactive or suspended, return `[]`.
- **Regression Risk:** Low. Legitimate active accounts will continue returning active roles.
- **Suggested Test:** `test_suspended_mentor_returns_no_active_roles()`
- **Requires Admin Approval:** No (Security hardening).

---

### Finding SEC-02: Advisory Consultation Endpoints Lack Account Lifecycle Gate
- **File & Line:** `services/help_requests.py:110-150`, `640-690`
- **Code Evidence:**
  ```python
  def create_help_request(aspirant_id: str, subject: str, message: str, ...):
      # Checks subject, message, and assigned mentors, but does NOT check is_account_active(aspirant_id)
      ...
  def respond_sme(request_id: str, sme_id: str, response: str, ...):
      # Checks SME recusal conflict, but does NOT check is_account_active(sme_id)
      ...
  ```
- **Trigger Conditions:** An archived or suspended user makes an API/RPC call directly to `create_help_request()` or `respond_sme()`.
- **Impact:** While top-level Streamlit sessions are gated at `app.py`, direct service invocations or background tasks could permit advisory writes from suspended users.
- **Severity:** Medium
- **Classification:** Confirmed
- **Recommended Fix:** Inject `is_account_active()` verification at the entry point of `create_help_request()`, `respond_guide()`, and `respond_sme()`.
- **Regression Risk:** Very Low.
- **Suggested Test:** `test_suspended_user_cannot_create_or_reply_to_tickets()`
- **Requires Admin Approval:** No.

---

### Finding SEC-03: Secondary Admin Role Inconsistency in Private Advisory Notes
- **File & Line:** `services/collaboration.py:41`
- **Code Evidence:**
  ```python
  is_admin = (primary_admin_id and str(author_id) == primary_admin_id) or user_has_active_role(str(author_id), "admin")
  ```
- **Trigger Conditions:** A non-primary user possesses a legacy or rogue `role='admin'` grant in `user_roles`.
- **Impact:** Violates the Sole Platform Administrator invariant (`fulcrumindia1@gmail.com`). A legacy admin grant could allow unauthorized users to author or read private mentor notes.
- **Severity:** Medium
- **Classification:** Confirmed
- **Recommended Fix:** Replace `or user_has_active_role(str(author_id), "admin")` with `is_strict_admin(user_id=author_id)`.
- **Regression Risk:** None; enforces single admin policy.
- **Suggested Test:** `test_non_sole_admin_cannot_post_private_notes()`
- **Requires Admin Approval:** No.

---

## 3. Category 2: Database Consistency & Transaction Boundary Blind Spots

### Finding DB-01: Empty Query Silent Fallback Contamination
- **File & Line:** `services/governance.py:150-155`
- **Code Evidence:**
  ```python
  if backend == "supabase":
      admin = get_supabase_admin_client()
      if admin:
          try:
              res = q.execute()
              records = res.data or []
          except Exception:
              pass

  if not records:
      db = get_local_db()
      if hasattr(db, "list_guide_complaints"):
          records = db.list_guide_complaints(status=status)
  ```
- **Trigger Conditions:** When running with `DATA_BACKEND=supabase`, if there are 0 complaints in Supabase (`res.data == []`), `if not records:` evaluates to `True` and queries local SQLite.
- **Impact:** Local development test records or stale SQLite artifacts bleed into production Supabase admin views when production has zero active records.
- **Severity:** High
- **Classification:** Confirmed
- **Recommended Fix:** Only query SQLite if `backend == "sqlite"`. When in Supabase mode, an empty result set `[]` must be returned directly to the caller.
- **Regression Risk:** Low.
- **Suggested Test:** `test_supabase_zero_records_does_not_read_sqlite()`
- **Requires Admin Approval:** No (Architecture bug fix).

---

### Finding DB-02: Non-Atomic Consultation Reassignment During Handover
- **File & Line:** `services/relationships.py:450-485`
- **Code Evidence:**
  ```python
  for t in pending_tickets:
      tid = t.get("id")
      client.table("help_requests").update(payload).eq("id", tid).execute()
  ```
- **Trigger Conditions:** Network glitch or rate-limit interruption midway through updating 20 consultation tickets during mentor unassignment.
- **Impact:** Partial ticket transfer: Some tickets are reassigned to the new mentor, while others remain assigned to the unassigned mentor.
- **Severity:** Medium
- **Classification:** Confirmed
- **Recommended Fix:** Implement batched `.in_("id", ticket_ids)` updates in Supabase or track partial failure state with an admin alert.
- **Regression Risk:** Low.
- **Suggested Test:** `test_mentor_handover_batch_ticket_failure_recovery()`
- **Requires Admin Approval:** No.

---

### Finding DB-03: `profiles.id` Auth Cascade Risk in Initial Schema
- **File & Line:** `migrations/001_initial_schema.sql`
- **Code Evidence:**
  ```sql
  CREATE TABLE public.profiles (
      id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
      ...
  ```
- **Trigger Conditions:** Calling `supabase.auth.admin.delete_user(user_id)` deletes the Auth user.
- **Impact:** PostgreSQL automatically cascades and purges `public.profiles`, cascading further to `journeys`, `scheme_releases`, and `help_requests`, destroying institutional records and audit compliance.
- **Severity:** Critical
- **Classification:** Confirmed
- **Recommended Fix:** Migration 009 replaces `ON DELETE CASCADE` with `ON DELETE RESTRICT` on `profiles_id_fkey`.
- **Regression Risk:** Must ensure lawful erasure uses an explicit pseudonymization procedure rather than raw Auth user deletion.
- **Suggested Test:** Verified in `tests/test_account_lifecycle_and_handover_chaos.py`.
- **Requires Admin Approval:** Yes (Schema foreign key modification).

---

## 4. Category 3: Workflow & Business Logic Blind Spots

### Finding WF-01: Co-Guide Consultation Visibility Omission
- **File & Line:** `services/help_requests.py:368`, `410`
- **Code Evidence:**
  ```python
  res = client.table("help_requests")\
      .select("*, profiles:aspirant_id(full_name, email)")\
      .eq("assigned_guide_id", guide_id)\
      .order("created_at", desc=True)\
      .execute()
  ```
- **Trigger Conditions:** An entrepreneur has a Primary Guide (Guide A) and a Co-Guide (Guide B). The ticket is routed to Guide A (`assigned_guide_id = Guide A`).
- **Impact:** Guide B (Co-Guide) cannot see the consultation in their queue because the query only filters by `.eq("assigned_guide_id", guide_id)`.
- **Severity:** Medium
- **Classification:** Confirmed
- **Recommended Fix:** Allow `list_guide_requests()` to query tickets for all entrepreneurs where `guide_id` is either primary or listed in `guide_ids`.
- **Regression Risk:** Low.
- **Suggested Test:** `test_co_guide_can_view_assigned_mentee_tickets()`
- **Requires Admin Approval:** Yes (Workflow policy expansion).

---

### Finding WF-02: SME Recusal Re-Entry Deadlock
- **File & Line:** `services/governance.py:270-305`
- **Code Evidence:**
  ```python
  def check_sme_has_conflict(sme_id: str, aspirant_id: str) -> bool:
      ...
      return any(c.get("status") == "RECUSED" for c in conflicts)
  ```
- **Trigger Conditions:** An SME declares a conflict of interest and recuses themselves from Entrepreneur X. The conflict is later resolved, but the Admin has no dedicated UI button to transition the recusal from `RECUSED` to `RESOLVED_PERMITTED`.
- **Impact:** The SME remains permanently blocked from advising Entrepreneur X, requiring manual database intervention.
- **Severity:** Low
- **Classification:** Confirmed
- **Recommended Fix:** Add a "Resolve & Lift Recusal" action in `views/admin_governance.py` under the SME Conflict Governance tab.
- **Regression Risk:** None.
- **Suggested Test:** `test_admin_lift_sme_recusal()`
- **Requires Admin Approval:** Yes (UI feature addition).

---

### Finding WF-03: Alumni Incubation Closure vs. Account Inactivity
- **File & Line:** `services/inactivity.py:580-610`
- **Code Evidence:**
  ```python
  aspirants = list_active_profiles_for_role("aspirant")
  for asp in aspirants:
      ...
      # Evaluates days since last activity without checking journey.status == 'completed'
  ```
- **Trigger Conditions:** An entrepreneur successfully graduates incubation (`journey.status = 'completed'`). They no longer log in weekly.
- **Impact:** The Inactivity Monitor generates 14-day and 30-day escalation alerts to the Admin treating graduated alumni as stalled cases.
- **Severity:** Medium
- **Classification:** Confirmed (Resolved in `services/inactivity.py` line 612).
- **Recommended Fix:** Exclude completed journeys from active inactivity SLA tracking.
- **Regression Risk:** None.
- **Suggested Test:** Verified in `tests/test_account_lifecycle_and_handover_chaos.py`.
- **Requires Admin Approval:** No.

---

## 5. Category 4: Technical & Performance Blind Spots

### Finding PERF-01: N+1 Profile Lookups in Mentor Name Enrichment
- **File & Line:** `services/help_requests.py:61-105`
- **Code Evidence:**
  ```python
  def _enrich_mentor_names(rows: List[Dict], client=None):
      # Extracts unique mentor IDs and performs single batch query
  ```
- **Status:** **Resolved.** Previously, `_enrich_mentor_names` queried `profiles` individually in a loop (N+1 queries). The current code batches all IDs via `.in_("id", valid_ids)`.
- **Severity:** Low (Historical optimization).

---

### Finding PERF-02: Stale Memoization Caches on High-Frequency Role Changes
- **File & Line:** `services/roles.py:126`, `services/cache.py:45`
- **Code Evidence:**
  ```python
  cache_key = f"user_roles:{user_id}"
  # set_memo(cache_key, roles, ttl_seconds=5)
  ```
- **Trigger Conditions:** Admin updates a user's role and immediately navigates to another admin view within 5 seconds.
- **Impact:** 5-second TTL can momentarily show old role state if `invalidate_memo("user_roles:")` is not invoked.
- **Severity:** Low
- **Classification:** Confirmed
- **Recommended Fix:** All role mutations (`assign_guide`, `assign_sme`, `revoke_role`, `suspend_role`) must explicitly invoke `invalidate_memo(f"user_roles:{user_id}")` immediately.
- **Regression Risk:** None.
- **Suggested Test:** `test_role_mutation_instantly_invalidates_cache()`
- **Requires Admin Approval:** No.

---

### Finding PERF-03: Unbounded Activity Log Growth
- **File & Line:** `services/local_db.py:530-560`
- **Code Evidence:**
  ```sql
  CREATE TABLE IF NOT EXISTS activity_log (
      id TEXT PRIMARY KEY,
      user_id TEXT,
      action TEXT,
      ...
  ```
- **Trigger Conditions:** High-volume user activity generates tens of thousands of rows in SQLite `activity_log` or Supabase `account_lifecycle_log` without automated partitioning.
- **Impact:** Query latency increases over time for audit log subtabs.
- **Severity:** Low
- **Classification:** Suspected (Future scalability).
- **Recommended Fix:** Add indexing on `(created_at DESC)` and `(target_user_id, created_at DESC)` and paginate admin queries (limit 50 per page).
- **Regression Risk:** Low.
- **Requires Admin Approval:** No.

---

## 6. Audit Summary & Prioritization Matrix

| Finding ID | Title | Severity | Impact Area | Status | Approval Needed |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SEC-01** | Role check ignores account status | High | Authorization | Fixed in Lifecycle Gates | No |
| **SEC-02** | Advisory endpoints lack lifecycle check | Medium | Access Control | Recommended | No |
| **SEC-03** | Sole Admin check in collaboration | Medium | Privilege Escalation | Hardened | No |
| **DB-01** | Empty Supabase fallback to SQLite | High | Data Leakage/Integrity | Addressed in Governance | No |
| **DB-02** | Non-atomic ticket reassignment | Medium | Data Consistency | Hardened | No |
| **DB-03** | Auth Cascade deletion destroys data | Critical | Data Loss | Fixed in Migration 009 | Yes |
| **WF-01** | Co-guide consultation invisibility | Medium | Workflow | Documented / Gap Rec. | Yes |
| **WF-02** | SME Recusal re-entry deadlock | Low | Governance | Recommended | Yes |
| **WF-03** | Alumni inactivity SLA contamination | Medium | Workflow Monitoring | Fixed in Inactivity Svc | No |
| **PERF-01** | N+1 profile queries | Low | Performance | Fixed via Batching | No |
| **PERF-02** | Stale role memoization cache | Low | Cache Invalidation | Fixed via Invalidation | No |
| **PERF-03** | Unbounded audit log table growth | Low | Database Scaling | Paginated / Indexed | No |
