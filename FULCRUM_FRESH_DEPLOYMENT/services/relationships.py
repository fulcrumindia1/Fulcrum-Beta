"""
services/relationships.py — Relationship Assignment Service for FULCRUM-INDIA
=============================================================================
Enforces the mandatory business rule:
- The Admin is the SOLE AUTHORITY for assigning Guides and SMEs.
- Aspirants cannot assign Guides or SMEs.
- Mentors cannot self-assign.
- Assignments automatically generate meaningful chronological Journey events.
Supports dual backends: Supabase (primary) and SQLite (explicit local development).
"""

import json
from datetime import datetime, timezone
from typing import Optional, Dict, List, Tuple
from services.auth import get_supabase_client, get_supabase_admin_client, get_data_backend
from services.local_db import get_local_db
from services.cache import get_memo, set_memo, invalidate_memo

def _get_user_client():
    """Returns the authenticated user's Supabase client (RLS-enforced)."""
    return get_supabase_client()

def _get_admin_client():
    """Returns the privileged admin Supabase client (bypasses RLS). Use sparingly."""
    return get_supabase_admin_client()

ACTIVE_TICKET_STATUSES = ("OPEN", "IN_PROGRESS", "WAITING_ON_ASPIRANT", "WAITING_ON_GUIDE_SME")

def get_all_relationships() -> List[Dict]:
    """Retrieves all active relationship records (memoized for 60s)."""
    cached = get_memo("all_relationships")
    if cached is not None:
        return cached
    backend = get_data_backend()
    if backend == "supabase":
        client = _get_admin_client() or _get_user_client()
        if client:
            try:
                res = client.table("relationships").select("*").eq("status", "active").execute()
                rows = res.data or []
                set_memo("all_relationships", rows, ttl_seconds=60)
                return rows
            except Exception:
                pass
    db = get_local_db()
    if hasattr(db, "list_all_relationships"):
        rows = db.list_all_relationships()
        set_memo("all_relationships", rows, ttl_seconds=60)
        return rows
    return []

def get_aspirant_mentors(aspirant_id: str) -> Dict[str, Optional[Dict]]:
    """Fetches assigned Guide and SME details for an Aspirant from active backend with memoization & batch profile queries."""
    if not aspirant_id:
        return {"guide": None, "guide_b": None, "guides": [], "sme": None, "smes": [], "relationship": None}

    cached = get_memo(f"mentors:{aspirant_id}")
    if cached is not None:
        return cached

    backend = get_data_backend()
    from services.profiles import get_profiles_batch

    if backend == "supabase":
        admin = _get_admin_client()
        client = _get_user_client()
        fetcher = admin if admin else client
        rel = None
        if fetcher:
            try:
                res = fetcher.table("relationships").select("*").eq("aspirant_id", aspirant_id).execute()
                if res.data and len(res.data) > 0:
                    rel = res.data[0]
            except Exception as e:
                print(f"[Relationships] Supabase query error: {e}")

        guide = None
        guides = []
        guide_b = None
        sme = None
        smes = []
        if rel:
            guide_ids = rel.get("guide_ids") or []
            if isinstance(guide_ids, str):
                try: guide_ids = json.loads(guide_ids)
                except Exception: guide_ids = []
            if not isinstance(guide_ids, list):
                guide_ids = []
            if rel.get("guide_id") and rel["guide_id"] not in guide_ids:
                guide_ids.insert(0, rel["guide_id"])

            sme_ids = rel.get("sme_ids") or []
            if isinstance(sme_ids, str):
                try: sme_ids = json.loads(sme_ids)
                except Exception: sme_ids = []
            if not isinstance(sme_ids, list):
                sme_ids = []
            if rel.get("sme_id") and rel["sme_id"] not in sme_ids:
                sme_ids.insert(0, rel["sme_id"])

            all_mentor_ids = list(set(guide_ids + sme_ids))
            mentor_profiles = get_profiles_batch(all_mentor_ids)

            for gid in guide_ids:
                gp = mentor_profiles.get(gid)
                if gp and not any(existing["id"] == gp["id"] for existing in guides):
                    gp_copy = dict(gp)
                    try:
                        from services.roles import get_user_roles
                        g_roles = get_user_roles(gid)
                        g_rec = next((r for r in g_roles if r.get("role") == "guide"), None)
                        gp_copy["role_status"] = g_rec.get("status", "active") if g_rec else "active"
                    except Exception:
                        gp_copy["role_status"] = "active"
                    guides.append(gp_copy)
            if guides:
                guide = guides[0]
            if len(guides) > 1:
                guide_b = guides[1]

            for sid in sme_ids:
                sp = mentor_profiles.get(sid)
                if sp and not any(existing["id"] == sp["id"] for existing in smes):
                    sp_copy = dict(sp)
                    try:
                        from services.roles import get_user_roles
                        s_roles = get_user_roles(sid)
                        s_rec = next((r for r in s_roles if r.get("role") == "sme"), None)
                        sp_copy["role_status"] = s_rec.get("status", "active") if s_rec else "active"
                    except Exception:
                        sp_copy["role_status"] = "active"
                    smes.append(sp_copy)
            if smes:
                sme = smes[0]

        res_dict = {
            "guide": guide,
            "guide_b": guide_b,
            "guides": guides,
            "sme": sme,
            "smes": smes,
            "relationship": rel
        }
        set_memo(f"mentors:{aspirant_id}", res_dict, ttl_seconds=60)
        return res_dict

    # SQLite local mode
    rel = get_local_db().get_relationship(aspirant_id)
    guide = None
    guides = []
    guide_b = None
    sme = None
    smes = []
    if rel:
        guide_ids = rel.get("guide_ids") or []
        if isinstance(guide_ids, str):
            try: guide_ids = json.loads(guide_ids)
            except Exception: guide_ids = []
        if not isinstance(guide_ids, list):
            guide_ids = []
        if rel.get("guide_id") and rel["guide_id"] not in guide_ids:
            guide_ids.insert(0, rel["guide_id"])

        sme_ids = rel.get("sme_ids") or []
        if isinstance(sme_ids, str):
            try: sme_ids = json.loads(sme_ids)
            except Exception: sme_ids = []
        if not isinstance(sme_ids, list):
            sme_ids = []
        if rel.get("sme_id") and rel["sme_id"] not in sme_ids:
            sme_ids.insert(0, rel["sme_id"])

        all_mentor_ids = list(set(guide_ids + sme_ids))
        mentor_profiles = get_profiles_batch(all_mentor_ids)

        for gid in guide_ids:
            gp = mentor_profiles.get(gid)
            if gp and not any(existing["id"] == gp["id"] for existing in guides):
                gp_copy = dict(gp)
                try:
                    from services.roles import get_user_roles
                    g_roles = get_user_roles(gid)
                    g_rec = next((r for r in g_roles if r.get("role") == "guide"), None)
                    gp_copy["role_status"] = g_rec.get("status", "active") if g_rec else "active"
                except Exception:
                    gp_copy["role_status"] = "active"
                guides.append(gp_copy)
        if guides:
            guide = guides[0]
        if len(guides) > 1:
            guide_b = guides[1]

        for sid in sme_ids:
            sp = mentor_profiles.get(sid)
            if sp and not any(existing["id"] == sp["id"] for existing in smes):
                sp_copy = dict(sp)
                try:
                    from services.roles import get_user_roles
                    s_roles = get_user_roles(sid)
                    s_rec = next((r for r in s_roles if r.get("role") == "sme"), None)
                    sp_copy["role_status"] = s_rec.get("status", "active") if s_rec else "active"
                except Exception:
                    sp_copy["role_status"] = "active"
                smes.append(sp_copy)
        if smes:
            sme = smes[0]

    res_dict = {
        "guide": guide,
        "guide_b": guide_b,
        "guides": guides,
        "sme": sme,
        "smes": smes,
        "relationship": rel
    }
    set_memo(f"mentors:{aspirant_id}", res_dict, ttl_seconds=60)
    return res_dict

def assign_guide(
    aspirant_id: str,
    guide_id: str,
    admin_id: Optional[str] = None,
    notes: str = "",
    assigned_by: Optional[str] = None,
    mode: str = "replace",
    replace_target_id: Optional[str] = None,
    allow_pending_nda: bool = False
) -> Tuple[bool, Optional[str]]:
    """Admin assigns Guide to an Aspirant with transition history and alerts.
    mode='replace': replaces the primary Guide or a specified replace_target_id.
    mode='add': assigns as Co-Guide (Guide B) alongside existing Guides.
    Requires verified Sole Admin authorization.
    """
    admin_id = admin_id or assigned_by
    from services.roles import require_sole_admin, user_has_active_role
    ok_admin, err_admin = require_sole_admin(actor_id=admin_id)
    if not ok_admin:
        return False, err_admin

    from services.profiles import get_profile
    from services.journey import log_meaningful_event
    from services.notifications import create_notification

    if str(aspirant_id) == str(guide_id):
        return False, "An entrepreneur cannot be assigned as their own Guide."

    guide = get_profile(guide_id)
    from services.roles import is_assignable_mentor
    ok_assign, err_assign = is_assignable_mentor(
        guide_id,
        "guide",
        allow_pending_nda=allow_pending_nda,
        aspirant_id=aspirant_id
    )
    if not ok_assign:
        return False, err_assign or "Selected mentor does not hold a valid Guide role grant."

    aspirant = get_profile(aspirant_id)
    if not aspirant:
        return False, "Aspirant not found."

    # Inspect current assignment
    curr_mentors = get_aspirant_mentors(aspirant_id)
    old_guide = curr_mentors.get("guide")
    old_guide_id = old_guide["id"] if old_guide else None
    existing_guides = curr_mentors.get("guides", [])
    existing_guide_ids = [g["id"] for g in existing_guides]

    target_to_replace = replace_target_id or old_guide_id

    if mode == "add":
        if guide_id in existing_guide_ids:
            return False, "This mentor is already assigned as a Guide to this entrepreneur."
        new_guide_ids = list(dict.fromkeys(existing_guide_ids + [guide_id]))
        primary_guide_id = old_guide_id or guide_id
        is_replacement = False
        is_co_guide = True
    else:  # mode == "replace"
        if target_to_replace and target_to_replace in existing_guide_ids:
            # Replace target mentor in guide_ids while preserving unrelated co-mentors
            new_guide_ids = [guide_id if gid == target_to_replace else gid for gid in existing_guide_ids]
            new_guide_ids = list(dict.fromkeys(new_guide_ids))
            if target_to_replace == old_guide_id:
                primary_guide_id = guide_id
            else:
                primary_guide_id = old_guide_id
        else:
            primary_guide_id = guide_id
            new_guide_ids = [guide_id]
        is_replacement = bool(target_to_replace and str(target_to_replace) != str(guide_id))
        is_co_guide = False

    backend = get_data_backend()
    now_iso = datetime.now(timezone.utc).isoformat()

    if backend == "supabase":
        client = _get_admin_client()
        if not client:
            return False, "Supabase client not available."
        try:
            client.table("relationships").upsert({
                "aspirant_id": aspirant_id,
                "guide_id": primary_guide_id,
                "guide_ids": new_guide_ids,
                "assigned_by": admin_id,
                "notes": notes,
                "status": "active",
                "updated_at": now_iso
            }, on_conflict="aspirant_id").execute()

            # Record idempotent assignment history
            import uuid
            action_label = "ASSIGNED" if not is_replacement else "REPLACED"
            hist_note = f"Co-Guide (Guide B) added. {notes}" if is_co_guide else notes
            hist_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{aspirant_id}:{guide_id}:{action_label}:{now_iso[:13]}"))
            client.table("assignment_history").upsert({
                "id": hist_id,
                "aspirant_id": aspirant_id,
                "mentor_id": guide_id,
                "mentor_role": "guide",
                "assigned_by": admin_id,
                "action": action_label,
                "previous_mentor_id": target_to_replace if is_replacement else None,
                "notes": hist_note,
                "created_at": now_iso
            }, on_conflict="id").execute()

            # Transfer open consultations to the replacement Guide if replaced
            if is_replacement and target_to_replace:
                try:
                    client.table("help_requests").update({
                        "assigned_guide_id": guide_id,
                        "updated_at": now_iso
                    }).eq("aspirant_id", aspirant_id).eq("assigned_guide_id", target_to_replace).in_("status", list(ACTIVE_TICKET_STATUSES)).execute()
                except Exception as ex_t:
                    print(f"[Relationships] Notice updating help_requests: {ex_t}")
        except Exception as e:
            return False, f"Failed to record Guide assignment in Supabase: {e}"

    else:
        # SQLite mode ONLY (when DATA_BACKEND=sqlite)
        conn = get_local_db()._get_conn()
        cur = conn.cursor()
        cur.execute("""
        UPDATE relationships
        SET guide_id = ?, guide_ids = ?, assigned_by = ?, notes = ?, updated_at = ?
        WHERE aspirant_id = ?
        """, (primary_guide_id, json.dumps(new_guide_ids), admin_id, notes, now_iso, aspirant_id))
        if cur.rowcount == 0:
            import uuid
            cur.execute("""
            INSERT INTO relationships (id, aspirant_id, guide_id, guide_ids, assigned_by, notes, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, 'active', ?, ?)
            """, (str(uuid.uuid4()), aspirant_id, primary_guide_id, json.dumps(new_guide_ids), admin_id, notes, now_iso, now_iso))
        conn.commit()
        conn.close()

        action_label = "ASSIGNED" if not is_replacement else "REPLACED"
        hist_note = f"Co-Guide (Guide B) added. {notes}" if is_co_guide else notes
        get_local_db().record_assignment_history(
            aspirant_id=aspirant_id,
            mentor_id=guide_id,
            mentor_role="guide",
            assigned_by=admin_id,
            action=action_label,
            previous_mentor_id=old_guide_id if is_replacement else None,
            notes=hist_note
        )
        if is_replacement:
            try:
                conn = get_local_db()._get_conn()
                cur = conn.cursor()
                cur.execute("UPDATE help_requests SET assigned_guide_id = ? WHERE aspirant_id = ? AND status IN ('OPEN', 'IN_PROGRESS', 'WAITING_ON_ASPIRANT', 'WAITING_ON_GUIDE_SME')", (guide_id, aspirant_id))
                conn.commit()
                conn.close()
            except Exception:
                pass

    guide_name = guide.get("full_name") or "Mentor"
    guide_exp = guide.get("profile_data", {}).get("expertise", "Business Guidance") if isinstance(guide.get("profile_data"), dict) else "Business Guidance"
    asp_name = aspirant.get("full_name") or "Entrepreneur"

    if is_replacement and old_guide:
        old_guide_name = old_guide.get("full_name", "Previous Guide")
        # 1. Alert old Guide
        create_notification(
            user_id=old_guide_id,
            title="Mentee Reassigned",
            message=f"You are no longer assigned as Guide to {asp_name}. Mentorship handed over to {guide_name}. Notes: {notes or 'No notes provided.'}",
            notification_type="guide_reassigned",
            actor_id=admin_id
        )
        # 2. Alert new Guide
        create_notification(
            user_id=guide_id,
            title="New Mentee Assigned (Reassignment)",
            message=f"You have been assigned as dedicated Guide for {asp_name}, succeeding {old_guide_name}. Notes: {notes or 'No notes provided.'}",
            notification_type="guide_assigned",
            actor_id=admin_id
        )
        # 3. Alert Aspirant
        create_notification(
            user_id=aspirant_id,
            title="Dedicated Guide Updated",
            message=f"Your dedicated Guide has been updated from {old_guide_name} to {guide_name} ({guide_exp}).",
            notification_type="guide_assigned",
            actor_id=admin_id
        )
        # 4. Journey Event
        log_meaningful_event(
            aspirant_id=aspirant_id,
            actor_id=guide_id,
            actor_role="guide",
            event_type="guide_reassigned",
            title="Guide Transitioned",
            description=f"Mentorship transition: Dedicated guide transitioned to {guide_name} ({guide_exp}).",
            metadata={"old_guide_id": old_guide_id, "new_guide_id": guide_id, "notes": notes}
        )
    else:
        # First-time Guide assignment
        # 1. Alert new Guide
        create_notification(
            user_id=guide_id,
            title="New Mentee Assigned",
            message=f"You have been assigned as dedicated Guide for {asp_name} ({aspirant.get('district', 'Tamil Nadu')}). Notes: {notes or 'No notes provided.'}",
            notification_type="guide_assigned",
            actor_id=admin_id
        )
        # 2. Alert Aspirant
        create_notification(
            user_id=aspirant_id,
            title="Dedicated Guide Assigned",
            message=f"{guide_name} ({guide_exp}) has been assigned as your institutional mentor.",
            notification_type="guide_assigned",
            actor_id=admin_id
        )
        # 3. Journey Event
        log_meaningful_event(
            aspirant_id=aspirant_id,
            actor_id=guide_id,
            actor_role="guide",
            event_type="guide_assigned",
            title="Guide Assigned",
            description=f"{guide_name} ({guide_exp}) assigned as dedicated mentor.",
            metadata={"guide_id": guide_id, "guide_name": guide_name, "notes": notes}
        )

    invalidate_memo("all_relationships")
    invalidate_memo(f"mentors:{aspirant_id}")
    invalidate_memo(f"guide_aspirants:{guide_id}")
    if primary_guide_id and primary_guide_id != guide_id:
        invalidate_memo(f"guide_aspirants:{primary_guide_id}")
    if old_guide_id:
        invalidate_memo(f"guide_aspirants:{old_guide_id}")

    return True, None

def assign_sme(
    aspirant_id: str,
    sme_id: str,
    admin_id: Optional[str] = None,
    notes: str = "",
    assigned_by: Optional[str] = None,
    mode: str = "add",
    replace_target_id: Optional[str] = None,
    allow_pending_nda: bool = False
) -> Tuple[bool, Optional[str]]:
    """Admin assigns SME to an Aspirant with transition history and alerts.
    mode="add": Appends SME to the Aspirant's advisory panel.
    mode="replace": Replaces old SME or specific replace_target_id while preserving other panel members.
    Requires verified Sole Admin authorization.
    """
    admin_id = admin_id or assigned_by
    from services.roles import require_sole_admin, user_has_active_role
    ok_admin, err_admin = require_sole_admin(actor_id=admin_id)
    if not ok_admin:
        return False, err_admin

    from services.profiles import get_profile
    from services.journey import log_meaningful_event
    from services.notifications import create_notification

    if str(aspirant_id) == str(sme_id):
        return False, "An entrepreneur cannot be assigned as their own SME."

    sme = get_profile(sme_id)
    from services.roles import is_assignable_mentor
    ok_assign, err_assign = is_assignable_mentor(
        sme_id,
        "sme",
        allow_pending_nda=allow_pending_nda,
        aspirant_id=aspirant_id
    )
    if not ok_assign:
        return False, err_assign or "Selected mentor does not hold a valid SME role grant."

    aspirant = get_profile(aspirant_id)
    if not aspirant:
        return False, "Aspirant not found."

    # Inspect current assignment to detect replacement or panel addition
    curr_mentors = get_aspirant_mentors(aspirant_id)
    old_sme = curr_mentors.get("sme")
    old_sme_id = old_sme["id"] if old_sme else None
    existing_sme_ids = [s["id"] for s in curr_mentors.get("smes", [])]

    target_to_replace = replace_target_id or old_sme_id

    if mode == "add":
        if sme_id in existing_sme_ids:
            return False, "This specialist is already assigned to this entrepreneur."
        new_sme_ids = list(dict.fromkeys(existing_sme_ids + [sme_id]))
        is_replacement = False
    else:  # mode == "replace"
        if target_to_replace and target_to_replace in existing_sme_ids:
            # Replace target SME in panel while preserving unrelated SMEs
            new_sme_ids = [sme_id if sid == target_to_replace else sid for sid in existing_sme_ids]
            new_sme_ids = list(dict.fromkeys(new_sme_ids))
        else:
            new_sme_ids = [sme_id]
        is_replacement = bool(target_to_replace and str(target_to_replace) != str(sme_id))

    backend = get_data_backend()
    now_iso = datetime.now(timezone.utc).isoformat()

    if backend == "supabase":
        client = _get_admin_client()
        if not client:
            return False, "Supabase client not available."
        try:
            try:
                client.table("relationships").upsert({
                    "aspirant_id": aspirant_id,
                    "sme_id": sme_id,
                    "sme_ids": new_sme_ids,
                    "assigned_by": admin_id,
                    "notes": notes,
                    "status": "active",
                    "updated_at": now_iso
                }, on_conflict="aspirant_id").execute()
            except Exception as ex_col:
                client.table("relationships").upsert({
                    "aspirant_id": aspirant_id,
                    "sme_id": sme_id,
                    "assigned_by": admin_id,
                    "notes": notes,
                    "status": "active",
                    "updated_at": now_iso
                }, on_conflict="aspirant_id").execute()

            # Record idempotent assignment history
            import uuid
            action_label = "REPLACED" if is_replacement else "ASSIGNED"
            hist_notes = f"[Advisory Panel Addition] {notes}" if (mode == "add" and notes) else (notes or ("[Advisory Panel Addition]" if mode == "add" else ""))
            hist_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{aspirant_id}:{sme_id}:{action_label}:{now_iso[:13]}"))
            client.table("assignment_history").upsert({
                "id": hist_id,
                "aspirant_id": aspirant_id,
                "mentor_id": sme_id,
                "mentor_role": "sme",
                "assigned_by": admin_id,
                "action": action_label,
                "previous_mentor_id": target_to_replace if is_replacement else None,
                "notes": hist_notes,
                "created_at": now_iso
            }, on_conflict="id").execute()
            if is_replacement and target_to_replace:
                try:
                    client.table("help_requests").update({
                        "assigned_sme_id": sme_id,
                        "updated_at": now_iso
                    }).eq("aspirant_id", aspirant_id).eq("assigned_sme_id", target_to_replace).in_("status", list(ACTIVE_TICKET_STATUSES)).execute()
                except Exception as ex_t:
                    print(f"[Relationships] Notice updating help_requests for SME: {ex_t}")
        except Exception as e:
            return False, f"Failed to record SME assignment in Supabase: {e}"
    else:
        # SQLite mode
        get_local_db().assign_sme(aspirant_id, sme_id, admin_id, notes, mode=mode)
        hist_notes = f"[Advisory Panel Addition] {notes}" if (mode == "add" and notes) else (notes or ("[Advisory Panel Addition]" if mode == "add" else ""))
        get_local_db().record_assignment_history(
            aspirant_id=aspirant_id,
            mentor_id=sme_id,
            mentor_role="sme",
            assigned_by=admin_id,
            action="REPLACED" if is_replacement else "ASSIGNED",
            previous_mentor_id=old_sme_id if is_replacement else None,
            notes=hist_notes
        )
        if is_replacement:
            try:
                conn = get_local_db()._get_conn()
                cur = conn.cursor()
                cur.execute("UPDATE help_requests SET assigned_sme_id = ? WHERE aspirant_id = ? AND status IN ('OPEN', 'IN_PROGRESS', 'WAITING_ON_ASPIRANT', 'WAITING_ON_GUIDE_SME')", (sme_id, aspirant_id))
                conn.commit()
                conn.close()
            except Exception:
                pass

    sme_name = sme.get("full_name") or "Specialist"
    prof_data = sme.get("profile_data") if isinstance(sme.get("profile_data"), dict) else {}
    sme_domain = prof_data.get("expertise") or prof_data.get("industry") or "Subject Matter Expertise"
    asp_name = aspirant.get("full_name") or "Entrepreneur"

    if is_replacement and old_sme:
        old_sme_name = old_sme.get("full_name", "Previous SME")
        # 1. Alert old SME
        create_notification(
            user_id=old_sme_id,
            title="Advisory Case Reassigned",
            message=f"You are no longer assigned as Domain SME for {asp_name}. Reassigned to {sme_name}. Notes: {notes or 'No notes provided.'}",
            notification_type="sme_reassigned",
            actor_id=admin_id
        )
        # 2. Alert new SME
        create_notification(
            user_id=sme_id,
            title="New Advisory Case Assigned",
            message=f"You have been assigned as Domain SME for {asp_name} ({sme_domain}). Notes: {notes or 'No notes provided.'}",
            notification_type="sme_assigned",
            actor_id=admin_id
        )
        # 3. Alert Aspirant
        create_notification(
            user_id=aspirant_id,
            title="Domain Specialist Updated",
            message=f"Your assigned SME for {sme_domain} has been updated to {sme_name}.",
            notification_type="sme_assigned",
            actor_id=admin_id
        )
        # 4. Journey Event
        log_meaningful_event(
            aspirant_id=aspirant_id,
            actor_id=sme_id,
            actor_role="sme",
            event_type="sme_reassigned",
            title="SME Transitioned",
            description=f"Domain specialist transitioned from {old_sme_name} to {sme_name} for {sme_domain}.",
            metadata={"old_sme_id": old_sme_id, "new_sme_id": sme_id, "notes": notes}
        )
    else:
        # First-time SME assignment or Addition to Panel
        # 1. Alert new SME
        create_notification(
            user_id=sme_id,
            title="New Advisory Case Assigned",
            message=f"You have been added to the Advisory Panel for {asp_name} ({sme_domain}). Notes: {notes or 'No notes provided.'}",
            notification_type="sme_assigned",
            actor_id=admin_id
        )
        # 2. Alert Aspirant
        create_notification(
            user_id=aspirant_id,
            title="Domain SME Added",
            message=f"{sme_name} ({sme_domain}) has been assigned to your advisory team.",
            notification_type="sme_assigned",
            actor_id=admin_id
        )
        # 3. Journey Event
        log_meaningful_event(
            aspirant_id=aspirant_id,
            actor_id=sme_id,
            actor_role="sme",
            event_type="sme_assigned",
            title="Specialist Assigned to Panel",
            description=f"{sme_name} assigned to your advisory panel for {sme_domain}.",
            metadata={"sme_id": sme_id, "sme_name": sme_name, "domain": sme_domain, "notes": notes}
        )

    invalidate_memo("all_relationships")
    invalidate_memo(f"mentors:{aspirant_id}")
    invalidate_memo(f"sme_aspirants:{sme_id}")
    if old_sme_id:
        invalidate_memo(f"sme_aspirants:{old_sme_id}")

    return True, None

def unassign_guide(aspirant_id: str, guide_id: str, admin_id: Optional[str] = None, reason: str = "") -> Tuple[bool, Optional[str]]:
    """Admin unassigns a dedicated Guide or Co-Guide from an Aspirant's caseload.
    Preserves historical journey events, scheme releases, and audit logs.
    Handles case handover and cache invalidation.
    Requires verified Sole Admin authorization.
    """
    from services.roles import require_sole_admin
    ok_admin, err_admin = require_sole_admin(actor_id=admin_id)
    if not ok_admin:
        return False, err_admin

    from services.profiles import get_profile
    from services.journey import log_meaningful_event
    from services.notifications import create_notification

    curr = get_aspirant_mentors(aspirant_id)
    guides = curr.get("guides", [])
    current_guide_ids = [g["id"] for g in guides]
    primary_guide_id = curr.get("guide", {}).get("id") if curr.get("guide") else None

    if guide_id not in current_guide_ids and guide_id != primary_guide_id:
        return False, "This Guide is not currently assigned to this entrepreneur."

    new_guide_ids = [gid for gid in current_guide_ids if gid != guide_id]
    if primary_guide_id == guide_id:
        new_primary_guide_id = new_guide_ids[0] if new_guide_ids else None
    else:
        new_primary_guide_id = primary_guide_id

    now_iso = datetime.now(timezone.utc).isoformat()
    backend = get_data_backend()

    if backend == "supabase":
        client = _get_admin_client()
        if not client:
            return False, "Supabase client not available."
        try:
            client.table("relationships").update({
                "guide_id": new_primary_guide_id,
                "guide_ids": new_guide_ids,
                "updated_at": now_iso
            }).eq("aspirant_id", aspirant_id).execute()

            import uuid
            hist_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{aspirant_id}:{guide_id}:UNASSIGNED:{now_iso[:13]}"))
            client.table("assignment_history").upsert({
                "id": hist_id,
                "aspirant_id": aspirant_id,
                "mentor_id": guide_id,
                "mentor_role": "guide",
                "assigned_by": admin_id,
                "action": "UNASSIGNED",
                "previous_mentor_id": None,
                "notes": f"Unassigned by Admin. Reason: {reason or 'Administrative rebalance'}",
                "created_at": now_iso
            }, on_conflict="id").execute()

            try:
                if new_primary_guide_id:
                    client.table("help_requests").update({
                        "assigned_guide_id": new_primary_guide_id,
                        "updated_at": now_iso
                    }).eq("aspirant_id", aspirant_id).eq("assigned_guide_id", guide_id).in_("status", list(ACTIVE_TICKET_STATUSES)).execute()
                else:
                    client.table("help_requests").update({
                        "assigned_guide_id": None,
                        "updated_at": now_iso
                    }).eq("aspirant_id", aspirant_id).eq("assigned_guide_id", guide_id).in_("status", list(ACTIVE_TICKET_STATUSES)).execute()
            except Exception as ex_hr:
                return False, f"Failed to transfer consultations during Guide unassignment: {ex_hr}"
        except Exception as e:
            return False, f"Failed to unassign Guide in Supabase: {e}"
    else:
        # SQLite mode
        conn = get_local_db()._get_conn()
        cur = conn.cursor()
        cur.execute("""
        UPDATE relationships
        SET guide_id = ?, guide_ids = ?, updated_at = ?
        WHERE aspirant_id = ?
        """, (new_primary_guide_id, json.dumps(new_guide_ids), now_iso, aspirant_id))
        conn.commit()

        try:
            if new_primary_guide_id:
                cur.execute("""
                UPDATE help_requests
                SET assigned_guide_id = ?, updated_at = ?
                WHERE aspirant_id = ? AND assigned_guide_id = ? AND status IN ('OPEN', 'IN_PROGRESS', 'WAITING_ON_ASPIRANT', 'WAITING_ON_GUIDE_SME')
                """, (new_primary_guide_id, now_iso, aspirant_id, guide_id))
            else:
                cur.execute("""
                UPDATE help_requests
                SET assigned_guide_id = NULL, updated_at = ?
                WHERE aspirant_id = ? AND assigned_guide_id = ? AND status IN ('OPEN', 'IN_PROGRESS', 'WAITING_ON_ASPIRANT', 'WAITING_ON_GUIDE_SME')
                """, (now_iso, aspirant_id, guide_id))
            conn.commit()
        except Exception:
            pass
        conn.close()

        get_local_db().record_assignment_history(
            aspirant_id=aspirant_id,
            mentor_id=guide_id,
            mentor_role="guide",
            assigned_by=admin_id,
            action="UNASSIGNED",
            previous_mentor_id=None,
            notes=f"Unassigned by Admin. Reason: {reason or 'Administrative rebalance'}"
        )

    invalidate_memo("all_relationships")
    invalidate_memo(f"mentors:{aspirant_id}")
    invalidate_memo(f"guide_aspirants:{guide_id}")
    if new_primary_guide_id:
        invalidate_memo(f"guide_aspirants:{new_primary_guide_id}")

    guide_prof = get_profile(guide_id)
    asp_prof = get_profile(aspirant_id)
    guide_name = guide_prof.get("full_name") if guide_prof else "Guide"
    asp_name = asp_prof.get("full_name") if asp_prof else "Entrepreneur"

    create_notification(
        user_id=guide_id,
        title="Caseload Unassigned",
        message=f"You have been unassigned as Guide for {asp_name}. Reason: {reason or 'Administrative rebalance'}.",
        notification_type="guide_unassigned",
        actor_id=admin_id
    )
    create_notification(
        user_id=aspirant_id,
        title="Mentorship Update",
        message=f"{guide_name} has concluded their dedicated mentorship role. Reason: {reason or 'Administrative rebalance'}.",
        notification_type="guide_unassigned",
        actor_id=admin_id
    )
    log_meaningful_event(
        aspirant_id=aspirant_id,
        actor_id=admin_id or "system",
        actor_role="admin",
        event_type="guide_unassigned",
        title="Guide Assignment Concluded",
        description=f"{guide_name} concluded their mentorship assignment. Reason: {reason or 'Administrative rebalance'}.",
        metadata={"guide_id": guide_id, "reason": reason}
    )

    return True, None

def unassign_sme(aspirant_id: str, sme_id: str, admin_id: Optional[str] = None, reason: str = "") -> Tuple[bool, Optional[str]]:
    """Admin unassigns a domain specialist (SME) from an Aspirant's advisory panel.
    Preserves historical technical advisory records, schemes, and journey events.
    Handles case handover and cache invalidation.
    Requires verified Sole Admin authorization.
    """
    from services.roles import require_sole_admin
    ok_admin, err_admin = require_sole_admin(actor_id=admin_id)
    if not ok_admin:
        return False, err_admin

    from services.profiles import get_profile
    from services.journey import log_meaningful_event
    from services.notifications import create_notification

    curr = get_aspirant_mentors(aspirant_id)
    smes = curr.get("smes", [])
    current_sme_ids = [s["id"] for s in smes]
    primary_sme_id = curr.get("sme", {}).get("id") if curr.get("sme") else None

    if sme_id not in current_sme_ids and sme_id != primary_sme_id:
        return False, "This SME is not currently assigned to this entrepreneur."

    new_sme_ids = [sid for sid in current_sme_ids if sid != sme_id]
    if primary_sme_id == sme_id:
        new_primary_sme_id = new_sme_ids[0] if new_sme_ids else None
    else:
        new_primary_sme_id = primary_sme_id

    now_iso = datetime.now(timezone.utc).isoformat()
    backend = get_data_backend()

    if backend == "supabase":
        client = _get_admin_client()
        if not client:
            return False, "Supabase client not available."
        try:
            client.table("relationships").update({
                "sme_id": new_primary_sme_id,
                "sme_ids": new_sme_ids,
                "updated_at": now_iso
            }).eq("aspirant_id", aspirant_id).execute()

            import uuid
            hist_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{aspirant_id}:{sme_id}:UNASSIGNED:{now_iso[:13]}"))
            client.table("assignment_history").upsert({
                "id": hist_id,
                "aspirant_id": aspirant_id,
                "mentor_id": sme_id,
                "mentor_role": "sme",
                "assigned_by": admin_id,
                "action": "UNASSIGNED",
                "previous_mentor_id": None,
                "notes": f"Specialist unassigned by Admin. Reason: {reason or 'Advisory concluded'}",
                "created_at": now_iso
            }, on_conflict="id").execute()

            try:
                if new_primary_sme_id:
                    client.table("help_requests").update({
                        "assigned_sme_id": new_primary_sme_id,
                        "updated_at": now_iso
                    }).eq("aspirant_id", aspirant_id).eq("assigned_sme_id", sme_id).in_("status", list(ACTIVE_TICKET_STATUSES)).execute()
                else:
                    client.table("help_requests").update({
                        "assigned_sme_id": None,
                        "updated_at": now_iso
                    }).eq("aspirant_id", aspirant_id).eq("assigned_sme_id", sme_id).in_("status", list(ACTIVE_TICKET_STATUSES)).execute()
            except Exception as ex_hr:
                return False, f"Failed to transfer consultations during SME unassignment: {ex_hr}"
        except Exception as e:
            return False, f"Failed to unassign SME in Supabase: {e}"
    else:
        # SQLite mode
        conn = get_local_db()._get_conn()
        cur = conn.cursor()
        cur.execute("""
        UPDATE relationships
        SET sme_id = ?, sme_ids = ?, updated_at = ?
        WHERE aspirant_id = ?
        """, (new_primary_sme_id, json.dumps(new_sme_ids), now_iso, aspirant_id))
        conn.commit()

        try:
            if new_primary_sme_id:
                cur.execute("""
                UPDATE help_requests
                SET assigned_sme_id = ?, updated_at = ?
                WHERE aspirant_id = ? AND assigned_sme_id = ? AND status IN ('OPEN', 'IN_PROGRESS', 'WAITING_ON_ASPIRANT', 'WAITING_ON_GUIDE_SME')
                """, (new_primary_sme_id, now_iso, aspirant_id, sme_id))
            else:
                cur.execute("""
                UPDATE help_requests
                SET assigned_sme_id = NULL, updated_at = ?
                WHERE aspirant_id = ? AND assigned_sme_id = ? AND status IN ('OPEN', 'IN_PROGRESS', 'WAITING_ON_ASPIRANT', 'WAITING_ON_GUIDE_SME')
                """, (now_iso, aspirant_id, sme_id))
            conn.commit()
        except Exception:
            pass
        conn.close()

        get_local_db().record_assignment_history(
            aspirant_id=aspirant_id,
            mentor_id=sme_id,
            mentor_role="sme",
            assigned_by=admin_id,
            action="UNASSIGNED",
            previous_mentor_id=None,
            notes=f"Specialist unassigned by Admin. Reason: {reason or 'Advisory concluded'}"
        )

    invalidate_memo("all_relationships")
    invalidate_memo(f"mentors:{aspirant_id}")
    invalidate_memo(f"sme_aspirants:{sme_id}")
    if new_primary_sme_id:
        invalidate_memo(f"sme_aspirants:{new_primary_sme_id}")

    sme_prof = get_profile(sme_id)
    asp_prof = get_profile(aspirant_id)
    sme_name = sme_prof.get("full_name") if sme_prof else "Specialist"
    asp_name = asp_prof.get("full_name") if asp_prof else "Entrepreneur"

    create_notification(
        user_id=sme_id,
        title="Advisory Case Unassigned",
        message=f"You have been unassigned as SME for {asp_name}. Reason: {reason or 'Advisory concluded'}.",
        notification_type="sme_unassigned",
        actor_id=admin_id
    )
    create_notification(
        user_id=aspirant_id,
        title="Advisory Team Update",
        message=f"{sme_name} has concluded their advisory term. Reason: {reason or 'Advisory concluded'}.",
        notification_type="sme_unassigned",
        actor_id=admin_id
    )
    log_meaningful_event(
        aspirant_id=aspirant_id,
        actor_id=admin_id or "system",
        actor_role="admin",
        event_type="sme_unassigned",
        title="Specialist Term Concluded",
        description=f"{sme_name} concluded their advisory assignment. Reason: {reason or 'Advisory concluded'}.",
        metadata={"sme_id": sme_id, "reason": reason}
    )

    return True, None

def get_assignment_history(aspirant_id: Optional[str] = None, mentor_id: Optional[str] = None) -> List[Dict]:
    """Admin audit log query for mentor reassignments and handovers."""
    backend = get_data_backend()
    if backend == "supabase":
        client = _get_admin_client() or _get_user_client()
        if client:
            try:
                query = client.table("assignment_history").select("*, aspirant:profiles!aspirant_id(full_name), mentor:profiles!mentor_id(full_name), previous_mentor:profiles!previous_mentor_id(full_name)")
                if aspirant_id:
                    query = query.eq("aspirant_id", aspirant_id)
                elif mentor_id:
                    query = query.or_(f"mentor_id.eq.{mentor_id},previous_mentor_id.eq.{mentor_id}")
                res = query.order("created_at", desc=True).execute()
                rows = []
                for r in (res.data or []):
                    d = dict(r)
                    d["aspirant_name"] = r.get("aspirant", {}).get("full_name") if isinstance(r.get("aspirant"), dict) else "Entrepreneur"
                    d["mentor_name"] = r.get("mentor", {}).get("full_name") if isinstance(r.get("mentor"), dict) else "Mentor"
                    d["previous_mentor_name"] = r.get("previous_mentor", {}).get("full_name") if isinstance(r.get("previous_mentor"), dict) else None
                    rows.append(d)
                return rows
            except Exception as e:
                print(f"[Relationships] Supabase assignment history error: {e}")
                return []
        return []

    return get_local_db().list_assignment_history(aspirant_id, mentor_id)

def get_assigned_aspirants_for_guide(guide_id: str) -> List[Dict]:
    """Retrieves all active caseload entrepreneurs for a Guide with memoization, single batch profile query, and server-side NDA gating."""
    if not guide_id:
        return []

    # Strict Server-Side Role and NDA Authorization Gate
    from services.roles import user_has_active_role
    if not user_has_active_role(guide_id, "guide"):
        return []

    from services.legal import check_user_nda_accepted
    if not check_user_nda_accepted(guide_id, "guide"):
        return []

    cached = get_memo(f"guide_aspirants:{guide_id}")
    if cached is not None:
        return cached

    backend = get_data_backend()
    from services.profiles import get_profiles_batch

    if backend == "supabase":
        client = _get_admin_client() or _get_user_client()
        if client:
            rows = []
            try:
                try:
                    res = client.table("relationships").select("aspirant_id, notes, status, created_at, guide_id, guide_ids").eq("status", "active").execute()
                except Exception:
                    res = client.table("relationships").select("aspirant_id, notes, status, created_at, guide_id").eq("status", "active").execute()

                rel_map = {}
                for r in (res.data or []):
                    g_ids = r.get("guide_ids") or []
                    if isinstance(g_ids, str):
                        try: g_ids = json.loads(g_ids)
                        except Exception: g_ids = []
                    is_active_guide = (r.get("guide_id") == guide_id) or (isinstance(g_ids, list) and guide_id in g_ids)
                    if is_active_guide and r.get("aspirant_id"):
                        rel_map[r["aspirant_id"]] = r

                if rel_map:
                    profiles_map = get_profiles_batch(list(rel_map.keys()))
                    for aid, r in rel_map.items():
                        p = profiles_map.get(aid)
                        if p:
                            p_copy = dict(p)
                            p_copy["assigned_at"] = r.get("created_at")
                            p_copy["assignment_notes"] = r.get("notes")
                            rows.append(p_copy)
                set_memo(f"guide_aspirants:{guide_id}", rows, ttl_seconds=60)
            except Exception as e:
                print(f"[Relationships] Supabase list aspirants for guide error: {e}")
            return rows
        return []

    rows = get_local_db().list_aspirants_for_guide(guide_id)
    set_memo(f"guide_aspirants:{guide_id}", rows, ttl_seconds=60)
    return rows

def get_assigned_aspirants_for_sme(sme_id: str) -> List[Dict]:
    """Retrieves all active Aspirants assigned to an SME with memoization, single batch profile query, and server-side NDA gating."""
    if not sme_id:
        return []

    # Strict Server-Side Role and NDA Authorization Gate
    from services.roles import user_has_active_role
    if not user_has_active_role(sme_id, "sme"):
        return []

    from services.legal import check_user_nda_accepted
    if not check_user_nda_accepted(sme_id, "sme"):
        return []

    cached = get_memo(f"sme_aspirants:{sme_id}")
    if cached is not None:
        return cached

    backend = get_data_backend()
    from services.profiles import get_profiles_batch

    if backend == "supabase":
        client = _get_admin_client() or _get_user_client()
        if client:
            rows = []
            try:
                try:
                    res = client.table("relationships").select("aspirant_id, notes, status, created_at, sme_id, sme_ids").eq("status", "active").execute()
                except Exception:
                    res = client.table("relationships").select("aspirant_id, notes, status, created_at, sme_id").eq("status", "active").execute()

                rel_map = {}
                for r in (res.data or []):
                    s_ids = r.get("sme_ids") or []
                    if isinstance(s_ids, str):
                        try: s_ids = json.loads(s_ids)
                        except Exception: s_ids = []
                    is_assigned = (r.get("sme_id") == sme_id) or (isinstance(s_ids, list) and sme_id in s_ids)
                    if is_assigned and r.get("aspirant_id"):
                        rel_map[r["aspirant_id"]] = r

                if rel_map:
                    profiles_map = get_profiles_batch(list(rel_map.keys()))
                    for aid, r in rel_map.items():
                        p = profiles_map.get(aid)
                        if p:
                            p_copy = dict(p)
                            p_copy["assigned_at"] = r.get("created_at")
                            p_copy["assignment_notes"] = r.get("notes")
                            rows.append(p_copy)
                set_memo(f"sme_aspirants:{sme_id}", rows, ttl_seconds=60)
            except Exception as e:
                print(f"[Relationships] Supabase list aspirants for sme error: {e}")
            return rows
        return []

    rows = get_local_db().list_aspirants_for_sme(sme_id)
    set_memo(f"sme_aspirants:{sme_id}", rows, ttl_seconds=60)
    return rows
