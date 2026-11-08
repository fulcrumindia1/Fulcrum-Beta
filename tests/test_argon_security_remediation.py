"""
tests/test_argon_security_remediation.py
=========================================
Phase 0 Automated Security Remediation Test Suite (SEC-01 through SEC-16).
Validates:
  - Account takeover prevention & admin account protection
  - Multi-role authorization and Single Admin isolation
  - Private case notes confidentiality and parameter-tampering defense
  - Photo access control, viewer authentication & fail-closed behavior
  - Safe credential provisioning and fail-closed persistence
"""

import pytest
import os
import io
from unittest.mock import patch, MagicMock
from services.auth import complete_password_reset, complete_first_login_password_change
from services.collaboration import create_case_message, list_case_messages
from services.aspirant_photos import get_aspirant_photo, upload_aspirant_photo, can_view_aspirant_photo
from services.roles import grant_role, list_active_profiles_for_role, VALID_GRANTABLE_ROLES
from services.profiles import update_aspirant_profile


class TestArgonSecurityRemediation:

    # ─────────────────────────────────────────────────────────────
    # SEC-01: Anonymous password reset attempt without token fails
    # ─────────────────────────────────────────────────────────────
    def test_sec_01_anonymous_reset_without_token_fails(self):
        with patch("services.auth.get_data_backend", return_value="supabase"):
            with patch("services.auth.get_supabase_client", return_value=MagicMock()):
                ok, err = complete_password_reset(
                    new_password="NewSecurePassword123!",
                    access_token=None,
                    email="victim@example.com"
                )
                assert ok is False
                assert "token" in err.lower() or "recovery" in err.lower()

    # ─────────────────────────────────────────────────────────────
    # SEC-02: Password reset with mismatched session email fails
    # ─────────────────────────────────────────────────────────────
    def test_sec_02_password_reset_mismatched_session_email_fails(self):
        mock_client = MagicMock()
        mock_sess = MagicMock()
        mock_sess.user.email = "attacker@evil.com"
        mock_client.auth.set_session.return_value = mock_sess

        with patch("services.auth.get_data_backend", return_value="supabase"):
            with patch("services.auth.get_supabase_client", return_value=mock_client):
                ok, err = complete_password_reset(
                    new_password="NewSecurePassword123!",
                    access_token="fake_token_123",
                    email="victim@example.com"
                )
                assert ok is False
                assert "security violation" in err.lower() or "does not match" in err.lower()

    # ─────────────────────────────────────────────────────────────
    # SEC-03: Reset targeting fulcrumindia1@gmail.com is rejected
    # ─────────────────────────────────────────────────────────────
    def test_sec_03_admin_account_reset_is_strictly_rejected(self):
        with patch("services.auth.get_data_backend", return_value="supabase"):
            ok, err = complete_password_reset(
                new_password="NewSecurePassword123!",
                access_token="valid_recovery_token",
                email="fulcrumindia1@gmail.com"
            )
            assert ok is False
            assert "platform administrator" in err.lower() or "self-service" in err.lower()

    # ─────────────────────────────────────────────────────────────
    # SEC-04: Password reset with password length < 8 fails
    # ─────────────────────────────────────────────────────────────
    def test_sec_04_password_length_under_8_fails(self):
        ok, err = complete_password_reset(
            new_password="short",
            access_token="some_token",
            email="user@test.in"
        )
        assert ok is False
        assert "8 characters" in err

    # ─────────────────────────────────────────────────────────────
    # SEC-05: Photo retrieval without viewer fails closed
    # ─────────────────────────────────────────────────────────────
    def test_sec_05_photo_retrieval_without_viewer_fails_closed(self):
        # viewer_id=None and no streamlit session
        res = get_aspirant_photo(user_id="test_asp_123", viewer_id=None)
        assert res is None

    # ─────────────────────────────────────────────────────────────
    # SEC-06: Unassigned mentor cannot view aspirant photo
    # ─────────────────────────────────────────────────────────────
    def test_sec_06_unassigned_mentor_photo_view_denied(self):
        with patch("services.aspirant_photos.can_view_aspirant_photo", return_value=(False, "Unauthorized: Viewer is not an active, NDA-certified mentor assigned to this entrepreneur.")):
            res = get_aspirant_photo(user_id="asp_test_id", viewer_id="unassigned_mentor_id", viewer_role="guide")
            assert res is None

    # ─────────────────────────────────────────────────────────────
    # SEC-07: Mentor with pending NDA cannot view aspirant photo
    # ─────────────────────────────────────────────────────────────
    def test_sec_07_mentor_pending_nda_photo_view_denied(self):
        with patch("services.roles.get_active_roles", return_value=["guide"]):
            with patch("services.legal.check_user_nda_accepted", return_value=False):
                with patch("services.aspirant_photos.get_data_backend", return_value="sqlite"):
                    with patch("services.aspirant_photos.get_local_db") as mock_db:
                        mock_db.return_value.get_relationship.return_value = {
                            "aspirant_id": "asp_1",
                            "guide_id": "guide_1",
                            "status": "active"
                        }
                        ok, msg = can_view_aspirant_photo(viewer_id="guide_1", aspirant_id="asp_1", viewer_role="guide")
                        assert ok is False
                        assert "nda" in msg.lower()

    # ─────────────────────────────────────────────────────────────
    # SEC-08: Aspirant cannot author private mentor advisory notes
    # ─────────────────────────────────────────────────────────────
    def test_sec_08_aspirant_cannot_author_private_mentor_notes(self):
        ok, err = create_case_message(
            aspirant_id="asp_1",
            author_id="asp_1",
            author_role="aspirant",
            title="Private Thoughts",
            message="Secret message",
            is_private_mentor_note=True
        )
        assert ok is False
        assert "entrepreneurs cannot create private mentor notes" in err.lower()

    # ─────────────────────────────────────────────────────────────
    # SEC-09: Unassigned mentor cannot author private advisory notes
    # ─────────────────────────────────────────────────────────────
    def test_sec_09_unassigned_mentor_cannot_author_private_notes(self):
        with patch("services.relationships.get_all_relationships", return_value=[]):
            with patch("services.governance.get_primary_admin_id", return_value="admin_id"):
                with patch("services.roles.user_has_active_role", return_value=False):
                    ok, err = create_case_message(
                        aspirant_id="asp_1",
                        author_id="random_guide_id",
                        author_role="guide",
                        title="Advisory Note",
                        message="Should be blocked",
                        is_private_mentor_note=True
                    )
                    assert ok is False
                    assert "unauthorized" in err.lower()

    # ─────────────────────────────────────────────────────────────
    # SEC-10: Aspirant cannot view private notes via parameter tampering
    # ─────────────────────────────────────────────────────────────
    def test_sec_10_aspirant_cannot_view_private_notes_via_role_tampering(self):
        fake_private_note = {
            "id": "msg_priv",
            "aspirant_id": "asp_1",
            "is_private_mentor_note": True,
            "title": "Confidential Strategy",
            "message": "Risk assessment: do not fund without collateral"
        }
        with patch("services.auth.get_data_backend", return_value="sqlite"):
            with patch("services.collaboration.get_memo", return_value=None):
                with patch("services.local_db.get_local_db") as mock_db:
                    mock_db.return_value.list_case_discussions.return_value = [fake_private_note]
                    # Caller is the aspirant themselves, but passes requesting_role="guide"
                    msgs = list_case_messages(aspirant_id="asp_1", requesting_role="guide", viewer_id="asp_1")
                    assert len(msgs) == 0

    # ─────────────────────────────────────────────────────────────
    # SEC-11: Unassigned third party cannot view private mentor notes
    # ─────────────────────────────────────────────────────────────
    def test_sec_11_unassigned_third_party_cannot_view_private_notes(self):
        fake_private_note = {
            "id": "msg_priv",
            "aspirant_id": "asp_1",
            "is_private_mentor_note": True,
            "title": "Advisory",
            "message": "Note"
        }
        with patch("services.relationships.get_all_relationships", return_value=[]):
            with patch("services.governance.get_primary_admin_id", return_value="admin_root"):
                with patch("services.roles.user_has_active_role", return_value=False):
                    with patch("services.collaboration.get_memo", return_value=None):
                        with patch("services.auth.get_data_backend", return_value="sqlite"):
                            with patch("services.local_db.get_local_db") as mock_db:
                                mock_db.return_value.list_case_discussions.return_value = [fake_private_note]
                                msgs = list_case_messages(aspirant_id="asp_1", requesting_role="guide", viewer_id="stranger_id")
                                assert len(msgs) == 0

    # ─────────────────────────────────────────────────────────────
    # SEC-12 & SEC-13: Admin role cannot be granted via grant_role
    # ─────────────────────────────────────────────────────────────
    def test_sec_12_13_admin_role_cannot_be_granted(self):
        assert "admin" not in VALID_GRANTABLE_ROLES
        ok, err = grant_role(user_id="user_victim", role="admin")
        assert ok is False
        assert "unauthorized" in err.lower()

    # ─────────────────────────────────────────────────────────────
    # SEC-14: Platform Admin is strictly excluded from active role lists
    # ─────────────────────────────────────────────────────────────
    def test_sec_14_platform_admin_excluded_from_role_candidate_lists(self):
        with patch("services.profiles.list_profiles_by_role", return_value=[
            {"id": "admin_uuid", "email": "fulcrumindia1@gmail.com", "full_name": "Fulcrum Admin", "role": "admin"},
            {"id": "normal_guide", "email": "guide@test.in", "full_name": "Normal Guide", "role": "guide"}
        ]):
            with patch("services.roles.list_users_with_multi_roles", return_value=[]):
                candidates = list_active_profiles_for_role("guide")
                candidate_emails = [c["email"] for c in candidates]
                assert "fulcrumindia1@gmail.com" not in candidate_emails
                assert "guide@test.in" in candidate_emails

    # ─────────────────────────────────────────────────────────────
    # SEC-15: Cross-user unauthorized profile update is rejected
    # ─────────────────────────────────────────────────────────────
    def test_sec_15_cross_user_profile_update_rejected(self):
        with patch("services.profiles.get_profile", return_value={"id": "actor_attacker", "role": "aspirant"}):
            prof, err = update_aspirant_profile(
                user_id="victim_user_id",
                actor_id="actor_attacker",
                full_name="Compromised Name"
            )
            assert prof is None
            assert "unauthorized" in err.lower()

    # ─────────────────────────────────────────────────────────────
    # SEC-16: Fail-closed photo upload: cloud errors are not masked
    # ─────────────────────────────────────────────────────────────
    def test_sec_16_fail_closed_photo_upload_reports_cloud_error(self):
        mock_admin = MagicMock()
        mock_admin.storage.from_().upload.side_effect = Exception("Storage service unavailable")

        with patch("services.aspirant_photos.get_data_backend", return_value="supabase"):
            with patch("services.aspirant_photos.get_supabase_admin_client", return_value=mock_admin):
                with patch("services.aspirant_photos.validate_and_process_photo", return_value=(True, b"fake_webp_bytes", "image/webp", 300, 300, None)):
                    ok, err = upload_aspirant_photo(user_id="test_asp", file_bytes=b"dummy_bytes")
                    assert ok is False
                    assert "failed to persist profile photo" in err.lower()
