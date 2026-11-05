"""
views/admin_governance.py — Admin Governance, Multi-Role, Legal Audit & Inactivity Panels
========================================================================================
Implements the 5 new administrative oversight consoles:
1. Multi-Role Management & Grants (One Identity, Multiple Roles)
2. Legal Documents & Mandatory NDA Signature Audit Trail
3. Confidential Guide Complaints & Reassignment Review
4. Caseload Inactivity Monitor (Day 7, 10, 14 Idempotent Alerts)
5. SME Directory & Conflict of Interest Governance
"""

import streamlit as st
import html
import textwrap
from datetime import datetime
from services.roles import (
    list_users_with_multi_roles,
    grant_role,
    revoke_role,
    suspend_role,
    activate_role
)
from services.legal import (
    list_legal_acceptances,
    get_active_legal_document
)
from services.governance import (
    list_guide_complaints,
    resolve_guide_complaint,
    list_sme_conflicts
)
from services.inactivity import (
    list_inactivity_records,
    check_and_process_caseload_inactivity
)
from services.profiles import list_profiles_by_role, get_profile


def _safe(v, default="—"):
    if v is None:
        return default
    return html.escape(str(v))


# ─────────────────────────────────────────────────────────────────────────────
# 1. MULTI-ROLE MANAGEMENT & ROLE GRANTS
# ─────────────────────────────────────────────────────────────────────────────
def render_admin_role_grants_tab(admin_id: str):
    st.subheader("🔑 Multi-Role Grants & Identity Architecture")
    st.caption("Manage user identity permissions. Fulcrum supports one person holding multiple roles under the same login credentials.")

    users = list_users_with_multi_roles()
    search_q = st.text_input("🔍 Search user by name or email", placeholder="Type user name or email...", key="adm_role_search")
    if search_q.strip():
        users = [u for u in users if search_q.lower() in u["full_name"].lower() or search_q.lower() in u["email"].lower()]

    col_g1, col_g2 = st.columns([2, 1])

    with col_g1:
        st.markdown(f"#### Active Roster ({len(users)} Users)")
        for u in users:
            uid = u["id"]
            active_badges = " ".join([f"<span style='background:#10B981; color:#fff; padding:2px 8px; border-radius:10px; font-size:0.75rem; font-weight:700;'>{r.upper()}</span>" for r in u["active_roles"]])
            pending_badges = " ".join([f"<span style='background:#F59E0B; color:#fff; padding:2px 8px; border-radius:10px; font-size:0.75rem; font-weight:700;'>PENDING NDA: {r.upper()}</span>" for r in u["pending_nda_roles"]])
            revoked_badges = " ".join([f"<span style='background:#EF4444; color:#fff; padding:2px 8px; border-radius:10px; font-size:0.75rem; font-weight:700;'>REVOKED: {r.upper()}</span>" for r in u["revoked_roles"]])

            st.markdown(textwrap.dedent(f"""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:1rem; margin-bottom:0.75rem; box-shadow:0 1px 3px rgba(0,0,0,0.03);">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-weight:700; font-size:1rem; color:#0F172A;">{_safe(u['full_name'])}</div>
                        <div style="font-size:0.8rem; color:#64748B;">{_safe(u['email'])} · 📍 {_safe(u['district'])}</div>
                    </div>
                    <div>
                        {active_badges} {pending_badges} {revoked_badges}
                    </div>
                </div>
            </div>
            """).strip(), unsafe_allow_html=True)

    with col_g2:
        st.markdown("#### Grant Additional Role")
        with st.form("form_grant_additional_role"):
            user_options = {u["id"]: f"{u['full_name']} ({u['email']})" for u in users}
            sel_user_id = st.selectbox("Select User", list(user_options.keys()), format_func=lambda x: user_options[x], key="sel_user_grant")
            new_role = st.selectbox("Role to Grant", ["guide", "sme", "admin", "district_admin", "operational_admin"], format_func=lambda x: x.replace('_', ' ').title(), key="sel_new_role")
            
            st.info("ℹ️ Promoting to Guide or SME sets status to **PENDING NDA**. The user will be required to sign the binding NDA before accessing protected caseloads.")
            
            submit_grant = st.form_submit_button("Grant Role Grant", type="primary")
            if submit_grant:
                ok, err = grant_role(sel_user_id, new_role, granted_by=admin_id)
                if ok:
                    st.success(f"Role '{new_role.upper()}' granted! Status set to PENDING NDA.")
                    st.rerun()
                else:
                    st.error(err or "Failed to grant role.")

        st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
        st.markdown("#### Revoke or Suspend Role")
        with st.form("form_revoke_role"):
            sel_rev_user = st.selectbox("Select User", list(user_options.keys()), format_func=lambda x: user_options[x], key="sel_rev_user")
            sel_target_user = next((u for u in users if u["id"] == sel_rev_user), None)
            revokable_roles = [r for r in (sel_target_user["active_roles"] if sel_target_user else []) if r != "aspirant"]
            
            if not revokable_roles:
                st.caption("This user holds only the base Aspirant role (cannot be revoked).")
                submit_rev = st.form_submit_button("Revoke Role", disabled=True)
            else:
                sel_rev_role = st.selectbox("Select Role to Revoke", revokable_roles, key="sel_rev_role")
                rev_reason = st.text_input("Reason for Revocation *", placeholder="e.g. Inactivity, ethics breach, caseload rotation")
                submit_rev = st.form_submit_button("Revoke Role Immediately", type="secondary")
                if submit_rev:
                    if not rev_reason.strip():
                        st.warning("Please enter a revocation reason.")
                    else:
                        ok, err = revoke_role(sel_rev_user, sel_rev_role, reason=rev_reason.strip(), revoked_by=admin_id)
                        if ok:
                            st.success(f"Role '{sel_rev_role.upper()}' revoked.")
                            st.rerun()
                        else:
                            st.error(err or "Failed to revoke role.")


# ─────────────────────────────────────────────────────────────────────────────
# 2. LEGAL DOCUMENTS & NDA ACCEPTANCE AUDIT TRAIL
# ─────────────────────────────────────────────────────────────────────────────
def render_admin_legal_records_tab():
    st.subheader("📜 Legal Agreements & NDA Signature Audit Trail")
    st.caption("Cryptographic audit logs of all user acceptances for platform Terms & Conditions and mentor Non-Disclosure Agreements.")

    doc_filter = st.selectbox("Filter Document Type", ["ALL", "terms_and_conditions", "nda_dual", "nda_guide", "nda_sme"])
    records = list_legal_acceptances(doc_type=None if doc_filter == "ALL" else doc_filter)

    st.markdown(f"**Total Signed Legal Acceptances Recorded:** {len(records)}")

    if not records:
        st.info("No legal acceptance records match the selected filter.")
    else:
        for r in records:
            roles_cov = r.get("roles_covered") or []
            roles_str = ", ".join(roles_cov) if isinstance(roles_cov, list) else str(roles_cov)
            hash_display = (r.get("doc_hash") or "")[:16] + "..."

            st.markdown(textwrap.dedent(f"""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-left:4px solid #10B981; border-radius:10px; padding:1rem; margin-bottom:0.75rem; box-shadow:0 1px 3px rgba(0,0,0,0.03);">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <div style="font-weight:700; font-size:0.95rem; color:#0F172A;">{_safe(r.get('typed_legal_name'))} <span style="font-weight:400; color:#64748B;">({_safe(r.get('user_email_snapshot'))})</span></div>
                        <div style="font-size:0.8rem; color:#059669; font-weight:600; margin-top:2px;">Document: {_safe(r.get('doc_type'))} · v{_safe(r.get('doc_version'))} · Roles: {_safe(roles_str)}</div>
                        <div style="font-size:0.75rem; color:#64748B; margin-top:4px;">Signature Phrase: <strong>"{_safe(r.get('typed_acceptance_phrase'))}"</strong> · Hash: <code>{hash_display}</code></div>
                    </div>
                    <div style="text-align:right;">
                        <span style="background:#DEF7EC; color:#03543F; font-size:0.75rem; font-weight:700; padding:2px 8px; border-radius:10px;">BINDING & VERIFIED</span>
                        <div style="font-size:0.72rem; color:#94A3B8; margin-top:4px;">{_safe(r.get('accepted_at', '')[:19].replace('T', ' '))}</div>
                        <div style="font-size:0.7rem; color:#94A3B8;">IP: {_safe(r.get('ip_address'))}</div>
                    </div>
                </div>
            </div>
            """).strip(), unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 3. CONFIDENTIAL GUIDE COMPLAINTS & REASSIGNMENT REVIEW
# ─────────────────────────────────────────────────────────────────────────────
def render_admin_complaints_tab(admin_id: str):
    st.subheader("🛡️ Confidential Mentor Complaints & Reassignment Requests")
    st.caption("Confidential reports submitted by entrepreneurs regarding Guide engagement, inactivity, or conflicts. Visible strictly to Administration.")

    complaints = list_guide_complaints()

    c_cnt_pending = sum(1 for c in complaints if c.get("status") == "PENDING")
    c_cnt_resolved = sum(1 for c in complaints if c.get("status") == "RESOLVED")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Complaints", len(complaints))
    c2.metric("Pending Review", c_cnt_pending)
    c3.metric("Resolved", c_cnt_resolved)

    if not complaints:
        st.info("No confidential mentor complaints filed.")
    else:
        for c in complaints:
            cid = c["id"]
            asp = get_profile(c.get("aspirant_id", "")) or {}
            guide = get_profile(c.get("guide_id", "")) or {}
            status = c.get("status", "PENDING")

            status_color = "#F59E0B" if status == "PENDING" else ("#3B82F6" if status == "UNDER_REVIEW" else "#10B981")

            with st.expander(f"Report: {asp.get('full_name', 'Founder')} on {guide.get('full_name', 'Guide')} [{status}]", expanded=(status == "PENDING")):
                st.markdown(textwrap.dedent(f"""
                <div style="margin-bottom:0.75rem;">
                    <p style="margin:0; font-size:0.9rem;"><strong>Entrepreneur:</strong> {asp.get('full_name')} ({asp.get('email')})</p>
                    <p style="margin:0; font-size:0.9rem;"><strong>Assigned Guide:</strong> {guide.get('full_name')} ({guide.get('email')})</p>
                    <p style="margin:0; font-size:0.9rem;"><strong>Report Reason:</strong> <span style="font-weight:700; color:#DC2626;">{c.get('reason', '').replace('_', ' ').title()}</span></p>
                    <p style="margin:0; font-size:0.85rem; color:#64748B;">Submitted At: {c.get('created_at', '')[:19].replace('T', ' ')}</p>
                </div>
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:0.85rem; margin-bottom:1rem; font-size:0.9rem; color:#1E293B;">
                    <strong>Entrepreneur Statement:</strong><br/>
                    {_safe(c.get('details'))}
                </div>
                """).strip(), unsafe_allow_html=True)

                if c.get("resolution_notes"):
                    st.info(f"Resolution Notes: {c.get('resolution_notes')}")

                if status in ("PENDING", "UNDER_REVIEW"):
                    with st.form(f"form_resolve_comp_{cid}"):
                        res_status = st.selectbox("Update Status", ["UNDER_REVIEW", "RESOLVED", "DISMISSED"], key=f"res_stat_{cid}")
                        res_notes = st.text_area("Administrative Resolution Notes *", placeholder="Describe action taken (e.g. Mentor cautioned, reassignment initiated)...", key=f"res_note_{cid}")
                        if st.form_submit_button("Submit Administrative Decision", type="primary"):
                            if not res_notes.strip():
                                st.warning("Please enter resolution notes.")
                            else:
                                ok, err = resolve_guide_complaint(cid, res_status, res_notes.strip(), admin_id)
                                if ok:
                                    st.success("Decision recorded.")
                                    st.rerun()
                                else:
                                    st.error(err or "Failed to record decision.")


# ─────────────────────────────────────────────────────────────────────────────
# 4. CASELOAD INACTIVITY MONITOR (DAY 7, 10, 14 ALERTS)
# ─────────────────────────────────────────────────────────────────────────────
def render_admin_inactivity_tab():
    st.subheader("⏱️ Mentor Caseload Inactivity Monitor")
    st.caption("Automated tracking of mentor engagement. Scans elapsed time since last interaction and logs idempotent alerts.")

    c_btn1, c_btn2 = st.columns([1, 2])
    with c_btn1:
        if st.button("🚀 Run Caseload Inactivity Scan Now", type="primary", use_container_width=True):
            alerts = check_and_process_caseload_inactivity()
            st.success(f"Scan complete! {len(alerts)} new inactivity notifications triggered.")
            st.rerun()

    records = list_inactivity_records()
    st.markdown(f"**Inactivity Escalation Log Records:** {len(records)}")

    if not records:
        st.info("No inactivity escalation records logged yet. Run a scan to check all active caseloads.")
    else:
        for r in records:
            guide = get_profile(r.get("guide_id", "")) or {}
            asp = get_profile(r.get("aspirant_id", "")) or {}
            stage = r.get("escalation_stage", "")
            days = r.get("days_inactive", 0)

            badge_color = "#F59E0B" if "DAY_7" in stage else ("#DC2626" if "DAY_14" in stage else "#E11D48")

            st.markdown(textwrap.dedent(f"""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-left:4px solid {badge_color}; border-radius:10px; padding:0.9rem; margin-bottom:0.6rem;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="font-weight:700; color:#0F172A;">{guide.get('full_name', 'Guide')}</span>
                        <span style="color:#64748B;"> ➔ </span>
                        <span style="font-weight:700; color:#0F172A;">{asp.get('full_name', 'Entrepreneur')}</span>
                        <div style="font-size:0.8rem; color:#64748B; margin-top:2px;">Inactive for <strong>{days} days</strong> · Stage: <code>{stage}</code></div>
                    </div>
                    <div style="text-align:right;">
                        <span style="background:{badge_color}; color:#fff; font-size:0.75rem; font-weight:700; padding:2px 8px; border-radius:8px;">{stage.replace('_', ' ')}</span>
                        <div style="font-size:0.7rem; color:#94A3B8; margin-top:4px;">Notified: {r.get('notification_sent_at', '')[:16].replace('T', ' ')}</div>
                    </div>
                </div>
            </div>
            """).strip(), unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 5. SME DIRECTORY & CONFLICT OF INTEREST GOVERNANCE
# ─────────────────────────────────────────────────────────────────────────────
def render_admin_sme_conflicts_tab(admin_id: str):
    st.subheader("⚖️ Subject Matter Expert (SME) Directory & Conflict Governance")
    st.caption("Domain specialist credentials and mandatory conflict-of-interest declarations.")

    smes = list_profiles_by_role("sme")
    conflicts = list_sme_conflicts()

    tab_dir, tab_conf = st.tabs([f"🔬 SME Directory ({len(smes)})", f"⚠️ Conflict Declarations ({len(conflicts)})"])

    with tab_dir:
        for s in smes:
            p_data = s.get("profile_data", {})
            st.markdown(f"""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:1rem; margin-bottom:0.75rem;">
                <div style="font-weight:700; font-size:1.05rem; color:#0F172A;">{_safe(s.get('full_name'))}</div>
                <div style="color:#2563EB; font-size:0.82rem; font-weight:600;">{_safe(p_data.get('expertise', 'Specialist'))} · {_safe(p_data.get('industry', 'Domain Advisory'))}</div>
                <div style="font-size:0.8rem; color:#64748B; margin-top:2px;">Email: {_safe(s.get('email'))} · Phone: {_safe(s.get('phone', '—'))} · District: {_safe(s.get('district', 'Tamil Nadu'))}</div>
            </div>
            """, unsafe_allow_html=True)

    with tab_conf:
        if not conflicts:
            st.info("No conflict of interest declarations on record.")
        else:
            for c in conflicts:
                sme_p = get_profile(c.get("sme_id", "")) or {}
                asp_p = get_profile(c.get("aspirant_id", "")) or {}
                has_conf = c.get("has_conflict", False)

                color = "#DC2626" if has_conf else "#10B981"
                text = "CONFLICT DECLARED" if has_conf else "CLEARED / NO CONFLICT"

                st.markdown(f"""
                <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-left:4px solid {color}; border-radius:10px; padding:0.9rem; margin-bottom:0.75rem;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <span style="font-weight:700; color:#0F172A;">{sme_p.get('full_name', 'SME')}</span> ➔ <span style="font-weight:700; color:#0F172A;">{asp_p.get('full_name', 'Aspirant')}</span>
                            <div style="font-size:0.85rem; color:#334155; margin-top:4px;">{_safe(c.get('conflict_details'))}</div>
                        </div>
                        <div style="text-align:right;">
                            <span style="background:{color}; color:#fff; font-size:0.75rem; font-weight:700; padding:2px 8px; border-radius:8px;">{text}</span>
                            <div style="font-size:0.7rem; color:#94A3B8; margin-top:4px;">Declared: {c.get('created_at', '')[:16].replace('T', ' ')}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

