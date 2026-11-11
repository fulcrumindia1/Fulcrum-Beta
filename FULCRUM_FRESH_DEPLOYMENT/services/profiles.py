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

import json
from datetime import datetime, timezone
from typing import Optional, Dict, List, Tuple, Set
from services.auth import get_supabase_client, get_supabase_admin_client, get_data_backend
from services.local_db import get_local_db
from services.cache import get_memo, set_memo, invalidate_memo


def _get_relationship_authorized_ids_supabase(admin_cli, actor_id: str) -> Set[str]:
    """Returns peer/mentee/mentor user IDs connected to actor_id via active relationships (including guide_ids/sme_ids arrays)."""
    authorized_ids: Set[str] = set()
    if not admin_cli or not actor_id:
        return authorized_ids
    actor_str = str(actor_id)
    rel_filter = (
        f"aspirant_id.eq.{actor_str},guide_id.eq.{actor_str},sme_id.eq.{actor_str},"
        f"guide_ids.cs.{{{actor_str}}},sme_ids.cs.{{{actor_str}}}"
    )
    rows: List[Dict] = []
    try:
        rel_res = (
            admin_cli.table("relationships")
            .select("aspirant_id, guide_id, guide_ids, sme_id, sme_ids")
            .eq("status", "active")
            .or_(rel_filter)
            .execute()
        )
        rows = rel_res.data or []
    except Exception:
        try:
            rel_res = (
                admin_cli.table("relationships")
                .select("aspirant_id, guide_id, guide_ids, sme_id, sme_ids")
                .eq("status", "active")
                .execute()
            )
            rows = rel_res.data or []
        except Exception as ex_rel:
            print(f"[Profiles] Relationship check notice: {ex_rel}")
            rows = []

    for r in rows:
        r_asp = str(r.get("aspirant_id") or "")
        raw_g = r.get("guide_ids") or []
        if isinstance(raw_g, str):
            try:
                raw_g = json.loads(raw_g)
            except Exception:
                raw_g = []
        r_gids = [str(gid) for gid in raw_g if gid]
        if r.get("guide_id") and str(r["guide_id"]) not in r_gids:
            r_gids.append(str(r["guide_id"]))

        raw_s = r.get("sme_ids") or []
        if isinstance(raw_s, str):
            try:
                raw_s = json.loads(raw_s)
            except Exception:
                raw_s = []
        r_sids = [str(sid) for sid in raw_s if sid]
        if r.get("sme_id") and str(r["sme_id"]) not in r_sids:
            r_sids.append(str(r["sme_id"]))

        if actor_str == r_asp:
            authorized_ids.update(r_gids + r_sids)
        elif actor_str in r_gids or actor_str in r_sids:
            if r_asp:
                authorized_ids.add(r_asp)
            # Co-mentors on the same active caseload can inspect sibling team profiles (Guide/Co-Guide/SME)
            authorized_ids.update(r_gids + r_sids)
    return authorized_ids

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

def get_profile(
    user_id: str,
    requesting_actor_id: Optional[str] = None,
    is_system: bool = False
) -> Optional[Dict]:
    """
    Fetches user profile by ID using active backend with actor-scoped authorization & memoization.

    SECURITY GUARANTEES:
    1. Verified Actor Authorization: Ordinary users can only access their own profile or
       assigned mentors/mentees with verified active pairwise relationships.
    2. Zero Implicit Privilege: A missing actor identity is NOT implicitly trusted as system.
    3. Least-Privilege Projection: Non-admin viewers receive sanitized profiles (admin notes,
       temporary credentials, and deletion metadata stripped).
    4. No Cross-Backend Leakage: In Supabase mode, failed or denied cloud reads NEVER silently
       fall back to local SQLite.
    5. Actor-Partitioned Cache: Cache keys are partitioned by actor scope to eliminate cross-user leakage.
    """
    if not user_id:
        return None

    # Resolve requesting actor identity
    actor_id = requesting_actor_id
    if not actor_id:
        try:
            import streamlit as st
            actor_id = st.session_state.get("user_id") or (st.session_state.get("user") or {}).get("id")
        except Exception:
            actor_id = None

    actor_scope = str(actor_id or ("system" if is_system else "anonymous"))
    cache_key = f"profile:{user_id}:{actor_scope}"

    # Check request memo cache first
    cached = get_memo(cache_key)
    if cached is not None:
        return cached

    backend = get_data_backend()

    if backend == "supabase":
        from services.roles import is_strict_admin
        from services.account_lifecycle import get_account_status

        is_admin = is_system or (actor_id and is_strict_admin(user_id=actor_id))
        is_self = bool(actor_id and str(actor_id) == str(user_id))

        authorized = False
        if is_admin or is_self:
            authorized = True
        elif actor_id is not None:
            # Verify actor account status is active
            st_info = get_account_status(actor_id)
            if st_info.get("account_status") == "ACTIVE" and st_info.get("is_active", True):
                admin_cli = _get_admin_client()
                if str(user_id) in _get_relationship_authorized_ids_supabase(admin_cli, str(actor_id)):
                    authorized = True

        if not authorized:
            # Denied: Actor does not have verified permission to inspect this profile
            return None

        p = None
        if is_self:
            client = _get_user_client()
            if client:
                try:
                    res = client.table("profiles").select("*").eq("id", user_id).execute()
                    if res.data and len(res.data) > 0:
                        p = res.data[0]
                except Exception:
                    pass

        if not p:
            admin = _get_admin_client()
            if admin:
                try:
                    res = admin.table("profiles").select("*").eq("id", user_id).execute()
                    if res.data and len(res.data) > 0:
                        p = res.data[0]
                except Exception:
                    pass

        if not p:
            # Record not found in Supabase — STRICT: No silent SQLite fallback in Supabase mode!
            return None

        p_clean = dict(p)
        if not is_admin and not is_self:
            p_clean.pop("admin_notes", None)
            p_clean.pop("temp_password_issued", None)
            p_clean.pop("deletion_requested_by", None)
            p_clean.pop("retention_notes", None)

        p_clean["completion_pct"] = calculate_completion(p_clean)
        set_memo(cache_key, p_clean, ttl_seconds=60)
        return p_clean

    # SQLite mode ONLY (when DATA_BACKEND=sqlite)
    p = get_local_db().get_profile_by_id(user_id)
    if p:
        p_clean = dict(p)
        p_clean["completion_pct"] = calculate_completion(p_clean)
        set_memo(cache_key, p_clean, ttl_seconds=60)
        return p_clean
    return None

def get_profile_by_email(
    email: str,
    requesting_actor_id: Optional[str] = None,
    is_system: bool = False
) -> Optional[Dict]:
    """
    Fetches user profile by email using active backend.
    """
    if not email or not str(email).strip():
        return None
    clean_email = str(email).strip().lower()

    backend = get_data_backend()
    if backend == "supabase":
        admin = _get_admin_client()
        if admin:
            try:
                res = admin.table("profiles").select("*").ilike("email", clean_email).limit(1).execute()
                if res.data and len(res.data) > 0:
                    p = dict(res.data[0])
                    if isinstance(p.get("profile_data"), str):
                        try:
                            p["profile_data"] = json.loads(p["profile_data"])
                        except Exception:
                            p["profile_data"] = {}
                    p["completion_pct"] = calculate_completion(p)
                    return p
            except Exception as e:
                print(f"[Profiles] get_profile_by_email cloud error: {e}")
        return None

    # SQLite mode ONLY
    try:
        ldb = get_local_db()
        conn = ldb._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM profiles WHERE LOWER(email) = ?", (clean_email,))
        row = cur.fetchone()
        conn.close()
        if row:
            p = dict(row)
            if isinstance(p.get("profile_data"), str):
                try:
                    p["profile_data"] = json.loads(p["profile_data"])
                except Exception:
                    p["profile_data"] = {}
            p["completion_pct"] = calculate_completion(p)
            return p
    except Exception as e:
        print(f"[Profiles] get_profile_by_email local error: {e}")
    return None


def get_profiles_batch(
    user_ids: List[str],
    requesting_actor_id: Optional[str] = None,
    is_system: bool = False
) -> Dict[str, Dict]:
    """
    Batched profile retrieval with least-privilege actor-scoped authorization.
    Retrieves multiple profiles in a single query and caches them in session memo.

    SECURITY INVARIANTS:
    1. Admin can retrieve profiles required for roster governance.
    2. Assigned Guides & SMEs can retrieve authorized mentee information.
    3. Entrepreneurs can retrieve their assigned mentors' profiles.
    4. Ordinary Aspirants CANNOT batch-fetch unrelated users' protected profiles.
    5. Unassigned mentors CANNOT retrieve unrelated Aspirants through privileged fallback.
    6. Revoked mentors CANNOT retrieve former Aspirants.
    7. Suspended or archived actors are strictly DENIED privileged fallback access.
    8. Cache entries are partitioned per-actor to prevent privilege escalation leakage.
    9. An RLS-denied read is NEVER universally overridden with service-role access without verified relationship.
    10. Non-admin batch results contain only public & relationship-authorized attributes.
    """
    if not user_ids:
        return {}

    unique_ids = list(set(filter(None, user_ids)))
    result: Dict[str, Dict] = {}
    missing_ids: List[str] = []

    # Infer actor from argument or active Streamlit session
    actor_id = requesting_actor_id
    if not actor_id:
        try:
            import streamlit as st
            actor_id = st.session_state.get("user_id") or (st.session_state.get("user") or {}).get("id")
        except Exception:
            actor_id = None

    actor_scope = str(actor_id or ("system" if is_system else "anonymous"))

    # Check actor-scoped memo cache first (Prevents admin-level cache leakage to ordinary users)
    for uid in unique_ids:
        cached = get_memo(f"profile:{uid}:{actor_scope}")
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
                    p_clean = dict(p)
                    p_clean["completion_pct"] = calculate_completion(p_clean)
                    set_memo(f"profile:{p_clean['id']}:{actor_scope}", p_clean, ttl_seconds=60)
                    result[p_clean["id"]] = p_clean
            except Exception:
                pass

        still_to_fetch = [uid for uid in missing_ids if uid not in result]
        if still_to_fetch:
            admin = _get_admin_client()
            if admin:
                # Determine privileged access authorization for still_to_fetch
                from services.roles import is_strict_admin
                from services.account_lifecycle import get_account_status

                is_admin = is_system or (actor_id and is_strict_admin(user_id=actor_id))
                authorized_ids = set()

                if is_admin:
                    # Admin or explicit system background capability -> Authorized for requested IDs
                    authorized_ids = set(still_to_fetch)
                elif actor_id is not None:
                    # Non-admin user: verify account status is ACTIVE
                    st_info = get_account_status(actor_id)
                    if st_info.get("account_status") == "ACTIVE" and st_info.get("is_active", True):
                        authorized_ids = _get_relationship_authorized_ids_supabase(admin, str(actor_id))
                else:
                    # Missing actor identity without system capability -> Deny all
                    authorized_ids = set()

                # Fetch ONLY the explicitly authorized subset via admin client
                fetch_targets = [uid for uid in still_to_fetch if uid in authorized_ids]
                if fetch_targets:
                    try:
                        res_admin = admin.table("profiles").select("*").in_("id", fetch_targets).execute()
                        for p in (res_admin.data or []):
                            p_clean = dict(p)
                            # Least-privilege projection for non-admins
                            if not is_admin and actor_id is not None:
                                p_clean.pop("admin_notes", None)
                                p_clean.pop("temp_password_issued", None)
                                p_clean.pop("deletion_requested_by", None)
                                p_clean.pop("retention_notes", None)
                            p_clean["completion_pct"] = calculate_completion(p_clean)
                            set_memo(f"profile:{p_clean['id']}:{actor_scope}", p_clean, ttl_seconds=60)
                            result[p_clean["id"]] = p_clean
                    except Exception as ex_adm:
                        print(f"[Profiles] Privileged fallback error: {ex_adm}")

        # Removed SQLite fallback in Supabase mode completely!
        return result

    # SQLite mode
    db = get_local_db()
    for uid in missing_ids:
        p = db.get_profile_by_id(uid)
        if p:
            p["completion_pct"] = calculate_completion(p)
            set_memo(f"profile:{uid}:{actor_scope}", p, ttl_seconds=60)
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

def list_profiles_by_role(role: str, requesting_actor_id: Optional[str] = None, **kwargs) -> List[Dict]:
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

                # For professional roles (guide, sme), user_roles is the verified source of truth!
                # Strictly exclude any user whose role is not active in user_roles
                # (e.g. revoked, suspended, pending NDA, or missing active grant).
                if role in ("guide", "sme"):
                    profile_rows = [p for p in profile_rows if p["id"] in role_uids]

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
            session_role = st.session_state.get("active_workspace") or st.session_state.get("role")
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
    if isinstance(existing_pdata, str):
        try:
            existing_pdata = json.loads(existing_pdata)
        except Exception:
            existing_pdata = {}
    if not isinstance(existing_pdata, dict):
        existing_pdata = {}

    profile_data = dict(existing_pdata)
    profile_data.update({
        "personal": personal_data or {},
        "professional": professional_data or {},
        "business": business_data or {},
        "demographics": demographics_data or {},
        "assistance_need": assistance_need_data if assistance_need_data is not None else existing_pdata.get("assistance_need", {})
    })

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
    invalidate_memo(f"profile:{user_id}")
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
    invalidate_memo(f"profile:{user_id}")
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
    invalidate_memo(f"profile:{user_id}")
    invalidate_memo("all_profiles")
    invalidate_memo("list_profiles_by_role:")
    invalidate_memo("active_profiles_for_role:")
    invalidate_memo("multi_role_users")
    return merged, None


def list_users_with_multi_roles() -> List[Dict]:
    """Compatibility wrapper re-exporting list_users_with_multi_roles from services.roles."""
    from services.roles import list_users_with_multi_roles as _list_roles
    return _list_roles()



