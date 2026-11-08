"""
tests/test_single_admin_and_photos.py
=====================================
Single-Admin Identity Lock + Private Professional Photographs regression suite.
Covers NEG-01..NEG-12 from 08_REGRESSION_AND_NEGATIVE_TEST_PLAN.md (unit level, mocked I/O).
"""

import io
from unittest.mock import patch, MagicMock

import pytest
from PIL import Image

from services.roles import is_strict_admin, grant_role, SOLE_ADMIN_EMAIL, SOLE_ADMIN_UUID

PRAVIN_ID = "2970a3ee-46fc-483c-b276-aa2a955ba123"
PRAVIN_EMAIL = "pravindev666@gmail.com"
GUIDE_A = "e7cb2135-063f-4fa1-91f3-4e058ee22650"
GUIDE_B = "abdc3747-bf27-446d-9d4b-a9b80beae46b"
SME_A = "781f0854-7126-4479-a693-52a0ca945550"
ASPIRANT_ID = "4c9cf064-6146-4ff8-b826-2678028f7eb1"


def _img_bytes(fmt="PNG", size=(400, 300), mode="RGB"):
    buf = io.BytesIO()
    Image.new(mode, size, (120, 80, 200) if mode == "RGB" else (120, 80, 200, 128)).save(buf, format=fmt)
    return buf.getvalue()


# ── SINGLE ADMIN IDENTITY ────────────────────────────────────────────────
class TestSingleAdminLock:

    def test_rc1_sole_admin_is_admin(self):
        assert is_strict_admin(user_id=SOLE_ADMIN_UUID, email=SOLE_ADMIN_EMAIL) is True
        assert is_strict_admin(user_dict={"id": SOLE_ADMIN_UUID, "email": SOLE_ADMIN_EMAIL, "role": "admin"}) is True

    @pytest.mark.parametrize("injected_role", ["admin", "district_admin", "operational_admin"])
    def test_neg01_pravin_never_admin_even_with_injected_role(self, injected_role):
        user = {"id": PRAVIN_ID, "email": PRAVIN_EMAIL, "role": injected_role}
        assert is_strict_admin(user_dict=user) is False

    def test_neg01b_pravin_uuid_with_admin_email_spoof_denied(self):
        # Email matches but UUID belongs to someone else -> profile lookup says pravin
        with patch("services.profiles.get_profile", return_value={"id": PRAVIN_ID, "email": PRAVIN_EMAIL, "role": "admin"}):
            assert is_strict_admin(user_id=PRAVIN_ID) is False

    def test_neg01c_active_roles_strip_admin_for_non_primary(self):
        from services import roles as roles_mod
        with patch.object(roles_mod, "get_data_backend", return_value="sqlite"), \
             patch.object(roles_mod, "get_memo", return_value=None), \
             patch.object(roles_mod, "set_memo"), \
             patch.object(roles_mod, "get_local_db") as mdb, \
             patch("services.profiles.get_profile", return_value={"id": PRAVIN_ID, "email": PRAVIN_EMAIL, "role": "admin"}):
            mdb.return_value.get_user_roles.return_value = [
                {"user_id": PRAVIN_ID, "role": "admin", "status": "active"},
            ]
            active = roles_mod.get_active_roles(PRAVIN_ID)
            assert "admin" not in active
            assert "aspirant" in active

    def test_neg02_promote_non_primary_email_blocked(self):
        from services.auth import promote_user_to_admin
        ok, err = promote_user_to_admin(PRAVIN_EMAIL)
        assert ok is False
        assert "only fulcrumindia1@gmail.com" in err.lower()

    def test_neg02b_backfill_demotes_rogue_admin_and_ignores_custom_email(self):
        from services import auth as auth_mod
        admin_client = MagicMock()
        u = MagicMock(); u.id = PRAVIN_ID; u.email = PRAVIN_EMAIL; u.user_metadata = {"role": "admin"}
        admin_client.auth.admin.list_users.return_value = [u]
        admin_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [{"id": PRAVIN_ID, "role": "admin"}]
        with patch.object(auth_mod, "get_supabase_admin_client", return_value=admin_client):
            auth_mod.backfill_auth_users(default_admin_email=PRAVIN_EMAIL)
        admin_client.table.return_value.update.assert_called_with({"role": "aspirant"})

    def test_neg03_admin_role_cannot_be_granted(self):
        ok, err = grant_role(user_id=PRAVIN_ID, role="admin")
        assert ok is False

    def test_neg04_primary_admin_id_never_falls_back_to_other_admin(self):
        from services import governance as gov
        with patch.object(gov, "get_global_cache", return_value=None), \
             patch.object(gov, "set_global_cache"), \
             patch("services.profiles.list_profiles_by_role", return_value=[{"id": PRAVIN_ID, "email": PRAVIN_EMAIL, "role": "admin"}]):
            assert gov.get_primary_admin_id() == SOLE_ADMIN_UUID

    def test_neg05_external_contact_rejects_rogue_admin(self):
        from services.external_contact import is_authorized_admin
        assert is_authorized_admin({"id": PRAVIN_ID, "email": PRAVIN_EMAIL, "role": "admin"}) is False
        with patch("services.profiles.get_profile", return_value={"id": PRAVIN_ID, "email": PRAVIN_EMAIL, "role": "admin"}):
            assert is_authorized_admin(PRAVIN_ID) is False
        assert is_authorized_admin(SOLE_ADMIN_UUID) is True


# ── PROFESSIONAL PHOTOS ──────────────────────────────────────────────────
def _mentor_roles(uid):
    return {GUIDE_A: ["guide"], GUIDE_B: ["guide"], SME_A: ["sme"]}.get(uid, ["aspirant"])


@pytest.fixture
def mentor_roles():
    with patch("services.professional_photos.get_active_roles", side_effect=_mentor_roles), \
         patch("services.professional_photos.get_pending_nda_roles", return_value=[]), \
         patch("services.profiles.get_profile", side_effect=lambda uid: {"id": uid, "email": f"{uid}@x.in", "role": _mentor_roles(uid)[0]}):
        yield


class TestProfessionalPhotos:

    def test_self_and_admin_can_view(self, mentor_roles):
        from services.professional_photos import can_view_professional_photo
        assert can_view_professional_photo(GUIDE_A, GUIDE_A)[0] is True
        assert can_view_professional_photo(SME_A, SME_A)[0] is True
        assert can_view_professional_photo(SOLE_ADMIN_UUID, GUIDE_A, viewer_email=SOLE_ADMIN_EMAIL)[0] is True

    def test_neg06_aspirant_cannot_view_mentor_photo(self, mentor_roles):
        from services.professional_photos import can_view_professional_photo, get_professional_photo_url, get_professional_photos_batch
        assert can_view_professional_photo(ASPIRANT_ID, GUIDE_A)[0] is False
        assert can_view_professional_photo(PRAVIN_ID, SME_A, viewer_email=PRAVIN_EMAIL)[0] is False
        assert get_professional_photo_url(ASPIRANT_ID, GUIDE_A) is None
        assert get_professional_photos_batch(ASPIRANT_ID, [GUIDE_A, SME_A]) == {}

    def test_neg06b_aspirant_cannot_view_own_professional_photo_slot(self, mentor_roles):
        from services.professional_photos import can_view_professional_photo
        assert can_view_professional_photo(ASPIRANT_ID, ASPIRANT_ID)[0] is False

    def test_neg07_guide_cannot_view_or_upload_other_guide(self, mentor_roles):
        from services.professional_photos import can_view_professional_photo, upload_professional_photo
        assert can_view_professional_photo(GUIDE_A, GUIDE_B)[0] is False
        ok, err = upload_professional_photo(GUIDE_B, _img_bytes(), uploaded_by=GUIDE_A)
        assert ok is False and "unauthorized" in err.lower()

    def test_neg08_sme_cannot_delete_guide_photo(self, mentor_roles):
        from services.professional_photos import delete_professional_photo
        ok, err = delete_professional_photo(GUIDE_A, actor_id=SME_A)
        assert ok is False and "unauthorized" in err.lower()

    def test_neg10_validation_rejects_bad_inputs(self):
        from services.professional_photos import validate_and_normalize_professional_photo as v
        assert v(b"")[0] is False
        assert v(b"MZ\x90\x00 not an image" * 10, "exploit.jpg")[0] is False
        assert v(_img_bytes(size=(80, 80)))[0] is False
        assert v(b"0" * (5 * 1024 * 1024 + 1))[0] is False
        buf = io.BytesIO(); Image.new("RGB", (300, 300)).save(buf, format="GIF")
        assert v(buf.getvalue())[0] is False

    def test_normalization_output_is_320_webp_under_150kb(self):
        from services.professional_photos import validate_and_normalize_professional_photo as v
        ok, data, mime, w, h, sha, err = v(_img_bytes("PNG", (1200, 800), "RGBA"))
        assert ok, err
        assert mime == "image/webp" and (w, h) == (320, 320)
        assert len(data) <= 150 * 1024 and len(sha) == 64
        out = Image.open(io.BytesIO(data))
        assert out.size == (320, 320) and out.format == "WEBP"
        assert not out.getexif()

    def test_neg11_failed_db_upsert_rolls_back_new_object_and_keeps_old(self, mentor_roles):
        from services import professional_photos as pp
        admin = MagicMock()
        tbl = admin.table.return_value
        tbl.select.return_value.eq.return_value.execute.return_value.data = [{"storage_path": f"{GUIDE_A}/headshot_old.webp"}]
        tbl.upsert.return_value.execute.side_effect = Exception("violates check constraint byte_size")
        bucket = admin.storage.from_.return_value
        bucket.list.return_value = []
        with patch.object(pp, "get_data_backend", return_value="supabase"), \
             patch.object(pp, "get_supabase_admin_client", return_value=admin), \
             patch.object(pp, "ensure_professional_photo_bucket", return_value=True):
            ok, err = pp.upload_professional_photo(GUIDE_A, _img_bytes(), uploaded_by=GUIDE_A)
        assert ok is False
        removed = [c.args[0] for c in bucket.remove.call_args_list]
        assert removed, "new object must be rolled back"
        assert all(f"{GUIDE_A}/headshot_old.webp" not in paths for paths in removed), "old photo must be preserved"

    def test_sqlite_roundtrip_upload_view_delete(self, mentor_roles):
        from services import professional_photos as pp
        with patch.object(pp, "get_data_backend", return_value="sqlite"):
            ok, err = pp.upload_professional_photo(GUIDE_A, _img_bytes(), uploaded_by=GUIDE_A)
            assert ok, err
            url = pp.get_professional_photo_url(GUIDE_A, GUIDE_A)
            assert url and url.startswith("data:image/webp;base64,")
            assert pp.get_professional_photo_url(ASPIRANT_ID, GUIDE_A) is None
            ok, _ = pp.delete_professional_photo(GUIDE_A, actor_id=GUIDE_A)
            assert ok
            assert pp.get_professional_photo_url(GUIDE_A, GUIDE_A) is None


# ── WORKFLOW FIXES ───────────────────────────────────────────────────────
class TestWorkflowFixes:

    def test_neg12_conflicted_sme_cannot_respond(self):
        from services import help_requests as hr
        db = MagicMock()
        conn = db._get_conn.return_value
        conn.cursor.return_value.fetchone.return_value = {"id": "t1", "aspirant_id": ASPIRANT_ID, "assigned_sme_id": SME_A, "subject": "s", "sme_response": ""}
        with patch.object(hr, "get_data_backend", return_value="sqlite"), \
             patch.object(hr, "get_local_db", return_value=db), \
             patch("services.governance.check_sme_has_conflict", return_value=True):
            ok, err = hr.sme_respond_request("t1", SME_A, "IN_PROGRESS", "advice")
        assert ok is False and "conflict of interest" in err.lower()

    def test_engagement_roster_exposes_view_keys(self):
        from services import inactivity as ina
        asp = {"id": ASPIRANT_ID, "full_name": "Austin Thambi", "email": "a@x.in", "phone": "9876543210",
               "completion_pct": 80, "profile_data": {"business": {"business_name": "TechNova"}},
               "created_at": "2026-11-01T00:00:00+00:00"}
        with patch.object(ina, "get_memo", return_value=None), patch.object(ina, "set_memo"), \
             patch("services.roles.list_active_profiles_for_role", return_value=[asp]), \
             patch("services.relationships.get_all_relationships", return_value=[]), \
             patch("services.help_requests.list_requests", return_value=[]), \
             patch("services.schemes.get_released_schemes_for_aspirant", return_value=[]), \
             patch("services.journey.get_journey_timeline", return_value=[]), \
             patch("services.profiles.get_profiles_batch", return_value={}):
            roster = ina.evaluate_aspirant_engagement_roster()
        r = roster[0]
        for k in ("full_name", "business_name", "email", "phone", "engagement_state", "is_blocked",
                  "state_label", "days_inactive", "last_activity_source", "guide_names", "sme_names"):
            assert k in r, k
        assert r["full_name"] == "Austin Thambi" and r["business_name"] == "TechNova"
        assert r["is_blocked"] is True  # no guide assigned

