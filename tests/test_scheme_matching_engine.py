"""
tests/test_scheme_matching_engine.py — Automated Unit Tests for X+Y->Z Matching & Photo Services
"""

import pytest
from services.scheme_rules import parse_quantum_limits, get_scheme_structured_rules
from services.scheme_matching_engine import (
    normalize_aspirant_profile,
    evaluate_gatekeeper_eligibility,
    calculate_relevance_score,
    build_evidence_checklist,
    match_aspirant_schemes_intelligent
)
from services.aspirant_photos import validate_and_process_photo
import io
from PIL import Image


def test_quantum_parsing():
    min_l, max_l = parse_quantum_limits("Up to ₹25 Lakhs")
    assert max_l == 25.0

    min_l, max_l = parse_quantum_limits("₹50 Lakhs to ₹5 Crores")
    assert min_l == 50.0
    assert max_l == 500.0


def test_women_only_gatekeeper_disqualification():
    male_profile = {
        "id": "male-1",
        "full_name": "Male Founder",
        "state": "Tamil Nadu",
        "district": "Madurai",
        "profile_data": {
            "personal": {"gender": "Male"},
            "business": {"sector": "Food Processing", "stage": "Seed"},
            "demographics": {"is_women_led": False, "women_equity_pct": 0, "founder_category": "General"}
        }
    }
    x = normalize_aspirant_profile(male_profile)
    assert not x["is_women_led"]

    scheme = {
        "id": "sch-twees",
        "name": "TWEES Women Entrepreneurship Scheme",
        "state_scope": "Tamil Nadu",
        "eligibility": ["Must have at least 51% women equity"]
    }
    rules = get_scheme_structured_rules(scheme)
    assert rules["is_women_only"]

    is_eligible, disq, warnings = evaluate_gatekeeper_eligibility(x, scheme, rules)
    assert not is_eligible
    assert any("women" in d.lower() for d in disq)


def test_category_affirmative_quota_isolation():
    general_profile = {
        "id": "gen-1",
        "full_name": "General Founder",
        "state": "Tamil Nadu",
        "district": "Madurai",
        "profile_data": {
            "personal": {"gender": "Male"},
            "business": {"sector": "Food Processing", "stage": "Seed"},
            "demographics": {"is_women_led": False, "women_equity_pct": 0, "founder_category": "General"}
        }
    }
    x = normalize_aspirant_profile(general_profile)

    scheme = {
        "id": "sch-scst",
        "name": "Special SC/ST Entrepreneur Subsidy",
        "state_scope": "All India",
        "brief": "Affirmative capital subsidy for SC/ST founders",
        "eligibility": ["SC/ST founders only"]
    }
    rules = get_scheme_structured_rules(scheme)
    assert rules["is_sc_st_only"]

    is_eligible, disq, warnings = evaluate_gatekeeper_eligibility(x, scheme, rules)
    assert not is_eligible
    assert any("category" in d.lower() for d in disq)


def test_state_jurisdiction_gatekeeper():
    karnataka_profile = {
        "id": "kar-1",
        "full_name": "Karnataka Founder",
        "state": "Karnataka",
        "district": "Bengaluru",
        "profile_data": {
            "personal": {"gender": "Male"},
            "business": {"sector": "IT & Services", "stage": "Early Traction"},
            "demographics": {"state": "Karnataka", "district": "Bengaluru"}
        }
    }
    x = normalize_aspirant_profile(karnataka_profile)
    assert not x["is_tn"]

    scheme = {
        "id": "sch-uyegp",
        "name": "Unemployed Youth Employment Generation Programme (UYEGP)",
        "agency": "MSME Department, Government of Tamil Nadu",
        "state_scope": "Tamil Nadu",
        "eligibility": ["Resident of Tamil Nadu"]
    }
    rules = get_scheme_structured_rules(scheme)
    assert rules["is_tn_only"]

    is_eligible, disq, warnings = evaluate_gatekeeper_eligibility(x, scheme, rules)
    assert not is_eligible
    assert any("state" in d.lower() or "tamil nadu" in d.lower() for d in disq)


def test_photo_validation_and_compression():
    img = Image.new("RGB", (1024, 1024), color=(37, 99, 235))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    raw_bytes = buf.getvalue()

    ok, proc_b, ctype, w, h, err = validate_and_process_photo(raw_bytes)
    assert ok
    assert ctype == "image/webp"
    assert w <= 320 and h <= 320
    assert len(proc_b) <= 150 * 1024  # Strict 150 KB stored-file cap


def test_saved_profile_assistance_need_matching():
    # Profile with assistance_need saved in profile_data
    profile_with_need = {
        "id": "asp-need-01",
        "full_name": "Agri Tech Founder",
        "state": "Tamil Nadu",
        "district": "Madurai",
        "profile_data": {
            "personal": {"gender": "Male"},
            "business": {"sector": "Food Processing & Agribusiness", "stage": "Pre-Seed / Seed"},
            "demographics": {"state": "Tamil Nadu", "district": "Madurai", "founder_category": "General"},
            "assistance_need": {
                "assistance_goal": "Capital Grant / Seed Subsidy",
                "support_type": "Direct Project Subsidy (Capex)",
                "quantum_range": "MICRO (< ₹5 Lakhs)",
                "timeframe": "NEAR_TERM (1 to 3 Months)"
            }
        }
    }

    schemes = [
        {
            "id": "sch-pmfme",
            "name": "PM Formalisation of Micro Food Processing Enterprises (PM FME)",
            "agency": "Ministry of Food Processing Industries",
            "funding_type": "Grant / Capital Subsidy",
            "sectors": ["Food Processing & Agribusiness"],
            "stage": "Seed",
            "amount": "Up to ₹10 Lakhs",
            "state_scope": "National",
            "is_active": True
        }
    ]

    # Calling matching engine WITHOUT passing assistance_need explicitly
    # The engine must automatically extract it from profile["profile_data"]["assistance_need"]
    matches = match_aspirant_schemes_intelligent(profile_with_need, schemes, assistance_need=None, min_score=50)
    assert len(matches) == 1
    m = matches[0]
    assert m["match_score"] >= 80
    assert any("assistance need match" in r.lower() or "capital grant" in r.lower() for r in m["match_reasons"])


