"""
views/legal_ui.py — Mandatory Terms & Conditions and Non-Disclosure Agreement Gatekeeper
========================================================================================
Presents unskippable legal screens when:
1. User has not yet accepted Platform Terms & Conditions.
2. User with a promoted Guide or SME role has not yet executed the binding NDA.
"""

import streamlit as st
import html
from services.legal import (
    get_active_legal_document,
    check_user_terms_accepted,
    check_user_nda_accepted,
    record_legal_acceptance
)


def render_terms_and_conditions_gate(user: dict) -> bool:
    """
    Checks if user has accepted the mandatory platform terms.
    If not, renders an unskippable terms agreement screen.
    Returns True if already accepted, False if blocking.
    """
    user_id = user.get("id")
    if not user_id:
        return True

    if check_user_terms_accepted(user_id):
        return True

    doc = get_active_legal_document("terms_and_conditions")
    if not doc or len(doc.get("content", "")) < 500:
        from services.legal import DEFAULT_TERMS_DOC
        doc = DEFAULT_TERMS_DOC
    doc_title = doc.get("title", "Fulcrum-India Platform Terms & Conditions")
    doc_content = doc.get("content", "")
    doc_version = doc.get("version", "1.0.0")

    st.markdown("""
    <div style="max-width:760px; margin: 1.5rem auto 1rem; background:#FFFFFF; border:1px solid #E2E8F0; border-top:4px solid #3B82F6; border-radius:14px; padding:2rem; box-shadow:0 4px 14px rgba(0,0,0,0.06);">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:1rem;">
            <div style="font-size:2rem;">📜</div>
            <div>
                <h2 style="margin:0; font-size:1.35rem; color:#0F172A;">Platform Terms & Conditions Required</h2>
                <div style="color:#64748B; font-size:0.85rem; margin-top:2px;">Version {version} — Institutional Governance & Data Integrity Standards</div>
            </div>
        </div>
        <p style="color:#334155; font-size:0.92rem; line-height:1.5;">
            Welcome to Fulcrum-India. Prior to accessing entrepreneur services, mentorship dossiers, or scheme matching, please review and accept the official platform terms.
        </p>
    </div>
    """.format(version=doc_version), unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        with st.container(border=True):
            clean_content = doc_content.replace("\\n", "\n")
            with st.container(height=320):
                st.markdown(clean_content)

            with st.form("form_accept_terms"):
                st.markdown("#### Formal Agreement Confirmation")
                full_name_input = st.text_input("Full Legal Name *", value=user.get("full_name", ""), help="Must match your government identity")
                phrase_input = st.text_input("Type 'I ACCEPT' in capital letters *", placeholder="I ACCEPT", help="Type the exact phrase I ACCEPT to legally confirm")
                cb = st.checkbox("I confirm that I have read, understood, and agree to be bound by the Fulcrum-India Terms & Conditions.", value=False)

                if st.form_submit_button("ACCEPT TERMS & PROCEED TO WORKSPACE", type="primary", use_container_width=True):
                    if not cb:
                        st.error("You must check the confirmation checkbox.")
                    elif phrase_input.strip().upper() != "I ACCEPT":
                        st.error("You must type 'I ACCEPT' exactly.")
                    elif not full_name_input.strip() or len(full_name_input.strip()) < 3:
                        st.error("Please enter your full legal name.")
                    else:
                        ok, err = record_legal_acceptance(
                            user_id=user_id,
                            user_email=user.get("email", ""),
                            doc_type="terms_and_conditions",
                            typed_name=full_name_input.strip(),
                            typed_phrase=phrase_input.strip().upper(),
                            checkbox_confirmed=True
                        )
                        if ok:
                            st.success("Terms accepted successfully! Entering Fulcrum workspace...")
                            st.rerun()
                        else:
                            st.error(err or "Failed to record acceptance.")

    return False


def render_nda_gate(user: dict, role: str) -> bool:
    """
    Checks if a Guide or SME has executed the mandatory NDA.
    If not, renders the mandatory Non-Disclosure Agreement screen.
    Returns True if accepted, False if blocking.
    """
    user_id = user.get("id")
    if not user_id or role not in ("guide", "sme"):
        return True

    if check_user_nda_accepted(user_id, role):
        return True

    doc = get_active_legal_document("nda_dual")
    if not doc or len(doc.get("content", "")) < 500:
        from services.legal import DEFAULT_NDA_DOC
        doc = DEFAULT_NDA_DOC
    doc_title = doc.get("title", "Fulcrum-India Confidentiality & Non-Disclosure Agreement")
    doc_content = doc.get("content", "")
    doc_version = doc.get("version", "1.0.0")

    role_title = "Certified Guide" if role == "guide" else "Domain Subject Matter Expert (SME)"

    st.markdown("""
    <div style="max-width:760px; margin: 1.5rem auto 1rem; background:#FFFFFF; border:1px solid #E2E8F0; border-top:4px solid #10B981; border-radius:14px; padding:2rem; box-shadow:0 4px 14px rgba(0,0,0,0.06);">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:1rem;">
            <div style="font-size:2rem;">🔐</div>
            <div>
                <h2 style="margin:0; font-size:1.35rem; color:#0F172A;">Mandatory Non-Disclosure Agreement (NDA) Execution</h2>
                <div style="color:#059669; font-size:0.85rem; font-weight:600; margin-top:2px;">Role: {role_title} · Version {version}</div>
            </div>
        </div>
        <p style="color:#334155; font-size:0.92rem; line-height:1.5;">
            As an institutional mentor, you will have access to sensitive entrepreneur business models, financial data, intellectual property, and government scheme applications. Execution of this binding Non-Disclosure Agreement is mandatory before accessing your caseload.
        </p>
    </div>
    """.format(role_title=role_title, version=doc_version), unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        with st.container(border=True):
            clean_nda_content = doc_content.replace("\\n", "\n")
            with st.container(height=260):
                st.markdown(clean_nda_content)

            with st.form(f"form_sign_nda_{role}"):
                st.markdown("#### Digital Signature & Confidentiality Pledge")
                legal_name = st.text_input("Confirmed Full Legal Name *", value=user.get("full_name", ""), help="Must match your official credentials")
                phrase = st.text_input("Type 'I ACCEPT' to bind this Non-Disclosure Agreement *", placeholder="I ACCEPT")
                cb = st.checkbox("I agree to keep all entrepreneur venture data, financial information, trade secrets, and journey events strictly confidential.", value=False)

                if st.form_submit_button("✍️ DIGITALLY SIGN NDA & ACTIVATE MENTOR WORKSPACE", type="primary", use_container_width=True):
                    if not cb:
                        st.error("You must check the confirmation checkbox.")
                    elif phrase.strip().upper() != "I ACCEPT":
                        st.error("You must type 'I ACCEPT' in capital letters.")
                    elif not legal_name.strip() or len(legal_name.strip()) < 3:
                        st.error("Please enter your full legal name.")
                    else:
                        ok, err = record_legal_acceptance(
                            user_id=user_id,
                            user_email=user.get("email", ""),
                            doc_type="nda_dual",
                            typed_name=legal_name.strip(),
                            typed_phrase=phrase.strip().upper(),
                            checkbox_confirmed=True
                        )
                        if ok:
                            st.success(f"Non-Disclosure Agreement signed successfully! {role_title} workspace activated.")
                            st.rerun()
                        else:
                            st.error(err or "Failed to record NDA signature.")

    return False

