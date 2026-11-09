"""
services/account_lifecycle.py — Account-Wide Lifecycle & Archive Governance Engine
==================================================================================
Canonical Account Lifecycle Implementation for FULCRUM-INDIA.
Distinct from role grants (user_roles.status):
- Account Statuses: ACTIVE, TEMPORARILY_SUSPENDED, ARCHIVED, PENDING_DELETION.
- Separate Legal Hold Flag (prevents deletion while under compliance hold).
- Strict Sole Admin authorization (fulcrumindia1@gmail.com).
- Preserves all historical Journeys, Consultations, and Legal Acceptances.
- Restores users under their original immutable UUID without re-granting revoked roles
  or automatically re-assigning past caseloads.
- Supports dual backends: Supabase (production authoritative) & SQLite (local development).
"""

import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, List, Tuple

from services.auth import get_supabase_admin_client, get_supabase_client, get_data_backend
from services.local_db import get_local_db
from services.cache import get_memo, set_memo, invalidate_memo
from services.roles import (
    require_sole_admin,
    is_strict_admin,
    get_user_roles,
    SOLE_ADMIN_EMAIL,
    SOLE_ADMIN_UUID,
)

VALID_ACCOUNT_STATUSES = ("ACTIVE", "TEMPORARILY_SUSPENDED", "ARCHIVED", "PENDING_DELETION")

VALID_LIFECYCLE_ACTIONS = (
    "SUSPEND",
    "RESUME",
    "ARCHIVE",
    "RESTORE",
    "REQUEST_DELETION",
    "CANCEL_DELETION",
    "APPLY_LEGAL_HOLD",
    "RELEASE_LEGAL_HOLD"
)


def _invalidate_account_caches(user_id: str) -> None:
    """Invalidates all cached state across roles, profiles, assignments, and directories."""
    invalidate_memo(f"profile:{user_id}")
    invalidate_memo(f"user_roles:{user_id}")
    invalidate_memo(f"account_status:{user_id}")
    invalidate_memo(f"mentors:{user_id}")
    invalidate_memo("all_relationships")
    invalidate_memo("active_profiles_for_role:")
    invalidate_memo("list_profiles_by_role:")
    invalidate_memo("multi_role_users")


def get_account_status(user_id: str) -> Dict:
    """
    Retrieves full account lifecycle status details for a user.
    Falls back gracefully to 'ACTIVE' for legacy records lacking explicit lifecycle columns.
    """
    if not user_id:
        return {
            "account_status": "ACTIVE",
            "is_active": True,
            "legal_hold": False,
            "lifecycle_reason": None,
            "status_updated_at": None,
            "status_updated_by": None,
            "deletion_requested_at": None,
            "deletion_requested_by": None,
            "deletion_scheduled_for": None,
            "retention_notes": None,
        }

    cache_key = f"account_status:{user_id}"
    cached = get_memo(cache_key)
    if cached is not None:
        return cached

    backend = get_data_backend()
    status_dict = {}

    if backend == "supabase":
        admin = get_supabase_admin_client() or get_supabase_client()
        if admin:
            try:
                res = admin.table("profiles").select(
                    "id, is_active, account_status, legal_hold, lifecycle_reason, status_updated_at, "
                    "status_updated_by, deletion_requested_at, deletion_requested_by, "
                    "deletion_scheduled_for, retention_notes"
                ).eq("id", user_id).limit(1).execute()
                if res.data and len(res.data) > 0:
                    status_dict = res.data[0]
            except Exception as e:
                # If migration 009 columns are not yet present in Supabase table, query standard fields
                try:
                    res_std = admin.table("profiles").select("id, is_active").eq("id", user_id).limit(1).execute()
                    if res_std.data and len(res_std.data) > 0:
                        status_dict = res_std.data[0]
                except Exception:
                    pass
    else:
        db = get_local_db()
        p = db.get_profile_by_id(user_id)
        if p:
            status_dict = p

    # Default to ACTIVE if column is unset or null
    raw_status = str(status_dict.get("account_status") or "").strip().upper()
    if raw_status not in VALID_ACCOUNT_STATUSES:
        raw_status = "ACTIVE" if status_dict.get("is_active", True) else "TEMPORARILY_SUSPENDED"

    result = {
        "user_id": user_id,
        "account_status": raw_status,
        "is_active": bool(status_dict.get("is_active", True) and raw_status == "ACTIVE"),
        "legal_hold": bool(status_dict.get("legal_hold", False)),
        "lifecycle_reason": status_dict.get("lifecycle_reason"),
        "status_updated_at": status_dict.get("status_updated_at"),
        "status_updated_by": status_dict.get("status_updated_by"),
        "deletion_requested_at": status_dict.get("deletion_requested_at"),
        "deletion_requested_by": status_dict.get("deletion_requested_by"),
        "deletion_scheduled_for": status_dict.get("deletion_scheduled_for"),
        "retention_notes": status_dict.get("retention_notes"),
    }

    set_memo(cache_key, result, ttl_seconds=10)
    return result


def is_account_active(user_id: str) -> Tuple[bool, Optional[str]]:
    """
    Fast boolean authorization gate. Returns (True, None) if account is ACTIVE.
    Returns (False, refusal_reason) if suspended, archived, or scheduled for deletion.
    """
    if not user_id:
        return False, "Missing user ID."

    details = get_account_status(user_id)
    status = details.get("account_status", "ACTIVE")

    if status == "ACTIVE":
        if not details.get("is_active", True):
            return False, "Account access is marked inactive by administration."
        return True, None
    elif status == "TEMPORARILY_SUSPENDED":
        reason = details.get("lifecycle_reason") or "Administrative compliance review"
        return False, f"Account is temporarily suspended: {reason}. Contact fulcrumindia1@gmail.com."
    elif status == "ARCHIVED":
        reason = details.get("lifecycle_reason") or "Institutional archival"
        return False, f"Account is archived: {reason}. Historical records are preserved. Contact administration for restoration."
    elif status == "PENDING_DELETION":
        sched = (details.get("deletion_scheduled_for") or "")[:10]
        return False, f"Account is pending deletion review (scheduled review: {sched}). You may cancel this request or contact administration."

    return False, f"Account is restricted (status: {status})."


def suspend_account(
    user_id: str,
    reason: str,
    actor_id: Optional[str] = None
) -> Tuple[bool, Optional[str]]:
    """
    Temporarily suspends an account. Locks dashboard access immediately while preserving all data.
    Requires verified Sole Admin authorization.
    """
    ok_admin, err_admin = require_sole_admin(actor_id=actor_id)
    if not ok_admin:
        return False, err_admin

    if not user_id or not reason.strip():
        return False, "User ID and a clear suspension reason are required."

    from services.profiles import get_profile
    prof = get_profile(user_id)
    if not prof:
        return False, "Account profile not found."

    if is_strict_admin(user_id=user_id, email=prof.get("email")):
        return False, "Security violation: The Sole Platform Administrator account cannot be suspended."

    now_iso = datetime.now(timezone.utc).isoformat()
    prev_details = get_account_status(user_id)
    prev_status = prev_details.get("account_status", "ACTIVE")

    backend = get_data_backend()
    if backend == "supabase":
        admin = get_supabase_admin_client()
        if not admin:
            return False, "Supabase admin client unavailable."
        try:
            admin.table("profiles").update({
                "account_status": "TEMPORARILY_SUSPENDED",
                "is_active": False,
                "lifecycle_reason": reason.strip(),
                "status_updated_at": now_iso,
                "status_updated_by": actor_id,
                "updated_at": now_iso
            }).eq("id", user_id).execute()

            # Record audit log
            try:
                admin.table("account_lifecycle_log").insert({
                    "id": str(uuid.uuid4()),
                    "user_id": user_id,
                    "actor_id": actor_id,
                    "action": "SUSPEND",
                    "previous_status": prev_status,
                    "new_status": "TEMPORARILY_SUSPENDED",
                    "reason": reason.strip(),
                    "metadata": {"timestamp": now_iso},
                    "created_at": now_iso
                }).execute()
            except Exception as log_err:
                print(f"[AccountLifecycle] Audit log write notice: {log_err}")
        except Exception as e:
            return False, f"Failed to suspend account in Supabase: {e}"
    else:
        db = get_local_db()
        db.update_account_status(
            user_id=user_id,
            status="TEMPORARILY_SUSPENDED",
            is_active=0,
            reason=reason.strip(),
            actor_id=actor_id,
            updated_at=now_iso
        )
        db.log_account_lifecycle({
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "actor_id": actor_id,
            "action": "SUSPEND",
            "previous_status": prev_status,
            "new_status": "TEMPORARILY_SUSPENDED",
            "reason": reason.strip(),
            "metadata": "{}",
            "created_at": now_iso
        })

    _invalidate_account_caches(user_id)

    # In-app notification to affected user
    try:
        from services.notifications import create_notification
        create_notification(
            user_id=user_id,
            title="Account Temporarily Suspended",
            message=f"Your account access has been temporarily paused by Administration. Reason: {reason.strip()}.",
            notification_type="account_suspended",
            actor_id=actor_id
        )
    except Exception:
        pass

    return True, None


def resume_account(
    user_id: str,
    actor_id: Optional[str] = None,
    reason: str = ""
) -> Tuple[bool, Optional[str]]:
    """
    Reactivates a temporarily suspended account back to ACTIVE status.
    Requires verified Sole Admin authorization.
    """
    ok_admin, err_admin = require_sole_admin(actor_id=actor_id)
    if not ok_admin:
        return False, err_admin

    if not user_id:
        return False, "User ID is required."

    curr_details = get_account_status(user_id)
    curr_status = curr_details.get("account_status")
    if curr_status != "TEMPORARILY_SUSPENDED":
        return False, f"Cannot resume: Account status is '{curr_status}', expected 'TEMPORARILY_SUSPENDED'."

    now_iso = datetime.now(timezone.utc).isoformat()
    note = reason.strip() or "Administrative review resolved; account resumed."

    backend = get_data_backend()
    if backend == "supabase":
        admin = get_supabase_admin_client()
        if not admin:
            return False, "Supabase admin client unavailable."
        try:
            admin.table("profiles").update({
                "account_status": "ACTIVE",
                "is_active": True,
                "lifecycle_reason": note,
                "status_updated_at": now_iso,
                "status_updated_by": actor_id,
                "updated_at": now_iso
            }).eq("id", user_id).execute()

            try:
                admin.table("account_lifecycle_log").insert({
                    "id": str(uuid.uuid4()),
                    "user_id": user_id,
                    "actor_id": actor_id,
                    "action": "RESUME",
                    "previous_status": curr_status,
                    "new_status": "ACTIVE",
                    "reason": note,
                    "metadata": {"timestamp": now_iso},
                    "created_at": now_iso
                }).execute()
            except Exception as log_err:
                print(f"[AccountLifecycle] Audit log write notice: {log_err}")
        except Exception as e:
            return False, f"Failed to resume account in Supabase: {e}"
    else:
        db = get_local_db()
        db.update_account_status(
            user_id=user_id,
            status="ACTIVE",
            is_active=1,
            reason=note,
            actor_id=actor_id,
            updated_at=now_iso
        )
        db.log_account_lifecycle({
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "actor_id": actor_id,
            "action": "RESUME",
            "previous_status": curr_status,
            "new_status": "ACTIVE",
            "reason": note,
            "metadata": "{}",
            "created_at": now_iso
        })

    _invalidate_account_caches(user_id)

    try:
        from services.notifications import create_notification
        create_notification(
            user_id=user_id,
            title="Account Access Restored",
            message="Your Fulcrum account has been reactivated. You may now access your dashboard normally.",
            notification_type="account_resumed",
            actor_id=actor_id
        )
    except Exception:
        pass

    return True, None


def get_archive_impact_preview(user_id: str) -> Dict:
    """
    Forensic pre-action impact preview before archiving or closing an account.
    Calculates active caseload, consultations, remaining co-mentors, and orphaned risk.
    """
    from services.profiles import get_profile
    from services.relationships import get_all_relationships, get_aspirant_mentors
    from services.help_requests import list_requests

    p = get_profile(user_id) or {}
    lifecycle = get_account_status(user_id)
    roles = get_user_roles(user_id)
    active_role_names = [r["role"] for r in roles if r.get("status") == "active"]

    assigned_as_guide: List[Dict] = []
    assigned_as_sme: List[Dict] = []
    orphaned_guide_cases: List[Dict] = []
    orphaned_sme_cases: List[Dict] = []

    rels = get_all_relationships()
    uid_str = str(user_id)

    for rel in rels:
        aid = rel.get("aspirant_id")
        if not aid:
            continue

        # Check guide assignments
        raw_gids = rel.get("guide_ids") or []
        if isinstance(raw_gids, str):
            import json
            try: raw_gids = json.loads(raw_gids)
            except Exception: raw_gids = [raw_gids]
        if rel.get("guide_id") and rel["guide_id"] not in raw_gids:
            raw_gids.insert(0, rel["guide_id"])
        guides_set = {str(gid) for gid in raw_gids if gid}

        if uid_str in guides_set:
            remaining_guides = [gid for gid in guides_set if gid != uid_str]
            case_info = {
                "aspirant_id": aid,
                "remaining_guide_count": len(remaining_guides),
                "has_co_guide": len(remaining_guides) > 0,
            }
            assigned_as_guide.append(case_info)
            if len(remaining_guides) == 0:
                orphaned_guide_cases.append(case_info)

        # Check SME assignments
        raw_sids = rel.get("sme_ids") or []
        if isinstance(raw_sids, str):
            import json
            try: raw_sids = json.loads(raw_sids)
            except Exception: raw_sids = [raw_sids]
        if rel.get("sme_id") and rel["sme_id"] not in raw_sids:
            raw_sids.insert(0, rel["sme_id"])
        smes_set = {str(sid) for sid in raw_sids if sid}

        if uid_str in smes_set:
            remaining_smes = [sid for sid in smes_set if sid != uid_str]
            case_info = {
                "aspirant_id": aid,
                "remaining_sme_count": len(remaining_smes),
                "has_co_sme": len(remaining_smes) > 0,
            }
            assigned_as_sme.append(case_info)
            if len(remaining_smes) == 0:
                orphaned_sme_cases.append(case_info)

    # Count pending consultations
    open_tickets = []
    try:
        all_reqs = list_requests()
        open_tickets = [
            r for r in all_reqs
            if str(r.get("assigned_guide_id")) == uid_str or str(r.get("assigned_sme_id")) == uid_str
            if str(r.get("status", "")).upper() in ("OPEN", "IN_PROGRESS", "WAITING_ON_ASPIRANT", "WAITING_ON_GUIDE_SME")
        ]
    except Exception:
        pass

    is_admin_user = is_strict_admin(user_id=user_id, email=p.get("email"))

    return {
        "user_id": user_id,
        "full_name": p.get("full_name") or "User",
        "email": p.get("email") or "",
        "current_status": lifecycle.get("account_status", "ACTIVE"),
        "legal_hold": lifecycle.get("legal_hold", False),
        "active_roles": active_role_names,
        "assigned_guide_cases_count": len(assigned_as_guide),
        "assigned_sme_cases_count": len(assigned_as_sme),
        "orphaned_guide_cases_count": len(orphaned_guide_cases),
        "orphaned_sme_cases_count": len(orphaned_sme_cases),
        "open_consultations_count": len(open_tickets),
        "is_admin_user": is_admin_user,
        "is_archive_eligible": not is_admin_user,
        "is_deletion_eligible": (not is_admin_user and not lifecycle.get("legal_hold", False)),
    }


def archive_account(
    user_id: str,
    reason: str,
    actor_id: Optional[str] = None
) -> Tuple[bool, Optional[str]]:
    """
    Archives a user account.
    - Locks application access and removes from active mentor/candidate directories.
    - Executes safe mentor handover: unassigns from active cases, re-routes tickets to co-mentors
      or sets them to unassigned triage queue for Admin reassignment.
    - Preserves all historical Journeys, Consultations, and Legal records intact.
    - Preserves individual role grants (does NOT write 'archived' into user_roles.status).
    - Requires verified Sole Admin authorization.
    """
    ok_admin, err_admin = require_sole_admin(actor_id=actor_id)
    if not ok_admin:
        return False, err_admin

    if not user_id or not reason.strip():
        return False, "User ID and a clear archival reason are required."

    from services.profiles import get_profile
    prof = get_profile(user_id)
    if not prof:
        return False, "User profile not found."

    if is_strict_admin(user_id=user_id, email=prof.get("email")):
        return False, "Security violation: The Sole Platform Administrator account cannot be archived."

    now_iso = datetime.now(timezone.utc).isoformat()
    prev_details = get_account_status(user_id)
    prev_status = prev_details.get("account_status", "ACTIVE")

    # ─────────────────────────────────────────────────────────────────
    # SAFE MENTOR HANDOVER: Process all assigned cases before archival
    # ─────────────────────────────────────────────────────────────────
    from services.relationships import get_all_relationships, unassign_guide, unassign_sme
    rels = get_all_relationships()
    uid_str = str(user_id)

    for rel in rels:
        aid = rel.get("aspirant_id")
        if not aid or rel.get("status") != "active":
            continue

        # Handle Guide unassignment
        raw_gids = rel.get("guide_ids") or []
        if isinstance(raw_gids, str):
            import json
            try: raw_gids = json.loads(raw_gids)
            except Exception: raw_gids = [raw_gids]
        if rel.get("guide_id") and rel["guide_id"] not in raw_gids:
            raw_gids.insert(0, rel["guide_id"])
        guides_set = {str(gid) for gid in raw_gids if gid}

        if uid_str in guides_set:
            unassign_guide(
                aspirant_id=aid,
                guide_id=uid_str,
                admin_id=actor_id,
                reason=f"Account archived by Administration: {reason.strip()}"
            )

        # Handle SME unassignment
        raw_sids = rel.get("sme_ids") or []
        if isinstance(raw_sids, str):
            import json
            try: raw_sids = json.loads(raw_sids)
            except Exception: raw_sids = [raw_sids]
        if rel.get("sme_id") and rel["sme_id"] not in raw_sids:
            raw_sids.insert(0, rel["sme_id"])
        smes_set = {str(sid) for sid in raw_sids if sid}

        if uid_str in smes_set:
            unassign_sme(
                aspirant_id=aid,
                sme_id=uid_str,
                admin_id=actor_id,
                reason=f"Account archived by Administration: {reason.strip()}"
            )

    # Update account status in persistence layer
    backend = get_data_backend()
    if backend == "supabase":
        admin = get_supabase_admin_client()
        if not admin:
            return False, "Supabase admin client unavailable."
        try:
            admin.table("profiles").update({
                "account_status": "ARCHIVED",
                "is_active": False,
                "lifecycle_reason": reason.strip(),
                "status_updated_at": now_iso,
                "status_updated_by": actor_id,
                "updated_at": now_iso
            }).eq("id", user_id).execute()

            try:
                admin.table("account_lifecycle_log").insert({
                    "id": str(uuid.uuid4()),
                    "user_id": user_id,
                    "actor_id": actor_id,
                    "action": "ARCHIVE",
                    "previous_status": prev_status,
                    "new_status": "ARCHIVED",
                    "reason": reason.strip(),
                    "metadata": {"timestamp": now_iso},
                    "created_at": now_iso
                }).execute()
            except Exception as log_err:
                print(f"[AccountLifecycle] Audit log write notice: {log_err}")
        except Exception as e:
            return False, f"Failed to archive account in Supabase: {e}"
    else:
        db = get_local_db()
        db.update_account_status(
            user_id=user_id,
            status="ARCHIVED",
            is_active=0,
            reason=reason.strip(),
            actor_id=actor_id,
            updated_at=now_iso
        )
        db.log_account_lifecycle({
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "actor_id": actor_id,
            "action": "ARCHIVE",
            "previous_status": prev_status,
            "new_status": "ARCHIVED",
            "reason": reason.strip(),
            "metadata": "{}",
            "created_at": now_iso
        })

    _invalidate_account_caches(user_id)
    return True, None


def restore_account(
    user_id: str,
    actor_id: Optional[str] = None,
    reason: str = ""
) -> Tuple[bool, Optional[str]]:
    """
    Restores an archived or pending-deletion account back to ACTIVE under the same immutable Auth UUID.
    CRITICAL SAFETY RULES:
    1. Preserves original Auth UUID and profile identity.
    2. Does NOT automatically restore previously revoked roles.
    3. Does NOT automatically reclaim past caseloads (cases remain with current mentors).
    Requires verified Sole Admin authorization.
    """
    ok_admin, err_admin = require_sole_admin(actor_id=actor_id)
    if not ok_admin:
        return False, err_admin

    if not user_id:
        return False, "User ID is required."

    curr_details = get_account_status(user_id)
    curr_status = curr_details.get("account_status")
    if curr_status not in ("ARCHIVED", "PENDING_DELETION"):
        return False, f"Cannot restore: Account status is '{curr_status}', expected 'ARCHIVED' or 'PENDING_DELETION'."

    now_iso = datetime.now(timezone.utc).isoformat()
    note = reason.strip() or "Restored to active status by Administration."

    backend = get_data_backend()
    if backend == "supabase":
        admin = get_supabase_admin_client()
        if not admin:
            return False, "Supabase admin client unavailable."
        try:
            admin.table("profiles").update({
                "account_status": "ACTIVE",
                "is_active": True,
                "lifecycle_reason": note,
                "status_updated_at": now_iso,
                "status_updated_by": actor_id,
                "deletion_requested_at": None,
                "deletion_requested_by": None,
                "deletion_scheduled_for": None,
                "updated_at": now_iso
            }).eq("id", user_id).execute()

            try:
                admin.table("account_lifecycle_log").insert({
                    "id": str(uuid.uuid4()),
                    "user_id": user_id,
                    "actor_id": actor_id,
                    "action": "RESTORE",
                    "previous_status": curr_status,
                    "new_status": "ACTIVE",
                    "reason": note,
                    "metadata": {"timestamp": now_iso},
                    "created_at": now_iso
                }).execute()
            except Exception as log_err:
                print(f"[AccountLifecycle] Audit log write notice: {log_err}")
        except Exception as e:
            return False, f"Failed to restore account in Supabase: {e}"
    else:
        db = get_local_db()
        db.update_account_status(
            user_id=user_id,
            status="ACTIVE",
            is_active=1,
            reason=note,
            actor_id=actor_id,
            updated_at=now_iso,
            clear_deletion=True
        )
        db.log_account_lifecycle({
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "actor_id": actor_id,
            "action": "RESTORE",
            "previous_status": curr_status,
            "new_status": "ACTIVE",
            "reason": note,
            "metadata": "{}",
            "created_at": now_iso
        })

    _invalidate_account_caches(user_id)

    try:
        from services.notifications import create_notification
        create_notification(
            user_id=user_id,
            title="Account Restored",
            message="Your account has been reactivated by Administration. Welcome back to FULCRUM-INDIA.",
            notification_type="account_restored",
            actor_id=actor_id
        )
    except Exception:
        pass

    return True, None


def request_account_deletion(
    user_id: str,
    actor_id: Optional[str] = None,
    reason: str = "",
    grace_days: int = 30
) -> Tuple[bool, Optional[str]]:
    """
    Schedules an account for closure with an owner-configurable 30-day grace period.
    STRICT INSTITUTIONAL ENFORCEMENT:
    - Rejects if legal hold is active.
    - NEVER performs automatic permanent purge during this implementation phase.
    - Supports cancellation by Admin or user during grace window.
    """
    if not user_id:
        return False, "User ID is required."

    from services.profiles import get_profile
    prof = get_profile(user_id)
    if not prof:
        return False, "User profile not found."

    if is_strict_admin(user_id=user_id, email=prof.get("email")):
        return False, "Security violation: The Sole Platform Administrator account cannot be scheduled for deletion."

    # Authorization: Must be Sole Admin or the user themselves
    actor_id = actor_id or user_id
    is_self = (str(actor_id) == str(user_id))
    is_admin = is_strict_admin(user_id=actor_id)

    if not is_self and not is_admin:
        return False, "Unauthorized: Only the account owner or Sole Administrator can schedule account closure."

    curr_details = get_account_status(user_id)
    if curr_details.get("legal_hold"):
        return False, "Action prohibited: Account is currently under legal hold. Legal hold must be officially released before scheduling closure."

    now_dt = datetime.now(timezone.utc)
    now_iso = now_dt.isoformat()
    scheduled_for = (now_dt + timedelta(days=max(1, grace_days))).isoformat()
    note = reason.strip() or f"Account closure scheduled with {grace_days}-day review window."

    backend = get_data_backend()
    if backend == "supabase":
        admin = get_supabase_admin_client()
        if not admin:
            return False, "Supabase admin client unavailable."
        try:
            admin.table("profiles").update({
                "account_status": "PENDING_DELETION",
                "deletion_requested_at": now_iso,
                "deletion_requested_by": actor_id,
                "deletion_scheduled_for": scheduled_for,
                "lifecycle_reason": note,
                "status_updated_at": now_iso,
                "status_updated_by": actor_id,
                "updated_at": now_iso
            }).eq("id", user_id).execute()

            try:
                admin.table("account_lifecycle_log").insert({
                    "id": str(uuid.uuid4()),
                    "user_id": user_id,
                    "actor_id": actor_id,
                    "action": "REQUEST_DELETION",
                    "previous_status": curr_details.get("account_status", "ACTIVE"),
                    "new_status": "PENDING_DELETION",
                    "reason": note,
                    "metadata": {"scheduled_for": scheduled_for, "grace_days": grace_days},
                    "created_at": now_iso
                }).execute()
            except Exception as log_err:
                print(f"[AccountLifecycle] Audit log write notice: {log_err}")
        except Exception as e:
            return False, f"Failed to schedule account deletion in Supabase: {e}"
    else:
        db = get_local_db()
        db.update_account_status(
            user_id=user_id,
            status="PENDING_DELETION",
            is_active=1,  # Keep profile active to allow login into grace review banner
            reason=note,
            actor_id=actor_id,
            updated_at=now_iso,
            deletion_requested_at=now_iso,
            deletion_requested_by=actor_id,
            deletion_scheduled_for=scheduled_for
        )
        db.log_account_lifecycle({
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "actor_id": actor_id,
            "action": "REQUEST_DELETION",
            "previous_status": curr_details.get("account_status", "ACTIVE"),
            "new_status": "PENDING_DELETION",
            "reason": note,
            "metadata": f"{{\"scheduled_for\": \"{scheduled_for}\", \"grace_days\": {grace_days}}}",
            "created_at": now_iso
        })

    _invalidate_account_caches(user_id)
    return True, None


def cancel_account_deletion(
    user_id: str,
    actor_id: Optional[str] = None,
    reason: str = ""
) -> Tuple[bool, Optional[str]]:
    """
    Cancels a pending account deletion request and restores normal ACTIVE status.
    Can be invoked by the account owner or the Sole Administrator during the grace period.
    """
    if not user_id:
        return False, "User ID is required."

    actor_id = actor_id or user_id
    is_self = (str(actor_id) == str(user_id))
    is_admin = is_strict_admin(user_id=actor_id)

    if not is_self and not is_admin:
        return False, "Unauthorized: Only the account owner or Sole Administrator can cancel account closure."

    curr_details = get_account_status(user_id)
    if curr_details.get("account_status") != "PENDING_DELETION":
        return False, "Account is not currently pending deletion."

    now_iso = datetime.now(timezone.utc).isoformat()
    note = reason.strip() or "Deletion request cancelled during review period."

    backend = get_data_backend()
    if backend == "supabase":
        admin = get_supabase_admin_client()
        if not admin:
            return False, "Supabase admin client unavailable."
        try:
            admin.table("profiles").update({
                "account_status": "ACTIVE",
                "is_active": True,
                "deletion_requested_at": None,
                "deletion_requested_by": None,
                "deletion_scheduled_for": None,
                "lifecycle_reason": note,
                "status_updated_at": now_iso,
                "status_updated_by": actor_id,
                "updated_at": now_iso
            }).eq("id", user_id).execute()

            try:
                admin.table("account_lifecycle_log").insert({
                    "id": str(uuid.uuid4()),
                    "user_id": user_id,
                    "actor_id": actor_id,
                    "action": "CANCEL_DELETION",
                    "previous_status": "PENDING_DELETION",
                    "new_status": "ACTIVE",
                    "reason": note,
                    "metadata": {"timestamp": now_iso},
                    "created_at": now_iso
                }).execute()
            except Exception as log_err:
                print(f"[AccountLifecycle] Audit log write notice: {log_err}")
        except Exception as e:
            return False, f"Failed to cancel account deletion in Supabase: {e}"
    else:
        db = get_local_db()
        db.update_account_status(
            user_id=user_id,
            status="ACTIVE",
            is_active=1,
            reason=note,
            actor_id=actor_id,
            updated_at=now_iso,
            clear_deletion=True
        )
        db.log_account_lifecycle({
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "actor_id": actor_id,
            "action": "CANCEL_DELETION",
            "previous_status": "PENDING_DELETION",
            "new_status": "ACTIVE",
            "reason": note,
            "metadata": "{}",
            "created_at": now_iso
        })

    _invalidate_account_caches(user_id)
    return True, None


def set_legal_hold(
    user_id: str,
    enabled: bool,
    reason: str,
    actor_id: Optional[str] = None
) -> Tuple[bool, Optional[str]]:
    """
    Applies or releases an institutional Legal Hold on an account.
    When Legal Hold is active, deletion requests and erasure procedures are strictly blocked.
    Requires verified Sole Admin authorization.
    """
    ok_admin, err_admin = require_sole_admin(actor_id=actor_id)
    if not ok_admin:
        return False, err_admin

    if not user_id or not reason.strip():
        return False, "User ID and reason are required."

    from services.profiles import get_profile
    prof = get_profile(user_id)
    if not prof:
        return False, "User profile not found."

    now_iso = datetime.now(timezone.utc).isoformat()
    curr_details = get_account_status(user_id)
    curr_status = curr_details.get("account_status", "ACTIVE")
    action_label = "APPLY_LEGAL_HOLD" if enabled else "RELEASE_LEGAL_HOLD"

    backend = get_data_backend()
    if backend == "supabase":
        admin = get_supabase_admin_client()
        if not admin:
            return False, "Supabase admin client unavailable."
        try:
            admin.table("profiles").update({
                "legal_hold": enabled,
                "retention_notes": f"Legal hold {'applied' if enabled else 'released'}: {reason.strip()}",
                "updated_at": now_iso
            }).eq("id", user_id).execute()

            try:
                admin.table("account_lifecycle_log").insert({
                    "id": str(uuid.uuid4()),
                    "user_id": user_id,
                    "actor_id": actor_id,
                    "action": action_label,
                    "previous_status": curr_status,
                    "new_status": curr_status,
                    "reason": reason.strip(),
                    "metadata": {"legal_hold": enabled},
                    "created_at": now_iso
                }).execute()
            except Exception as log_err:
                print(f"[AccountLifecycle] Audit log write notice: {log_err}")
        except Exception as e:
            return False, f"Failed to update legal hold in Supabase: {e}"
    else:
        db = get_local_db()
        db.update_legal_hold(user_id, enabled, reason.strip())
        db.log_account_lifecycle({
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "actor_id": actor_id,
            "action": action_label,
            "previous_status": curr_status,
            "new_status": curr_status,
            "reason": reason.strip(),
            "metadata": f"{{\"legal_hold\": {str(enabled).lower()}}}",
            "created_at": now_iso
        })

    _invalidate_account_caches(user_id)
    return True, None


def list_account_lifecycle_logs(
    user_id: Optional[str] = None,
    limit: int = 150
) -> List[Dict]:
    """
    Retrieves chronological, immutable account action history for audit inspection.
    """
    backend = get_data_backend()
    if backend == "supabase":
        admin = get_supabase_admin_client() or get_supabase_client()
        if admin:
            try:
                q = admin.table("account_lifecycle_log").select("*")
                if user_id:
                    q = q.eq("user_id", user_id)
                res = q.order("created_at", desc=True).limit(limit).execute()
                return res.data or []
            except Exception as e:
                print(f"[AccountLifecycle] Log fetch notice: {e}")
                return []
    db = get_local_db()
    if hasattr(db, "list_account_lifecycle_logs"):
        return db.list_account_lifecycle_logs(user_id=user_id, limit=limit)
    return []


def list_accounts_by_status(status_filter: Optional[str] = None) -> List[Dict]:
    """
    Retrieves all accounts annotated with current lifecycle status, legal hold, and role tags.
    """
    from services.profiles import list_users_with_multi_roles
    users = list_users_with_multi_roles()

    results = []
    for u in users:
        uid = u.get("id")
        raw_status = str(u.get("account_status") or "").strip().upper()
        if raw_status not in VALID_ACCOUNT_STATUSES:
            raw_status = "ACTIVE" if u.get("is_active", True) else "TEMPORARILY_SUSPENDED"

        u_copy = dict(u)
        u_copy["account_status"] = raw_status
        u_copy["legal_hold"] = bool(u.get("legal_hold", False))

        if status_filter and status_filter.upper() != "ALL":
            if u_copy["account_status"] != status_filter.upper():
                continue

        results.append(u_copy)

    return results
