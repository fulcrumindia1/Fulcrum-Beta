"""
services/profiles.py — Profile Service for FULCRUM-INDIA (Cluster A)
====================================================================
Manages Naukri/LinkedIn-style profile with 4 sections:
1. PERSONAL (Name, Email, Phone, Gender, DOB, Address, District, State)
2. PROFESSIONAL (Education, Skills, Experience, Certifications, Expertise)
3. BUSINESS (Name, Type, Sector, Stage, Description, Founded Date, Revenue, Team, Location)
4. DEMOGRAPHICS (District, State, Category, Special eligibility)

Automation:
- Saving an important business profile update recalculates scheme matches
- Records a meaningful Journey event
"""

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

def calculate_completion(p: Dict) -> int:
    """Calculates profile completion percentage (0-100%)."""
    data = p.get("profile_data", {})
    if isinstance(data, str):
        try:
            import json
            data = json.loads(data)
        except Exception:
            data = {}

    personal = data.get("personal", {})
    prof = data.get("professional", {})
    biz = data.get("business", {})
    demo = data.get("demographics", {})

    points = 0
    total = 10

    # 1. Personal (2 pts)
    if p.get("full_name") and p.get("phone"): points += 1
    if personal.get("address") or p.get("district"): points += 1

    # 2. Professional (2 pts)
    if prof.get("education") or prof.get("skills"): points += 1
    if prof.get("experience") or prof.get("experience_years") or prof.get("expertise"): points += 1

    # 3. Business (4 pts)
    if biz.get("business_name"): points += 1
    if biz.get("sector"): points += 1
    if biz.get("stage"): points += 1
    if biz.get("description") or biz.get("revenue") or biz.get("brief"): points += 1

    # 4. Demographics (2 pts)
    if demo.get("category") or demo.get("founder_category") or demo.get("social_category"): points += 1
    if p.get("district") and p.get("state"): points += 1

    return int((points / total) * 100)

def get_profile(user_id: str) -> Optional[Dict]:
    """Fetches user profile by ID using active backend with request-scoped memoization."""
    if not user_id:
        return None

    # Check request memo cache first
    cached = get_memo(f"profile:{user_id}")
    if cached is not None:
        return cached

    backend = get_data_backend()

    if backend == "supabase":
        client = _get_user_client()
        if client:
            try:
                res = client.table("profiles").select("*").eq("id", user_id).execute()
                if res.data and len(res.data) > 0:
                    p = res.data[0]
                    p["completion_pct"] = calculate_completion(p)
                    set_memo(f"profile:{user_id}", p, ttl_seconds=60)
                    return p
            except Exception as e:
                pass
        
        # Admin client fallback for service lookups & background tasks
        admin = _get_admin_client()
        if admin:
            try:
                res = admin.table("profiles").select("*").eq("id", user_id).execute()
                if res.data and len(res.data) > 0:
                    p = res.data[0]
                    p["completion_pct"] = calculate_completion(p)
                    set_memo(f"profile:{user_id}", p, ttl_seconds=60)
                    return p
            except Exception as e:
                pass
        # Fallback to local DB if record not found in cloud table
        p_loc = get_local_db().get_profile_by_id(user_id)
        if p_loc:
            p_loc["completion_pct"] = calculate_completion(p_loc)
            set_memo(f"profile:{user_id}", p_loc, ttl_seconds=60)
            return p_loc
        return None

    # SQLite mode ONLY (when DATA_BACKEND=sqlite)
    p = get_local_db().get_profile_by_id(user_id)
    if p:
        p["completion_pct"] = calculate_completion(p)
        set_memo(f"profile:{user_id}", p, ttl_seconds=60)
        return p
    return None

def get_profiles_batch(user_ids: List[str]) -> Dict[str, Dict]:
    """
    Batched profile retrieval to completely eliminate N+1 queries.
    Retrieves multiple profiles in a single query and caches them in session memo.
    """
    if not user_ids:
        return {}

    unique_ids = list(set(filter(None, user_ids)))
    result: Dict[str, Dict] = {}
    missing_ids: List[str] = []

    # Check cache first
    for uid in unique_ids:
        cached = get_memo(f"profile:{uid}")
        if cached is not None:
            result[uid] = cached
        else:
            missing_ids.append(uid)

    if not missing_ids:
        return result

    backend = get_data_backend()

    if backend == "supabase":
        client = _get_user_client()
        if client:
            try:
                res = client.table("profiles").select("*").in_("id", missing_ids).execute()
                for p in (res.data or []):
                    p["completion_pct"] = calculate_completion(p)
                    set_memo(f"profile:{p['id']}", p, ttl_seconds=60)
                    result[p["id"]] = p
            except Exception:
                pass

        # Query admin client for any remaining missing profiles (bypasses RLS for mentor panels & background tasks)
        still_to_fetch = [uid for uid in missing_ids if uid not in result]
        if still_to_fetch:
            admin = _get_admin_client()
            if admin:
                try:
                    res_admin = admin.table("profiles").select("*").in_("id", still_to_fetch).execute()
                    for p in (res_admin.data or []):
                        p["completion_pct"] = calculate_completion(p)
                        set_memo(f"profile:{p['id']}", p, ttl_seconds=60)
                        result[p["id"]] = p
                except Exception:
                    pass
        still_missing = [uid for uid in missing_ids if uid not in result]
        if still_missing:
            db = get_local_db()
            for uid in still_missing:
                p = db.get_profile_by_id(uid)
                if p:
                    p["completion_pct"] = calculate_completion(p)
                    set_memo(f"profile:{uid}", p, ttl_seconds=60)
                    result[uid] = p
        return result

    # SQLite mode
    db = get_local_db()
    for uid in missing_ids:
        p = db.get_profile_by_id(uid)
        if p:
            p["completion_pct"] = calculate_completion(p)
            set_memo(f"profile:{uid}", p, ttl_seconds=60)
            result[uid] = p
    return result

def list_all_profiles() -> List[Dict]:
    """Lists all active profiles in a single query and populates per-profile cache."""
    cached = get_memo("all_profiles")
    if cached is not None:
        return cached

    backend = get_data_backend()
    if backend == "supabase":
        client = _get_admin_client() or _get_user_client()
        if client:
            try:
                res = client.table("profiles").select("*").neq("is_active", False).order("created_at", desc=True).execute()
                rows = res.data or []
                for r in rows:
                    r["completion_pct"] = calculate_completion(r)
                    if r.get("id"):
                        set_memo(f"profile:{r['id']}", r, ttl_seconds=60)
                set_memo("all_profiles", rows, ttl_seconds=60)
                return rows
            except Exception as e:
                print(f"[Profiles] list_all_profiles error: {e}")
                return []
        return []

    rows = get_local_db().list_all_profiles()
    for r in rows:
        r["completion_pct"] = calculate_completion(r)
        if r.get("id"):
            set_memo(f"profile:{r['id']}", r, ttl_seconds=60)
    set_memo("all_profiles", rows, ttl_seconds=60)
    return rows

def list_profiles_by_role(role: str) -> List[Dict]:
    """Lists profiles holding a specific role from active backend.
    In Multi-Role architecture, a user holds a role if:
      1. profiles.role == role, OR
      2. user_roles contains an active grant with user_roles.role == role AND status == 'active'.
      3. For 'aspirant', any user who has an enterprise roadmap in journeys (excluding admins).
    Users are deduplicated by ID so each distinct user is returned exactly once.
    """
    cache_key = f"list_profiles_by_role:{role}"
    cached = get_memo(cache_key)
    if cached is not None:
        return cached

    backend = get_data_backend()

    if backend == "supabase":
        client = _get_admin_client() or _get_user_client()
        if client:
            try:
                role_uids = set()
                # 1. Fetch user_ids holding this role with status 'active' in user_roles
                try:
                    ur_res = client.table("user_roles").select("user_id").eq("role", role).eq("status", "active").execute()
                    if ur_res.data:
                        for row in ur_res.data:
                            if row.get("user_id"):
                                role_uids.add(row["user_id"])
                except Exception:
                    pass

                # If querying aspirants, also include any user with a recorded venture journey
                if role == "aspirant":
                    try:
                        j_res = client.table("journeys").select("aspirant_id").execute()
                        if j_res.data:
                            for row in j_res.data:
                                if row.get("aspirant_id"):
                                    role_uids.add(row["aspirant_id"])
                    except Exception:
                        pass

                # 2. Fetch profiles where primary role is this role (excluding explicitly inactive)
                res1 = client.table("profiles").select("*").eq("role", role).neq("is_active", False).execute()
                profile_rows = res1.data or []
                found_ids = {p["id"] for p in profile_rows}

                # 3. Fetch missing profiles where user holds this role via user_roles grant or journey
                missing_ids = [uid for uid in role_uids if uid not in found_ids]
                if missing_ids:
                    res2 = client.table("profiles").select("*").in_("id", missing_ids).neq("is_active", False).execute()
                    if res2.data:
                        profile_rows.extend(res2.data)

                # Strictly protect: never include designated administrators in aspirants list
                if role == "aspirant":
                    profile_rows = [p for p in profile_rows if p.get("role") != "admin"]

                # Exclude accounts that are temporarily suspended, archived, or pending deletion
                profile_rows = [
                    p for p in profile_rows
                    if str(p.get("account_status") or "ACTIVE").upper() == "ACTIVE"
                    and p.get("is_active", True)
                ]

                # Sort by created_at desc
                profile_rows.sort(key=lambda r: str(r.get("created_at") or ""), reverse=True)
                for r in profile_rows:
                    r["completion_pct"] = calculate_completion(r)
                    if r.get("id"):
                        set_memo(f"profile:{r['id']}", r, ttl_seconds=60)
                set_memo(cache_key, profile_rows, ttl_seconds=60)
                return profile_rows
            except Exception as e:
                print(f"[Profiles] list_profiles_by_role error: {e}")
                return []
        return []

    # SQLite mode ONLY (when DATA_BACKEND=sqlite)
    rows = get_local_db().list_profiles_by_role(role)
    rows = [
        r for r in rows
        if str(r.get("account_status") or "ACTIVE").upper() == "ACTIVE"
        and r.get("is_active", 1) in (1, True)
    ]
    for r in rows:
        r["completion_pct"] = calculate_completion(r)
        if r.get("id"):
            set_memo(f"profile:{r['id']}", r, ttl_seconds=60)
    set_memo(cache_key, rows, ttl_seconds=60)
    return rows

def update_aspirant_profile(
    user_id: str,
    full_name: Optional[str] = None,
    phone: Optional[str] = None,
    district: Optional[str] = None,
    state: Optional[str] = None,
    personal_data: Optional[Dict] = None,
    professional_data: Optional[Dict] = None,
    business_data: Optional[Dict] = None,
    demographics_data: Optional[Dict] = None,
    actor_id: Optional[str] = None,
    assistance_need_data: Optional[Dict] = None
) -> Tuple[Optional[Dict], Optional[str]]:
    """
    Updates Aspirant profile across the core sections and strategic assistance requirements.
    Supports either individual fields or a combined dictionary passed as second argument.
    Triggers automated scheme match recalculation & Journey event logging.
    """
    # PART 7 — AUTHORIZATION: Verify authenticated caller is the owner or admin
    if actor_id:
        actor_prof = get_profile(actor_id)
        actor_role = actor_prof.get("role") if actor_prof else None
        if actor_role != "admin" and str(actor_id) != str(user_id):
            return None, "Unauthorized: You do not have permission to modify another user's profile."
    else:
        try:
            import streamlit as st
            session_user = st.session_state.get("user")
            session_user_id = st.session_state.get("user_id")
            session_role = st.session_state.get("role")
            if session_user and session_role != "admin" and str(session_user_id) != str(user_id):
                return None, "Unauthorized: You do not have permission to modify another user's profile."
        except Exception:
            pass

    current = get_profile(user_id)
    if not current:
        return None, "User profile not found."

    # If full_name was passed as a dict of sections (e.g. in test script or API)
    if isinstance(full_name, dict):
        d = full_name
        personal_data = d.get("personal", {})
        professional_data = d.get("professional", {})
        business_data = d.get("business", {})
        demographics_data = d.get("demographics", {})
        if "assistance_need" in d:
            assistance_need_data = d.get("assistance_need")
        full_name = personal_data.get("full_name") or current.get("full_name", "")
        phone = personal_data.get("phone") or current.get("phone", "")
        district = demographics_data.get("district") or personal_data.get("district") or current.get("district", "Tamil Nadu")
        state = demographics_data.get("state") or personal_data.get("state") or current.get("state", "Tamil Nadu")

    full_name = (full_name or current.get("full_name", "")).strip()
    phone = (phone or current.get("phone", "")).strip()
    district = (district or current.get("district", "")).strip()
    state = (state or current.get("state", "Tamil Nadu")).strip()

    existing_pdata = current.get("profile_data") or {}
    if not isinstance(existing_pdata, dict):
        existing_pdata = {}

    profile_data = {
        "personal": personal_data or {},
        "professional": professional_data or {},
        "business": business_data or {},
        "demographics": demographics_data or {},
        "assistance_need": assistance_need_data if assistance_need_data is not None else existing_pdata.get("assistance_need", {})
    }

    updated_record = {
        "id": user_id,
        "email": current["email"],
        "role": current.get("role", "aspirant"),
        "full_name": full_name.strip(),
        "phone": phone.strip(),
        "district": district.strip(),
        "state": state.strip(),
        "profile_data": profile_data,
        "is_active": True,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }

    backend = get_data_backend()

    if backend == "supabase":
        client = _get_user_client() or _get_admin_client()
        if not client:
            return None, "Supabase client not available."
        try:
            admin = _get_admin_client() or client
            res = admin.table("profiles").update(updated_record).eq("id", user_id).execute()
            admin_c = _get_admin_client() or client
            if admin_c:
                admin_c.table("journeys").update({
                    "title": f"{business_data.get('business_name') or full_name}'s Journey",
                    "business_type": business_data.get("sector") or business_data.get("business_type") or "Entrepreneurship",
                    "stage": business_data.get("stage", "idea"),
                    "updated_at": datetime.now(timezone.utc).isoformat()
                }).eq("aspirant_id", user_id).execute()
        except Exception as e:
            return None, f"Failed to update profile in Supabase: {e}"
    else:
        # SQLite mode ONLY (when DATA_BACKEND=sqlite)
        local_db = get_local_db()
        local_db.upsert_profile(updated_record)
        j = local_db.get_journey(user_id)
        if j:
            conn = local_db._get_conn()
            cur = conn.cursor()
            cur.execute("""
            UPDATE journeys
            SET title = ?, business_type = ?, stage = ?, updated_at = ?
            WHERE aspirant_id = ?
            """, (
                f"{business_data.get('business_name') or full_name}'s Journey",
                business_data.get("sector") or business_data.get("business_type") or "Entrepreneurship",
                business_data.get("stage", "idea"),
                datetime.now(timezone.utc).isoformat(),
                user_id
            ))
            conn.commit()
            conn.close()

    # Automate Meaningful Journey Event
    from services.journey import log_meaningful_event
    sector_name = business_data.get("sector") or "General"
    biz_name = business_data.get("business_name") or "Enterprise"
    log_meaningful_event(
        aspirant_id=user_id,
        actor_id=user_id,
        actor_role="aspirant",
        event_type="profile_updated",
        title="Business Profile Updated",
        description=f"Updated venture details for '{biz_name}' ({sector_name}, {business_data.get('stage', 'early stage')}).",
        metadata={"sector": sector_name, "stage": business_data.get("stage"), "district": district}
    )

    updated_record["completion_pct"] = calculate_completion(updated_record)
    set_memo(f"profile:{user_id}", updated_record, ttl_seconds=60)
    invalidate_memo("all_profiles")
    invalidate_memo("list_profiles_by_role:")
    invalidate_memo("active_profiles_for_role:")
    invalidate_memo("multi_role_users")
    invalidate_memo(f"scheme_matches_ai:{user_id}")
    return updated_record, None

def update_mentor_profile(
    user_id: str,
    full_name: str,
    phone: str,
    district: str,
    expertise: str,
    bio: str,
    industry: Optional[str] = None,
    role: Optional[str] = None
) -> Tuple[Optional[Dict], Optional[str]]:
    """
    Allows Guides and SMEs to update their own contact details and professional background.
    """
    current = get_profile(user_id)
    if not current:
        return None, "Profile not found."

    cur_data = current.get("profile_data", {})
    if isinstance(cur_data, str):
        import json
        try:
            cur_data = json.loads(cur_data)
        except Exception:
            cur_data = {}

    cur_data["expertise"] = expertise.strip() if expertise else ""
    cur_data["bio"] = bio.strip() if bio else ""
    if industry is not None:
        cur_data["industry"] = industry.strip()

    updated_record = {
        "id": user_id,
        "email": current["email"],
        "role": current.get("role", "guide"),
        "full_name": full_name.strip() if full_name else current.get("full_name", ""),
        "phone": phone.strip() if phone else current.get("phone", ""),
        "district": district.strip() if district else current.get("district", "Tamil Nadu"),
        "state": current.get("state", "Tamil Nadu"),
        "profile_data": cur_data,
        "is_active": True,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }

    backend = get_data_backend()
    if backend == "supabase":
        client = _get_user_client() or _get_admin_client()
        if not client:
            return None, "Supabase client not available."
        try:
            res = client.table("profiles").update(updated_record).eq("id", user_id).execute()
            if not res.data:
                admin = _get_admin_client()
                if admin and admin != client:
                    admin.table("profiles").update(updated_record).eq("id", user_id).execute()
        except Exception as e:
            return None, f"Failed to update profile in Supabase: {e}"
    else:
        # SQLite mode ONLY (when DATA_BACKEND=sqlite)
        get_local_db().upsert_profile(updated_record)

    try:
        import streamlit as st
        if "user" in st.session_state and st.session_state.get("user_id") == user_id:
            st.session_state.user = updated_record
    except Exception:
        pass

    updated_record["completion_pct"] = calculate_completion(updated_record)
    set_memo(f"profile:{user_id}", updated_record, ttl_seconds=60)
    invalidate_memo("all_profiles")
    invalidate_memo("list_profiles_by_role:")
    invalidate_memo("active_profiles_for_role:")
    invalidate_memo("multi_role_users")
    return updated_record, None

def update_profile(user_id: str, updates: Dict) -> Tuple[Optional[Dict], Optional[str]]:
    """Generic profile update utility for system routines (e.g. password change flag, metadata)."""
    current = get_profile(user_id)
    if not current:
        return None, "Profile not found."

    merged = dict(current)
    for k, v in updates.items():
        if k == "profile_data" and isinstance(v, dict) and isinstance(merged.get("profile_data"), dict):
            merged_pd = dict(merged["profile_data"])
            merged_pd.update(v)
            merged["profile_data"] = merged_pd
        else:
            merged[k] = v

    merged["updated_at"] = datetime.now(timezone.utc).isoformat()
    backend = get_data_backend()
    if backend == "supabase":
        client = _get_admin_client() or _get_user_client()
        if client:
            try:
                valid_cols = {"id", "email", "role", "full_name", "phone", "district", "state", "profile_data", "is_active", "updated_at"}
                db_payload = {k: v for k, v in merged.items() if k in valid_cols}
                client.table("profiles").update(db_payload).eq("id", user_id).execute()
            except Exception as e:
                return None, f"Supabase update error: {e}"
    else:
        # SQLite mode ONLY (when DATA_BACKEND=sqlite)
        get_local_db().upsert_profile(merged)

    merged["completion_pct"] = calculate_completion(merged)
    set_memo(f"profile:{user_id}", merged, ttl_seconds=60)
    invalidate_memo("all_profiles")
    invalidate_memo("list_profiles_by_role:")
    invalidate_memo("active_profiles_for_role:")
    invalidate_memo("multi_role_users")
    return merged, None


def list_users_with_multi_roles() -> List[Dict]:
    """Compatibility wrapper re-exporting list_users_with_multi_roles from services.roles."""
    from services.roles import list_users_with_multi_roles as _list_roles
    return _list_roles()



