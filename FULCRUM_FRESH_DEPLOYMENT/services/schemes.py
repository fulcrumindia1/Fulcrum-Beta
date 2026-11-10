"""
services/schemes.py — Scheme Intelligence & Matching Engine for FULCRUM-INDIA
=============================================================================
Manages the 170-scheme catalogue with Admin CRUD and executes a
deterministic, explainable matching engine against founder profiles.

Rules:
- Terminology: "Recommended", "Matched", "Potentially Eligible"
- NEVER use: "Approved", "Guaranteed", "Granted"
- Generates transparent "WHY THIS MATCHED" checklists.
Supports dual backends: Supabase (primary) and SQLite (explicit local development).
"""

import json
from datetime import datetime, timezone
from typing import Any, Optional, Dict, List, Tuple
from services.auth import get_supabase_client, get_supabase_admin_client, get_data_backend
from services.local_db import get_local_db
from services.cache import (
    get_global_cache, set_global_cache, invalidate_global_cache,
    get_memo, set_memo, invalidate_memo
)

def _get_user_client():
    """Returns the authenticated user's Supabase client (RLS-enforced)."""
    return get_supabase_client()

def _get_admin_client():
    """Returns the privileged admin Supabase client (bypasses RLS). Use sparingly."""
    return get_supabase_admin_client()

def list_schemes(
    search: str = "",
    category: str = "ALL",
    stage: str = "ALL",
    sector: str = "ALL",
    active_only: bool = True
) -> List[Dict]:
    """Retrieves schemes from the active backend."""
    backend = get_data_backend()

    # Fast in-memory cache check for active or all schemes
    cache_key = "schemes:all_active" if active_only else "schemes:all"
    cached_schemes = get_global_cache(cache_key)
    if cached_schemes is not None:
        schemes_data = cached_schemes
    elif backend == "supabase":
        client = _get_user_client()
        admin = _get_admin_client()
        reader = client if (client and hasattr(client, "auth") and client.auth.get_session()) else admin
        if not reader:
            reader = client or admin
        if reader:
            try:
                q = reader.table("schemes").select("*")
                if active_only:
                    q = q.eq("is_active", True)
                try:
                    res = q.order("display_order", desc=False).order("name", desc=False).execute()
                except Exception:
                    res = q.order("name", desc=False).execute()

                schemes_data = res.data or []
                if not schemes_data and admin and admin != reader:
                    q_admin = admin.table("schemes").select("*")
                    if active_only:
                        q_admin = q_admin.eq("is_active", True)
                    try:
                        res_admin = q_admin.order("display_order", desc=False).order("name", desc=False).execute()
                    except Exception:
                        res_admin = q_admin.order("name", desc=False).execute()
                    schemes_data = res_admin.data or []

                if schemes_data:
                    set_global_cache(cache_key, schemes_data, ttl_seconds=300)
                    set_global_cache("schemes_catalogue_last_good", schemes_data, ttl_seconds=86400)
            except Exception as e:
                print(f"[Schemes] Supabase list error: {e}")
                if admin and admin != reader:
                    try:
                        q_adm = admin.table("schemes").select("*")
                        if active_only:
                            q_adm = q_adm.eq("is_active", True)
                        res_admin = q_adm.execute()
                        schemes_data = res_admin.data or []
                        if schemes_data:
                            set_global_cache(cache_key, schemes_data, ttl_seconds=300)
                            set_global_cache("schemes_catalogue_last_good", schemes_data, ttl_seconds=86400)
                    except Exception:
                        schemes_data = []
                else:
                    schemes_data = []
        else:
            schemes_data = []

        if not schemes_data:
            # When DATA_BACKEND=supabase, NEVER silently substitute the local SQLite database.
            # Instead, serve the last-known-good verified catalogue cache if available, or fail cleanly.
            lkg = get_global_cache("schemes_catalogue_last_good")
            if lkg:
                print("[Schemes] Warning: Serving last-known-good scheme catalogue cache during cloud query outage.")
                schemes_data = lkg
            else:
                print("[Schemes] Notice: Supabase query returned no schemes and no LKG cache available; refusing silent fallback to SQLite.")
                schemes_data = []
    else:
        schemes_data = get_local_db().list_schemes(active_only=active_only)

    if schemes_data:
        set_global_cache(cache_key, schemes_data, ttl_seconds=300)

    # In-memory filtering (instant execution without extra round-trips)
    filtered = []
    for s in schemes_data:
        if active_only and not s.get("is_active", True):
            continue
        if category and category != "ALL" and s.get("category_type") != category:
            continue
        if stage and stage != "ALL" and s.get("stage") != stage:
            continue
        # Filter by search term
        if search:
            term = search.lower()
            text_corpus = f"{s.get('name','')} {s.get('agency','')} {s.get('description','')} {s.get('brief','')}".lower()
            if term not in text_corpus:
                continue
        # Filter by sector
        if sector and sector != "ALL":
            sec_raw = s.get("sectors") or []
            if isinstance(sec_raw, str):
                try:
                    sec_raw = json.loads(sec_raw)
                except Exception:
                    sec_raw = [sec_raw]
            sec_list = [str(x).lower() for x in sec_raw]
            if sector.lower() not in sec_list and "all sectors" not in sec_list:
                continue
        filtered.append(s)
    return filtered

    # SQLite local mode
    return get_local_db().list_schemes(search, category, stage, sector, active_only)

def get_scheme(scheme_id: str) -> Optional[Dict]:
    """Retrieves full details of a single scheme."""
    backend = get_data_backend()

    if backend == "supabase":
        client = _get_user_client()
        admin = _get_admin_client()
        reader = client if client else admin
        if reader:
            try:
                res = reader.table("schemes").select("*").or_(f"id.eq.{scheme_id},source_id.eq.{scheme_id}").execute()
                if res.data and len(res.data) > 0:
                    return res.data[0]
            except Exception:
                pass
            if admin and admin != reader:
                try:
                    res = admin.table("schemes").select("*").or_(f"id.eq.{scheme_id},source_id.eq.{scheme_id}").execute()
                    if res.data and len(res.data) > 0:
                        return res.data[0]
                except Exception:
                    pass
        return None

    # SQLite mode ONLY (when DATA_BACKEND=sqlite)
    return get_local_db().get_scheme_by_id(scheme_id)

def upsert_scheme(scheme: Dict, admin_id: str) -> Tuple[bool, Optional[str]]:
    """Admin adds or updates a funding opportunity."""
    if not scheme.get("name"):
        return False, "Scheme name is required."

    if not scheme.get("id"):
        import uuid
        scheme["id"] = f"SCH-ADMIN-{uuid.uuid4().hex[:8].upper()}"

    scheme["updated_at"] = datetime.now(timezone.utc).isoformat()
    backend = get_data_backend()

    if backend == "supabase":
        client = _get_admin_client()
        if not client:
            return False, "Supabase client not available."
        try:
            client.table("schemes").upsert(scheme, on_conflict="id").execute()
            invalidate_global_cache("schemes")
            invalidate_memo("scheme_matches_ai:")
            return True, None
        except Exception as e:
            return False, f"Failed to save scheme to Supabase: {e}"

    # SQLite mode
    get_local_db().upsert_scheme(scheme)
    get_local_db().log_activity(admin_id, "upsert_scheme", "schemes", scheme["id"], {"name": scheme["name"]})
    invalidate_global_cache("schemes")
    invalidate_memo("scheme_matches_ai:")

    return True, None

def toggle_archive_scheme(scheme_id: str, admin_id: str) -> Tuple[bool, Optional[str]]:
    """Toggles active/archived state for a scheme."""
    s = get_scheme(scheme_id)
    if not s:
        return False, "Scheme not found."

    new_active = not s.get("is_active", True)
    new_status = "active" if new_active else "archived"
    now_iso = datetime.now(timezone.utc).isoformat()
    backend = get_data_backend()

    if backend == "supabase":
        client = _get_admin_client()
        if not client:
            return False, "Supabase client not available."
        try:
            client.table("schemes").update({
                "is_active": new_active,
                "status": new_status,
                "updated_at": now_iso
            }).eq("id", scheme_id).execute()
            invalidate_global_cache("schemes")
            invalidate_memo("scheme_matches_ai:")
            return True, None
        except Exception as e:
            return False, f"Failed to toggle archive state in Supabase: {e}"

    # SQLite mode
    s["is_active"] = new_active
    s["status"] = new_status
    get_local_db().upsert_scheme(s)
    get_local_db().log_activity(admin_id, f"set_{new_status}", "schemes", scheme_id)
    invalidate_global_cache("schemes")
    invalidate_memo("scheme_matches_ai:")
    return True, None

def delete_scheme(scheme_id: str, admin_id: str) -> Tuple[bool, Optional[str]]:
    """Permanently deletes a scheme from the catalogue."""
    backend = get_data_backend()

    if backend == "supabase":
        client = _get_admin_client()
        if not client:
            return False, "Supabase client not available."
        try:
            try:
                client.table("scheme_releases").delete().eq("scheme_id", scheme_id).execute()
                client.table("scheme_support_reviews").delete().eq("scheme_id", scheme_id).execute()
            except Exception as ex_fk:
                print(f"[Schemes] Best-effort cascade cleanup: {ex_fk}")
            client.table("schemes").delete().eq("id", scheme_id).execute()
            invalidate_global_cache("schemes")
            invalidate_memo("scheme_matches_ai:")
            return True, None
        except Exception as e:
            return False, f"Failed to delete scheme in Supabase: {e}"

    # SQLite mode
    get_local_db().delete_scheme(scheme_id)
    get_local_db().log_activity(admin_id, "delete_scheme", "schemes", scheme_id)
    invalidate_global_cache("schemes")
    invalidate_memo("scheme_matches_ai:")
    return True, None

def match_schemes_for_aspirant(
    aspirant_id: str, 
    profile: Optional[Dict] = None, 
    limit: Optional[int] = None, 
    min_score: Optional[int] = 60,
    assistance_need: Optional[Dict] = None
) -> List[Dict]:
    """
    Explainable Deterministic AI-Based Scheme Matching Engine:
    Computes a contextual match score (0-100%) for each active scheme based on:
    - Founder Profile & Venture Reality (Domain, Stage, Geography, Demographics, Registrations)
    - Strategic Assistance Requirements (Need, Type, Bracket, Timeline)
    - Rigorous 3-stage statutory & relevance evaluation
    
    Returns list of matched schemes scoring >= min_score ordered by match_score DESC.
    """
    if not aspirant_id:
        return []

    if profile is None:
        from services.profiles import get_profile
        profile = get_profile(aspirant_id)
        if not profile:
            admin = _get_admin_client()
            if admin:
                try:
                    res_p = admin.table("profiles").select("*").eq("id", aspirant_id).execute()
                    if res_p.data:
                        profile = res_p.data[0]
                except Exception:
                    pass
    if not profile:
        return []

    if assistance_need is None and profile:
        p_data = profile.get("profile_data")
        if isinstance(p_data, dict):
            assistance_need = p_data.get("assistance_need") or {}
        else:
            assistance_need = {}

    y_goal = (assistance_need or {}).get("assistance_goal", "ALL")
    y_quantum = (assistance_need or {}).get("quantum_range", "ANY_AMOUNT")
    cache_key = f"scheme_matches_ai:{aspirant_id}:{min_score}:{limit}:{y_goal}:{y_quantum}"
    cached = get_memo(cache_key)
    if cached is not None:
        return cached

    from services.scheme_matching_engine import match_aspirant_schemes_intelligent
    all_schemes = list_schemes(active_only=True)
    res_final = match_aspirant_schemes_intelligent(
        profile=profile,
        schemes=all_schemes,
        assistance_need=assistance_need,
        min_score=min_score if min_score is not None else 0,
        limit=limit
    )

    set_memo(cache_key, res_final, ttl_seconds=60)
    return res_final

def evaluate_scheme_for_aspirant(aspirant_id: str, scheme_or_id: Any, profile: Optional[Dict] = None, assistance_need: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Evaluates a specific scheme against an Aspirant's profile for the Guide's evaluation panel.
    Accepts either a scheme dict or a scheme_id string.
    Returns calculated score, match reasons, itemized evidence checklist, red flags, and hidden agenda.
    """
    if isinstance(scheme_or_id, str):
        scheme = get_scheme(scheme_or_id)
        if not scheme:
            admin = _get_admin_client()
            if admin:
                try:
                    res_s = admin.table("schemes").select("*").eq("id", scheme_or_id).execute()
                    if res_s.data:
                        scheme = res_s.data[0]
                except Exception:
                    pass
    else:
        scheme = scheme_or_id

    if not scheme:
        return {}

    # Run matching for this scheme
    matches = match_schemes_for_aspirant(aspirant_id, profile=profile, limit=None, min_score=None, assistance_need=assistance_need)
    s_id = str(scheme.get("id") or scheme.get("source_id") or "")
    match_record = next((m for m in matches if str(m.get("id")) == s_id or str(m.get("source_id")) == s_id), None)

    if match_record:
        score = match_record["match_score"]
        reasons = match_record.get("match_reasons", [])
        concerns = match_record.get("potential_concerns", [])
        status = match_record.get("recommendation_status", "POTENTIALLY ELIGIBLE")
        checklist = match_record.get("checklist", [])
        is_disqualified = match_record.get("is_disqualified", False)
    else:
        score = 0
        reasons = []
        concerns = ["Scheme record could not be evaluated against profile."]
        status = "LOW FIT"
        checklist = []
        is_disqualified = False

    hidden_agenda = scheme.get("hidden_agenda") or []
    if isinstance(hidden_agenda, str):
        try:
            hidden_agenda = json.loads(hidden_agenda)
        except Exception:
            hidden_agenda = [hidden_agenda] if hidden_agenda else []

    red_flags = scheme.get("red_flags") or []
    if isinstance(red_flags, str):
        try:
            red_flags = json.loads(red_flags)
        except Exception:
            red_flags = [red_flags] if red_flags else []

    return {
        "match_score": score,
        "score": score,
        "recommendation_status": status,
        "match_reasons": reasons,
        "reasons": reasons,
        "potential_concerns": concerns,
        "scheme": scheme,
        "checklist": checklist,
        "is_disqualified": is_disqualified,
        "eligibility_summary": f"Score: {score}% Match ({status}) | {len(reasons)} criteria met",
        "red_flags": red_flags,
        "hidden_agenda": hidden_agenda,
        "prompt": scheme.get("application_prompt") or ""
    }

def release_scheme_to_aspirant(
    guide_id: str,
    aspirant_id: str,
    scheme_id: str,
    guide_recommendation: str = "",
    guide_note: str = "",
    allow_disqualified_override: bool = False
) -> Tuple[bool, Optional[str]]:
    """
    Guide Gatekeeper action: Releases a scheme to an assigned Aspirant.
    """
    from services.relationships import get_aspirant_mentors
    from services.journey import log_meaningful_event

    # 1. Authorization check: Assigned Guide (Primary or Co-Guide) or Admin
    mentors = get_aspirant_mentors(aspirant_id)
    assigned_guide = mentors.get("guide")
    all_assigned_guide_ids = [str(g.get("id")) for g in mentors.get("guides", []) if g and g.get("id")]
    if assigned_guide and assigned_guide.get("id") and str(assigned_guide["id"]) not in all_assigned_guide_ids:
        all_assigned_guide_ids.append(str(assigned_guide["id"]))
    from services.profiles import get_profile
    actor_prof = get_profile(guide_id)
    is_admin = (actor_prof.get("role") == "admin") if actor_prof else False
    if not is_admin and str(guide_id) not in all_assigned_guide_ids:
        return False, "You are not authorized to release schemes to this Aspirant."

    scheme = get_scheme(scheme_id)
    if not scheme:
        return False, "Scheme record not found."
    scheme_name = scheme.get("name", "Funding Opportunity")

    # Evaluate summary & check if Fulcrum Support already approved a Scheme Support Review override
    eval_res = evaluate_scheme_for_aspirant(aspirant_id, scheme)
    if eval_res.get("is_disqualified") and not allow_disqualified_override:
        try:
            from services.scheme_reviews import list_scheme_support_reviews
            reviews = list_scheme_support_reviews(aspirant_id=aspirant_id)
            has_approved_review = any(
                str(r.get("scheme_id")) == str(scheme_id) and r.get("status") == "APPROVED"
                for r in reviews
            )
            if has_approved_review:
                allow_disqualified_override = True
        except Exception:
            pass
    if eval_res.get("is_disqualified") and not allow_disqualified_override:
        disq_reasons = "; ".join(eval_res.get("potential_concerns", [])) or "Statutory eligibility criteria not met"
        return False, f"Gatekeeper Restriction: Scheme does not meet mandatory criteria for this founder ({disq_reasons}). Please confirm verification override to proceed." 
    eligibility_summary = eval_res.get("eligibility_summary", "Potentially Eligible") if eval_res else "Potentially Eligible"

    now_iso = datetime.now(timezone.utc).isoformat()
    note_text = guide_note.strip() if guide_note else ""
    rec_text = guide_recommendation.strip() if guide_recommendation else "Reviewed and recommended by your Guide."

    backend = get_data_backend()

    if backend == "supabase":
        admin = _get_admin_client()
        client = _get_user_client()
        writer = admin or client
        if not writer:
            return False, "Supabase client not available."
        try:
            try:
                writer.table("scheme_releases").upsert({
                    "aspirant_id": aspirant_id,
                    "guide_id": guide_id,
                    "scheme_id": scheme_id,
                    "status": "RELEASED",
                    "guide_note": note_text,
                    "guide_recommendation": rec_text,
                    "eligibility_summary": eligibility_summary,
                    "released_at": now_iso,
                    "released_by": guide_id,
                    "withdrawn_at": None,
                    "withdrawn_by": None,
                    "updated_at": now_iso
                }, on_conflict="aspirant_id,scheme_id").execute()
            except Exception as e:
                if admin and admin != writer:
                    admin.table("scheme_releases").upsert({
                        "aspirant_id": aspirant_id,
                        "guide_id": guide_id,
                        "scheme_id": scheme_id,
                        "status": "RELEASED",
                        "guide_note": note_text,
                        "guide_recommendation": rec_text,
                        "eligibility_summary": eligibility_summary,
                        "released_at": now_iso,
                        "released_by": guide_id,
                        "withdrawn_at": None,
                        "withdrawn_by": None,
                        "updated_at": now_iso
                    }, on_conflict="aspirant_id,scheme_id").execute()
                else:
                    raise e
        except Exception as e:
            return False, f"Failed to release scheme in Supabase: {e}"
    else:
        # SQLite mode
        get_local_db().create_or_update_scheme_release(
            aspirant_id=aspirant_id,
            guide_id=guide_id,
            scheme_id=scheme_id,
            guide_recommendation=rec_text,
            guide_note=note_text,
            eligibility_summary=eligibility_summary
        )

    # Log Journey Event
    log_meaningful_event(
        aspirant_id=aspirant_id,
        actor_id=guide_id,
        actor_role="guide",
        event_type="scheme_released",
        title=f"Funding Opportunity Recommended: {scheme_name}",
        description=f"Guide released {scheme_name} as a recommended funding opportunity. Note: {rec_text}",
        metadata={
            "scheme_id": scheme_id,
            "scheme_name": scheme_name,
            "guide_id": guide_id,
            "recommendation": rec_text
        }
    )

    # Dispatch In-App Notification to Aspirant
    try:
        from services.notifications import create_notification
        create_notification(
            user_id=aspirant_id,
            title=f"Scheme Released: {scheme_name}",
            message=f"Your Guide has released a curated scheme: '{scheme_name}'. Recommendation: {rec_text}",
            notification_type="scheme_released",
            actor_id=guide_id
        )
    except Exception as e:
        print(f"[Schemes] Notification error: {e}")

    # Invalidate caches
    invalidate_memo(f"released_schemes:{aspirant_id}")

    return True, None

def withdraw_scheme_release(
    guide_id: str,
    aspirant_id: str,
    scheme_id: str
) -> Tuple[bool, Optional[str]]:
    """
    Guide Gatekeeper action: Withdraws a previously released scheme.
    """
    from services.relationships import get_aspirant_mentors
    from services.journey import log_meaningful_event

    mentors = get_aspirant_mentors(aspirant_id)
    assigned_guide = mentors.get("guide")
    all_assigned_guide_ids = [str(g.get("id")) for g in mentors.get("guides", []) if g and g.get("id")]
    if assigned_guide and assigned_guide.get("id") and str(assigned_guide["id"]) not in all_assigned_guide_ids:
        all_assigned_guide_ids.append(str(assigned_guide["id"]))
    from services.profiles import get_profile
    actor_prof = get_profile(guide_id)
    is_admin = (actor_prof.get("role") == "admin") if actor_prof else False
    if not is_admin and str(guide_id) not in all_assigned_guide_ids:
        return False, "You are not authorized to release schemes to this Aspirant."

    scheme = get_scheme(scheme_id)
    scheme_name = scheme.get("name", "Funding Opportunity") if scheme else "Funding Opportunity"
    now_iso = datetime.now(timezone.utc).isoformat()

    backend = get_data_backend()

    if backend == "supabase":
        admin = _get_admin_client()
        client = _get_user_client()
        writer = admin or client
        if not writer:
            return False, "Supabase client not available."
        try:
            try:
                writer.table("scheme_releases").update({
                    "status": "WITHDRAWN",
                    "withdrawn_at": now_iso,
                    "withdrawn_by": guide_id,
                    "updated_at": now_iso
                }).eq("aspirant_id", aspirant_id).eq("scheme_id", scheme_id).execute()
            except Exception as e:
                if admin and admin != writer:
                    admin.table("scheme_releases").update({
                        "status": "WITHDRAWN",
                        "withdrawn_at": now_iso,
                        "withdrawn_by": guide_id,
                        "updated_at": now_iso
                    }).eq("aspirant_id", aspirant_id).eq("scheme_id", scheme_id).execute()
                else:
                    raise e
        except Exception as e:
            return False, f"Failed to withdraw scheme release in Supabase: {e}"
    else:
        # SQLite mode
        get_local_db().withdraw_scheme_release(aspirant_id, scheme_id, guide_id)

    # Log Journey Event
    log_meaningful_event(
        aspirant_id=aspirant_id,
        actor_id=guide_id,
        actor_role="guide",
        event_type="scheme_release_withdrawn",
        title=f"Scheme Release Withdrawn: {scheme_name}",
        description=f"Guide withdrew prior release of {scheme_name}.",
        metadata={
            "scheme_id": scheme_id,
            "scheme_name": scheme_name,
            "guide_id": guide_id
        }
    )

    # Invalidate caches
    invalidate_memo(f"released_schemes:{aspirant_id}")

    return True, None

def get_released_schemes_for_aspirant(aspirant_id: str) -> List[Dict]:
    """
    Aspirant-facing scheme query:
    STRICTLY returns ONLY released schemes with Guide recommendations.
    CRITICAL SECURITY INVARIANT:
    Sanitizes and eliminates all Guide-only private intelligence
    (hidden_agenda, red_flags, AI pitch prompt) from the payload.
    """
    if not aspirant_id:
        return []

    cache_key = f"released_schemes:{aspirant_id}"
    cached = get_memo(cache_key)
    if cached is not None:
        return cached

    backend = get_data_backend()

    if backend == "supabase":
        client = _get_user_client()
        admin = _get_admin_client()
        reader = client if client else admin
        if reader:
            try:
                # 1. Fetch release records for this aspirant (RLS enforces aspirant reads own released records)
                res = None
                try:
                    res = reader.table("scheme_releases")\
                        .select("*")\
                        .eq("aspirant_id", aspirant_id)\
                        .eq("status", "RELEASED")\
                        .execute()
                except Exception:
                    pass
                if res is None and admin and admin != reader:
                    try:
                        res = admin.table("scheme_releases")\
                            .select("*")\
                            .eq("aspirant_id", aspirant_id)\
                            .eq("status", "RELEASED")\
                            .execute()
                    except Exception:
                        pass
                if not res or not res.data:
                    set_memo(cache_key, [], ttl_seconds=60)
                    return []

                # 2. Extract scheme IDs and fetch scheme catalogue records (admin client bypasses guide-only RLS on schemes)
                scheme_ids = [r["scheme_id"] for r in res.data if r.get("scheme_id")]
                if not scheme_ids:
                    set_memo(cache_key, [], ttl_seconds=60)
                    return []

                s_res = None
                if admin:
                    try:
                        s_res = admin.table("schemes").select("*").in_("id", scheme_ids).execute()
                    except Exception as ex:
                        print(f"[Schemes] Admin query for released schemes failed: {ex}")
                if not s_res or not s_res.data:
                    try:
                        s_res = reader.table("schemes").select("*").in_("id", scheme_ids).execute()
                    except Exception as ex:
                        print(f"[Schemes] Reader query for released schemes failed: {ex}")

                s_map = {str(s["id"]): s for s in (s_res.data or []) if s.get("id")}

                cleaned = []
                for r in res.data:
                    sid = str(r.get("scheme_id"))
                    s = s_map.get(sid)
                    if not s:
                        continue
                    s_clean = dict(s)
                    s_clean["id"] = sid
                    s_clean["scheme_id"] = sid
                    s_clean["release_id"] = r.get("id")
                    s_clean["guide_id"] = r.get("guide_id")
                    s_clean["guide_recommendation"] = r.get("guide_recommendation")
                    s_clean["released_at"] = r.get("released_at")
                    s_clean["eligibility_summary"] = r.get("eligibility_summary")
                    s_clean["application_stage"] = _extract_application_stage(r)
                    # STRICT PRIVATE INTELLIGENCE STRIPPING:
                    # Never leak internal Guide evaluation notes, hidden agenda, or AI prompt to entrepreneur
                    s_clean.pop("guide_note", None)
                    s_clean.pop("hidden_agenda", None)
                    s_clean.pop("red_flags", None)
                    s_clean.pop("application_prompt", None)
                    cleaned.append(s_clean)
                set_memo(cache_key, cleaned, ttl_seconds=60)
                return cleaned
            except Exception as e:
                print(f"[Schemes] Supabase released schemes query error: {e}")
                return []
        return []

    local_res = get_local_db().get_released_schemes_for_aspirant(aspirant_id)
    cleaned_local = []
    for item in (local_res or []):
        c_item = dict(item)
        c_item["application_stage"] = _extract_application_stage(c_item)
        c_item.pop("guide_note", None)
        c_item.pop("hidden_agenda", None)
        c_item.pop("red_flags", None)
        c_item.pop("application_prompt", None)
        cleaned_local.append(c_item)
    set_memo(cache_key, cleaned_local, ttl_seconds=60)
    return cleaned_local

SCHEME_APPLICATION_STAGES = (
    "Recommended",
    "Preparing DPR / Documents",
    "Applied on Portal",
    "Sanctioned / Funded",
    "Rejected / Not Pursuing"
)

def _extract_application_stage(release_row: Dict) -> str:
    """Extracts the post-release application stage from a scheme_releases row."""
    if not release_row:
        return "Recommended"
    if release_row.get("application_stage") in SCHEME_APPLICATION_STAGES:
        return release_row["application_stage"]
    for field in ("eligibility_summary", "guide_note"):
        txt = str(release_row.get(field) or "")
        if "[AppStage:" in txt:
            try:
                part = txt.split("[AppStage:", 1)[1].split("]", 1)[0].strip()
                if part in SCHEME_APPLICATION_STAGES:
                    return part
            except Exception:
                pass
    return "Recommended"

def update_scheme_application_stage(
    aspirant_id: str,
    scheme_id: str,
    actor_id: str,
    actor_role: str,
    stage: str = "",
    note: str = "",
    new_stage: Optional[str] = None,
    stage_note: Optional[str] = None,
    **kwargs
) -> Tuple[bool, Optional[str]]:
    """
    Updates the post-release application tracking stage for a released scheme
    (Recommended -> Preparing DPR / Documents -> Applied on Portal -> Sanctioned / Funded / Rejected / Not Pursuing)
    and logs a Journey milestone event.
    """
    actual_stage = new_stage if new_stage is not None else stage
    actual_note = stage_note if stage_note is not None else note

    if actual_stage not in SCHEME_APPLICATION_STAGES:
        return False, f"Invalid application stage. Must be one of: {', '.join(SCHEME_APPLICATION_STAGES)}"
    if not aspirant_id or not scheme_id:
        return False, "Aspirant ID and Scheme ID are required."

    # Authorization: Aspirant owner, assigned Guide (primary or Co-Guide), or verified Platform Admin
    from services.relationships import get_aspirant_mentors
    from services.profiles import get_profile
    from services.roles import is_strict_admin
    actor_prof = get_profile(actor_id) or {}
    # Anti-spoofing: Verify actual admin identity rather than trusting caller-supplied text parameter
    is_admin = is_strict_admin(user_id=actor_id, user_dict=actor_prof)
    is_owner = (str(actor_id) == str(aspirant_id))
    mentors = get_aspirant_mentors(aspirant_id) or {}
    guide_ids = [str(g.get("id")) for g in mentors.get("guides", []) if g and g.get("id")]
    if mentors.get("guide") and mentors["guide"].get("id"):
        guide_ids.append(str(mentors["guide"]["id"]))
    is_assigned_guide = str(actor_id) in guide_ids

    if not (is_admin or is_owner or is_assigned_guide):
        return False, "Unauthorized: Only the entrepreneur or their assigned Guide may update application progress."

    scheme = get_scheme(scheme_id) or {}
    scheme_name = scheme.get("name", "Funding Opportunity")
    now_iso = datetime.now(timezone.utc).isoformat()
    backend = get_data_backend()

    if backend == "supabase":
        admin = _get_admin_client()
        client = _get_user_client()
        writer = admin or client
        if not writer:
            return False, "Database client unavailable."
        try:
            r_res = writer.table("scheme_releases").select("*").eq("aspirant_id", aspirant_id).eq("scheme_id", scheme_id).execute()
            if not r_res.data:
                return False, "Scheme release record not found."
            row = r_res.data[0]
            curr_elig = str(row.get("eligibility_summary") or "Potentially Eligible")
            if "[AppStage:" in curr_elig:
                base_elig = curr_elig.split("[AppStage:", 1)[0].strip()
            else:
                base_elig = curr_elig.strip()
            new_elig = f"{base_elig} [AppStage: {actual_stage}]".strip()
            upd_payload = {
                "eligibility_summary": new_elig,
                "updated_at": now_iso
            }
            if actual_note and actual_note.strip():
                curr_note = str(row.get("guide_note") or "").strip()
                upd_payload["guide_note"] = f"{curr_note} | [{actual_stage}] {actual_note.strip()}".strip(" |")
            writer.table("scheme_releases").update(upd_payload).eq("aspirant_id", aspirant_id).eq("scheme_id", scheme_id).execute()
            # Best-effort: persist to dedicated columns (Migration 008). Silently skipped if columns absent.
            try:
                writer.table("scheme_releases").update({
                    "application_stage": actual_stage,
                    "application_note": (actual_note or "").strip(),
                    "stage_updated_at": now_iso,
                    "stage_updated_by": actor_id
                }).eq("aspirant_id", aspirant_id).eq("scheme_id", scheme_id).execute()
            except Exception:
                pass
        except Exception as e:
            return False, f"Failed to update scheme application stage: {e}"
    else:
        db = get_local_db()
        conn = db._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT eligibility_summary, guide_note FROM scheme_releases WHERE aspirant_id = ? AND scheme_id = ?", (aspirant_id, scheme_id))
        row = cur.fetchone()
        if not row:
            conn.close()
            return False, "Scheme release record not found."
        curr_elig = str(row["eligibility_summary"] or "Potentially Eligible")
        base_elig = curr_elig.split("[AppStage:", 1)[0].strip() if "[AppStage:" in curr_elig else curr_elig.strip()
        new_elig = f"{base_elig} [AppStage: {actual_stage}]".strip()
        curr_note = str(row["guide_note"] or "").strip()
        new_note = f"{curr_note} | [{actual_stage}] {actual_note.strip()}".strip(" |") if (actual_note and actual_note.strip()) else curr_note
        cur.execute("""
            UPDATE scheme_releases
            SET eligibility_summary = ?, guide_note = ?, updated_at = ?
            WHERE aspirant_id = ? AND scheme_id = ?
        """, (new_elig, new_note, now_iso, aspirant_id, scheme_id))
        conn.commit()
        conn.close()

    from services.journey import log_meaningful_event
    desc = f"Scheme application progress for '{scheme_name}' updated to: {actual_stage}."
    if actual_note and actual_note.strip():
        desc += f" Note: {actual_note.strip()}"
    log_meaningful_event(
        aspirant_id=aspirant_id,
        actor_id=actor_id,
        actor_role=actor_role,
        event_type="scheme_stage_updated",
        title=f"Scheme Progress ({stage}): {scheme_name}",
        description=desc,
        metadata={"scheme_id": scheme_id, "scheme_name": scheme_name, "application_stage": stage}
    )

    invalidate_memo(f"released_schemes:{aspirant_id}")
    return True, None

def get_guide_scheme_releases(guide_id: str, aspirant_id: Optional[str] = None) -> List[Dict]:
    """
    Returns complete release history (RELEASED and WITHDRAWN) for Guide view.
    When aspirant_id is provided, returns all releases for that aspirant so Co-Guides have shared visibility.
    """
    backend = get_data_backend()

    if backend == "supabase":
        client = _get_user_client()
        admin = _get_admin_client()
        reader = client if client else admin
        if reader:
            try:
                res = None
                try:
                    q = reader.table("scheme_releases").select("*, schemes(name, agency, amount), profiles:aspirant_id(full_name, email)")
                    if aspirant_id:
                        q = q.eq("aspirant_id", aspirant_id)
                    else:
                        q = q.eq("guide_id", guide_id)
                    res = q.order("updated_at", desc=True).execute()
                except Exception:
                    pass
                if (not res or not res.data) and admin and admin != reader:
                    try:
                        q = admin.table("scheme_releases").select("*, schemes(name, agency, amount), profiles:aspirant_id(full_name, email)")
                        if aspirant_id:
                            q = q.eq("aspirant_id", aspirant_id)
                        else:
                            q = q.eq("guide_id", guide_id)
                        res = q.order("updated_at", desc=True).execute()
                    except Exception:
                        pass
                if res and res.data:
                    rows = []
                    for r in res.data:
                        sc = r.get("schemes") or {}
                        ap = r.get("profiles") or {}
                        r["scheme_name"] = sc.get("name") or "Scheme"
                        r["scheme_agency"] = sc.get("agency") or ""
                        r["scheme_amount"] = sc.get("amount") or ""
                        r["aspirant_name"] = ap.get("full_name") or "Entrepreneur"
                        r["aspirant_email"] = ap.get("email") or ""
                        r["application_stage"] = _extract_application_stage(r)
                        rows.append(r)
                    return rows
                return []
            except Exception as e:
                print(f"[Schemes] Supabase guide releases query error: {e}")
                return []
        return []

    rows = get_local_db().get_scheme_releases_for_guide(guide_id, aspirant_id)
    for r in (rows or []):
        r["application_stage"] = _extract_application_stage(r)
    return rows
