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
    if not title or not message:
        return False, "Title and message cannot be empty."

    # Only guides, SMEs and admins can post private mentor notes
    if is_private_mentor_note and author_role not in ("guide", "sme", "admin", "district_admin", "operational_admin"):
        return False, "Entrepreneurs cannot create private mentor notes."

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
        if client:
            try:
                client.table("case_discussions").insert(record).execute()
            except Exception:
                pass

    db = get_local_db()
    if hasattr(db, "insert_case_discussion"):
        db.insert_case_discussion(record)

    invalidate_memo(f"case_discussions:{aspirant_id}")
    return True, None


def list_case_messages(
    aspirant_id: str,
    requesting_role: str = "aspirant"
) -> List[Dict]:
    """
    Retrieves case messages for an entrepreneur.
    Gating:
      If requesting_role is 'aspirant', filters out 'is_private_mentor_note' == True!
    """
    if not aspirant_id:
        return []

    cache_key = f"case_discussions:{aspirant_id}:{requesting_role}"
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
                if requesting_role == "aspirant":
                    q = q.eq("is_private_mentor_note", False)
                res = q.execute()
                records = res.data or []
            except Exception:
                pass

    if not records:
        db = get_local_db()
        if hasattr(db, "list_case_discussions"):
            include_private = (requesting_role != "aspirant")
            records = db.list_case_discussions(aspirant_id=aspirant_id, include_private=include_private)

    # Attach author profile details
    from services.profiles import get_profile
    for r in records:
        author = get_profile(r.get("author_id", ""))
        r["author_name"] = author.get("full_name", "Team Member") if author else "Team Member"

    set_memo(cache_key, records, ttl_seconds=30)
    return records

