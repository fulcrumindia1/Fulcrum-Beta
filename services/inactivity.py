"""
services/inactivity.py — Guide & SME Inactivity Monitoring & Idempotent Escalation System
========================================================================================
Monitors both Guide and Domain SME caseload engagement independently.
Evaluates distinct authorized mentor assignments:
  aspirant_id + mentor_id + mentor_role + assignment lifecycle

Thresholds:
  - Day 7: Gentle in-app reminder to the responsible Guide or SME
  - Day 10: Inactivity alert to Administration
  - Day 14: Critical administrative escalation with reassignment prompt

Key Rules:
  1. Independent Activity Tracking: Guide interactions do NOT reset SME clocks, and vice-versa.
  2. Actor Verification: Aspirant replies NEVER reset mentor inactivity clocks.
  3. Effective Assignment Dates: Newly added co-guides or SMEs start calculating inactivity
     from their own assignment date, not the original relationship creation date.
  4. Episode Idempotency: Distinguishes separate inactivity episodes without suppressing
     future legitimate alerts after a mentor resumes work and later becomes inactive again.
  5. Live Status Evaluation: Dynamically labels alerts as:
     Needs Attention, Follow-up Initiated, Mentor Active Again, Resolved, or Historical Record.
"""

import json
import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, List, Tuple

from services.auth import get_supabase_client, get_supabase_admin_client, get_data_backend
from services.local_db import get_local_db
from services.cache import get_memo, set_memo


# ─────────────────────────────────────────────────────────────────────────────
# 1. INDEPENDENT INTERACTION COMPUTATION
# ─────────────────────────────────────────────────────────────────────────────
def get_last_interaction_date(
    guide_id: str,
    aspirant_id: str,
    mentor_role: str = "guide",
    assignment_date: Optional[datetime] = None
) -> Optional[datetime]:
    """
    Computes the most recent verified meaningful interaction by a specific mentor
    (Guide or SME) with an Aspirant.

    Checks:
      - Consultations / Help Requests: Mentor's verified responses only
      - Journey Events: Authored by this specific mentor
      - Case Discussions / Private Notes: Authored by this mentor in this role
      - Scheme Releases: Authored by this guide (Guide only)

    Strictly ignores:
      - Aspirant replies / messages
      - Admin directives / system notes
      - Different mentors' responses
      - Interactions prior to mentor's effective assignment date
    """
    mentor_id = guide_id  # Parameter named guide_id for 100% backward compatibility
    timestamps: List[datetime] = []

    # 1. Check scheme releases (Guide only)
    if mentor_role == "guide":
        try:
            from services.schemes import get_released_schemes_for_aspirant
            releases = get_released_schemes_for_aspirant(aspirant_id)
            for r in releases:
                if str(r.get("guide_id")) == str(mentor_id) and r.get("released_at"):
                    timestamps.append(datetime.fromisoformat(r["released_at"].replace("Z", "+00:00")))
        except Exception:
            pass

    # 2. Check journey timeline events authored by this specific mentor
    try:
        from services.journey import get_journey_timeline
        events = get_journey_timeline(aspirant_id)
        for ev in events:
            if str(ev.get("actor_id")) == str(mentor_id) and ev.get("created_at"):
                timestamps.append(datetime.fromisoformat(ev["created_at"].replace("Z", "+00:00")))
    except Exception:
        pass

    # 3. Check case discussions / private advisory notes authored by this mentor
    try:
        from services.collaboration import list_case_messages
        msgs = list_case_messages(aspirant_id=aspirant_id, requesting_role="admin")
        for m in msgs:
            if str(m.get("author_id")) == str(mentor_id) and m.get("created_at"):
                # verify author role matches or author is this mentor
                if m.get("author_role") in (mentor_role, None):
                    timestamps.append(datetime.fromisoformat(m["created_at"].replace("Z", "+00:00")))
    except Exception:
        pass

    # 4. Check help requests / consultations (Mentor responses ONLY)
    try:
        from services.help_requests import list_requests
        reqs = list_requests(aspirant_id=aspirant_id)
        for req in reqs:
            # Verify ticket relevancy for this mentor role
            is_relevant = False
            if mentor_role == "guide":
                if str(req.get("assigned_guide_id")) == str(mentor_id) or (req.get("requester_role") == "guide" and str(req.get("requester_id")) == str(mentor_id)):
                    is_relevant = True
            elif mentor_role == "sme":
                if str(req.get("assigned_sme_id")) == str(mentor_id) or (req.get("requester_role") == "sme" and str(req.get("requester_id")) == str(mentor_id)):
                    is_relevant = True

            if str(req.get("resolved_by")) == str(mentor_id) or str(req.get("last_interaction_actor_id")) == str(mentor_id):
                is_relevant = True

            if not is_relevant:
                continue

            actor_role = req.get("last_interaction_actor_role")
            actor_id = req.get("last_interaction_actor_id")

            # CRITICAL RULE: NEVER count Aspirant responses!
            if actor_role == "aspirant":
                # Only use prior mentor response timestamp if present
                if req.get("last_mentor_response_at"):
                    # Check that the prior mentor response belonged to this mentor/role
                    if str(req.get("resolved_by")) == str(mentor_id) or (req.get("assigned_guide_id") == mentor_id and mentor_role == "guide") or (req.get("assigned_sme_id") == mentor_id and mentor_role == "sme"):
                        timestamps.append(datetime.fromisoformat(req["last_mentor_response_at"].replace("Z", "+00:00")))
                continue

            # 4a. Mentor directly interacted as last actor
            if str(actor_id) == str(mentor_id) and actor_role == mentor_role:
                t_str = req.get("last_mentor_response_at") or req.get("last_handled_at") or req.get("updated_at")
                if t_str:
                    timestamps.append(datetime.fromisoformat(t_str.replace("Z", "+00:00")))
            elif req.get("last_mentor_response_at") and str(req.get("resolved_by")) == str(mentor_id):
                timestamps.append(datetime.fromisoformat(req["last_mentor_response_at"].replace("Z", "+00:00")))
            elif req.get("guide_response") and mentor_role == "guide" and str(req.get("resolved_by")) == str(mentor_id):
                t_str = req.get("resolved_at") or req.get("last_handled_at")
                if t_str:
                    timestamps.append(datetime.fromisoformat(t_str.replace("Z", "+00:00")))
            elif req.get("sme_response") and mentor_role == "sme" and str(req.get("resolved_by")) == str(mentor_id):
                t_str = req.get("resolved_at") or req.get("last_handled_at")
                if t_str:
                    timestamps.append(datetime.fromisoformat(t_str.replace("Z", "+00:00")))
    except Exception:
        pass

    # Filter out timestamps prior to assignment date if given
    if assignment_date:
        timestamps = [t for t in timestamps if t >= assignment_date]

    if timestamps:
        return max(timestamps)
    return None


# ─────────────────────────────────────────────────────────────────────────────
# 2. CASELOAD SCANNER (GUIDES + SMES)
# ─────────────────────────────────────────────────────────────────────────────
def check_and_process_caseload_inactivity() -> List[Dict]:
    """
    Evaluates all active Guide and SME assignments for inactivity.
    Scans:
      - Primary Guides
      - Additional/Co-Guides (Guide B)
      - Primary Domain SMEs
      - Additional Domain SMEs

    Enforces:
      - Active role and NDA verification before scanning
      - Independent inactivity clocks
      - Episode-level deduplication
      - Day 7 (Mentor reminder), Day 10 (Admin alert), Day 14 (Admin escalation)
    """
    from services.relationships import get_all_relationships
    from services.notifications import create_notification
    from services.profiles import get_profile
    from services.governance import get_primary_admin_id
    from services.roles import user_has_active_role
    from services.legal import check_user_nda_accepted

    relationships = get_all_relationships()
    now = datetime.now(timezone.utc)
    results = []
    admin_id = get_primary_admin_id()

    # Pre-fetch assignment histories for accurate effective assignment dates
    db = get_local_db()
    all_asg_hist = []
    if hasattr(db, "list_assignment_history"):
        try:
            all_asg_hist = db.list_assignment_history()
        except Exception:
            all_asg_hist = []

    def _get_assignment_effective_date(asp_id: str, m_id: str, m_role: str, fallback_dt: datetime) -> datetime:
        matching = [
            h for h in all_asg_hist
            if str(h.get("aspirant_id")) == str(asp_id)
            and str(h.get("mentor_id")) == str(m_id)
            and h.get("mentor_role") == m_role
            and h.get("action") == "ASSIGNED"
        ]
        if matching:
            # Sort by created_at desc
            t_str = matching[0].get("created_at")
            if t_str:
                try:
                    return datetime.fromisoformat(t_str.replace("Z", "+00:00"))
                except Exception:
                    pass
        return fallback_dt

    for rel in relationships:
        if rel.get("status") != "active":
            continue

        aspirant_id = rel.get("aspirant_id")
        if not aspirant_id:
            continue

        rel_id = rel.get("id")
        rel_created_str = rel.get("created_at")
        rel_created_dt = (
            datetime.fromisoformat(rel_created_str.replace("Z", "+00:00"))
            if rel_created_str
            else (now - timedelta(days=1))
        )

        asp_profile = get_profile(aspirant_id) or {}
        asp_name = asp_profile.get("full_name", "Entrepreneur")

        # ── Collect all distinct authorized Guides ──
        guide_ids: List[str] = []
        if rel.get("guide_id"):
            guide_ids.append(rel["guide_id"])
        add_g = rel.get("guide_ids") or []
        if isinstance(add_g, str):
            try: add_g = json.loads(add_g)
            except Exception: add_g = []
        if isinstance(add_g, list):
            for gid in add_g:
                if gid and gid not in guide_ids:
                    guide_ids.append(gid)

        # ── Collect all distinct authorized SMEs ──
        sme_ids: List[str] = []
        if rel.get("sme_id"):
            sme_ids.append(rel["sme_id"])
        add_s = rel.get("sme_ids") or []
        if isinstance(add_s, str):
            try: add_s = json.loads(add_s)
            except Exception: add_s = []
        if isinstance(add_s, list):
            for sid in add_s:
                if sid and sid not in sme_ids:
                    sme_ids.append(sid)

        # Build list of distinct assignments: (mentor_id, mentor_role)
        assignments: List[Tuple[str, str]] = []
        for gid in guide_ids:
            if user_has_active_role(gid, "guide") and check_user_nda_accepted(gid, "guide"):
                assignments.append((gid, "guide"))

        for sid in sme_ids:
            if user_has_active_role(sid, "sme") and check_user_nda_accepted(sid, "sme"):
                assignments.append((sid, "sme"))

        for mentor_id, mentor_role in assignments:
            asg_date = _get_assignment_effective_date(aspirant_id, mentor_id, mentor_role, rel_created_dt)
            last_date = get_last_interaction_date(mentor_id, aspirant_id, mentor_role, asg_date)

            if not last_date:
                last_date = asg_date

            days_inactive = (now - last_date).days
            if days_inactive < 7:
                continue

            # Deterministic episode key based on last interaction date
            episode_id = f"ep_{mentor_id[:8]}_{aspirant_id[:8]}_{last_date.strftime('%Y%m%d%H%M')}"
            m_profile = get_profile(mentor_id) or {}
            m_name = m_profile.get("full_name") or ("Guide" if mentor_role == "guide" else "Domain SME")

            if days_inactive >= 14:
                stage = "DAY_14_ADMIN_REVIEW"
                if _record_inactivity_log(rel_id, mentor_id, aspirant_id, days_inactive, stage, mentor_role, episode_id):
                    role_lbl = "Guide" if mentor_role == "guide" else "Domain SME"
                    term_lbl = "caseload" if mentor_role == "guide" else "advisory"
                    create_notification(
                        user_id=admin_id,
                        title=f"Critical Inactivity Escalation (14 Days) — {role_lbl}",
                        message=f"{role_lbl} {m_name} has not interacted with {asp_name} for {days_inactive} days. Urgent {term_lbl} review or reassignment recommended.",
                        notification_type="INACTIVITY_CRITICAL",
                        actor_id=mentor_id
                    )
                    results.append({"mentor_id": mentor_id, "mentor_role": mentor_role, "aspirant_id": aspirant_id, "stage": stage, "days": days_inactive})

            elif days_inactive >= 10:
                stage = "DAY_10_ADMIN_ALERT"
                if _record_inactivity_log(rel_id, mentor_id, aspirant_id, days_inactive, stage, mentor_role, episode_id):
                    role_lbl = "Guide" if mentor_role == "guide" else "Domain SME"
                    create_notification(
                        user_id=admin_id,
                        title=f"Mentor Inactivity Alert (10 Days) — {role_lbl}",
                        message=f"{role_lbl} {m_name} has not interacted with {asp_name} for {days_inactive} days. Automated monitoring notification dispatched.",
                        notification_type="INACTIVITY_WARNING",
                        actor_id=mentor_id
                    )
                    results.append({"mentor_id": mentor_id, "mentor_role": mentor_role, "aspirant_id": aspirant_id, "stage": stage, "days": days_inactive})

            elif days_inactive >= 7:
                stage = "DAY_7_REMINDER"
                if _record_inactivity_log(rel_id, mentor_id, aspirant_id, days_inactive, stage, mentor_role, episode_id):
                    if mentor_role == "guide":
                        title_msg = "Friendly Reminder: Entrepreneur Check-in"
                        body_msg = f"It has been {days_inactive} days since your last update with {asp_name}. Please review their journey or recommend schemes."
                    else:
                        title_msg = "Friendly Reminder: Technical Advisory Check-in"
                        body_msg = f"It has been {days_inactive} days since your last advisory update with {asp_name}. Please review pending consultation requests."

                    create_notification(
                        user_id=mentor_id,
                        title=title_msg,
                        message=body_msg,
                        notification_type="INACTIVITY_REMINDER",
                        actor_id=admin_id
                    )
                    results.append({"mentor_id": mentor_id, "mentor_role": mentor_role, "aspirant_id": aspirant_id, "stage": stage, "days": days_inactive})

    return results


# ─────────────────────────────────────────────────────────────────────────────
# 3. IDEMPOTENT INACTIVITY RECORDING
# ─────────────────────────────────────────────────────────────────────────────
def _record_inactivity_log(
    relationship_id: Optional[str],
    mentor_id: str,
    aspirant_id: str,
    days: int,
    stage: str,
    mentor_role: str = "guide",
    inactivity_episode: Optional[str] = None
) -> bool:
    """
    Records an inactivity stage log entry.
    Maintains 100% backward compatibility by always populating guide_id=mentor_id.
    Returns True if successfully logged (first time for this episode & stage), False if duplicate.
    """
    log_id = str(uuid.uuid4())
    now_iso = datetime.now(timezone.utc).isoformat()

    record = {
        "id": log_id,
        "relationship_id": relationship_id,
        "guide_id": mentor_id,  # Maintains backwards compat with legacy queries & foreign keys
        "mentor_id": mentor_id,
        "mentor_role": mentor_role,
        "aspirant_id": aspirant_id,
        "days_inactive": days,
        "escalation_stage": stage,
        "inactivity_episode": inactivity_episode,
        "status": "ACTIVE",
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


# ─────────────────────────────────────────────────────────────────────────────
# 4. LISTING & AUDIT ENRICHMENT
# ─────────────────────────────────────────────────────────────────────────────
def list_inactivity_records(
    mentor_role: Optional[str] = None,
    aspirant_id: Optional[str] = None,
    mentor_id: Optional[str] = None
) -> List[Dict]:
    """Retrieves all inactivity logs for admin review with backward-compatible defaults."""
    backend = get_data_backend()
    records = []

    if backend == "supabase":
        admin = get_supabase_admin_client()
        if admin:
            try:
                q = admin.table("inactivity_logs").select("*").order("created_at", desc=True)
                if mentor_role:
                    q = q.eq("mentor_role", mentor_role)
                if aspirant_id:
                    q = q.eq("aspirant_id", aspirant_id)
                res = q.execute()
                records = res.data or []
            except Exception:
                pass

    if not records:
        db = get_local_db()
        if hasattr(db, "list_inactivity_logs"):
            records = db.list_inactivity_logs(
                aspirant_id=aspirant_id,
                mentor_id=mentor_id,
                mentor_role=mentor_role
            )

    # Ensure backward-compatible dictionary keys
    for r in records:
        if not r.get("mentor_id"):
            r["mentor_id"] = r.get("guide_id")
        if not r.get("mentor_role"):
            r["mentor_role"] = "guide"
        if not r.get("status"):
            r["status"] = "ACTIVE"

    return records


def mark_inactivity_followup_sent(
    inactivity_record_id: str,
    channel: str,
    admin_id: str,
    notes: str = ""
) -> bool:
    """Updates the inactivity log to indicate that manual follow-up was dispatched."""
    now_iso = datetime.now(timezone.utc).isoformat()
    backend = get_data_backend()
    if backend == "supabase":
        admin = get_supabase_admin_client()
        if admin:
            try:
                admin.table("inactivity_logs").update({
                    "status": "FOLLOW_UP_INITIATED",
                    "follow_up_channel": channel,
                    "follow_up_sent_at": now_iso,
                    "follow_up_notes": notes
                }).eq("id", inactivity_record_id).execute()
            except Exception as e:
                print(f"[Inactivity] Supabase follow-up update note: {e}")

    db = get_local_db()
    if hasattr(db, "update_inactivity_log_followup"):
        return db.update_inactivity_log_followup(inactivity_record_id, channel, notes)

    return True


# ─────────────────────────────────────────────────────────────────────────────
# 5. LIVE STATUS EVALUATION
# ─────────────────────────────────────────────────────────────────────────────
def compute_alert_live_status(
    record: Dict,
    current_relationships: Optional[List[Dict]] = None
) -> Tuple[str, str, int, Optional[str]]:
    """
    Dynamically assesses the current live state of an inactivity record against
    real-time assignment and engagement data.

    Returns:
      (status_label, badge_color, live_days_inactive, last_verified_engagement_str)

    Status Labels:
      - 'Needs Attention': Currently inactive and no follow-up dispatched
      - 'Follow-up Initiated': Follow-up reminder was marked sent by Admin
      - 'Mentor Active Again': Mentor has resumed meaningful work since the alert
      - 'Resolved': Manually marked resolved
      - 'Historical Record': Mentor no longer actively assigned to this entrepreneur
    """
    mentor_id = record.get("mentor_id") or record.get("guide_id", "")
    aspirant_id = record.get("aspirant_id", "")
    mentor_role = record.get("mentor_role", "guide")
    recorded_days = record.get("days_inactive", 0)
    notif_sent_str = record.get("notification_sent_at") or record.get("created_at")

    notif_dt = (
        datetime.fromisoformat(notif_sent_str.replace("Z", "+00:00"))
        if notif_sent_str
        else datetime.now(timezone.utc)
    )

    # 1. Verify active relationship
    from services.relationships import get_all_relationships
    rels = current_relationships if current_relationships is not None else get_all_relationships()

    is_currently_assigned = False
    for rel in rels:
        if rel.get("status") == "active" and str(rel.get("aspirant_id")) == str(aspirant_id):
            if mentor_role == "guide":
                g_ids = [rel.get("guide_id")]
                add_g = rel.get("guide_ids") or []
                if isinstance(add_g, str):
                    try: add_g = json.loads(add_g)
                    except Exception: add_g = []
                if isinstance(add_g, list): g_ids.extend(add_g)
                if any(str(gid) == str(mentor_id) for gid in g_ids if gid):
                    is_currently_assigned = True
                    break
            elif mentor_role == "sme":
                s_ids = [rel.get("sme_id")]
                add_s = rel.get("sme_ids") or []
                if isinstance(add_s, str):
                    try: add_s = json.loads(add_s)
                    except Exception: add_s = []
                if isinstance(add_s, list): s_ids.extend(add_s)
                if any(str(sid) == str(mentor_id) for sid in s_ids if sid):
                    is_currently_assigned = True
                    break

    if not is_currently_assigned:
        return "Historical Record", "#64748B", recorded_days, "Assignment concluded"

    # 2. Check for recent meaningful interaction since the alert
    latest_dt = get_last_interaction_date(mentor_id, aspirant_id, mentor_role)
    now = datetime.now(timezone.utc)

    if latest_dt and latest_dt > notif_dt:
        days_since = (now - latest_dt).days
        date_str = latest_dt.strftime("%d %b %Y")
        return "Mentor Active Again", "#10B981", days_since, f"Active on {date_str} ({days_since}d ago)"

    live_days = (now - latest_dt).days if latest_dt else recorded_days
    last_eng_str = f"Last verified engagement: {live_days} days ago" if latest_dt else "No verified interaction since assignment"

    # 3. Check follow-up status
    if record.get("status") == "RESOLVED":
        return "Resolved", "#059669", live_days, last_eng_str

    if record.get("follow_up_sent_at") or record.get("status") == "FOLLOW_UP_INITIATED":
        fu_channel = (record.get("follow_up_channel") or "External").title()
        return f"Follow-up Initiated ({fu_channel})", "#3B82F6", live_days, last_eng_str

    # 3b. Check if mentor has already responded and is waiting on the Aspirant's reply (SLA Grace)
    try:
        from services.help_requests import list_requests
        reqs = list_requests(aspirant_id=aspirant_id)
        mentor_tickets = [
            r for r in reqs
            if (mentor_role == "guide" and str(r.get("assigned_guide_id")) == str(mentor_id))
            or (mentor_role == "sme" and str(r.get("assigned_sme_id")) == str(mentor_id))
        ]
        active_mentor_tickets = [r for r in mentor_tickets if r.get("status") not in ("RESOLVED",)]
        if active_mentor_tickets and all(r.get("status") == "WAITING_ON_ASPIRANT" for r in active_mentor_tickets) and live_days <= 21:
            return "Waiting on Entrepreneur Reply", "#8B5CF6", live_days, f"{last_eng_str} (Awaiting founder reply)"
    except Exception:
        pass

    # 4. Needs Attention
    stage = record.get("escalation_stage", "")
    badge_color = "#DC2626" if "DAY_14" in stage else "#F59E0B"
    return "Needs Attention", badge_color, live_days, last_eng_str


# ─────────────────────────────────────────────────────────────────────────────
# 6. SUPPORTIVE ASPIRANT ENGAGEMENT & BLOCKER MONITOR (DEC-05: 14 / 30 / 60 DAYS)
# ─────────────────────────────────────────────────────────────────────────────
def evaluate_aspirant_engagement_roster() -> List[Dict]:
    """
    Supportive, blocker-aware Aspirant Engagement Monitor (14 / 30 / 60 days).
    Never penalizes or suspends an entrepreneur; first checks whether the founder
    is blocked on Fulcrum (unassigned Guide, waiting on mentor reply, stalled onboarding,
    or waiting on first scheme release) before classifying 14d/30d/60d quietness.
    """
    cached = get_memo("aspirant_engagement_roster")
    if cached is not None:
        return cached

    from services.roles import list_active_profiles_for_role
    from services.relationships import get_all_relationships
    from services.help_requests import list_requests
    from services.schemes import get_released_schemes_for_aspirant
    from services.journey import get_journey_timeline
    from services.profiles import get_profiles_batch

    aspirants = list_active_profiles_for_role("aspirant")
    all_rels = get_all_relationships()
    rel_by_asp = {str(r.get("aspirant_id")): r for r in all_rels if r.get("status") == "active" and r.get("aspirant_id")}
    all_tickets = list_requests()
    tickets_by_asp: Dict[str, List[Dict]] = {}
    for t in all_tickets:
        aid = str(t.get("aspirant_id") or "")
        if aid:
            tickets_by_asp.setdefault(aid, []).append(t)

    guide_ids = [str(r.get("guide_id")) for r in all_rels if r.get("guide_id")]
    guide_profiles = get_profiles_batch(guide_ids)

    now = datetime.now(timezone.utc)
    roster: List[Dict] = []

    for asp in aspirants:
        asp_id = str(asp.get("id") or "")
        if not asp_id:
            continue
        comp_pct = int(asp.get("completion_pct") or 0)
        rel = rel_by_asp.get(asp_id)
        guide_id = str(rel.get("guide_id")) if (rel and rel.get("guide_id")) else None
        guide_prof = guide_profiles.get(guide_id) if guide_id else None
        guide_name = guide_prof.get("full_name", "Unassigned") if guide_prof else "Unassigned"

        asp_tickets = tickets_by_asp.get(asp_id, [])
        released_schemes = get_released_schemes_for_aspirant(asp_id)
        events = get_journey_timeline(asp_id)

        # Compute last verified Aspirant activity timestamp
        asp_timestamps: List[datetime] = []
        for field in ("updated_at", "created_at"):
            val = asp.get(field)
            if val:
                try:
                    asp_timestamps.append(datetime.fromisoformat(str(val).replace("Z", "+00:00")))
                except Exception:
                    pass
        for ev in events:
            if ev.get("actor_role") == "aspirant" and ev.get("created_at"):
                try:
                    asp_timestamps.append(datetime.fromisoformat(str(ev["created_at"]).replace("Z", "+00:00")))
                except Exception:
                    pass
        for tk in asp_tickets:
            for tf in ("last_aspirant_response_at", "created_at"):
                tval = tk.get(tf)
                if tval and (tf == "last_aspirant_response_at" or tk.get("requester_role") in (None, "aspirant")):
                    try:
                        asp_timestamps.append(datetime.fromisoformat(str(tval).replace("Z", "+00:00")))
                    except Exception:
                        pass

        last_active_dt = max(asp_timestamps) if asp_timestamps else (now - timedelta(days=1))
        days_quiet = max(0, (now - last_active_dt).days)

        # Check Blocker Exclusion Rules BEFORE classifying quietness
        waiting_on_mentor_tickets = [
            tk for tk in asp_tickets
            if tk.get("status") in ("OPEN", "IN_PROGRESS", "WAITING_ON_GUIDE_SME")
        ]
        waiting_on_aspirant_tickets = [
            tk for tk in asp_tickets
            if tk.get("status") == "WAITING_ON_ASPIRANT"
        ]

        if not guide_id:
            category = "BLOCKED_ON_ADMIN"
            badge_label = "Blocked on Admin (No Guide Assigned)"
            badge_color = "#DC2626"
            recommended_action = "Assign a Dedicated Guide in Tab 2 (Guide Assignments)."
        elif waiting_on_mentor_tickets:
            category = "WAITING_ON_MENTOR"
            badge_label = f"Waiting on Mentor Reply ({len(waiting_on_mentor_tickets)} Open)"
            badge_color = "#D97706"
            recommended_action = "Follow up with assigned Guide/SME to answer pending consultation."
        elif comp_pct < 60:
            category = "STALLED_ONBOARDING"
            badge_label = f"Stalled Onboarding ({comp_pct}% Profile)"
            badge_color = "#7C3AED"
            recommended_action = "Guide should send a supportive check-in to help complete Business & Assistance profile."
        elif len(released_schemes) == 0 and days_quiet >= 7:
            category = "WAITING_ON_SCHEME_RELEASE"
            badge_label = "Waiting on Guide Scheme Release"
            badge_color = "#2563EB"
            recommended_action = "Guide should evaluate and release initial curated scheme recommendations."
        elif days_quiet >= 60:
            category = "DAY_60_DORMANT_REVIEW"
            badge_label = f"60d+ Dormant Review ({days_quiet}d quiet)"
            badge_color = "#64748B"
            recommended_action = "Admin & Guide review: Send supportive re-engagement outreach (never auto-archived)."
        elif days_quiet >= 30:
            category = "DAY_30_SUPPORTIVE_OUTREACH"
            badge_label = f"30d Supportive Outreach ({days_quiet}d quiet)"
            badge_color = "#F59E0B"
            recommended_action = "Guide outreach recommended via WhatsApp/Email or Proactive Consultation."
        elif days_quiet >= 14:
            category = "DAY_14_GENTLE_CHECKIN"
            badge_label = f"14d Gentle Check-In ({days_quiet}d quiet)"
            badge_color = "#3B82F6"
            recommended_action = "Gentle Guide check-in on venture milestones or DPR progress."
        else:
            category = "ACTIVE_ENGAGED"
            badge_label = f"Active & Engaged ({days_quiet}d ago)"
            badge_color = "#10B981"
            recommended_action = "No intervention needed; venture is actively progressing."

        roster.append({
            "aspirant_id": asp_id,
            "aspirant_name": asp.get("full_name", "Entrepreneur"),
            "aspirant_email": asp.get("email", ""),
            "aspirant_phone": asp.get("phone", ""),
            "district": asp.get("district", "Tamil Nadu"),
            "completion_pct": comp_pct,
            "guide_id": guide_id,
            "guide_name": guide_name,
            "days_quiet": days_quiet,
            "last_active_str": last_active_dt.strftime("%d %b %Y"),
            "released_schemes_count": len(released_schemes),
            "open_tickets_count": len(waiting_on_mentor_tickets),
            "waiting_on_aspirant_count": len(waiting_on_aspirant_tickets),
            "category": category,
            "badge_label": badge_label,
            "badge_color": badge_color,
            "recommended_action": recommended_action
        })

    # Sort so blockers and longest quietness appear first
    priority_order = {
        "BLOCKED_ON_ADMIN": 0,
        "WAITING_ON_MENTOR": 1,
        "STALLED_ONBOARDING": 2,
        "WAITING_ON_SCHEME_RELEASE": 3,
        "DAY_60_DORMANT_REVIEW": 4,
        "DAY_30_SUPPORTIVE_OUTREACH": 5,
        "DAY_14_GENTLE_CHECKIN": 6,
        "ACTIVE_ENGAGED": 7
    }
    roster.sort(key=lambda x: (priority_order.get(x["category"], 9), -x["days_quiet"]))
    set_memo("aspirant_engagement_roster", roster, ttl_seconds=30)
    return roster
