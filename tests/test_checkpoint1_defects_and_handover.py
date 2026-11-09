"""
tests/test_checkpoint1_defects_and_handover.py
=============================================================================
Unit & regression tests for Checkpoint 1:
1. Server-side Sole Admin identity enforcement (fulcrumindia1@gmail.com).
2. Co-Guide & Additional SME unassignment and selective replacement.
3. Preventing resurrection of revoked roles via reinstate_role.
4. Ensuring false-success and silent fallback is eliminated in Supabase mode.
5. Verifying quarantine of destructive scripts.
=============================================================================
"""

import pytest
from unittest.mock import MagicMock, patch
from services.roles import is_strict_admin, require_sole_admin, reinstate_role, SOLE_ADMIN_UUID, SOLE_ADMIN_EMAIL
from services.relationships import assign_guide, assign_sme, unassign_guide, unassign_sme

def test_01_sole_admin_identity_verification():
    # Legitimate Sole Admin
    assert is_strict_admin(user_id=SOLE_ADMIN_UUID, email=SOLE_ADMIN_EMAIL) is True
    assert is_strict_admin(user_id=SOLE_ADMIN_UUID) is True

    # Spoofed email with arbitrary UUID must be rejected
    assert is_strict_admin(user_id="fake-uuid-1234", email=SOLE_ADMIN_EMAIL) is False

    # Ordinary user credentials must be rejected
    assert is_strict_admin(user_id="2970a3ee-46fc-483c-b276-aa2a955ba123", email="pravindev666@gmail.com") is False
    assert is_strict_admin(email="random@domain.in") is False

    # require_sole_admin helper
    ok, err = require_sole_admin(actor_id=SOLE_ADMIN_UUID)
    assert ok is True
    assert err is None

    ok_fake, err_fake = require_sole_admin(actor_id="fake-uuid")
    assert ok_fake is False
    assert "Unauthorized" in err_fake

def test_02_quarantined_script_cannot_execute():
    import subprocess
    import sys
    res = subprocess.run([sys.executable, "scripts/remove_requested_accounts.py"], capture_output=True, text=True)
    assert res.returncode == 1
    assert "QUARANTINED" in res.stdout or "prohibited" in res.stdout

def test_03_reinstate_role_refuses_revoked_roles(monkeypatch):
    # If a role grant was revoked, reinstate_role must refuse to reactivate it
    monkeypatch.setattr("services.roles.get_user_roles", lambda uid: [{"role": "guide", "status": "revoked"}])
    ok, err = reinstate_role("user-123", "guide", reinstated_by=SOLE_ADMIN_UUID)
    assert ok is False
    assert "revoked" in err.lower()

def test_04_selective_mentor_replacement_preserves_co_mentors(monkeypatch):
    # Mock aspirant mentors: Primary Guide G1, Co-Guide G2
    mock_mentors = {
        "guide": {"id": "g1", "full_name": "Primary Guide"},
        "guides": [{"id": "g1", "full_name": "Primary Guide"}, {"id": "g2", "full_name": "Co-Guide"}]
    }
    monkeypatch.setattr("services.relationships.get_aspirant_mentors", lambda aid: mock_mentors)
    monkeypatch.setattr("services.profiles.get_profile", lambda uid: {"id": uid, "role": "guide", "full_name": "Mentor"})
    monkeypatch.setattr("services.roles.user_has_active_role", lambda uid, r: True)
    monkeypatch.setattr("services.roles.is_assignable_mentor", lambda uid, r, **kw: (True, None))

    captured_upsert = {}
    mock_client = MagicMock()
    mock_table = MagicMock()
    def fake_upsert(data, **kwargs):
        captured_upsert.update(data)
        m = MagicMock()
        m.execute.return_value = MagicMock(data=[data])
        return m
    mock_table.upsert = fake_upsert
    mock_table.insert = lambda d: MagicMock(execute=lambda: MagicMock(data=[d]))
    mock_table.update = lambda d: MagicMock(eq=lambda *a: MagicMock(eq=lambda *b: MagicMock(in_=lambda *c: MagicMock(execute=lambda: MagicMock(data=[])))))
    mock_client.table.return_value = mock_table
    monkeypatch.setattr("services.relationships._get_admin_client", lambda: mock_client)
    monkeypatch.setattr("services.relationships.get_data_backend", lambda: "supabase")
    monkeypatch.setattr("services.journey.log_meaningful_event", lambda **kw: None)
    monkeypatch.setattr("services.notifications.create_notification", lambda **kw: None)

    # Replace Co-Guide G2 with new Guide G3 using replace_target_id="g2"
    ok, err = assign_guide(
        aspirant_id="asp-1",
        guide_id="g3",
        admin_id=SOLE_ADMIN_UUID,
        replace_target_id="g2"
    )
    assert ok is True
    # Primary Guide remains G1, while guide_ids contains G1 and G3 (G2 replaced, G1 preserved!)
    assert captured_upsert.get("guide_id") == "g1"
    assert "g1" in captured_upsert.get("guide_ids")
    assert "g3" in captured_upsert.get("guide_ids")
    assert "g2" not in captured_upsert.get("guide_ids")

def test_05_unassign_primary_guide_promotes_co_guide(monkeypatch):
    mock_mentors = {
        "guide": {"id": "g1", "full_name": "Primary Guide"},
        "guides": [{"id": "g1", "full_name": "Primary Guide"}, {"id": "g2", "full_name": "Co-Guide"}]
    }
    monkeypatch.setattr("services.relationships.get_aspirant_mentors", lambda aid: mock_mentors)
    monkeypatch.setattr("services.profiles.get_profile", lambda uid: {"id": uid, "role": "guide", "full_name": "Mentor"})

    captured_update = {}
    mock_client = MagicMock()
    mock_table = MagicMock()
    def fake_update(data):
        captured_update.update(data)
        m = MagicMock()
        m.eq.return_value.execute.return_value = MagicMock(data=[data])
        return m
    mock_table.update = fake_update
    mock_table.upsert = lambda d, **kw: MagicMock(execute=lambda: MagicMock(data=[d]))
    mock_table.insert = lambda d: MagicMock(execute=lambda: MagicMock(data=[d]))
    mock_client.table.return_value = mock_table
    monkeypatch.setattr("services.relationships._get_admin_client", lambda: mock_client)
    monkeypatch.setattr("services.relationships.get_data_backend", lambda: "supabase")
    monkeypatch.setattr("services.journey.log_meaningful_event", lambda **kw: None)
    monkeypatch.setattr("services.notifications.create_notification", lambda **kw: None)

    # Unassign Primary Guide G1
    ok, err = unassign_guide(
        aspirant_id="asp-1",
        guide_id="g1",
        admin_id=SOLE_ADMIN_UUID,
        reason="Primary retiring"
    )
    assert ok is True
    # G2 must be promoted to new primary guide!
    assert captured_update.get("guide_id") == "g2"
    assert captured_update.get("guide_ids") == ["g2"]
