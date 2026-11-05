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
    "title": "Platform Terms of Service & User Agreement",
    "content": """# FULCRUM-INDIA
## PLATFORM TERMS OF SERVICE & USER AGREEMENT

**Version:** 1.0 — Legal Review Draft  
**Effective Date:** [DD Month YYYY]  
**Platform Operator:** [Full legally registered name of individual, proprietorship, partnership, LLP or company]  
**Registered / Principal Business Address:** [Full address, India]  
**Official Website:** [Verified website URL]  
**Legal Contact:** [legal@your-domain]  
**Grievance Contact:** [grievance@your-domain]

**IMPORTANT: THIS IS A DRAFT. It must be reviewed, completed and approved by qualified Indian legal counsel before being presented as the official agreement.**

### 1. INTRODUCTION AND ACCEPTANCE
1.1. Welcome to FULCRUM-INDIA ("FULCRUM", "Platform", "we", "us", or "our"), an entrepreneurship-support technology platform operated by the entity identified above ("Operator").
1.2. FULCRUM provides digital tools for entrepreneurial profile management, business mentoring coordination, scheme discovery, preliminary eligibility assessment, Guide and Subject Matter Expert collaboration, opportunity tracking and related services.
1.3. These Terms govern access to and use of the Platform by Aspirants, Guides, Subject Matter Experts ("SMEs"), institutional representatives and other authorized users ("Users").
1.4. By actively selecting the agreement checkbox and completing the acceptance action, a User acknowledges having had an opportunity to read these Terms and agrees to be bound by them, subject to applicable Indian law.
1.5. A User who does not agree must not proceed with account registration or restricted Platform services. Public legal notices and lawful grievance channels will remain accessible.
1.6. The Privacy Notice, applicable service-specific terms, published policies and role-specific agreements supplement these Terms. Where a conflict exists, mandatory applicable law prevails.

### 2. ELIGIBILITY AND AUTHORITY
2.1. Individual Users must be legally competent to enter into this agreement under applicable Indian law.
2.2. Accounts are intended for persons aged 18 years or above unless the Operator introduces a separately reviewed lawful process for other eligible users.
2.3. A User acting for a business, startup, institution or other organization represents that they have sufficient authority to provide information or undertake the specific actions they perform on its behalf.
2.4. Users must provide accurate registration information and maintain the security of their accounts.
2.5. Creating an account does not establish that a User's business is registered, government-recognized, investment-ready or eligible for any programme.

### 3. PLATFORM STATUS AND GOVERNMENT NON-AFFILIATION
3.1. FULCRUM is an independent technology and entrepreneurship-support platform.
3.2. Unless expressly stated with independently verifiable supporting authorization, FULCRUM is not a Government of India department, statutory authority, official government application portal, bank, financial institution, government scheme administrator or sanctioned intermediary.
3.3. References to central or state government schemes, grants, subsidies, loans, credit programmes, incubators or other opportunities are provided to assist discovery and informed decision-making.
3.4. Listing a programme does not imply government endorsement of FULCRUM or endorsement by FULCRUM of any third-party organization.
3.5. Users should independently consult official programme notifications and designated government portals before making applications or commitments.

### 4. SERVICES AND LIMITATIONS
4.1. The Platform may provide:
- Aspirant business profiles and entrepreneurial development records.
- Scheme discovery, filtering and preliminary matching.
- Guide assignment, mentoring coordination and recommendations.
- SME consultations and specialist input.
- Business-development journeys, milestones and progress tracking.
- Documents, notes, communications and support workflows.
- Other features expressly made available through the Platform.
4.2. Features, availability and access permissions may differ by user role, account status, service plan and applicable programme.
4.3. FULCRUM does not guarantee that a User will obtain funding, government approval, business registration, incubation, a loan, investor interest, commercial success or any specific financial benefit.
4.4. Any estimated eligibility, match percentage, recommendation rank, funding range or programme suitability indicator is an informational assessment unless expressly identified as a verified determination by the responsible issuing authority.
4.5. Automated or AI-assisted outputs may be incomplete, inaccurate or based on outdated or missing information. They must not be treated as final official decisions.

### 5. SCHEME MATCHING AND OFFICIAL ELIGIBILITY
5.1. Scheme matching may consider business sector, location, stage, registration status, funding purpose, support requirements and other information relevant to the applicable programme.
5.2. A high match score does not establish that every mandatory eligibility condition is met.
5.3. FULCRUM will distinguish, where supported by the actual service, between preliminary relevance, information requiring verification, Guide-reviewed recommendations and official application outcomes.
5.4. Scheme terms, funding availability, application deadlines and government requirements may change without advance notice to FULCRUM.
5.5. Users remain responsible for reviewing official notifications and submitting complete, truthful applications through authorized channels.
5.6. FULCRUM must not present a recommendation or a Guide's release of a scheme as official government approval.
5.7. If a discrepancy exists between information on FULCRUM and an official programme notification, the applicable official notification and issuing authority's decision govern programme eligibility.

### 6. USER INFORMATION, DOCUMENTS AND REPRESENTATIONS
6.1. Users must submit information that is accurate to the best of their knowledge and must correct material inaccuracies when discovered.
6.2. Users must not knowingly submit forged certificates, fabricated business records, false funding claims, manipulated ownership details or documents belonging to another person without lawful authorization.
6.3. Users are responsible for having the necessary rights and permissions to upload documents, business plans, financial information, intellectual property and personal data concerning third parties.
6.4. FULCRUM may seek reasonable clarification or supporting documentation before treating a claim as verified.
6.5. Where a programme lawfully requires information relating to ownership, enterprise size or an applicable eligibility category, that information should be requested only for the relevant stated purpose and handled under appropriate access controls.
6.6. Users must not assume that uploading a document constitutes submission to a government agency. Any official submission must be separately and clearly identified.

### 7. GUIDES, SMEs AND PROFESSIONAL RESPONSIBILITIES
7.1. Guides and SMEs assist with mentoring, programme interpretation and entrepreneurship-related support within their authorized roles.
7.2. Assignment of a Guide or SME does not, by itself, create an employment relationship, partnership, fiduciary relationship or professional-client relationship with the Platform Operator.
7.3. Guides and SMEs must disclose material conflicts of interest and must not misrepresent their credentials, government affiliations, experience or authority.
7.4. Guides and SMEs must not demand unauthorized payments, commissions, gifts or preferential treatment in exchange for recommendations, introductions or scheme releases.
7.5. Advice requiring a legally regulated professional qualification—including certain legal, accounting, financial or investment activities—must be provided only by appropriately qualified and authorized professionals.
7.6. Guides and SMEs must access and use Aspirant information only for authorized Platform purposes. Separate role-specific confidentiality, conflict-of-interest and service agreements may apply.
7.7. FULCRUM may investigate credible complaints of misconduct and take proportionate action in accordance with applicable law, published policies and appropriate review procedures.

### 8. PAYMENTS AND CHARGES
8.1. FULCRUM will disclose any applicable Platform subscription, service charge or optional paid service before a User commits to payment.
8.2. No government grant, subsidy or sanctioned financial benefit is guaranteed in exchange for a Platform payment.
8.3. Government application fees, statutory charges or independent professional fees, where applicable, must be clearly identified and must not be misrepresented as mandatory FULCRUM charges.
8.4. Payment terms, applicable taxes, invoices, cancellation procedures and refund eligibility must be stated in a separate published Pricing, Cancellation and Refund Policy before paid services are activated.
8.5. Users must not be enrolled in paid subscriptions or automatic renewals without appropriate disclosure and authorization.
8.6. Nothing in these Terms excludes refunds, remedies or other rights available under mandatory consumer law.

### 9. CONFIDENTIAL BUSINESS INFORMATION
9.1. Aspirants may provide business ideas, financial projections, product concepts, operational plans, customer information and other confidential information.
9.2. FULCRUM will restrict access to such information according to the service's documented permissions, security controls and authorized operational needs.
9.3. A User who receives another User's nonpublic information through an authorized collaboration must not disclose, exploit or redistribute it without appropriate permission or another lawful basis.
9.4. Users should not upload trade secrets or other highly sensitive materials unless the relevant service genuinely requires them and appropriate protections are available.
9.5. The Platform's confidentiality obligations and limitations must be described accurately in the Privacy Notice and any separate written confidentiality agreement.
9.6. This clause does not prevent lawful disclosure to competent authorities, compliance with binding legal process, or reporting suspected unlawful conduct.

### 10. INTELLECTUAL PROPERTY
10.1. FULCRUM's original platform software, branding, interface designs, documentation and other Operator-owned materials remain the intellectual property of the Operator or applicable licensors.
10.2. Users retain the rights they lawfully possess in their business plans, uploaded documents, inventions, trademarks and other independently created material.
10.3. By uploading authorized content, Users grant the Operator a limited, nonexclusive licence to store, process, reproduce and display that content only to the extent reasonably necessary to provide the requested services, administer authorized collaboration, maintain security and comply with applicable law.
10.4. Uploading a business idea does not transfer ownership of that idea or create a right for FULCRUM, a Guide or an SME to commercialize it.
10.5. Nothing in these Terms grants Users ownership of the Platform's source code, trademarks or proprietary databases.
10.6. Intellectual-property rights between collaborating Users or between an Aspirant and an SME must be governed by a separate written agreement where necessary.

### 11. PRIVACY AND DATA PROTECTION
11.1. Personal-data processing is described in FULCRUM's separate Privacy Notice.
11.2. The Privacy Notice must explain, as applicable, the categories of personal data collected, specific purposes of processing, relevant recipients and service providers, retention practices, security measures, contact mechanisms and available individual rights.
11.3. Access to Aspirant information by Guides, SMEs, administrators and service providers must be governed by role-based authorization and legitimate operational requirements.
11.4. The Operator must provide required notices and obtain any necessary consent or other lawful authorization in accordance with applicable law and the commencement status of relevant statutory provisions.
11.5. Users must have access to the data-related rights and grievance procedures applicable to their circumstances under prevailing law.
11.6. FULCRUM will not treat acceptance of these Terms as unrestricted permission for unrelated marketing, unnecessary sharing of confidential business information or processing requiring a separate consent.
11.7. Users should consult the published Privacy Notice for information on account closure, access requests, correction, withdrawal of applicable consents and deletion requests.

### 12. ACCEPTABLE USE AND PROHIBITED CONDUCT
Users must not:
a. Impersonate another person, enterprise, government employee, regulator, Guide or SME.
b. Submit fraudulent applications, forged records or misleading declarations.
c. Offer or solicit bribes, kickbacks, unlawful commissions or other improper advantages.
d. Attempt unauthorized access to accounts, records, private notes, databases or administrator functions.
e. Scrape restricted records, harvest personal information or circumvent access controls.
f. Upload malware or use the Platform to facilitate fraud, phishing or unlawful activity.
g. Harass, threaten, intimidate or unlawfully discriminate against other Users.
h. Misrepresent Platform recommendations as government-issued approvals.
i. Publish content that violates applicable law or infringes another person's rights.
j. Misuse Guide or SME communications for unauthorized solicitation or exploitation.

### 13. THIRD-PARTY SERVICES
13.1. The Platform may link to official government websites, external programme portals, payment processors, authentication providers or third-party resources.
13.2. Such services may operate under their own terms and privacy policies.
13.3. FULCRUM does not control decisions by government authorities, banks, investors, incubators or unrelated external organizations.
13.4. The Operator remains responsible for its own legal obligations and cannot avoid responsibility for its own unlawful conduct merely because a third-party provider is involved.

### 14. ACCOUNT RESTRICTION AND TERMINATION
14.1. Users may request account closure through the available account controls or designated support channel.
14.2. FULCRUM may restrict or suspend access for reasonably supported concerns involving fraud, serious security risks, unlawful activity, misuse of confidential information or material violations of these Terms.
14.3. Where reasonably possible and legally appropriate, Users will receive notice and an opportunity to seek review of adverse account actions.
14.4. Immediate restrictions may be necessary to address credible security or safety threats.
14.5. Account closure, data deletion and legally required retention will be handled under the published Privacy Notice and applicable law.
14.6. A User's termination does not extinguish accrued payment obligations, valid intellectual-property rights, lawful claims or other provisions that reasonably survive termination.

### 15. SERVICE AVAILABILITY AND WARRANTIES
15.1. FULCRUM aims to operate the Platform with reasonable care and skill.
15.2. Availability may be affected by maintenance, connectivity problems, third-party outages, security incidents or technical failures.
15.3. The Operator does not guarantee uninterrupted access, error-free automated recommendations or successful business outcomes.
15.4. Any warranty disclaimer applies only to the extent permitted by applicable law and does not exclude a statutory guarantee or consumer remedy that cannot lawfully be waived.

### 16. LIMITATION OF LIABILITY
16.1. Each party remains responsible for its own unlawful acts, fraud, deliberate misconduct and other liabilities that cannot be lawfully excluded.
16.2. FULCRUM is not responsible solely because an independent authority rejects an application, modifies scheme conditions, withdraws funding or makes a decision outside the Operator's control.
16.3. Users acknowledge that entrepreneurship and funding decisions involve commercial risk and require independent professional assessment where appropriate.
16.4. Any contractual financial liability limitation must be separately assessed for fairness, enforceability and the nature of the service actually offered.
16.5. Nothing in these Terms limits rights or remedies that applicable Indian law does not permit the parties to exclude.

### 17. COMPLAINTS AND GRIEVANCE REDRESSAL
17.1. Complaints concerning account access, information accuracy, service quality, unauthorized charges, misuse of data or User conduct may be submitted through:
Grievance Officer: [Full name/designation]
Email: [Verified grievance email]
Contact Address: [Verified Indian address]
Online Complaint Form: [URL]
17.2. The Operator will acknowledge, process and resolve grievances within the timelines required by the laws and rules applicable to the relevant complaint and to the Platform's classification.
17.3. Where applicable law provides a statutory grievance escalation or appellate mechanism, Users may exercise that right.
17.4. Nothing in these Terms prevents a person from approaching an appropriate government authority, consumer commission, regulator, court or law-enforcement agency.

### 18. CHANGES TO THESE TERMS
18.1. FULCRUM may amend these Terms for lawful operational, security, service or regulatory reasons.
18.2. Material changes will be communicated appropriately, including advance notice where required by law or reasonably practicable.
18.3. If legally required, the Operator will obtain fresh acceptance or consent before applying material changes.
18.4. Updated versions will identify the version number, effective date and a means of reviewing the terms.
18.5. Changes will not retrospectively extinguish rights already accrued under mandatory law.

### 19. GOVERNING LAW AND DISPUTES
19.1. These Terms are governed by the laws of India.
19.2. Users are encouraged to raise service-related disputes through the Platform's designated grievance channel before commencing formal proceedings, where appropriate.
19.3. Parties may explore good-faith negotiation or voluntary mediation without restricting access to mandatory statutory remedies.
19.4. Subject to applicable law and the jurisdiction of competent consumer, statutory or other designated forums, disputes may be brought before competent courts at [Verified Indian city and state] where a valid jurisdiction agreement is legally permissible.
19.5. No provision of these Terms shall be construed to remove a consumer's non-waivable statutory rights or to restrict a remedy that applicable law requires to remain available.

### 20. SEVERABILITY AND ENTIRE AGREEMENT
20.1. If a particular provision is held unenforceable, the remaining provisions continue to apply insofar as they can operate lawfully and consistently with the parties' underlying agreement.
20.2. Failure to enforce one provision does not automatically waive the Operator's right to enforce other lawful provisions.
20.3. These Terms, together with the applicable policies and role-specific agreements expressly incorporated by reference, describe the contractual basis for the services concerned.
20.4. A User's acceptance does not constitute an acknowledgment that every Platform-generated recommendation is correct or that any government authority has approved the User's application.

### ELECTRONIC ACCEPTANCE DECLARATION
By selecting the required acceptance checkbox and clicking "I Agree & Continue", I confirm that:
1. I have been given access to the complete FULCRUM-INDIA Platform Terms of Service.
2. I have had an opportunity to read them and understand the nature of the Platform.
3. I am legally competent to accept these Terms, or I possess the necessary legal authority to act for the organization represented.
4. I understand that FULCRUM is not an official government scheme approval authority unless separately identified with verifiable authorization.
5. I understand that scheme recommendations and eligibility estimates do not guarantee funding or approval.
6. I agree to provide accurate information and use the Platform lawfully.
7. I accept these Terms voluntarily.""",
    "effective_date": "2026-11-01",
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

    if not doc or len(doc.get("content", "")) < 500:
        db = get_local_db()
        if hasattr(db, "get_legal_document"):
            doc = db.get_legal_document(doc_type)

    if not doc or len(doc.get("content", "")) < 500:
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

