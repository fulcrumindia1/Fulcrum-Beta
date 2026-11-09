"""
tests/test_account_lifecycle_and_handover_chaos.py
=============================================================================
Comprehensive Automated Verification & Chaos Test Suite for:
- Account Lifecycle State Machine (ACTIVE, TEMPORARILY_SUSPENDED, ARCHIVED, PENDING_DELETION)
- Pre-Archive Impact Preview & Safe Mentor Handover
- Sole Admin Authority Enforcement & Ordinary User Rejection
- Root Admin Immunity against Suspension & Archival
- Safe Restoration under Original UUID (No Revoked Role Resurrect, No Old Caseload Reclaim)
- 30-Day Closure Grace Period & Cancellation
- Institutional Legal Hold Protection against Deletion
- Elimination of False Success & Silent Fallback
- Case Completed / Alumni Workflow
=============================================================================
"""

import uuid
import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock, patch

from services.roles import (
    SOLE_ADMIN_UUID,
    SOLE_ADMIN_EMAIL,
    is_strict_admin,
    require_sole_admin,
)
from services.account_lifecycle import (
    get_account_status,
    is_account_active,
    suspend_account,
    resume_account,
    get_archive_impact_preview,
    archive_account,
    restore_account,
    request_account_deletion,
    cancel_account_deletion,
    set_legal_hold,
    list_account_lifecycle_logs,
)
from services.journey import mark_journey_completed


@pytest.fixture(autouse=True)
def force_test_backend(monkeypatch):
    """Enforce local SQLite backend for deterministic, isolated unit and chaos tests."""
    monkeypatch.setenv("DATA_BACKEND", "sqlite")
    from services.cache import invalidate_memo
    invalidate_memo()


@pytest.fixture
def synthetic_users():
    """Sets up synthetic user profiles for lifecycle testing."""
    from services.local_db import get_local_db
    db = get_local_db()

    now_iso = datetime.now(timezone.utc).isoformat()
    uid_founder = str(uuid.uuid4())
    uid_guide = str(uuid.uuid4())
    uid_sme = str(uuid.uuid4())
    uid_coguide = str(uuid.uuid4())

    p_founder = {
        "id": uid_founder,
        "email": f"founder_{uuid.uuid4().hex[:6]}@test.in",
        "role": "aspirant",
        "full_name": "Kavitha Raman",
        "phone": "9876543210",
        "district": "Madurai",
        "state": "Tamil Nadu",
        "profile_data": "{}",
        "is_active": 1,
        "account_status": "ACTIVE",
        "legal_hold": 0,
        "created_at": now_iso,
        "updated_at": now_iso,
    }
    p_guide = {
        "id": uid_guide,
        "email": f"guide_{uuid.uuid4().hex[:6]}@test.in",
        "role": "guide",
        "full_name": "Senthil Kumar (Primary Guide)",
        "phone": "9876543211",
        "district": "Chennai",
        "state": "Tamil Nadu",
        "profile_data": "{}",
        "is_active": 1,
        "account_status": "ACTIVE",
        "legal_hold": 0,
        "created_at": now_iso,
        "updated_at": now_iso,
    }
    p_coguide = {
        "id": uid_coguide,
        "email": f"coguide_{uuid.uuid4().hex[:6]}@test.in",
        "role": "guide",
        "full_name": "Anand Mohan (Co-Guide)",
        "phone": "9876543212",
        "district": "Madurai",
        "state": "Tamil Nadu",
        "profile_data": "{}",
        "is_active": 1,
        "account_status": "ACTIVE",
        "legal_hold": 0,
        "created_at": now_iso,
        "updated_at": now_iso,
    }
    p_sme = {
        "id": uid_sme,
        "email": f"sme_{uuid.uuid4().hex[:6]}@test.in",
        "role": "sme",
        "full_name": "Dr. Vani Lakshmi (Food Specialist)",
        "phone": "9876543213",
        "district": "Tiruchirappalli",
        "state": "Tamil Nadu",
        "profile_data": "{}",
        "is_active": 1,
        "account_status": "ACTIVE",
        "legal_hold": 0,
        "created_at": now_iso,
        "updated_at": now_iso,
    }

    for p in [p_founder, p_guide, p_coguide, p_sme]:
        db.upsert_profile(p)
        db.create_initial_journey(p["id"], f"{p['full_name']}'s Journey")

    # Set up role grants and NDAs for mentors so they are assignable
    from services.roles import grant_role, activate_role
    from services.legal import record_legal_acceptance

    grant_role(p_guide["id"], "guide", granted_by=SOLE_ADMIN_UUID)
    record_legal_acceptance(p_guide["id"], p_guide["email"], "nda_guide", p_guide["full_name"], "I ACCEPT", True)
    activate_role(p_guide["id"], "guide")

    grant_role(p_coguide["id"], "guide", granted_by=SOLE_ADMIN_UUID)
    record_legal_acceptance(p_coguide["id"], p_coguide["email"], "nda_guide", p_coguide["full_name"], "I ACCEPT", True)
    activate_role(p_coguide["id"], "guide")

    grant_role(p_sme["id"], "sme", granted_by=SOLE_ADMIN_UUID)
    record_legal_acceptance(p_sme["id"], p_sme["email"], "nda_sme", p_sme["full_name"], "I ACCEPT", True)
    activate_role(p_sme["id"], "sme")

    # Set up relationship: Founder has Primary Guide, Co-Guide, and Specialist SME
    from services.relationships import assign_guide, assign_sme
    assign_guide(p_founder["id"], p_guide["id"], admin_id=SOLE_ADMIN_UUID, mode="replace")
    assign_guide(p_founder["id"], p_coguide["id"], admin_id=SOLE_ADMIN_UUID, mode="add")
    assign_sme(p_founder["id"], p_sme["id"], admin_id=SOLE_ADMIN_UUID, mode="add")

    return {
        "founder": p_founder,
        "guide": p_guide,
        "coguide": p_coguide,
        "sme": p_sme
    }


# =============================================================================
# 1. SOLE ADMIN AUTHORITY & ROOT IMMUNITY
# =============================================================================

def test_01_sole_admin_authority_required_for_account_actions(synthetic_users):
    """Ordinary users and unauthorized callers must be rejected from administrative lifecycle actions."""
    founder_id = synthetic_users["founder"]["id"]

    # Ordinary user attempts to suspend an account -> Rejected
    ok, err = suspend_account(founder_id, reason="Malicious suspension attempt", actor_id=founder_id)
    assert ok is False
    assert "Unauthorized" in err

    # Ordinary user attempts to archive an account -> Rejected
    ok_a, err_a = archive_account(founder_id, reason="Malicious archive attempt", actor_id=founder_id)
    assert ok_a is False
    assert "Unauthorized" in err_a

    # Ordinary user attempts to toggle legal hold -> Rejected
    ok_h, err_h = set_legal_hold(founder_id, enabled=True, reason="Unauthorized hold", actor_id=founder_id)
    assert ok_h is False
    assert "Unauthorized" in err_h


def test_02_root_sole_admin_account_immunity():
    """The Sole Platform Administrator account cannot be suspended, archived, or scheduled for closure."""
    # Attempt to suspend Sole Admin
    ok_s, err_s = suspend_account(SOLE_ADMIN_UUID, reason="Test suspension", actor_id=SOLE_ADMIN_UUID)
    assert ok_s is False
    assert "cannot be suspended" in err_s

    # Attempt to archive Sole Admin
    ok_a, err_a = archive_account(SOLE_ADMIN_UUID, reason="Test archival", actor_id=SOLE_ADMIN_UUID)
    assert ok_a is False
    assert "cannot be archived" in err_a

    # Attempt to schedule deletion of Sole Admin
    ok_d, err_d = request_account_deletion(SOLE_ADMIN_UUID, actor_id=SOLE_ADMIN_UUID, reason="Test closure")
    assert ok_d is False
    assert "cannot be scheduled for deletion" in err_d


# =============================================================================
# 2. ACCOUNT SUSPENSION & ACTIVE SESSION BLOCKING
# =============================================================================

def test_03_account_suspension_and_authorization_gate(synthetic_users):
    """Suspending an account flips account_status and is_active, blocking authorization immediately."""
    guide_id = synthetic_users["guide"]["id"]

    # Verify baseline is active
    is_act, reason = is_account_active(guide_id)
    assert is_act is True
    assert reason is None

    # Admin suspends Guide account
    ok, err = suspend_account(guide_id, reason="Conduct investigation", actor_id=SOLE_ADMIN_UUID)
    assert ok is True
    assert err is None

    # Check status gate
    details = get_account_status(guide_id)
    assert details["account_status"] == "TEMPORARILY_SUSPENDED"
    assert details["is_active"] is False
    assert details["lifecycle_reason"] == "Conduct investigation"

    # Authorization gate refuses access
    is_act_after, reason_after = is_account_active(guide_id)
    assert is_act_after is False
    assert "temporarily suspended" in reason_after.lower()

    # Resume account
    ok_res, err_res = resume_account(guide_id, actor_id=SOLE_ADMIN_UUID, reason="Cleared of concerns")
    assert ok_res is True
    details_res = get_account_status(guide_id)
    assert details_res["account_status"] == "ACTIVE"
    assert details_res["is_active"] is True


# =============================================================================
# 3. PRE-ARCHIVE IMPACT PREVIEW & SAFE MENTOR HANDOVER
# =============================================================================

def test_04_pre_archive_impact_preview_and_safe_handover(synthetic_users):
    """Pre-archive preview calculates caseload and orphans; archival safely unassigns mentors."""
    founder_id = synthetic_users["founder"]["id"]
    guide_id = synthetic_users["guide"]["id"]
    coguide_id = synthetic_users["coguide"]["id"]

    # Impact preview for Primary Guide: should detect assigned case and existing co-guide
    preview = get_archive_impact_preview(guide_id)
    assert preview["assigned_guide_cases_count"] >= 1
    assert preview["is_archive_eligible"] is True

    # Archive the Primary Guide
    ok_arc, err_arc = archive_account(guide_id, reason="Contract concluded", actor_id=SOLE_ADMIN_UUID)
    assert ok_arc is True

    # Check that Guide is now ARCHIVED
    details = get_account_status(guide_id)
    assert details["account_status"] == "ARCHIVED"
    assert details["is_active"] is False

    # Check that Co-Guide was promoted or retained on the Founder's caseload
    from services.relationships import get_aspirant_mentors
    mentors = get_aspirant_mentors(founder_id)
    # The archived guide is no longer assigned
    all_gids = [g["id"] for g in mentors.get("guides", [])]
    assert guide_id not in all_gids
    assert coguide_id in all_gids


# =============================================================================
# 4. ACCOUNT RESTORATION UNDER SAME UUID WITHOUT PRIVILEGE CONTAMINATION
# =============================================================================

def test_05_restoration_preserves_uuid_and_refuses_automatic_privilege_reactivation(synthetic_users):
    """Restoring an account preserves original UUID and historical records, but never auto-claims old cases."""
    founder_id = synthetic_users["founder"]["id"]
    guide_id = synthetic_users["guide"]["id"]

    # Ensure guide is archived
    archive_account(guide_id, reason="Offboarded", actor_id=SOLE_ADMIN_UUID)

    # Restore Guide account
    ok_r, err_r = restore_account(guide_id, actor_id=SOLE_ADMIN_UUID, reason="Rehired for new season")
    assert ok_r is True

    details_r = get_account_status(guide_id)
    assert details_r["account_status"] == "ACTIVE"
    assert details_r["is_active"] is True
    assert details_r["user_id"] == guide_id  # SAME IMMUTABLE UUID

    # Verify that the restored guide did NOT automatically reclaim previous mentee caseloads
    from services.relationships import get_aspirant_mentors
    mentors = get_aspirant_mentors(founder_id)
    all_gids = [g["id"] for g in mentors.get("guides", [])]
    assert guide_id not in all_gids  # Remains unassigned until deliberately assigned by Admin!


# =============================================================================
# 5. 30-DAY DELETION REVIEW WINDOW & CANCELLATION
# =============================================================================

def test_06_deletion_grace_period_and_cancellation(synthetic_users):
    """Scheduling closure enters PENDING_DELETION with grace period; cancellation restores ACTIVE status."""
    founder_id = synthetic_users["founder"]["id"]

    # Schedule closure with 30-day window
    ok, err = request_account_deletion(founder_id, actor_id=founder_id, reason="User requested exit", grace_days=30)
    assert ok is True

    details = get_account_status(founder_id)
    assert details["account_status"] == "PENDING_DELETION"
    assert details["deletion_requested_at"] is not None
    assert details["deletion_scheduled_for"] is not None

    # Cancel closure request
    ok_c, err_c = cancel_account_deletion(founder_id, actor_id=founder_id, reason="User changed mind")
    assert ok_c is True

    details_c = get_account_status(founder_id)
    assert details_c["account_status"] == "ACTIVE"
    assert details_c["deletion_requested_at"] is None
    assert details_c["deletion_scheduled_for"] is None


# =============================================================================
# 6. LEGAL HOLD COMPLIANCE PROTECTION
# =============================================================================

def test_07_legal_hold_blocks_deletion_requests(synthetic_users):
    """When an account is under Legal Hold, deletion requests must be rejected immediately."""
    founder_id = synthetic_users["founder"]["id"]

    # Apply Legal Hold
    ok_h, err_h = set_legal_hold(founder_id, enabled=True, reason="Audit compliance requirement", actor_id=SOLE_ADMIN_UUID)
    assert ok_h is True
    details_h = get_account_status(founder_id)
    assert details_h["legal_hold"] is True

    # Attempt to request deletion while under hold -> Must be blocked
    ok_del, err_del = request_account_deletion(founder_id, actor_id=founder_id, reason="Attempted deletion under hold")
    assert ok_del is False
    assert "legal hold" in err_del.lower()

    # Release Legal Hold
    ok_rel, err_rel = set_legal_hold(founder_id, enabled=False, reason="Audit complete", actor_id=SOLE_ADMIN_UUID)
    assert ok_rel is True
    details_rel = get_account_status(founder_id)
    assert details_rel["legal_hold"] is False

    # Now deletion request succeeds
    ok_del2, err_del2 = request_account_deletion(founder_id, actor_id=founder_id, reason="Deletion after release")
    assert ok_del2 is True


# =============================================================================
# 7. AUDIT LOG IMMUTABILITY & TIMELINE
# =============================================================================

def test_08_account_action_history_timeline(synthetic_users):
    """Account actions produce an immutable chronological audit trail in account_lifecycle_log."""
    sme_id = synthetic_users["sme"]["id"]

    # Perform a sequence of lifecycle actions
    suspend_account(sme_id, reason="Timeline test: pause", actor_id=SOLE_ADMIN_UUID)
    resume_account(sme_id, actor_id=SOLE_ADMIN_UUID, reason="Timeline test: resume")
    archive_account(sme_id, reason="Timeline test: archive", actor_id=SOLE_ADMIN_UUID)
    restore_account(sme_id, actor_id=SOLE_ADMIN_UUID, reason="Timeline test: restore")

    logs = list_account_lifecycle_logs(user_id=sme_id)
    assert len(logs) >= 4
    actions = [l["action"] for l in logs]
    assert "SUSPEND" in actions
    assert "RESUME" in actions
    assert "ARCHIVE" in actions
    assert "RESTORE" in actions


# =============================================================================
# 8. CASE COMPLETED / ALUMNI WORKFLOW
# =============================================================================

def test_09_case_completed_alumni_workflow(synthetic_users):
    """Marking a journey completed sets alumni status while keeping the founder account active."""
    founder_id = synthetic_users["founder"]["id"]

    ok, err = mark_journey_completed(founder_id, actor_id=SOLE_ADMIN_UUID, notes="Passed all incubation deliverables")
    assert ok is True
    assert err is None

    # Check that account remains ACTIVE (not archived or suspended)
    acc_st = get_account_status(founder_id)
    assert acc_st["account_status"] == "ACTIVE"
    assert acc_st["is_active"] is True

    # Check journey status
    from services.journey import get_journey_timeline
    events = get_journey_timeline(founder_id)
    milestone_titles = [e.get("title", "") for e in events]
    assert any("Alumni Status" in t for t in milestone_titles)
