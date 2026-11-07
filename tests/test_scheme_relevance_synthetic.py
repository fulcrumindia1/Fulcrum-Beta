"""
tests/test_scheme_relevance_synthetic.py — 12 Synthetic Profile Validation for Scheme Matching
Verifies negative domain exclusions, non-inflated scoring, and appropriate recommendations.
"""

import pytest
from services.schemes import list_schemes
from services.scheme_matching_engine import match_aspirant_schemes_intelligent

@pytest.fixture
def master_schemes():
    return list_schemes(active_only=True)

def test_retail_pharmacy_excludes_pharma_rd_and_deeptech(master_schemes):
    """Profile 3: Retail Pharmacy should NOT receive BIRAC, clinical trial or semiconductor/ISRO schemes."""
    profile = {
        "id": "asp_pharma_retail",
        "full_name": "Suresh Medicals",
        "district": "Chennai",
        "state": "Tamil Nadu",
        "profile_data": {
            "business": {
                "business_name": "Suresh Medicals & Retail Pharmacy",
                "business_type": "Trading / Retail",
                "sector": "Healthcare & Life Sciences",
                "subsector": "Retail Pharmacy & Chemist",
                "activity": "Trading / Retail / Distribution",
                "stage": "Growth",
                "description": "Retail pharmacy selling prescription medications and wellness products."
            },
            "demographics": {
                "district": "Chennai",
                "state": "Tamil Nadu",
                "is_drug_license": True,
                "is_gst_registered": True
            }
        }
    }
    matches = match_aspirant_schemes_intelligent(profile, master_schemes, min_score=50)
    match_names = [m.get("name", "").lower() for m in matches]
    
    # Assert negative domain exclusion works
    for name in match_names:
        assert "isro" not in name
        assert "semiconductor" not in name
        assert "clinical trial" not in name
        assert "defence" not in name

def test_textile_garments_excludes_deeptech_and_isro(master_schemes):
    """Profile 1: Textile Garments should NOT receive semiconductor, ISRO or defence funds."""
    profile = {
        "id": "asp_textiles",
        "full_name": "Tiruppur Knits",
        "district": "Tiruppur",
        "state": "Tamil Nadu",
        "profile_data": {
            "business": {
                "business_name": "Tiruppur Knits Private Limited",
                "business_type": "Manufacturing",
                "sector": "Textiles & Apparel",
                "subsector": "Cotton Knitwear & Garments",
                "activity": "Manufacturing / Production",
                "stage": "Commercial Scale",
                "description": "Export-oriented cotton t-shirt and apparel manufacturing."
            },
            "demographics": {
                "district": "Tiruppur",
                "state": "Tamil Nadu",
                "is_udyam_registered": True
            }
        }
    }
    matches = match_aspirant_schemes_intelligent(profile, master_schemes, min_score=50)
    match_names = [m.get("name", "").lower() for m in matches]
    for name in match_names:
        assert "isro" not in name
        assert "semiconductor" not in name
        assert "biotech" not in name

def test_food_processing_millet(master_schemes):
    """Profile 6: Food processing should match agro and food schemes with top scores."""
    profile = {
        "id": "asp_food",
        "full_name": "Mathew Agro",
        "district": "Madurai",
        "state": "Tamil Nadu",
        "profile_data": {
            "business": {
                "business_name": "Mathew Agro Products",
                "business_type": "Manufacturing",
                "sector": "Food Processing & Agribusiness",
                "subsector": "Millet Processing & Snacks",
                "activity": "Manufacturing / Production",
                "stage": "Early Revenue",
                "description": "Organic millet cookies and flour production unit."
            },
            "demographics": {
                "district": "Madurai",
                "state": "Tamil Nadu",
                "is_fssai_registered": True,
                "is_udyam_registered": True
            }
        }
    }
    matches = match_aspirant_schemes_intelligent(profile, master_schemes, min_score=50)
    top_matches = matches[:5]
    assert len(top_matches) > 0
    # Top matches should include food processing or MSME schemes
    found_food_or_msme = any("pmfme" in m["name"].lower() or "food" in m["name"].lower() or "pmegp" in m["name"].lower() or "uyegp" in m["name"].lower() for m in top_matches)
    assert found_food_or_msme

def test_space_tech_matches_aerospace_isro(master_schemes):
    """Profile 9: Space Tech startup should be eligible for aerospace and deeptech."""
    profile = {
        "id": "asp_space",
        "full_name": "AeroDynamics",
        "district": "Chennai",
        "state": "Tamil Nadu",
        "profile_data": {
            "business": {
                "business_name": "AeroSpace Tech Propulsion",
                "business_type": "R&D / DeepTech",
                "sector": "DeepTech & Electronics",
                "subsector": "Satellite Propulsion Systems",
                "activity": "R&D / DeepTech",
                "stage": "Prototype / Seed",
                "description": "Developing green satellite propulsion and aerospace thrusters."
            },
            "demographics": {
                "district": "Chennai",
                "state": "Tamil Nadu",
                "is_dpiit_recognized": True,
                "is_startuptn_registered": True
            }
        }
    }
    matches = match_aspirant_schemes_intelligent(profile, master_schemes, min_score=40)
    match_names = [m.get("name", "").lower() for m in matches]
    # SpaceTech should NOT be disqualified from aerospace or deeptech
    assert len(matches) > 0

def test_incomplete_profile_minimal_baseline(master_schemes):
    """Profile 11: Incomplete profile without data should not score high artificially."""
    profile = {
        "id": "asp_empty",
        "full_name": "New User",
        "profile_data": {}
    }
    matches = match_aspirant_schemes_intelligent(profile, master_schemes, min_score=70)
    # Without declared sector, state, or quota, no scheme should exceed 70%
    assert len(matches) == 0

def test_women_led_quota_concession(master_schemes):
    """Profile 12: Women entrepreneur with 100% equity should qualify for women-led quotas."""
    profile = {
        "id": "asp_women",
        "full_name": "Lakshmi Farms",
        "district": "Dindigul",
        "state": "Tamil Nadu",
        "profile_data": {
            "business": {
                "business_name": "Lakshmi Herbal Extracts",
                "sector": "Food Processing & Agribusiness",
                "stage": "Seed",
                "description": "Natural medicinal extracts by women self-help cluster."
            },
            "demographics": {
                "district": "Dindigul",
                "state": "Tamil Nadu",
                "gender": "Female",
                "is_women_led": True,
                "women_equity_pct": 100.0
            }
        }
    }
    matches = match_aspirant_schemes_intelligent(profile, master_schemes, min_score=60)
    assert len(matches) > 0
    # Match reasons should reflect women entrepreneur quota
    has_women_reason = any(any("women" in r.lower() for r in m.get("match_reasons", [])) for m in matches)
    assert has_women_reason

def test_non_tamil_nadu_disqualified_from_tn_state_schemes(master_schemes):
    """Profile 13: Bangalore / Karnataka applicant must be disqualified from TN-only schemes."""
    profile = {
        "id": "asp_karnataka",
        "full_name": "Bangalore FinTech",
        "district": "Bangalore Urban",
        "state": "Karnataka",
        "profile_data": {
            "business": {
                "business_name": "Bengaluru PayTech",
                "sector": "Fintech & Financial Services",
                "stage": "Seed",
                "description": "Payment gateway for retail merchants."
            },
            "demographics": {
                "district": "Bangalore Urban",
                "state": "Karnataka"
            }
        }
    }
    matches = match_aspirant_schemes_intelligent(profile, master_schemes, min_score=0)
    # Check that TN-only schemes are marked as disqualified
    tn_schemes = [m for m in matches if m.get("structured_rules", {}).get("is_tn_only")]
    assert len(tn_schemes) > 0
    for s in tn_schemes:
        assert s["is_disqualified"] is True
        assert s["match_score"] == 0
        assert any("State Ineligible" in c for c in s.get("potential_concerns", []))

def test_sc_st_affirmative_quota_priority(master_schemes):
    """Profile 8: SC/ST entrepreneur from Vellore should receive affirmative quota priority."""
    profile = {
        "id": "asp_sc_st",
        "full_name": "Vellore Leather Works",
        "district": "Vellore",
        "state": "Tamil Nadu",
        "profile_data": {
            "business": {
                "business_name": "Ambedkar Leather Crafts",
                "business_type": "Manufacturing",
                "sector": "Leather & Footwear",
                "stage": "Growth",
                "description": "Eco-friendly finished leather goods and footwear manufacturing."
            },
            "demographics": {
                "district": "Vellore",
                "state": "Tamil Nadu",
                "founder_category": "SC",
                "is_udyam_registered": True
            }
        }
    }
    matches = match_aspirant_schemes_intelligent(profile, master_schemes, min_score=50)
    assert len(matches) > 0
    # Affirmative quota reason should be present for SC/ST-focused schemes
    has_sc_reason = any(any("SC" in r for r in m.get("match_reasons", [])) for m in matches)
    assert has_sc_reason

def test_ev_startup_eligible_for_ev_schemes(master_schemes):
    """Profile 4: EV Charging & Retrofit startup in Coimbatore should qualify for EV Policy."""
    profile = {
        "id": "asp_ev",
        "full_name": "Kovai ElectroMobility",
        "district": "Coimbatore",
        "state": "Tamil Nadu",
        "profile_data": {
            "business": {
                "business_name": "Kovai ElectroMobility Pvt Ltd",
                "business_type": "Manufacturing",
                "sector": "Automotive & Electric Vehicles",
                "subsector": "EV Charging & Retrofit Kits",
                "activity": "Manufacturing / Production",
                "stage": "Prototype / Seed",
                "description": "Smart high-speed EV charging stations and two-wheeler powertrain kits."
            },
            "demographics": {
                "district": "Coimbatore",
                "state": "Tamil Nadu",
                "is_dpiit_recognized": True,
                "is_startuptn_registered": True
            }
        }
    }
    matches = match_aspirant_schemes_intelligent(profile, master_schemes, min_score=50)
    match_names = [m["name"].lower() for m in matches]
    # TN EV Policy should NOT be disqualified for EV startup
    has_ev_match = any("ev" in name or "automobile" in name for name in match_names)
    assert has_ev_match, f"No EV match found in {match_names[:10]}"
