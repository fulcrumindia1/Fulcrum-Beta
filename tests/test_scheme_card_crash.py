"""
tests/test_scheme_card_crash.py — Regression test for render_fund_explorer_card
Verifies that render_fund_explorer_card accepts user_id and is_aspirant kwargs,
and does not raise TypeError or leak private intelligence.
"""

import pytest
from unittest.mock import patch, MagicMock
from services.schemes_ui import render_fund_explorer_card

def test_render_fund_explorer_card_signature_and_execution():
    fake_scheme = {
        "id": "SCH-TEST-001",
        "name": "Test Innovation Scheme",
        "agency": "TANSIM",
        "amount": "₹10,00,000",
        "brief": "Grant for early stage startups",
        "sectors": ["Technology", "Healthcare"],
        "hidden_agenda": "Private Guide Notes",
        "red_flags": "Beware of repayment clause",
        "application_prompt": "Prompt for AI",
        "guide_recommendation": "Strong recommendation"
    }

    # Mock streamlit components to verify crash-freedom without UI server
    with patch("streamlit.markdown") as mock_md, \
         patch("streamlit.expander") as mock_expander, \
         patch("streamlit.columns") as mock_cols:
        
        # Test call as invoked from views/aspirant.py:716
        render_fund_explorer_card(
            fake_scheme,
            user_id="test-aspirant-123",
            is_aspirant=True,
            key_prefix="asp_rel_0_0"
        )

        # Confirm markdown rendered
        assert mock_md.called
        # Aspirant must NOT render AI Pitch Prompt expander
        assert not mock_expander.called

