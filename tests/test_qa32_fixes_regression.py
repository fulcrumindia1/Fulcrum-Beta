"""
Regression & Verification Suite for DEF-32-001 through DEF-32-010
==================================================================
Covers every defect uncovered in the 32-user live E2E simulation:
- DEF-32-001: Schema-adaptive Supabase account lifecycle writes + atomic handover rollback
- DEF-32-002: Hybrid active_workspace session authorization for help requests & journey toggle
- DEF-32-003: Session-cached provisional password across Admin Tab 2/3 form reruns
- DEF-32-004: paginate_profiles('aspirant') & Control Tower KPI union with user_roles grants
- DEF-32-005: Tab 12 COI APPROVED/REJECTED transitions & explicit recusal clearance
- DEF-32-006: update_aspirant_profile preserves mentor keys inside profile_data
- DEF-32-007: Co-Guide array membership (guide_ids/sme_ids) & co-mentor profile visibility
- DEF-32-008: Co-Guide additive radio, Chennai default, mentor edit helper, scheme delegation, complaint summary
- DEF-32-009: app.py first-login password UI gate enforces >= 8 characters matching backend
- DEF-32-010: Workspace-bound sidebar role pill, role sync & workspace-scoped notifications
"""
import copy
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
import streamlit as st

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


@pytest.fixture
def isolated_local_db(tmp_path, monkeypatch):
    from services.local_db import LocalDatabase
    import services.local_db as local_db_mod
    import services.auth as auth_mod
    import services.cache as cache_mod

    db_file = tmp_path / "qa32_fixes_reg.db"
    ldb = LocalDatabase(db_file=db_file)
    cache_mod._MEMO_STORE.clear() if hasattr(cache_mod, "_MEMO_STORE") else None
    monkeypatch.setenv("DATA_BACKEND", "local")
    monkeypatch.setattr(auth_mod, "get_data_backend", lambda: "local")
    monkeypatch.setattr(local_db_mod, "get_local_db", lambda: ldb)
    for mod_name, mod in list(sys.modules.items()):
        if mod_name.startswith("services."):
            if hasattr(mod, "get_local_db"):
                monkeypatch.setattr(mod, "get_local_db", lambda: ldb)
            if hasattr(mod, "get_data_backend"):
                monkeypatch.setattr(mod, "get_data_backend", lambda: "local")
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    return ldb


class _FakePostgrestTable:
    """Simulates a PostgREST table enforcing strict column whitelist (raising PGRST204 on unknown cols)."""

    def __init__(self, store, name, allowed_cols):
        self.store = store
        self.name = name
        self.allowed_cols = set(allowed_cols)
        self._op = None
        self._payload = None
        self._filters = []
        self._limit = None

    def select(self, cols="*", count=None, head=False):
        self._op = ("select", cols, count, head)
        return self

    def update(self, payload):
        self._op = ("update", dict(payload))
        return self

    def insert(self, payload):
        self._op = ("insert", dict(payload))
        return self

    def eq(self, col, val):
        self._filters.append(("eq", col, val))
        return self

    def neq(self, col, val):
        self._filters.append(("neq", col, val))
        return self

    def in_(self, col, vals):
        self._filters.append(("in", col, list(vals)))
        return self

    def or_(self, expr):
        return self

    def order(self, col, desc=False):
        return self

    def range(self, start, end):
        self._range = (start, end)
        return self

    def limit(self, n):
        self._limit = n
        return self

    def _match(self, row):
        for kind, col, val in self._filters:
            if kind == "eq" and str(row.get(col)) != str(val):
                return False
            if kind == "neq" and row.get(col) == val:
                return False
            if kind == "in" and row.get(col) not in val:
                return False
        return True

    def execute(self):
        op = self._op[0]
        if op == "select":
            cols = self._op[1]
            head = self._op[3]
            if cols != "*":
                for c in [x.strip() for x in cols.split(",") if x.strip()]:
                    if c not in self.allowed_cols:
                        raise Exception(f"{{'code': '42703', 'message': 'column {self.name}.{c} does not exist'}}")
            rows = [copy.deepcopy(r) for r in self.store[self.name] if self._match(r)]
            if hasattr(self, "_range"):
                s, e = self._range
                sliced = rows[s:e + 1]
                return SimpleNamespace(data=[] if head else sliced, count=len(rows))
            if self._limit is not None:
                rows = rows[: self._limit]
            return SimpleNamespace(data=[] if head else rows, count=len(rows))

        if op == "update":
            payload = self._op[1]
            for k in payload.keys():
                if k not in self.allowed_cols:
                    msg = "Could not find the '" + k + "' column of '" + self.name + "' in the schema cache"
                    raise Exception(f"{{'code': 'PGRST204', 'message': {msg!r}}}")
            updated = []
            for r in self.store[self.name]:
                if self._match(r):
                    r.update(copy.deepcopy(payload))
                    updated.append(copy.deepcopy(r))
            return SimpleNamespace(data=updated)

        if op == "insert":
            payload = self._op[1]
            for k in payload.keys():
                if k not in self.allowed_cols:
                    msg = "Could not find the '" + k + "' column of '" + self.name + "' in the schema cache"
                    raise Exception(f"{{'code': 'PGRST204', 'message': {msg!r}}}")
            row = copy.deepcopy(payload)
            self.store[self.name].append(row)
            return SimpleNamespace(data=[copy.deepcopy(row)])


class _FakeSupabaseClient:
    def __init__(self, store, schemas):
        self.store = store
        self.schemas = schemas

    def table(self, name):
        return _FakePostgrestTable(self.store, name, self.schemas[name])


# =============================================================================
# DEF-32-001: Live Pre-009 Schema Compatibility & Atomic Handover Rollback
# =============================================================================
def test_def001_lifecycle_works_on_live_pre009_schema(monkeypatch):
    import services.account_lifecycle as alc
    import services.cache as cache_mod
    from services.roles import SOLE_ADMIN_UUID, SOLE_ADMIN_EMAIL

    alc._UNSUPPORTED_COLS_CACHE.clear()
    cache_mod._MEMO_STORE.clear() if hasattr(cache_mod, "_MEMO_STORE") else None
    live_schemas = {
        "profiles": {
            "id", "email", "role", "full_name", "phone", "district", "state",
            "profile_data", "is_active", "created_at", "updated_at", "account_status",
            "archived_at", "deletion_requested_at", "deletion_scheduled_for", "legal_hold",
            "restored_at", "status_reason", "reactivated_at", "deleted_at", "grace_period_days",
        },
        "account_lifecycle_log": {
            "id", "user_id", "actor_id", "action", "old_status",
            "new_status", "reason", "details", "ip_address", "created_at",
        },
        "relationships": {"aspirant_id", "guide_id", "guide_ids", "sme_id", "sme_ids", "status", "updated_at"},
    }
    store = {
        "profiles": [
            {"id": SOLE_ADMIN_UUID, "email": SOLE_ADMIN_EMAIL, "role": "admin", "full_name": "Admin", "account_status": "ACTIVE", "is_active": True},
            {"id": "qa_v", "email": "v@test.in", "role": "aspirant", "full_name": "QA V", "account_status": "ACTIVE", "is_active": True, "legal_hold": False},
        ],
        "account_lifecycle_log": [],
        "relationships": [],
    }
    fake_sb = _FakeSupabaseClient(store, live_schemas)

    monkeypatch.setattr(alc, "get_data_backend", lambda: "supabase")
    monkeypatch.setattr(alc, "get_supabase_admin_client", lambda: fake_sb)
    monkeypatch.setattr(alc, "get_supabase_client", lambda: fake_sb)
    monkeypatch.setattr(alc, "require_sole_admin", lambda actor_id=None: (True, None))
    monkeypatch.setattr(alc, "is_strict_admin", lambda **kw: str(kw.get("user_id") or "") == SOLE_ADMIN_UUID)
    monkeypatch.setattr("services.profiles.get_profile", lambda uid: next((p for p in store["profiles"] if p["id"] == uid), None))
    monkeypatch.setattr("services.relationships.get_all_relationships", lambda: [])
    monkeypatch.setattr("services.notifications.create_notification", lambda **kw: ({}, None))

    # 1. Suspend & Resume
    ok_s, err_s = alc.suspend_account("qa_v", "Compliance check", actor_id=SOLE_ADMIN_UUID)
    assert ok_s is True, err_s
    st_s = alc.get_account_status("qa_v")
    assert st_s["account_status"] == "TEMPORARILY_SUSPENDED"
    assert st_s["lifecycle_reason"] == "Compliance check"

    ok_r, err_r = alc.resume_account("qa_v", actor_id=SOLE_ADMIN_UUID, reason="Cleared")
    assert ok_r is True, err_r
    assert alc.get_account_status("qa_v")["account_status"] == "ACTIVE"

    # 2. Legal hold & Scheduled deletion guard
    ok_lh, err_lh = alc.set_legal_hold("qa_v", True, "Audit retention", actor_id=SOLE_ADMIN_UUID)
    assert ok_lh is True, err_lh
    ok_del_blk, _ = alc.request_account_deletion("qa_v", actor_id=SOLE_ADMIN_UUID, reason="Should block")
    assert ok_del_blk is False

    ok_lh2, err_lh2 = alc.set_legal_hold("qa_v", False, "Hold lifted", actor_id=SOLE_ADMIN_UUID)
    assert ok_lh2 is True, err_lh2
    ok_del, err_del = alc.request_account_deletion("qa_v", actor_id=SOLE_ADMIN_UUID, reason="Owner request")
    assert ok_del is True, err_del
    assert alc.get_account_status("qa_v")["account_status"] == "PENDING_DELETION"

    ok_cd, err_cd = alc.cancel_account_deletion("qa_v", actor_id=SOLE_ADMIN_UUID, reason="Cancelled")
    assert ok_cd is True, err_cd
    assert alc.get_account_status("qa_v")["account_status"] == "ACTIVE"

    # 3. Archive & Restore
    ok_arc, err_arc = alc.archive_account("qa_v", "Cohort ended", actor_id=SOLE_ADMIN_UUID)
    assert ok_arc is True, err_arc
    assert store["profiles"][1]["archived_at"] is not None
    assert alc.get_account_status("qa_v")["account_status"] == "ARCHIVED"

    ok_rst, err_rst = alc.restore_account("qa_v", actor_id=SOLE_ADMIN_UUID, reason="Rejoined")
    assert ok_rst is True, err_rst
    assert store["profiles"][1]["restored_at"] is not None
    assert alc.get_account_status("qa_v")["account_status"] == "ACTIVE"
    assert len(store["account_lifecycle_log"]) >= 7
    assert store["account_lifecycle_log"][0]["old_status"] is not None


def test_def001_archive_rolls_back_relationships_if_profile_or_log_fails(isolated_local_db, monkeypatch):
    import services.account_lifecycle as alc
    from services.relationships import assign_guide, get_aspirant_mentors
    from services.roles import SOLE_ADMIN_UUID, SOLE_ADMIN_EMAIL

    ldb = isolated_local_db
    ldb.upsert_profile({"id": SOLE_ADMIN_UUID, "email": SOLE_ADMIN_EMAIL, "role": "admin", "full_name": "Admin", "is_active": 1})
    ldb.upsert_profile({"id": "qa_q", "email": "q@test.in", "role": "guide", "full_name": "QA Q", "is_active": 1})
    ldb.upsert_profile({"id": "qa_z", "email": "z@test.in", "role": "aspirant", "full_name": "QA Z", "is_active": 1})
    ldb.upsert_user_role({"user_id": "qa_q", "role": "guide", "status": "active", "granted_by": SOLE_ADMIN_UUID})

    ok_a, err_a = assign_guide("qa_z", "qa_q", admin_id=SOLE_ADMIN_UUID, allow_pending_nda=True)
    assert ok_a is True, err_a

    # Force audit log failure after guide unassignment + profile archival
    monkeypatch.setattr(ldb, "log_account_lifecycle", lambda entry: (_ for _ in ()).throw(RuntimeError("Simulated DB failure")))
    ok_arc, err_arc = alc.archive_account("qa_q", "Should rollback cleanly", actor_id=SOLE_ADMIN_UUID)
    assert ok_arc is False
    assert "rolled back" in (err_arc or "").lower()

    # Profile MUST remain ACTIVE and Q MUST be restored as Z's assigned guide!
    assert alc.get_account_status("qa_q")["account_status"] == "ACTIVE"
    mentors = get_aspirant_mentors("qa_z")
    assert "qa_q" in [g["id"] for g in mentors.get("guides", [])]


# =============================================================================
# DEF-32-002: Hybrid Active Workspace Authorization (Consultations + Journey)
# =============================================================================
def test_def002_hybrid_workspace_consultation_replies_and_roadmap_toggle(isolated_local_db, monkeypatch):
    from services.journey import toggle_event_roadmap_inclusion
    from services.help_requests import guide_respond_request, sme_respond_request, create_request
    from services.roles import SOLE_ADMIN_UUID

    ldb = isolated_local_db
    ldb.upsert_profile({"id": "qa_a", "email": "a@test.in", "role": "aspirant", "full_name": "QA A", "is_active": 1})
    ldb.upsert_profile({"id": "qa_b", "email": "b@test.in", "role": "aspirant", "full_name": "QA B", "is_active": 1})
    ldb.upsert_profile({"id": "qa_t", "email": "t@test.in", "role": "guide", "full_name": "QA T", "is_active": 1})
    ldb.upsert_user_role({"user_id": "qa_a", "role": "guide", "status": "active", "granted_by": SOLE_ADMIN_UUID})
    ldb.upsert_user_role({"user_id": "qa_b", "role": "sme", "status": "active", "granted_by": SOLE_ADMIN_UUID})
    ldb.upsert_user_role({"user_id": "qa_t", "role": "guide", "status": "active", "granted_by": SOLE_ADMIN_UUID})
    ldb.upsert_user_role({"user_id": "qa_t", "role": "aspirant", "status": "active", "granted_by": SOLE_ADMIN_UUID})
    ldb.assign_guide("qa_b", "qa_a", SOLE_ADMIN_UUID, "A guides B")
    ldb.assign_guide("qa_t", "qa_a", SOLE_ADMIN_UUID, "A guides T")
    ldb.assign_sme("qa_t", "qa_b", SOLE_ADMIN_UUID, "B advises T")

    req_g, _ = create_request("qa_b", "Guide Query", "Help", "MEDIUM", "GENERAL", "guide")
    req_s, _ = create_request("qa_t", "SME Query", "GST Help", "MEDIUM", "COMPLIANCE", "sme")

    # Hybrid A switched into Guide workspace even if base role key was stale 'aspirant'
    monkeypatch.setattr(st, "session_state", {
        "user": {"id": "qa_a", "email": "a@test.in", "role": "aspirant"},
        "user_id": "qa_a",
        "role": "aspirant",
        "active_workspace": "guide",
    })
    ok_g, err_g = guide_respond_request(req_g["id"], "qa_a", "IN_PROGRESS", "Hybrid Guide response")
    assert ok_g is True, err_g

    # Hybrid B switched into SME workspace
    monkeypatch.setattr(st, "session_state", {
        "user": {"id": "qa_b", "email": "b@test.in", "role": "aspirant"},
        "user_id": "qa_b",
        "role": "aspirant",
        "active_workspace": "sme",
    })
    ok_s, err_s = sme_respond_request(req_s["id"], "qa_b", "RESOLVED", "Hybrid SME response")
    assert ok_s is True, err_s

    # Forged workspace without active role grant still rejected
    monkeypatch.setattr(st, "session_state", {
        "user": {"id": "qa_b", "email": "b@test.in", "role": "aspirant"},
        "user_id": "qa_b",
        "role": "aspirant",
        "active_workspace": "guide",
    })
    ok_forged, err_forged = guide_respond_request(req_g["id"], "qa_b", "RESOLVED", "Spoof")
    assert ok_forged is False
    assert "Unauthorized" in (err_forged or "")

    # Hybrid T (guide base + aspirant active grant) toggling roadmap in aspirant workspace succeeds
    from services.journey import add_guide_contribution
    ok_c, err_c = add_guide_contribution("qa_t", "qa_a", "Milestone", "Test roadmap item")
    assert ok_c is not None and err_c is None
    ev_id = ok_c["id"]
    monkeypatch.setattr(st, "session_state", {
        "user": {"id": "qa_t", "email": "t@test.in", "role": "guide"},
        "user_id": "qa_t",
        "role": "guide",
        "active_workspace": "aspirant",
    })
    ok_t, err_t = toggle_event_roadmap_inclusion(ev_id, "qa_t", False)
    assert ok_t is True, err_t

    # Explicit guide role caller still denied
    ok_g_den, _ = toggle_event_roadmap_inclusion(ev_id, "qa_t", True, actor_id="qa_t", actor_role="guide")
    assert ok_g_den is False


# =============================================================================
# DEF-32-003, DEF-32-008, DEF-32-009: Admin Provisioning, Defaults & First Login UI
# =============================================================================
def test_def003_def008_def009_ui_contracts_and_delegation(isolated_local_db, monkeypatch):
    import views.admin as admin_view
    from services.constants import MASTER_DISTRICTS_TN
    from services.roles import SOLE_ADMIN_UUID, SOLE_ADMIN_EMAIL
    from services.scheme_reviews import delegate_scheme_to_guide
    from services.notifications import list_notifications

    # DEF-32-003: provisional password helper stays stable across reruns until cleared
    st.session_state.clear()
    p1 = admin_view._get_or_init_provisional_password("test_cg_pwd")
    p2 = admin_view._get_or_init_provisional_password("test_cg_pwd")
    assert p1 == p2 and len(p1) >= 12
    st.session_state.pop("test_cg_pwd")
    p3 = admin_view._get_or_init_provisional_password("test_cg_pwd")
    assert p3 != p1

    # DEF-32-008 checks in views/admin.py & views/aspirant.py
    admin_src = (REPO_ROOT / "views" / "admin.py").read_text(encoding="utf-8")
    assert 'MASTER_DISTRICTS_TN.index("Chennai")' in admin_src
    assert 'Add Co-Guide (Concurrent Multi-Guide)' in admin_src
    assert 'Delegate / Recommend Scheme to Guide' in admin_src
    assert '_render_admin_mentor_edit_expander' in admin_src
    assert MASTER_DISTRICTS_TN.index("Chennai") == 2

    asp_src = (REPO_ROOT / "views" / "aspirant.py").read_text(encoding="utf-8")
    assert "Fulcrum Support Reports (" in asp_src

    # Test delegate_scheme_to_guide end-to-end
    ldb = isolated_local_db
    ldb.upsert_profile({"id": SOLE_ADMIN_UUID, "email": SOLE_ADMIN_EMAIL, "role": "admin", "full_name": "Admin", "is_active": 1})
    ldb.upsert_profile({"id": "qa_d", "email": "d@test.in", "role": "guide", "full_name": "QA D", "is_active": 1})
    ldb.upsert_profile({"id": "qa_f", "email": "f@test.in", "role": "aspirant", "full_name": "QA F", "is_active": 1})
    monkeypatch.setattr("services.schemes.get_scheme", lambda sid: {"id": sid, "name": "NEEDS Scheme"})
    ok_del, err_del = delegate_scheme_to_guide(SOLE_ADMIN_UUID, "SCH-NEEDS", "qa_d", "Evaluate capital grant.", aspirant_id="qa_f", priority="HIGH")
    assert ok_del is True, err_del
    notifs = list_notifications("qa_d")
    assert any("NEEDS Scheme" in n.get("title", "") for n in notifs)

    # DEF-32-009: app.py first-login gate enforces >= 8 chars matching backend
    app_src = (REPO_ROOT / "app.py").read_text(encoding="utf-8")
    assert "len(np1) < 8" in app_src
    assert "len(np1) < 6" not in app_src


# =============================================================================
# DEF-32-004: Multi-Role Aspirant Pagination & KPI Inclusion
# =============================================================================
def test_def004_hybrid_aspirants_included_and_deduped_in_directory_and_kpi(isolated_local_db):
    from services.pagination import paginate_profiles
    from services.admin_metrics import get_admin_dashboard_metrics
    from services.roles import SOLE_ADMIN_UUID, SOLE_ADMIN_EMAIL

    ldb = isolated_local_db
    ldb.upsert_profile({"id": SOLE_ADMIN_UUID, "email": SOLE_ADMIN_EMAIL, "role": "admin", "full_name": "Admin", "is_active": 1})
    ldb.upsert_profile({"id": "qa_f", "email": "f@test.in", "role": "aspirant", "full_name": "QA F", "is_active": 1})
    ldb.upsert_profile({"id": "qa_t", "email": "t@test.in", "role": "guide", "full_name": "QA T", "is_active": 1})
    ldb.upsert_profile({"id": "qa_u", "email": "u@test.in", "role": "sme", "full_name": "QA U", "is_active": 1})
    ldb.upsert_profile({"id": "qa_pure_g", "email": "pg@test.in", "role": "guide", "full_name": "Pure Guide", "is_active": 1})
    ldb.upsert_user_role({"user_id": "qa_t", "role": "guide", "status": "active", "granted_by": SOLE_ADMIN_UUID})
    ldb.upsert_user_role({"user_id": "qa_t", "role": "aspirant", "status": "active", "granted_by": SOLE_ADMIN_UUID})
    ldb.upsert_user_role({"user_id": "qa_u", "role": "sme", "status": "active", "granted_by": SOLE_ADMIN_UUID})
    ldb.upsert_user_role({"user_id": "qa_u", "role": "aspirant", "status": "active", "granted_by": SOLE_ADMIN_UUID})
    ldb.upsert_user_role({"user_id": "qa_f", "role": "aspirant", "status": "active", "granted_by": SOLE_ADMIN_UUID})

    rows, total = paginate_profiles(role="aspirant", page=1, page_size=50)
    ids = [r["id"] for r in rows]
    assert set(ids) == {"qa_f", "qa_t", "qa_u"}
    assert total == 3
    assert len(ids) == 3  # Strictly deduplicated

    metrics = get_admin_dashboard_metrics(SOLE_ADMIN_UUID)
    assert metrics["aspirants_count"] == 3


# =============================================================================
# DEF-32-005: Conflict of Interest Approved/Cleared State Lifecycle
# =============================================================================
def test_def005_coi_approval_and_clearance_lifecycle(isolated_local_db):
    from services.governance import declare_sme_conflict, resolve_sme_conflict, check_sme_has_conflict, list_sme_conflicts
    from services.relationships import assign_sme, unassign_sme
    from services.admin_metrics import get_admin_dashboard_metrics
    from services.roles import SOLE_ADMIN_UUID, SOLE_ADMIN_EMAIL

    ldb = isolated_local_db
    ldb.upsert_profile({"id": SOLE_ADMIN_UUID, "email": SOLE_ADMIN_EMAIL, "role": "admin", "full_name": "Admin", "is_active": 1})
    ldb.upsert_profile({"id": "qa_c", "email": "c@test.in", "role": "aspirant", "full_name": "QA C", "is_active": 1})
    ldb.upsert_profile({"id": "qa_p", "email": "p@test.in", "role": "sme", "full_name": "QA P", "is_active": 1})
    ldb.upsert_user_role({"user_id": "qa_p", "role": "sme", "status": "active", "granted_by": SOLE_ADMIN_UUID})

    assert assign_sme("qa_c", "qa_p", admin_id=SOLE_ADMIN_UUID, allow_pending_nda=True)[0] is True
    assert declare_sme_conflict("qa_p", "qa_c", True, "Vendor overlap")[0] is True
    assert get_admin_dashboard_metrics(SOLE_ADMIN_UUID)["open_conflicts_count"] == 1

    cid = list_sme_conflicts(sme_id="qa_p", aspirant_id="qa_c")[0]["id"]
    assert unassign_sme("qa_c", "qa_p", admin_id=SOLE_ADMIN_UUID, reason="Recusal approved")[0] is True
    ok_res, err_res = resolve_sme_conflict(cid, SOLE_ADMIN_UUID, "APPROVED")
    assert ok_res is True, err_res

    updated_c = list_sme_conflicts(sme_id="qa_p", aspirant_id="qa_c")[0]
    assert updated_c["status"] == "APPROVED"
    assert updated_c["reviewed_by"] == SOLE_ADMIN_UUID
    assert get_admin_dashboard_metrics(SOLE_ADMIN_UUID)["open_conflicts_count"] == 0
    assert check_sme_has_conflict("qa_p", "qa_c") is True

    # Lift restriction -> permits re-assignment cleanly
    ok_clr, err_clr = resolve_sme_conflict(cid, SOLE_ADMIN_UUID, "REJECTED")
    assert ok_clr is True, err_clr
    assert check_sme_has_conflict("qa_p", "qa_c") is False
    assert assign_sme("qa_c", "qa_p", admin_id=SOLE_ADMIN_UUID, allow_pending_nda=True)[0] is True


# =============================================================================
# DEF-32-006: Aspirant Profile Save Preserves Mentor Metadata
# =============================================================================
def test_def006_aspirant_save_preserves_existing_mentor_profile_data(isolated_local_db):
    from services.profiles import update_aspirant_profile, get_profile

    ldb = isolated_local_db
    ldb.upsert_profile({
        "id": "qa_u",
        "email": "u@test.in",
        "role": "sme",
        "full_name": "QA U",
        "district": "Chennai",
        "is_active": 1,
        "profile_data": {
            "expertise": "GST Compliance & Export Law",
            "bio": "15 years practice",
            "industry": "Textiles & Exports",
            "temp_password_issued": False,
        },
    })

    upd, err = update_aspirant_profile(
        user_id="qa_u",
        full_name="QA U",
        phone="9876543210",
        district="Chennai",
        personal_data={"gender": "Female"},
        professional_data={"education": "CA"},
        business_data={"business_name": "U Advisory Tech", "sector": "FinTech"},
        demographics_data={"district": "Chennai"},
        assistance_need_data={"assistance_goal": "Market Access"},
        actor_id="qa_u",
    )
    assert upd is not None and err is None
    saved_pd = get_profile("qa_u")["profile_data"]
    assert saved_pd["expertise"] == "GST Compliance & Export Law"
    assert saved_pd["bio"] == "15 years practice"
    assert saved_pd["industry"] == "Textiles & Exports"
    assert saved_pd["business"]["business_name"] == "U Advisory Tech"


# =============================================================================
# DEF-32-007: Co-Guide #2 Relationship Array Auth & Peer Mentor Visibility
# =============================================================================
def test_def007_coguide_array_auth_allows_assigned_sme_and_denies_unrelated(monkeypatch):
    import services.profiles as prof_mod

    rel_row = {
        "aspirant_id": "qa_b",
        "guide_id": "qa_a",
        "guide_ids": ["qa_a", "qa_e"],  # Co-Guide #2 qa_e is NOT scalar guide_id
        "sme_id": "qa_c",
        "sme_ids": ["qa_c"],
        "status": "active",
    }
    captured_filters = []

    class _RelQuery:
        def select(self, *a, **k): return self
        def eq(self, *a, **k): return self
        def or_(self, expr):
            captured_filters.append(expr)
            return self
        def execute(self):
            return SimpleNamespace(data=[rel_row])

    mock_admin = MagicMock()
    mock_admin.table.return_value = _RelQuery()

    auth_ids = prof_mod._get_relationship_authorized_ids_supabase(mock_admin, "qa_e")
    assert any("guide_ids.cs.{qa_e}" in f and "sme_ids.cs.{qa_e}" in f for f in captured_filters)
    assert "qa_b" in auth_ids
    assert "qa_a" in auth_ids
    assert "qa_c" in auth_ids
    assert "unrelated_user" not in auth_ids


# =============================================================================
# DEF-32-010: Workspace-Scoped Notifications & Role Badge Binding
# =============================================================================
def test_def010_workspace_notification_isolation(isolated_local_db):
    from services.notifications import (
        filter_notifications_by_workspace,
        infer_notification_workspace,
        is_notification_allowed,
    )
    from services.roles import SOLE_ADMIN_UUID

    n_guide = {"id": "1", "notification_type": "guide_assigned", "title": "New Mentee Assigned", "message": "You have been assigned"}
    n_sme = {"id": "2", "notification_type": "help_ticket_created", "title": "[Domain SME] New Ticket", "message": "Needs GST advice"}
    n_asp = {"id": "3", "notification_type": "scheme_released", "title": "Scheme Unlocked", "message": "Review TANSEED"}
    n_sys = {"id": "4", "notification_type": "account_resumed", "title": "Account Access Restored", "message": "Active"}

    assert infer_notification_workspace(n_guide) == "guide"
    assert infer_notification_workspace(n_sme) == "sme"
    assert infer_notification_workspace(n_asp) == "aspirant"
    assert infer_notification_workspace(n_sys) == "all"

    all_n = [n_guide, n_sme, n_asp, n_sys]
    sme_only = filter_notifications_by_workspace(all_n, "sme")
    assert {x["id"] for x in sme_only} == {"2", "4"}
    guide_only = filter_notifications_by_workspace(all_n, "guide")
    assert {x["id"] for x in guide_only} == {"1", "4"}

    # Hybrid user with base role='guide' and active 'aspirant' grant can notify assigned guide
    ldb = isolated_local_db
    ldb.upsert_profile({"id": "qa_t", "email": "t@test.in", "role": "guide", "full_name": "QA T", "is_active": 1})
    ldb.upsert_profile({"id": "qa_a", "email": "a@test.in", "role": "aspirant", "full_name": "QA A", "is_active": 1})
    ldb.upsert_profile({"id": "qa_stranger", "email": "s@test.in", "role": "aspirant", "full_name": "Stranger", "is_active": 1})
    ldb.upsert_user_role({"user_id": "qa_t", "role": "aspirant", "status": "active", "granted_by": SOLE_ADMIN_UUID})
    ldb.upsert_user_role({"user_id": "qa_a", "role": "guide", "status": "active", "granted_by": SOLE_ADMIN_UUID})
    ldb.assign_guide("qa_t", "qa_a", SOLE_ADMIN_UUID)

    assert is_notification_allowed("qa_t", "qa_a", "help_ticket_created") is True
    assert is_notification_allowed("qa_t", "qa_stranger", "system_alert") is False

    app_src = (REPO_ROOT / "app.py").read_text(encoding="utf-8")
    assert "role_badges.get(curr_ws" in app_src
    assert 'st.session_state["role"] = selected_ws' in app_src


def test_def001_lifecycle_works_on_migration_009_schema(monkeypatch):
    import services.account_lifecycle as alc
    import services.cache as cache_mod
    from services.roles import SOLE_ADMIN_UUID, SOLE_ADMIN_EMAIL

    alc._UNSUPPORTED_COLS_CACHE.clear()
    cache_mod._MEMO_STORE.clear() if hasattr(cache_mod, "_MEMO_STORE") else None
    schemas_009 = {
        "profiles": {
            "id", "email", "role", "full_name", "is_active", "updated_at",
            "account_status", "legal_hold", "lifecycle_reason", "status_updated_at",
            "status_updated_by", "deletion_requested_at", "deletion_requested_by",
            "deletion_scheduled_for", "retention_notes",
        },
        "account_lifecycle_log": {
            "id", "user_id", "actor_id", "action", "previous_status",
            "new_status", "reason", "metadata", "created_at",
        },
    }
    store = {
        "profiles": [
            {"id": SOLE_ADMIN_UUID, "email": SOLE_ADMIN_EMAIL, "role": "admin", "account_status": "ACTIVE", "is_active": True},
            {"id": "qa_ac", "email": "ac@test.in", "role": "aspirant", "account_status": "ACTIVE", "is_active": True, "legal_hold": False},
        ],
        "account_lifecycle_log": [],
    }
    fake_sb = _FakeSupabaseClient(store, schemas_009)
    monkeypatch.setattr(alc, "get_data_backend", lambda: "supabase")
    monkeypatch.setattr(alc, "get_supabase_admin_client", lambda: fake_sb)
    monkeypatch.setattr(alc, "get_supabase_client", lambda: fake_sb)
    monkeypatch.setattr(alc, "require_sole_admin", lambda actor_id=None: (True, None))
    monkeypatch.setattr(alc, "is_strict_admin", lambda **kw: str(kw.get("user_id") or "") == SOLE_ADMIN_UUID)
    monkeypatch.setattr("services.profiles.get_profile", lambda uid: next((p for p in store["profiles"] if p["id"] == uid), None))
    monkeypatch.setattr("services.relationships.get_all_relationships", lambda: [])
    monkeypatch.setattr("services.notifications.create_notification", lambda **kw: ({}, None))

    ok_s, err_s = alc.suspend_account("qa_ac", "009 check", actor_id=SOLE_ADMIN_UUID)
    assert ok_s is True, err_s
    assert store["profiles"][1]["lifecycle_reason"] == "009 check"
    assert store["account_lifecycle_log"][0]["previous_status"] == "ACTIVE"


def test_def004_supabase_mode_paginate_profiles_and_metrics(monkeypatch):
    import services.pagination as pag
    import services.admin_metrics as adm
    import services.cache as cache_mod
    from services.roles import SOLE_ADMIN_UUID

    cache_mod._MEMO_STORE.clear() if hasattr(cache_mod, "_MEMO_STORE") else None
    schemas = {
        "profiles": {"id", "email", "role", "full_name", "district", "is_active", "created_at"},
        "user_roles": {"id", "user_id", "role", "status"},
        "journeys": {"id", "status"},
        "help_requests": {"id", "request_type", "status"},
        "schemes": {"id"},
        "guide_complaints": {"id", "status"},
        "scheme_support_reviews": {"id", "status"},
        "sme_conflict_declarations": {"id", "has_conflict", "status"},
    }
    store = {
        "profiles": [
            {"id": "qa_f", "email": "f@test.in", "role": "aspirant", "full_name": "QA F", "district": "Chennai", "is_active": True, "created_at": "2026-11-11T01:00:00Z"},
            {"id": "qa_t", "email": "t@test.in", "role": "guide", "full_name": "QA T", "district": "Madurai", "is_active": True, "created_at": "2026-11-11T02:00:00Z"},
            {"id": "qa_u", "email": "u@test.in", "role": "sme", "full_name": "QA U", "district": "Chennai", "is_active": True, "created_at": "2026-11-11T03:00:00Z"},
            {"id": SOLE_ADMIN_UUID, "email": "fulcrumindia1@gmail.com", "role": "admin", "full_name": "Admin", "district": "Chennai", "is_active": True, "created_at": "2026-11-11T00:00:00Z"},
        ],
        "user_roles": [
            {"id": "ur1", "user_id": "qa_f", "role": "aspirant", "status": "active"},
            {"id": "ur2", "user_id": "qa_t", "role": "aspirant", "status": "active"},
            {"id": "ur3", "user_id": "qa_u", "role": "aspirant", "status": "active"},
        ],
        "journeys": [],
        "help_requests": [],
        "schemes": [],
        "guide_complaints": [],
        "scheme_support_reviews": [],
        "sme_conflict_declarations": [],
    }
    fake_sb = _FakeSupabaseClient(store, schemas)
    monkeypatch.setattr(pag, "get_data_backend", lambda: "supabase")
    monkeypatch.setattr(pag, "get_supabase_admin_client", lambda: fake_sb)
    monkeypatch.setattr(adm, "get_data_backend", lambda: "supabase")
    monkeypatch.setattr(adm, "get_supabase_admin_client", lambda: fake_sb)
    monkeypatch.setattr(adm, "require_sole_admin", lambda actor_id=None: (True, None))

    rows, total = pag.paginate_profiles(role="aspirant", page=1, page_size=25)
    assert total == 3
    assert {r["id"] for r in rows} == {"qa_f", "qa_t", "qa_u"}

    metrics = adm.get_admin_dashboard_metrics(SOLE_ADMIN_UUID)
    assert metrics["aspirants_count"] == 3


def test_help_requests_adaptive_status_fallback_and_migration_011(monkeypatch):
    """Verify Guide/SME/Aspirant replies survive un-migrated help_requests_status_check (23514) and Migration 011 defines all statuses."""
    import services.help_requests as hr
    import services.cache as cache_mod
    from services.roles import SOLE_ADMIN_UUID

    mig_011 = (REPO_ROOT / "migrations" / "011_expand_help_requests_status_check.sql").read_text(encoding="utf-8")
    for s_val in ("WAITING_ON_ASPIRANT", "WAITING_ON_GUIDE_SME", "ACTION_REQUIRED", "REPLIED", "IN_PROGRESS", "RESOLVED"):
        assert s_val in mig_011

    cache_mod._MEMO_STORE.clear() if hasattr(cache_mod, "_MEMO_STORE") else None

    class _StatusCheckFakeQuery:
        def __init__(self, tbl_name, rows, allowed_statuses):
            self._tbl = tbl_name
            self._rows = rows
            self._allowed = allowed_statuses
            self._op = "select"
            self._payload = None
            self._filters = []

        def select(self, *args, **kwargs):
            self._op = "select"
            return self

        def update(self, payload):
            self._op = "update"
            self._payload = dict(payload)
            return self

        def eq(self, k, v):
            self._filters.append((k, v))
            return self

        def execute(self):
            matched = [r for r in self._rows if all(str(r.get(k)) == str(v) for k, v in self._filters)]
            if self._op == "update":
                if self._tbl == "help_requests":
                    st_val = self._payload.get("status")
                    if st_val and st_val not in self._allowed:
                        raise Exception(
                            "{'message': 'new row for relation \"help_requests\" violates check constraint \"help_requests_status_check\"', 'code': '23514'}"
                        )
                for r in matched:
                    r.update(self._payload)
                return type("R", (), {"data": [dict(r) for r in matched]})()
            return type("R", (), {"data": [dict(r) for r in matched]})()

    class _StatusCheckFakeSB:
        def __init__(self, rows, allowed_statuses):
            self._rows = rows
            self._allowed = allowed_statuses

        def table(self, name):
            return _StatusCheckFakeQuery(name, self._rows, self._allowed)

    legacy_allowed = {"OPEN", "IN_PROGRESS", "RESOLVED", "ESCALATED", "PENDING_ADMIN", "DIRECTIVE_ISSUED"}
    rows = [
        {"id": "req-g", "aspirant_id": "qa_b", "assigned_guide_id": "qa_a", "assigned_sme_id": None, "subject": "G", "status": "OPEN", "guide_response": None},
        {"id": "req-s", "aspirant_id": "qa_b", "assigned_guide_id": None, "assigned_sme_id": "qa_c", "subject": "S", "status": "OPEN", "sme_response": None},
        {"id": "req-a", "aspirant_id": "qa_b", "assigned_guide_id": "qa_a", "assigned_sme_id": None, "subject": "A", "status": "OPEN", "aspirant_response": None},
    ]
    fake_legacy_sb = _StatusCheckFakeSB(rows, legacy_allowed)

    st.session_state.clear()
    monkeypatch.setattr(hr, "get_data_backend", lambda: "supabase")
    monkeypatch.setattr(hr, "_get_user_client", lambda: fake_legacy_sb)
    monkeypatch.setattr(hr, "_get_admin_client", lambda: fake_legacy_sb)
    monkeypatch.setattr("services.account_lifecycle.get_account_status", lambda uid: {"account_status": "ACTIVE"})
    monkeypatch.setattr("services.governance.check_sme_has_conflict", lambda s, a: False)
    monkeypatch.setattr("services.notifications.create_notification", lambda **kw: ({}, None))

    # Guide reply with WAITING_ON_ASPIRANT (UI default) succeeds under legacy DB constraint
    ok_g, err_g = hr.guide_respond_request("req-g", "qa_a", "WAITING_ON_ASPIRANT", "Guide action items")
    assert ok_g is True, err_g
    assert rows[0]["status"] == "IN_PROGRESS"
    assert rows[0]["guide_response"] == "Guide action items"
    assert rows[0]["last_interaction_actor_role"] == "guide"

    # SME reply with WAITING_ON_ASPIRANT succeeds under legacy DB constraint
    ok_s, err_s = hr.sme_respond_request("req-s", "qa_c", "WAITING_ON_ASPIRANT", "SME GST guidance")
    assert ok_s is True, err_s
    assert rows[1]["status"] == "IN_PROGRESS"
    assert rows[1]["sme_response"] == "SME GST guidance"

    # Aspirant reply (WAITING_ON_GUIDE_SME) preserves aspirant_response rather than falling back to admin_response
    ok_a, err_a = hr.aspirant_respond_request("req-a", "qa_b", "Founder follow-up docs attached")
    assert ok_a is True, err_a
    assert rows[2]["status"] == "IN_PROGRESS"
    assert rows[2]["aspirant_response"] == "Founder follow-up docs attached"
    assert rows[2].get("admin_response") is None

    # After Migration 011 is applied, WAITING_ON_ASPIRANT persists natively
    expanded_allowed = legacy_allowed | {"WAITING_ON_ASPIRANT", "WAITING_ON_GUIDE_SME", "ACTION_REQUIRED", "REPLIED"}
    fake_011_sb = _StatusCheckFakeSB(rows, expanded_allowed)
    monkeypatch.setattr(hr, "_get_user_client", lambda: fake_011_sb)
    monkeypatch.setattr(hr, "_get_admin_client", lambda: fake_011_sb)
    ok_g2, err_g2 = hr.guide_respond_request("req-g", "qa_a", "WAITING_ON_ASPIRANT", "Please upload incorporation cert")
    assert ok_g2 is True, err_g2
    assert rows[0]["status"] == "WAITING_ON_ASPIRANT"



