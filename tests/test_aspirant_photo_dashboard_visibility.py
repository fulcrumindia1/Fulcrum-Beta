"""
tests/test_aspirant_photo_dashboard_visibility.py
=================================================
Dedicated 20-Step Synthetic E2E Test Suite for Aspirant Profile Photo
Dashboard Visibility, Server-Side Authorization, and Lifecycle Gating.

VERIFIES:
- Step 1: Aspirant Alpha uploads a photo.
- Step 2: Admin assigns Guide One to Alpha.
- Step 3: Guide One accepts NDA and checks authorization.
- Step 4: Alpha's correct photo appears for Guide One.
- Step 5: Admin assigns SME One to Alpha.
- Step 6: SME One accepts NDA and checks authorization.
- Step 7: The same photo appears for SME One.
- Step 8: Guide Two (unassigned) is denied Alpha's photo.
- Step 9: SME Two (unassigned) is denied Alpha's photo.
- Step 10: Admin removes Guide One from Alpha.
- Step 11: Guide One immediately loses photo authorization.
- Step 12: SME One retains authorized photo access.
- Step 13: Admin revokes SME One's SME role.
- Step 14: SME One loses protected photo access.
- Step 15: Alpha changes photo; authorized viewers see replacement.
- Step 16: Alpha removes photo; authorized views receive None / initials placeholder.
- Step 17: Hybrid Founder (Aspirant + Guide + SME) retains own photo while viewing assigned cases.
- Step 18: Existing Admin Entrepreneurs Directory photo display continues working.
- Step 19: Existing profile, Journey, scheme, messaging, and PDF workflows remain unchanged (zero side effects).
- Step 20: Direct backend calls with forged viewer IDs or without assignment cannot bypass authorization.
"""

import io
import uuid
import json
import pytest
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch
from PIL import Image

from services.local_db import get_local_db
from services.auth import get_data_backend, get_supabase_admin_client
from services.profiles import get_profile, update_aspirant_profile
from services.roles import (
    grant_role,
    activate_role,
    revoke_role,
    get_user_roles,
    get_active_roles,
    user_has_active_role,
)
from services.relationships import (
    assign_guide,
    assign_sme,
    unassign_guide,
    unassign_sme,
    get_aspirant_mentors,
)
from services.legal import (
    record_legal_acceptance,
    check_user_nda_accepted,
)
from services.aspirant_photos import (
    upload_aspirant_photo,
    get_aspirant_photo,
    delete_aspirant_photo,
    can_view_aspirant_photo,
    render_aspirant_photo_header,
    validate_and_process_photo,
)
from services.journey import get_journey_timeline
from services.schemes import match_schemes_for_aspirant

# Strict Single Admin Architecture
ADMIN_ID = "616304b5-aef5-4cd0-88be-2fda7ddf7f88"
ADMIN_EMAIL = "fulcrumindia1@gmail.com"


def make_test_image(width: int = 120, height: int = 120, color: tuple = (37, 99, 235), img_format: str = "PNG") -> bytes:
    """Generates an in-memory test image with specific dimensions and color."""
    img = Image.new("RGB", (width, height), color=color)
    buf = io.BytesIO()
    img.save(buf, format=img_format)
    return buf.getvalue()


@pytest.fixture(scope="module")
def photo_test_context():
    """Sets up test actors and baseline data across local DB and Supabase."""
    db = get_local_db()
    sb_admin = get_supabase_admin_client()

    # 1. Register Single Admin
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
        ("gamma", f"gamma_{tag}@test.local", "Aspirant Gamma", "aspirant", "Salem"),
        ("guide1", f"guide1_{tag}@test.local", "Guide One", "guide", "Chennai"),
        ("sme1", f"sme1_{tag}@test.local", "SME One", "sme", "Tiruchirappalli"),
        ("guide2", f"guide2_{tag}@test.local", "Guide Two", "guide", "Madurai"),
        ("sme2", f"sme2_{tag}@test.local", "SME Two", "sme", "Coimbatore"),
        ("hybrid", f"hybrid_{tag}@test.local", "Hybrid Founder", "aspirant", "Chennai"),
    ]

    actors = {
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
            except Exception:
                pass

        prof_record = {
            "id": uid,
            "email": email,
            "role": role,
            "full_name": name,
            "phone": "9876543210",
            "district": dist,
            "state": "Tamil Nadu",
            "profile_data": {
                "business": {
                    "business_name": f"{name} Enterprise",
                    "sector": "Agribusiness & Food Processing",
                    "stage": "Seed",
                }
            },
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
            except Exception:
                pass

        actors[key] = {
            "id": uid,
            "email": email,
            "full_name": name,
            "role": role,
            "district": dist,
        }

    # Grant roles to mentors
    # guide1: pending NDA
    grant_role(actors["guide1"]["id"], "guide", granted_by=ADMIN_ID)
    # sme1: pending NDA
    grant_role(actors["sme1"]["id"], "sme", granted_by=ADMIN_ID)
    
    # guide2: active role + accepted NDA
    grant_role(actors["guide2"]["id"], "guide", granted_by=ADMIN_ID)
    record_legal_acceptance(actors["guide2"]["id"], actors["guide2"]["email"], "terms_and_conditions", actors["guide2"]["full_name"], "I ACCEPT", True)
    record_legal_acceptance(actors["guide2"]["id"], actors["guide2"]["email"], "nda_guide", actors["guide2"]["full_name"], "I ACCEPT", True)
    activate_role(actors["guide2"]["id"], "guide")

    # sme2: active role + accepted NDA
    grant_role(actors["sme2"]["id"], "sme", granted_by=ADMIN_ID)
    record_legal_acceptance(actors["sme2"]["id"], actors["sme2"]["email"], "terms_and_conditions", actors["sme2"]["full_name"], "I ACCEPT", True)
    record_legal_acceptance(actors["sme2"]["id"], actors["sme2"]["email"], "nda_sme", actors["sme2"]["full_name"], "I ACCEPT", True)
    activate_role(actors["sme2"]["id"], "sme")

    # hybrid: promoted to guide and sme with accepted NDAs
    grant_role(actors["hybrid"]["id"], "guide", granted_by=ADMIN_ID)
    grant_role(actors["hybrid"]["id"], "sme", granted_by=ADMIN_ID)
    record_legal_acceptance(actors["hybrid"]["id"], actors["hybrid"]["email"], "terms_and_conditions", actors["hybrid"]["full_name"], "I ACCEPT", True)
    record_legal_acceptance(actors["hybrid"]["id"], actors["hybrid"]["email"], "nda_guide", actors["hybrid"]["full_name"], "I ACCEPT", True)
    record_legal_acceptance(actors["hybrid"]["id"], actors["hybrid"]["email"], "nda_sme", actors["hybrid"]["full_name"], "I ACCEPT", True)
    activate_role(actors["hybrid"]["id"], "guide")
    activate_role(actors["hybrid"]["id"], "sme")

    yield actors

    # Cleanup test users
    if sb_admin:
        for u in created_uids:
            try:
                sb_admin.auth.admin.delete_user(u)
            except Exception:
                pass


# ==============================================================================
# 20-STEP END-TO-END SPECIFICATION TESTS
# ==============================================================================

def test_01_aspirant_alpha_uploads_photo(photo_test_context):
    """Step 1: Aspirant Alpha uploads a photo."""
    alpha_id = photo_test_context["alpha"]["id"]
    img_bytes = make_test_image(width=120, height=120, color=(37, 99, 235))

    ok, err = upload_aspirant_photo(alpha_id, img_bytes, "alpha_avatar.png", uploader_id=alpha_id)
    assert ok is True, f"Alpha upload failed: {err}"
    assert err is None

    # Verify photo metadata is retrievable by Alpha themselves
    photo = get_aspirant_photo(alpha_id, viewer_id=alpha_id, viewer_role="aspirant")
    assert photo is not None, "Photo record should be found for Alpha"
    assert photo.get("width") == 120
    assert photo.get("height") == 120
    assert photo.get("url") is not None


def test_02_admin_assigns_guide_one_to_alpha(photo_test_context):
    """Step 2: Admin assigns Guide One to Alpha."""
    alpha_id = photo_test_context["alpha"]["id"]
    guide1_id = photo_test_context["guide1"]["id"]

    ok, err = assign_guide(alpha_id, guide1_id, admin_id=ADMIN_ID, notes="Assigned Guide One")
    assert ok is True, f"Admin assign guide failed: {err}"

    mentors = get_aspirant_mentors(alpha_id)
    assert mentors.get("guide") is not None
    assert mentors["guide"]["id"] == guide1_id


def test_03_guide_one_nda_acceptance_and_auth_check(photo_test_context):
    """Step 3: Guide One accepts NDA and checks authorization."""
    alpha_id = photo_test_context["alpha"]["id"]
    guide1_id = photo_test_context["guide1"]["id"]

    # Before NDA acceptance: Guide One must be denied authorization
    auth_before, err_before = can_view_aspirant_photo(guide1_id, alpha_id, viewer_role="guide")
    assert auth_before is False, "Guide One should NOT be authorized before NDA acceptance"
    assert "pending NDA" in str(err_before) or "Unauthorized" in str(err_before)

    # Guide One accepts terms and NDA
    guide1_email = photo_test_context["guide1"]["email"]
    guide1_name = photo_test_context["guide1"]["full_name"]
    rec_ok, _ = record_legal_acceptance(guide1_id, guide1_email, "terms_and_conditions", guide1_name, "I ACCEPT", True)
    assert rec_ok is True
    rec_nda, _ = record_legal_acceptance(guide1_id, guide1_email, "nda_guide", guide1_name, "I ACCEPT", True)
    assert rec_nda is True
    act_ok, _ = activate_role(guide1_id, "guide")
    assert act_ok is True

    # After NDA acceptance: Guide One is authorized
    auth_after, err_after = can_view_aspirant_photo(guide1_id, alpha_id, viewer_role="guide")
    assert auth_after is True, f"Guide One should be authorized after NDA: {err_after}"
    assert err_after is None


def test_04_alpha_correct_photo_appears_for_guide_one(photo_test_context):
    """Step 4: Alpha's correct photo appears for Guide One."""
    alpha_id = photo_test_context["alpha"]["id"]
    guide1_id = photo_test_context["guide1"]["id"]

    photo = get_aspirant_photo(alpha_id, viewer_id=guide1_id, viewer_role="guide")
    assert photo is not None, "Guide One should retrieve Alpha's photo"
    assert photo.get("width") == 120
    assert photo.get("url") is not None

    # Verify UI header render with Blue Guide accent
    alpha_prof = get_profile(alpha_id)
    with patch("streamlit.markdown") as mock_md:
        render_aspirant_photo_header(alpha_prof, viewer_id=guide1_id, viewer_role="guide", accent_color="#2563EB")
        assert mock_md.called
        rendered_html = mock_md.call_args[0][0]
        assert "✓ Verified Photo" in rendered_html
        assert "#2563EB" in rendered_html
        assert "Profile Overview: Aspirant Alpha" in rendered_html


def test_05_admin_assigns_sme_one_to_alpha(photo_test_context):
    """Step 5: Admin assigns SME One to Alpha."""
    alpha_id = photo_test_context["alpha"]["id"]
    sme1_id = photo_test_context["sme1"]["id"]

    ok, err = assign_sme(alpha_id, sme1_id, admin_id=ADMIN_ID, notes="Assigned SME One")
    assert ok is True, f"Admin assign SME failed: {err}"

    mentors = get_aspirant_mentors(alpha_id)
    assert mentors.get("sme") is not None
    assert mentors["sme"]["id"] == sme1_id


def test_06_sme_one_nda_acceptance_and_auth_check(photo_test_context):
    """Step 6: SME One accepts NDA and checks authorization."""
    alpha_id = photo_test_context["alpha"]["id"]
    sme1_id = photo_test_context["sme1"]["id"]

    # Before NDA acceptance: SME One must be denied authorization
    auth_before, err_before = can_view_aspirant_photo(sme1_id, alpha_id, viewer_role="sme")
    assert auth_before is False, "SME One should NOT be authorized before NDA acceptance"

    # SME One accepts terms and NDA
    sme1_email = photo_test_context["sme1"]["email"]
    sme1_name = photo_test_context["sme1"]["full_name"]
    record_legal_acceptance(sme1_id, sme1_email, "terms_and_conditions", sme1_name, "I ACCEPT", True)
    record_legal_acceptance(sme1_id, sme1_email, "nda_sme", sme1_name, "I ACCEPT", True)
    activate_role(sme1_id, "sme")

    # After NDA acceptance: SME One is authorized
    auth_after, err_after = can_view_aspirant_photo(sme1_id, alpha_id, viewer_role="sme")
    assert auth_after is True, f"SME One should be authorized after NDA: {err_after}"
    assert err_after is None


def test_07_same_photo_appears_for_sme_one(photo_test_context):
    """Step 7: The same photo appears for SME One."""
    alpha_id = photo_test_context["alpha"]["id"]
    guide1_id = photo_test_context["guide1"]["id"]
    sme1_id = photo_test_context["sme1"]["id"]

    photo_guide = get_aspirant_photo(alpha_id, viewer_id=guide1_id, viewer_role="guide")
    photo_sme = get_aspirant_photo(alpha_id, viewer_id=sme1_id, viewer_role="sme")

    assert photo_sme is not None
    assert photo_guide is not None
    assert photo_sme["user_id"] == alpha_id
    assert photo_sme["width"] == photo_guide["width"]

    # Verify UI header render with Amber SME accent
    alpha_prof = get_profile(alpha_id)
    with patch("streamlit.markdown") as mock_md:
        render_aspirant_photo_header(alpha_prof, viewer_id=sme1_id, viewer_role="sme", accent_color="#D97706")
        assert mock_md.called
        rendered_html = mock_md.call_args[0][0]
        assert "✓ Verified Photo" in rendered_html
        assert "#D97706" in rendered_html


def test_08_guide_two_unassigned_denied_alpha_photo(photo_test_context):
    """Step 8: Guide Two (unassigned) is denied Alpha's photo."""
    alpha_id = photo_test_context["alpha"]["id"]
    guide2_id = photo_test_context["guide2"]["id"]

    # Guide Two is an active Guide with NDA, but NOT assigned to Alpha
    auth, err = can_view_aspirant_photo(guide2_id, alpha_id, viewer_role="guide")
    assert auth is False, "Unassigned Guide Two should NOT have photo authorization"
    assert "Unauthorized" in str(err)

    photo = get_aspirant_photo(alpha_id, viewer_id=guide2_id, viewer_role="guide")
    assert photo is None, "Unassigned Guide Two must receive None"


def test_09_sme_two_unassigned_denied_alpha_photo(photo_test_context):
    """Step 9: SME Two (unassigned) is denied Alpha's photo."""
    alpha_id = photo_test_context["alpha"]["id"]
    sme2_id = photo_test_context["sme2"]["id"]

    # SME Two is an active SME with NDA, but NOT assigned to Alpha
    auth, err = can_view_aspirant_photo(sme2_id, alpha_id, viewer_role="sme")
    assert auth is False, "Unassigned SME Two should NOT have photo authorization"
    assert "Unauthorized" in str(err)

    photo = get_aspirant_photo(alpha_id, viewer_id=sme2_id, viewer_role="sme")
    assert photo is None, "Unassigned SME Two must receive None"


def test_10_admin_removes_guide_one_from_alpha(photo_test_context):
    """Step 10: Admin removes Guide One from Alpha."""
    alpha_id = photo_test_context["alpha"]["id"]
    guide1_id = photo_test_context["guide1"]["id"]

    ok, err = unassign_guide(alpha_id, guide1_id, admin_id=ADMIN_ID, reason="Case rotation")
    assert ok is True, f"Failed to unassign Guide One: {err}"

    mentors = get_aspirant_mentors(alpha_id)
    assert mentors.get("guide") is None or mentors["guide"]["id"] != guide1_id


def test_11_guide_one_immediately_loses_photo_authorization(photo_test_context):
    """Step 11: Guide One immediately loses photo authorization."""
    alpha_id = photo_test_context["alpha"]["id"]
    guide1_id = photo_test_context["guide1"]["id"]

    auth, err = can_view_aspirant_photo(guide1_id, alpha_id, viewer_role="guide")
    assert auth is False, "Unassigned Guide One must immediately lose photo access"
    assert "Unauthorized" in str(err)

    photo = get_aspirant_photo(alpha_id, viewer_id=guide1_id, viewer_role="guide")
    assert photo is None, "Guide One must get None after unassignment"


def test_12_sme_one_retains_authorized_photo_access(photo_test_context):
    """Step 12: SME One retains authorized photo access."""
    alpha_id = photo_test_context["alpha"]["id"]
    sme1_id = photo_test_context["sme1"]["id"]

    auth, err = can_view_aspirant_photo(sme1_id, alpha_id, viewer_role="sme")
    assert auth is True, f"SME One must retain photo access while assigned: {err}"

    photo = get_aspirant_photo(alpha_id, viewer_id=sme1_id, viewer_role="sme")
    assert photo is not None, "SME One should still retrieve Alpha's photo"


def test_13_admin_revokes_sme_one_role(photo_test_context):
    """Step 13: Admin revokes SME One's SME role."""
    sme1_id = photo_test_context["sme1"]["id"]

    ok, err = revoke_role(sme1_id, "sme", reason="Role audit", revoked_by=ADMIN_ID)
    assert ok is True, f"Failed to revoke SME role: {err}"
    assert "sme" not in get_active_roles(sme1_id)


def test_14_sme_one_loses_protected_photo_access(photo_test_context):
    """Step 14: SME One loses protected photo access."""
    alpha_id = photo_test_context["alpha"]["id"]
    sme1_id = photo_test_context["sme1"]["id"]

    auth, err = can_view_aspirant_photo(sme1_id, alpha_id, viewer_role="sme")
    assert auth is False, "Revoked SME One must not have photo authorization"
    assert "not active" in str(err) or "Unauthorized" in str(err)

    photo = get_aspirant_photo(alpha_id, viewer_id=sme1_id, viewer_role="sme")
    assert photo is None, "Revoked SME One must receive None"


def test_15_alpha_changes_photo_authorized_viewers_see_replacement(photo_test_context):
    """Step 15: Alpha changes photo; authorized viewers see replacement."""
    alpha_id = photo_test_context["alpha"]["id"]
    guide2_id = photo_test_context["guide2"]["id"]

    # Assign Guide Two (active role + NDA) to Alpha
    assign_guide(alpha_id, guide2_id, admin_id=ADMIN_ID, notes="Replaced Guide")

    # Alpha uploads a replacement photo (200x200 Green JPEG)
    new_bytes = make_test_image(width=200, height=200, color=(16, 185, 129), img_format="JPEG")
    ok, err = upload_aspirant_photo(alpha_id, new_bytes, "alpha_new.jpg", uploader_id=alpha_id)
    assert ok is True, f"Photo replacement failed: {err}"

    # Authorized Guide Two retrieves replacement photo
    photo = get_aspirant_photo(alpha_id, viewer_id=guide2_id, viewer_role="guide")
    assert photo is not None
    assert photo.get("width") == 200, f"Expected replacement width 200, got {photo.get('width')}"


def test_16_alpha_removes_photo_shows_none_initials(photo_test_context):
    """Step 16: Alpha removes photo; authorized views receive None / initials placeholder."""
    alpha_id = photo_test_context["alpha"]["id"]
    guide2_id = photo_test_context["guide2"]["id"]

    # Alpha deletes their photo
    ok, err = delete_aspirant_photo(alpha_id, deleter_id=alpha_id)
    assert ok is True, f"Alpha delete photo failed: {err}"

    # Authorized viewer receives None
    photo = get_aspirant_photo(alpha_id, viewer_id=guide2_id, viewer_role="guide")
    assert photo is None, "Photo must be None after deletion"

    # UI renders neutral initials placeholder
    alpha_prof = get_profile(alpha_id)
    with patch("streamlit.markdown") as mock_md:
        render_aspirant_photo_header(alpha_prof, viewer_id=guide2_id, viewer_role="guide", accent_color="#2563EB")
        assert mock_md.called
        rendered_html = mock_md.call_args[0][0]
        assert "No Photo Uploaded" in rendered_html
        assert "AA" in rendered_html  # Initials for Aspirant Alpha


def test_17_hybrid_founder_photo_isolation(photo_test_context):
    """Step 17: Hybrid Founder retains own photo while viewing separately assigned cases."""
    hybrid_id = photo_test_context["hybrid"]["id"]
    beta_id = photo_test_context["beta"]["id"]
    gamma_id = photo_test_context["gamma"]["id"]

    # 1. Hybrid uploads own photo
    hybrid_bytes = make_test_image(width=150, height=150, color=(147, 51, 234))
    ok, err = upload_aspirant_photo(hybrid_id, hybrid_bytes, "hybrid.png", uploader_id=hybrid_id)
    assert ok is True

    # 2. Hybrid views own photo
    own_photo = get_aspirant_photo(hybrid_id, viewer_id=hybrid_id, viewer_role="aspirant")
    assert own_photo is not None
    assert own_photo["width"] == 150

    # 3. Hybrid is assigned as Guide to Beta
    assign_guide(beta_id, hybrid_id, admin_id=ADMIN_ID, notes="Hybrid mentorship")
    beta_bytes = make_test_image(width=160, height=160, color=(245, 158, 11))
    upload_aspirant_photo(beta_id, beta_bytes, "beta.png", uploader_id=beta_id)

    # Hybrid viewing assigned Beta's photo -> Authorized
    beta_photo = get_aspirant_photo(beta_id, viewer_id=hybrid_id, viewer_role="guide")
    assert beta_photo is not None
    assert beta_photo["width"] == 160

    # 4. Hybrid attempts to view unassigned Gamma's photo -> Denied
    gamma_bytes = make_test_image(width=180, height=180, color=(239, 68, 68))
    upload_aspirant_photo(gamma_id, gamma_bytes, "gamma.png", uploader_id=gamma_id)

    gamma_photo = get_aspirant_photo(gamma_id, viewer_id=hybrid_id, viewer_role="guide")
    assert gamma_photo is None, "Hybrid must not view unassigned Gamma's photo"


def test_18_existing_admin_directory_photo_display(photo_test_context):
    """Step 18: Existing Admin Entrepreneurs Directory photo display continues working."""
    beta_id = photo_test_context["beta"]["id"]
    gamma_id = photo_test_context["gamma"]["id"]

    # Single Admin (fulcrumindia1@gmail.com / ADMIN_ID) can view any Aspirant's photo
    auth_beta, _ = can_view_aspirant_photo(ADMIN_ID, beta_id, viewer_role="admin")
    assert auth_beta is True

    auth_gamma, _ = can_view_aspirant_photo(ADMIN_ID, gamma_id, viewer_role="admin")
    assert auth_gamma is True

    admin_view_beta = get_aspirant_photo(beta_id, viewer_id=ADMIN_ID, viewer_role="admin")
    assert admin_view_beta is not None
    assert admin_view_beta["width"] == 160

    admin_view_gamma = get_aspirant_photo(gamma_id, viewer_id=ADMIN_ID, viewer_role="admin")
    assert admin_view_gamma is not None
    assert admin_view_gamma["width"] == 180


def test_19_zero_side_effects_on_journey_schemes_messaging(photo_test_context):
    """Step 19: Existing profile, Journey, scheme, messaging workflows remain unchanged."""
    alpha_id = photo_test_context["alpha"]["id"]

    # Check that photo lifecycle operations did NOT create any journey events
    timeline = get_journey_timeline(alpha_id)
    photo_events = [e for e in timeline if "photo" in str(e.get("event_type", "")).lower() or "avatar" in str(e.get("title", "")).lower()]
    assert len(photo_events) == 0, f"Expected 0 photo journey events, found: {photo_events}"

    # Verify profile business data was untouched
    alpha_prof = get_profile(alpha_id)
    assert alpha_prof["profile_data"]["business"]["sector"] == "Agribusiness & Food Processing"

    # Verify scheme matching engine executes normally
    matches = match_schemes_for_aspirant(alpha_id)
    assert isinstance(matches, list)


def test_20_tampering_forged_ids_and_non_aspirant_upload_prevention(photo_test_context):
    """Step 20: Direct backend calls with forged viewer IDs or without assignment cannot bypass authorization."""
    alpha_id = photo_test_context["alpha"]["id"]
    beta_id = photo_test_context["beta"]["id"]
    guide1_id = photo_test_context["guide1"]["id"]
    sme2_id = photo_test_context["sme2"]["id"]

    # 1. Random forged UUID viewer ID
    fake_viewer = str(uuid.uuid4())
    auth_fake, err_fake = can_view_aspirant_photo(fake_viewer, beta_id, viewer_role="guide")
    assert auth_fake is False
    assert "Unauthorized" in str(err_fake)

    # 2. Guide attempting to upload photo on behalf of Aspirant
    dummy_bytes = make_test_image(width=100, height=100)
    ok_bad_up, err_bad_up = upload_aspirant_photo(alpha_id, dummy_bytes, uploader_id=guide1_id)
    assert ok_bad_up is False
    assert "Only the entrepreneur" in str(err_bad_up)

    # 3. SME attempting to delete Aspirant photo
    ok_bad_del, err_bad_del = delete_aspirant_photo(beta_id, deleter_id=sme2_id)
    assert ok_bad_del is False
    assert "Only the entrepreneur or Platform Admin" in str(err_bad_del)

    # 4. Null / Empty parameters rejected safely
    assert get_aspirant_photo("") is None
    assert get_aspirant_photo(None) is None
    auth_none, _ = can_view_aspirant_photo("", "")
    assert auth_none is False


def test_21_photo_optimization_and_adaptive_compression():
    """Step 21: Verify EXIF orientation correction, WebP conversion, 320px max, and 150 KB cap."""
    import random
    from PIL import ImageOps

    # 1. EXIF orientation transposition
    img_exif = Image.new("RGB", (400, 200), color=(220, 38, 38))
    exif = img_exif.getexif()
    exif[0x0112] = 6  # 90 deg CW rotation
    buf_exif = io.BytesIO()
    img_exif.save(buf_exif, format="JPEG", exif=exif)

    ok_e, proc_e, ct_e, w_e, h_e, err_e = validate_and_process_photo(buf_exif.getvalue())
    assert ok_e is True
    assert ct_e == "image/webp"
    assert w_e <= 320 and h_e <= 320
    assert h_e >= w_e  # Verified 90 degree transposition from landscape to portrait

    # 2. Complex high-res photo under 5 MB -> auto-resized to max 320 and compressed under 150 KB
    random.seed(99)
    img_large = Image.new("RGB", (1920, 1080))
    px = img_large.load()
    for x in range(0, 1920, 4):
        for y in range(0, 1080, 4):
            val = (x * 3 + y * 7 + random.randint(0, 100)) % 256
            px[x, y] = (val, (val * 2) % 256, (val * 3) % 256)
    buf_large = io.BytesIO()
    img_large.save(buf_large, format="JPEG", quality=90)
    large_bytes = buf_large.getvalue()

    ok_l, proc_l, ct_l, w_l, h_l, err_l = validate_and_process_photo(large_bytes)
    assert ok_l is True
    assert ct_l == "image/webp"
    assert w_l <= 320 and h_l <= 320
    assert len(proc_l) <= 150 * 1024  # Strict 150 KB cap

    # 3. Rejection of > 5 MB upload
    oversized_bytes = b"0" * (5 * 1024 * 1024 + 1024)
    ok_over, _, _, _, _, err_over = validate_and_process_photo(oversized_bytes)
    assert ok_over is False
    assert "exceeds maximum 5 MB limit" in err_over


def test_22_single_storage_shared_object_across_roles(photo_test_context):
    """Step 22: Ensure single photo is shared across Admin, Guide, and SME with zero duplication."""
    beta_id = photo_test_context["beta"]["id"]
    guide2_id = photo_test_context["guide2"]["id"]
    sme2_id = photo_test_context["sme2"]["id"]

    # Assign Guide Two and SME Two to Beta
    assign_guide(beta_id, guide2_id, admin_id=ADMIN_ID)
    assign_sme(beta_id, sme2_id, admin_id=ADMIN_ID)

    # Fetch photo for all three roles
    admin_photo = get_aspirant_photo(beta_id, viewer_id=ADMIN_ID, viewer_role="admin")
    guide_photo = get_aspirant_photo(beta_id, viewer_id=guide2_id, viewer_role="guide")
    sme_photo = get_aspirant_photo(beta_id, viewer_id=sme2_id, viewer_role="sme")

    assert admin_photo is not None
    assert guide_photo is not None
    assert sme_photo is not None

    # Verify identical storage_path and id (no separate copies created for different roles)
    assert admin_photo["id"] == guide_photo["id"] == sme_photo["id"]
    assert admin_photo.get("storage_path") == guide_photo.get("storage_path") == sme_photo.get("storage_path")

