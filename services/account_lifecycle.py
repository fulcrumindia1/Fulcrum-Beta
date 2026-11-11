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

import re
import uuid
import json
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, List, Tuple, Set, Any

from services.auth import get_supabase_admin_client, get_supabase_client, get_data_backend
from services.local_db import get_local_db
from services.cache import get_memo, set_memo, invalidate_memo
import services.roles as roles_mod

SOLE_ADMIN_EMAIL = "fulcrumindia1@gmail.com"
SOLE_ADMIN_UUID = "616304b5-aef5-4cd0-88be-2fda7ddf7f88"

def require_sole_admin(*args, **kwargs):
    return roles_mod.require_sole_admin(*args, **kwargs)

def is_strict_admin(*args, **kwargs):
    return roles_mod.is_strict_admin(*args, **kwargs)

def get_user_roles(*args, **kwargs):
    return roles_mod.get_user_roles(*args, **kwargs)

def get_configured_admin_uuid(*args, **kwargs):
    return roles_mod.get_configured_admin_uuid(*args, **kwargs)


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


# Runtime schema cache & PostgREST column compatibility helpers (supports both
# live pre-009 status_reason/old_status/details schema and Migration 009 columns)
_UNSUPPORTED_COLS_CACHE: Dict[str, Set[str]] = {}

_PROFILE_COL_ALIASES: Dict[str, Optional[str]] = {
    "lifecycle_reason": "status_reason",
    "status_reason": "lifecycle_reason",
    "retention_notes": "status_reason",
    "status_updated_at": "updated_at",
    "status_updated_by": None,
    "deletion_requested_by": None,
    "archived_at": None,
    "restored_at": None,
    "reactivated_at": None,
}

_LOG_COL_ALIASES: Dict[str, Optional[str]] = {
    "previous_status": "old_status",
    "old_status": "previous_status",
    "metadata": "details",
    "details": "metadata",
}


def _extract_missing_col_name(err_msg: str) -> Optional[str]:
    """Parses missing column identifier from PostgREST PGRST204 or Postgres 42703 messages."""
    for pat in (
        r"Could not find the ['\"]([a-zA-Z0-9_]+)['\"] column",
        r'column\s+"?([a-zA-Z0-9_]+)"?\s+(?:of relation|does not exist)',
        r"\.([a-zA-Z0-9_]+)\s+does not exist",
    ):
        m = re.search(pat, err_msg, re.IGNORECASE)
        if m:
            return m.group(1)
    return None


def _execute_supabase_adaptive(
    admin: Any,
    table_name: str,
    op: str,
    payload: Dict[str, Any],
    eq_col: Optional[str] = None,
    eq_val: Optional[Any] = None,
    col_aliases: Optional[Dict[str, Optional[str]]] = None,
) -> Any:
    """Executes insert/update adaptively, caching PostgREST PGRST204 unsupported columns and remapping aliases."""
    aliases = col_aliases or {}
    unsupported = _UNSUPPORTED_COLS_CACHE.setdefault(table_name, set())

    current: Dict[str, Any] = {}
    for k, v in payload.items():
        if k in unsupported:
            mapped = aliases.get(k)
            if mapped and mapped not in unsupported:
                current.setdefault(mapped, v)
            continue
        current[k] = v

    if not current:
        current = dict(payload)

    tried_cols: Set[str] = set(current.keys())
    max_attempts = max(3, len(current) + 6)
    for _ in range(max_attempts):
        try:
            tbl = admin.table(table_name)
            q = tbl.update(current).eq(eq_col, eq_val) if op == "update" else tbl.insert(current)
            return q.execute()
        except Exception as err:
            err_str = str(err)
            is_col_err = (
                "PGRST204" in err_str
                or "42703" in err_str
                or "Could not find the" in err_str
                or ("column" in err_str.lower() and "exist" in err_str.lower())
            )
            bad_col = _extract_missing_col_name(err_str) if is_col_err else None
            if not bad_col or bad_col not in current:
                raise
            unsupported.add(bad_col)
            removed_val = current.pop(bad_col)
            mapped = aliases.get(bad_col)
            if mapped and mapped not in unsupported and mapped not in tried_cols:
                tried_cols.add(mapped)
                current.setdefault(mapped, removed_val)
            # Fold stripped audit metadata safely into details/metadata payload when logging
            if table_name == "account_lifecycle_log" and bad_col not in aliases:
                detail_key = "details" if "details" in current else ("metadata" if "metadata" in current else None)
                if detail_key and isinstance(current.get(detail_key), dict):
                    current[detail_key][bad_col] = removed_val
            if not current:
                raise
    raise RuntimeError(f"Adaptive Supabase {op} exhausted retries on {table_name}.")


def _build_profile_lifecycle_payload(
    admin: Any,
    account_status: Optional[str] = None,
    is_active: Optional[bool] = None,
    reason: Optional[str] = None,
    actor_id: Optional[str] = None,
    now_iso: Optional[str] = None,
    action: Optional[str] = None,
    legal_hold: Optional[bool] = None,
    retention_notes: Optional[str] = None,
    deletion_requested_at: Optional[str] = None,
    deletion_requested_by: Optional[str] = None,
    deletion_scheduled_for: Optional[str] = None,
    clear_deletion: bool = False,
) -> Dict[str, Any]:
    """Builds a profile lifecycle update dict using verified or canonical column names."""
    unsupported = _UNSUPPORTED_COLS_CACHE.get("profiles", set())
    payload: Dict[str, Any] = {}
    if account_status is not None:
        payload["account_status"] = account_status
    if is_active is not None:
        payload["is_active"] = is_active
    if reason is not None:
        if "lifecycle_reason" in unsupported and "status_reason" not in unsupported:
            payload["status_reason"] = reason
        else:
            payload["lifecycle_reason"] = reason
    if retention_notes is not None:
        payload["retention_notes"] = retention_notes
    if legal_hold is not None:
        payload["legal_hold"] = legal_hold
    if now_iso:
        payload["status_updated_at"] = now_iso
        payload["updated_at"] = now_iso
        if action == "ARCHIVE":
            payload["archived_at"] = now_iso
        elif action == "RESTORE":
            payload["restored_at"] = now_iso
            payload["reactivated_at"] = now_iso
        elif action == "RESUME":
            payload["reactivated_at"] = now_iso
    if actor_id:
        payload["status_updated_by"] = actor_id
    if clear_deletion:
        payload["deletion_requested_at"] = None
        payload["deletion_requested_by"] = None
        payload["deletion_scheduled_for"] = None
    else:
        if deletion_requested_at is not None:
            payload["deletion_requested_at"] = deletion_requested_at
        if deletion_requested_by is not None:
            payload["deletion_requested_by"] = deletion_requested_by
        if deletion_scheduled_for is not None:
            payload["deletion_scheduled_for"] = deletion_scheduled_for
    return payload


def _supabase_update_and_log(
    admin: Any,
    user_id: str,
    actor_id: Optional[str],
    action: str,
    prev_status: str,
    new_status: str,
    reason: str,
    profile_payload: Dict[str, Any],
    rollback_payload: Dict[str, Any],
    now_iso: str,
    log_metadata: Optional[Dict[str, Any]] = None,
    strict_log: bool = True,
    rollback_label: str = "Action",
) -> Tuple[bool, Optional[str]]:
    """Executes profile lifecycle update + immutable audit log insert with rollback on failure."""
    _execute_supabase_adaptive(
        admin,
        "profiles",
        "update",
        profile_payload,
        eq_col="id",
        eq_val=user_id,
        col_aliases=_PROFILE_COL_ALIASES,
    )
    meta_dict = dict(log_metadata or {"timestamp": now_iso})
    meta_dict.setdefault("actor_id", actor_id or get_configured_admin_uuid())
    log_payload = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "actor_id": actor_id or get_configured_admin_uuid(),
        "action": action,
        "previous_status": prev_status,
        "new_status": new_status,
        "reason": reason,
        "metadata": meta_dict,
        "created_at": now_iso,
    }
    try:
        ins_log = _execute_supabase_adaptive(
            admin,
            "account_lifecycle_log",
            "insert",
            log_payload,
            col_aliases=_LOG_COL_ALIASES,
        )
        if strict_log and (not ins_log or not getattr(ins_log, "data", None)):
            _execute_supabase_adaptive(
                admin, "profiles", "update", rollback_payload,
                eq_col="id", eq_val=user_id, col_aliases=_PROFILE_COL_ALIASES,
            )
            return False, f"Failed to persist immutable lifecycle audit log. {rollback_label} rolled back."
    except Exception as log_err:
        if not strict_log:
            print(f"[AccountLifecycle] Audit log write notice: {log_err}")
            return True, None
        _execute_supabase_adaptive(
            admin, "profiles", "update", rollback_payload,
            eq_col="id", eq_val=user_id, col_aliases=_PROFILE_COL_ALIASES,
        )
        return False, f"Failed to persist immutable lifecycle audit log: {log_err}. {rollback_label} rolled back."
    return True, None


def _restore_relationship_snapshots(snapshots: List[Dict[str, Any]]) -> None:
    """Compensating rollback restoring prior mentor assignments if archival fails."""
    if not snapshots:
        return
    backend = get_data_backend()
    now_iso = datetime.now(timezone.utc).isoformat()
    if backend == "supabase":
        admin = get_supabase_admin_client()
        if admin:
            for snap in snapshots:
                try:
                    admin.table("relationships").update({
                        "guide_id": snap.get("guide_id"),
                        "guide_ids": snap.get("guide_ids", []),
                        "sme_id": snap.get("sme_id"),
                        "sme_ids": snap.get("sme_ids", []),
                        "updated_at": now_iso,
                    }).eq("aspirant_id", snap["aspirant_id"]).execute()
                except Exception as ex_r:
                    print(f"[AccountLifecycle] Relationship rollback notice for {snap.get('aspirant_id')}: {ex_r}")
    else:
        db = get_local_db()
        conn = db._get_conn()
        cur = conn.cursor()
        for snap in snapshots:
            cur.execute(
                """
                UPDATE relationships
                SET guide_id = ?, guide_ids = ?, sme_id = ?, sme_ids = ?, updated_at = ?
                WHERE aspirant_id = ?
                """,
                (
                    snap.get("guide_id"),
                    json.dumps(snap.get("guide_ids", [])),
                    snap.get("sme_id"),
                    json.dumps(snap.get("sme_ids", [])),
                    now_iso,
                    snap["aspirant_id"],
                ),
            )
        conn.commit()
        conn.close()
    invalidate_memo("all_relationships")
    for snap in snapshots:
        invalidate_memo(f"mentors:{snap['aspirant_id']}")


def get_account_status(user_id: str, prefetched_profile: Optional[Dict] = None) -> Dict:
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

    if (
        isinstance(prefetched_profile, dict)
        and str(prefetched_profile.get("id") or "") == clean_uid
        and ("is_active" in prefetched_profile or "account_status" in prefetched_profile)
    ):
        status_dict = prefetched_profile
    elif backend == "supabase":
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
                "id, is_active, account_status, legal_hold, lifecycle_reason, "
                "deletion_requested_at, deletion_requested_by, deletion_scheduled_for, status_updated_at, status_updated_by, retention_notes, updated_at"
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
            # If migration 009 columns differ from live schema, retry SELECT * before minimal fields
            if "column" in err_str or "does not exist" in err_str or "42703" in err_str or "pgrst204" in err_str:
                try:
                    try:
                        res_std = admin.table("profiles").select("*").eq("id", clean_uid).limit(1).execute()
                    except Exception:
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
            eff_actor = actor_id or get_configured_admin_uuid()
            prof_payload = _build_profile_lifecycle_payload(
                admin,
                account_status="TEMPORARILY_SUSPENDED",
                is_active=False,
                reason=reason.strip(),
                actor_id=eff_actor,
                now_iso=now_iso,
                action="SUSPEND",
            )
            rb_payload = {
                "account_status": prev_status,
                "is_active": True if prev_status == "ACTIVE" else False,
            }
            ok_tx, err_tx = _supabase_update_and_log(
                admin=admin,
                user_id=user_id,
                actor_id=eff_actor,
                action="SUSPEND",
                prev_status=prev_status,
                new_status="TEMPORARILY_SUSPENDED",
                reason=reason.strip(),
                profile_payload=prof_payload,
                rollback_payload=rb_payload,
                now_iso=now_iso,
                rollback_label="Suspension",
            )
            if not ok_tx:
                return False, err_tx
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
            eff_actor = actor_id or get_configured_admin_uuid()
            prof_payload = _build_profile_lifecycle_payload(
                admin,
                account_status="ACTIVE",
                is_active=True,
                reason=note,
                actor_id=eff_actor,
                now_iso=now_iso,
                action="RESUME",
            )
            ok_tx, err_tx = _supabase_update_and_log(
                admin=admin,
                user_id=user_id,
                actor_id=eff_actor,
                action="RESUME",
                prev_status=curr_status,
                new_status="ACTIVE",
                reason=note,
                profile_payload=prof_payload,
                rollback_payload={"account_status": curr_status, "is_active": False},
                now_iso=now_iso,
                rollback_label="Resume",
            )
            if not ok_tx:
                return False, err_tx
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
    modified_snapshots: Dict[str, Dict[str, Any]] = {}

    for rel in rels:
        aid = rel.get("aspirant_id")
        if not aid or rel.get("status") != "active":
            continue

        # Handle Guide unassignment
        raw_gids = rel.get("guide_ids") or []
        if isinstance(raw_gids, str):
            try: raw_gids = json.loads(raw_gids)
            except Exception: raw_gids = [raw_gids]
        orig_gids = [str(g) for g in raw_gids if g]
        if rel.get("guide_id") and rel["guide_id"] not in raw_gids:
            raw_gids.insert(0, rel["guide_id"])
        guides_set = {str(gid) for gid in raw_gids if gid}

        # Handle SME unassignment (collect original list before mutating)
        raw_sids = rel.get("sme_ids") or []
        if isinstance(raw_sids, str):
            try: raw_sids = json.loads(raw_sids)
            except Exception: raw_sids = [raw_sids]
        orig_sids = [str(s) for s in raw_sids if s]
        if rel.get("sme_id") and rel["sme_id"] not in raw_sids:
            raw_sids.insert(0, rel["sme_id"])
        smes_set = {str(sid) for sid in raw_sids if sid}

        snap_before = {
            "aspirant_id": aid,
            "guide_id": rel.get("guide_id"),
            "guide_ids": orig_gids,
            "sme_id": rel.get("sme_id"),
            "sme_ids": orig_sids,
        }

        if uid_str in guides_set:
            ok_un, err_un = unassign_guide(
                aspirant_id=aid,
                guide_id=uid_str,
                admin_id=actor_id,
                reason=f"Account archived by Administration: {reason.strip()}"
            )
            if ok_un:
                modified_snapshots.setdefault(aid, snap_before)
            else:
                handover_errors.append(f"Guide unassignment failed for mentee {aid}: {err_un}")

        if uid_str in smes_set:
            ok_un_sme, err_un_sme = unassign_sme(
                aspirant_id=aid,
                sme_id=uid_str,
                admin_id=actor_id,
                reason=f"Account archived by Administration: {reason.strip()}"
            )
            if ok_un_sme:
                modified_snapshots.setdefault(aid, snap_before)
            else:
                handover_errors.append(f"SME unassignment failed for mentee {aid}: {err_un_sme}")

    # P0 Safeguard: If any mentor unassignment or consultation transfer failed,
    # halt archival immediately and restore any partial handover mutations!
    if handover_errors:
        _restore_relationship_snapshots(list(modified_snapshots.values()))
        return False, f"Archival aborted: Handover incomplete due to errors: {'; '.join(handover_errors)}"

    # Update account status in persistence layer
    backend = get_data_backend()
    if backend == "supabase":
        admin = get_supabase_admin_client()
        if not admin:
            _restore_relationship_snapshots(list(modified_snapshots.values()))
            return False, "Supabase admin client unavailable."
        try:
            eff_actor = actor_id or get_configured_admin_uuid()
            prof_payload = _build_profile_lifecycle_payload(
                admin,
                account_status="ARCHIVED",
                is_active=False,
                reason=reason.strip(),
                actor_id=eff_actor,
                now_iso=now_iso,
                action="ARCHIVE",
            )
            rb_payload = {
                "account_status": prev_status,
                "is_active": True if prev_status == "ACTIVE" else False,
            }
            ok_tx, err_tx = _supabase_update_and_log(
                admin=admin,
                user_id=user_id,
                actor_id=eff_actor,
                action="ARCHIVE",
                prev_status=prev_status,
                new_status="ARCHIVED",
                reason=reason.strip(),
                profile_payload=prof_payload,
                rollback_payload=rb_payload,
                now_iso=now_iso,
                rollback_label="Archival",
            )
            if not ok_tx:
                _restore_relationship_snapshots(list(modified_snapshots.values()))
                return False, err_tx
        except Exception as e:
            _restore_relationship_snapshots(list(modified_snapshots.values()))
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
            _restore_relationship_snapshots(list(modified_snapshots.values()))
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
            eff_actor = actor_id or get_configured_admin_uuid()
            prof_payload = _build_profile_lifecycle_payload(
                admin,
                account_status="ACTIVE",
                is_active=True,
                reason=note,
                actor_id=eff_actor,
                now_iso=now_iso,
                action="RESTORE",
                clear_deletion=True,
            )
            ok_tx, err_tx = _supabase_update_and_log(
                admin=admin,
                user_id=user_id,
                actor_id=eff_actor,
                action="RESTORE",
                prev_status=curr_status,
                new_status="ACTIVE",
                reason=note,
                profile_payload=prof_payload,
                rollback_payload={"account_status": curr_status, "is_active": False},
                now_iso=now_iso,
                rollback_label="Restoration",
            )
            if not ok_tx:
                return False, err_tx
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
            eff_actor = actor_id or user_id
            prev_st = curr_details.get("account_status", "ACTIVE")
            prof_payload = _build_profile_lifecycle_payload(
                admin,
                account_status="PENDING_DELETION",
                reason=note,
                actor_id=eff_actor,
                now_iso=now_iso,
                action="REQUEST_DELETION",
                deletion_requested_at=now_iso,
                deletion_requested_by=eff_actor,
                deletion_scheduled_for=scheduled_for,
            )
            rb_payload = {
                "account_status": prev_st,
                "deletion_requested_at": None,
                "deletion_requested_by": None,
                "deletion_scheduled_for": None,
            }
            ok_tx, err_tx = _supabase_update_and_log(
                admin=admin,
                user_id=user_id,
                actor_id=eff_actor,
                action="REQUEST_DELETION",
                prev_status=prev_st,
                new_status="PENDING_DELETION",
                reason=note,
                profile_payload=prof_payload,
                rollback_payload=rb_payload,
                now_iso=now_iso,
                log_metadata={"scheduled_for": scheduled_for, "grace_days": grace_days, "requested_by": actor_id},
                rollback_label="Deletion request",
            )
            if not ok_tx:
                return False, err_tx
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
            eff_actor = actor_id or user_id
            prof_payload = _build_profile_lifecycle_payload(
                admin,
                account_status="ACTIVE",
                is_active=True,
                reason=note,
                actor_id=eff_actor,
                now_iso=now_iso,
                action="CANCEL_DELETION",
                clear_deletion=True,
            )
            rb_payload = {
                "account_status": "PENDING_DELETION",
                "deletion_requested_at": curr_details.get("deletion_requested_at"),
                "deletion_scheduled_for": curr_details.get("deletion_scheduled_for"),
            }
            ok_tx, err_tx = _supabase_update_and_log(
                admin=admin,
                user_id=user_id,
                actor_id=eff_actor,
                action="CANCEL_DELETION",
                prev_status="PENDING_DELETION",
                new_status="ACTIVE",
                reason=note,
                profile_payload=prof_payload,
                rollback_payload=rb_payload,
                now_iso=now_iso,
                rollback_label="Cancellation",
            )
            if not ok_tx:
                return False, err_tx
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
            eff_actor = actor_id or get_configured_admin_uuid()
            hold_reason = f"Legal hold {'applied' if enabled else 'released'}: {reason.strip()}"
            prof_payload = _build_profile_lifecycle_payload(
                admin,
                legal_hold=enabled,
                reason=hold_reason,
                retention_notes=reason.strip(),
                actor_id=eff_actor,
                now_iso=now_iso,
                action=action_label,
            )
            _supabase_update_and_log(
                admin=admin,
                user_id=user_id,
                actor_id=eff_actor,
                action=action_label,
                prev_status=curr_status,
                new_status=curr_status,
                reason=reason.strip(),
                profile_payload=prof_payload,
                rollback_payload={"legal_hold": not enabled},
                now_iso=now_iso,
                log_metadata={"legal_hold": enabled, "notes": reason.strip()},
                strict_log=False,
                rollback_label="Legal hold",
            )
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

