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
    assert w <= 512 and h <= 512
    assert len(proc_b) < 100 * 1024  # WebP 512x512 should be < 100 KB

