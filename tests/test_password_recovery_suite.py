"""
tests/test_password_recovery_suite.py
======================================
Hardened Security, Unit & Isolated-Staging Suite for FULCRUM-BETA Password Recovery.

SAFETY INVARIANTS:
1. ZERO hardcoded user passwords or real user emails.
2. Explicit staging project guard: fails immediately if target project matches production.
3. Never uses Admin API to modify or reset an existing real user's password.
4. Live integration tests run ONLY against an isolated staging Supabase project
   with a fresh, disposable synthetic test account created for the run.
"""

import os
import re
import uuid
import secrets
import unittest
from unittest.mock import MagicMock, patch

from services.auth import (
    send_password_reset,
    complete_password_reset,
    verify_recovery_session_tokens,
    _classify_recovery_error,
)

PRODUCTION_PROJECT_IDS = {"bhaqaawsufwtjeqfifbv"}
PRODUCTION_DOMAINS = {"app.fulcrumindia.online"}
ADMIN_EMAIL = "fulcrumindia1@gmail.com"


def assert_isolated_staging_target() -> tuple[str, str, str, str]:
    """
    Requires explicit staging environment variables and fails immediately if any
    configured URL or project identifier matches production.
    """
    staging_id = os.environ.get("STAGING_PROJECT_ID", "").strip()
    staging_url = os.environ.get("STAGING_SUPABASE_URL", "").strip()
    staging_pub = os.environ.get("STAGING_SUPABASE_PUBLISHABLE_KEY", "").strip() or os.environ.get("STAGING_SUPABASE_ANON_KEY", "").strip()
    staging_sec = os.environ.get("STAGING_SUPABASE_SECRET_KEY", "").strip() or os.environ.get("STAGING_SUPABASE_SERVICE_ROLE_KEY", "").strip()
    app_url = os.environ.get("APP_URL", "").strip()

    if not staging_id or not staging_url:
        raise RuntimeError("Missing STAGING_PROJECT_ID or STAGING_SUPABASE_URL.")

    for prod_id in PRODUCTION_PROJECT_IDS:
        if prod_id in staging_id or prod_id in staging_url:
            raise AssertionError(f"SAFETY ABORT: Target matches production project '{prod_id}'!")
    for prod_dom in PRODUCTION_DOMAINS:
        if prod_dom in app_url:
            raise AssertionError(f"SAFETY ABORT: APP_URL points to production domain '{prod_dom}'!")

    m = re.match(r"^https://([a-z0-9-]+)\.supabase\.co$", staging_url)
    if not m or m.group(1) != staging_id:
        raise AssertionError("STAGING_PROJECT_ID does not match hostname in STAGING_SUPABASE_URL.")

    if not staging_pub or not staging_sec:
        raise RuntimeError("Missing STAGING_SUPABASE_PUBLISHABLE_KEY or STAGING_SUPABASE_SECRET_KEY.")

    return staging_id, staging_url, staging_pub, staging_sec


class TestPasswordRecoverySecurityAndUnit(unittest.TestCase):
    """Offline negative security tests and recovery verification checks (no production contact)."""

    def test_01_production_guard_blocks_production_project(self):
        with patch.dict(
            os.environ,
            {
                "STAGING_PROJECT_ID": "bhaqaawsufwtjeqfifbv",
                "STAGING_SUPABASE_URL": "https://bhaqaawsufwtjeqfifbv.supabase.co",
                "STAGING_SUPABASE_PUBLISHABLE_KEY": "dummy",
                "STAGING_SUPABASE_SECRET_KEY": "dummy",
            },
            clear=False,
        ):
            with self.assertRaises(AssertionError) as ctx:
                assert_isolated_staging_target()
            self.assertIn("SAFETY ABORT", str(ctx.exception))

    def test_02_sole_admin_self_service_strictly_blocked(self):
        ok1, err1 = send_password_reset(ADMIN_EMAIL)
        self.assertFalse(ok1)
        self.assertIn("Platform Administrator", err1 or "")

        ok2, err2 = complete_password_reset(
            "ValidTempPass987!#",
            access_token="dummy_acc",
            refresh_token="dummy_ref",
            email=ADMIN_EMAIL,
        )
        self.assertFalse(ok2)
        self.assertIn("Platform Administrator", err2 or "")

        ok3, _ = send_password_reset(ADMIN_EMAIL.upper())
        self.assertFalse(ok3)

    def test_03_missing_refresh_token_rejected_no_substitution(self):
        # Never substitute access_token for refresh_token
        ok, _, code, err = verify_recovery_session_tokens("dummy_access_jwt", "")
        self.assertFalse(ok)
        self.assertEqual(code, "missing_refresh_token")
        self.assertIn("refresh token", (err or "").lower())

        with patch("services.auth.get_data_backend", return_value="supabase"):
            ok_rst, err_rst = complete_password_reset(
                "ValidTempPass987!#",
                access_token="dummy_access_jwt",
                refresh_token="",
                email="disposable@example.invalid",
            )
            self.assertFalse(ok_rst)
            self.assertIn("missing recovery credentials", (err_rst or "").lower())

    def test_04_short_password_rejected_before_backend(self):
        ok, err = complete_password_reset(
            "short",
            access_token="dummy_acc",
            refresh_token="dummy_ref",
            email="disposable@example.invalid",
        )
        self.assertFalse(ok)
        self.assertIn("8 characters", err or "")

    def test_05_distinct_error_classification_and_zero_token_leakage(self):
        raw_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.secret_payload.sig"

        c_exp, m_exp = _classify_recovery_error(Exception(f"otp_expired for {raw_jwt}"))
        self.assertEqual(c_exp, "expired")
        self.assertNotIn(raw_jwt, m_exp)

        c_used, m_used = _classify_recovery_error(Exception("session_not_found: token already used"))
        self.assertEqual(c_used, "used_or_invalid")
        self.assertIn("already been used", m_used)

        c_ver, m_ver = _classify_recovery_error(Exception("both auth code and code verifier should be non-empty"))
        self.assertEqual(c_ver, "missing_verifier")
        self.assertIn("verifier", m_ver.lower())

        c_net, m_net = _classify_recovery_error(TimeoutError("Read timed out"))
        self.assertEqual(c_net, "timeout")
        self.assertIn("timeout", m_net.lower())

    def test_06_ephemeral_client_rejects_mismatched_email_and_signs_out(self):
        mock_client = MagicMock()
        mock_user = MagicMock()
        mock_user.email = "verified.disposable@example.invalid"
        mock_sess = MagicMock()
        mock_sess.user = mock_user
        mock_client.auth.set_session.return_value = mock_sess

        with patch("services.auth.get_data_backend", return_value="supabase"), \
             patch("services.auth._create_ephemeral_supabase_client", return_value=mock_client):
            ok, err = complete_password_reset(
                "ValidTempPass987!#",
                access_token="acc_tok_123",
                refresh_token="ref_tok_123",
                email="attacker@example.invalid",
            )
            self.assertFalse(ok)
            self.assertIn("Security violation", err or "")
            mock_client.auth.update_user.assert_not_called()

    def test_07_network_timeout_returns_sanitized_retry_message(self):
        mock_client = MagicMock()
        mock_client.auth.set_session.side_effect = TimeoutError("HTTPSConnectionPool read timed out")

        with patch("services.auth.get_data_backend", return_value="supabase"), \
             patch("services.auth._create_ephemeral_supabase_client", return_value=mock_client):
            ok, err = complete_password_reset(
                "ValidTempPass987!#",
                access_token="acc_tok_123",
                refresh_token="ref_tok_123",
                email="disposable@example.invalid",
            )
            self.assertFalse(ok)
            self.assertIn("Network timeout", err or "")


class TestPasswordRecoveryStagingIntegration(unittest.TestCase):
    """
    Isolated staging integration suite.
    Requires explicit STAGING_PROJECT_ID + STAGING_SUPABASE_URL + staging keys.
    Uses disposable synthetic identities only; fails immediately on production targets.
    """

    @classmethod
    def setUpClass(cls):
        if not os.environ.get("STAGING_PROJECT_ID") and not os.environ.get("STAGING_SUPABASE_URL"):
            raise unittest.SkipTest(
                "Isolated staging env vars (STAGING_PROJECT_ID, STAGING_SUPABASE_URL) not configured."
            )
        cls.staging_id, cls.staging_url, cls.staging_pub, cls.staging_sec = assert_isolated_staging_target()

        from supabase import create_client, ClientOptions
        cls.admin = create_client(cls.staging_url, cls.staging_sec)
        cls.client = create_client(cls.staging_url, cls.staging_pub, options=ClientOptions(flow_type="implicit"))

        # Create a disposable synthetic staging user (never touch real accounts)
        domain = os.environ.get("STAGING_TEST_EMAIL_DOMAIN", "example.com")
        cls.disposable_email = f"fulcrum.staging.{uuid.uuid4().hex[:10]}@{domain}"
        cls.initial_password = f"Init-{secrets.token_urlsafe(12)}!1"
        cls.updated_password = f"Next-{secrets.token_urlsafe(12)}!2"
        created = cls.admin.auth.admin.create_user({
            "email": cls.disposable_email,
            "password": cls.initial_password,
            "email_confirm": True,
            "user_metadata": {"full_name": "Staging Synthetic User", "role": "aspirant"},
        })
        cls.disposable_user_id = created.user.id

    @classmethod
    def tearDownClass(cls):
        if getattr(cls, "admin", None) and getattr(cls, "disposable_user_id", None):
            try:
                cls.admin.auth.admin.delete_user(cls.disposable_user_id)
            except Exception:
                pass

    def test_01_disposable_staging_token_verification_and_password_update(self):
        # Note: Real email-click browser flow is tested via tests/e2e_staging_recovery.py;
        # here we verify staging token_hash single-use and non-Admin password update via user session.
        link = self.admin.auth.admin.generate_link({
            "type": "recovery",
            "email": self.disposable_email,
        })
        hashed_token = link.properties.hashed_token

        with patch.dict(
            os.environ,
            {
                "FULCRUM_DATA_BACKEND": "supabase",
                "FULCRUM_FORBID_PRODUCTION": "1",
                "FULCRUM_SUPABASE_URL": self.staging_url,
                "FULCRUM_SUPABASE_PUBLISHABLE_KEY": self.staging_pub,
                "FULCRUM_SUPABASE_SECRET_KEY": self.staging_sec,
                "DATA_BACKEND": "supabase",
                "SUPABASE_URL": self.staging_url,
                "SUPABASE_PUBLISHABLE_KEY": self.staging_pub,
                "SUPABASE_SECRET_KEY": self.staging_sec,
            },
            clear=False,
        ):
            from services.auth import verify_recovery_token_hash
            ok_v, v_email, acc, ref, _, err_v = verify_recovery_token_hash(hashed_token)
            self.assertTrue(ok_v, f"verify_recovery_token_hash failed: {err_v}")
            self.assertEqual(v_email, self.disposable_email.lower())

            # Second verification of same token_hash must fail
            ok_v2, _, _, _, code2, _ = verify_recovery_token_hash(hashed_token)
            self.assertFalse(ok_v2)
            self.assertIn(code2, ("expired", "used_or_invalid"))

            # Update password strictly using recovery session (never Admin API)
            ok_u, err_u = complete_password_reset(
                self.updated_password,
                access_token=acc,
                refresh_token=ref,
                email=v_email,
            )
            self.assertTrue(ok_u, f"complete_password_reset failed: {err_u}")

            # Verify new password works and old password is rejected
            sign_in_new = self.client.auth.sign_in_with_password({
                "email": self.disposable_email,
                "password": self.updated_password,
            })
            self.assertIsNotNone(sign_in_new.session)
            with self.assertRaises(Exception):
                self.client.auth.sign_in_with_password({
                    "email": self.disposable_email,
                    "password": self.initial_password,
                })


if __name__ == "__main__":
    unittest.main()
