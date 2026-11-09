"""
services/external_contact.py — Shared External Contact Actions (WhatsApp & Gmail)
=================================================================================
Provides safe, authorized, and compliant external communication actions for the
single Platform Admin to contact Guides, SMEs, and Aspirants.

Core Guarantees:
  1. Strict Admin Authorization: Only the verified Platform Admin may generate contact links.
  2. Public Persona: All outward communications represent "Fulcrum Support", preserving Admin anonymity.
  3. No Automated Delivery: All actions generate draft links (wa.me & Gmail compose); Admin must manually review and press Send.
  4. Privacy & Consent: Resolves only authorized account contact details without exposing internal tokens or credentials.
  5. Audit Distinction: Distinguishes draft opening from confirmed manual transmission.
"""

import re
import uuid
import urllib.parse
from datetime import datetime, timezone
from typing import Optional, Dict, List, Tuple

from services.auth import get_supabase_admin_client, get_data_backend
from services.local_db import get_local_db
from services.governance import get_primary_admin_id


# ─────────────────────────────────────────────────────────────────────────────
# 1. AUTHORIZATION GATE
# ─────────────────────────────────────────────────────────────────────────────
def is_authorized_admin(user_id: Optional[str]) -> bool:
    """Verifies that the caller is the authorized single Platform Admin (fulcrumindia1@gmail.com)."""
    if not user_id:
        return False
    from services.roles import is_strict_admin
    if isinstance(user_id, dict):
        return is_strict_admin(user_dict=user_id)
    return is_strict_admin(user_id=str(user_id))


# ─────────────────────────────────────────────────────────────────────────────
# 2. PHONE & EMAIL NORMALIZATION & VALIDATION
# ─────────────────────────────────────────────────────────────────────────────
def normalize_phone_number(phone: Optional[str], default_country_code: str = "91") -> Tuple[Optional[str], Optional[str]]:
    """
    Sanitizes and normalizes a phone number to international E.164 digits-only format.
    Accepts formats like:
      - "+91 98765 43210" -> "919876543210"
      - "9876543210"      -> "919876543210" (defaults to India 91)
      - "09876543210"     -> "919876543210"
      - "+1 (555) 234-5678" -> "15552345678"
    Returns (normalized_digits, error_message).
    """
    if not phone or not isinstance(phone, str):
        return None, "Phone number is not provided."

    raw = phone.strip()
    if not raw:
        return None, "Phone number is empty."

    # Remove standard whitespace, hyphens, parentheses, dots
    cleaned = re.sub(r"[\s\-\(\)\.]+", "", raw)

    # Strip leading plus
    if cleaned.startswith("+"):
        cleaned = cleaned[1:]

    # Remove leading trunk zero if followed by 10 digits (common in India/UK)
    if cleaned.startswith("0") and len(cleaned) == 11:
        cleaned = cleaned[1:]

    # Digits only check
    if not cleaned.isdigit():
        return None, "Phone number contains invalid non-numeric characters."

    # If exactly 10 digits (standard Indian mobile starting with 6, 7, 8, or 9), prepend default country code
    if len(cleaned) == 10:
        if cleaned[0] in "6789":
            cleaned = f"{default_country_code}{cleaned}"
        else:
            cleaned = f"{default_country_code}{cleaned}"

    # E.164 length check: between 10 and 15 digits
    if len(cleaned) < 10 or len(cleaned) > 15:
        return None, f"Invalid phone length ({len(cleaned)} digits). Expected 10-15 digits."

    return cleaned, None


def validate_email_address(email: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    """Validates and trims an email address according to standard email RFC format."""
    if not email or not isinstance(email, str):
        return None, "Email address is not provided."

    clean = email.strip()
    if not clean:
        return None, "Email address is empty."

    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(pattern, clean):
        return None, "Invalid email address format."

    return clean, None


# ─────────────────────────────────────────────────────────────────────────────
# 3. SAFE URL GENERATION (WhatsApp & Gmail)
# ─────────────────────────────────────────────────────────────────────────────
def generate_whatsapp_url(phone: str, message: str) -> Optional[str]:
    """Generates a safe https://wa.me/ click-to-chat URL with URL-encoded prefilled text."""
    norm_phone, err = normalize_phone_number(phone)
    if not norm_phone or err:
        return None

    clean_msg = message.strip() if message else ""
    encoded_text = urllib.parse.quote(clean_msg)
    return f"https://wa.me/{norm_phone}?text={encoded_text}"


def generate_gmail_compose_url(email: str, subject: str, body: str) -> Optional[str]:
    """
    Generates a tested Gmail web compose deep link:
    https://mail.google.com/mail/?view=cm&fs=1&to=...&su=...&body=...
    Opens a draft in the Admin's signed-in Gmail account. Does NOT access recipient's inbox.
    """
    clean_email, err = validate_email_address(email)
    if not clean_email or err:
        return None

    encoded_to = urllib.parse.quote(clean_email)
    encoded_su = urllib.parse.quote(subject.strip() if subject else "")
    encoded_body = urllib.parse.quote(body.strip() if body else "")
    return f"https://mail.google.com/mail/?view=cm&fs=1&to={encoded_to}&su={encoded_su}&body={encoded_body}"


def generate_mailto_url(email: str, subject: str, body: str) -> Optional[str]:
    """Generates standard RFC 6068 mailto: URI as fallback for native email clients."""
    clean_email, err = validate_email_address(email)
    if not clean_email or err:
        return None

    encoded_su = urllib.parse.quote(subject.strip() if subject else "")
    encoded_body = urllib.parse.quote(body.strip() if body else "")
    return f"mailto:{clean_email}?subject={encoded_su}&body={encoded_body}"


# ─────────────────────────────────────────────────────────────────────────────
# 4. COURTEOUS MESSAGE TEMPLATES
# ─────────────────────────────────────────────────────────────────────────────
def get_guide_inactivity_template(guide_name: str, aspirant_name: str) -> Tuple[str, str]:
    """Returns (subject, message_body) for Guide caseload inactivity reminder."""
    clean_guide = guide_name.strip() if guide_name else "Guide"
    clean_asp = aspirant_name.strip() if aspirant_name else "the Entrepreneur"

    subject = f"Fulcrum Support — Gentle Follow-up on {clean_asp}'s Mentorship Case"
    body = (
        f"Dear {clean_guide},\n\n"
        "Greetings from Fulcrum Support.\n\n"
        "We hope you are doing well.\n\n"
        f"We kindly request you to review the mentorship case of {clean_asp} and check "
        "whether any guidance, consultation responses or follow-up actions are pending.\n\n"
        "Your valuable time and support are greatly appreciated.\n\n"
        "If you are experiencing any difficulty or require assistance, please let Fulcrum Support know.\n\n"
        "Thank you for your continued contribution.\n\n"
        "Warm regards,\n"
        "Fulcrum Support"
    )
    return subject, body


def get_sme_inactivity_template(sme_name: str, aspirant_name: str) -> Tuple[str, str]:
    """Returns (subject, message_body) for SME advisory caseload inactivity reminder."""
    clean_sme = sme_name.strip() if sme_name else "Specialist"
    clean_asp = aspirant_name.strip() if aspirant_name else "the Entrepreneur"

    subject = f"Fulcrum Support — Gentle Follow-up on {clean_asp}'s Advisory Case"
    body = (
        f"Dear {clean_sme},\n\n"
        "Greetings from Fulcrum Support.\n\n"
        "We hope you are doing well.\n\n"
        f"We kindly request you to review the advisory case of {clean_asp} and attend "
        "to any pending technical guidance or consultation requests when possible.\n\n"
        "Your expertise is valuable to the entrepreneur's progress.\n\n"
        "If additional information or assistance is required, please inform Fulcrum Support.\n\n"
        "Thank you for your support.\n\n"
        "Warm regards,\n"
        "Fulcrum Support"
    )
    return subject, body


ASPIRANT_PURPOSE_TEMPLATES: Dict[str, Dict[str, str]] = {
    "General check-in": {
        "subject": "Fulcrum Support — Checking In on Your Entrepreneurial Journey",
        "body": (
            "Dear {name},\n\n"
            "Greetings from Fulcrum Support.\n\n"
            "We hope you are doing well.\n\n"
            "We are reaching out to check on your entrepreneurial journey and whether you require "
            "any additional assistance, mentoring support or clarification regarding your Fulcrum experience.\n\n"
            "Please feel free to share any concerns or support requirements through your Fulcrum Dashboard.\n\n"
            "We appreciate your participation and wish you continued progress.\n\n"
            "Warm regards,\n"
            "Fulcrum Support"
        )
    },
    "Profile completion reminder": {
        "subject": "Fulcrum Support — Entrepreneur Profile Update Reminder",
        "body": (
            "Dear {name},\n\n"
            "Greetings from Fulcrum Support.\n\n"
            "We hope you are doing well.\n\n"
            "We noticed that a few details in your entrepreneur profile may still be incomplete. "
            "Completing your profile ensures our matching engine can accurately recommend relevant "
            "state and central government grant schemes for your venture.\n\n"
            "Please log in to your Fulcrum Dashboard to review and complete your profile when convenient.\n\n"
            "Warm regards,\n"
            "Fulcrum Support"
        )
    },
    "Mentorship follow-up": {
        "subject": "Fulcrum Support — Mentorship Progress Follow-up",
        "body": (
            "Dear {name},\n\n"
            "Greetings from Fulcrum Support.\n\n"
            "We are following up regarding your dedicated mentorship case. We want to ensure "
            "you are receiving the guidance and milestone direction needed for your venture.\n\n"
            "If you have any feedback or require assistance coordinating with your mentor, "
            "please let us know through your dashboard.\n\n"
            "Warm regards,\n"
            "Fulcrum Support"
        )
    },
    "Consultation follow-up": {
        "subject": "Fulcrum Support — Consultation Status Follow-up",
        "body": (
            "Dear {name},\n\n"
            "Greetings from Fulcrum Support.\n\n"
            "We are checking in regarding your recent consultation on Fulcrum. "
            "Please let us know if your query was addressed satisfactorily or if further "
            "specialized advisory is needed.\n\n"
            "You can continue the discussion or submit follow-up queries directly from your dashboard.\n\n"
            "Warm regards,\n"
            "Fulcrum Support"
        )
    },
    "Scheme guidance follow-up": {
        "subject": "Fulcrum Support — Government Scheme Guidance Follow-up",
        "body": (
            "Dear {name},\n\n"
            "Greetings from Fulcrum Support.\n\n"
            "We are checking in on your government scheme recommendations and applications. "
            "If you need any assistance understanding scheme guidelines, eligibility criteria, "
            "or documentation requirements, Fulcrum Support is here to help.\n\n"
            "Warm regards,\n"
            "Fulcrum Support"
        )
    },
    "Support request follow-up": {
        "subject": "Fulcrum Support — Support Inquiry Follow-up",
        "body": (
            "Dear {name},\n\n"
            "Greetings from Fulcrum Support.\n\n"
            "We are following up on your recent support inquiry to ensure your concern "
            "has been fully resolved.\n\n"
            "If you require any further assistance or clarification, please reach out via your Fulcrum Dashboard.\n\n"
            "Warm regards,\n"
            "Fulcrum Support"
        )
    }
}


def get_aspirant_contact_template(aspirant_name: str, purpose: str = "General check-in") -> Tuple[str, str]:
    """Generates courteous subject and body for contacting an Aspirant based on purpose."""
    clean_name = aspirant_name.strip() if aspirant_name else "Entrepreneur"
    data = ASPIRANT_PURPOSE_TEMPLATES.get(purpose) or ASPIRANT_PURPOSE_TEMPLATES["General check-in"]
    subject = data["subject"]
    body = data["body"].format(name=clean_name)
    return subject, body


# ─────────────────────────────────────────────────────────────────────────────
# 5. COMMUNICATION AUDIT & TRACKING
# ─────────────────────────────────────────────────────────────────────────────
def record_external_contact(
    admin_id: str,
    recipient_id: str,
    recipient_role: str,
    aspirant_id: str,
    channel: str,
    purpose: str = "General check-in",
    status: str = "SENT_CONFIRMED",
    inactivity_record_id: Optional[str] = None,
    notes: str = ""
) -> Tuple[bool, Optional[str]]:
    """
    Records an external communication tracking entry.
    Does NOT store private conversation content.
    Prevents duplicates from Streamlit reruns.
    """
    if not is_authorized_admin(admin_id):
        return False, "Unauthorized: Only the Platform Admin can record communication logs."

    if channel not in ("whatsapp", "email"):
        return False, f"Invalid channel: {channel}. Expected 'whatsapp' or 'email'."

    if recipient_role not in ("guide", "sme", "aspirant"):
        return False, f"Invalid recipient role: {recipient_role}."

    contact_id = str(uuid.uuid4())
    now_iso = datetime.now(timezone.utc).isoformat()

    record = {
        "id": contact_id,
        "admin_id": admin_id,
        "recipient_id": recipient_id,
        "recipient_role": recipient_role,
        "aspirant_id": aspirant_id,
        "inactivity_record_id": inactivity_record_id,
        "channel": channel,
        "purpose": purpose,
        "status": status,
        "notes": notes.strip() if notes else None,
        "created_at": now_iso
    }

    backend = get_data_backend()
    if backend == "supabase":
        admin_client = get_supabase_admin_client()
        if admin_client:
            try:
                admin_client.table("external_contact_logs").insert(record).execute()
            except Exception as e:
                print(f"[ExternalContact] Supabase insert note: {e}")

    # Local SQLite persistence
    db = get_local_db()
    if hasattr(db, "insert_external_contact_log"):
        db.insert_external_contact_log(record)

    # If linked to an inactivity record, update follow-up metadata on the inactivity log
    if inactivity_record_id:
        try:
            from services.inactivity import mark_inactivity_followup_sent
            mark_inactivity_followup_sent(inactivity_record_id, channel=channel, admin_id=admin_id, notes=notes)
        except Exception as e:
            print(f"[ExternalContact] Inactivity follow-up sync note: {e}")

    return True, contact_id


def list_external_contacts(
    recipient_id: Optional[str] = None,
    aspirant_id: Optional[str] = None,
    inactivity_record_id: Optional[str] = None,
    limit: int = 50
) -> List[Dict]:
    """Retrieves communication logs for an entity or inactivity alert."""
    backend = get_data_backend()
    records = []

    if backend == "supabase":
        admin_client = get_supabase_admin_client()
        if admin_client:
            try:
                q = admin_client.table("external_contact_logs").select("*").order("created_at", desc=True).limit(limit)
                if recipient_id:
                    q = q.eq("recipient_id", recipient_id)
                if aspirant_id:
                    q = q.eq("aspirant_id", aspirant_id)
                if inactivity_record_id:
                    q = q.eq("inactivity_record_id", inactivity_record_id)
                res = q.execute()
                records = res.data or []
            except Exception as e:
                print(f"[ExternalContact] Supabase query note: {e}")

    if not records:
        db = get_local_db()
        if hasattr(db, "list_external_contact_logs"):
            records = db.list_external_contact_logs(
                recipient_id=recipient_id,
                aspirant_id=aspirant_id,
                inactivity_record_id=inactivity_record_id,
                limit=limit
            )

    return records

