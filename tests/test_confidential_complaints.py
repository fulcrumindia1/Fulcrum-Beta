"""
tests/test_confidential_complaints.py — Tests for confidential complaints submitted to Fulcrum Support
"""

import pytest
from unittest.mock import patch, MagicMock
from services.governance import submit_guide_complaint, get_primary_admin_id

def test_submit_guide_complaint_validation():
    # Should reject too short details
    ok, err = submit_guide_complaint("asp-1", "guide-1", "inactivity", "too short")
    assert not ok
    assert "minimum 10 characters" in err

    # Should reject invalid reason
    ok, err = submit_guide_complaint("asp-1", "guide-1", "invalid_reason", "Valid length details context")
    assert not ok
    assert "Invalid complaint reason" in err

def test_submit_guide_complaint_without_guide():
    with patch("services.governance.get_supabase_admin_client") as mock_admin, \
         patch("services.governance.get_data_backend", return_value="supabase"), \
         patch("services.notifications.create_notification") as mock_notify:
        
        mock_client = MagicMock()
        mock_table = MagicMock()
        mock_admin.return_value = mock_client
        mock_client.table.return_value = mock_table
        mock_table.insert.return_value.execute.return_value.data = [{"id": "comp-123"}]

        ok, comp_id = submit_guide_complaint("asp-user", None, "inactivity", "Guide has not responded in over 14 days.")
        assert ok
        assert comp_id is not None
        # Assert notification sent to primary admin
        assert mock_notify.called
        assert mock_notify.call_args[1]["user_id"] == get_primary_admin_id()

