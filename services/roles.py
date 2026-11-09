"""
services/roles.py — Multi-Role Identity & Normalized Role Grants Engine
=======================================================================
Supports: One User Identity -> Multiple Independent Roles (Aspirant, Guide, SME, Admin).
Preserves backward compatibility with profiles.role while maintaining
normalized role grants, audit timestamps, and NDA gating.
"""

import json
from datetime import datetime, timezone
from typing import Optional, Dict, List, Tuple
from services.auth import get_supabase_client, get_supabase_admin_client, get_data_backend
from services.local_db import get_local_db
from services.cache import get_memo, set_memo, invalidate_memo

VALID_GRANTABLE_ROLES = ("aspirant", "guide", "sme")
VALID_ROLES = ("aspirant", "guide", "sme", "admin")
VALID_STATUSES = ("active", "pending_nda", "suspended", "revoked")

SOLE_ADMIN_EMAIL = "fulcrumindia1@gmail.com"
SOLE_ADMIN_UUID = "616304b5-aef5-4cd0-88be-2fda7ddf7f88"


def is_strict_admin(
    user_id: Optional[str] = None,
    email: Optional[str] = None,
    user_dict: Optional[dict] = None,
) -> bool:
    """
    Canonical Single-Admin Identity Gate.
    Returns True ONLY when the identity is verified to belong to fulcrumindia1@gmail.com
    (UUID: 616304b5-aef5-4cd0-88be-2fda7ddf7f88).
    Never trusts profiles.role == 'admin', district_admin, operational_admin,
    or user_metadata.role alone.
    Never trusts a caller-supplied email alone without verified matching UUID.
    """
    if isinstance(user_dict, dict):
        user_id = user_id or user_dict.get("id")
        email = email or user_dict.get("email")

    clean_email = str(email or "").strip().lower()
    clean_uid = str(user_id or "").strip().lower()

    # If neither user_id nor email was supplied, inspect the active session context
    if not clean_uid and not clean_email:
        try:
            import streamlit as st
            sess_u = st.session_state.get("user") or {}
            clean_uid = str(sess_u.get("id") or "").strip().lower()
            clean_email = str(sess_u.get("email") or "").strip().lower()
        except Exception:
            pass

    # If email is explicitly provided and is NOT fulcrumindia1@gmail.com, deny immediately
    if clean_email and clean_email != SOLE_ADMIN_EMAIL:
        return False

    # If UUID is explicitly provided and is NOT SOLE_ADMIN_UUID, deny immediately
    if clean_uid and clean_uid != SOLE_ADMIN_UUID:
        return False

    # Positive match on verified Sole Admin UUID
    if clean_uid == SOLE_ADMIN_UUID:
        if clean_email and clean_email != SOLE_ADMIN_EMAIL:
            return False
        return True

    # If only email was passed without UUID, verify the persistent profile actually bears SOLE_ADMIN_UUID
    if clean_email == SOLE_ADMIN_EMAIL and not clean_uid:
        try:
            from services.profiles import get_profile_by_email
            p = get_profile_by_email(clean_email)
            if p and str(p.get("id") or "").strip().lower() == SOLE_ADMIN_UUID:
                return True
        except Exception:
            pass

    return False


def require_sole_admin(
    actor_id: Optional[str] = None,
    actor_dict: Optional[dict] = None
) -> Tuple[bool, Optional[str]]:
    """
    Server-side authorization gate for privileged administrative mutations.
    Enforces that only the verified Sole Platform Administrator (fulcrumindia1@gmail.com)
    can execute administrative actions. Rejects unauthorized or spoofed requests.
    """
    if is_strict_admin(user_id=actor_id, user_dict=actor_dict):
        return True, None
    return False, "Unauthorized: Only the Sole Platform Administrator (fulcrumindia1@gmail.com) has authority to perform this action."


def _get_admin_client():
    return get_supabase_admin_client()


def _get_user_client():
    return get_supabase_client()


def _invalidate_role_caches(user_id: str) -> None:
    """Invalidates all per-user and directory role caches upon role grant/status mutation."""
    invalidate_memo(f"user_roles:{user_id}")
    invalidate_memo(f"guide_aspirants:{user_id}")
    invalidate_memo(f"sme_aspirants:{user_id}")
    invalidate_memo("multi_role_users")
    invalidate_memo("active_profiles_for_role:")
    invalidate_memo("list_profiles_by_role:")
    invalidate_memo("mentors:")


def get_user_roles(user_id: str) -> List[Dict]:
    """Retrieves all role grant records for a user."""
    if not user_id:
        return []

    cache_key = f"user_roles:{user_id}"
    cached = get_memo(cache_key)
    if cached is not None:
        return cached

    backend = get_data_backend()
    roles = []

    if backend == "supabase":
        client = _get_admin_client() or _get_user_client()
        if client:
            try:
                res = client.table("user_roles").select("*").eq("user_id", user_id).execute()
                roles = res.data or []
            except Exception as e:
                print(f"[Roles] Supabase user_roles fetch notice for {user_id}: {e}")
                roles = []
    else:
        # Check SQLite ONLY when DATA_BACKEND=sqlite
        db = get_local_db()
        roles = db.get_user_roles(user_id) if hasattr(db, "get_user_roles") else []

    # Ensure the user's primary/registered role is included if no explicit multi-role grants exist
    from services.profiles import get_profile
    p = get_profile(user_id)
    user_email = str(p.get("email", "")).strip().lower() if p else ""
    is_platform_admin = is_strict_admin(user_id=user_id, email=user_email)

    if not is_platform_admin:
        # Strip any unauthorized admin/district_admin/operational_admin grants from non-primary accounts
        roles = [
            r for r in roles
            if str(r.get("role", "")).strip().lower() not in ("admin", "district_admin", "operational_admin")
        ]

    if p:
        base_role = str(p.get("role", "aspirant")).strip().lower()
        if not is_platform_admin and base_role in ("admin", "district_admin", "operational_admin"):
            base_role = "aspirant"

        if is_platform_admin:
            # Single Platform Admin is strictly an Admin, NEVER an Aspirant
            roles = [r for r in roles if r.get("role") != "aspirant"]
            if not any(r.get("role") == "admin" for r in roles):
                roles.append({
                    "id": f"role_{user_id}_admin",
                    "user_id": user_id,
                    "role": "admin",
                    "status": "active",
                    "granted_at": p.get("created_at"),
                    "activated_at": p.get("created_at")
                })
        else:
            # For entrepreneurs and mentors, ensure base registered role is present
            # BUT never resurrect a role that was explicitly revoked or suspended
            existing_base = next((r for r in roles if r.get("role") == base_role), None)
            if not existing_base:
                roles.append({
                    "id": f"role_{user_id}_{base_role}",
                    "user_id": user_id,
                    "role": base_role,
                    "status": "active",
                    "granted_at": p.get("created_at"),
                    "activated_at": p.get("created_at")
                })

    set_memo(cache_key, roles, ttl_seconds=5)
    return roles


def get_active_roles(user_id: str) -> List[str]:
    """Returns list of currently active role strings for a user."""
    all_grants = get_user_roles(user_id)
    return [g["role"] for g in all_grants if g.get("status") == "active"]


def get_pending_nda_roles(user_id: str) -> List[str]:
    """Returns list of roles awaiting NDA acceptance for a user."""
    all_grants = get_user_roles(user_id)
    return [g["role"] for g in all_grants if g.get("status") == "pending_nda"]


def user_has_active_role(user_id: str, role: str) -> bool:
    """Strict authorization check: True ONLY if user holds this role with status 'active'."""
    return role in get_active_roles(user_id)


def grant_role(
    user_id: str,
    role: str,
    granted_by: Optional[str] = None,
    require_nda: Optional[bool] = None
) -> Tuple[bool, Optional[str]]:
    """
    Grants a role to a user.
    Single Admin rule: Only 'guide' and 'sme' can be granted via administration.
    Strict Rule: When promoting to Guide or SME, status defaults to 'pending_nda'
    unless explicit non-NDA status is authorized.
    Requires verified Sole Admin authorization.
    """
    ok_admin, err_admin = require_sole_admin(actor_id=granted_by)
    if not ok_admin:
        return False, err_admin

    if role not in VALID_GRANTABLE_ROLES:
        return False, f"Unauthorized: Only {VALID_GRANTABLE_ROLES} can be granted via Fulcrum Administration."

    if not user_id:
        return False, "User ID is required."

    # Determine initial status: Guide and SME require NDA acceptance
    if require_nda is None:
        initial_status = "pending_nda" if role in ("guide", "sme") else "active"
    else:
        initial_status = "pending_nda" if require_nda else "active"

    now_iso = datetime.now(timezone.utc).isoformat()
    backend = get_data_backend()

    record = {
        "user_id": user_id,
        "role": role,
        "status": initial_status,
        "granted_by": granted_by,
        "granted_at": now_iso,
        "activated_at": now_iso if initial_status == "active" else None,
        "suspended_at": None,
        "revoked_at": None,
        "revocation_reason": None,
        "updated_at": now_iso
    }

    if backend == "supabase":
        admin = _get_admin_client()
        if not admin:
            return False, "Supabase admin client unavailable."
        try:
            admin.table("user_roles").upsert(record, on_conflict="user_id, role").execute()
        except Exception as e:
            return False, f"Supabase error granting role: {e}"
        _invalidate_role_caches(user_id)
    else:
        # SQLite Mode ONLY
        db = get_local_db()
        if hasattr(db, "upsert_user_role"):
            db.upsert_user_role(record)
        _invalidate_role_caches(user_id)

    try:
        from services.notifications import create_notification
        from services.governance import get_primary_admin_id
        role_display = "Guide" if role == "guide" else ("Domain SME" if role == "sme" else role.capitalize())
        nda_msg = " Please switch to your new workspace and accept the Confidentiality & Non-Disclosure Agreement (NDA) to activate access." if initial_status == "pending_nda" else ""
        create_notification(
            user_id=user_id,
            title=f"New Role Granted: {role_display}",
            message=f"You have been granted the {role_display} role on Fulcrum.{nda_msg}",
            notification_type="role_granted",
            actor_id=granted_by or get_primary_admin_id()
        )
    except Exception as e:
        print(f"[Roles] Grant notification notice: {e}")

    return True, None


# Alias for backward/blueprint compatibility
assign_user_role = grant_role


def activate_role(user_id: str, role: str) -> Tuple[bool, Optional[str]]:
    """Activates a role grant after verifying NDA compliance. Strictly refuses to activate revoked roles."""
    if not user_id:
        return False, "User ID is required."

    # Safety check: Never activate an explicitly revoked role grant
    existing_roles = get_user_roles(user_id)
    grant = next((r for r in existing_roles if r.get("role") == role), None)
    if grant and grant.get("status") == "revoked":
        return False, f"Cannot activate: The {role.upper()} role grant was explicitly revoked by Administration. Re-granting is required."

    # Legal integrity: Guide and SME roles strictly require a verified signed NDA
    if role in ("guide", "sme"):
        from services.legal import check_user_nda_accepted
        if not check_user_nda_accepted(user_id, role):
            return False, f"Cannot activate {role.upper()}: A verified Non-Disclosure Agreement (NDA) has not been executed."

    now_iso = datetime.now(timezone.utc).isoformat()
    backend = get_data_backend()

    if backend == "supabase":
        admin = _get_admin_client()
        if not admin:
            return False, "Supabase admin client unavailable."
        try:
            res = admin.table("user_roles").update({
                "status": "active",
                "activated_at": now_iso,
                "updated_at": now_iso
            }).eq("user_id", user_id).eq("role", role).neq("status", "revoked").execute()
            if not res.data:
                return False, f"Role activation failed in Supabase: No pending grant found for role '{role}' or role is revoked."
        except Exception as e:
            return False, f"Failed to activate role in Supabase: {e}"
        _invalidate_role_caches(user_id)
        return True, None

    db = get_local_db()
    if hasattr(db, "update_role_status"):
        db.update_role_status(user_id, role, "active", activated_at=now_iso)

    _invalidate_role_caches(user_id)
    return True, None


def revoke_role(user_id: str, role: str, reason: str = "", revoked_by: Optional[str] = None) -> Tuple[bool, Optional[str]]:
    """Revokes a role grant. Requires verified Sole Admin authorization."""
    ok_admin, err_admin = require_sole_admin(actor_id=revoked_by)
    if not ok_admin:
        return False, err_admin

    from services.profiles import get_profile
    p = get_profile(user_id)
    base_role = p.get("role") if p else "aspirant"
    if role == "aspirant" and base_role == "aspirant":
        return False, "The base registered Aspirant role cannot be revoked."

    now_iso = datetime.now(timezone.utc).isoformat()
    backend = get_data_backend()

    if backend == "supabase":
        admin = _get_admin_client()
        if not admin:
            return False, "Supabase admin client unavailable."
        try:
            u_res = admin.table("user_roles").update({
                "status": "revoked",
                "revoked_at": now_iso,
                "revocation_reason": reason or "Revoked by Administration",
                "updated_at": now_iso
            }).eq("user_id", user_id).eq("role", role).execute()
            if not u_res.data:
                admin.table("user_roles").upsert({
                    "user_id": user_id,
                    "role": role,
                    "status": "revoked",
                    "granted_at": now_iso,
                    "revoked_at": now_iso,
                    "revocation_reason": reason or "Revoked by Administration",
                    "updated_at": now_iso
                }, on_conflict="user_id, role").execute()
        except Exception as e:
            return False, f"Failed to revoke role in Supabase: {e}"
    else:
        db = get_local_db()
        if hasattr(db, "update_role_status"):
            db.update_role_status(user_id, role, "revoked", revocation_reason=reason)

    # If revoking a Guide, immediately unassign active primary or co-guide caseload
    if role == "guide":
        try:
            from services.relationships import get_all_relationships, unassign_guide
            rels = get_all_relationships()
            for rel in rels:
                raw_gids = rel.get("guide_ids") or []
                if isinstance(raw_gids, str):
                    try: raw_gids = json.loads(raw_gids)
                    except Exception: raw_gids = [raw_gids]
                if not isinstance(raw_gids, list):
                    raw_gids = []
                if rel.get("guide_id"):
                    raw_gids.append(str(rel["guide_id"]))
                guides_set = {str(gid) for gid in raw_gids if gid}

                if str(user_id) in guides_set and rel.get("status") == "active":
                    unassign_guide(aspirant_id=rel["aspirant_id"], guide_id=str(user_id), admin_id=revoked_by, reason=f"Mentor role revoked: {reason}")
        except Exception as e:
            print(f"[Roles] Caseload unassignment notice for revoked guide {user_id}: {e}")

    # If revoking an SME, immediately unassign active primary or additional SME caseload
    if role == "sme":
        try:
            from services.relationships import get_all_relationships, unassign_sme
            rels = get_all_relationships()
            for rel in rels:
                raw_sids = rel.get("sme_ids") or []
                if isinstance(raw_sids, str):
                    try: raw_sids = json.loads(raw_sids)
                    except Exception: raw_sids = [raw_sids]
                if not isinstance(raw_sids, list):
                    raw_sids = []
                if rel.get("sme_id"):
                    raw_sids.append(str(rel["sme_id"]))
                smes_set = {str(sid) for sid in raw_sids if sid}

                if str(user_id) in smes_set and rel.get("status") == "active":
                    unassign_sme(aspirant_id=rel["aspirant_id"], sme_id=str(user_id), admin_id=revoked_by, reason=f"SME role revoked: {reason}")
        except Exception as e:
            print(f"[Roles] Advisory unassignment notice for revoked SME {user_id}: {e}")

    _invalidate_role_caches(user_id)
    try:
        from services.notifications import create_notification
        from services.governance import get_primary_admin_id
        role_display = "Guide" if role == "guide" else ("Domain SME" if role == "sme" else role.capitalize())
        create_notification(
            user_id=user_id,
            title=f"Role Grant Concluded: {role_display}",
            message=f"Your {role_display} role grant has been revoked. Reason: {reason or 'Administrative update'}.",
            notification_type="role_revoked",
            actor_id=revoked_by or get_primary_admin_id()
        )
    except Exception:
        pass
    return True, None


def suspend_role(user_id: str, role: str, reason: str = "", suspended_by: Optional[str] = None) -> Tuple[bool, Optional[str]]:
    """Suspends a role grant temporarily. Requires verified Sole Admin authorization."""
    ok_admin, err_admin = require_sole_admin(actor_id=suspended_by)
    if not ok_admin:
        return False, err_admin

    if role == "aspirant":
        return False, "The base Aspirant role cannot be suspended."

    now_iso = datetime.now(timezone.utc).isoformat()
    backend = get_data_backend()

    if backend == "supabase":
        admin = _get_admin_client()
        if not admin:
            return False, "Supabase admin client unavailable."
        try:
            res = admin.table("user_roles").update({
                "status": "suspended",
                "suspended_at": now_iso,
                "revocation_reason": reason or "Suspended by Administration",
                "updated_at": now_iso
            }).eq("user_id", user_id).eq("role", role).neq("status", "revoked").execute()
            if not res or not getattr(res, "data", None):
                return False, f"Role suspension failed in Supabase: No active grant found for role '{role}' or role is already revoked."
        except Exception as e:
            return False, f"Failed to suspend role in Supabase: {e}"
        _invalidate_role_caches(user_id)
    else:
        db = get_local_db()
        if hasattr(db, "update_role_status"):
            db.update_role_status(user_id, role, "suspended", revocation_reason=reason)
        _invalidate_role_caches(user_id)

    try:
        from services.notifications import create_notification
        from services.governance import get_primary_admin_id
        role_display = "Guide" if role == "guide" else ("Domain SME" if role == "sme" else role.capitalize())
        create_notification(
            user_id=user_id,
            title=f"Role Temporarily Suspended: {role_display}",
            message=f"Your {role_display} workspace access has been temporarily suspended. Note: {reason or 'Administrative review'}.",
            notification_type="role_suspended",
            actor_id=suspended_by or get_primary_admin_id()
        )
    except Exception:
        pass
    return True, None


def reinstate_role(user_id: str, role: str, reinstated_by: Optional[str] = None) -> Tuple[bool, Optional[str]]:
    """Reinstates a suspended role back to active status. Refuses to reinstate revoked roles."""
    ok_admin, err_admin = require_sole_admin(actor_id=reinstated_by)
    if not ok_admin:
        return False, err_admin

    curr_roles = get_user_roles(user_id)
    matching = next((r for r in curr_roles if r.get("role") == role), None)
    if matching and matching.get("status") == "revoked":
        return False, f"Cannot reinstate: The {role.upper()} role grant was revoked. Revoked roles cannot be reinstated; a new grant is required."

    now_iso = datetime.now(timezone.utc).isoformat()
    backend = get_data_backend()

    if backend == "supabase":
        admin = _get_admin_client()
        if not admin:
            return False, "Supabase admin client unavailable."
        try:
            res = admin.table("user_roles").update({
                "status": "active",
                "suspended_at": None,
                "revocation_reason": None,
                "updated_at": now_iso
            }).eq("user_id", user_id).eq("role", role).eq("status", "suspended").execute()
            if not res or not getattr(res, "data", None):
                return False, f"Role reinstatement failed in Supabase: Role '{role}' is not in suspended status."
        except Exception as e:
            return False, f"Failed to reinstate role in Supabase: {e}"
        _invalidate_role_caches(user_id)
    else:
        db = get_local_db()
        if hasattr(db, "update_role_status"):
            db.update_role_status(user_id, role, "active")
        _invalidate_role_caches(user_id)

    try:
        from services.notifications import create_notification
        from services.governance import get_primary_admin_id
        role_display = "Guide" if role == "guide" else ("Domain SME" if role == "sme" else role.capitalize())
        create_notification(
            user_id=user_id,
            title=f"Role Reinstated: {role_display}",
            message=f"Your {role_display} role grant has been reinstated to active status.",
            notification_type="role_reinstated",
            actor_id=reinstated_by or get_primary_admin_id()
        )
    except Exception:
        pass
    return True, None


def cancel_grant(user_id: str, role: str, actor_id: Optional[str] = None) -> Tuple[bool, Optional[str]]:
    """Cancels a pending NDA role grant. Requires verified Sole Admin authorization."""
    ok_admin, err_admin = require_sole_admin(actor_id=actor_id)
    if not ok_admin:
        return False, err_admin
    now_iso = datetime.now(timezone.utc).isoformat()
    backend = get_data_backend()

    if backend == "supabase":
        admin = _get_admin_client()
        if admin:
            try:
                res = admin.table("user_roles").delete().eq("user_id", user_id).eq("role", role).execute()
            except Exception as e:
                err_str = str(e)
                print(f"[Roles] Supabase cancel notice: {err_str}")
                if "PGRST205" not in err_str and "user_roles" not in err_str:
                    return False, f"Failed to cancel role grant in Supabase: {e}"

    db = get_local_db()
    if hasattr(db, "delete_user_role"):
        db.delete_user_role(user_id, role)
    elif hasattr(db, "update_role_status"):
        db.update_role_status(user_id, role, "revoked", revocation_reason="Pending grant cancelled by admin")

    _invalidate_role_caches(user_id)
    return True, None


def list_users_with_multi_roles() -> List[Dict]:
    """Lists all non-admin users with their full role grants roster for Admin Console (Batched & Memoized)."""
    cached = get_memo("multi_role_users")
    if cached is not None:
        return cached

    from services.profiles import list_profiles_by_role, calculate_completion
    from services.governance import get_primary_admin_id
    backend = get_data_backend()
    profiles_map: Dict[str, Dict] = {}
    primary_admin_id = str(get_primary_admin_id() or "")

    all_role_rows: List[Dict] = []

    if backend == "supabase":
        client = _get_admin_client() or _get_user_client()
        if client:
            try:
                # 1. Single batched fetch of all active profiles
                p_res = client.table("profiles").select("*").neq("is_active", False).execute()
                for p in (p_res.data or []):
                    p_id = str(p.get("id", ""))
                    p_email = str(p.get("email", "")).strip().lower()
                    if p_email == "fulcrumindia1@gmail.com" or (primary_admin_id and p_id == primary_admin_id) or p.get("role") == "admin":
                        continue
                    p["completion_pct"] = calculate_completion(p)
                    set_memo(f"profile:{p_id}", p, ttl_seconds=60)
                    profiles_map[p_id] = p

                # 2. Single batched fetch of all user_roles rows
                ur_res = client.table("user_roles").select("*").execute()
                all_role_rows = ur_res.data or []
            except Exception as e:
                print(f"[Roles] Batched multi-role fetch fallback: {e}")

    if not profiles_map:
        for r in ("aspirant", "guide", "sme"):
            for p in list_profiles_by_role(r):
                p_id = str(p.get("id", ""))
                p_email = str(p.get("email", "")).strip().lower()
                if p_email == "fulcrumindia1@gmail.com" or (primary_admin_id and p_id == primary_admin_id) or p.get("role") == "admin":
                    continue
                profiles_map[p_id] = p

    roles_by_uid: Dict[str, List[Dict]] = {}
    if all_role_rows:
        for r_row in all_role_rows:
            uid_key = str(r_row.get("user_id", ""))
            if uid_key:
                roles_by_uid.setdefault(uid_key, []).append(dict(r_row))

    results = []
    for uid, prof in profiles_map.items():
        if all_role_rows:
            roles = [dict(r) for r in roles_by_uid.get(str(uid), [])]
            base_role = prof.get("role", "aspirant")
            existing_base = next((r for r in roles if r.get("role") == base_role), None)
            if not existing_base:
                roles.append({
                    "id": f"role_{uid}_{base_role}",
                    "user_id": uid,
                    "role": base_role,
                    "status": "active",
                    "granted_at": prof.get("created_at"),
                    "activated_at": prof.get("created_at")
                })
            set_memo(f"user_roles:{uid}", roles, ttl_seconds=60)
        else:
            roles = get_user_roles(uid)

        active_r = [g["role"] for g in roles if g.get("status") == "active"]
        pending_r = [g["role"] for g in roles if g.get("status") == "pending_nda"]
        suspended_r = [g["role"] for g in roles if g.get("status") == "suspended"]
        revoked_r = [g["role"] for g in roles if g.get("status") == "revoked"]
        results.append({
            "id": uid,
            "full_name": prof.get("full_name", "User"),
            "email": prof.get("email", ""),
            "primary_role": prof.get("role", "aspirant"),
            "active_roles": active_r,
            "pending_nda_roles": pending_r,
            "suspended_roles": suspended_r,
            "revoked_roles": revoked_r,
            "role_grants": roles,
            "district": prof.get("district", "Tamil Nadu"),
            "created_at": prof.get("created_at")
        })

    results.sort(key=lambda x: x["full_name"])
    set_memo("multi_role_users", results, ttl_seconds=60)
    return results


def list_active_profiles_for_role(target_role: str) -> List[Dict]:
    """
    Returns all user profiles eligible for target_role ('aspirant', 'guide', 'sme').
    Includes both base profiles and secondary multi-role holders whose grant is currently ACTIVE.
    Excludes users whose grant is suspended, revoked, or pending NDA.
    Strictly excludes the Platform Administrator from candidate lists.
    """
    cache_key = f"active_profiles_for_role:{target_role}"
    cached = get_memo(cache_key)
    if cached is not None:
        return cached

    from services.profiles import list_profiles_by_role, get_profile
    from services.governance import get_primary_admin_id
    primary_admin_id = str(get_primary_admin_id() or "")

    base_profiles = list_profiles_by_role(target_role)
    profiles_by_id = {}
    for p in base_profiles:
        p_id = str(p.get("id", ""))
        p_email = str(p.get("email", "")).strip().lower()
        if p_email == "fulcrumindia1@gmail.com" or (primary_admin_id and p_id == primary_admin_id) or p.get("role") == "admin":
            continue
        profiles_by_id[p_id] = p

    # Inspect all multi-role users
    for u in list_users_with_multi_roles():
        uid = str(u["id"])
        u_email = str(u.get("email", "")).strip().lower()
        if u_email == "fulcrumindia1@gmail.com" or (primary_admin_id and uid == primary_admin_id):
            continue

        if target_role in u.get("active_roles", []):
            if uid not in profiles_by_id:
                prof = get_profile(uid)
                if prof:
                    profiles_by_id[uid] = prof
        else:
            # If primary profile was target_role but is explicitly suspended or revoked in user_roles
            if target_role in u.get("revoked_roles", []) or target_role in u.get("suspended_roles", []) or target_role in u.get("pending_nda_roles", []):
                profiles_by_id.pop(uid, None)

    results = list(profiles_by_id.values())
    results.sort(key=lambda x: str(x.get("full_name", "")))
    set_memo(cache_key, results, ttl_seconds=60)
    return results
