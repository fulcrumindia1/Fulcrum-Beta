"""
services/scheme_reviews.py — Human-in-the-Loop Scheme Support Review Workflow
==============================================================================
Enables Caseload Guides to escalate borderline or uncertain scheme matches
to Fulcrum Support (Administration) for authoritative review and approval.
Supports dual backends: Supabase (primary) and SQLite (local resilient mode).
"""

import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, List, Tuple
from services.auth import get_supabase_client, get_supabase_admin_client, get_data_backend
from services.local_db import get_local_db
from services.governance import get_primary_admin_id
from services.cache import invalidate_memo


def submit_scheme_support_review(
    aspirant_id: str,
    scheme_id: str,
    guide_id: str,
    match_score: int,
    guide_justification: str,
    failed_criteria: Optional[List[str]] = None,
    missing_criteria: Optional[List[str]] = None
) -> Tuple[bool, Optional[str]]:
    """
    Submits a scheme match for administrative review by Fulcrum Support.
    Triggered by a Guide when an opportunity shows strong commercial promise
    despite failing algorithmic gatekeeper checks or missing statutory evidence.
    """
    if not guide_justification or len(guide_justification.strip()) < 10:
        return False, "Please provide a detailed justification for this review (minimum 10 characters)."

    review_id = str(uuid.uuid4())
    now_iso = datetime.now(timezone.utc).isoformat()
    fc = failed_criteria or []
    mc = missing_criteria or []

    record = {
        "id": review_id,
        "aspirant_id": aspirant_id,
        "scheme_id": scheme_id,
        "guide_id": guide_id,
        "match_score": int(match_score),
        "guide_justification": guide_justification.strip(),
        "failed_criteria": fc,
        "missing_criteria": mc,
        "status": "PENDING",
        "admin_decision_notes": None,
        "reviewed_by": None,
        "reviewed_at": None,
        "created_at": now_iso,
        "updated_at": now_iso
    }

    backend = get_data_backend()
    if backend == "supabase":
        admin = get_supabase_admin_client()
        if admin:
            try:
                admin.table("scheme_support_reviews").upsert(
                    record,
                    on_conflict="aspirant_id, scheme_id, guide_id"
                ).execute()
            except Exception as e:
                # If Supabase table is not yet migrated, we continue to local DB safely
                print(f"[SchemeReviews] Supabase insertion note: {e}")

    # Mirror to local DB
    db = get_local_db()
    if hasattr(db, "insert_or_update_scheme_support_review"):
        db.insert_or_update_scheme_support_review(record)

    # Dispatch notification to Super Admin (Fulcrum Support)
    try:
        from services.notifications import create_notification
        from services.profiles import get_profile
        from services.schemes import get_scheme

        admin_id = get_primary_admin_id()
        asp_p = get_profile(aspirant_id) or {}
        asp_name = asp_p.get("full_name", "Entrepreneur")
        scheme = get_scheme(scheme_id) or {}
        scheme_name = scheme.get("name", "Scheme")

        create_notification(
            user_id=admin_id,
            title="Scheme Support Review Requested",
            message=f"Guide requested administrative review for '{scheme_name}' on behalf of {asp_name} ({match_score}% match).",
            notification_type="SCHEME_SUPPORT_REVIEW",
            actor_id=guide_id
        )
    except Exception as e:
        print(f"[SchemeReviews] Notification dispatch error: {e}")

    return True, None


def list_scheme_support_reviews(
    status: Optional[str] = None,
    guide_id: Optional[str] = None,
    aspirant_id: Optional[str] = None
) -> List[Dict]:
    """Retrieves scheme support reviews for the Admin Inbox or Guide View."""
    backend = get_data_backend()
    records = []

    if backend == "supabase":
        admin = get_supabase_admin_client()
        if admin:
            try:
                q = admin.table("scheme_support_reviews").select(
                    "*, profiles:aspirant_id(full_name, email), schemes:scheme_id(name, agency, amount), guide:guide_id(full_name, email)"
                ).order("created_at", desc=True)
                if status:
                    q = q.eq("status", status)
                if guide_id:
                    q = q.eq("guide_id", guide_id)
                if aspirant_id:
                    q = q.eq("aspirant_id", aspirant_id)
                res = q.execute()
                for r in (res.data or []):
                    asp = r.get("profiles") or {}
                    sch = r.get("schemes") or {}
                    g = r.get("guide") or {}
                    r["aspirant_name"] = asp.get("full_name") or "Entrepreneur"
                    r["aspirant_email"] = asp.get("email") or ""
                    r["scheme_name"] = sch.get("name") or "Scheme"
                    r["scheme_agency"] = sch.get("agency") or ""
                    r["scheme_amount"] = sch.get("amount") or ""
                    r["guide_name"] = g.get("full_name") or "Guide"
                    r["guide_email"] = g.get("email") or ""
                    records.append(r)
            except Exception as e:
                print(f"[SchemeReviews] Supabase query note: {e}")

    if not records:
        try:
            db = get_local_db()
            if hasattr(db, "list_scheme_support_reviews"):
                records = db.list_scheme_support_reviews(
                    status=status,
                    guide_id=guide_id,
                    aspirant_id=aspirant_id
                )
        except Exception as e:
            print(f"[SchemeReviews] Local DB fallback note: {e}")
            records = []

    return records


def decide_scheme_support_review(
    review_id: str,
    decision: str,
    admin_notes: str,
    admin_id: str
) -> Tuple[bool, Optional[str]]:
    """
    Super Admin (Fulcrum Support) records decision ('APPROVED' or 'REJECTED')
    with authoritative audit notes and alerts the submitting Guide.
    """
    if decision not in ("APPROVED", "REJECTED"):
        return False, "Decision must be either 'APPROVED' or 'REJECTED'."

    if not admin_notes or len(admin_notes.strip()) < 5:
        return False, "Please provide administrative decision notes (minimum 5 characters)."

    now_iso = datetime.now(timezone.utc).isoformat()
    backend = get_data_backend()
    target_review = None

    # Fetch review record to find guide_id and aspirant_id
    reviews = list_scheme_support_reviews()
    target_review = next((r for r in reviews if r.get("id") == review_id), None)

    if backend == "supabase":
        admin = get_supabase_admin_client()
        if admin:
            try:
                admin.table("scheme_support_reviews").update({
                    "status": decision,
                    "admin_decision_notes": admin_notes.strip(),
                    "reviewed_by": admin_id,
                    "reviewed_at": now_iso,
                    "updated_at": now_iso
                }).eq("id", review_id).execute()
            except Exception as e:
                print(f"[SchemeReviews] Supabase update note: {e}")

    db = get_local_db()
    if hasattr(db, "update_scheme_support_review"):
        db.update_scheme_support_review(
            review_id=review_id,
            status=decision,
            admin_decision_notes=admin_notes.strip(),
            reviewed_by=admin_id
        )

    # Notify Guide of Support Decision & Auto-Release Scheme on Approval
    if target_review:
        if decision == "APPROVED" and target_review.get("aspirant_id") and target_review.get("scheme_id"):
            try:
                from services.schemes import release_scheme_to_aspirant
                release_scheme_to_aspirant(
                    guide_id=target_review.get("guide_id") or admin_id,
                    aspirant_id=target_review["aspirant_id"],
                    scheme_id=target_review["scheme_id"],
                    guide_recommendation=target_review.get("justification") or admin_notes.strip(),
                    guide_note=f"Approved via Scheme Support Review: {admin_notes.strip()}",
                )
            except Exception as rel_err:
                print(f"[SchemeReviews] Auto-release note: {rel_err}")

        try:
            from services.notifications import create_notification
            guide_recipient_id = target_review.get("guide_id")
            scheme_title = target_review.get("scheme_name", "Scheme")
            asp_title = target_review.get("aspirant_name", "Entrepreneur")

            if guide_recipient_id:
                if decision == "APPROVED":
                    n_title = f"Review Approved: {scheme_title}"
                    n_msg = f"Fulcrum Support approved your review for {asp_title}. You may now release this scheme to their venture dashboard."
                else:
                    n_title = f"Review Rejected: {scheme_title}"
                    n_msg = f"Fulcrum Support reviewed and did not approve '{scheme_title}' for {asp_title}. Notes: {admin_notes.strip()}"

                create_notification(
                    user_id=guide_recipient_id,
                    title=n_title,
                    message=n_msg,
                    notification_type="SCHEME_REVIEW_DECISION",
                    actor_id=admin_id
                )
        except Exception as e:
            print(f"[SchemeReviews] Guide notification error: {e}")

    return True, None

