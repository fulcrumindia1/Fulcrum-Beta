# FULCRUM-BETA — SAFE MENTOR HANDOVER & REVOCATION FIXES

**Author:** Fulcrum Systems Engineering Team  
**Date:** November 2026  
**Status:** IMPLEMENTED & TESTED (Branch: `dev/account-lifecycle-and-archive`)  
**Target:** Sole Platform Administrator (`fulcrumindia1@gmail.com`)

---

## 1. Defect Analysis & Root Causes

### Defect 1: Dictionary Key Discrepancy in Role Revocation
- **The Bug:** In `services/roles.py`, `revoke_role()` checked `rel.get("guides", [])` and `rel.get("smes", [])` when iterating over raw relationship records. However, raw database rows from `relationships` store mentor arrays in `guide_ids` and `sme_ids` (as JSON or lists).
- **The Impact:** When an Admin revoked a Guide or SME role, the system failed to identify and unassign co-guides and additional SMEs. As a result, revoked mentors remained assigned in the underlying relationship arrays, creating dangling assignments and potential authorization leaks.
- **Permanent Fix:**
  - Rewrote relationship inspection in `services/roles.py` to inspect both raw keys (`guide_ids`, `sme_ids`) and expanded dictionary keys (`guides`, `smes`).
  - Implemented automatic extraction regardless of whether values are stored as native Python lists or serialized JSON strings.
  - Revocation of a professional role now processes all assignments across all entrepreneurs where the user was assigned as primary or co-mentor.

### Defect 2: Co-Mentor Wiping During Single Mentor Replacement
- **The Bug:** `assign_guide()` and `assign_sme()` previously replaced the primary mentor by writing `guide_id` or `sme_id`, but often overwrote or emptied the supplementary mentor arrays (`guide_ids`, `sme_ids`).
- **Permanent Fix:**
  - Added `replace_target_id` parameter to `services/relationships.py`. When an Admin replaces a specific co-mentor, only that mentor is swapped out; remaining primary and co-mentors are preserved.
  - Implemented promotion logic: If a primary guide is unassigned, the first available co-guide is automatically promoted to primary `guide_id`, and removed from `guide_ids`.

### Defect 3: Dangling Consultation Tickets & Silent Failures
- **The Bug:** During mentor unassignment or handover, outstanding consultation tickets (`help_requests`) assigned to the outgoing mentor were either left pointing to the removed mentor or silently failed during update.
- **Permanent Fix:**
  - `services/relationships.py` now queries all active/open help requests assigned to the outgoing mentor (`STATUS_OPEN`, `STATUS_IN_PROGRESS`, `STATUS_WAITING_ON_GUIDE_SME`).
  - If a successor mentor is designated or promoted, tickets are systematically transferred with an audited follow-up note.
  - If no successor mentor exists, tickets are moved to `assigned_guide_id = None` or `assigned_sme_id = None` and queued for Admin reassignment (`status = STATUS_ESCALATED`), ensuring no entrepreneur is left in an unhandled deadlock.

---

## 2. Supported Mentorship Topologies

The system now fully supports all complex multi-mentor arrangements:

```
                                  [ ENTREPRENEUR ]
                                         |
         +-------------------------------+-------------------------------+
         |                                                               |
  [ GUIDE PANEL ]                                                 [ SME PANEL ]
         |                                                               |
    +----+----+                                                     +----+----+
    |         |                                                     |         |
[Primary] [Co-Guide]                                            [Primary] [Add'l SME]
 Guide A   Guide B                                                SME X     SME Y
```

### Full Matrix of Supported Topologies:
1. **Primary Guide Only:** Solo guide with full case oversight.
2. **Primary Guide + Co-Guide(s):** Primary guide aided by one or more co-guides. Co-guides share case visibility while primary maintains primary responsibility.
3. **Primary SME Only:** Specialized technical advisory.
4. **Primary SME + Additional SME(s):** Multi-disciplinary domain panel (e.g., AgriTech legal specialist + IoT hardware engineer).
5. **Hybrid Guide + SME Users:** Single professional holding both Guide and SME role grants across different (or same) entrepreneurs. Revoking the SME role unassigns them from SME panels while preserving Guide assignments.
6. **One-to-Many Caseloads:** Single mentor assigned to multiple entrepreneurs across multiple districts. Archiving or revoking the mentor safely iterates and unassigns them from all rosters.

---

## 3. Fail-Safe Handover Workflow

When executing a mentor handover or revocation, the system follows this strict execution pipeline:

```
[ Sole Admin Invokes Handover / Revocation ]
                    |
                    v
    [ Verify Sole Admin Identity ] (fulcrumindia1@gmail.com)
                    |
                    v
    [ Inspect Active Caseload & Open Tickets ]
                    |
                    v
    [ Collect Remaining Co-Mentors ]
         |
         +---> If Co-Mentor exists: Promote Co-Mentor to Primary
         |
         +---> If No Co-Mentor: Unassign; Set status to Unassigned
                    |
                    v
    [ Transfer or Queue Open Consultations ]
         |
         +---> Outstanding tickets updated with successor ID
         |
         +---> If no successor: Update tickets to unassigned & escalate to Admin
                    |
                    v
    [ Update Relationship Record & Assignment History ]
         |
         +---> Insert immutable record into assignment_history
                    |
                    v
    [ Invalidate Role, Relationship & Ticket Caches ]
                    |
                    v
    [ Send Non-Duplicative Notifications to Affected Parties ]
                    |
                    v
    [ Return Confirmed Transaction Result to Admin ]
```

---

## 4. Elimination of False-Success & Silent Fallbacks

In production environments running `DATA_BACKEND=supabase`:
1. **No Silent SQLite Fallbacks:** Operations do not fall back to local SQLite and report success when Supabase returns an error. If a write fails in Supabase, the function returns `(False, "Supabase write error: ...")` fail-closed.
2. **Photo Storage Hardening (`services/aspirant_photos.py`):** Eliminated the legacy fallback that silently wrote photos to SQLite when cloud storage was unreachable. Photo uploads fail cleanly with informative error messages.
3. **Roles Service Error Reporting (`services/roles.py`):** `suspend_role()` and `reinstate_role()` return explicit database error messages instead of swallowing exceptions.

---

## 5. Automated Verification Results

The safe handover engine has been validated by automated tests:

### Test Execution Log:
```
tests/test_checkpoint1_defects_and_handover.py::test_chk1_co_guide_revocation_cleans_guide_ids PASSED
tests/test_checkpoint1_defects_and_handover.py::test_chk1_sme_revocation_cleans_sme_ids PASSED
tests/test_checkpoint1_defects_and_handover.py::test_chk1_hybrid_role_revocation_isolation PASSED
tests/test_checkpoint1_defects_and_handover.py::test_chk1_unauthorized_admin_rejected PASSED
tests/test_checkpoint1_defects_and_handover.py::test_chk1_mentor_handover_transfers_consultations PASSED
tests/test_account_lifecycle_and_handover_chaos.py::test_chaos_01_co_mentor_promotion_on_primary_unassign PASSED
tests/test_account_lifecycle_and_handover_chaos.py::test_chaos_02_pre_archive_handover_caseload_transfer PASSED
tests/test_account_lifecycle_and_handover_chaos.py::test_chaos_03_handover_consultation_queuing_when_no_successor PASSED
tests/test_account_lifecycle_and_handover_chaos.py::test_chaos_04_idempotent_handover_retries_no_duplicate_history PASSED

Results: 9 passed, 0 failed
```

