"""
services/notifications.py — Universal In-App Notification System for FULCRUM-INDIA
==================================================================================
Real-time notification engine for all roles (Aspirant, Guide, SME, Admin):
- Mentor assignments and handoffs
- Scheme recommendations and releases
- Support tickets and expert replies
- Administrative alerts and milestones

Production Rule (PART 2 & PART 8):
- When DATA_BACKEND=supabase: strictly Supabase ONLY. Zero silent fallback to SQLite.
- Authorization: Enforces strict relationship checks. Unauthorized cross-user notifications are blocked.
"""

import json
import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, List, Tuple
from services.auth import get_supabase_client, get_supabase_admin_client, get_data_backend
from services.logger import app_logger
from services.cache import get_memo, set_memo, invalidate_memo

def _get_user_client():
    return get_supabase_client()

def _get_admin_client():
    return get_supabase_admin_client()

def _invalidate_user_notifications(user_id: str) -> None:
    if user_id:
        invalidate_memo(f"notif_count:{user_id}")
        invalidate_memo(f"notif_list:{user_id}:")

def is_notification_allowed(actor_id: Optional[str], target_user_id: str, notification_type: str) -> bool:
    """
    PART 8 — NOTIFICATION SAFETY
    Verifies that actor_id is authorized to notify target_user_id across single or hybrid roles.
    - System/automated (actor_id None): Allowed.
    - Self notification: Allowed.
    - Admin actor: Allowed to notify anyone.
    - Target is Admin: Any authenticated user can notify Admin.
    - Aspirant role holder: Can notify assigned Guide(s) or SME(s).
    - Guide / SME role holder: Can notify an assigned Aspirant (or peer co-mentor on shared case).
    - All other arbitrary cross-user notifications are blocked.
    """
    if not actor_id or actor_id == target_user_id:
        return True

    from services.profiles import get_profile
    from services.relationships import get_aspirant_mentors
    from services.roles import get_active_roles, is_strict_admin

    actor_prof = get_profile(actor_id)
    if not actor_prof:
        return False

    if is_strict_admin(user_id=actor_id, user_dict=actor_prof):
        return True

    target_prof = get_profile(target_user_id)
    if not target_prof:
        return False

    if is_strict_admin(user_id=target_user_id, user_dict=target_prof):
        return True

    actor_roles = set(get_active_roles(actor_id))
    base_actor_role = str(actor_prof.get("role") or "aspirant").strip().lower()
    if base_actor_role in ("aspirant", "guide", "sme"):
        actor_roles.add(base_actor_role)

    if "aspirant" in actor_roles:
        mentors = get_aspirant_mentors(actor_id) or {}
        valid_mentor_ids = [m["id"] for m in mentors.get("guides", [])] + [m["id"] for m in mentors.get("smes", [])]
        if target_user_id in valid_mentor_ids:
            return True

    if "guide" in actor_roles or "sme" in actor_roles:
        mentors = get_aspirant_mentors(target_user_id) or {}
        if "guide" in actor_roles:
            valid_guide_ids = [m["id"] for m in mentors.get("guides", [])]
            if actor_id in valid_guide_ids:
                return True
        if "sme" in actor_roles:
            valid_sme_ids = [m["id"] for m in mentors.get("smes", [])]
            if actor_id in valid_sme_ids:
                return True

    return False

def create_notification(
    user_id: str,
    title: str,
    message: str,
    notification_type: str,
    actor_id: Optional[str] = None,
    link: Optional[str] = None
) -> Tuple[Optional[Dict], Optional[str]]:
    """
    Creates an in-app notification for a specific user.
    Types: 'guide_assigned', 'guide_reassigned', 'sme_assigned', 'sme_reassigned',
           'scheme_released', 'help_ticket_created', 'help_ticket_replied', 'system_alert'
    """
    if not user_id or not title:
        return None, "user_id and title are required."

    # PART 8: Relationship & Authorization Validation
    if not is_notification_allowed(actor_id, user_id, notification_type):
        err = f"Unauthorized: User {actor_id} is not permitted to send notifications to {user_id}."
        app_logger.warning("notifications", "create_notification_blocked", err, actor_id=actor_id)
        return None, "Unauthorized: Notification recipient is not in an authorized relationship with the sender."

    backend = get_data_backend()
    notif_id = str(uuid.uuid4())
    now_iso = datetime.now(timezone.utc).isoformat()

    notif_data = {
        "id": notif_id,
        "user_id": user_id,
        "actor_id": actor_id,
        "title": title.strip(),
        "message": message.strip() if message else "",
        "notification_type": notification_type,
        "link": link,
        "is_read": False,
        "created_at": now_iso
    }

    if backend == "supabase":
        client = _get_admin_client() or _get_user_client()
        if not client:
            app_logger.error("notifications", "create_notification", "Supabase client unavailable", actor_id=actor_id)
            return None, "Supabase client unavailable."
        try:
            res = client.table("notifications").insert(notif_data).execute()
            _invalidate_user_notifications(user_id)
            if res.data and len(res.data) > 0:
                app_logger.info("notifications", "create_notification", f"Notification created for {user_id}", actor_id=actor_id)
                return res.data[0], None
            return notif_data, None
        except Exception as e:
            app_logger.error("notifications", "create_notification", f"Supabase notification insert failed: {e}", error=e, actor_id=actor_id)
            return None, f"Failed to record notification in Supabase: {e}"

    # SQLite local mode (ONLY when DATA_BACKEND=sqlite)
    from services.local_db import get_local_db
    try:
        rec = get_local_db().create_notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            actor_id=actor_id,
            link=link
        )
        _invalidate_user_notifications(user_id)
        return rec, None
    except Exception as e:
        return None, f"Local DB notification error: {e}"

_MENTOR_ASSIGNED_TITLE_MARKERS = (
    "new mentee",
    "co-guide",
    "assigned as",
    "added to advisory",
    "unassigned",
    "caseload",
    "reassigned from",
)


def infer_notification_workspace(notif: Dict) -> str:
    """Infers the target workspace ('aspirant', 'guide', 'sme', 'admin', or 'all') for a notification."""
    if not isinstance(notif, dict):
        return "all"
    explicit = str(notif.get("target_role") or notif.get("workspace") or "").strip().lower()
    if explicit in ("aspirant", "guide", "sme", "admin", "all"):
        return explicit

    ntype = str(notif.get("notification_type") or "").strip()
    ntype_low = ntype.lower()
    title_low = str(notif.get("title") or "").lower()
    msg_low = str(notif.get("message") or "").lower()
    combined = f"{title_low} {msg_low}"

    if ntype in ("account_restored", "account_resumed", "account_suspended", "system_alert"):
        return "all"
    if ntype in ("CONFIDENTIAL_COMPLAINT", "SCHEME_SUPPORT_REVIEW", "admin_directive_needed", "INACTIVITY_CRITICAL"):
        return "admin"
    if ntype in ("scheme_released", "CONFIDENTIAL_COMPLAINT_UPDATE", "programme_completed", "mentor_guidance_issued", "help_ticket_replied"):
        return "aspirant"
    if ntype in ("SCHEME_REVIEW_DECISION", "INACTIVITY_REMINDER", "INACTIVITY_WARNING", "admin_directive_issued"):
        return "sme" if ("domain sme" in combined or " sme" in combined or "sme " in combined) else "guide"
    if ntype in ("help_ticket_created", "aspirant_reply_submitted"):
        if "[domain sme]" in combined or "domain sme" in combined or "sme consultation" in combined:
            return "sme"
        return "guide"
    if ntype in ("guide_assigned", "guide_reassigned", "guide_unassigned"):
        if any(m in combined for m in _MENTOR_ASSIGNED_TITLE_MARKERS) or "you have been assigned" in msg_low or "you are no longer assigned" in msg_low:
            return "guide"
        return "aspirant"
    if ntype in ("sme_assigned", "sme_reassigned", "sme_unassigned"):
        if any(m in combined for m in _MENTOR_ASSIGNED_TITLE_MARKERS) or "you have been assigned" in msg_low or "you are no longer assigned" in msg_low:
            return "sme"
        return "aspirant"
    if ntype in ("role_granted", "role_reinstated", "role_revoked", "role_suspended"):
        if "domain sme" in combined or " sme " in combined or "sme role" in combined:
            return "sme"
        if "guide" in combined:
            return "guide"
        if "aspirant" in combined:
            return "aspirant"
        return "all"
    if ntype_low.startswith("sme"):
        return "sme"
    if ntype_low.startswith("guide"):
        return "guide"
    return "all"


def filter_notifications_by_workspace(notifs: List[Dict], workspace: Optional[str]) -> List[Dict]:
    """Filters a notification list to items belonging to `workspace` or universal ('all') notices."""
    if not workspace:
        return list(notifs or [])
    ws = str(workspace).strip().lower()
    if ws not in ("aspirant", "guide", "sme", "admin"):
        return list(notifs or [])
    filtered = []
    for n in (notifs or []):
        inferred = infer_notification_workspace(n)
        if inferred in (ws, "all"):
            filtered.append(n)
    return filtered


def list_notifications(user_id: str, unread_only: bool = False, workspace: Optional[str] = None) -> List[Dict]:
    """Retrieves notifications for a user (with 30s session memoization)."""
    if not user_id:
        return []
    cache_key = f"notif_list:{user_id}:{bool(unread_only)}"
    cached = get_memo(cache_key)
    if cached is not None:
        return filter_notifications_by_workspace(cached, workspace) if workspace else cached

    backend = get_data_backend()

    if backend == "supabase":
        client = _get_user_client()
        admin = _get_admin_client()
        reader = client if (client and hasattr(client, "auth") and client.auth.get_session()) else admin
        if not reader:
            reader = client or admin
        if reader:
            try:
                q = reader.table("notifications").select("*").eq("user_id", user_id)
                if unread_only:
                    q = q.eq("is_read", False)
                res = q.order("created_at", desc=True).limit(50).execute()
                if res.data is not None:
                    set_memo(cache_key, res.data, ttl_seconds=30)
                    return filter_notifications_by_workspace(res.data, workspace) if workspace else res.data
                if admin and admin != reader:
                    q2 = admin.table("notifications").select("*").eq("user_id", user_id)
                    if unread_only:
                        q2 = q2.eq("is_read", False)
                    res2 = q2.order("created_at", desc=True).limit(50).execute()
                    if res2.data is not None:
                        set_memo(cache_key, res2.data, ttl_seconds=30)
                        return filter_notifications_by_workspace(res2.data, workspace) if workspace else res2.data
                out = []
                set_memo(cache_key, out, ttl_seconds=30)
                return out
            except Exception as e:
                app_logger.error("notifications", "list_notifications", f"Supabase list error for {user_id}: {e}", error=e, actor_id=user_id)
                if admin and admin != reader:
                    try:
                        q2 = admin.table("notifications").select("*").eq("user_id", user_id)
                        if unread_only:
                            q2 = q2.eq("is_read", False)
                        res2 = q2.order("created_at", desc=True).limit(50).execute()
                        if res2.data is not None:
                            set_memo(cache_key, res2.data, ttl_seconds=30)
                            return filter_notifications_by_workspace(res2.data, workspace) if workspace else res2.data
                    except Exception:
                        pass
        return []

    # SQLite local mode ONLY
    from services.local_db import get_local_db
    try:
        rows = get_local_db().list_notifications(user_id=user_id, unread_only=unread_only)
        set_memo(cache_key, rows, ttl_seconds=30)
        return filter_notifications_by_workspace(rows, workspace) if workspace else rows
    except Exception as e:
        print(f"[Notifications] Local DB query error: {e}")
        return []

def mark_as_read(notification_id: str, user_id: str) -> bool:
    """Marks a specific notification as read."""
    backend = get_data_backend()

    if backend == "supabase":
        user_client = _get_user_client()
        admin = _get_admin_client()
        if user_client:
            try:
                res = user_client.table("notifications").update({"is_read": True}).eq("id", notification_id).eq("user_id", user_id).execute()
                if res.data:
                    _invalidate_user_notifications(user_id)
                    return True
            except Exception:
                pass
        if admin:
            try:
                res = admin.table("notifications").update({"is_read": True}).eq("id", notification_id).eq("user_id", user_id).execute()
                _invalidate_user_notifications(user_id)
                return bool(res.data)
            except Exception as e:
                app_logger.error("notifications", "mark_as_read", f"Supabase mark_as_read error: {e}", error=e, actor_id=user_id)
                return False
        return False

    from services.local_db import get_local_db
    try:
        ok = get_local_db().mark_notification_as_read(notification_id, user_id)
        _invalidate_user_notifications(user_id)
        return ok
    except Exception:
        return False

def mark_all_as_read(user_id: str) -> bool:
    """Marks all unread notifications for a user as read."""
    backend = get_data_backend()

    if backend == "supabase":
        user_client = _get_user_client()
        admin = _get_admin_client()
        if user_client:
            try:
                res = user_client.table("notifications").update({"is_read": True}).eq("user_id", user_id).eq("is_read", False).execute()
                if res.data is not None:
                    _invalidate_user_notifications(user_id)
                    return True
            except Exception:
                pass
        if admin:
            try:
                res = admin.table("notifications").update({"is_read": True}).eq("user_id", user_id).eq("is_read", False).execute()
                _invalidate_user_notifications(user_id)
                return res.data is not None
            except Exception as e:
                app_logger.error("notifications", "mark_all_as_read", f"Supabase mark_all_as_read error: {e}", error=e, actor_id=user_id)
                return False
        return False

    from services.local_db import get_local_db
    try:
        ok = get_local_db().mark_all_notifications_as_read(user_id)
        _invalidate_user_notifications(user_id)
        return ok
    except Exception:
        return False

def get_unread_count(user_id: str) -> int:
    """Returns the count of unread notifications for a user (with 30s session memoization)."""
    if not user_id:
        return 0
    cache_key = f"notif_count:{user_id}"
    cached = get_memo(cache_key)
    if cached is not None:
        return int(cached)

    backend = get_data_backend()

    if backend == "supabase":
        client = _get_user_client()
        admin = _get_admin_client()
        reader = client if (client and hasattr(client, "auth") and client.auth.get_session()) else admin
        if not reader:
            reader = client or admin
        if reader:
            try:
                res = reader.table("notifications").select("id", count="exact").eq("user_id", user_id).eq("is_read", False).execute()
                if hasattr(res, "count") and res.count is not None:
                    cnt = int(res.count)
                    set_memo(cache_key, cnt, ttl_seconds=30)
                    return cnt
                if res.data is not None:
                    cnt = len(res.data)
                    set_memo(cache_key, cnt, ttl_seconds=30)
                    return cnt
                set_memo(cache_key, 0, ttl_seconds=30)
                return 0
            except Exception as e:
                app_logger.error("notifications", "get_unread_count", f"Supabase unread count error: {e}", error=e, actor_id=user_id)
                if admin and admin != reader:
                    try:
                        res2 = admin.table("notifications").select("id", count="exact").eq("user_id", user_id).eq("is_read", False).execute()
                        if hasattr(res2, "count") and res2.count is not None:
                            cnt = int(res2.count)
                            set_memo(cache_key, cnt, ttl_seconds=30)
                            return cnt
                        if res2.data is not None:
                            cnt = len(res2.data)
                            set_memo(cache_key, cnt, ttl_seconds=30)
                            return cnt
                    except Exception:
                        pass
                return 0
        return 0

    from services.local_db import get_local_db
    try:
        cnt = get_local_db().get_unread_notifications_count(user_id)
        set_memo(cache_key, cnt, ttl_seconds=30)
        return cnt
    except Exception:
        return 0
