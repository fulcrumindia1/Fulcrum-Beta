"""
Post-Fix Verification Suite for Fulcrum-Beta 32-User Live QA Campaign
=====================================================================
Originally reproduced DEF-32-001..010 on commit 988127b; updated to verify that
all confirmed codebase/schema defects remain resolved in isolated temp storage
and static AST inspection without touching production databases.
"""
import sys
from pathlib import Path

import pytest
import streamlit as st

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


@pytest.fixture
def isolated_local_db(tmp_path, monkeypatch):
    from services.local_db import LocalDatabase
    import services.local_db as local_db_mod
    import services.auth as auth_mod

    db_file = tmp_path / "qa32_verify.db"
    ldb = LocalDatabase(db_file=db_file)
    monkeypatch.setenv("DATA_BACKEND", "local")
    monkeypatch.setattr(auth_mod, "get_data_backend", lambda: "local")
    monkeypatch.setattr(local_db_mod, "get_local_db", lambda: ldb)
    for mod_name in list(sys.modules.keys()):
        if mod_name.startswith("services."):
            m = sys.modules[mod_name]
            if hasattr(m, "get_local_db"):
                monkeypatch.setattr(m, "get_local_db", lambda: ldb)
            if hasattr(m, "get_data_backend"):
                monkeypatch.setattr(m, "get_data_backend", lambda: "local")
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    return ldb


def test_repro_def_001_lifecycle_supabase_column_mismatch():
    """
    DEF-32-001 (FIXED): services/account_lifecycle.py adapts between pre-009 live schema
    (status_reason/old_status/details) and Migration 009 columns, with compensating rollback.
    """
    src = (REPO_ROOT / "services" / "account_lifecycle.py").read_text(encoding="utf-8")
    mig10 = (REPO_ROOT / "migrations" / "010_align_account_lifecycle_columns.sql").read_text(encoding="utf-8")
    assert "_execute_supabase_adaptive" in src
    assert "_restore_relationship_snapshots" in src
    assert "status_reason" in src and "old_status" in src
    assert "ADD COLUMN IF NOT EXISTS status_reason TEXT" in mig10


def test_repro_def_002_hybrid_workspace_session_role_rejection(isolated_local_db, monkeypatch):
    """
    DEF-32-002 (FIXED): Hybrid user active_workspace overrides stale base st.session_state['role']
    for authorized active role holders in consultation replies and roadmap toggles.
    """
    from services.journey import toggle_event_roadmap_inclusion, add_guide_contribution
    from services.help_requests import guide_respond_request, create_request
    from services.roles import SOLE_ADMIN_UUID

    ldb = isolated_local_db
    ldb.upsert_profile({"id": "qa_a", "email": "a@test.in", "role": "aspirant", "full_name": "QA A", "is_active": 1})
    ldb.upsert_profile({"id": "qa_b", "email": "b@test.in", "role": "aspirant", "full_name": "QA B", "is_active": 1})
    ldb.upsert_profile({"id": "qa_t", "email": "t@test.in", "role": "guide", "full_name": "QA T", "is_active": 1})
    ldb.upsert_user_role({"user_id": "qa_a", "role": "guide", "status": "active", "granted_by": SOLE_ADMIN_UUID})
    ldb.upsert_user_role({"user_id": "qa_b", "role": "sme", "status": "active", "granted_by": SOLE_ADMIN_UUID})
    ldb.upsert_user_role({"user_id": "qa_t", "role": "aspirant", "status": "active", "granted_by": SOLE_ADMIN_UUID})
    ldb.assign_guide("qa_b", "qa_a", SOLE_ADMIN_UUID, "assign A->B")
    ldb.assign_guide("qa_t", "qa_a", SOLE_ADMIN_UUID, "assign A->T")

    req, err = create_request("qa_b", "Hyb Test", "Body text", "MEDIUM", "GENERAL", "guide")
    assert req is not None and err is None

    monkeypatch.setattr(st, "session_state", {
        "user": {"id": "qa_a", "email": "a@test.in", "role": "aspirant"},
        "user_id": "qa_a",
        "role": "aspirant",
        "active_workspace": "guide",
    })
    ok_reply, err_reply = guide_respond_request(req["id"], "qa_a", "IN_PROGRESS", "Reply from active Guide workspace")
    assert ok_reply is True, err_reply

    ev, _ = add_guide_contribution("qa_t", "qa_a", "Test Milestone", "Body")
    assert ev is not None
    monkeypatch.setattr(st, "session_state", {
        "user": {"id": "qa_t", "email": "t@test.in", "role": "guide"},
        "user_id": "qa_t",
        "role": "guide",
        "active_workspace": "aspirant",
    })
    ok_tog, err_tog = toggle_event_roadmap_inclusion(ev["id"], "qa_t", False)
    assert ok_tog is True, err_tog

    # Explicit guide role invocation stays rejected
    ok_den, _ = toggle_event_roadmap_inclusion(ev["id"], "qa_t", True, actor_id="qa_t", actor_role="guide")
    assert ok_den is False


def test_repro_def_003_admin_provisioning_temp_pw_regenerates_per_rerun():
    """
    DEF-32-003 (FIXED): views/admin.py caches Tab 2 & Tab 3 provisional passwords in st.session_state.
    """
    admin_src = (REPO_ROOT / "views" / "admin.py").read_text(encoding="utf-8")
    assert '_get_or_init_provisional_password("adm_cg_provisional_pwd")' in admin_src
    assert '_get_or_init_provisional_password("adm_cs_provisional_pwd")' in admin_src
    assert 'st.session_state.pop("adm_cg_provisional_pwd"' in admin_src
    assert 'st.session_state.pop("adm_cs_provisional_pwd"' in admin_src


def test_repro_def_004_mentor_base_hybrid_invisible_in_paginate_profiles(isolated_local_db):
    """
    DEF-32-004 (FIXED): paginate_profiles(role='aspirant') includes active 'aspirant' grants in user_roles.
    """
    from services.pagination import paginate_profiles

    ldb = isolated_local_db
    ldb.upsert_profile({"id": "qa_f", "email": "f@test.in", "role": "aspirant", "full_name": "QA F", "is_active": 1})
    ldb.upsert_profile({"id": "qa_t", "email": "t@test.in", "role": "guide", "full_name": "QA T", "is_active": 1})
    ldb.upsert_user_role({"user_id": "qa_t", "role": "guide", "status": "active", "granted_by": "admin"})
    ldb.upsert_user_role({"user_id": "qa_t", "role": "aspirant", "status": "active", "granted_by": "admin"})

    rows, total = paginate_profiles(role="aspirant", page=1, page_size=50)
    ids = {r["id"] for r in rows}
    assert "qa_f" in ids
    assert "qa_t" in ids
    assert total == 2


def test_repro_def_005_tab12_coi_recusal_leaves_conflict_declared_and_blocks_reassignment(isolated_local_db):
    """
    DEF-32-005 (FIXED): resolve_sme_conflict transitions COI records ('APPROVED' -> 'REJECTED')
    and allows Tab 12 / Admin re-assignment once recusal restriction is lifted.
    """
    from services.governance import declare_sme_conflict, resolve_sme_conflict, check_sme_has_conflict, list_sme_conflicts
    from services.relationships import assign_sme, unassign_sme
    from services.roles import SOLE_ADMIN_UUID, SOLE_ADMIN_EMAIL

    ldb = isolated_local_db
    ldb.upsert_profile({"id": SOLE_ADMIN_UUID, "email": SOLE_ADMIN_EMAIL, "role": "admin", "full_name": "Admin", "is_active": 1})
    ldb.upsert_profile({"id": "qa_c", "email": "c@test.in", "role": "aspirant", "full_name": "QA C", "is_active": 1})
    ldb.upsert_profile({"id": "qa_p", "email": "p@test.in", "role": "sme", "full_name": "QA P", "is_active": 1})
    ldb.upsert_user_role({"user_id": "qa_p", "role": "sme", "status": "active", "granted_by": SOLE_ADMIN_UUID})

    ok1, err1 = assign_sme("qa_c", "qa_p", admin_id=SOLE_ADMIN_UUID, allow_pending_nda=True)
    assert ok1 is True, f"Initial assign failed: {err1}"

    ok_d, err_d = declare_sme_conflict("qa_p", "qa_c", True, "Vendor overlap")
    assert ok_d is True, f"Declare COI failed: {err_d}"

    decls = list_sme_conflicts(sme_id="qa_p", aspirant_id="qa_c")
    ok_u, err_u = unassign_sme("qa_c", "qa_p", admin_id=SOLE_ADMIN_UUID, reason="COI approved")
    assert ok_u is True, f"Unassign failed: {err_u}"
    ok_app, err_app = resolve_sme_conflict(decls[0]["id"], SOLE_ADMIN_UUID, "APPROVED")
    assert ok_app is True, err_app
    assert list_sme_conflicts(sme_id="qa_p", aspirant_id="qa_c")[0]["status"] == "APPROVED"

    ok_clr, err_clr = resolve_sme_conflict(decls[0]["id"], SOLE_ADMIN_UUID, "REJECTED")
    assert ok_clr is True, err_clr
    assert check_sme_has_conflict("qa_p", "qa_c") is False

    ok_r, err_r = assign_sme("qa_c", "qa_p", admin_id=SOLE_ADMIN_UUID, allow_pending_nda=True)
    assert ok_r is True, f"Re-assign after clearing restriction failed: {err_r}"


def test_repro_def_007_coguide_profile_auth_query_omits_guide_ids_array():
    """
    DEF-32-007 (FIXED): services/profiles.py relationship check includes guide_ids.cs & sme_ids.cs.
    """
    src = (REPO_ROOT / "services" / "profiles.py").read_text(encoding="utf-8")
    assert "guide_ids.cs." in src and "sme_ids.cs." in src


def test_repro_def_009_password_min_length_mismatch_ui_6_vs_backend_8(isolated_local_db):
    """
    DEF-32-009 (FIXED): app.py gate aligns with services/auth.py (>= 8 characters).
    """
    from services.auth import complete_first_login_password_change

    app_src = (REPO_ROOT / "app.py").read_text(encoding="utf-8")
    assert "len(np1) < 8" in app_src

    ok, err = complete_first_login_password_change("any-uid", "Ab1234")
    assert ok is False
    assert "at least 8 characters" in (err or "").lower()
