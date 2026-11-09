"""
tests/test_argon_p0_negative_security.py
=============================================================================
ARGON Phase 10: Exhaustive Pre-Production Negative Security & Integrity Tests
Validates all P0/P1 fixes against deliberate adversarial tampering, fail-open
scenarios, admin spoofing, transaction partial failures, and lifecycle boundaries.
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
    grant_role,
    activate_role,
    is_assignable_mentor,
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
from services.relationships import assign_guide, assign_sme
from services.help_requests import create_request


@pytest.fixture(autouse=True)
def force_test_backend(monkeypatch):
    """Enforce local backend and clear memoization before each test."""
    monkeypatch.setenv("DATA_BACKEND", "sqlite")
    from services.cache import invalidate_memo
    invalidate_memo()


# =============================================================================
# 1. FAIL-OPEN AUTHORIZATION NEGATIVE TESTS (P0)
# =============================================================================

class TestFailOpenAccountAuthorization:
    """Validates that get_account_status and is_account_active fail strictly closed."""

    def test_neg01_empty_and_none_user_id_fails_closed(self):
        """Empty or None user ID must immediately return DENIED and is_active=False."""
        status_none = get_account_status(None)
        assert status_none["account_status"] == "DENIED"
        assert status_none["is_active"] is False
        assert status_none["exists"] is False
        act_none, _ = is_account_active(None)
        assert act_none is False

        status_empty = get_account_status("")
        assert status_empty["account_status"] == "DENIED"
        assert status_empty["is_active"] is False
        assert status_empty["exists"] is False
        act_empty, _ = is_account_active("")
        assert act_empty is False

        status_whitespace = get_account_status("   ")
        assert status_whitespace["account_status"] == "DENIED"
        assert status_whitespace["is_active"] is False
        act_ws, _ = is_account_active("   ")
        assert act_ws is False

    def test_neg02_nonexistent_uuid_fails_closed(self):
        """A UUID not found in the database must return DENIED and exists=False (never default to ACTIVE)."""
        ghost_uuid = str(uuid.uuid4())
        status = get_account_status(ghost_uuid)
        assert status["account_status"] == "DENIED"
        assert status["is_active"] is False
        assert status["exists"] is False
        assert "not found" in status["error"].lower()
        act_ghost, _ = is_account_active(ghost_uuid)
        assert act_ghost is False

    def test_neg03_supabase_service_failure_fails_closed(self, monkeypatch):
        """When Supabase is unavailable in DATA_BACKEND=supabase, must fail-closed (no silent fallback)."""
        monkeypatch.setenv("DATA_BACKEND", "supabase")
        monkeypatch.setattr("services.account_lifecycle.get_supabase_admin_client", lambda: None)
        monkeypatch.setattr("services.account_lifecycle.get_supabase_client", lambda: None)

        test_uid = str(uuid.uuid4())
        status = get_account_status(test_uid)
        assert status["account_status"] == "DENIED"
        assert status["is_active"] is False
        assert "unavailable" in status["error"].lower()
        act_sb, _ = is_account_active(test_uid)
        assert act_sb is False

    def test_neg04_supabase_query_exception_fails_closed(self, monkeypatch):
        """Network/query exceptions against Supabase must yield DENIED, never an active default."""
        monkeypatch.setenv("DATA_BACKEND", "supabase")
        mock_client = MagicMock()
        mock_client.table.side_effect = ConnectionError("PostgREST connection timeout")
        monkeypatch.setattr("services.account_lifecycle.get_supabase_admin_client", lambda: mock_client)

        test_uid = str(uuid.uuid4())
        status = get_account_status(test_uid)
        assert status["account_status"] == "DENIED"
        assert status["is_active"] is False
        assert "unavailable" in status["error"].lower() or "timeout" in status["error"].lower()
        act_fail, _ = is_account_active(test_uid)
        assert act_fail is False

    def test_neg05_corrupt_unknown_lifecycle_status_fails_closed(self, monkeypatch):
        """Corrupt or unrecognized account_status values (e.g. 'CORRUPT_UNKNOWN_STATE') must fail-closed to DENIED."""
        from services.local_db import get_local_db
        db = get_local_db()
        test_uid = str(uuid.uuid4())
        test_email = f"corrupt_{uuid.uuid4().hex[:6]}@test.in"

        with db._get_conn() as conn:
            conn.execute(
                """
                INSERT INTO profiles (id, email, role, full_name, is_active, account_status)
                VALUES (?, ?, ?, ?, 1, 'CORRUPT_UNKNOWN_STATE')
                """,
                (test_uid, test_email, "aspirant", "Corrupt User")
            )

        status = get_account_status(test_uid)
        # Unrecognized lifecycle states fail-closed to DENIED
        assert status["account_status"] == "DENIED"
        assert status["is_active"] is False
        act_corrupt, _ = is_account_active(test_uid)
        assert act_corrupt is False


# =============================================================================
# 2. SOLE ADMIN IDENTITY & ANTI-SPOOFING NEGATIVE TESTS (P0)
# =============================================================================

class TestSoleAdminAntiSpoofing:
    """Verifies that privileged operations verify actual server session and cannot be spoofed."""

    def test_neg06_aspirant_session_cannot_spoof_admin_uuid(self):
        """An aspirant with an active session who passes admin_id=SOLE_ADMIN_UUID is rejected."""
        fake_aspirant_session = {
            "id": str(uuid.uuid4()),
            "email": f"aspirant_{uuid.uuid4().hex[:6]}@attacker.in",
            "role": "aspirant"
        }

        with patch("streamlit.session_state", {"user": fake_aspirant_session}):
            # is_strict_admin must detect spoofing and return False
            assert is_strict_admin(user_id=SOLE_ADMIN_UUID) is False
            assert is_strict_admin(user_id=SOLE_ADMIN_UUID, email=SOLE_ADMIN_EMAIL) is False

            # require_sole_admin must reject with explicit spoofing error
            ok, err = require_sole_admin(actor_id=SOLE_ADMIN_UUID)
            assert ok is False
            assert "spoofing detected" in err.lower()

    def test_neg07_guide_session_cannot_spoof_admin_uuid(self):
        """A guide with an active session cannot perform admin operations by passing SOLE_ADMIN_UUID."""
        fake_guide_session = {
            "id": str(uuid.uuid4()),
            "email": f"guide_{uuid.uuid4().hex[:6]}@attacker.in",
            "role": "guide"
        }

        with patch("streamlit.session_state", {"user": fake_guide_session}):
            ok, err = suspend_account(str(uuid.uuid4()), reason="Malicious suspension", actor_id=SOLE_ADMIN_UUID)
            assert ok is False
            assert "spoofing detected" in err.lower()

    def test_neg08_admin_email_with_wrong_uuid_rejected(self):
        """Passing the sole admin email with a forged UUID must be rejected."""
        forged_uuid = str(uuid.uuid4())
        assert is_strict_admin(user_id=forged_uuid, email=SOLE_ADMIN_EMAIL) is False
        ok, err = require_sole_admin(actor_id=forged_uuid)
        assert ok is False
        assert "Unauthorized" in err

    def test_neg09_admin_uuid_with_wrong_email_rejected(self):
        """Passing the sole admin UUID with a non-admin email must be rejected."""
        assert is_strict_admin(user_id=SOLE_ADMIN_UUID, email="imposter@gmail.com") is False

    def test_neg10_expired_or_invalid_supabase_token_rejected(self, monkeypatch):
        """If a cryptographic token is supplied, an invalid token rejected by Supabase Auth denies access."""
        monkeypatch.setenv("DATA_BACKEND", "supabase")
        mock_client = MagicMock()
        mock_client.auth.get_user.side_effect = Exception("JWT expired or invalid signature")
        monkeypatch.setattr("services.roles.get_supabase_client", lambda: mock_client)

        result = is_strict_admin(user_id=SOLE_ADMIN_UUID, email=SOLE_ADMIN_EMAIL, token="bad_token")
        assert result is False


# =============================================================================
# 3. ARCHIVING & MENTOR HANDOVER FAILURE RECOVERY TESTS (P0)
# =============================================================================

class TestArchivingAndHandoverFailureRecovery:
    """Verifies that failures during unassignment halt archival and rollback state changes."""

    def test_neg11_archive_account_aborts_when_guide_unassignment_fails(self, monkeypatch):
        """If unassign_guide fails, archive_account must halt immediately and NOT mark account ARCHIVED."""
        from services.local_db import get_local_db
        db = get_local_db()
        now_iso = datetime.now(timezone.utc).isoformat()
        guide_uid = str(uuid.uuid4())
        guide_email = f"failing_guide_{uuid.uuid4().hex[:6]}@test.in"
        db.upsert_profile({
            "id": guide_uid,
            "email": guide_email,
            "role": "guide",
            "full_name": "Failing Guide",
            "account_status": "ACTIVE",
            "is_active": 1,
            "created_at": now_iso,
            "updated_at": now_iso,
        })

        # Mock active relationship indicating assigned case
        monkeypatch.setattr(
            "services.relationships.get_all_relationships",
            lambda: [{"aspirant_id": "asp-test-1", "status": "active", "guide_ids": [guide_uid]}]
        )

        # Simulate unassign_guide failing due to a database exception
        monkeypatch.setattr(
            "services.relationships.unassign_guide",
            lambda *args, **kwargs: (False, "Database lock timeout on relationship update")
        )

        ok, err = archive_account(guide_uid, reason="Test archive abort", actor_id=SOLE_ADMIN_UUID)
        assert ok is False
        assert "Database lock timeout" in err

        # The profile MUST NOT be ARCHIVED
        status = get_account_status(guide_uid)
        assert status["account_status"] == "ACTIVE"
        assert status["is_active"] is True

    def test_neg12_archive_account_aborts_when_audit_log_write_fails(self, monkeypatch):
        """If writing the immutable lifecycle audit log fails, profile status changes are rolled back."""
        from services.local_db import get_local_db
        db = get_local_db()
        now_iso = datetime.now(timezone.utc).isoformat()
        target_uid = str(uuid.uuid4())
        target_email = f"rollback_test_{uuid.uuid4().hex[:6]}@test.in"
        db.upsert_profile({
            "id": target_uid,
            "email": target_email,
            "role": "aspirant",
            "full_name": "Rollback Test User",
            "account_status": "ACTIVE",
            "is_active": 1,
            "created_at": now_iso,
            "updated_at": now_iso,
        })

        # Mock get_archive_impact_preview with 0 cases
        monkeypatch.setattr(
            "services.account_lifecycle.get_archive_impact_preview",
            lambda uid: {
                "user_id": uid,
                "role": "aspirant",
                "assigned_guide_cases_count": 0,
                "assigned_guide_cases": [],
                "assigned_sme_cases_count": 0,
                "assigned_sme_cases": [],
                "open_tickets_count": 0,
                "orphaned_guide_cases_count": 0,
            }
        )

        # Simulate audit log write failure in local_db
        def fail_log(*args, **kwargs):
            raise RuntimeError("PostgreSQL disk full / audit table error")
        monkeypatch.setattr("services.local_db.LocalDatabase.log_account_lifecycle", fail_log)

        ok, err = archive_account(target_uid, reason="Test audit rollback", actor_id=SOLE_ADMIN_UUID)
        assert ok is False
        assert "audit table error" in err

        # Status must have rolled back to ACTIVE
        status = get_account_status(target_uid)
        assert status["account_status"] == "ACTIVE"


# =============================================================================
# 4. MIGRATION 009 BACKFILL & INACTIVE USER PRESERVATION (P0)
# =============================================================================

class TestMigrationBackfillIntegrity:
    """Verifies that pre-migration inactive profiles are classified as TEMPORARILY_SUSPENDED."""

    def test_neg13_pre_migration_inactive_user_classified_suspended(self):
        """A user with is_active=0 who had no account_status set must be TEMPORARILY_SUSPENDED, never ACTIVE."""
        from services.local_db import get_local_db
        db = get_local_db()
        inactive_uid = str(uuid.uuid4())
        inactive_email = f"legacy_inactive_{uuid.uuid4().hex[:6]}@test.in"

        # Insert user simulating legacy schema (is_active=0, account_status not set or NULL)
        with db._get_conn() as conn:
            conn.execute(
                """
                INSERT INTO profiles (id, email, role, full_name, is_active, account_status)
                VALUES (?, ?, ?, ?, 0, NULL)
                """,
                (inactive_uid, inactive_email, "aspirant", "Legacy Inactive")
            )

        status = get_account_status(inactive_uid)
        # Because is_active == 0, safe classification must be TEMPORARILY_SUSPENDED, not ACTIVE
        assert status["account_status"] == "TEMPORARILY_SUSPENDED"
        assert status["is_active"] is False
        act_inact, _ = is_account_active(inactive_uid)
        assert act_inact is False


# =============================================================================
# 5. PENDING DELETION ACCESS & MUTATION RESTRICTIONS (P1)
# =============================================================================

class TestPendingDeletionRestrictions:
    """Verifies that accounts pending deletion cannot create help requests or mutate workflows."""

    def test_neg14_pending_deletion_blocks_help_request_creation(self):
        """An aspirant in PENDING_DELETION cannot submit new help requests."""
        from services.local_db import get_local_db
        db = get_local_db()
        now_iso = datetime.now(timezone.utc).isoformat()
        pending_uid = str(uuid.uuid4())
        pending_email = f"pending_del_{uuid.uuid4().hex[:6]}@test.in"
        db.upsert_profile({
            "id": pending_uid,
            "email": pending_email,
            "role": "aspirant",
            "full_name": "Pending Deletion Aspirant",
            "account_status": "ACTIVE",
            "is_active": 1,
            "created_at": now_iso,
            "updated_at": now_iso,
        })

        # Request deletion via the standard lifecycle workflow
        ok_req, err_req = request_account_deletion(
            user_id=pending_uid,
            reason="Leaving the platform",
            actor_id=pending_uid
        )
        assert ok_req is True

        res, err = create_request(
            aspirant_id=pending_uid,
            subject="Need help with pitch deck",
            message="Pitch deck review needed",
            target_role="guide"
        )
        assert res is None
        assert "pending deletion" in err.lower() or "unauthorized" in err.lower()

    def test_neg15_pending_deletion_can_be_cancelled(self):
        """An aspirant in PENDING_DELETION can cancel the deletion request during grace period."""
        from services.local_db import get_local_db
        db = get_local_db()
        now_iso = datetime.now(timezone.utc).isoformat()
        pending_uid = str(uuid.uuid4())
        pending_email = f"cancel_del_{uuid.uuid4().hex[:6]}@test.in"
        db.upsert_profile({
            "id": pending_uid,
            "email": pending_email,
            "role": "aspirant",
            "full_name": "Cancel Deletion Aspirant",
            "account_status": "ACTIVE",
            "is_active": 1,
            "created_at": now_iso,
            "updated_at": now_iso,
        })

        # Request deletion first
        ok_req, err_req = request_account_deletion(
            user_id=pending_uid,
            reason="Leaving the platform",
            actor_id=pending_uid
        )
        assert ok_req is True

        # Now cancel deletion
        ok_cancel, err_cancel = cancel_account_deletion(pending_uid, actor_id=pending_uid)
        assert ok_cancel is True
        assert err_cancel is None

        status = get_account_status(pending_uid)
        assert status["account_status"] == "ACTIVE"
        assert status["is_active"] is True


# =============================================================================
# 6. MENTOR ELIGIBILITY & LEGACY FALLBACK REMOVAL (P1)
# =============================================================================

class TestMentorEligibilityStrictGating:
    """Verifies that pending NDA mentors cannot be assigned and legacy profiles.role fallback is dead."""

    def test_neg16_pending_nda_mentor_cannot_be_assigned(self):
        """A mentor whose role grant is pending_nda is strictly rejected from case assignments."""
        from services.local_db import get_local_db
        db = get_local_db()
        now_iso = datetime.now(timezone.utc).isoformat()
        mentor_uid = str(uuid.uuid4())
        mentor_email = f"pending_nda_mentor_{uuid.uuid4().hex[:6]}@test.in"
        asp_uid = str(uuid.uuid4())
        asp_email = f"asp_target_{uuid.uuid4().hex[:6]}@test.in"

        db.upsert_profile({
            "id": mentor_uid,
            "email": mentor_email,
            "role": "guide",
            "full_name": "Pending NDA Guide",
            "account_status": "ACTIVE",
            "is_active": 1,
            "created_at": now_iso,
            "updated_at": now_iso,
        })
        db.upsert_profile({
            "id": asp_uid,
            "email": asp_email,
            "role": "aspirant",
            "full_name": "Target Aspirant",
            "account_status": "ACTIVE",
            "is_active": 1,
            "created_at": now_iso,
            "updated_at": now_iso,
        })

        # Grant role as pending_nda (default)
        grant_role(mentor_uid, "guide", granted_by=SOLE_ADMIN_UUID, require_nda=True)

        # Assignment must be rejected because NDA is not completed
        ok, err = assign_guide(asp_uid, mentor_uid, admin_id=SOLE_ADMIN_UUID)
        assert ok is False
        assert "pending nda" in err.lower() or "nda" in err.lower()

    def test_neg17_mentor_without_explicit_user_roles_grant_rejected(self):
        """An aspirant who has no guide/sme grant in user_roles cannot be assigned as a Guide."""
        from services.local_db import get_local_db
        db = get_local_db()
        now_iso = datetime.now(timezone.utc).isoformat()
        non_mentor_uid = str(uuid.uuid4())
        non_mentor_email = f"aspirant_mentor_{uuid.uuid4().hex[:6]}@test.in"
        asp_uid = str(uuid.uuid4())
        asp_email = f"asp_legacy_{uuid.uuid4().hex[:6]}@test.in"

        # User is an aspirant with NO guide grant in user_roles
        db.upsert_profile({
            "id": non_mentor_uid,
            "email": non_mentor_email,
            "role": "aspirant",
            "full_name": "Ordinary Aspirant",
            "account_status": "ACTIVE",
            "is_active": 1,
            "created_at": now_iso,
            "updated_at": now_iso,
        })
        db.upsert_profile({
            "id": asp_uid,
            "email": asp_email,
            "role": "aspirant",
            "full_name": "Aspirant Target",
            "account_status": "ACTIVE",
            "is_active": 1,
            "created_at": now_iso,
            "updated_at": now_iso,
        })

        ok, err = assign_guide(asp_uid, non_mentor_uid, admin_id=SOLE_ADMIN_UUID)
        assert ok is False
        assert "user_roles" in err.lower() or "grant" in err.lower()
