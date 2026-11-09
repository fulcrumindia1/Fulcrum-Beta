"""
services/collaboration.py — Case Discussions & Private Advisory Notes
=====================================================================
Provides unified case collaboration between Aspirant, assigned Guide, and assigned SME.
Supports:
  - Open case discussions (visible to Aspirant, Guide, SME, Admin)
  - Private mentor advisory notes (visible only to Guide, SME, Admin; hidden from Aspirant)
"""

import json
from datetime import datetime, timezone
from typing import Optional, Dict, List, Tuple
from services.auth import get_supabase_client, get_supabase_admin_client, get_data_backend
from services.local_db import get_local_db
from services.cache import get_memo, set_memo, invalidate_memo


def create_case_message(
    aspirant_id: str,
    author_id: str,
    author_role: str,
    title: str,
    message: str,
    is_private_mentor_note: bool = False,
    attachments: Optional[List[str]] = None
) -> Tuple[bool, Optional[str]]:
    """Creates a new case discussion message or private mentor note."""
    if not author_id or not str(author_id).strip():
        return False, "Author identity is required."
    if not aspirant_id or not str(aspirant_id).strip():
        return False, "Entrepreneur ID is required."
    if not title or not message:
        return False, "Title and message cannot be empty."

    # Only guides, SMEs and admins can post private mentor notes
    if is_private_mentor_note:
        if author_role not in ("guide", "sme", "admin"):
            return False, "Entrepreneurs cannot create private mentor notes."

        from services.governance import get_primary_admin_id
        from services.roles import is_strict_admin, user_has_active_role
        from services.legal import check_user_nda_accepted

        primary_admin_id = str(get_primary_admin_id() or "")
        is_admin = (primary_admin_id and str(author_id) == primary_admin_id) or is_strict_admin(user_id=str(author_id)) or user_has_active_role(str(author_id), "admin")

        if not is_admin:
            # Must be an assigned mentor with active status and accepted NDA
            from services.relationships import get_all_relationships
            rels = get_all_relationships()
            assigned_rel = next((r for r in rels if str(r.get("aspirant_id")) == str(aspirant_id) and r.get("status") == "active"), None)
            if not assigned_rel:
                return False, "Unauthorized: No active mentorship relationship exists for this entrepreneur."

            raw_gids = assigned_rel.get("guide_ids") or []
            if isinstance(raw_gids, str):
                try: raw_gids = json.loads(raw_gids)
                except Exception: raw_gids = [raw_gids]
            if not isinstance(raw_gids, list):
                raw_gids = []
            if assigned_rel.get("guide_id"):
                raw_gids.append(str(assigned_rel["guide_id"]))
            for g in assigned_rel.get("guides", []):
                if isinstance(g, dict) and g.get("id"):
                    raw_gids.append(str(g["id"]))
            guides_list = [str(gid) for gid in raw_gids if gid]

            raw_sids = assigned_rel.get("sme_ids") or []
            if isinstance(raw_sids, str):
                try: raw_sids = json.loads(raw_sids)
                except Exception: raw_sids = [raw_sids]
            if not isinstance(raw_sids, list):
                raw_sids = []
            if assigned_rel.get("sme_id"):
                raw_sids.append(str(assigned_rel["sme_id"]))
            for s in assigned_rel.get("smes", []):
                if isinstance(s, dict) and s.get("id"):
                    raw_sids.append(str(s["id"]))
            smes_list = [str(sid) for sid in raw_sids if sid]

            str_author = str(author_id)
            if str_author not in guides_list and str_author not in smes_list:
                return False, "Unauthorized: Only mentors actively assigned to this entrepreneur may author private advisory notes."

            if str_author in guides_list and not check_user_nda_accepted(str_author, "guide"):
                return False, "Unauthorized: Mentor NDA is required before posting private advisory notes."
            if str_author in smes_list and not check_user_nda_accepted(str_author, "sme"):
                return False, "Unauthorized: SME NDA is required before posting private advisory notes."

    import uuid
    msg_id = str(uuid.uuid4())
    now_iso = datetime.now(timezone.utc).isoformat()

    record = {
        "id": msg_id,
        "aspirant_id": aspirant_id,
        "author_id": author_id,
        "author_role": author_role,
        "title": title.strip(),
        "message": message.strip(),
        "attachments": attachments or [],
        "is_private_mentor_note": is_private_mentor_note,
        "created_at": now_iso
    }

    backend = get_data_backend()
    if backend == "supabase":
        client = get_supabase_admin_client() or get_supabase_client()
        if not client:
            return False, "Supabase connection is not available."
        try:
            client.table("case_discussions").insert(record).execute()
        except Exception as e:
            return False, f"Failed to persist case message in Supabase: {e}"
    else:
        db = get_local_db()
        if hasattr(db, "insert_case_discussion"):
            db.insert_case_discussion(record)

    invalidate_memo(f"case_discussions:{aspirant_id}")
    return True, None


def list_case_messages(
    aspirant_id: str,
    requesting_role: str = "aspirant",
    viewer_id: Optional[str] = None
) -> List[Dict]:
    """
    Retrieves case messages for an entrepreneur.
    Strictly gates private mentor advisory notes:
      - Visible ONLY to Platform Admin or active, NDA-certified mentors assigned to this entrepreneur.
      - Hidden from Aspirants and unassigned third parties regardless of requesting_role argument.
    """
    if not aspirant_id:
        return []

    # Resolve viewer_id from session context if not explicitly provided
    effective_viewer = viewer_id
    if effective_viewer is None:
        try:
            import streamlit as st
            effective_viewer = st.session_state.get("user_id") or st.session_state.get("user", {}).get("id")
        except Exception:
            pass

    can_view_private = False
    if effective_viewer:
        from services.governance import get_primary_admin_id
        from services.roles import is_strict_admin, user_has_active_role
        from services.legal import check_user_nda_accepted

        primary_admin_id = str(get_primary_admin_id() or "")
        is_admin = (primary_admin_id and str(effective_viewer) == primary_admin_id) or is_strict_admin(user_id=str(effective_viewer)) or user_has_active_role(str(effective_viewer), "admin")

        if is_admin:
            can_view_private = (requesting_role != "aspirant")
        elif str(effective_viewer) == str(aspirant_id):
            can_view_private = False
        else:
            # Check mentor assignment and NDA status
            from services.relationships import get_all_relationships
            rels = get_all_relationships()
            assigned_rel = next((r for r in rels if str(r.get("aspirant_id")) == str(aspirant_id) and r.get("status") == "active"), None)
            if assigned_rel:
                raw_gids = assigned_rel.get("guide_ids") or []
                if isinstance(raw_gids, str):
                    try: raw_gids = json.loads(raw_gids)
                    except Exception: raw_gids = [raw_gids]
                if not isinstance(raw_gids, list):
                    raw_gids = []
                if assigned_rel.get("guide_id"):
                    raw_gids.append(str(assigned_rel["guide_id"]))
                for g in assigned_rel.get("guides", []):
                    if isinstance(g, dict) and g.get("id"):
                        raw_gids.append(str(g["id"]))
                guides_list = [str(gid) for gid in raw_gids if gid]

                raw_sids = assigned_rel.get("sme_ids") or []
                if isinstance(raw_sids, str):
                    try: raw_sids = json.loads(raw_sids)
                    except Exception: raw_sids = [raw_sids]
                if not isinstance(raw_sids, list):
                    raw_sids = []
                if assigned_rel.get("sme_id"):
                    raw_sids.append(str(assigned_rel["sme_id"]))
                for s in assigned_rel.get("smes", []):
                    if isinstance(s, dict) and s.get("id"):
                        raw_sids.append(str(s["id"]))
                smes_list = [str(sid) for sid in raw_sids if sid]

                str_v = str(effective_viewer)
                if str_v in guides_list and check_user_nda_accepted(str_v, "guide"):
                    can_view_private = (requesting_role != "aspirant")
                elif str_v in smes_list and check_user_nda_accepted(str_v, "sme"):
                    can_view_private = (requesting_role != "aspirant")
    else:
        # No authenticated viewer session — STRICT FAIL CLOSED: NEVER allow private notes!
        can_view_private = False

    cache_key = f"case_discussions:{aspirant_id}:{requesting_role}:{effective_viewer}:{can_view_private}"
    cached = get_memo(cache_key)
    if cached is not None:
        return cached

    backend = get_data_backend()
    records = []

    if backend == "supabase":
        client = get_supabase_admin_client() or get_supabase_client()
        if client:
            try:
                q = client.table("case_discussions").select("*").eq("aspirant_id", aspirant_id).order("created_at", desc=False)
                if not can_view_private:
                    q = q.eq("is_private_mentor_note", False)
                res = q.execute()
                records = res.data or []
            except Exception as e:
                print(f"[Collaboration] Supabase query notice: {e}")
                records = []
    else:
        db = get_local_db()
        if hasattr(db, "list_case_discussions"):
            records = db.list_case_discussions(aspirant_id=aspirant_id, include_private=can_view_private)

    # Fail-closed defense-in-depth: guarantee no private note leaks if unauthorized
    if not can_view_private:
        records = [r for r in records if not r.get("is_private_mentor_note")]

    # Attach author profile details
    from services.profiles import get_profile
    for r in records:
        author = get_profile(r.get("author_id", ""))
        r["author_name"] = author.get("full_name", "Team Member") if author else "Team Member"

    set_memo(cache_key, records, ttl_seconds=30)
    return records

