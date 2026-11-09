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
    reinstate_role,
    cancel_grant,
    activate_role,
    get_active_roles
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
            suspended_badges = " ".join([f"<span style='background:#6B7280; color:#fff; padding:2px 8px; border-radius:10px; font-size:0.75rem; font-weight:700;'>SUSPENDED: {r.upper()}</span>" for r in u.get("suspended_roles", [])])
            revoked_badges = " ".join([f"<span style='background:#EF4444; color:#fff; padding:2px 8px; border-radius:10px; font-size:0.75rem; font-weight:700;'>REVOKED: {r.upper()}</span>" for r in u["revoked_roles"]])

            st.markdown(textwrap.dedent(f"""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:1rem; margin-bottom:0.75rem; box-shadow:0 1px 3px rgba(0,0,0,0.03);">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-weight:700; font-size:1rem; color:#0F172A;">{_safe(u['full_name'])}</div>
                        <div style="font-size:0.8rem; color:#64748B;">{_safe(u['email'])} · 📍 {_safe(u['district'])}</div>
                    </div>
                    <div>
                        {active_badges} {pending_badges} {suspended_badges} {revoked_badges}
                    </div>
                </div>
            </div>
            """).strip(), unsafe_allow_html=True)

    with col_g2:
        st.markdown("#### Grant Additional Role")
        user_options = {u["id"]: f"{u['full_name']} ({u['email']})" for u in users}
        if not user_options:
            st.info("No non-admin users found.")
            return

        sel_user_id = st.selectbox("Select User", list(user_options.keys()), format_func=lambda x: user_options[x], key="sel_user_grant")
        target_u = next((u for u in users if u["id"] == sel_user_id), None)
        curr_active = target_u.get("active_roles", []) if target_u else []
        curr_pending = target_u.get("pending_nda_roles", []) if target_u else []
        curr_all = set(curr_active + curr_pending)

        available_roles = [r for r in ["aspirant", "guide", "sme"] if r not in curr_all]
        role_labels = {
            "aspirant": "🌱 ASPIRANT (Entrepreneur / Venture Founder)",
            "guide": "🧭 GUIDE (Domain Mentor / Caseload Guide)",
            "sme": "🔬 SME (Domain Subject Matter Expert)"
        }

        if available_roles:
            with st.form(f"form_grant_role_{sel_user_id}"):
                new_role = st.selectbox(
                    "Role to Grant",
                    available_roles,
                    format_func=lambda x: role_labels.get(x, x.upper()),
                    key=f"sel_new_role_{sel_user_id}"
                )
                
                if new_role in ("guide", "sme"):
                    st.info("ℹ️ Promoting to Guide or SME sets status to **PENDING NDA**. The user will be required to sign the binding NDA before accessing protected caseloads.")
                else:
                    st.info("ℹ️ Granting the Aspirant role enables the user to build their own entrepreneurial venture and apply for grant schemes.")
                
                submit_grant = st.form_submit_button("Grant Role", type="primary")
                if submit_grant:
                    ok, err = grant_role(sel_user_id, new_role, granted_by=admin_id)
                    if ok:
                        st.success(f"Role '{new_role.upper()}' granted! {'Status set to PENDING NDA.' if new_role in ('guide', 'sme') else 'Active immediately.'}")
                        st.rerun()
                    else:
                        st.error(err or "Failed to grant role.")
        else:
            st.success(f"✅ {target_u.get('full_name', 'User')} already holds all available roles (Aspirant, Guide, SME).")

        st.markdown("<div style='height:1.25rem;'></div>", unsafe_allow_html=True)
        st.markdown("#### Manage Existing Role Grants")
        sel_manage_user = st.selectbox("Select User to Manage", list(user_options.keys()), format_func=lambda x: user_options[x], key="sel_manage_user")
        sel_target_user = next((u for u in users if u["id"] == sel_manage_user), None)

        grants = []
        if sel_target_user:
            primary_r = sel_target_user.get("primary_role", "aspirant")
            for r in sel_target_user.get("active_roles", []):
                if r in ("guide", "sme") or r != primary_r:
                    grants.append((r, "ACTIVE"))
            for r in sel_target_user.get("pending_nda_roles", []):
                if r in ("guide", "sme") or r != primary_r:
                    grants.append((r, "PENDING NDA"))
            for r in sel_target_user.get("suspended_roles", []):
                if r in ("guide", "sme") or r != primary_r:
                    grants.append((r, "SUSPENDED"))
            for r in sel_target_user.get("revoked_roles", []):
                if r in ("guide", "sme") or r != primary_r:
                    grants.append((r, "REVOKED"))

        if not grants:
            p_label = sel_target_user.get('primary_role', 'user').title() if sel_target_user else "registered"
            st.caption(f"ℹ️ This user holds only their base {p_label} role. Grant a Guide or SME role above to manage mentor privileges.")
        else:
            sel_grant_idx = st.selectbox(
                "Select Role Grant to Manage",
                range(len(grants)),
                format_func=lambda i: f"{grants[i][0].upper()} — Status: {grants[i][1]}",
                key=f"sel_grant_{sel_manage_user}"
            )
            sel_role, sel_status = grants[sel_grant_idx]
            status_colors = {"ACTIVE": "#10B981", "PENDING NDA": "#F59E0B", "SUSPENDED": "#6B7280", "REVOKED": "#EF4444"}
            badge_c = status_colors.get(sel_status, "#64748B")
            st.markdown(
                f"<div style='margin-bottom:0.75rem; font-size:0.9rem;'>Current Status: "
                f"<span style='background:{badge_c}; color:#fff; padding:2px 8px; border-radius:8px; font-weight:700;'>{sel_status}</span></div>",
                unsafe_allow_html=True
            )

            if sel_status == "ACTIVE":
                reason = st.text_input("Reason *", placeholder="e.g. Inactivity, ethics breach, caseload rotation", key="rev_reason_act")
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    if st.button("⏸️ Suspend Role", key="btn_susp_role", type="secondary", use_container_width=True):
                        if not reason.strip():
                            st.warning("Please enter a reason.")
                        else:
                            ok, err = suspend_role(sel_manage_user, sel_role, reason=reason.strip())
                            if ok:
                                st.success(f"Role '{sel_role.upper()}' suspended.")
                                st.rerun()
                            else:
                                st.error(err or "Failed to suspend role.")
                with col_b2:
                    if st.button("🚫 Revoke Role", key="btn_rev_role", type="primary", use_container_width=True):
                        if not reason.strip():
                            st.warning("Please enter a reason.")
                        else:
                            ok, err = revoke_role(sel_manage_user, sel_role, reason=reason.strip(), revoked_by=admin_id)
                            if ok:
                                st.success(f"Role '{sel_role.upper()}' revoked.")
                                st.rerun()
                            else:
                                st.error(err or "Failed to revoke role.")

            elif sel_status == "PENDING NDA":
                from services.legal import check_user_nda_accepted
                has_existing_nda = check_user_nda_accepted(sel_manage_user, sel_role)
                if has_existing_nda:
                    st.info(f"Role '{sel_role.upper()}' is awaiting workspace activation. Institutional Master NDA is already verified on record. You may administratively activate this role.")
                else:
                    st.warning(f"Role '{sel_role.upper()}' requires the user's digital NDA execution. The mentor must log in to digitally sign the Non-Disclosure Agreement before activation.")

                col_b1, col_b2, col_b3 = st.columns([1.3, 1, 1])
                with col_b1:
                    if has_existing_nda:
                        if st.button("✅ Verify & Activate Role", key=f"btn_act_pnd_{sel_manage_user}_{sel_role}", type="primary", use_container_width=True, help="Activate this role grant (Master NDA confirmed)."):
                            from services.roles import activate_role
                            ok, err = activate_role(sel_manage_user, sel_role)
                            if ok:
                                st.success(f"Role '{sel_role.upper()}' activated successfully! {sel_target_user.get('full_name')} is now active.")
                                st.rerun()
                            else:
                                st.error(err or "Failed to activate role.")
                    else:
                        st.button("🔒 Awaiting User Signature", key=f"btn_act_dis_{sel_manage_user}_{sel_role}", disabled=True, use_container_width=True, help="Mentor must sign their own NDA before activation.")
                with col_b2:
                    if st.button("❌ Cancel Grant", key="btn_cancel_grant", type="secondary", use_container_width=True):
                        ok, err = cancel_grant(sel_manage_user, sel_role)
                        if ok:
                            st.success(f"Pending grant for '{sel_role.upper()}' cancelled.")
                            st.rerun()
                        else:
                            st.error(err or "Failed to cancel grant.")
                with col_b3:
                    if st.button("🚫 Revoke Role", key="btn_rev_pnd_role", use_container_width=True):
                        ok, err = revoke_role(sel_manage_user, sel_role, reason="Cancelled pending NDA", revoked_by=admin_id)
                        if ok:
                            st.success(f"Role '{sel_role.upper()}' marked revoked.")
                            st.rerun()
                        else:
                            st.error(err or "Failed to revoke role.")

            elif sel_status == "SUSPENDED":
                st.warning(f"Role '{sel_role.upper()}' is currently suspended.")
                reason = st.text_input("Revocation Reason (if revoking)", placeholder="e.g. Non-compliance", key="rev_reason_susp")
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    if st.button("▶️ Reinstate Role", key="btn_reinstate_role", type="primary", use_container_width=True):
                        ok, err = reinstate_role(sel_manage_user, sel_role)
                        if ok:
                            st.success(f"Role '{sel_role.upper()}' reinstated to active status.")
                            st.rerun()
                        else:
                            st.error(err or "Failed to reinstate role.")
                with col_b2:
                    if st.button("🚫 Revoke Permanently", key="btn_rev_susp_role", type="secondary", use_container_width=True):
                        ok, err = revoke_role(sel_manage_user, sel_role, reason=reason.strip() or "Revoked after suspension", revoked_by=admin_id)
                        if ok:
                            st.success(f"Role '{sel_role.upper()}' revoked.")
                            st.rerun()
                        else:
                            st.error(err or "Failed to revoke role.")

            elif sel_status == "REVOKED":
                st.info(f"Role '{sel_role.upper()}' is currently revoked. To grant it again, use the Grant Additional Role form above.")


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
# 4. CASELOAD INACTIVITY & FOUNDER ENGAGEMENT MONITOR
# ─────────────────────────────────────────────────────────────────────────────
def render_admin_inactivity_tab(admin_id: str = None):
    from services.inactivity import (
        list_inactivity_records,
        check_and_process_caseload_inactivity,
        compute_alert_live_status,
        evaluate_aspirant_engagement_roster,
    )
    from services.external_contact import (
        normalize_phone_number,
        validate_email_address,
        generate_whatsapp_url,
        generate_gmail_compose_url,
        generate_mailto_url,
        get_guide_inactivity_template,
        get_sme_inactivity_template,
        get_aspirant_contact_template,
        record_external_contact
    )
    from services.governance import get_primary_admin_id

    effective_admin_id = admin_id or get_primary_admin_id()

    st.subheader("⏱️ Caseload Inactivity & Founder Engagement Monitor")
    st.caption("Dual-lens governance: track Mentor SLA responsiveness (7 / 10 / 14 days) alongside Blocker-Aware Founder Engagement (14 / 30 / 60 days).")

    monitor_mode = st.radio(
        "Select Monitoring Lens",
        options=[
            "🧭 Mentor SLA Monitor (7 / 10 / 14 Days)",
            "🌱 Founder Engagement & Blocker Monitor (14 / 30 / 60 Days)"
        ],
        horizontal=True,
        key="adm_inact_monitor_mode"
    )

    if monitor_mode == "🌱 Founder Engagement & Blocker Monitor (14 / 30 / 60 Days)":
        roster = evaluate_aspirant_engagement_roster()
        cnt_active = sum(1 for x in roster if x.get("engagement_state") == "ACTIVE")
        cnt_blocked = sum(1 for x in roster if x.get("is_blocked"))
        cnt_gentle = sum(1 for x in roster if x.get("engagement_state") == "GENTLE_CHECKIN")
        cnt_support = sum(1 for x in roster if x.get("engagement_state") in ("SUPPORT_NEEDED", "DORMANT"))

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("🟢 Active (<14d)", cnt_active)
        k2.metric("🛑 Blocked by Mentor/Admin", cnt_blocked)
        k3.metric("🟡 Gentle Check-In (14–29d)", cnt_gentle)
        k4.metric("🟠 Support Needed (30d+)", cnt_support)

        eng_filter = st.selectbox(
            "Filter Entrepreneurs by Engagement State",
            options=["ALL", "BLOCKED_ONLY", "GENTLE_CHECKIN", "SUPPORT_NEEDED", "DORMANT", "ACTIVE"],
            format_func=lambda k: {
                "ALL": "All Entrepreneurs",
                "BLOCKED_ONLY": "🛑 Blocked by Unassigned Mentor / Unanswered Ticket / Pending Review",
                "GENTLE_CHECKIN": "🟡 Gentle Check-In (14–29 Days Quiet)",
                "SUPPORT_NEEDED": "🟠 Support Needed (30–59 Days Quiet)",
                "DORMANT": "🔴 Stalled / Dormant (60+ Days Quiet)",
                "ACTIVE": "🟢 Active (<14 Days)"
            }.get(k, k),
            key="adm_founder_eng_filter"
        )

        filtered_roster = roster
        if eng_filter == "BLOCKED_ONLY":
            filtered_roster = [x for x in roster if x.get("is_blocked")]
        elif eng_filter != "ALL":
            filtered_roster = [x for x in roster if x.get("engagement_state") == eng_filter]

        if not filtered_roster:
            st.info("No entrepreneurs match the selected engagement filter.")
            return

        for item in filtered_roster:
            aid = item["aspirant_id"]
            aname = html.escape(item.get("full_name") or "Entrepreneur")
            abiz = html.escape(item.get("business_name") or "Enterprise")
            adist = html.escape(item.get("district") or "Tamil Nadu")
            b_color = item.get("badge_color", "#10B981")
            s_label = html.escape(item.get("state_label", "Active"))
            days_q = item.get("days_inactive", 0)
            last_src = html.escape(item.get("last_activity_source") or "Registration")
            rec_act = html.escape(item.get("recommended_action") or "")
            g_names = ", ".join(item.get("guide_names") or []) or "Unassigned"
            s_names = ", ".join(item.get("sme_names") or []) or "Unassigned"

            st.markdown(textwrap.dedent(f"""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-left:4px solid {b_color}; border-radius:10px; padding:0.95rem 1.1rem; margin-bottom:0.5rem; box-shadow:0 1px 3px rgba(0,0,0,0.03);">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:0.5rem;">
                    <div>
                        <div style="font-size:1rem; font-weight:800; color:#0F172A;">
                            {aname} <span style="font-weight:600; color:#2563EB; font-size:0.88rem;">· {abiz}</span>
                            <span style="font-weight:500; color:#64748B; font-size:0.8rem;">({adist})</span>
                        </div>
                        <div style="font-size:0.82rem; color:#475569; margin-top:3px;">
                            <strong>Guide:</strong> {html.escape(g_names)} · <strong>SME:</strong> {html.escape(s_names)} · <strong>Last Founder Activity:</strong> {days_q}d ago ({last_src})
                        </div>
                        <div style="font-size:0.8rem; color:#1E293B; margin-top:4px; background:#F8FAFC; padding:4px 8px; border-radius:6px; border:1px solid #E2E8F0;">
                            💡 <strong>Recommended Next Step:</strong> {rec_act}
                        </div>
                    </div>
                    <div style="text-align:right;">
                        <span style="background:{b_color}; color:#fff; font-size:0.74rem; font-weight:800; padding:3px 10px; border-radius:999px;">{s_label}</span>
                    </div>
                </div>
            </div>
            """).strip(), unsafe_allow_html=True)

            f_phone = item.get("phone") or ""
            f_email = item.get("email") or ""
            subj_f, body_f = get_aspirant_contact_template(item.get("full_name", "Founder"), "Supportive Check-In & Progress Update")
            wa_f = generate_whatsapp_url(f_phone, body_f) if f_phone else None
            gm_f = generate_gmail_compose_url(f_email, subj_f, body_f) if f_email else None

            cf1, cf2, cf3 = st.columns([1.2, 1.2, 2.6])
            with cf1:
                if wa_f:
                    st.link_button("💬 WhatsApp Check-In", url=wa_f, use_container_width=True)
                else:
                    st.button("💬 No Phone", disabled=True, key=f"f_wa_dis_{aid}", use_container_width=True)
            with cf2:
                if gm_f:
                    st.link_button("✉️ Gmail Check-In", url=gm_f, use_container_width=True)
                else:
                    st.button("✉️ No Email", disabled=True, key=f"f_gm_dis_{aid}", use_container_width=True)
            with cf3:
                if st.button("✅ Log Supportive Check-In Sent", key=f"f_log_sent_{aid}", use_container_width=True):
                    record_external_contact(
                        admin_id=effective_admin_id,
                        recipient_id=aid,
                        recipient_role="aspirant",
                        aspirant_id=aid,
                        channel="whatsapp" if wa_f else "email",
                        purpose="Founder Engagement Check-In",
                        notes=f"Supportive check-in logged from Engagement Monitor ({item.get('state_label')})."
                    )
                    st.success(f"Supportive check-in logged for {item.get('full_name')}!")
                    st.rerun()
        return

    c_btn1, c_btn2 = st.columns([1, 2])
    with c_btn1:
        if st.button("🚀 Run Caseload Inactivity Scan Now", type="primary", use_container_width=True):
            alerts = check_and_process_caseload_inactivity()
            st.success(f"Scan complete! {len(alerts)} new inactivity notifications triggered.")
            st.rerun()

    records = list_inactivity_records()

    # ── FILTERS ──
    f_col1, f_col2 = st.columns([1.5, 1.5])
    with f_col1:
        status_filter = st.selectbox(
            "Filter by Live Status",
            ["ALL", "Needs Attention", "Waiting on Entrepreneur Reply", "Follow-up Initiated", "Mentor Active Again", "Historical Record"],
            key="adm_inact_status_filter"
        )
    with f_col2:
        role_filter = st.selectbox(
            "Filter by Mentor Role",
            ["ALL", "guide", "sme"],
            format_func=lambda x: "All Mentor Types" if x == "ALL" else ("Guides Only" if x == "guide" else "Domain SMEs Only"),
            key="adm_inact_role_filter"
        )

    st.markdown(f"**Inactivity Escalation Log Records:** {len(records)}")

    if not records:
        st.info("No inactivity escalation records logged yet. Run a scan to check all active caseloads.")
        return

    # Pre-fetch current relationships for live status evaluation
    from services.relationships import get_all_relationships
    active_rels = get_all_relationships()

    rendered_count = 0
    for r in records:
        r_id = r.get("id")
        mentor_id = r.get("mentor_id") or r.get("guide_id", "")
        asp_id = r.get("aspirant_id", "")
        mentor_role = r.get("mentor_role", "guide")

        if role_filter != "ALL" and mentor_role != role_filter:
            continue

        live_status, status_badge_color, live_days, last_eng_str = compute_alert_live_status(r, active_rels)

        if status_filter != "ALL":
            if status_filter == "Needs Attention" and "Needs Attention" not in live_status:
                continue
            elif status_filter == "Waiting on Entrepreneur Reply" and live_status != "Waiting on Entrepreneur Reply":
                continue
            elif status_filter == "Follow-up Initiated" and "Follow-up Initiated" not in live_status:
                continue
            elif status_filter == "Mentor Active Again" and live_status != "Mentor Active Again":
                continue
            elif status_filter == "Historical Record" and live_status != "Historical Record":
                continue

        rendered_count += 1
        mentor = get_profile(mentor_id) or {}
        asp = get_profile(asp_id) or {}
        stage = r.get("escalation_stage", "")
        stage_color = "#DC2626" if "DAY_14" in stage else ("#F59E0B" if "DAY_7" in stage else "#E11D48")

        mentor_name = html.escape(mentor.get("full_name") or ("Dedicated Guide" if mentor_role == "guide" else "Domain SME"))
        asp_name = html.escape(asp.get("full_name", "Entrepreneur"))
        asp_bname = html.escape(asp.get("profile_data", {}).get("business", {}).get("business_name", "Enterprise"))
        role_label = "Dedicated Guide" if mentor_role == "guide" else "Domain Specialist (SME)"
        case_type = "Caseload mentorship" if mentor_role == "guide" else "Technical advisory case"

        mentor_phone = mentor.get("phone") or mentor.get("profile_data", {}).get("personal", {}).get("phone")
        mentor_email = mentor.get("email")

        # Resolve templates
        if mentor_role == "guide":
            subj, body = get_guide_inactivity_template(mentor.get("full_name", ""), asp.get("full_name", ""))
        else:
            subj, body = get_sme_inactivity_template(mentor.get("full_name", ""), asp.get("full_name", ""))

        wa_url = generate_whatsapp_url(mentor_phone, body) if mentor_phone else None
        gmail_url = generate_gmail_compose_url(mentor_email, subj, body) if mentor_email else None
        mailto_url = generate_mailto_url(mentor_email, subj, body) if mentor_email else None

        st.markdown(textwrap.dedent(f"""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-left:4px solid {stage_color}; border-radius:10px; padding:0.95rem; margin-bottom:0.5rem; box-shadow:0 1px 3px rgba(0,0,0,0.03);">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:0.5rem;">
                <div>
                    <div style="font-size:0.95rem;">
                        <span style="font-weight:700; color:#0F172A;">{mentor_name}</span>
                        <span style="font-size:0.75rem; font-weight:600; color:#475569; background:#F1F5F9; padding:2px 6px; border-radius:6px; margin-left:4px;">{mentor_role.upper()}</span>
                        <span style="color:#64748B; margin:0 4px;">➔</span>
                        <span style="font-weight:700; color:#0F172A;">{asp_name}</span>
                        <span style="font-size:0.8rem; color:#64748B;">({asp_bname})</span>
                    </div>
                    <div style="font-size:0.82rem; color:#475569; margin-top:3px;">
                        <strong>{role_label}</strong> · {case_type} · Inactive for <strong>{live_days} days</strong>
                    </div>
                    <div style="font-size:0.75rem; color:#64748B; margin-top:2px;">
                        {last_eng_str}
                    </div>
                </div>
                <div style="text-align:right;">
                    <span style="background:{stage_color}; color:#fff; font-size:0.72rem; font-weight:700; padding:2px 8px; border-radius:8px;">{stage.replace('_', ' ')}</span>
                    <span style="background:{status_badge_color}; color:#fff; font-size:0.72rem; font-weight:700; padding:2px 8px; border-radius:8px; margin-left:4px;">{live_status}</span>
                    <div style="font-size:0.68rem; color:#94A3B8; margin-top:4px;">Notified: {r.get('notification_sent_at', '')[:16].replace('T', ' ')}</div>
                </div>
            </div>
        </div>
        """).strip(), unsafe_allow_html=True)

        # Compact follow-up actions
        col_act1, col_act2, col_act3, col_act4 = st.columns([1.2, 1.2, 1.3, 1.8])
        with col_act1:
            if wa_url:
                st.link_button("💬 WhatsApp", url=wa_url, use_container_width=True, help=f"Open prefilled WhatsApp chat with {mentor_name}")
            else:
                st.button("💬 WhatsApp", disabled=True, key=f"btn_wa_dis_{r_id}", use_container_width=True, help="WhatsApp phone number not on mentor profile")
        with col_act2:
            if gmail_url:
                st.link_button("✉️ Gmail", url=gmail_url, use_container_width=True, help=f"Open pre-addressed Gmail compose draft to {mentor_name}")
            elif mailto_url:
                st.link_button("✉️ Email", url=mailto_url, use_container_width=True, help=f"Open mail client addressed to {mentor_name}")
            else:
                st.button("✉️ Gmail", disabled=True, key=f"btn_gm_dis_{r_id}", use_container_width=True, help="Verified email address not on mentor profile")
        with col_act3:
            if live_status not in ("Mentor Active Again", "Historical Record") and "Follow-up Initiated" not in live_status:
                if st.button("✅ Mark as Sent", key=f"mark_fu_btn_{r_id}", use_container_width=True):
                    record_external_contact(
                        admin_id=effective_admin_id,
                        recipient_id=mentor_id,
                        recipient_role=mentor_role,
                        aspirant_id=asp_id,
                        channel="whatsapp" if wa_url else "email",
                        purpose="Caseload Inactivity Reminder",
                        inactivity_record_id=r_id,
                        notes="Admin marked follow-up reminder sent."
                    )
                    st.success("Follow-up logged!")
                    st.rerun()
            else:
                st.caption(f"Status: {live_status}")
        with col_act4:
            with st.expander("Preview prefilled message", expanded=False):
                st.code(body, language="text")

        st.markdown("<div style='height:0.3rem;'></div>", unsafe_allow_html=True)

    if rendered_count == 0:
        st.info(f"No records match filter: {status_filter} / {role_filter}.")


# ─────────────────────────────────────────────────────────────────────────────
# 5. SME DIRECTORY & CONFLICT OF INTEREST GOVERNANCE
# ─────────────────────────────────────────────────────────────────────────────
def render_admin_sme_conflicts_tab(admin_id: str):
    st.subheader("⚖️ Subject Matter Expert (SME) Directory & Conflict Governance")
    st.caption("Domain specialist credentials and mandatory conflict-of-interest declarations.")

    from services.roles import list_active_profiles_for_role
    smes = list_active_profiles_for_role("sme")
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
            from services.profiles import list_all_profiles
            from services.relationships import unassign_sme
            all_p = {p["id"]: p for p in list_all_profiles()}
            for c in conflicts:
                sme_p = all_p.get(c.get("sme_id", "")) or {}
                asp_p = all_p.get(c.get("aspirant_id", "")) or {}
                has_conf = c.get("has_conflict", False)
                c_status = str(c.get("status") or "DECLARED").upper()

                color = "#DC2626" if (has_conf and c_status not in ("RESOLVED", "DISMISSED")) else "#10B981"
                text = f"CONFLICT ({c_status})" if has_conf else "CLEARED / NO CONFLICT"

                st.markdown(f"""
                <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-left:4px solid {color}; border-radius:10px; padding:0.9rem; margin-bottom:0.5rem;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <span style="font-weight:700; color:#0F172A;">{_safe(sme_p.get('full_name', 'SME'))}</span> ➔ <span style="font-weight:700; color:#0F172A;">{_safe(asp_p.get('full_name', 'Aspirant'))}</span>
                            <div style="font-size:0.85rem; color:#334155; margin-top:4px;">{_safe(c.get('conflict_details'))}</div>
                        </div>
                        <div style="text-align:right;">
                            <span style="background:{color}; color:#fff; font-size:0.75rem; font-weight:700; padding:2px 8px; border-radius:8px;">{text}</span>
                            <div style="font-size:0.7rem; color:#94A3B8; margin-top:4px;">Declared: {str(c.get('created_at', ''))[:16].replace('T', ' ')}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if has_conf and c_status not in ("RESOLVED", "DISMISSED") and c.get("aspirant_id") and c.get("sme_id"):
                    if st.button(
                        f"🔄 Approve Recusal & Unassign {sme_p.get('full_name', 'SME')} from {asp_p.get('full_name', 'Aspirant')}",
                        key=f"btn_resolve_coi_{c.get('id')}",
                        type="primary"
                    ):
                        ok_u, err_u = unassign_sme(
                            aspirant_id=c["aspirant_id"],
                            sme_id=c["sme_id"],
                            admin_id=admin_id,
                            reason=f"Conflict of Interest Recusal Approved: {c.get('conflict_details', '')}"
                        )
                        if ok_u:
                            st.success("Conflicted SME unassigned and logged in Assignment History.")
                            st.rerun()
                        else:
                            st.error(err_u or "Failed to unassign SME.")


# ─────────────────────────────────────────────────────────────────────────────
# 6. CONTACT ASPIRANTS CONSOLE (WHATSAPP & GMAIL ENGAGEMENT)
# ─────────────────────────────────────────────────────────────────────────────
def render_admin_contact_aspirants_tab(admin_id: str, aspirants: list):
    from services.external_contact import (
        normalize_phone_number,
        validate_email_address,
        generate_whatsapp_url,
        generate_gmail_compose_url,
        generate_mailto_url,
        get_aspirant_contact_template,
        ASPIRANT_PURPOSE_TEMPLATES,
        record_external_contact,
        list_external_contacts
    )
    from services.aspirant_photos import get_aspirant_photo
    from services.roles import list_users_with_multi_roles
    from services.relationships import get_aspirant_mentors

    st.subheader("💬 Contact Aspirants")
    st.caption("Direct, authorized communication with entrepreneurs from Fulcrum Support via WhatsApp and Gmail. Manual dispatch required.")

    if not aspirants:
        st.info("No entrepreneurs registered on Fulcrum yet.")
        return

    # 1. Search Bar & Filter
    c_s1, c_s2 = st.columns([2.5, 1])
    with c_s1:
        search_query = st.text_input(
            "🔍 Search Aspirants",
            placeholder="Search by founder name, business name, sector, or district...",
            key="adm_contact_asp_search"
        ).strip().lower()

    filtered_asp = []
    for a in aspirants:
        name = str(a.get("full_name", "")).lower()
        b_name = str(a.get("profile_data", {}).get("business", {}).get("business_name", "")).lower()
        sector = str(a.get("profile_data", {}).get("business", {}).get("sector", "")).lower()
        district = str(a.get("district", "")).lower()
        if not search_query or (search_query in name or search_query in b_name or search_query in sector or search_query in district):
            filtered_asp.append(a)

    with c_s2:
        st.markdown(f"<div style='margin-top:1.8rem; font-size:0.85rem; color:#64748B; font-weight:600;'>Found {len(filtered_asp)} entrepreneurs</div>", unsafe_allow_html=True)

    if not filtered_asp:
        st.warning("No entrepreneurs match your search filter.")
        return

    # 2. Dropdown Selector
    multi_roles_map = {u["id"]: u.get("active_roles", ["aspirant"]) for u in list_users_with_multi_roles()}
    def _format_contact_asp(a):
        bname = a.get("profile_data", {}).get("business", {}).get("business_name") or "Enterprise"
        dist = a.get("district") or "TN"
        roles = multi_roles_map.get(a["id"], ["aspirant"])
        extra = [r.title() for r in roles if r != "aspirant"]
        extra_str = f" [{', '.join(extra)}]" if extra else ""
        return f"{a.get('full_name', 'Founder')} — {bname} ({dist}){extra_str}"

    asp_dict = {a["id"]: _format_contact_asp(a) for a in filtered_asp}
    selected_id = st.selectbox(
        "Select Entrepreneur to Contact",
        list(asp_dict.keys()),
        format_func=lambda x: asp_dict[x],
        key="adm_contact_selected_asp"
    )

    selected_asp = next((a for a in filtered_asp if a["id"] == selected_id), None)
    if not selected_asp:
        return

    # 3. Entrepreneur Profile & Contact Card
    b_data = selected_asp.get("profile_data", {}).get("business", {})
    p_data = selected_asp.get("profile_data", {}).get("personal", {})
    phone_val = selected_asp.get("phone") or p_data.get("phone") or ""
    email_val = selected_asp.get("email") or ""
    asp_name = selected_asp.get("full_name") or "Entrepreneur"
    business_name = b_data.get("business_name") or "Enterprise"
    sector_val = b_data.get("sector") or "General"
    stage_val = b_data.get("stage") or "Early Stage"
    district_val = selected_asp.get("district") or "Tamil Nadu"

    norm_phone, phone_err = normalize_phone_number(phone_val)
    clean_email, email_err = validate_email_address(email_val)

    # Photo retrieval
    asp_photo = get_aspirant_photo(selected_id, viewer_id=admin_id, viewer_role="admin")
    photo_html = ""
    if asp_photo and asp_photo.get("url"):
        photo_html = f'<img src="{asp_photo["url"]}" alt="Aspirant Headshot" style="width:68px; height:68px; border-radius:50%; object-fit:cover; border:2px solid #2563EB; box-shadow:0 2px 6px rgba(0,0,0,0.1); margin-right:1rem;" />'
    else:
        photo_html = '<div style="width:68px; height:68px; border-radius:50%; background:#EFF6FF; border:2px solid #CBD5E1; display:flex; align-items:center; justify-content:center; font-size:1.6rem; color:#3B82F6; margin-right:1rem;">👤</div>'

    # Assigned Mentors
    mentors_info = get_aspirant_mentors(selected_id)
    g_info = mentors_info.get("guide")
    s_info = mentors_info.get("sme")
    g_name = g_info.get("full_name") if g_info else "Unassigned"
    s_name = s_info.get("full_name") if s_info else "Unassigned"

    phone_badge = f'<span style="color:#059669; font-weight:700;">✓ +{norm_phone}</span>' if norm_phone else '<span style="color:#DC2626; font-weight:600;">✗ Unavailable</span>'
    email_badge = f'<span style="color:#059669; font-weight:700;">✓ {clean_email}</span>' if clean_email else '<span style="color:#DC2626; font-weight:600;">✗ Unavailable</span>'

    st.markdown(textwrap.dedent(f"""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-left:4px solid #2563EB; border-radius:12px; padding:1.1rem; margin-top:0.75rem; margin-bottom:1rem; box-shadow:0 1px 3px rgba(0,0,0,0.04);">
        <div style="display:flex; align-items:center; flex-wrap:wrap;">
            {photo_html}
            <div style="flex:1; min-width:240px;">
                <div style="font-size:1.15rem; font-weight:800; color:#0F172A;">{html.escape(asp_name)}</div>
                <div style="font-size:0.88rem; color:#475569; margin-top:2px;">
                    <strong>{html.escape(business_name)}</strong> · {html.escape(sector_val)} · {html.escape(stage_val)} · {html.escape(district_val)}
                </div>
                <div style="font-size:0.82rem; color:#64748B; margin-top:4px;">
                    <strong>Guide:</strong> {html.escape(g_name)} | <strong>Domain SME:</strong> {html.escape(s_name)}
                </div>
            </div>
            <div style="text-align:right; min-width:200px; font-size:0.8rem; line-height:1.6; margin-top:0.5rem;">
                <div>📱 <strong>Mobile:</strong> {phone_badge}</div>
                <div>✉️ <strong>Email:</strong> {email_badge}</div>
            </div>
        </div>
    </div>
    """).strip(), unsafe_allow_html=True)

    # 4. Purpose Selection & Editable Message Preview
    st.markdown("#### 📝 Compose Courteous Outreach")
    purposes = list(ASPIRANT_PURPOSE_TEMPLATES.keys())
    sel_purpose = st.selectbox(
        "Communication Purpose",
        purposes,
        key=f"adm_asp_purpose_{selected_id}"
    )

    default_subject, default_body = get_aspirant_contact_template(asp_name, sel_purpose)

    edited_subject = st.text_input("Email Subject Line", value=default_subject, key=f"adm_asp_subj_{selected_id}")
    edited_body = st.text_area("Message Body (Editable before opening draft)", value=default_body, height=180, key=f"adm_asp_body_{selected_id}")

    # Generate links from edited content
    wa_url = generate_whatsapp_url(phone_val, edited_body) if norm_phone else None
    gmail_url = generate_gmail_compose_url(email_val, edited_subject, edited_body) if clean_email else None
    mailto_url = generate_mailto_url(email_val, edited_subject, edited_body) if clean_email else None

    # 5. Compact Action Buttons
    c_btn_wa, c_btn_gm, c_btn_mark = st.columns([1.2, 1.2, 1.4])
    with c_btn_wa:
        if wa_url:
            st.link_button("💬 Open WhatsApp Chat", url=wa_url, use_container_width=True, help="Open WhatsApp with prefilled message to founder")
        else:
            st.button("💬 WhatsApp Unavailable", disabled=True, key=f"btn_asp_wa_dis_{selected_id}", use_container_width=True, help="No valid phone number on founder profile")
    with c_btn_gm:
        if gmail_url:
            st.link_button("✉️ Open Gmail Compose", url=gmail_url, use_container_width=True, help="Open Gmail draft addressed to founder")
        elif mailto_url:
            st.link_button("✉️ Open Email Draft", url=mailto_url, use_container_width=True, help="Open default mail client addressed to founder")
        else:
            st.button("✉️ Email Unavailable", disabled=True, key=f"btn_asp_gm_dis_{selected_id}", use_container_width=True, help="No valid email address on founder profile")
    with c_btn_mark:
        if st.button("✅ Mark as Sent", key=f"btn_mark_asp_sent_{selected_id}", use_container_width=True, help="Record that reminder/check-in was manually dispatched"):
            channel_used = "whatsapp" if wa_url else "email"
            ok, err = record_external_contact(
                admin_id=admin_id,
                recipient_id=selected_id,
                recipient_role="aspirant",
                aspirant_id=selected_id,
                channel=channel_used,
                purpose=sel_purpose,
                notes=f"Admin confirmed message sent for purpose: {sel_purpose}"
            )
            if ok:
                st.success("Outreach recorded for institutional audit trail.")
                st.rerun()
            else:
                st.error(err or "Failed to record communication.")

    st.markdown("<div style='height:0.8rem;'></div>", unsafe_allow_html=True)

    # 6. Communication History
    comm_history = list_external_contacts(recipient_id=selected_id, limit=5)
    with st.expander(f"📜 Recent Communication Log with {asp_name} ({len(comm_history)})", expanded=False):
        if not comm_history:
            st.caption("No previous external communication logged for this founder.")
        else:
            for ch in comm_history:
                ch_icon = "💬 WhatsApp" if ch.get("channel") == "whatsapp" else "✉️ Email"
                sent_at = ch.get("created_at", "")[:16].replace("T", " ")
                st.markdown(f"• **{sent_at}** · {ch_icon} · *{ch.get('purpose', 'General check-in')}* · Status: `{ch.get('status', 'SENT_CONFIRMED')}`")


