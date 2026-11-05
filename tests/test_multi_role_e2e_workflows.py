"""
tests/test_multi_role_e2e_workflows.py — End-to-End Verification of Multi-Role Promotion,
Cross-Workspace Isolation, Mentorship Assignment, Scheme Release, and Bidirectional Messaging.
"""

import pytest
import uuid
from datetime import datetime, timezone

from services.local_db import get_local_db
from services.profiles import get_profile, list_profiles_by_role, update_aspirant_profile
from services.roles import (
    grant_role,
    activate_role,
    get_user_roles,
    get_active_roles,
    get_pending_nda_roles,
    user_has_active_role
)
from services.relationships import (
    assign_guide,
    assign_sme,
    get_aspirant_mentors,
    get_assigned_aspirants_for_guide,
    get_assigned_aspirants_for_sme
)
from services.schemes import (
    match_schemes_for_aspirant,
    release_scheme_to_aspirant,
    get_released_schemes_for_aspirant
)
from services.help_requests import (
    create_request,
    list_requests,
    list_guide_requests,
    list_sme_requests,
    guide_respond_request,
    sme_respond_request
)
from services.legal import record_legal_acceptance


@pytest.fixture(autouse=True)
def force_sqlite_backend(monkeypatch):
    monkeypatch.setenv("DATA_BACKEND", "sqlite")
    from services.cache import invalidate_memo
    invalidate_memo()


@pytest.fixture(scope="module")
def setup_e2e_profiles():
    db = get_local_db()

    # Generate 3 unique valid UUIDs for PostgreSQL schema compatibility
    p_alpha_id = str(uuid.uuid4())
    p_hybrid_id = str(uuid.uuid4())
    p_beta_id = str(uuid.uuid4())
    admin_id = str(uuid.uuid4())

    # Profile 1: Aspirant Alpha (Organic Food Processing)
    prof_alpha = {
        "id": p_alpha_id,
        "email": f"alpha_{uuid.uuid4().hex[:8]}@test.local",
        "full_name": "Aspirant Alpha (Food Founder)",
        "role": "aspirant",
        "district": "Madurai",
        "state": "Tamil Nadu",
        "profile_data": {
            "personal": {"gender": "Male"},
            "professional": {"education": "B.Tech Food Technology"},
            "business": {
                "business_name": "Madurai Millet Naturals",
                "sector": "Food Processing & Agribusiness",
                "stage": "Pre-Seed / Seed"
            },
            "demographics": {"district": "Madurai", "state": "Tamil Nadu", "founder_category": "General"},
            "assistance_need": {
                "assistance_goal": "Capital Grant / Seed Subsidy",
                "support_type": "Direct Project Subsidy (Capex)",
                "quantum_range": "MICRO (< ₹5 Lakhs)",
                "timeframe": "NEAR_TERM (1 to 3 Months)"
            }
        },
        "is_active": True
    }

    # Profile 2: Hybrid Entrepreneur (Agritech IoT Solutions - Starts as Aspirant)
    prof_hybrid = {
        "id": p_hybrid_id,
        "email": f"hybrid_{uuid.uuid4().hex[:8]}@test.local",
        "full_name": "Pravin Hybrid (Founder & Specialist)",
        "role": "aspirant",
        "district": "Chennai",
        "state": "Tamil Nadu",
        "profile_data": {
            "personal": {"gender": "Male"},
            "professional": {"education": "M.Tech / Agritech Specialist", "expertise": "IoT & Farm Automation"},
            "business": {
                "business_name": "Aztras AI Tech Solutions",
                "sector": "IT & Services",
                "stage": "Seed"
            },
            "demographics": {"district": "Chennai", "state": "Tamil Nadu", "founder_category": "General"},
            "assistance_need": {
                "assistance_goal": "Equity Investment / Angel / Seed Fund",
                "support_type": "Government Seed Fund (SISFS)",
                "quantum_range": "SMALL (₹5 Lakhs – ₹25 Lakhs)",
                "timeframe": "NEAR_TERM (1 to 3 Months)"
            }
        },
        "is_active": True
    }

    # Profile 3: Aspirant Beta (Bio-Fertilizer Innovation)
    prof_beta = {
        "id": p_beta_id,
        "email": f"beta_{uuid.uuid4().hex[:8]}@test.local",
        "full_name": "Aspirant Beta (BioTech Founder)",
        "role": "aspirant",
        "district": "Coimbatore",
        "state": "Tamil Nadu",
        "profile_data": {
            "personal": {"gender": "Female"},
            "professional": {"education": "Ph.D Biotechnology"},
            "business": {
                "business_name": "Coimbatore Bio-Enzymes",
                "sector": "Healthcare & Biotech",
                "stage": "Pre-Seed / Seed"
            },
            "demographics": {"district": "Coimbatore", "state": "Tamil Nadu", "is_women_led": True, "women_equity_pct": 100},
            "assistance_need": {
                "assistance_goal": "R&D / Prototype / Product Development",
                "support_type": "Innovation Grant (TANSEED / IVP)",
                "quantum_range": "MICRO (< ₹5 Lakhs)",
                "timeframe": "IMMEDIATE (< 30 Days)"
            }
        },
        "is_active": True
    }

    # Admin Profile
    prof_admin = {
        "id": admin_id,
        "email": f"admin_{uuid.uuid4().hex[:8]}@test.local",
        "full_name": "Program Governance Admin",
        "role": "admin",
        "district": "Chennai",
        "state": "Tamil Nadu",
        "profile_data": {},
        "is_active": True
    }

    # Upsert all profiles into DB
    for p in [prof_alpha, prof_hybrid, prof_beta, prof_admin]:
        db.upsert_profile(p)

    return {
        "alpha": prof_alpha,
        "hybrid": prof_hybrid,
        "beta": prof_beta,
        "admin": prof_admin
    }


def test_e2e_multi_role_promotion_and_workflows(setup_e2e_profiles):
    data = setup_e2e_profiles
    alpha_id = data["alpha"]["id"]
    hybrid_id = data["hybrid"]["id"]
    beta_id = data["beta"]["id"]
    admin_id = data["admin"]["id"]

    # ─────────────────────────────────────────────────────────────────
    # 1. BASELINE CHECK: HYBRID IS A PURE ASPIRANT
    # ─────────────────────────────────────────────────────────────────
    initial_guides = list_profiles_by_role("guide")
    initial_smes = list_profiles_by_role("sme")
    initial_guide_count = len(initial_guides)
    initial_sme_count = len(initial_smes)

    active_roles_0 = get_active_roles(hybrid_id)
    assert active_roles_0 == ["aspirant"], f"Expected ['aspirant'], got {active_roles_0}"

    # Aspirant cannot see unreleased schemes
    released_0 = get_released_schemes_for_aspirant(hybrid_id)
    assert len(released_0) == 0, "Aspirant must not see any schemes before guide release"

    # ─────────────────────────────────────────────────────────────────
    # 2. PROMOTION: ADMIN PROMOTES ASPIRANT TO GUIDE
    # ─────────────────────────────────────────────────────────────────
    ok, err = grant_role(user_id=hybrid_id, role="guide", granted_by=admin_id)
    assert ok, f"Failed to grant guide role: {err}"

    # Status must initially be pending_nda
    pending_roles = get_pending_nda_roles(hybrid_id)
    assert "guide" in pending_roles, "Guide role should be in pending_nda status before signature"

    # Guide count must NOT increase yet while NDA is pending
    guides_mid = list_profiles_by_role("guide")
    assert len(guides_mid) == initial_guide_count, "Pending NDA guides should not count as active"

    # Hybrid signs Guide NDA
    ok_nda, err_nda = record_legal_acceptance(
        user_id=hybrid_id,
        user_email=data["hybrid"]["email"],
        doc_type="nda_guide",
        typed_name="Pravin Hybrid",
        typed_phrase="I ACCEPT",
        checkbox_confirmed=True
    )
    assert ok_nda, f"Failed to accept NDA: {err_nda}"

    # Activate role
    ok_act, err_act = activate_role(hybrid_id, "guide")
    assert ok_act, f"Failed to activate guide role: {err_act}"

    # Active roles now contains guide
    active_roles_1 = get_active_roles(hybrid_id)
    assert "guide" in active_roles_1 and "aspirant" in active_roles_1, "Hybrid must hold both aspirant and guide roles"

    # Guide count in Admin portal INCREASES by 1!
    guides_after = list_profiles_by_role("guide")
    assert len(guides_after) == initial_guide_count + 1, "Active Guides metric must increment after activation"
    assert any(g["id"] == hybrid_id for g in guides_after), "Hybrid must be listed in active guides"

    # ─────────────────────────────────────────────────────────────────
    # 3. PROMOTION: ADMIN PROMOTES ASPIRANT TO SME AS WELL
    # ─────────────────────────────────────────────────────────────────
    ok_sme_grant, err_sme_grant = grant_role(user_id=hybrid_id, role="sme", granted_by=admin_id)
    assert ok_sme_grant, f"Failed to grant SME role: {err_sme_grant}"

    # Hybrid signs SME NDA
    ok_sme_nda, _ = record_legal_acceptance(
        user_id=hybrid_id,
        user_email=data["hybrid"]["email"],
        doc_type="nda_sme",
        typed_name="Pravin Hybrid",
        typed_phrase="I ACCEPT",
        checkbox_confirmed=True
    )
    assert ok_sme_nda

    # Activate SME role
    ok_sme_act, _ = activate_role(hybrid_id, "sme")
    assert ok_sme_act

    # Active roles now contains ALL 3: aspirant, guide, sme!
    active_roles_2 = get_active_roles(hybrid_id)
    assert set(active_roles_2) >= {"aspirant", "guide", "sme"}, f"Expected all 3 roles, got {active_roles_2}"

    # Active SMEs metric INCREASES by 1!
    smes_after = list_profiles_by_role("sme")
    assert len(smes_after) == initial_sme_count + 1, "Active SMEs metric must increment after activation"

    # ─────────────────────────────────────────────────────────────────
    # 4. SAFETY GUARD: PREVENT SELF-MENTORING CIRCULARITY
    # ─────────────────────────────────────────────────────────────────
    ok_self_g, err_self_g = assign_guide(aspirant_id=hybrid_id, guide_id=hybrid_id, admin_id=admin_id)
    assert not ok_self_g, "Self-assignment as Guide must be strictly blocked"
    assert "own Guide" in err_self_g

    ok_self_s, err_self_s = assign_sme(aspirant_id=hybrid_id, sme_id=hybrid_id, admin_id=admin_id)
    assert not ok_self_s, "Self-assignment as SME must be strictly blocked"
    assert "own SME" in err_self_s

    # ─────────────────────────────────────────────────────────────────
    # 5. MENTORSHIP ASSIGNMENTS: HYBRID GUIDES OTHERS
    # ─────────────────────────────────────────────────────────────────
    # Admin pairs Hybrid (as Guide) to Aspirant Alpha
    ok_asg_g, err_asg_g = assign_guide(aspirant_id=alpha_id, guide_id=hybrid_id, admin_id=admin_id, notes="Assigned for food tech scale-up")
    assert ok_asg_g, f"Failed to assign guide: {err_asg_g}"

    # Admin pairs Hybrid (as SME) to Aspirant Beta
    ok_asg_s, err_asg_s = assign_sme(aspirant_id=beta_id, sme_id=hybrid_id, admin_id=admin_id, notes="Assigned for IoT biotech sensor integration")
    assert ok_asg_s, f"Failed to assign SME: {err_asg_s}"

    # Verify relationships from Aspirant viewpoint
    alpha_mentors = get_aspirant_mentors(alpha_id)
    assert alpha_mentors.get("guide", {}).get("id") == hybrid_id, "Alpha's Guide must be Hybrid"

    beta_mentors = get_aspirant_mentors(beta_id)
    assert any(s["id"] == hybrid_id for s in beta_mentors.get("smes", [])), "Beta's SME must be Hybrid"

    # ─────────────────────────────────────────────────────────────────
    # 6. DATA PRIVACY & WORKSPACE ROSTER ISOLATION
    # ─────────────────────────────────────────────────────────────────
    # In Guide Workspace: Hybrid only sees assigned guide mentees (Alpha), NOT Beta
    guide_roster = get_assigned_aspirants_for_guide(hybrid_id)
    guide_roster_ids = [a["id"] for a in guide_roster]
    assert alpha_id in guide_roster_ids, "Hybrid must see assigned mentee Alpha in Guide roster"
    assert beta_id not in guide_roster_ids, "Hybrid MUST NOT see Beta in Guide roster (privacy violation)"
    assert hybrid_id not in guide_roster_ids, "Hybrid's own venture must not appear in mentee list"

    # In SME Workspace: Hybrid only sees assigned SME cases (Beta), NOT Alpha
    sme_roster = get_assigned_aspirants_for_sme(hybrid_id)
    sme_roster_ids = [a["id"] for a in sme_roster]
    assert beta_id in sme_roster_ids, "Hybrid must see assigned case Beta in SME roster"
    assert alpha_id not in sme_roster_ids, "Hybrid MUST NOT see Alpha in SME roster"

    # ─────────────────────────────────────────────────────────────────
    # 7. SCHEME EVALUATION & FORMAL RELEASE WORKFLOW
    # ─────────────────────────────────────────────────────────────────
    # Hybrid (as Guide) reviews AI suggested scheme matches for Alpha
    alpha_matches = match_schemes_for_aspirant(alpha_id)
    assert len(alpha_matches) > 0, "AI matching engine must score schemes for Alpha"

    # Pick top eligible scheme
    chosen_scheme = alpha_matches[0]
    scheme_id = chosen_scheme["id"]

    # Guide releases scheme to Alpha with mentoring note
    ok_rel, err_rel = release_scheme_to_aspirant(
        guide_id=hybrid_id,
        aspirant_id=alpha_id,
        scheme_id=scheme_id,
        guide_recommendation="Verified eligible for 35% Capex subsidy. Complete DPR before branch audit.",
        guide_note="Follow up with Madurai DIC officer next Tuesday."
    )
    assert ok_rel, f"Release failed: {err_rel}"

    # Alpha's dashboard now unlocks the released scheme!
    alpha_released = get_released_schemes_for_aspirant(alpha_id)
    assert len(alpha_released) == 1, "Alpha must now have exactly 1 released scheme"
    assert str(alpha_released[0]["id"]) == str(scheme_id)
    assert "35% Capex subsidy" in alpha_released[0]["guide_recommendation"]

    # Beta still has 0 released schemes (complete isolation)
    beta_released = get_released_schemes_for_aspirant(beta_id)
    assert len(beta_released) == 0, "Beta must not see schemes released to Alpha"

    # ─────────────────────────────────────────────────────────────────
    # 8. BIDIRECTIONAL MESSAGING & CONSULTATION WORKFLOW
    # ─────────────────────────────────────────────────────────────────
    # A. Aspirant Alpha -> Hybrid (Guide)
    ticket_alpha, err_t1 = create_request(
        aspirant_id=alpha_id,
        subject="Bank Collateral Advice for CGTMSE",
        message="Our bank branch manager requested 100% collateral. Does CGTMSE require this?",
        priority="HIGH",
        category="SCHEMES",
        target_role="guide",
        target_mentor_id=hybrid_id
    )
    assert ticket_alpha is not None, f"Failed to create request: {err_t1}"
    t_alpha_id = ticket_alpha["id"]

    # Hybrid in Guide workspace retrieves ticket from Alpha
    guide_tickets = list_guide_requests(hybrid_id)
    assert any(t["id"] == t_alpha_id for t in guide_tickets), "Hybrid must see ticket from Alpha in Guide workspace"

    # Hybrid responds as Guide
    ok_resp1, err_r1 = guide_respond_request(
        request_id=t_alpha_id,
        guide_id=hybrid_id,
        new_status="RESOLVED",
        response="No. CGTMSE is explicitly collateral-free up to Rs 5 Crores under RBI mandate. Share our platform dossier with the branch manager."
    )
    assert ok_resp1, f"Failed to respond as guide: {err_r1}"

    # Alpha receives response in their portal
    alpha_inbox = list_requests(alpha_id)
    resolved_t1 = next((t for t in alpha_inbox if t["id"] == t_alpha_id), None)
    assert resolved_t1 is not None
    assert resolved_t1["status"] == "RESOLVED"
    assert "collateral-free" in resolved_t1["guide_response"]

    # B. Aspirant Beta -> Hybrid (SME)
    ticket_beta, err_t2 = create_request(
        aspirant_id=beta_id,
        subject="IoT Sensor Calibration Parameters for Bio-reactor",
        message="Which NABL calibration protocol should we follow for the dissolved oxygen probes?",
        priority="URGENT",
        category="TECHNICAL",
        target_role="sme",
        target_mentor_id=hybrid_id
    )
    assert ticket_beta is not None, f"Failed to create request: {err_t2}"
    t_beta_id = ticket_beta["id"]

    # Hybrid in SME workspace retrieves ticket from Beta
    sme_tickets = list_sme_requests(hybrid_id)
    assert any(t["id"] == t_beta_id for t in sme_tickets), "Hybrid must see technical ticket from Beta in SME workspace"

    # Hybrid responds as SME
    ok_resp2, err_r2 = sme_respond_request(
        request_id=t_beta_id,
        sme_id=hybrid_id,
        new_status="RESOLVED",
        response="Follow ISO/IEC 17025 standard calibration with 2-point zero and saturation buffer at 25C."
    )
    assert ok_resp2, f"Failed to respond as SME: {err_r2}"

    # Beta receives technical response in their portal
    beta_inbox = list_requests(beta_id)
    resolved_t2 = next((t for t in beta_inbox if t["id"] == t_beta_id), None)
    assert resolved_t2 is not None
    assert resolved_t2["status"] == "RESOLVED"
    assert "ISO/IEC 17025" in resolved_t2["sme_response"]

    print("\n" + "="*80)
    print(">>> ALL 8 E2E WORKFLOW PERMUTATIONS & COMBINATIONS PASSED PERFECTLY! <<<")
    print("="*80)
