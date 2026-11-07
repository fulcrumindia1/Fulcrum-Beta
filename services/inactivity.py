"""
services/inactivity.py — Guide Inactivity Monitoring & Idempotent Escalation System
==================================================================================
Monitors Guide caseload engagement.
Checks elapsed time since last meaningful interaction:
  - Day 7: Automated gentle reminder to the Guide
  - Day 10: Inactivity alert to Administration
  - Day 14: Administrative escalation with reassignment prompt
Idempotently tracks alerts in inactivity_logs to prevent duplicate notifications.
"""

from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, List, Tuple
from services.auth import get_supabase_client, get_supabase_admin_client, get_data_backend
from services.local_db import get_local_db
from services.cache import get_memo, set_memo


def get_last_interaction_date(guide_id: str, aspirant_id: str) -> Optional[datetime]:
    """
    Computes the most recent meaningful interaction between Guide and Aspirant.
    Checks:
      1. Help requests / consultations handled by guide
      2. Scheme releases made by guide
      3. Journey events logged by guide
    """
    timestamps = []

    # 1. Check scheme releases
    try:
        from services.schemes import get_released_schemes_for_aspirant
        releases = get_released_schemes_for_aspirant(aspirant_id)
        for r in releases:
            if r.get("guide_id") == guide_id and r.get("released_at"):
                timestamps.append(datetime.fromisoformat(r["released_at"].replace("Z", "+00:00")))
    except Exception:
        pass

    # 2. Check journey events
    try:
        from services.journey import get_journey_timeline
        events = get_journey_timeline(aspirant_id)
        for ev in events:
            if ev.get("actor_id") == guide_id and ev.get("created_at"):
                timestamps.append(datetime.fromisoformat(ev["created_at"].replace("Z", "+00:00")))
    except Exception:
        pass

    # 3. Check help requests / consultations (Mentor responses ONLY)
    try:
        from services.help_requests import list_requests
        reqs = list_requests(aspirant_id=aspirant_id)
        for req in reqs:
            if req.get("assigned_guide_id") == guide_id or req.get("resolved_by") == guide_id or str(req.get("last_interaction_actor_id")) == str(guide_id):
                # 3a. Prioritize explicit mentor response timestamp
                if req.get("last_mentor_response_at"):
                    timestamps.append(datetime.fromisoformat(req["last_mentor_response_at"].replace("Z", "+00:00")))
                # 3b. If last interaction was by guide/sme, use last_handled_at
                elif req.get("last_interaction_actor_role") in ("guide", "sme") and str(req.get("last_interaction_actor_id")) == str(guide_id) and req.get("last_handled_at"):
                    timestamps.append(datetime.fromisoformat(req["last_handled_at"].replace("Z", "+00:00")))
                # 3c. Fallback for legacy records: only if guide provided response and actor was not aspirant
                elif req.get("guide_response") and str(req.get("resolved_by")) == str(guide_id) and req.get("last_interaction_actor_role") != "aspirant":
                    t_str = req.get("resolved_at") or req.get("last_handled_at")
                    if t_str:
                        timestamps.append(datetime.fromisoformat(t_str.replace("Z", "+00:00")))
    except Exception:
        pass

    if timestamps:
        return max(timestamps)
    return None


def check_and_process_caseload_inactivity() -> List[Dict]:
    """
    Evaluates all active Guide-Aspirant relationships for inactivity.
    Triggers idempotent alerts for Day 7, Day 10, and Day 14 thresholds.
    Returns list of processed notifications.
    """
    from services.relationships import get_all_relationships
    from services.notifications import create_notification
    from services.profiles import get_profile
    from services.governance import get_primary_admin_id

    relationships = get_all_relationships()
    now = datetime.now(timezone.utc)
    results = []
    admin_id = get_primary_admin_id()

    for rel in relationships:
        if rel.get("status") != "active":
            continue

        guide_id = rel.get("guide_id")
        aspirant_id = rel.get("aspirant_id")
        if not guide_id or not aspirant_id:
            continue

        last_date = get_last_interaction_date(guide_id, aspirant_id)
        if not last_date:
            # Fall back to relationship creation date
            created_at_str = rel.get("created_at")
            if created_at_str:
                last_date = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
            else:
                last_date = now - timedelta(days=1)

        days_inactive = (now - last_date).days
        asp_profile = get_profile(aspirant_id) or {}
        asp_name = asp_profile.get("full_name", "Entrepreneur")

        # Thresholds
        if days_inactive >= 14:
            stage = "DAY_14_ADMIN_REVIEW"
            if _record_inactivity_log(rel.get("id"), guide_id, aspirant_id, days_inactive, stage):
                create_notification(
                    user_id=admin_id,  # Platform Admin
                    title="Critical Inactivity Escalation (14 Days)",
                    message=f"Guide has not interacted with {asp_name} for {days_inactive} days. Urgent caseload review or reassignment recommended.",
                    notification_type="INACTIVITY_CRITICAL",
                    actor_id=guide_id
                )
                results.append({"guide_id": guide_id, "aspirant_id": aspirant_id, "stage": stage, "days": days_inactive})

        elif days_inactive >= 10:
            stage = "DAY_10_ADMIN_ALERT"
            if _record_inactivity_log(rel.get("id"), guide_id, aspirant_id, days_inactive, stage):
                create_notification(
                    user_id=admin_id,
                    title="Mentor Inactivity Alert (10 Days)",
                    message=f"Guide has not interacted with {asp_name} for {days_inactive} days. Automated monitoring notification dispatched.",
                    notification_type="INACTIVITY_WARNING",
                    actor_id=guide_id
                )
                results.append({"guide_id": guide_id, "aspirant_id": aspirant_id, "stage": stage, "days": days_inactive})

        elif days_inactive >= 7:
            stage = "DAY_7_REMINDER"
            if _record_inactivity_log(rel.get("id"), guide_id, aspirant_id, days_inactive, stage):
                create_notification(
                    user_id=guide_id,
                    title="Friendly Reminder: Entrepreneur Check-in",
                    message=f"It has been {days_inactive} days since your last update with {asp_name}. Please review their journey or recommend schemes.",
                    notification_type="INACTIVITY_REMINDER",
                    actor_id=admin_id
                )
                results.append({"guide_id": guide_id, "aspirant_id": aspirant_id, "stage": stage, "days": days_inactive})

    return results


def _record_inactivity_log(relationship_id: Optional[str], guide_id: str, aspirant_id: str, days: int, stage: str) -> bool:
    """Records an inactivity stage log entry. Returns True if successfully logged (first time), False if duplicate."""
    import uuid
    log_id = str(uuid.uuid4())
    now_iso = datetime.now(timezone.utc).isoformat()

    record = {
        "id": log_id,
        "relationship_id": relationship_id,
        "guide_id": guide_id,
        "aspirant_id": aspirant_id,
        "days_inactive": days,
        "escalation_stage": stage,
        "notification_sent_at": now_iso,
        "created_at": now_iso
    }

    backend = get_data_backend()
    if backend == "supabase":
        admin = get_supabase_admin_client()
        if admin:
            try:
                res = admin.table("inactivity_logs").insert(record).execute()
                if res.data:
                    return True
            except Exception:
                # Primary/unique constraint collision or table not present
                pass

    db = get_local_db()
    if hasattr(db, "insert_inactivity_log"):
        return db.insert_inactivity_log(record)

    return False


def list_inactivity_records() -> List[Dict]:
    """Retrieves all inactivity logs for admin review."""
    backend = get_data_backend()
    records = []

    if backend == "supabase":
        admin = get_supabase_admin_client()
        if admin:
            try:
                res = admin.table("inactivity_logs").select("*").order("created_at", desc=True).execute()
                records = res.data or []
            except Exception:
                pass

    if not records:
        db = get_local_db()
        if hasattr(db, "list_inactivity_logs"):
            records = db.list_inactivity_logs()

    return records

