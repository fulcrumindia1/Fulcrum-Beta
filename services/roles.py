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


def _get_admin_client():
    return get_supabase_admin_client()


def _get_user_client():
    return get_supabase_client()


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

    if not roles:
        # Check SQLite fallback whenever Supabase returns empty or fails
        db = get_local_db()
        roles = db.get_user_roles(user_id) if hasattr(db, "get_user_roles") else []

    # Ensure the user's primary/registered role is included if no explicit multi-role grants exist
    from services.profiles import get_profile
    from services.governance import get_primary_admin_id
    p = get_profile(user_id)
    if p:
        base_role = p.get("role", "aspirant")
        user_email = str(p.get("email", "")).strip().lower()
        primary_admin_id = str(get_primary_admin_id() or "")

        is_platform_admin = (
            base_role in ("admin", "district_admin", "operational_admin")
            or user_email == "fulcrumindia1@gmail.com"
            or (primary_admin_id and str(user_id) == primary_admin_id)
        )

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

    set_memo(cache_key, roles, ttl_seconds=60)
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
    """
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
        invalidate_memo(f"user_roles:{user_id}")
        invalidate_memo(f"guide_aspirants:{user_id}")
        invalidate_memo(f"sme_aspirants:{user_id}")
        return True, None

    # SQLite Mode ONLY
    db = get_local_db()
    if hasattr(db, "upsert_user_role"):
        db.upsert_user_role(record)

    invalidate_memo(f"user_roles:{user_id}")
    invalidate_memo(f"guide_aspirants:{user_id}")
    invalidate_memo(f"sme_aspirants:{user_id}")
    return True, None


def activate_role(user_id: str, role: str) -> Tuple[bool, Optional[str]]:
    """Activates a role (e.g. after valid NDA signature)."""
    now_iso = datetime.now(timezone.utc).isoformat()
    backend = get_data_backend()

    if backend == "supabase":
        admin = _get_admin_client()
        if not admin:
            return False, "Supabase admin client unavailable."
        try:
            admin.table("user_roles").update({
                "status": "active",
                "activated_at": now_iso,
                "updated_at": now_iso
            }).eq("user_id", user_id).eq("role", role).execute()
        except Exception as e:
            return False, f"Failed to activate role in Supabase: {e}"
        invalidate_memo(f"user_roles:{user_id}")
        invalidate_memo(f"guide_aspirants:{user_id}")
        invalidate_memo(f"sme_aspirants:{user_id}")
        return True, None

    db = get_local_db()
    if hasattr(db, "update_role_status"):
        db.update_role_status(user_id, role, "active", activated_at=now_iso)

    invalidate_memo(f"user_roles:{user_id}")
    invalidate_memo(f"guide_aspirants:{user_id}")
    invalidate_memo(f"sme_aspirants:{user_id}")
    return True, None


def revoke_role(user_id: str, role: str, reason: str = "", revoked_by: Optional[str] = None) -> Tuple[bool, Optional[str]]:
    """Revokes a role grant. Aspirants can never have their base registered aspirant role revoked."""
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
            admin.table("user_roles").update({
                "status": "revoked",
                "revoked_at": now_iso,
                "revocation_reason": reason or "Revoked by Administration",
                "updated_at": now_iso
            }).eq("user_id", user_id).eq("role", role).execute()
        except Exception as e:
            return False, f"Failed to revoke role in Supabase: {e}"
    else:
        db = get_local_db()
        if hasattr(db, "update_role_status"):
            db.update_role_status(user_id, role, "revoked", revocation_reason=reason)

    # If revoking a Guide, immediately unassign active caseload to prevent privileged data access
    if role == "guide":
        try:
            from services.relationships import get_all_relationships, unassign_guide
            rels = get_all_relationships()
            for rel in rels:
                guides_list = [str(g.get("id")) for g in rel.get("guides", [])]
                if (str(rel.get("guide_id")) == str(user_id) or str(user_id) in guides_list) and rel.get("status") == "active":
                    unassign_guide(aspirant_id=rel["aspirant_id"], guide_id=str(user_id), admin_id=revoked_by, reason=f"Mentor role revoked: {reason}")
        except Exception as e:
            print(f"[Roles] Caseload unassignment notice for revoked guide {user_id}: {e}")

    # If revoking an SME, immediately unassign active technical caseload
    if role == "sme":
        try:
            from services.relationships import get_all_relationships, unassign_sme
            rels = get_all_relationships()
            for rel in rels:
                smes_list = [str(s.get("id")) for s in rel.get("smes", [])]
                if (str(rel.get("sme_id")) == str(user_id) or str(user_id) in smes_list) and rel.get("status") == "active":
                    unassign_sme(aspirant_id=rel["aspirant_id"], sme_id=str(user_id), admin_id=revoked_by, reason=f"SME role revoked: {reason}")
        except Exception as e:
            print(f"[Roles] Advisory unassignment notice for revoked SME {user_id}: {e}")

    invalidate_memo(f"user_roles:{user_id}")
    invalidate_memo(f"guide_aspirants:{user_id}")
    invalidate_memo(f"sme_aspirants:{user_id}")
    return True, None


def suspend_role(user_id: str, role: str, reason: str = "") -> Tuple[bool, Optional[str]]:
    """Suspends a role grant temporarily."""
    if role == "aspirant":
        return False, "The base Aspirant role cannot be suspended."

    now_iso = datetime.now(timezone.utc).isoformat()
    backend = get_data_backend()

    if backend == "supabase":
        admin = _get_admin_client()
        if admin:
            try:
                res = admin.table("user_roles").update({
                    "status": "suspended",
                    "suspended_at": now_iso,
                    "revocation_reason": reason or "Suspended by Administration",
                    "updated_at": now_iso
                }).eq("user_id", user_id).eq("role", role).execute()
            except Exception as e:
                err_str = str(e)
                print(f"[Roles] Supabase suspend notice: {err_str}")
                if "PGRST205" not in err_str and "user_roles" not in err_str:
                    return False, f"Failed to suspend role in Supabase: {e}"

    db = get_local_db()
    if hasattr(db, "update_role_status"):
        db.update_role_status(user_id, role, "suspended", revocation_reason=reason)

    invalidate_memo(f"user_roles:{user_id}")
    invalidate_memo(f"guide_aspirants:{user_id}")
    invalidate_memo(f"sme_aspirants:{user_id}")
    return True, None


def reinstate_role(user_id: str, role: str) -> Tuple[bool, Optional[str]]:
    """Reinstates a suspended role back to active status."""
    now_iso = datetime.now(timezone.utc).isoformat()
    backend = get_data_backend()

    if backend == "supabase":
        admin = _get_admin_client()
        if admin:
            try:
                res = admin.table("user_roles").update({
                    "status": "active",
                    "suspended_at": None,
                    "revocation_reason": None,
                    "updated_at": now_iso
                }).eq("user_id", user_id).eq("role", role).execute()
            except Exception as e:
                err_str = str(e)
                print(f"[Roles] Supabase reinstate notice: {err_str}")
                if "PGRST205" not in err_str and "user_roles" not in err_str:
                    return False, f"Failed to reinstate role in Supabase: {e}"

    db = get_local_db()
    if hasattr(db, "update_role_status"):
        db.update_role_status(user_id, role, "active")

    invalidate_memo(f"user_roles:{user_id}")
    invalidate_memo(f"guide_aspirants:{user_id}")
    invalidate_memo(f"sme_aspirants:{user_id}")
    return True, None


def cancel_grant(user_id: str, role: str) -> Tuple[bool, Optional[str]]:
    """Cancels a pending NDA role grant."""
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

    invalidate_memo(f"user_roles:{user_id}")
    invalidate_memo(f"guide_aspirants:{user_id}")
    invalidate_memo(f"sme_aspirants:{user_id}")
    return True, None


def list_users_with_multi_roles() -> List[Dict]:
    """Lists all non-admin users with their full role grants roster for Admin Console."""
    from services.profiles import list_profiles_by_role
    from services.governance import get_primary_admin_id
    backend = get_data_backend()
    profiles_map = {}
    primary_admin_id = str(get_primary_admin_id() or "")

    # Gather all non-admin profiles
    for r in ("aspirant", "guide", "sme"):
        for p in list_profiles_by_role(r):
            p_id = str(p.get("id", ""))
            p_email = str(p.get("email", "")).strip().lower()
            if p_email == "fulcrumindia1@gmail.com" or (primary_admin_id and p_id == primary_admin_id) or p.get("role") == "admin":
                continue
            profiles_map[p["id"]] = p

    results = []
    for uid, prof in profiles_map.items():
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
    return results


def list_active_profiles_for_role(target_role: str) -> List[Dict]:
    """
    Returns all user profiles eligible for target_role ('aspirant', 'guide', 'sme').
    Includes both base profiles and secondary multi-role holders whose grant is currently ACTIVE.
    Excludes users whose grant is suspended, revoked, or pending NDA.
    Strictly excludes the Platform Administrator from candidate lists.
    """
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
    return results
