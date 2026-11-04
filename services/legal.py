"""
services/legal.py — Legal Agreements, Versioned Terms & Mandatory NDA System
=============================================================================
Manages versioned legal agreements (Terms & Conditions, Guide/SME NDAs),
audit logs of signed acceptances, cryptographic text hash verification,
and server-side authorization gating for sensitive entrepreneur caseloads.
"""

import hashlib
import json
from datetime import datetime, timezone
from typing import Optional, Dict, List, Tuple

from services.auth import get_supabase_client, get_supabase_admin_client, get_data_backend
from services.local_db import get_local_db
from services.cache import get_memo, set_memo, invalidate_memo

# Default Master Legal Documents
DEFAULT_TERMS_DOC = {
    "id": "terms_v1_0",
    "doc_type": "terms_and_conditions",
    "version": "1.0.0",
    "title": "Fulcrum-India Platform Terms & Conditions",
    "content": """FULCRUM-INDIA PLATFORM TERMS & CONDITIONS
Version 1.0.0 — Effective Date: 2026-09-01

1. PURPOSE & SCOPE
Fulcrum-India is an enterprise guidance operating system designed to assist entrepreneurs in Tamil Nadu and India by coordinating mentorship, journey documentation, and funding scheme intelligence.

2. USER CONDUCT & ACCURACY OF DATA
Entrepreneurs, Guides, Subject Matter Experts (SMEs), and Administrators agree to provide accurate, up-to-date venture information and respect intellectual property.

3. SCHEME RECOMMENDATIONS & DISCLAIMER
Scheme matching scores and recommendations are strictly indicative ("Recommended" or "Potentially Eligible") based on deterministic algorithms and do not constitute a legal grant guarantee or financial approval.

4. PRIVACY & DATA GOVERNANCE
User profile data is protected under institutional governance and Row Level Security. Data is shared with designated Guides and SMEs solely for authorized advisory engagements.

5. TERMINATION & MODIFICATION
Administration reserves the right to suspend accounts violating professional ethics or confidentiality agreements.""",
    "effective_date": "2026-09-01",
    "is_mandatory": True,
    "is_active": True,
    "roles_covered": ["aspirant", "guide", "sme", "admin"]
}

DEFAULT_NDA_DOC = {
    "id": "nda_dual_v1_0",
    "doc_type": "nda_dual",
    "version": "1.0.0",
    "title": "Fulcrum-India Confidentiality & Non-Disclosure Agreement (Guide & SME)",
    "content": """FULCRUM-INDIA CONFIDENTIALITY & NON-DISCLOSURE AGREEMENT (NDA)
For Certified Guides and Domain Subject Matter Experts (SMEs)
Version 1.0.0 — Effective Date: 2026-09-01

1. CONFIDENTIAL INFORMATION
As an institutional mentor (Guide) or specialist advisory consultant (SME), you will receive access to proprietary business plans, financial projections, GST details, trade secrets, intellectual property, private journey events, and funding strategies of grassroots entrepreneurs.

2. MANDATORY CONFIDENTIALITY OBLIGATION
You agree to maintain strict confidentiality of all entrepreneur information. You shall not disclose, copy, distribute, commercialize, or use any entrepreneur data for any purpose other than providing authorized guidance through Fulcrum-India.

3. CONFLICT OF INTEREST
You must promptly disclose any commercial, financial, or personal interest in an entrepreneur's venture or direct competitors before engaging in advisory consults.

4. NON-CIRCUMVENTION
You shall not independently solicit, contract, or transact with assigned entrepreneurs outside the governing framework of Fulcrum-India without prior administrative approval.

5. REMEDIES & GOVERNING LAW
Breach of this agreement shall result in immediate revocation of mentor privileges and may result in legal remedies under the Indian Contract Act, 1872 and Information Technology Act, 2000.""",
    "effective_date": "2026-09-01",
    "is_mandatory": True,
    "is_active": True,
    "roles_covered": ["guide", "sme"]
}


def _compute_hash(text: str) -> str:
    """Returns SHA-256 hash of document text for cryptographic immutability."""
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()


DEFAULT_TERMS_DOC["content_hash"] = _compute_hash(DEFAULT_TERMS_DOC["content"])
DEFAULT_NDA_DOC["content_hash"] = _compute_hash(DEFAULT_NDA_DOC["content"])


def get_active_legal_document(doc_type: str = "terms_and_conditions") -> Optional[Dict]:
    """Retrieves the active version of a legal document."""
    cache_key = f"legal_doc:{doc_type}"
    cached = get_memo(cache_key)
    if cached is not None:
        return cached

    backend = get_data_backend()
    doc = None

    if backend == "supabase":
        client = get_supabase_admin_client() or get_supabase_client()
        if client:
            try:
                res = client.table("legal_documents").select("*").eq("doc_type", doc_type).eq("is_active", True).order("created_at", desc=True).limit(1).execute()
                if res.data:
                    doc = res.data[0]
            except Exception:
                pass

    if not doc:
        db = get_local_db()
        if hasattr(db, "get_legal_document"):
            doc = db.get_legal_document(doc_type)

    if not doc:
        # Fallback to in-memory default
        if doc_type == "terms_and_conditions":
            doc = DEFAULT_TERMS_DOC
        elif doc_type in ("nda_guide", "nda_sme", "nda_dual"):
            doc = DEFAULT_NDA_DOC

    set_memo(cache_key, doc, ttl_seconds=300)
    return doc


def check_user_terms_accepted(user_id: str) -> bool:
    """Returns True if user has accepted the current mandatory Platform Terms & Conditions."""
    if not user_id:
        return False

    cache_key = f"terms_accepted:{user_id}"
    cached = get_memo(cache_key)
    if cached is not None:
        return cached

    backend = get_data_backend()
    accepted = False

    if backend == "supabase":
        client = get_supabase_admin_client() or get_supabase_client()
        if client:
            try:
                res = client.table("legal_acceptances").select("id").eq("user_id", user_id).eq("doc_type", "terms_and_conditions").limit(1).execute()
                accepted = bool(res.data)
            except Exception:
                pass

    if not accepted:
        db = get_local_db()
        if hasattr(db, "check_legal_acceptance"):
            accepted = db.check_legal_acceptance(user_id, "terms_and_conditions")

    set_memo(cache_key, accepted, ttl_seconds=60)
    return accepted


def check_user_nda_accepted(user_id: str, role: str) -> bool:
    """
    Returns True if user has accepted the mandatory NDA for the given role (guide or sme).
    Aspirants do not require an NDA.
    """
    if not user_id or role not in ("guide", "sme"):
        return True

    cache_key = f"nda_accepted:{user_id}:{role}"
    cached = get_memo(cache_key)
    if cached is not None:
        return cached

    backend = get_data_backend()
    accepted = False

    if backend == "supabase":
        client = get_supabase_admin_client() or get_supabase_client()
        if client:
            try:
                res = client.table("legal_acceptances").select("roles_covered").eq("user_id", user_id).execute()
                if res.data:
                    for acc in res.data:
                        roles = acc.get("roles_covered") or []
                        if isinstance(roles, str):
                            try:
                                roles = json.loads(roles)
                            except Exception:
                                roles = [roles]
                        if role in roles or "nda_dual" in str(acc):
                            accepted = True
                            break
            except Exception:
                pass

    if not accepted:
        db = get_local_db()
        if hasattr(db, "check_legal_acceptance"):
            accepted = db.check_legal_acceptance(user_id, role)

    set_memo(cache_key, accepted, ttl_seconds=60)
    return accepted


def record_legal_acceptance(
    user_id: str,
    user_email: str,
    doc_type: str,
    typed_name: str,
    typed_phrase: str,
    checkbox_confirmed: bool,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
) -> Tuple[bool, Optional[str]]:
    """
    Records a binding legal acceptance.
    Validates:
      1. typed_phrase equals 'I ACCEPT' (case-insensitive)
      2. checkbox_confirmed is True
      3. typed_name is non-empty
      4. hashes document text to ensure tamper resistance.
    If doc_type is NDA, automatically activates the corresponding role grant in user_roles.
    """
    if not user_id or not user_email:
        return False, "User identification missing."

    if not checkbox_confirmed:
        return False, "You must check the confirmation checkbox to agree to the legal terms."

    if not typed_phrase or typed_phrase.strip().upper() != "I ACCEPT":
        return False, "You must explicitly type 'I ACCEPT' in the confirmation box."

    if not typed_name or len(typed_name.strip()) < 3:
        return False, "Please enter your full legal name."

    # Fetch document metadata
    doc = get_active_legal_document(doc_type)
    if not doc:
        return False, f"Legal document not found for type: {doc_type}"

    doc_id = doc.get("id", "doc_default")
    doc_version = doc.get("version", "1.0.0")
    doc_hash = doc.get("content_hash") or _compute_hash(doc.get("content", ""))
    roles_covered = doc.get("roles_covered", [doc_type])
    if isinstance(roles_covered, str):
        try:
            roles_covered = json.loads(roles_covered)
        except Exception:
            roles_covered = [roles_covered]

    now_iso = datetime.now(timezone.utc).isoformat()
    import uuid
    acceptance_id = str(uuid.uuid4())

    acceptance_record = {
        "id": acceptance_id,
        "user_id": user_id,
        "document_id": doc_id,
        "doc_type": doc_type,
        "doc_version": doc_version,
        "doc_hash": doc_hash,
        "user_email_snapshot": user_email,
        "typed_legal_name": typed_name.strip(),
        "typed_acceptance_phrase": typed_phrase.strip().upper(),
        "checkbox_confirmed": True,
        "roles_covered": roles_covered,
        "ip_address": ip_address or "127.0.0.1",
        "user_agent": user_agent or "Streamlit/FulcrumApp",
        "status": "ACCEPTED",
        "accepted_at": now_iso
    }

    backend = get_data_backend()
    if backend == "supabase":
        admin = get_supabase_admin_client()
        if admin:
            try:
                admin.table("legal_acceptances").insert(acceptance_record).execute()
            except Exception as e:
                # If Supabase table missing, log and fallback to local
                pass

    # Always write to local DB
    db = get_local_db()
    if hasattr(db, "record_legal_acceptance"):
        db.record_legal_acceptance(acceptance_record)

    # Invalidate cache
    invalidate_memo(f"terms_accepted:{user_id}")
    invalidate_memo(f"nda_accepted:{user_id}:guide")
    invalidate_memo(f"nda_accepted:{user_id}:sme")

    # If this is an NDA, activate pending roles
    from services.roles import activate_role, get_pending_nda_roles
    pending = get_pending_nda_roles(user_id)
    for r in roles_covered:
        if r in pending:
            activate_role(user_id, r)

    return True, None


def list_legal_acceptances(user_id: Optional[str] = None, doc_type: Optional[str] = None) -> List[Dict]:
    """Retrieves legal acceptance audit logs for Super Admin review."""
    backend = get_data_backend()
    records = []

    if backend == "supabase":
        admin = get_supabase_admin_client()
        if admin:
            try:
                q = admin.table("legal_acceptances").select("*").order("accepted_at", desc=True)
                if user_id:
                    q = q.eq("user_id", user_id)
                if doc_type:
                    q = q.eq("doc_type", doc_type)
                res = q.execute()
                records = res.data or []
            except Exception:
                pass

    if not records:
        db = get_local_db()
        if hasattr(db, "get_legal_acceptances"):
            records = db.get_legal_acceptances(user_id=user_id, doc_type=doc_type)

    return records

