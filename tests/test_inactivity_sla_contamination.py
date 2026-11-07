"""
tests/test_inactivity_sla_contamination.py — Tests that Aspirant responses do not contaminate Guide Inactivity SLA
"""

import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import patch, MagicMock
from services.inactivity import get_last_interaction_date
from services.help_requests import aspirant_respond_request, guide_respond_request

def test_aspirant_response_does_not_reset_guide_inactivity():
    guide_id = "guide-uuid-111"
    aspirant_id = "asp-uuid-222"
    older_time = (datetime.now(timezone.utc) - timedelta(days=12)).isoformat()
    now_time = datetime.now(timezone.utc).isoformat()

    # Case 1: Guide interacted 12 days ago. Aspirant just replied today.
    # The last_interaction_date for the GUIDE must be 12 days ago, NOT today!
    mock_requests = [
        {
            "id": "req-1",
            "aspirant_id": aspirant_id,
            "assigned_guide_id": guide_id,
            "last_mentor_response_at": older_time,
            "last_aspirant_response_at": now_time,
            "last_interaction_actor_id": aspirant_id,
            "last_interaction_actor_role": "aspirant",
            "last_handled_at": now_time,
            "status": "WAITING_ON_GUIDE_SME"
        }
    ]

    with patch("services.help_requests.list_requests", return_value=mock_requests), \
         patch("services.schemes.get_released_schemes_for_aspirant", return_value=[]), \
         patch("services.journey.get_journey_timeline", return_value=[]):

        last_date = get_last_interaction_date(guide_id, aspirant_id)
        assert last_date is not None
        # It must match the older_time (12 days ago), NOT now_time!
        expected_date = datetime.fromisoformat(older_time.replace("Z", "+00:00"))
        assert last_date == expected_date

        days_inactive = (datetime.now(timezone.utc) - last_date).days
        assert days_inactive >= 11

def test_guide_response_updates_inactivity():
    guide_id = "guide-uuid-111"
    aspirant_id = "asp-uuid-222"
    now_time = datetime.now(timezone.utc).isoformat()

    # Case 2: Guide interacted today.
    mock_requests = [
        {
            "id": "req-1",
            "aspirant_id": aspirant_id,
            "assigned_guide_id": guide_id,
            "last_mentor_response_at": now_time,
            "last_interaction_actor_id": guide_id,
            "last_interaction_actor_role": "guide",
            "last_handled_at": now_time,
            "status": "WAITING_ON_ASPIRANT"
        }
    ]

    with patch("services.help_requests.list_requests", return_value=mock_requests), \
         patch("services.schemes.get_released_schemes_for_aspirant", return_value=[]), \
         patch("services.journey.get_journey_timeline", return_value=[]):

        last_date = get_last_interaction_date(guide_id, aspirant_id)
        assert last_date is not None
        days_inactive = (datetime.now(timezone.utc) - last_date).days
        assert days_inactive == 0

