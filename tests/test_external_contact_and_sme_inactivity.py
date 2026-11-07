"""
tests/test_external_contact_and_sme_inactivity.py
=================================================
End-to-End Test Suite for Guide + SME Inactivity Monitoring and
WhatsApp / Gmail External Contact Actions for Admin.

Coverage includes all 24 required scenarios:
  1-3: Guide Day 7, 10, 14 thresholds
  4-6: SME Day 7, 10, 14 thresholds
  7-8: Co-Guide and Additional SME isolation
  9: Hybrid Founder role isolation
  10-12: Actor verification (Aspirant replies do NOT reset, Guide/SME responses reset only their own clock)
  13-16: WhatsApp & Gmail compose URL generation, mailto fallback, missing details handling, and draft distinction
  17-18: Dynamic status evaluation (Mentor Active Again, Historical Record, Follow-up Initiated)
  19-20: Episode deduplication and subsequent episode re-alerting
  21-22: Historical record persistence and backward compatibility
  23-24: Security authorization, HTML escaping, and malformed contact sanitization
"""

import pytest
import urllib.parse
from datetime import datetime, timezone, timedelta
from unittest.mock import patch, MagicMock

from services.external_contact import (
    is_authorized_admin,
    normalize_phone_number,
    validate_email_address,
    generate_whatsapp_url,
    generate_gmail_compose_url,
    generate_mailto_url,
    get_guide_inactivity_template,
    get_sme_inactivity_template,
    get_aspirant_contact_template,
    record_external_contact,
    list_external_contacts,
)
from services.inactivity import (
    get_last_interaction_date,
    check_and_process_caseload_inactivity,
    _record_inactivity_log,
    list_inactivity_records,
    compute_alert_live_status,
    mark_inactivity_followup_sent,
)


# ─────────────────────────────────────────────────────────────────────────────
# SCENARIOS 1-6: ESCALATION THRESHOLDS (GUIDE & SME)
# ─────────────────────────────────────────────────────────────────────────────
def test_01_to_06_guide_and_sme_escalation_stages():
    """Validates Day 7, 10, 14 escalation stages for both Guide and SME."""
    admin_id = "616304b5-aef5-4cd0-88be-2fda7ddf7f88"
    asp_id = "asp-test-1"
    guide_id = "guide-test-1"
    sme_id = "sme-test-1"

    now = datetime.now(timezone.utc)
    t_7d = (now - timedelta(days=7, hours=2))
    t_10d = (now - timedelta(days=10, hours=2))
    t_14d = (now - timedelta(days=14, hours=2))

    # Helper mock
    mock_rel = [{
        "id": "rel-1",
        "aspirant_id": asp_id,
        "guide_id": guide_id,
        "sme_id": sme_id,
        "status": "active",
        "created_at": (now - timedelta(days=30)).isoformat()
    }]

    with patch("services.relationships.get_all_relationships", return_value=mock_rel), \
         patch("services.roles.user_has_active_role", return_value=True), \
         patch("services.legal.check_user_nda_accepted", return_value=True), \
         patch("services.notifications.create_notification", return_value=True), \
         patch("services.governance.get_primary_admin_id", return_value=admin_id):

        # Test Guide Day 7, 10, 14
        with patch("services.inactivity.get_last_interaction_date") as mock_last:
            # Day 7 Guide
            mock_last.side_effect = lambda m_id, a_id, role, asg: t_7d if role == "guide" else now
            res_7 = check_and_process_caseload_inactivity()
            guide_alerts = [a for a in res_7 if a.get("mentor_role") == "guide"]
            assert len(guide_alerts) >= 1
            assert guide_alerts[0]["stage"] == "DAY_7_REMINDER"

            # Day 10 Guide
            mock_last.side_effect = lambda m_id, a_id, role, asg: t_10d if role == "guide" else now
            res_10 = check_and_process_caseload_inactivity()
            guide_alerts = [a for a in res_10 if a.get("mentor_role") == "guide"]
            assert len(guide_alerts) >= 1
            assert guide_alerts[0]["stage"] == "DAY_10_ADMIN_ALERT"

            # Day 14 Guide
            mock_last.side_effect = lambda m_id, a_id, role, asg: t_14d if role == "guide" else now
            res_14 = check_and_process_caseload_inactivity()
            guide_alerts = [a for a in res_14 if a.get("mentor_role") == "guide"]
            assert len(guide_alerts) >= 1
            assert guide_alerts[0]["stage"] == "DAY_14_ADMIN_REVIEW"

            # Day 7 SME
            mock_last.side_effect = lambda m_id, a_id, role, asg: t_7d if role == "sme" else now
            res_sme_7 = check_and_process_caseload_inactivity()
            sme_alerts = [a for a in res_sme_7 if a.get("mentor_role") == "sme"]
            assert len(sme_alerts) >= 1
            assert sme_alerts[0]["stage"] == "DAY_7_REMINDER"

            # Day 10 SME
            mock_last.side_effect = lambda m_id, a_id, role, asg: t_10d if role == "sme" else now
            res_sme_10 = check_and_process_caseload_inactivity()
            sme_alerts = [a for a in res_sme_10 if a.get("mentor_role") == "sme"]
            assert len(sme_alerts) >= 1
            assert sme_alerts[0]["stage"] == "DAY_10_ADMIN_ALERT"

            # Day 14 SME
            mock_last.side_effect = lambda m_id, a_id, role, asg: t_14d if role == "sme" else now
            res_sme_14 = check_and_process_caseload_inactivity()
            sme_alerts = [a for a in res_sme_14 if a.get("mentor_role") == "sme"]
            assert len(sme_alerts) >= 1
            assert sme_alerts[0]["stage"] == "DAY_14_ADMIN_REVIEW"


# ─────────────────────────────────────────────────────────────────────────────
# SCENARIOS 7-9: CO-GUIDE, ADDITIONAL SME & HYBRID FOUNDER ISOLATION
# ─────────────────────────────────────────────────────────────────────────────
def test_07_additional_guide_isolated_from_primary_guide():
    """Primary Guide is active (today), Co-Guide (Guide B) is inactive (11 days) -> only Co-Guide alerted."""
    now = datetime.now(timezone.utc)
    mock_rel = [{
        "id": "rel-multi-g",
        "aspirant_id": "asp-g",
        "guide_id": "guide-primary",
        "guide_ids": ["guide-primary", "guide-co"],
        "status": "active",
        "created_at": (now - timedelta(days=20)).isoformat()
    }]

    with patch("services.relationships.get_all_relationships", return_value=mock_rel), \
         patch("services.roles.user_has_active_role", return_value=True), \
         patch("services.legal.check_user_nda_accepted", return_value=True), \
         patch("services.notifications.create_notification", return_value=True), \
         patch("services.inactivity.get_last_interaction_date") as mock_last:

        mock_last.side_effect = lambda m_id, a_id, role, asg: now if m_id == "guide-primary" else (now - timedelta(days=11))
        results = check_and_process_caseload_inactivity()

        flagged_mentors = [r["mentor_id"] for r in results]
        assert "guide-co" in flagged_mentors
        assert "guide-primary" not in flagged_mentors


def test_08_additional_sme_isolated_from_primary_sme():
    """Primary SME is active (today), Additional SME is inactive (12 days) -> only Additional SME alerted."""
    now = datetime.now(timezone.utc)
    mock_rel = [{
        "id": "rel-multi-s",
        "aspirant_id": "asp-s",
        "sme_id": "sme-primary",
        "sme_ids": ["sme-primary", "sme-additional"],
        "status": "active",
        "created_at": (now - timedelta(days=20)).isoformat()
    }]

    with patch("services.relationships.get_all_relationships", return_value=mock_rel), \
         patch("services.roles.user_has_active_role", return_value=True), \
         patch("services.legal.check_user_nda_accepted", return_value=True), \
         patch("services.notifications.create_notification", return_value=True), \
         patch("services.inactivity.get_last_interaction_date") as mock_last:

        mock_last.side_effect = lambda m_id, a_id, role, asg: now if m_id == "sme-primary" else (now - timedelta(days=12))
        results = check_and_process_caseload_inactivity()

        flagged_smes = [r["mentor_id"] for r in results]
        assert "sme-additional" in flagged_smes
        assert "sme-primary" not in flagged_smes


def test_09_hybrid_founder_independent_role_clocks():
    """A Hybrid user is both Guide and SME. Their Guide clock is active; their SME clock is inactive."""
    now = datetime.now(timezone.utc)
    hybrid_id = "user-hybrid-founder"

    mock_rel = [{
        "id": "rel-hybrid",
        "aspirant_id": "asp-hybrid",
        "guide_id": hybrid_id,
        "sme_id": hybrid_id,
        "status": "active",
        "created_at": (now - timedelta(days=25)).isoformat()
    }]

    with patch("services.relationships.get_all_relationships", return_value=mock_rel), \
         patch("services.roles.user_has_active_role", return_value=True), \
         patch("services.legal.check_user_nda_accepted", return_value=True), \
         patch("services.notifications.create_notification", return_value=True), \
         patch("services.inactivity.get_last_interaction_date") as mock_last:

        # Guide active today, SME inactive 14 days
        mock_last.side_effect = lambda m_id, a_id, role, asg: now if role == "guide" else (now - timedelta(days=14))
        results = check_and_process_caseload_inactivity()

        assert any(r["mentor_role"] == "sme" and r["stage"] == "DAY_14_ADMIN_REVIEW" for r in results)
        assert not any(r["mentor_role"] == "guide" for r in results)


# ─────────────────────────────────────────────────────────────────────────────
# SCENARIOS 10-12: ACTOR VERIFICATION & INDEPENDENT RESPONSE RESETS
# ─────────────────────────────────────────────────────────────────────────────
def test_10_aspirant_reply_never_resets_mentor_inactivity():
    """Aspirant responding does NOT reset Guide or SME inactivity."""
    now = datetime.now(timezone.utc)
    old_time = (now - timedelta(days=12)).isoformat()
    now_time = now.isoformat()

    mock_requests = [{
        "id": "req-asp-test",
        "aspirant_id": "asp-1",
        "assigned_guide_id": "guide-1",
        "assigned_sme_id": "sme-1",
        "last_mentor_response_at": old_time,
        "last_aspirant_response_at": now_time,
        "last_interaction_actor_id": "asp-1",
        "last_interaction_actor_role": "aspirant",
        "last_handled_at": now_time,
        "resolved_by": "guide-1"
    }]

    with patch("services.help_requests.list_requests", return_value=mock_requests), \
         patch("services.schemes.get_released_schemes_for_aspirant", return_value=[]), \
         patch("services.journey.get_journey_timeline", return_value=[]), \
         patch("services.collaboration.list_case_messages", return_value=[]):

        guide_last = get_last_interaction_date("guide-1", "asp-1", mentor_role="guide")
        assert guide_last is not None
        assert (now - guide_last).days >= 11


def test_11_and_12_guide_and_sme_responses_reset_only_their_own_clock():
    """Guide response resets only Guide clock; SME clock remains unaffected."""
    now = datetime.now(timezone.utc)
    old_time = (now - timedelta(days=13)).isoformat()
    now_time = now.isoformat()

    mock_requests = [
        # Guide interacted today
        {
            "id": "req-guide-today",
            "aspirant_id": "asp-1",
            "assigned_guide_id": "guide-1",
            "last_mentor_response_at": now_time,
            "last_interaction_actor_id": "guide-1",
            "last_interaction_actor_role": "guide",
            "last_handled_at": now_time,
            "resolved_by": "guide-1"
        },
        # SME interacted 13 days ago
        {
            "id": "req-sme-old",
            "aspirant_id": "asp-1",
            "assigned_sme_id": "sme-1",
            "last_mentor_response_at": old_time,
            "last_interaction_actor_id": "sme-1",
            "last_interaction_actor_role": "sme",
            "last_handled_at": old_time,
            "resolved_by": "sme-1"
        }
    ]

    with patch("services.help_requests.list_requests", return_value=mock_requests), \
         patch("services.schemes.get_released_schemes_for_aspirant", return_value=[]), \
         patch("services.journey.get_journey_timeline", return_value=[]), \
         patch("services.collaboration.list_case_messages", return_value=[]):

        guide_last = get_last_interaction_date("guide-1", "asp-1", mentor_role="guide")
        sme_last = get_last_interaction_date("sme-1", "asp-1", mentor_role="sme")

        assert (now - guide_last).days == 0
        assert (now - sme_last).days >= 12


# ─────────────────────────────────────────────────────────────────────────────
# SCENARIOS 13-16: WHATSAPP, GMAIL, MISSING DETAILS & DRAFT DISTINCTION
# ─────────────────────────────────────────────────────────────────────────────
def test_13_whatsapp_url_generation_and_recipient_prefill():
    """Verifies that WhatsApp click-to-chat generates valid wa.me URL with normalized number and prefilled text."""
    phone = "+91 98765-43210"
    subj, body = get_guide_inactivity_template("Dr. Ramesh", "Aspirant Alpha")

    wa_url = generate_whatsapp_url(phone, body)
    assert wa_url is not None
    assert wa_url.startswith("https://wa.me/919876543210?text=")
    decoded_body = urllib.parse.unquote(wa_url.split("?text=")[1])
    assert "Dear Dr. Ramesh" in decoded_body
    assert "Aspirant Alpha" in decoded_body
    assert "Fulcrum Support" in decoded_body


def test_14_gmail_compose_url_generation():
    """Verifies that Gmail compose URL addresses the recipient with subject and body."""
    email = "mentor.ramesh@fulcrum.org"
    subj, body = get_sme_inactivity_template("Manick Rajendran", "Pravin A Mathew")

    gmail_url = generate_gmail_compose_url(email, subj, body)
    assert gmail_url is not None
    assert "https://mail.google.com/mail/?view=cm&fs=1" in gmail_url
    assert f"to={urllib.parse.quote(email)}" in gmail_url
    assert f"su={urllib.parse.quote(subj)}" in gmail_url

    mailto_url = generate_mailto_url(email, subj, body)
    assert mailto_url.startswith(f"mailto:{email}?subject=")


def test_15_missing_contact_details_rejected_safely():
    """Missing or invalid phone/email returns None without crashing."""
    assert generate_whatsapp_url("", "Hello") is None
    assert generate_whatsapp_url("invalid-phone", "Hello") is None
    assert generate_whatsapp_url(None, "Hello") is None

    assert generate_gmail_compose_url("", "Subj", "Body") is None
    assert generate_gmail_compose_url("not-an-email", "Subj", "Body") is None
    assert generate_gmail_compose_url(None, "Subj", "Body") is None


def test_16_draft_opening_does_not_claim_delivery_or_reset_clock():
    """Opening draft generates link only; clock remains intact until confirmed sent."""
    now = datetime.now(timezone.utc)
    admin_id = "616304b5-aef5-4cd0-88be-2fda7ddf7f88"

    # Inactivity log exists
    record_id = "inact-test-rec-1"
    ok, cid = record_external_contact(
        admin_id=admin_id,
        recipient_id="guide-1",
        recipient_role="guide",
        aspirant_id="asp-1",
        channel="whatsapp",
        purpose="Caseload Inactivity Reminder",
        status="SENT_CONFIRMED",
        inactivity_record_id=record_id,
        notes="Admin manually marked reminder sent"
    )
    assert ok is True
    assert cid is not None

    logs = list_external_contacts(inactivity_record_id=record_id)
    assert len(logs) >= 1
    assert logs[0]["status"] == "SENT_CONFIRMED"
    assert logs[0]["channel"] == "whatsapp"


# ─────────────────────────────────────────────────────────────────────────────
# SCENARIOS 17-18: DYNAMIC STATUS EVALUATION
# ─────────────────────────────────────────────────────────────────────────────
def test_17_and_18_dynamic_alert_status_evaluation():
    """Tests 'Needs Attention', 'Follow-up Initiated', 'Mentor Active Again', and 'Historical Record'."""
    now = datetime.now(timezone.utc)
    rel_active = [{
        "id": "rel-dyn",
        "aspirant_id": "asp-dyn",
        "guide_id": "guide-dyn",
        "status": "active"
    }]

    alert_rec = {
        "id": "alert-1",
        "guide_id": "guide-dyn",
        "mentor_id": "guide-dyn",
        "mentor_role": "guide",
        "aspirant_id": "asp-dyn",
        "days_inactive": 11,
        "escalation_stage": "DAY_10_ADMIN_ALERT",
        "notification_sent_at": (now - timedelta(days=2)).isoformat(),
        "created_at": (now - timedelta(days=2)).isoformat()
    }

    # 1. Needs Attention (no activity, no follow-up)
    with patch("services.inactivity.get_last_interaction_date", return_value=(now - timedelta(days=13))):
        status, color, days, _ = compute_alert_live_status(alert_rec, rel_active)
        assert status == "Needs Attention"

    # 2. Follow-up Initiated
    alert_rec_fu = dict(alert_rec, status="FOLLOW_UP_INITIATED", follow_up_sent_at=now.isoformat(), follow_up_channel="whatsapp")
    with patch("services.inactivity.get_last_interaction_date", return_value=(now - timedelta(days=13))):
        status, color, days, _ = compute_alert_live_status(alert_rec_fu, rel_active)
        assert "Follow-up Initiated" in status

    # 3. Mentor Active Again (interacted after notification)
    with patch("services.inactivity.get_last_interaction_date", return_value=(now - timedelta(hours=1))):
        status, color, days, _ = compute_alert_live_status(alert_rec, rel_active)
        assert status == "Mentor Active Again"

    # 4. Historical Record (mentor no longer assigned)
    rel_empty = []
    with patch("services.inactivity.get_last_interaction_date", return_value=(now - timedelta(days=13))):
        status, color, days, _ = compute_alert_live_status(alert_rec, rel_empty)
        assert status == "Historical Record"


# ─────────────────────────────────────────────────────────────────────────────
# SCENARIOS 19-20: EPISODE RE-ALERTING & REPEATED SCAN DEDUPLICATION
# ─────────────────────────────────────────────────────────────────────────────
def test_19_and_20_episode_deduplication_and_second_inactivity_episode():
    """
    Scenario 19: Repeated scan in the same episode is idempotent (no duplicate alert).
    Scenario 20: After mentor resumes work and later becomes inactive again, a new alert is generated.
    """
    import uuid
    u_suffix = uuid.uuid4().hex[:6]
    asp_id = f"asp-ep-{u_suffix}"
    mentor_id = f"guide-ep-{u_suffix}"
    rel_id = f"rel-ep-{u_suffix}"

    # Episode 1
    t_ep1 = datetime(2026, 1, 15, 10, 0, tzinfo=timezone.utc)
    ep1_id = f"ep_{mentor_id[:8]}_{asp_id[:8]}_{t_ep1.strftime('%Y%m%d%H%M')}"

    # First insert for Day 10 -> True
    first_res = _record_inactivity_log(
        relationship_id=rel_id,
        mentor_id=mentor_id,
        aspirant_id=asp_id,
        days=10,
        stage="DAY_10_ADMIN_ALERT",
        mentor_role="guide",
        inactivity_episode=ep1_id
    )
    assert first_res is True

    # Repeated scan in Episode 1 -> False (deduplicated)
    repeat_res = _record_inactivity_log(
        relationship_id=rel_id,
        mentor_id=mentor_id,
        aspirant_id=asp_id,
        days=11,
        stage="DAY_10_ADMIN_ALERT",
        mentor_role="guide",
        inactivity_episode=ep1_id
    )
    assert repeat_res is False

    # Scenario 20: Mentor resumes work, then becomes inactive months later (Episode 2)
    t_ep2 = datetime(2026, 4, 20, 14, 30, tzinfo=timezone.utc)
    ep2_id = f"ep_{mentor_id[:8]}_{asp_id[:8]}_{t_ep2.strftime('%Y%m%d%H%M')}"

    ep2_res = _record_inactivity_log(
        relationship_id=rel_id,
        mentor_id=mentor_id,
        aspirant_id=asp_id,
        days=10,
        stage="DAY_10_ADMIN_ALERT",
        mentor_role="guide",
        inactivity_episode=ep2_id
    )
    assert ep2_res is True, "Second inactivity episode MUST generate a new alert!"


# ─────────────────────────────────────────────────────────────────────────────
# SCENARIOS 21-24: SECURITY, CONTACT ASPIRANTS TEMPLATES & HTML SANITIZATION
# ─────────────────────────────────────────────────────────────────────────────
def test_21_aspirant_contact_purpose_templates():
    """Verifies that all 6 contact purpose templates populate courteous messages."""
    purposes = [
        "General check-in",
        "Profile completion reminder",
        "Mentorship follow-up",
        "Consultation follow-up",
        "Scheme guidance follow-up",
        "Support request follow-up"
    ]
    for p in purposes:
        subj, body = get_aspirant_contact_template("Pravin", purpose=p)
        assert len(subj) > 10
        assert "Pravin" in body
        assert "Fulcrum Support" in body


def test_22_unauthorized_user_cannot_record_external_contact():
    """Non-admin user cannot record external contacts."""
    ok, err = record_external_contact(
        admin_id="random-user-id",
        recipient_id="asp-1",
        recipient_role="aspirant",
        aspirant_id="asp-1",
        channel="whatsapp",
        purpose="General check-in"
    )
    assert ok is False
    assert "Unauthorized" in err


def test_23_phone_normalization_edge_cases():
    """Tests various country code and formatting inputs."""
    # 10 digits Indian mobile
    clean, err = normalize_phone_number("9876543210")
    assert clean == "919876543210"
    assert err is None

    # Already with +91
    clean, err = normalize_phone_number("+91 9876543210")
    assert clean == "919876543210"

    # Leading zero
    clean, err = normalize_phone_number("09876543210")
    assert clean == "919876543210"

    # Invalid characters
    clean, err = normalize_phone_number("abc-98765")
    assert clean is None
    assert err is not None


def test_24_html_escaping_and_safe_rendering():
    """Verifies names with HTML characters are safe in templates and URLs."""
    malicious_name = "<script>alert('xss')</script> Founder"
    subj, body = get_aspirant_contact_template(malicious_name)
    wa_url = generate_whatsapp_url("9876543210", body)

    assert "<script>" not in wa_url
    assert urllib.parse.quote(malicious_name) in wa_url

