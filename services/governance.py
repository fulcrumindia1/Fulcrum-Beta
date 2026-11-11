"""
services/governance.py — Institutional Governance, Super Admin Masking, Complaints & SME Conflict
==================================================================================================
Implements:
1. Super Admin Identity Masking ("Fulcrum Administration")
2. Confidential Guide Complaints / Reassignment Requests
3. SME Directory & Conflict of Interest Governance
"""

import json
from datetime import datetime, timezone
from typing import Optional, Dict, List, Tuple
from services.auth import get_supabase_client, get_supabase_admin_client, get_data_backend
from services.local_db import get_local_db
from services.cache import (
    get_memo, set_memo, invalidate_memo,
    get_global_cache, set_global_cache
)

# Governance Masking Names
ADMIN_MASKED_NAME = "Fulcrum Support"
DISTRICT_ADMIN_MASKED_NAME = "Fulcrum Support"
OPS_ADMIN_MASKED_NAME = "Fulcrum Support"

PRIMARY_ADMIN_EMAIL = "fulcrumindia1@gmail.com"
PRIMARY_ADMIN_FALLBACK_UUID = "616304b5-aef5-4cd0-88be-2fda7ddf7f88"


def get_primary_admin_id() -> str:
    """Dynamically resolves the single primary platform administrator UUID (cached globally)."""
    cached = get_global_cache("primary_admin_id")
    if cached:
        return str(cached)
    try:
        from services.profiles import list_profiles_by_role
        admins = list_profiles_by_role("admin")
        for p in admins:
            if str(p.get("email") or "").strip().lower() == PRIMARY_ADMIN_EMAIL:
                resolved = str(p["id"])
                set_global_cache("primary_admin_id", resolved, ttl_seconds=3600)
                return resolved
    except Exception:
        pass
    set_global_cache("primary_admin_id", PRIMARY_ADMIN_FALLBACK_UUID, ttl_seconds=3600)
    return PRIMARY_ADMIN_FALLBACK_UUID


def get_masked_actor_name(user_id: str, real_name: str, role: str) -> str:
    """
    Masks platform administrator identity in entrepreneur-facing logs,
    journey events, notifications, and dossiers to preserve institutional neutrality.
    """
    if role in ("admin", "super_admin"):
        return ADMIN_MASKED_NAME
    elif role == "district_admin":
        return DISTRICT_ADMIN_MASKED_NAME
    elif role == "operational_admin":
        return OPS_ADMIN_MASKED_NAME
    return real_name


# ── CONFIDENTIAL GUIDE COMPLAINTS ──
def submit_guide_complaint(
    aspirant_id: str,
    guide_id: Optional[str],
    reason: str,
    details: str
) -> Tuple[bool, Optional[str]]:
    """
    Submits a confidential complaint or reassignment request against an assigned Guide or to Fulcrum Support.
    Strictly isolated: Visible only to Administrators.
    """
    valid_reasons = ("inactivity", "poor_communication", "conflict_of_interest", "professional_conduct", "other")
    if reason not in valid_reasons:
        return False, f"Invalid complaint reason. Must be one of: {', '.join(valid_reasons)}"

    if not details or len(details.strip()) < 10:
        return False, "Please provide detailed context for this request (minimum 10 characters)."

    admin_uuid = get_primary_admin_id()
    # If no guide is assigned or guide_id is empty, associate with primary admin as fallback recipient
    effective_guide_id = guide_id if (guide_id and guide_id != aspirant_id) else admin_uuid

    import uuid
    complaint_id = str(uuid.uuid4())
    now_iso = datetime.now(timezone.utc).isoformat()

    record = {
        "id": complaint_id,
        "aspirant_id": aspirant_id,
        "guide_id": effective_guide_id,
        "reason": reason,
        "details": details.strip(),
        "status": "PENDING",
        "resolution_notes": None,
        "resolved_by": None,
        "resolved_at": None,
        "created_at": now_iso
    }

    backend = get_data_backend()
    if backend == "supabase":
        admin = get_supabase_admin_client()
        if not admin:
            return False, "Database error: Administrative database client unavailable."
        try:
            res = admin.table("guide_complaints").insert(record).execute()
            if not res.data:
                return False, "Database error: Could not record confidential complaint."
        except Exception as e:
            return False, f"Database error submitting complaint: {e}"

    db = get_local_db()
    if hasattr(db, "insert_guide_complaint"):
        db.insert_guide_complaint(record)

    # Trigger admin alert notification
    try:
        from services.notifications import create_notification
        create_notification(
            user_id=admin_uuid,
            title="Confidential Support Report Filed",
            message=f"An entrepreneur has submitted a confidential {reason.replace('_', ' ')} report to Fulcrum Support.",
            notification_type="CONFIDENTIAL_COMPLAINT",
            actor_id=aspirant_id
        )
    except Exception as e:
        print(f"[Governance] Notification error: {e}")

    return True, complaint_id


def list_guide_complaints(status: Optional[str] = None) -> List[Dict]:
    """Retrieves all confidential complaints for Super Admin dashboard."""
    backend = get_data_backend()
    records = []

    if backend == "supabase":
        admin = get_supabase_admin_client()
        if admin:
            try:
                q = admin.table("guide_complaints").select("*").order("created_at", desc=True)
                if status:
                    q = q.eq("status", status)
                res = q.execute()
                records = res.data or []
            except Exception:
                pass

    if not records:
        db = get_local_db()
        if hasattr(db, "list_guide_complaints"):
            records = db.list_guide_complaints(status=status)

    return records


def list_aspirant_complaints(aspirant_id: str) -> List[Dict]:
    """Retrieves confidential complaints submitted by a specific Aspirant for their own status tracking."""
    if not aspirant_id:
        return []
    all_records = list_guide_complaints()
    return [r for r in all_records if str(r.get("aspirant_id")) == str(aspirant_id)]


def resolve_guide_complaint(
    complaint_id: str,
    status: str,
    resolution_notes: str,
    admin_id: str
) -> Tuple[bool, Optional[str]]:
    """Resolves or dismisses a confidential complaint with administrative notes."""
    if status not in ("RESOLVED", "DISMISSED", "UNDER_REVIEW"):
        return False, "Invalid status"

    now_iso = datetime.now(timezone.utc).isoformat()
    backend = get_data_backend()
    target_aspirant_id = None

    if backend == "supabase":
        admin = get_supabase_admin_client()
        if not admin:
            return False, "Database error: Administrative database client unavailable."
        try:
            res = admin.table("guide_complaints").update({
                "status": status,
                "resolution_notes": resolution_notes,
                "resolved_by": admin_id,
                "resolved_at": now_iso
            }).eq("id", complaint_id).execute()
            if not res.data:
                return False, "Database error: Complaint record not found or could not be updated."
            target_aspirant_id = res.data[0].get("aspirant_id")
        except Exception as e:
            return False, f"Database error updating complaint: {e}"

    db = get_local_db()
    if hasattr(db, "update_guide_complaint"):
        db.update_guide_complaint(complaint_id, status, resolution_notes, admin_id)
        if not target_aspirant_id and hasattr(db, "list_guide_complaints"):
            for c in db.list_guide_complaints():
                if str(c.get("id")) == str(complaint_id):
                    target_aspirant_id = c.get("aspirant_id")
                    break

    if target_aspirant_id:
        try:
            from services.notifications import create_notification
            status_label = status.replace("_", " ").title()
            note_snippet = (resolution_notes or "").strip()
            msg_body = f"Fulcrum Support updated your confidential report status to '{status_label}'."
            if note_snippet:
                msg_body += f" Note: {note_snippet}"
            create_notification(
                user_id=str(target_aspirant_id),
                title=f"Confidential Support Report: {status_label}",
                message=msg_body,
                notification_type="CONFIDENTIAL_COMPLAINT_UPDATE",
                actor_id=admin_id
            )
        except Exception as e:
            print(f"[Governance] Complaint resolution notification error: {e}")

    return True, None


# ── SME CONFLICT OF INTEREST GOVERNANCE ──
def declare_sme_conflict(
    sme_id: str,
    aspirant_id: str,
    has_conflict: bool,
    conflict_details: str = ""
) -> Tuple[bool, Optional[str]]:
    """Records an SME's mandatory Conflict of Interest declaration."""
    import uuid
    decl_id = str(uuid.uuid4())
    now_iso = datetime.now(timezone.utc).isoformat()

    record = {
        "id": decl_id,
        "sme_id": sme_id,
        "aspirant_id": aspirant_id,
        "has_conflict": has_conflict,
        "conflict_details": conflict_details.strip() if has_conflict else "No conflict declared.",
        "status": "DECLARED",
        "reviewed_by": None,
        "reviewed_at": None,
        "created_at": now_iso
    }

    backend = get_data_backend()
    if backend == "supabase":
        admin = get_supabase_admin_client()
        if admin:
            try:
                admin.table("sme_conflict_declarations").insert(record).execute()
            except Exception:
                pass

    db = get_local_db()
    if hasattr(db, "insert_sme_conflict"):
        db.insert_sme_conflict(record)

    invalidate_memo("admin_dashboard_metrics")
    return True, None


def resolve_sme_conflict(
    conflict_id: str,
    admin_id: str,
    decision: str = "APPROVED"
) -> Tuple[bool, Optional[str]]:
    """
    Transitions a Conflict of Interest declaration after Administrative review.
    Respects schema CHECK constraint ('DECLARED', 'APPROVED', 'REJECTED'):
      - 'APPROVED': Recusal approved & SME unassigned; clears Open COI KPI while retaining recusal restriction.
      - 'REJECTED': Conflict dismissed / recusal restriction cleared, allowing future SME assignment.
    Requires verified Sole Admin authorization.
    """
    from services.roles import require_sole_admin
    ok_admin, err_admin = require_sole_admin(actor_id=admin_id)
    if not ok_admin:
        return False, err_admin

    if not conflict_id:
        return False, "Conflict ID is required."

    clean_decision = str(decision or "").strip().upper()
    if clean_decision not in ("APPROVED", "REJECTED"):
        return False, f"Invalid conflict decision '{decision}'. Expected 'APPROVED' or 'REJECTED'."

    now_iso = datetime.now(timezone.utc).isoformat()
    backend = get_data_backend()

    if backend == "supabase":
        admin = get_supabase_admin_client()
        if not admin:
            return False, "Supabase admin client unavailable."
        try:
            admin.table("sme_conflict_declarations").update({
                "status": clean_decision,
                "reviewed_by": admin_id,
                "reviewed_at": now_iso,
            }).eq("id", conflict_id).execute()
        except Exception as e:
            return False, f"Failed to update COI status in Supabase: {e}"
    else:
        db = get_local_db()
        if hasattr(db, "update_sme_conflict"):
            db.update_sme_conflict(conflict_id, clean_decision, reviewed_by=admin_id)

    invalidate_memo("admin_dashboard_metrics")
    return True, None


def check_sme_has_conflict(sme_id: str, aspirant_id: str) -> bool:
    """Returns True if SME has an active (unresolved) conflict of interest declaration with an aspirant."""
    conflicts = list_sme_conflicts(sme_id=sme_id, aspirant_id=aspirant_id)
    for c in conflicts:
        if c.get("has_conflict") is True and str(c.get("status") or "DECLARED").upper() not in ("RESOLVED", "DISMISSED", "CLEARED", "REJECTED"):
            return True
    return False


has_active_sme_conflict = check_sme_has_conflict


def list_sme_conflicts(
    sme_id: Optional[str] = None,
    aspirant_id: Optional[str] = None,
    only_conflicts: bool = False
) -> List[Dict]:
    """Lists conflict of interest declarations."""
    backend = get_data_backend()
    records = []

    if backend == "supabase":
        admin = get_supabase_admin_client()
        if admin:
            try:
                q = admin.table("sme_conflict_declarations").select("*").order("created_at", desc=True)
                if sme_id:
                    q = q.eq("sme_id", sme_id)
                if aspirant_id:
                    q = q.eq("aspirant_id", aspirant_id)
                res = q.execute()
                records = res.data or []
            except Exception:
                pass

    if not records:
        db = get_local_db()
        if hasattr(db, "list_sme_conflicts"):
            records = db.list_sme_conflicts(sme_id=sme_id, aspirant_id=aspirant_id)

    if only_conflicts:
        records = [r for r in records if r.get("has_conflict") is True]

    return records

