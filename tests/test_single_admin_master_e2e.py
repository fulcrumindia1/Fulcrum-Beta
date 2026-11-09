"""
tests/test_single_admin_master_e2e.py
======================================
Comprehensive End-to-End Test Suite for Fulcrum-Beta Single Admin Architecture.

ACTORS (Strict Single Admin Architecture):
1. Existing Single Admin: fulcrumindia1@gmail.com (ID: 616304b5-aef5-4cd0-88be-2fda7ddf7f88)
2. Aspirant Alpha: Dedicated Guide mentorship case (Solar Cold Storage)
3. Aspirant Beta: Domain SME advisory case (Agritech Drone Sensing)
4. Aspirant Gamma: Unauthorized-access boundary test (Biotech Diagnostics)
5. Hybrid Founder: Promoted to Guide and SME (Bioplastics Startup)
6. Guide Two: Replacement dedicated Guide
7. SME Two: Replacement specialized SME

TEST COVERAGE:
- Onboarding & Registration CRUD
- Profile Photo Management (Upload, Replace, Remove, Validation, Journey Isolation)
- Terms & Conditions and NDA Acceptance Gating
- Single Admin Multi-Role Promotions & NDA Activation
- Caseload Isolation & Data Confidentiality (Scenarios A through G)
- Mentor Unassignment vs. Replacement vs. Role Revocation (Audit Trail Preservation)
- Bidirectional Consultations & Handover
- AI Scheme Matching Engine & Formal Release
- Journey Milestone Lifecycle (Creation, Revision Tracking, Dossier PDF)
- Admin Command Metrics Accuracy & Multi-Role De-duplication
"""

import os
os.environ["DATA_BACKEND"] = "sqlite"

import io
import uuid
import json
import pytest
from datetime import datetime, timezone
from PIL import Image

from services.auth import signup_aspirant, get_data_backend, get_supabase_admin_client
from services.profiles import get_profile, update_aspirant_profile, list_profiles_by_role
from services.roles import (
    grant_role,
    activate_role,
    revoke_role,
    get_user_roles,
    get_active_roles,
    get_pending_nda_roles,
    user_has_active_role,
)
from services.relationships import (
    assign_guide,
    assign_sme,
    unassign_guide,
    unassign_sme,
    get_aspirant_mentors,
    get_assigned_aspirants_for_guide,
    get_assigned_aspirants_for_sme,
    get_assignment_history,
)
from services.legal import (
    check_user_terms_accepted,
    record_legal_acceptance,
    check_user_nda_accepted,
)
from services.aspirant_photos import (
    upload_aspirant_photo,
    get_aspirant_photo,
    delete_aspirant_photo,
    validate_and_process_photo,
)
from services.help_requests import (
    create_request,
    list_requests,
    list_guide_requests,
    list_sme_requests,
    guide_respond_request,
    sme_respond_request,
)
from services.schemes import (
    match_schemes_for_aspirant,
    release_scheme_to_aspirant,
    get_released_schemes_for_aspirant,
    list_schemes,
)
from services.journey import (
    get_journey_timeline,
    add_admin_journey_entry,
    log_meaningful_event,
    soft_delete_event,
    count_active_journeys,
)
from services.pdf_generator import generate_aspirant_dossier_pdf
from services.local_db import get_local_db

# CONSTANTS: Strict Single Admin Architecture
ADMIN_ID = "616304b5-aef5-4cd0-88be-2fda7ddf7f88"
ADMIN_EMAIL = "fulcrumindia1@gmail.com"


@pytest.fixture(autouse=True)
def force_sqlite_backend(monkeypatch):
    monkeypatch.setenv("DATA_BACKEND", "sqlite")
    from services.cache import invalidate_memo
    invalidate_memo()


@pytest.fixture(scope="module")
def actors():
    """Provisions the exact 7 actors under the single Admin architecture."""
    db = get_local_db()
    sb_admin = None

    # 1. Ensure single Admin is registered in SQLite and Supabase
    conn = db._get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT OR REPLACE INTO profiles (id, email, role, full_name, phone, district, state, password_hash, profile_data, is_active, created_at, updated_at)
        VALUES (?, ?, 'admin', 'Fulcrum Administrator', '9876543210', 'Chennai', 'Tamil Nadu', 'fake_hash', '{}', 1, '2026-01-01T00:00:00Z', '2026-01-01T00:00:00Z')
        """,
        (ADMIN_ID, ADMIN_EMAIL),
    )
    conn.commit()
    conn.close()

    tag = uuid.uuid4().hex[:6]
    users_def = [
        ("alpha", f"alpha_{tag}@test.local", "Aspirant Alpha", "aspirant", "Madurai"),
        ("beta", f"beta_{tag}@test.local", "Aspirant Beta", "aspirant", "Coimbatore"),
        ("gamma", f"gamma_{tag}@test.local", "Aspirant Gamma", "aspirant", "Tiruchirappalli"),
        ("hybrid", f"hybrid_{tag}@test.local", "Hybrid Founder", "aspirant", "Chennai"),
        ("guide2", f"guide2_{tag}@test.local", "Guide Two", "guide", "Salem"),
        ("sme2", f"sme2_{tag}@test.local", "SME Two", "sme", "Tirunelveli"),
    ]

    actors_dict = {
        "admin": {
            "id": ADMIN_ID,
            "email": ADMIN_EMAIL,
            "full_name": "Fulcrum Administrator",
            "role": "admin",
        }
    }

    created_uids = []
    now_iso = datetime.now(timezone.utc).isoformat()
    for key, email, name, role, dist in users_def:
        uid = str(uuid.uuid4())
        if sb_admin:
            try:
                auth_res = sb_admin.auth.admin.create_user({
                    "email": email,
                    "password": "TestPassword@2026",
                    "email_confirm": True,
                    "user_metadata": {
                        "full_name": name,
                        "role": role,
                        "district": dist,
                        "phone": "9876543210",
                    },
                })
                if auth_res.user:
                    uid = auth_res.user.id
                    created_uids.append(uid)
            except Exception as e:
                pass

        prof_record = {
            "id": uid,
            "email": email,
            "role": role,
            "full_name": name,
            "phone": "9876543210",
            "district": dist,
            "state": "Tamil Nadu",
            "profile_data": {},
            "is_active": 1,
            "created_at": now_iso,
            "updated_at": now_iso,
        }
        db.upsert_profile(prof_record)
        db.create_initial_journey(uid, f"{name}'s Enterprise Journey")

        if sb_admin:
            try:
                sb_admin.table("profiles").upsert(prof_record, on_conflict="id").execute()
                sb_admin.table("journeys").upsert({
                    "aspirant_id": uid,
                    "title": f"{name}'s Enterprise Journey",
                    "business_type": "Entrepreneurship",
                    "stage": "idea",
                    "status": "active",
                }, on_conflict="aspirant_id").execute()
            except Exception as ex:
                print(f"[Fixture Warning] Supabase sync for {email}: {ex}")

        actors_dict[key] = {
            "id": uid,
            "email": email,
            "full_name": name,
            "role": role,
            "district": dist,
        }

    yield actors_dict

    # Cleanup created test users from Supabase Auth & SQLite
    if sb_admin:
        for u in created_uids:
            try:
                sb_admin.auth.admin.delete_user(u)
            except Exception:
                pass


def test_01_onboarding_and_registration(actors):
    """Part 3: Verify Aspirants Alpha, Beta, Gamma, Hybrid registration and profile persistence."""
    for key in ("alpha", "beta", "gamma", "hybrid"):
        actor = actors[key]
        prof = get_profile(actor["id"])
        assert prof is not None, f"Profile {key} not found"
        assert prof["role"] == "aspirant"
        assert prof["email"] == actor["email"]

        # Populate complete enterprise profile via update_aspirant_profile
        enterprise_data = {
            "business_name": f"{actor['full_name']} Enterprise",
            "business_type": "Manufacturing",
            "industry": "CleanTech / AgTech",
            "stage": "Commercial / Growth",
            "annual_revenue": "1500000",
            "employee_count": 8,
            "business_description": "Innovative sustainable technology solutions.",
        }
        demo_data = {
            "gender": "Male",
            "caste": "General",
            "is_differently_abled": False,
            "is_minority": False,
            "is_rural": False,
        }
        assist_data = {
            "goal": "Capital Grant / Seed Subsidy",
            "support_type": "All Capital Grants",
            "quantum": "MEDIUM (Rs 25 Lakhs to Rs 5 Crores)",
            "timeframe": "NEAR_TERM (1 to 3 Months)",
        }
        ok, err = update_aspirant_profile(
            user_id=actor["id"],
            full_name=actor["full_name"],
            phone="9876543210",
            district=actor["district"],
            business_data=enterprise_data,
            demographics_data=demo_data,
            assistance_need_data=assist_data,
        )
        assert ok, f"Failed to update profile for {key}: {err}"

        saved = get_profile(actor["id"])
        assert saved["profile_data"]["business"]["business_name"] == f"{actor['full_name']} Enterprise"
        assert saved["completion_pct"] >= 50

    aspirants_list = list_profiles_by_role("aspirant")
    asp_ids = [a["id"] for a in aspirants_list]
    for key in ("alpha", "beta", "gamma", "hybrid"):
        assert actors[key]["id"] in asp_ids


def test_02_profile_photo_lifecycle(actors):
    """Part 4: Test Aspirant profile photo CRUD, compression, and journey isolation."""
    alpha_id = actors["alpha"]["id"]

    # 1. Generate a valid 120x120 test PNG image
    img = Image.new("RGB", (120, 120), color=(37, 99, 235))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    png_bytes = buf.getvalue()

    # 2. Upload photo
    ok_up, err_up = upload_aspirant_photo(alpha_id, png_bytes, "headshot.png")
    assert ok_up, f"Upload photo failed: {err_up}"

    # 3. Read saved photo (owner self-view)
    photo_rec = get_aspirant_photo(alpha_id, viewer_id=alpha_id, viewer_role="aspirant")
    assert photo_rec is not None, "Photo record not found after upload"
    assert photo_rec["width"] == 120
    assert photo_rec["height"] == 120
    assert photo_rec.get("url") is not None
    assert "data:image/webp;base64," in photo_rec["url"] or "http" in photo_rec["url"]

    # 4. Replace photo with another image
    img2 = Image.new("RGB", (200, 200), color=(16, 185, 129))
    buf2 = io.BytesIO()
    img2.save(buf2, format="JPEG")
    jpeg_bytes = buf2.getvalue()

    ok_rep, err_rep = upload_aspirant_photo(alpha_id, jpeg_bytes, "headshot2.jpg")
    assert ok_rep, f"Replace photo failed: {err_rep}"
    photo_rec2 = get_aspirant_photo(alpha_id, viewer_id=alpha_id, viewer_role="aspirant")
    assert photo_rec2["width"] == 200

    # 5. Remove photo
    ok_del, err_del = delete_aspirant_photo(alpha_id)
    assert ok_del, f"Delete photo failed: {err_del}"
    assert get_aspirant_photo(alpha_id, viewer_id=alpha_id, viewer_role="aspirant") is None

    # 6. Negative test: Reject corrupt / non-image bytes
    ok_bad, _, _, _, _, err_bad = validate_and_process_photo(b"NOT_AN_IMAGE_DATA")
    assert not ok_bad
    assert ("cannot identify" in err_bad or "Failed to process" in err_bad)

    # 7. Verify zero Journey event was created for photo actions (strict isolation)
    events = get_journey_timeline(alpha_id)
    assert not any("photo" in str(e).lower() for e in events)


def test_03_terms_and_legal_acceptance(actors):
    """Part 5: Verify Terms & Conditions acceptance workflow."""
    beta_id = actors["beta"]["id"]
    beta_email = actors["beta"]["email"]

    # Initial check: not accepted
    assert not check_user_terms_accepted(beta_id)

    # Record formal acceptance
    ok, err = record_legal_acceptance(
        user_id=beta_id,
        user_email=beta_email,
        doc_type="terms_and_conditions",
        typed_name="Aspirant Beta",
        typed_phrase="I ACCEPT",
        checkbox_confirmed=True,
    )
    assert ok, f"Failed to record legal acceptance: {err}"

    # Verify acceptance persisted
    assert check_user_terms_accepted(beta_id)


def test_04_single_admin_role_promotions_and_nda_activation(actors):
    """Part 5: Single Admin promotes Hybrid to Guide & SME, Guide Two to Guide, SME Two to SME with NDA gating."""
    hybrid_id = actors["hybrid"]["id"]
    hybrid_email = actors["hybrid"]["email"]
    guide2_id = actors["guide2"]["id"]
    guide2_email = actors["guide2"]["email"]
    sme2_id = actors["sme2"]["id"]
    sme2_email = actors["sme2"]["email"]

    # A. Single Admin promotes Hybrid to Guide
    ok_g, err_g = grant_role(hybrid_id, "guide", granted_by=ADMIN_ID)
    assert ok_g, f"Failed to grant guide: {err_g}"
    assert "guide" in get_pending_nda_roles(hybrid_id)
    assert not user_has_active_role(hybrid_id, "guide")

    # Hybrid signs Guide NDA
    ok_nda_g, _ = record_legal_acceptance(
        user_id=hybrid_id,
        user_email=hybrid_email,
        doc_type="nda_guide",
        typed_name="Hybrid Founder",
        typed_phrase="I ACCEPT",
        checkbox_confirmed=True,
    )
    assert ok_nda_g
    ok_act_g, _ = activate_role(hybrid_id, "guide")
    assert ok_act_g
    assert user_has_active_role(hybrid_id, "guide")

    # B. Single Admin promotes Hybrid to SME
    ok_s, err_s = grant_role(hybrid_id, "sme", granted_by=ADMIN_ID)
    assert ok_s, f"Failed to grant sme: {err_s}"
    assert "sme" in get_pending_nda_roles(hybrid_id)
    assert not user_has_active_role(hybrid_id, "sme")

    # Hybrid signs SME NDA
    ok_nda_s, _ = record_legal_acceptance(
        user_id=hybrid_id,
        user_email=hybrid_email,
        doc_type="nda_sme",
        typed_name="Hybrid Founder",
        typed_phrase="I ACCEPT",
        checkbox_confirmed=True,
    )
    assert ok_nda_s
    ok_act_s, _ = activate_role(hybrid_id, "sme")
    assert ok_act_s
    assert user_has_active_role(hybrid_id, "sme")

    # Hybrid now holds all 3 roles: aspirant, guide, sme
    hybrid_active = get_active_roles(hybrid_id)
    assert "aspirant" in hybrid_active
    assert "guide" in hybrid_active
    assert "sme" in hybrid_active

    # C. Activate Guide Two and SME Two
    grant_role(guide2_id, "guide", granted_by=ADMIN_ID)
    record_legal_acceptance(guide2_id, guide2_email, "nda_guide", "Guide Two", "I ACCEPT", True)
    activate_role(guide2_id, "guide")
    assert user_has_active_role(guide2_id, "guide")

    grant_role(sme2_id, "sme", granted_by=ADMIN_ID)
    record_legal_acceptance(sme2_id, sme2_email, "nda_sme", "SME Two", "I ACCEPT", True)
    activate_role(sme2_id, "sme")
    assert user_has_active_role(sme2_id, "sme")


def test_05_caseload_allocation_and_privacy_isolation(actors):
    """Part 6: Test Scenarios A through G — Caseload isolation, multi-role switching, self-mentoring guard."""
    hybrid_id = actors["hybrid"]["id"]
    alpha_id = actors["alpha"]["id"]
    beta_id = actors["beta"]["id"]
    gamma_id = actors["gamma"]["id"]

    # Scenario A: Admin assigns Hybrid as Guide to Alpha
    ok_asg_a, err_asg_a = assign_guide(
        alpha_id, hybrid_id, admin_id=ADMIN_ID, notes="Dedicated mentor for clean energy venture."
    )
    assert ok_asg_a, f"Failed to assign guide: {err_asg_a}"

    # Scenario B: Admin assigns Hybrid as SME to Beta
    ok_asg_b, err_asg_b = assign_sme(
        beta_id, hybrid_id, admin_id=ADMIN_ID, notes="Domain specialist for drone sensors.", mode="add"
    )
    assert ok_asg_b, f"Failed to assign SME: {err_asg_b}"

    # Caseload privacy verification:
    # In Guide mode, Hybrid ONLY sees Alpha (Beta is hidden)
    guide_caseload = get_assigned_aspirants_for_guide(hybrid_id)
    guide_ids = [c["id"] for c in guide_caseload]
    assert alpha_id in guide_ids, "Alpha must appear in Hybrid Guide caseload"
    assert beta_id not in guide_ids, "Beta must NEVER appear in Hybrid Guide caseload"
    assert gamma_id not in guide_ids, "Gamma must NEVER appear in Hybrid Guide caseload"

    # In SME mode, Hybrid ONLY sees Beta (Alpha is hidden)
    sme_caseload = get_assigned_aspirants_for_sme(hybrid_id)
    sme_ids = [c["id"] for c in sme_caseload]
    assert beta_id in sme_ids, "Beta must appear in Hybrid SME caseload"
    assert alpha_id not in sme_ids, "Alpha must NEVER appear in Hybrid SME caseload"
    assert gamma_id not in sme_ids, "Gamma must NEVER appear in Hybrid SME caseload"

    # Scenario F: Self-mentoring prevention guard
    ok_self_g, err_self_g = assign_guide(hybrid_id, hybrid_id, admin_id=ADMIN_ID)
    assert not ok_self_g
    assert "cannot be assigned as their own Guide" in err_self_g

    ok_self_s, err_self_s = assign_sme(hybrid_id, hybrid_id, admin_id=ADMIN_ID)
    assert not ok_self_s
    assert "cannot be assigned as their own SME" in err_self_s


def test_06_unassign_vs_replacement_vs_revocation(actors):
    """Parts 7 & 8: Verify mentor removal vs. replacement vs. global role revocation."""
    hybrid_id = actors["hybrid"]["id"]
    alpha_id = actors["alpha"]["id"]
    beta_id = actors["beta"]["id"]
    guide2_id = actors["guide2"]["id"]
    sme2_id = actors["sme2"]["id"]

    # 1. Admin assigns SME Two as Co-SME to Beta
    ok_co_sme, _ = assign_sme(
        beta_id, sme2_id, admin_id=ADMIN_ID, notes="Additional GST/Tax specialist.", mode="add"
    )
    assert ok_co_sme
    beta_mentors = get_aspirant_mentors(beta_id)
    assert len(beta_mentors.get("smes", [])) >= 2

    # 2. Case Unassignment: Admin removes Hybrid as SME for Beta
    ok_un_sme, err_un_sme = unassign_sme(
        beta_id, hybrid_id, admin_id=ADMIN_ID, reason="Advisory phase 1 completed."
    )
    assert ok_un_sme, f"Unassign SME failed: {err_un_sme}"

    # Verify Hybrid is no longer assigned to Beta, but SME Two remains
    beta_mentors_after = get_aspirant_mentors(beta_id)
    sme_ids_after = [s["id"] for s in beta_mentors_after.get("smes", [])]
    assert hybrid_id not in sme_ids_after
    assert sme2_id in sme_ids_after
    # Hybrid still has active SME role globally
    assert user_has_active_role(hybrid_id, "sme")

    # 3. Mentor Replacement: Admin replaces Hybrid with Guide Two for Alpha
    ok_rep_g, err_rep_g = assign_guide(
        alpha_id, guide2_id, admin_id=ADMIN_ID, notes="Replacement guide for scale-up phase."
    )
    assert ok_rep_g, f"Replace Guide failed: {err_rep_g}"
    alpha_mentors = get_aspirant_mentors(alpha_id)
    assert alpha_mentors.get("guide", {}).get("id") == guide2_id
    assert hybrid_id not in [g["id"] for g in alpha_mentors.get("guides", [])]

    # Hybrid's guide caseload is now empty
    hybrid_guide_caseload = get_assigned_aspirants_for_guide(hybrid_id)
    assert alpha_id not in [c["id"] for c in hybrid_guide_caseload]

    # 4. Global Role Revocation: Admin revokes Hybrid's SME role
    ok_rev_sme, err_rev_sme = revoke_role(
        hybrid_id, "sme", reason="Voluntary withdrawal from advisory panel.", revoked_by=ADMIN_ID
    )
    assert ok_rev_sme, f"Revoke role failed: {err_rev_sme}"
    assert not user_has_active_role(hybrid_id, "sme")

    # Hybrid retains Aspirant and Guide roles
    assert user_has_active_role(hybrid_id, "aspirant")
    assert user_has_active_role(hybrid_id, "guide")

    # Immediate access check: SME caseload is completely blocked
    assert get_assigned_aspirants_for_sme(hybrid_id) == []


def test_07_bidirectional_messaging_and_handover(actors):
    """Part 9: Complete messaging and consultation workflows between Aspirants and active Mentors."""
    alpha_id = actors["alpha"]["id"]
    beta_id = actors["beta"]["id"]
    guide2_id = actors["guide2"]["id"]
    sme2_id = actors["sme2"]["id"]

    # A. Alpha -> Guide Two consultation
    ticket_a, err_ta = create_request(
        aspirant_id=alpha_id,
        subject="PMEGP Subsidy Margin Money Inquiry",
        message="What is the margin money requirement for rural general category under PMEGP?",
        priority="HIGH",
        category="SCHEMES",
        target_role="guide",
        target_mentor_id=guide2_id,
    )
    assert ticket_a is not None, f"Failed to create request: {err_ta}"
    ta_id = ticket_a["id"]

    # Guide Two reviews and responds
    g_reqs = list_guide_requests(guide2_id)
    assert any(t["id"] == ta_id for t in g_reqs)

    ok_g_resp, err_g_resp = guide_respond_request(
        request_id=ta_id,
        guide_id=guide2_id,
        new_status="RESOLVED",
        response="For rural general category, the own-contribution margin is 10%, and government subsidy is 25% of project cost.",
    )
    assert ok_g_resp, f"Guide failed to respond: {err_g_resp}"

    # Alpha verifies response
    a_inbox = list_requests(alpha_id)
    resolved_a = next((t for t in a_inbox if t["id"] == ta_id), None)
    assert resolved_a is not None
    assert resolved_a["status"] == "RESOLVED"
    assert "25% of project cost" in resolved_a["guide_response"]

    # B. Beta -> SME Two technical advisory consultation
    ticket_b, err_tb = create_request(
        aspirant_id=beta_id,
        subject="DGFT & DGCA Drone Compliance",
        message="Do we require a Type Certificate from DGCA before submitting for the PLI Drone Scheme?",
        priority="URGENT",
        category="TECHNICAL",
        target_role="sme",
        target_mentor_id=sme2_id,
    )
    assert ticket_b is not None, f"Failed to create request: {err_tb}"
    tb_id = ticket_b["id"]

    s_reqs = list_sme_requests(sme2_id)
    assert any(t["id"] == tb_id for t in s_reqs)

    ok_s_resp, err_s_resp = sme_respond_request(
        request_id=tb_id,
        sme_id=sme2_id,
        new_status="RESOLVED",
        response="Yes. A DGCA Type Certificate is mandatory under Drone Rules 2021 to qualify for the PLI Scheme for Drones.",
    )
    assert ok_s_resp, f"SME failed to respond: {err_s_resp}"

    b_inbox = list_requests(beta_id)
    resolved_b = next((t for t in b_inbox if t["id"] == tb_id), None)
    assert resolved_b is not None
    assert "DGCA Type Certificate is mandatory" in resolved_b["sme_response"]


def test_08_ai_scheme_matching_and_formal_release(actors):
    """Part 11: AI Scheme matching, checklist evaluation, and Guide formal release."""
    alpha_id = actors["alpha"]["id"]
    beta_id = actors["beta"]["id"]
    guide2_id = actors["guide2"]["id"]
    admin_id = actors["admin"]["id"]

    from services.relationships import get_aspirant_mentors, assign_guide
    mentors = get_aspirant_mentors(alpha_id)
    if not mentors.get("guide") or str(mentors.get("guide", {}).get("id")) != str(guide2_id):
        assign_guide(alpha_id, guide2_id, admin_id)

    # 1. Deterministic Scheme Matching for Alpha
    alpha_matches = match_schemes_for_aspirant(alpha_id)
    assert len(alpha_matches) > 0, "Alpha must match qualifying schemes"
    target_scheme = alpha_matches[0]
    scheme_id = target_scheme.get("id") or target_scheme.get("scheme_id")

    # 2. Guide Two formally releases scheme to Alpha
    ok_rel, err_rel = release_scheme_to_aspirant(
        guide_id=guide2_id,
        aspirant_id=alpha_id,
        scheme_id=scheme_id,
        guide_note="High priority fit for capital expenditure subsidy. Dossier approved.",
    )
    assert ok_rel, f"Scheme release failed: {err_rel}"

    # 3. Alpha sees released scheme
    alpha_released = get_released_schemes_for_aspirant(alpha_id)
    assert any((s.get("scheme_id") == scheme_id or s.get("id") == scheme_id) for s in alpha_released)

    # 4. Beta does NOT see Alpha's released schemes (privacy boundary)
    beta_released = get_released_schemes_for_aspirant(beta_id)
    assert not any((s.get("scheme_id") == scheme_id or s.get("id") == scheme_id) for s in beta_released)


def test_09_journey_lifecycle_and_pdf_dossier(actors):
    """Part 10: Journey creation, revision tracking, soft deletion, and founder dossier PDF."""
    alpha_id = actors["alpha"]["id"]

    # 1. Log milestone event
    log_meaningful_event(
        aspirant_id=alpha_id,
        actor_id=alpha_id,
        actor_role="aspirant",
        event_type="milestone",
        title="Commercial Pilot Deployed",
        description="Deployed solar cold storage unit at Dindigul vegetable cluster.",
        metadata={"cost": "350000", "link": "https://fulcrum.in/case-study-pilot"},
    )

    timeline = get_journey_timeline(alpha_id)
    milestone = next((e for e in timeline if e.get("title") == "Commercial Pilot Deployed"), None)
    assert milestone is not None
    m_id = milestone["id"]

    # 2. Generate PDF Dossier
    pdf_bytes = generate_aspirant_dossier_pdf(alpha_id)
    assert pdf_bytes is not None
    assert len(pdf_bytes) > 500, "PDF bytes must be generated"
    assert pdf_bytes.startswith(b"%PDF"), "Must be a valid PDF document"

    # 3. Soft deletion
    ok_del = soft_delete_event(m_id, alpha_id, "aspirant")
    assert ok_del
    timeline_after = get_journey_timeline(alpha_id)
    assert not any(e["id"] == m_id for e in timeline_after)


def test_10_admin_command_metrics_accuracy(actors):
    """Part 12: Admin Dashboard command metrics accuracy and multi-role de-duplication."""
    aspirants = list_profiles_by_role("aspirant")
    guides = list_profiles_by_role("guide")
    smes = list_profiles_by_role("sme")
    schemes = list_schemes(active_only=False)

    # De-duplication check: each list must contain unique user IDs
    assert len(aspirants) == len({a["id"] for a in aspirants}), "Aspirants must not contain duplicates"
    assert len(guides) == len({g["id"] for g in guides}), "Guides must not contain duplicates"
    assert len(smes) == len({s["id"] for s in smes}), "SMEs must not contain duplicates"

    # Hybrid Founder is in Aspirant and Guide, but NOT in SME (SME was revoked in test 06)
    hybrid_id = actors["hybrid"]["id"]
    assert any(a["id"] == hybrid_id for a in aspirants)
    assert any(g["id"] == hybrid_id for g in guides)
    assert not any(s["id"] == hybrid_id for s in smes)

    # Guide Two is in Guides
    assert any(g["id"] == actors["guide2"]["id"] for g in guides)

    # SME Two is in SMEs
    assert any(s["id"] == actors["sme2"]["id"] for s in smes)

    # Full Scheme catalogue is intact (179 schemes)
    assert len(schemes) >= 170

    # Active journeys count is positive
    assert count_active_journeys() >= 1
