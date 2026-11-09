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
    STRICT FAIL-CLOSED POLICY (P0):
    - Missing user ID: DENIED.
    - Missing account record: DENIED.
    - Supabase unavailable / network error: DENIED (no SQLite fallback in Supabase mode).
    - Schema configuration failure: DENIED.
    - Unknown lifecycle state: DENIED.
    - Legacy schema record (missing migration 009 columns): maps based on existing is_active flag.
    """
    if not user_id or not str(user_id).strip():
        return {
            "user_id": None,
            "account_status": "DENIED",
            "is_active": False,
            "exists": False,
            "error": "Missing user ID.",
            "legal_hold": False,
            "lifecycle_reason": "Missing user ID.",
            "status_updated_at": None,
            "status_updated_by": None,
            "deletion_requested_at": None,
            "deletion_requested_by": None,
            "deletion_scheduled_for": None,
            "retention_notes": None,
        }

    clean_uid = str(user_id).strip()
    cache_key = f"account_status:{clean_uid}"
    cached = get_memo(cache_key)
    if cached is not None:
        return cached

    backend = get_data_backend()
    status_dict = {}

    if backend == "supabase":
        admin = get_supabase_admin_client() or get_supabase_client()
        if not admin:
            res_err = {
                "user_id": clean_uid,
                "account_status": "DENIED",
                "is_active": False,
                "exists": False,
                "error": "Authentication backend unavailable: Supabase client is not configured.",
                "legal_hold": False,
                "lifecycle_reason": "Database connection unavailable.",
                "status_updated_at": None,
                "status_updated_by": None,
                "deletion_requested_at": None,
                "deletion_requested_by": None,
                "deletion_scheduled_for": None,
                "retention_notes": None,
            }
            return res_err

        try:
            res = admin.table("profiles").select(
                "id, is_active, account_status, legal_hold, status_reason, "
                "deletion_requested_at, deletion_scheduled_for, archived_at, restored_at, updated_at"
            ).eq("id", clean_uid).limit(1).execute()

            if res.data and len(res.data) > 0:
                status_dict = res.data[0]
            else:
                # User record does not exist in Supabase! Fail-closed immediately.
                res_not_found = {
                    "user_id": clean_uid,
                    "account_status": "DENIED",
                    "is_active": False,
                    "exists": False,
                    "error": f"Account profile record not found for user ID '{clean_uid}'.",
                    "legal_hold": False,
                    "lifecycle_reason": "Account record does not exist.",
                    "status_updated_at": None,
                    "status_updated_by": None,
                    "deletion_requested_at": None,
                    "deletion_requested_by": None,
                    "deletion_scheduled_for": None,
                    "retention_notes": None,
                }
                set_memo(cache_key, res_not_found, ttl_seconds=5)
                return res_not_found
        except Exception as e:
            err_str = str(e).lower()
            # If migration 009 columns are not yet present in Supabase table, query standard fields
            if "column" in err_str or "does not exist" in err_str or "42703" in err_str:
                try:
                    res_std = admin.table("profiles").select("id, is_active").eq("id", clean_uid).limit(1).execute()
                    if res_std.data and len(res_std.data) > 0:
                        status_dict = res_std.data[0]
                    else:
                        res_not_found = {
                            "user_id": clean_uid,
                            "account_status": "DENIED",
                            "is_active": False,
                            "exists": False,
                            "error": f"Account profile record not found for user ID '{clean_uid}'.",
                            "legal_hold": False,
                            "lifecycle_reason": "Account record does not exist.",
                            "status_updated_at": None,
                            "status_updated_by": None,
                            "deletion_requested_at": None,
                            "deletion_requested_by": None,
                            "deletion_scheduled_for": None,
                            "retention_notes": None,
                        }
                        return res_not_found
                except Exception as e2:
                    return {
                        "user_id": clean_uid,
                        "account_status": "DENIED",
                        "is_active": False,
                        "exists": False,
                        "error": f"Database schema configuration failure: {e2}",
                        "legal_hold": False,
                        "lifecycle_reason": "Database schema failure.",
                        "status_updated_at": None,
                        "status_updated_by": None,
                        "deletion_requested_at": None,
                        "deletion_requested_by": None,
                        "deletion_scheduled_for": None,
                        "retention_notes": None,
                    }
            else:
                # Network or database service failure in production backend:
                # STRICT RULE: Absolutely NO silent fallback to local SQLite in DATA_BACKEND=supabase!
                return {
                    "user_id": clean_uid,
                    "account_status": "DENIED",
                    "is_active": False,
                    "exists": False,
                    "error": f"Supabase backend unavailable: {e}",
                    "legal_hold": False,
                    "lifecycle_reason": "Backend connection failure.",
                    "status_updated_at": None,
                    "status_updated_by": None,
                    "deletion_requested_at": None,
                    "deletion_requested_by": None,
                    "deletion_scheduled_for": None,
                    "retention_notes": None,
                }
    else:
        # SQLite mode ONLY (DATA_BACKEND=sqlite)
        db = get_local_db()
        p = db.get_profile_by_id(clean_uid)
        if not p:
            res_not_found = {
                "user_id": clean_uid,
                "account_status": "DENIED",
                "is_active": False,
                "exists": False,
                "error": f"Account profile record not found in local database for user ID '{clean_uid}'.",
                "legal_hold": False,
                "lifecycle_reason": "Account record does not exist.",
                "status_updated_at": None,
                "status_updated_by": None,
                "deletion_requested_at": None,
                "deletion_requested_by": None,
                "deletion_scheduled_for": None,
                "retention_notes": None,
            }
            set_memo(cache_key, res_not_found, ttl_seconds=5)
            return res_not_found
        status_dict = p

    # Evaluate lifecycle state fail-closed
    raw_status = str(status_dict.get("account_status") or "").strip().upper()
    if raw_status and raw_status in VALID_ACCOUNT_STATUSES:
        final_status = raw_status
    elif not raw_status and "is_active" in status_dict:
        # Legacy pre-migration schema record: map directly from is_active
        is_act = bool(status_dict.get("is_active"))
        final_status = "ACTIVE" if is_act else "TEMPORARILY_SUSPENDED"
    else:
        # Corrupt or unknown lifecycle status string -> fail-closed DENIED
        return {
            "user_id": clean_uid,
            "account_status": "DENIED",
            "is_active": False,
            "exists": True,
            "error": f"Unknown or invalid account lifecycle state: '{raw_status}'. Access denied.",
            "legal_hold": False,
            "lifecycle_reason": "Invalid account lifecycle state.",
            "status_updated_at": None,
            "status_updated_by": None,
            "deletion_requested_at": None,
            "deletion_requested_by": None,
            "deletion_scheduled_for": None,
            "retention_notes": None,
        }

    is_act_flag = bool(status_dict.get("is_active", True))
    effective_active = bool(final_status == "ACTIVE" and is_act_flag)

    result = {
        "user_id": clean_uid,
        "account_status": final_status,
        "is_active": effective_active,
        "exists": True,
        "error": None,
        "legal_hold": bool(status_dict.get("legal_hold", False)),
        "lifecycle_reason": status_dict.get("status_reason") or status_dict.get("lifecycle_reason"),
        "status_reason": status_dict.get("status_reason"),
        "status_updated_at": status_dict.get("status_updated_at") or status_dict.get("updated_at"),
        "status_updated_by": status_dict.get("status_updated_by"),
        "deletion_requested_at": status_dict.get("deletion_requested_at"),
        "deletion_requested_by": status_dict.get("deletion_requested_by"),
        "deletion_scheduled_for": status_dict.get("deletion_scheduled_for"),
        "retention_notes": status_dict.get("retention_notes") or status_dict.get("status_reason"),
        "archived_at": status_dict.get("archived_at"),
        "restored_at": status_dict.get("restored_at"),
        "updated_at": status_dict.get("updated_at"),
    }

    set_memo(cache_key, result, ttl_seconds=10)
    return result


def is_account_active(user_id: str) -> Tuple[bool, Optional[str]]:
    """
    Fast boolean authorization gate. Returns (True, None) if account is ACTIVE.
    Returns (False, refusal_reason) if suspended, archived, scheduled for deletion, missing, or error.
    Strictly fail-closed.
    """
    if not user_id or not str(user_id).strip():
        return False, "Missing user ID."

    details = get_account_status(user_id)
    if not details.get("exists", True) or details.get("error"):
        err_msg = details.get("error") or "Account record not found or inaccessible."
        return False, f"Account access denied: {err_msg}"

    status = details.get("account_status")
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
        return False, f"Account is pending deletion review (scheduled review: {sched}). Ordinary operations are restricted."

    return False, f"Account access denied: Restricted lifecycle status '{status}'."


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
                "status_reason": reason.strip(),
                "updated_at": now_iso
            }).eq("id", user_id).execute()

            # Record audit log - fail closed if audit log cannot be persisted
            try:
                ins_log = admin.table("account_lifecycle_log").insert({
                    "id": str(uuid.uuid4()),
                    "user_id": user_id,
                    "actor_id": actor_id or SOLE_ADMIN_UUID,
                    "action": "SUSPEND",
                    "old_status": prev_status,
                    "new_status": "TEMPORARILY_SUSPENDED",
                    "reason": reason.strip(),
                    "details": {"timestamp": now_iso},
                    "created_at": now_iso
                }).execute()
                if not ins_log or not getattr(ins_log, "data", None):
                    admin.table("profiles").update({
                        "account_status": prev_status,
                        "is_active": True if prev_status == "ACTIVE" else False
                    }).eq("id", user_id).execute()
                    return False, "Failed to persist immutable lifecycle audit log. Suspension rolled back."
            except Exception as log_err:
                admin.table("profiles").update({
                    "account_status": prev_status,
                    "is_active": True if prev_status == "ACTIVE" else False
                }).eq("id", user_id).execute()
                return False, f"Failed to persist immutable lifecycle audit log: {log_err}. Suspension rolled back."
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
                "status_reason": note,
                "reactivated_at": now_iso,
                "updated_at": now_iso
            }).eq("id", user_id).execute()

            try:
                ins_log = admin.table("account_lifecycle_log").insert({
                    "id": str(uuid.uuid4()),
                    "user_id": user_id,
                    "actor_id": actor_id or SOLE_ADMIN_UUID,
                    "action": "RESUME",
                    "old_status": curr_status,
                    "new_status": "ACTIVE",
                    "reason": note,
                    "details": {"timestamp": now_iso},
                    "created_at": now_iso
                }).execute()
                if not ins_log or not getattr(ins_log, "data", None):
                    admin.table("profiles").update({
                        "account_status": curr_status,
                        "is_active": False
                    }).eq("id", user_id).execute()
                    return False, "Failed to persist immutable lifecycle audit log. Resume rolled back."
            except Exception as log_err:
                admin.table("profiles").update({
                    "account_status": curr_status,
                    "is_active": False
                }).eq("id", user_id).execute()
                return False, f"Failed to persist immutable lifecycle audit log: {log_err}. Resume rolled back."
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
    handover_errors = []

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
            ok_un, err_un = unassign_guide(
                aspirant_id=aid,
                guide_id=uid_str,
                admin_id=actor_id,
                reason=f"Account archived by Administration: {reason.strip()}"
            )
            if not ok_un:
                handover_errors.append(f"Guide unassignment failed for mentee {aid}: {err_un}")

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
            ok_un_sme, err_un_sme = unassign_sme(
                aspirant_id=aid,
                sme_id=uid_str,
                admin_id=actor_id,
                reason=f"Account archived by Administration: {reason.strip()}"
            )
            if not ok_un_sme:
                handover_errors.append(f"SME unassignment failed for mentee {aid}: {err_un_sme}")

    # P0 Safeguard: If any mentor unassignment or consultation transfer failed,
    # halt archival immediately to prevent orphaned caseloads!
    if handover_errors:
        return False, f"Archival aborted: Handover incomplete due to errors: {'; '.join(handover_errors)}"

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
                "status_reason": reason.strip(),
                "archived_at": now_iso,
                "updated_at": now_iso
            }).eq("id", user_id).execute()

            try:
                ins_log = admin.table("account_lifecycle_log").insert({
                    "id": str(uuid.uuid4()),
                    "user_id": user_id,
                    "actor_id": actor_id or SOLE_ADMIN_UUID,
                    "action": "ARCHIVE",
                    "old_status": prev_status,
                    "new_status": "ARCHIVED",
                    "reason": reason.strip(),
                    "details": {"timestamp": now_iso},
                    "created_at": now_iso
                }).execute()
                if not ins_log or not getattr(ins_log, "data", None):
                    admin.table("profiles").update({
                        "account_status": prev_status,
                        "is_active": True if prev_status == "ACTIVE" else False
                    }).eq("id", user_id).execute()
                    return False, "Failed to persist immutable lifecycle audit log. Archival rolled back."
            except Exception as log_err:
                admin.table("profiles").update({
                    "account_status": prev_status,
                    "is_active": True if prev_status == "ACTIVE" else False
                }).eq("id", user_id).execute()
                return False, f"Failed to persist immutable lifecycle audit log: {log_err}. Archival rolled back."
        except Exception as e:
            return False, f"Failed to archive account in Supabase: {e}"
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
        try:
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
        except Exception as e_log:
            db.update_account_status(
                user_id=user_id,
                status=prev_status,
                is_active=1 if prev_status == "ACTIVE" else 0,
                reason="Audit log failure rollback",
                actor_id=actor_id,
                updated_at=now_iso
            )
            return False, f"Failed to persist immutable lifecycle audit log: {e_log}. Archival rolled back."

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
                "status_reason": note,
                "restored_at": now_iso,
                "deletion_requested_at": None,
                "deletion_scheduled_for": None,
                "updated_at": now_iso
            }).eq("id", user_id).execute()

            try:
                ins_log = admin.table("account_lifecycle_log").insert({
                    "id": str(uuid.uuid4()),
                    "user_id": user_id,
                    "actor_id": actor_id or SOLE_ADMIN_UUID,
                    "action": "RESTORE",
                    "old_status": curr_status,
                    "new_status": "ACTIVE",
                    "reason": note,
                    "details": {"timestamp": now_iso},
                    "created_at": now_iso
                }).execute()
                if not ins_log or not getattr(ins_log, "data", None):
                    admin.table("profiles").update({
                        "account_status": curr_status,
                        "is_active": False
                    }).eq("id", user_id).execute()
                    return False, "Failed to persist immutable lifecycle audit log. Restoration rolled back."
            except Exception as log_err:
                admin.table("profiles").update({
                    "account_status": curr_status,
                    "is_active": False
                }).eq("id", user_id).execute()
                return False, f"Failed to persist immutable lifecycle audit log: {log_err}. Restoration rolled back."
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
                "deletion_scheduled_for": scheduled_for,
                "grace_period_days": max(1, grace_days),
                "status_reason": note,
                "updated_at": now_iso
            }).eq("id", user_id).execute()

            try:
                ins_log = admin.table("account_lifecycle_log").insert({
                    "id": str(uuid.uuid4()),
                    "user_id": user_id,
                    "actor_id": actor_id or user_id,
                    "action": "REQUEST_DELETION",
                    "old_status": curr_details.get("account_status", "ACTIVE"),
                    "new_status": "PENDING_DELETION",
                    "reason": note,
                    "details": {"scheduled_for": scheduled_for, "grace_days": grace_days, "requested_by": actor_id},
                    "created_at": now_iso
                }).execute()
                if not ins_log or not getattr(ins_log, "data", None):
                    admin.table("profiles").update({
                        "account_status": curr_details.get("account_status", "ACTIVE"),
                        "deletion_requested_at": None,
                        "deletion_requested_by": None,
                        "deletion_scheduled_for": None
                    }).eq("id", user_id).execute()
                    return False, "Failed to persist immutable audit log in Supabase. Deletion request rolled back."
            except Exception as log_err:
                admin.table("profiles").update({
                    "account_status": curr_details.get("account_status", "ACTIVE"),
                    "deletion_requested_at": None,
                    "deletion_requested_by": None,
                    "deletion_scheduled_for": None
                }).eq("id", user_id).execute()
                return False, f"Failed to persist immutable audit log: {log_err}. Deletion request rolled back."
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
            "metadata": json.dumps({"scheduled_for": str(scheduled_for), "grace_days": grace_days}),
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
                "deletion_scheduled_for": None,
                "status_reason": note,
                "updated_at": now_iso
            }).eq("id", user_id).execute()

            try:
                ins_log = admin.table("account_lifecycle_log").insert({
                    "id": str(uuid.uuid4()),
                    "user_id": user_id,
                    "actor_id": actor_id or user_id,
                    "action": "CANCEL_DELETION",
                    "old_status": "PENDING_DELETION",
                    "new_status": "ACTIVE",
                    "reason": note,
                    "details": {"timestamp": now_iso},
                    "created_at": now_iso
                }).execute()
                if not ins_log or not getattr(ins_log, "data", None):
                    admin.table("profiles").update({
                        "account_status": "PENDING_DELETION",
                        "deletion_requested_at": curr_details.get("deletion_requested_at"),
                        "deletion_scheduled_for": curr_details.get("deletion_scheduled_for")
                    }).eq("id", user_id).execute()
                    return False, "Failed to persist immutable audit log in Supabase. Cancellation rolled back."
            except Exception as log_err:
                admin.table("profiles").update({
                    "account_status": "PENDING_DELETION",
                    "deletion_requested_at": curr_details.get("deletion_requested_at"),
                    "deletion_scheduled_for": curr_details.get("deletion_scheduled_for")
                }).eq("id", user_id).execute()
                return False, f"Failed to persist immutable audit log: {log_err}. Cancellation rolled back."
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
                "status_reason": f"Legal hold {'applied' if enabled else 'released'}: {reason.strip()}",
                "updated_at": now_iso
            }).eq("id", user_id).execute()

            try:
                admin.table("account_lifecycle_log").insert({
                    "id": str(uuid.uuid4()),
                    "user_id": user_id,
                    "actor_id": actor_id or SOLE_ADMIN_UUID,
                    "action": action_label,
                    "old_status": curr_status,
                    "new_status": curr_status,
                    "reason": reason.strip(),
                    "details": {"legal_hold": enabled, "notes": reason.strip()},
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
            "metadata": json.dumps({"legal_hold": bool(enabled)}),
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
                if res.data:
                    normalized = []
                    for row in res.data:
                        r = dict(row)
                        r["previous_status"] = r.get("previous_status") or r.get("old_status") or "ACTIVE"
                        r["metadata"] = r.get("metadata") or r.get("details") or {}
                        normalized.append(r)
                    return normalized
                return []
            except Exception as e:
                print(f"[AccountLifecycle] Log fetch notice: {e}")
                return []
        return []
    else:
        db = get_local_db()
        if hasattr(db, "list_account_lifecycle_logs"):
            return db.list_account_lifecycle_logs(user_id=user_id, limit=limit)
        return []


def list_accounts_by_status(status_filter: Optional[str] = None) -> List[Dict]:
    """
    Retrieves all accounts annotated with current lifecycle status, legal hold, and role tags.
    """
    from services.roles import list_users_with_multi_roles
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

