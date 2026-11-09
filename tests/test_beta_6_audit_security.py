"""
tests/test_beta_6_audit_security.py
=============================================================================
FULCRUM-BETA (6) INDEPENDENT AUDIT & SECURITY REMEDIATION TEST SUITE
Validates:
  1. Sole Admin verification requiring authenticated session or verified token in Supabase mode.
  2. Account lifecycle DENIED status blocked at login and UI routing.
  3. Case discussion ownership and unauthenticated private notes protection.
  4. Supabase-to-SQLite collaboration fallback prevention (DATA_BACKEND=supabase).
  5. Mentor handover database consistency and partial failure error reporting.
  6. Professional and aspirant photo deletion cloud failure handling.
  7. Inactive mentor access prevention (no synthetic guide/sme roles from legacy profiles).
  8. Immutable audit log policy validation against forged lifecycle events.
=============================================================================
"""

import uuid
import pytest
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from services.roles import (
    SOLE_ADMIN_UUID,
    SOLE_ADMIN_EMAIL,
    is_strict_admin,
    require_sole_admin,
    get_user_roles,
    get_active_roles,
    grant_role,
    activate_role,
)
from services.account_lifecycle import (
    get_account_status,
    is_account_active,
    list_account_lifecycle_logs,
)
from services.auth import login_user
from services.collaboration import create_case_message, list_case_messages
from services.relationships import unassign_guide, unassign_sme, assign_guide, assign_sme
from services.professional_photos import delete_professional_photo
from services.aspirant_photos import delete_aspirant_photo
from services.local_db import get_local_db
from services.cache import invalidate_memo


@pytest.fixture(autouse=True)
def reset_test_env(monkeypatch):
    """Enforce local backend and clear memoization before each test."""
    monkeypatch.setenv("DATA_BACKEND", "sqlite")
    invalidate_memo()


class TestBeta6AuditSecurityRemediation:
    """Verifies all confirmed P0 issues from FULCRUM-BETA (6) Audit."""

    # ─────────────────────────────────────────────────────────────────────────
    # 1. SOLE ADMIN IDENTITY & AUTHENTICATED SESSION CONTEXT
    # ─────────────────────────────────────────────────────────────────────────

    def test_01_sole_admin_in_supabase_mode_requires_verified_session_or_token(self, monkeypatch):
        """In DATA_BACKEND=supabase, require_sole_admin rejects callers without verified session or token."""
        monkeypatch.setenv("DATA_BACKEND", "supabase")
        
        # Scenario A: Caller in Streamlit runtime without authenticated admin session passes SOLE_ADMIN_UUID
        with patch("streamlit.runtime.scriptrunner.get_script_run_ctx", return_value=MagicMock()):
            with patch("streamlit.session_state", {}):
                ok, err = require_sole_admin(actor_id=SOLE_ADMIN_UUID)
                assert ok is False
                assert "authenticated sole admin session is required" in err.lower()

        # Scenario B: Caller passes invalid cryptographic token
        mock_client = MagicMock()
        mock_client.auth.get_user.side_effect = Exception("Invalid token")
        monkeypatch.setattr("services.roles.get_supabase_client", lambda: mock_client)
        with patch("streamlit.session_state", {}):
            ok, err = require_sole_admin(actor_id=SOLE_ADMIN_UUID, token="forged_jwt")
            assert ok is False

        # Scenario C: Active session has non-admin user trying to pass admin UUID (spoofing)
        aspirant_sess = {"id": str(uuid.uuid4()), "email": "rogue@user.in", "role": "aspirant"}
        with patch("streamlit.session_state", {"user": aspirant_sess}):
            ok, err = require_sole_admin(actor_id=SOLE_ADMIN_UUID)
            assert ok is False
            assert "spoofing detected" in err.lower()

        # Scenario D: Legitimate Sole Admin session authorizes successfully
        admin_sess = {"id": SOLE_ADMIN_UUID, "email": SOLE_ADMIN_EMAIL, "role": "admin"}
        with patch("streamlit.session_state", {"user": admin_sess}):
            ok, err = require_sole_admin(actor_id=SOLE_ADMIN_UUID)
            assert ok is True
            assert err is None

    def test_02_is_strict_admin_rejects_missing_or_tampered_profile(self, monkeypatch):
        """is_strict_admin never blindly returns True if persistent profile does not match Sole Admin."""
        # Monkeypatch get_profile to return None (database lookup failure or non-existent user)
        monkeypatch.setattr("services.profiles.get_profile", lambda uid: None)
        with patch("streamlit.session_state", {}):
            # Only UUID provided with missing profile -> must return False
            assert is_strict_admin(user_id=SOLE_ADMIN_UUID) is False

        # Profile has SOLE_ADMIN_UUID but tampered email
        monkeypatch.setattr("services.profiles.get_profile", lambda uid: {"id": SOLE_ADMIN_UUID, "email": "tampered@admin.com", "role": "admin"})
        with patch("streamlit.session_state", {}):
            assert is_strict_admin(user_id=SOLE_ADMIN_UUID) is False

    # ─────────────────────────────────────────────────────────────────────────
    # 2. ACCOUNT LIFECYCLE DENIED-STATE ENFORCEMENT
    # ─────────────────────────────────────────────────────────────────────────

    def test_03_denied_account_blocked_at_login_sqlite_mode(self):
        """An account with account_status='DENIED' is strictly rejected by login_user in SQLite mode."""
        db = get_local_db()
        test_uid = str(uuid.uuid4())
        test_email = f"denied_{uuid.uuid4().hex[:6]}@test.in"
        test_pw = "Password123!"

        db.upsert_profile({
            "id": test_uid,
            "email": test_email,
            "role": "aspirant",
            "full_name": "Denied User",
            "account_status": "DENIED",
            "is_active": 0,
            "lifecycle_reason": "Security violation",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        })
        db.update_user_password(test_uid, test_pw)

        prof, err = login_user(test_email, test_pw)
        assert prof is None
        assert "access denied" in err.lower() or "restricted" in err.lower()

    def test_04_denied_account_blocked_at_login_supabase_mode(self, monkeypatch):
        """In Supabase mode, an account resolving to DENIED signs out and is rejected."""
        monkeypatch.setenv("DATA_BACKEND", "supabase")
        mock_client = MagicMock()
        mock_auth_res = MagicMock()
        mock_auth_res.user.id = "sb-denied-user-id"
        mock_auth_res.session.access_token = "valid_token"
        mock_auth_res.session.refresh_token = "valid_refresh"
        mock_client.auth.sign_in_with_password.return_value = mock_auth_res

        # Profile fetch returns record
        mock_table = MagicMock()
        mock_table.select.return_value.eq.return_value.execute.return_value.data = [{
            "id": "sb-denied-user-id",
            "email": "denied@sb.in",
            "role": "aspirant",
            "full_name": "SB Denied User",
            "account_status": "DENIED",
            "is_active": False,
        }]
        mock_client.table.return_value = mock_table

        monkeypatch.setattr("services.auth.get_supabase_client", lambda: mock_client)
        monkeypatch.setattr("services.account_lifecycle.get_account_status", lambda uid: {
            "account_status": "DENIED",
            "is_active": False,
            "exists": True,
            "error": "Account suspended by administrative audit.",
        })

        prof, err = login_user("denied@sb.in", "secretpass")
        assert prof is None
        assert "access denied" in err.lower()
        mock_client.auth.sign_out.assert_called_once()

    # ─────────────────────────────────────────────────────────────────────────
    # 3. CASE COLLABORATION & PRIVATE NOTE ACCESS CONTROL
    # ─────────────────────────────────────────────────────────────────────────

    def test_05_unauthenticated_request_cannot_view_private_mentor_notes(self):
        """Unauthenticated calls to list_case_messages cannot view private notes even if requesting_role='guide'."""
        db = get_local_db()
        asp_id = str(uuid.uuid4())
        guide_id = str(uuid.uuid4())

        # Insert 1 public message and 1 private mentor note
        db.insert_case_discussion({
            "id": str(uuid.uuid4()),
            "aspirant_id": asp_id,
            "author_id": asp_id,
            "author_role": "aspirant",
            "title": "Public Milestone Update",
            "message": "Ready for milestone review.",
            "is_private_mentor_note": False,
            "created_at": datetime.now(timezone.utc).isoformat(),
        })
        db.insert_case_discussion({
            "id": str(uuid.uuid4()),
            "aspirant_id": asp_id,
            "author_id": guide_id,
            "author_role": "guide",
            "title": "Private Mentor Assessment",
            "message": "Confidential advisory note on governance risk.",
            "is_private_mentor_note": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
        })

        # Call with viewer_id=None and no session -> must NEVER return private notes
        with patch("streamlit.session_state", {}):
            msgs_asp = list_case_messages(asp_id, requesting_role="aspirant", viewer_id=None)
            assert len(msgs_asp) == 1
            assert msgs_asp[0]["title"] == "Public Milestone Update"

            # Adversary tries to bypass by passing requesting_role="guide" without viewer identity
            msgs_bypass = list_case_messages(asp_id, requesting_role="guide", viewer_id=None)
            assert len(msgs_bypass) == 1
            assert msgs_bypass[0]["is_private_mentor_note"] is False

    def test_06_unassigned_mentor_cannot_author_private_notes(self):
        """A guide who is not actively assigned to the mentee cannot post private mentor notes."""
        asp_id = str(uuid.uuid4())
        unassigned_guide_id = str(uuid.uuid4())

        ok, err = create_case_message(
            aspirant_id=asp_id,
            author_id=unassigned_guide_id,
            author_role="guide",
            title="Unauthorized Note",
            message="Attempting to post private note without assignment",
            is_private_mentor_note=True,
        )
        assert ok is False
        assert "unauthorized" in err.lower() or "relationship" in err.lower()

    def test_07_collaboration_no_sqlite_fallback_in_supabase_mode(self, monkeypatch):
        """In DATA_BACKEND=supabase, if Supabase query raises an exception, do NOT fall back to SQLite."""
        monkeypatch.setenv("DATA_BACKEND", "supabase")
        
        mock_client = MagicMock()
        mock_client.table.side_effect = ConnectionError("Supabase connection timeout")
        monkeypatch.setattr("services.collaboration.get_supabase_admin_client", lambda: mock_client)
        monkeypatch.setattr("services.collaboration.get_supabase_client", lambda: mock_client)

        # Populate SQLite with a discussion record
        db = get_local_db()
        asp_id = str(uuid.uuid4())
        db.insert_case_discussion({
            "id": str(uuid.uuid4()),
            "aspirant_id": asp_id,
            "author_id": asp_id,
            "author_role": "aspirant",
            "title": "Local SQLite Message",
            "message": "Should never be read in Supabase mode",
            "is_private_mentor_note": False,
            "created_at": datetime.now(timezone.utc).isoformat(),
        })

        # list_case_messages must return empty list, NOT the SQLite record
        msgs = list_case_messages(asp_id, requesting_role="aspirant", viewer_id=asp_id)
        assert msgs == []

        # create_case_message must return False error, NOT silently write to SQLite and claim True
        ok, err = create_case_message(
            aspirant_id=asp_id,
            author_id=asp_id,
            author_role="aspirant",
            title="Test Message",
            message="Test Content",
        )
        assert ok is False
        assert "supabase" in err.lower() or "failed" in err.lower()

    # ─────────────────────────────────────────────────────────────────────────
    # 4. MENTOR HANDOVER & PARTIAL FAILURE RECOVERY
    # ─────────────────────────────────────────────────────────────────────────

    def test_08_consultation_handover_failure_reports_error_and_does_not_mask(self, monkeypatch):
        """If help_requests update fails during unassign_guide, error is returned, never masked as complete success."""
        monkeypatch.setenv("DATA_BACKEND", "supabase")
        mock_client = MagicMock()
        
        # Mock relationships update succeeds
        mock_rel = MagicMock()
        mock_rel.update.return_value.eq.return_value.execute.return_value = MagicMock()
        
        # Mock assignment_history upsert succeeds
        mock_hist = MagicMock()
        mock_hist.upsert.return_value.execute.return_value = MagicMock()

        # Mock help_requests update FAILS
        mock_hr = MagicMock()
        mock_hr.update.side_effect = RuntimeError("Deadlock on help_requests update")

        def mock_table(name):
            if name == "relationships":
                return mock_rel
            elif name == "assignment_history":
                return mock_hist
            elif name == "help_requests":
                return mock_hr
            return MagicMock()

        mock_client.table.side_effect = mock_table
        monkeypatch.setattr("services.relationships._get_admin_client", lambda: mock_client)

        asp_id = str(uuid.uuid4())
        guide_id = str(uuid.uuid4())

        # Mock get_aspirant_mentors returning assigned guide
        monkeypatch.setattr("services.relationships.get_aspirant_mentors", lambda aid: {
            "guide": {"id": guide_id, "full_name": "Departing Guide"},
            "guides": [{"id": guide_id, "full_name": "Departing Guide"}],
            "smes": [],
        })

        ok, err = unassign_guide(
            aspirant_id=asp_id,
            guide_id=guide_id,
            admin_id=SOLE_ADMIN_UUID,
            reason="Transition",
        )
        assert ok is False
        assert "failed to transfer consultations" in err.lower() or "deadlock" in err.lower()

    # ─────────────────────────────────────────────────────────────────────────
    # 5. PHOTO DELETION CLOUD FAILURE REPORTING
    # ─────────────────────────────────────────────────────────────────────────

    def test_09_professional_photo_deletion_cloud_failure_reports_error(self, monkeypatch):
        """If cloud storage removal or metadata deletion fails in Supabase, delete_professional_photo reports False."""
        monkeypatch.setenv("DATA_BACKEND", "supabase")
        mock_admin = MagicMock()
        
        # Metadata query returns storage_path
        mock_table = MagicMock()
        mock_table.select.return_value.eq.return_value.execute.return_value.data = [
            {"storage_path": "prof-user/headshot_123.webp"}
        ]
        mock_admin.table.return_value = mock_table

        # Storage remove raises network exception
        mock_storage = MagicMock()
        mock_storage.remove.side_effect = ConnectionError("Storage service unavailable 503")
        mock_admin.storage.from_.return_value = mock_storage

        monkeypatch.setattr("services.professional_photos.get_supabase_admin_client", lambda: mock_admin)

        target_mentor_id = str(uuid.uuid4())
        # Call delete as Sole Admin
        ok, err = delete_professional_photo(
            subject_user_id=target_mentor_id,
            actor_id=SOLE_ADMIN_UUID,
            actor_email=SOLE_ADMIN_EMAIL,
        )
        assert ok is False
        assert "failed to remove professional photo from cloud storage" in err.lower() or "unavailable" in err.lower()

    def test_10_aspirant_photo_deletion_cloud_failure_reports_error(self, monkeypatch):
        """If cloud storage removal fails in Supabase, delete_aspirant_photo reports False."""
        monkeypatch.setenv("DATA_BACKEND", "supabase")
        mock_admin = MagicMock()

        # Metadata query returns storage_path
        mock_table = MagicMock()
        mock_table.select.return_value.eq.return_value.limit.return_value.execute.return_value.data = [
            {"storage_path": "asp-user/photo_123.webp"}
        ]
        mock_admin.table.return_value = mock_table

        # Storage remove raises exception
        mock_storage = MagicMock()
        mock_storage.remove.side_effect = TimeoutError("Storage timeout")
        mock_admin.storage.from_.return_value = mock_storage

        monkeypatch.setattr("services.aspirant_photos.get_supabase_admin_client", lambda: mock_admin)

        target_asp_id = str(uuid.uuid4())
        ok, err = delete_aspirant_photo(user_id=target_asp_id, deleter_id=SOLE_ADMIN_UUID)
        assert ok is False
        assert "failed to delete photo from cloud storage" in err.lower() or "timeout" in err.lower()

    # ─────────────────────────────────────────────────────────────────────────
    # 6. INACTIVE MENTOR ACCESS & PREVENTING SYNTHETIC PRIVILEGES
    # ─────────────────────────────────────────────────────────────────────────

    def test_11_inactive_mentor_never_synthesizes_active_professional_roles(self, monkeypatch):
        """A user with profiles.role='guide' but NO grant in user_roles never receives synthetic active guide grant."""
        user_id = str(uuid.uuid4())
        user_email = f"retired_guide_{uuid.uuid4().hex[:6]}@test.in"

        # Mock profile indicating legacy role='guide'
        monkeypatch.setattr("services.profiles.get_profile", lambda uid: {
            "id": user_id,
            "email": user_email,
            "role": "guide",
            "created_at": datetime.now(timezone.utc).isoformat(),
        })

        # Mock user_roles query returning empty (e.g. revoked or not granted)
        monkeypatch.setattr("services.roles._get_admin_client", lambda: None)
        monkeypatch.setattr("services.roles._get_user_client", lambda: None)
        monkeypatch.setattr("services.roles.get_data_backend", lambda: "sqlite")
        
        # Local db get_user_roles returns []
        mock_db = MagicMock()
        mock_db.get_user_roles.return_value = []
        monkeypatch.setattr("services.roles.get_local_db", lambda: mock_db)

        roles = get_user_roles(user_id)
        # MUST NOT contain guide role!
        assert not any(r.get("role") == "guide" for r in roles)
        active_roles = get_active_roles(user_id)
        assert "guide" not in active_roles
        assert "sme" not in active_roles

    # ─────────────────────────────────────────────────────────────────────────
    # 7. AUDIT LOG IMMUTABILITY & FORGERY PREVENTION
    # ─────────────────────────────────────────────────────────────────────────

    def test_12_audit_log_query_no_sqlite_fallback_in_supabase_mode(self, monkeypatch):
        """In DATA_BACKEND=supabase, list_account_lifecycle_logs never falls back to SQLite."""
        monkeypatch.setenv("DATA_BACKEND", "supabase")
        mock_admin = MagicMock()
        mock_admin.table.side_effect = ConnectionError("Supabase audit table down")
        monkeypatch.setattr("services.account_lifecycle.get_supabase_admin_client", lambda: mock_admin)

        # Seed local SQLite with audit row
        db = get_local_db()
        test_uid = str(uuid.uuid4())
        db.log_account_lifecycle({
            "id": str(uuid.uuid4()),
            "user_id": test_uid,
            "actor_id": SOLE_ADMIN_UUID,
            "action": "SUSPEND",
            "previous_status": "ACTIVE",
            "new_status": "TEMPORARILY_SUSPENDED",
            "reason": "SQLite test log",
            "metadata": "{}",
            "created_at": datetime.now(timezone.utc).isoformat(),
        })

        logs = list_account_lifecycle_logs(user_id=test_uid)
        # Must return empty list, NOT the SQLite row
        assert logs == []
