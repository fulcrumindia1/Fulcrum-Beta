"""
pages/admin.py — Admin Control Tower for FULCRUM-INDIA (Cluster A)
=================================================================
The central operations desk:
- Command Metrics (Aspirants, Guides, SMEs, Journeys, Help Requests, Schemes)
- Guides Management & Account Provisioning (No public signup)
- SMEs Management & Account Provisioning (No public signup)
- Relationship Authority: Admin assigns Guide & SME to Aspirants
- Aspirants Directory & Drill-down (Full Profile, Relationships, Journey, Matches)
- Global Journey Timeline inspection with override management
- Help Requests Console (Ticket management & official responses)
- Scheme Catalogue CRUD (Add, Edit, Toggle Active/Archive)
"""

import streamlit as st
import html
from datetime import datetime, timezone

def _safe_esc(val, default=""):
    """Crash-proof HTML escape that safely handles None, booleans, and non-string types."""
    if val is None:
        return default
    return html.escape(str(val))
from services.auth import admin_create_mentor, backfill_auth_users, get_data_backend
from services.profiles import get_profile, list_profiles_by_role
from services.relationships import get_aspirant_mentors, assign_guide, assign_sme, unassign_guide, unassign_sme
from services.journey import get_journey_timeline, soft_delete_event, log_meaningful_event, add_admin_journey_entry, get_standard_role_label, count_active_journeys
from views.journey_edit_dialog import render_edit_journey_dialog
from services.roles import get_active_roles
from services.schemes import list_schemes, get_scheme, upsert_scheme, toggle_archive_scheme, delete_scheme, match_schemes_for_aspirant
from services.pdf_generator import generate_aspirant_dossier_pdf
from services.schemes_ui import render_fund_explorer_card
from services.cache import is_tab_active
from views.admin_governance import (
    render_admin_role_grants_tab,
    render_admin_legal_records_tab,
    render_admin_complaints_tab,
    render_admin_inactivity_tab,
    render_admin_contact_aspirants_tab,
    render_admin_sme_conflicts_tab
)
from services.help_requests import list_mentor_admin_queries, admin_respond_to_mentor
from services.constants import (
    MASTER_SECTORS,
    MASTER_STAGES,
    MASTER_DISTRICTS_TN,
    MASTER_FUNDING_TYPES,
    MASTER_CATEGORY_TYPES,
    MASTER_GEOGRAPHIC_SCOPES
)

def render_admin_portal(admin_profile: dict):
    admin_id = admin_profile["id"]
    admin_name = admin_profile.get("full_name", "Administrator")

    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:1.5rem; padding-bottom:1rem; border-bottom:1px solid #E2E8F0;">
        <div>
            <div style="font-size:0.8rem; font-weight:800; text-transform:uppercase; letter-spacing:1px; color:#DB2777;">Admin Command Center</div>
            <h1 style="font-size:2rem; font-weight:800; margin:0; color:#0F172A;">FULCRUM-INDIA Control Tower</h1>
            <p style="font-size:0.95rem; color:#475569; margin-top:0.25rem;">
                Program Administration, Mentorship Governance & Scheme Intelligence
            </p>
        </div>
        <div style="text-align:right;">
            <span style="display:inline-block; padding:4px 14px; border-radius:12px; font-size:0.85rem; font-weight:700; background:#FDF2F8; color:#DB2777; border:1px solid #FBCFE8;">
                Admin: {admin_name}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # In Supabase mode, allow Admin to run safe backfill/sync
    if get_data_backend() == "supabase":
        with st.expander("⚡ Supabase Auth Synchronization & User Backfill", expanded=False):
            st.markdown("<p style='font-size:0.85rem; color:#64748B;'>Sync registered Supabase Auth users to application profiles, journeys, and mentor relationship records.</p>", unsafe_allow_html=True)
            col_bf1, col_bf2 = st.columns([2, 1])
            with col_bf1:
                admin_email_to_promote = st.text_input("Designated Super Admin Email", value="fulcrumindia1@gmail.com", key="admin_sync_email")
            with col_bf2:
                st.write("")
                st.write("")
                if st.button("🔄 Sync Auth Users", key="btn_admin_sync_auth"):
                    bf_res = backfill_auth_users(default_admin_email=admin_email_to_promote)
                    if "error" in bf_res:
                        st.error(bf_res["error"])
                    else:
                        st.success(f"Sync complete: {bf_res.get('backfilled', 0)} backfilled, {bf_res.get('already_existing', 0)} verified (Total Auth Users: {bf_res.get('total_auth_users', 0)}).")
                        st.rerun()

    # Fetch stats
    aspirants = list_profiles_by_role("aspirant")
    guides = list_profiles_by_role("guide")
    smes = list_profiles_by_role("sme")
    all_schemes = list_schemes(active_only=False)
    mentor_queries = list_mentor_admin_queries()
    pending_directives = [q for q in mentor_queries if q.get("status") == "PENDING_ADMIN"]
    active_journeys_count = count_active_journeys()

    # 6 Top Metric Cards
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        st.markdown(f"""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-bottom:3px solid #6366f1; border-radius:12px; padding:0.9rem; text-align:center; box-shadow:0 1px 3px rgba(0,0,0,0.04);">
            <div style="font-size:0.72rem; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.5px;">Aspirants</div>
            <div style="font-size:1.75rem; font-weight:800; color:#0F172A; margin-top:2px;">{len(aspirants)}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-bottom:3px solid #10b981; border-radius:12px; padding:0.9rem; text-align:center; box-shadow:0 1px 3px rgba(0,0,0,0.04);">
            <div style="font-size:0.72rem; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.5px;">Active Guides</div>
            <div style="font-size:1.75rem; font-weight:800; color:#0F172A; margin-top:2px;">{len(guides)}</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-bottom:3px solid #f59e0b; border-radius:12px; padding:0.9rem; text-align:center; box-shadow:0 1px 3px rgba(0,0,0,0.04);">
            <div style="font-size:0.72rem; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.5px;">Active SMEs</div>
            <div style="font-size:1.75rem; font-weight:800; color:#0F172A; margin-top:2px;">{len(smes)}</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-bottom:3px solid #3b82f6; border-radius:12px; padding:0.9rem; text-align:center; box-shadow:0 1px 3px rgba(0,0,0,0.04);">
            <div style="font-size:0.72rem; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.5px;">Active Journeys</div>
            <div style="font-size:1.75rem; font-weight:800; color:#0F172A; margin-top:2px;">{active_journeys_count}</div>
        </div>
        """, unsafe_allow_html=True)
    with c5:
        st.markdown(f"""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-bottom:3px solid #ef4444; border-radius:12px; padding:0.9rem; text-align:center; box-shadow:0 1px 3px rgba(0,0,0,0.04);">
            <div style="font-size:0.72rem; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.5px;">Directives Needed</div>
            <div style="font-size:1.75rem; font-weight:800; color:#0F172A; margin-top:2px;">{len(pending_directives)}</div>
        </div>
        """, unsafe_allow_html=True)
    with c6:
        st.markdown(f"""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-bottom:3px solid #ec4899; border-radius:12px; padding:0.9rem; text-align:center; box-shadow:0 1px 3px rgba(0,0,0,0.04);">
            <div style="font-size:0.72rem; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.5px;">Schemes</div>
            <div style="font-size:1.75rem; font-weight:800; color:#0F172A; margin-top:2px;">{len(all_schemes)}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

    # Admin Tabs (Lazy evaluated with state tracking)
    tabs = st.tabs([
        "👥 Aspirants & Journeys",
        "🧭 Guides Management",
        "🔬 SMEs Management",
        "🎯 Mentor Assignments",
        "🏛️ Mentor Inquiries & Directives",
        "🏦 Scheme Catalogue (CRUD)",
        "🔑 Multi-Role Grants",
        "📜 Legal & NDA Records",
        "🛡️ Confidential Complaints",
        "⏱️ Inactivity Monitor",
        "💬 Contact Aspirants",
        "⚖️ SME Conflict Governance"
    ], on_change="rerun", key="admin_main_tabs")

    # ─────────────────────────────────────────────────────────────
    # TAB 1: ASPIRANTS & JOURNEYS
    # ─────────────────────────────────────────────────────────────
    with tabs[0]:
        st.subheader("Entrepreneurs Directory")
        if not aspirants:
            st.info("No Aspirants have signed up yet.")
        else:
            col_sel1, col_sel2 = st.columns([2, 1])
            with col_sel1:
                def _format_asp_label(a):
                    bname = a.get('profile_data',{}).get('business',{}).get('business_name','Enterprise')
                    dist = a.get('district','TN')
                    roles = get_active_roles(a['id'])
                    extra = [r.title() for r in roles if r != 'aspirant']
                    extra_str = f" [{', '.join(extra)}]" if extra else ""
                    return f"{a['full_name']} — {bname} ({dist}){extra_str}"
                asp_options = {a["id"]: _format_asp_label(a) for a in aspirants}
                selected_asp_id = st.selectbox("Select Entrepreneur to inspect", list(asp_options.keys()), format_func=lambda x: asp_options[x], key="adm_sel_asp")
            with col_sel2:
                st.markdown("<div style='height: 1.75rem;'></div>", unsafe_allow_html=True)

            curr_asp = get_profile(selected_asp_id)
            if curr_asp:
                with col_sel2:
                    try:
                        cached_bytes = st.session_state.get("cached_dossier_pdf")
                        has_pdf = (st.session_state.get("cached_dossier_asp_id") == selected_asp_id and cached_bytes and len(cached_bytes) >= 1000)
                        if has_pdf:
                            clean_name = "".join(c for c in curr_asp.get("full_name", "Aspirant") if c.isalnum() or c == "_")
                            st.download_button(
                                label="📥 Download Founder Dossier (PDF)",
                                data=cached_bytes,
                                file_name=f"FULCRUM_Dossier_{clean_name}.pdf",
                                mime="application/pdf",
                                use_container_width=True,
                                key=f"dl_pdf_dossier_{selected_asp_id}"
                            )
                        else:
                            if st.button("📄 Generate Founder Dossier (PDF)", use_container_width=True, key=f"btn_gen_pdf_{selected_asp_id}"):
                                with st.spinner("Compiling Dossier PDF..."):
                                    pdf_data = generate_aspirant_dossier_pdf(selected_asp_id)
                                    st.session_state["cached_dossier_pdf"] = pdf_data
                                    st.session_state["cached_dossier_asp_id"] = selected_asp_id
                                    st.rerun()
                    except Exception as e:
                        st.error(f"PDF generation error: {e}")
                mentors_info = get_aspirant_mentors(selected_asp_id)
                g_assigned = mentors_info.get("guide")
                s_assigned = mentors_info.get("sme")
                b_info = curr_asp.get("profile_data", {}).get("business", {})

                from services.aspirant_photos import get_aspirant_photo
                adm_asp_photo = get_aspirant_photo(selected_asp_id)
                if adm_asp_photo and adm_asp_photo.get("url"):
                    photo_html = (
                        '<div style="text-align:center; padding:0 1.5rem;">'
                        f'<img src="{adm_asp_photo["url"]}" alt="Founder Headshot" style="width:72px; height:72px; border-radius:50%; object-fit:cover; border:2.5px solid #2563EB; box-shadow:0 3px 10px rgba(37,99,235,0.2);" />'
                        '<div style="font-size:0.68rem; color:#059669; font-weight:700; margin-top:4px;">✓ Verified Photo</div>'
                        '</div>'
                    )
                else:
                    ini = "".join([part[0].upper() for part in curr_asp.get("full_name", "A").split()[:2]]) or "A"
                    photo_html = (
                        '<div style="text-align:center; padding:0 1.5rem;">'
                        f'<div style="width:68px; height:68px; border-radius:50%; background:linear-gradient(135deg, #E2E8F0 0%, #CBD5E1 100%); color:#475569; display:flex; align-items:center; justify-content:center; font-size:1.3rem; font-weight:800; border:2px solid #E2E8F0; margin:0 auto; box-shadow:0 2px 6px rgba(0,0,0,0.04);">{ini}</div>'
                        '<div style="font-size:0.68rem; color:#94A3B8; font-weight:600; margin-top:4px;">No Photo Uploaded</div>'
                        '</div>'
                    )

                guide_label = g_assigned.get('full_name') if g_assigned else 'None'
                sme_label = s_assigned.get('full_name') if s_assigned else 'None'
                b_name_disp = b_info.get('business_name', 'Enterprise')
                b_sec_disp = b_info.get('sector', 'General')
                b_stage_disp = b_info.get('stage', 'idea')
                f_name_disp = curr_asp['full_name']
                email_disp = curr_asp['email']
                phone_disp = curr_asp.get('phone') or 'Not Provided'
                district_disp = curr_asp.get('district') or 'Not Provided'

                card_html = (
                    '<div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:1.25rem; margin:1rem 0; box-shadow:0 1px 3px rgba(0,0,0,0.04);">'
                    '<div style="display:flex; justify-content:space-between; align-items:center; gap:12px;">'
                    '<div style="flex:1;">'
                    f'<h3 style="margin:0; color:#0F172A;">{f_name_disp}</h3>'
                    f'<div style="color:#2563EB; font-weight:600; margin-top:2px;">{b_name_disp} · {b_sec_disp} ({b_stage_disp})</div>'
                    f'<div style="color:#475569; font-size:0.85rem; margin-top:0.25rem;">Email: {email_disp} | Phone: {phone_disp} | District: {district_disp}</div>'
                    '</div>'
                    f'{photo_html}'
                    '<div style="text-align:right; flex-shrink:0;">'
                    f'<div style="font-size:0.9rem; color:#334155;"><strong style="color:#0F172A;">Guide:</strong> <span style="color:#059669; font-weight:700;">{guide_label}</span></div>'
                    f'<div style="font-size:0.9rem; color:#334155; margin-top:3px;"><strong style="color:#0F172A;">SME:</strong> <span style="color:#D97706; font-weight:700;">{sme_label}</span></div>'
                    '</div>'
                    '</div>'
                    '</div>'
                )
                st.markdown(card_html, unsafe_allow_html=True)

                st.markdown("#### Complete Chronological Journey")

                with st.expander(f"➕ Log Official Administrative Directive to {curr_asp['full_name']}'s Journey", expanded=False):
                    if "admin_directive_success" in st.session_state:
                        _ad_msg = st.session_state.pop("admin_directive_success")
                        st.success(_ad_msg)
                        try:
                            st.toast(_ad_msg, icon="✅")
                        except Exception:
                            pass
                    with st.form(f"form_admin_add_journey_{selected_asp_id}"):
                        c_ad1, c_ad2 = st.columns(2)
                        with c_ad1:
                            ad_title = st.text_input("Title / Directive Milestone *", placeholder="e.g. Subsidy Sanction Review & Allocation Approval")
                            ad_cat = st.selectbox("Directive Category", ["Official Sanction", "Administrative Review", "Compliance Clearance", "Grant Allocation", "Program Onboarding", "Other / Custom Directive"])
                        with c_ad2:
                            ad_date = st.date_input("Directive Date", value=datetime.now(timezone.utc).date())
                        ad_desc = st.text_area("Administrative Notes / Directive Details *", placeholder="Formally reviewed founder's DPR and cap table. Cleared for departmental tranche disbursement.")
                        if st.form_submit_button("RECORD ADMINISTRATIVE DIRECTIVE", type="primary"):
                            if ad_title and ad_desc:
                                ev, err = add_admin_journey_entry(
                                    aspirant_id=selected_asp_id,
                                    admin_id=admin_id,
                                    title=ad_title,
                                    description=ad_desc,
                                    category=ad_cat,
                                    event_date=ad_date.isoformat()
                                )
                                if ev:
                                    st.session_state.pop("cached_dossier_pdf", None)
                                    st.session_state["admin_directive_success"] = f"Administrative directive '{ad_title}' recorded to {curr_asp['full_name']}'s Journey!"
                                    st.rerun()
                                else:
                                    st.error(err or "Failed to record directive.")
                            else:
                                st.warning("Please provide both title and description.")

                if "del_event_success" in st.session_state:
                    _d_msg = st.session_state.pop("del_event_success")
                    st.success(_d_msg)
                    try:
                        st.toast(_d_msg, icon="✅")
                    except Exception:
                        pass
                if "del_event_err" in st.session_state:
                    st.error(st.session_state.pop("del_event_err"))

                timeline = get_journey_timeline(selected_asp_id)
                if not timeline:
                    st.info("No journey events recorded yet for this entrepreneur.")
                else:
                    for event in timeline:
                        actor_role = event.get("actor_role", "aspirant")
                        actor_name = event.get("actor_name")
                        if actor_role == "system":
                            actor_name = "Platform Intelligence"
                        elif not actor_name:
                            if actor_role == "aspirant":
                                actor_name = "Entrepreneur"
                            elif actor_role == "guide":
                                actor_name = "Dedicated Guide"
                            elif actor_role == "sme":
                                actor_name = "Domain SME"
                            else:
                                actor_name = "System"
                        std_role = get_standard_role_label(actor_role)
                        ev_data = event.get("event_data", {})
                        raw_title = ev_data.get("title") or event.get("event_type") or "Milestone"
                        raw_desc = ev_data.get("description", "")
                        title = _safe_esc(raw_title, default="Milestone")
                        desc = _safe_esc(raw_desc, default="").replace("\n", "<br>")
                        date_display = str(event.get("event_date", ""))[:10]

                        badge_bg = "#6366f1" if actor_role == "aspirant" else "#10b981" if actor_role == "guide" else "#f59e0b" if actor_role == "sme" else "#ec4899" if actor_role == "admin" else "#64748b"

                        is_included = event.get("included_in_roadmap", True) is not False
                        if is_included:
                            status_badge_html = '<div style="margin-bottom:4px;"><span style="display:inline-block; font-size:0.72rem; font-weight:800; padding:2px 8px; border-radius:10px; background:#10B981; color:#ffffff;">✓ Active on Aspirant Roadmap</span></div>'
                        else:
                            status_badge_html = '<div style="margin-bottom:4px;"><span style="display:inline-block; font-size:0.72rem; font-weight:800; padding:2px 8px; border-radius:10px; background:#EF4444; color:#ffffff;">⚠️ Marked \'Not Needed\' by Aspirant</span></div>'

                        col_t, col_b, col_ov = st.columns([1.2, 5.2, 0.8])
                        with col_t:
                            st.markdown(
                                f'<div style="font-weight:700; color:#64748B; font-size:0.9rem;">{date_display}</div>'
                                f'<span style="display:inline-block; font-size:0.7rem; font-weight:800; padding:2px 8px; border-radius:10px; background:{badge_bg}; color:#ffffff; text-transform:uppercase;">{std_role}</span>',
                                unsafe_allow_html=True
                            )
                        with col_b:
                            st.markdown(
                                f'<div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:0.9rem 1.2rem; margin-bottom:0.75rem; box-shadow:0 1px 2px rgba(0,0,0,0.03);">'
                                f'{status_badge_html}'
                                f'<div style="font-weight:700; color:#0F172A; font-size:1.02rem;">{title}</div>'
                                f'<div style="color:#334155; font-size:0.88rem; margin-top:0.25rem; line-height:1.4;">{desc}</div>'
                                f'<div style="font-size:0.75rem; color:#64748B; margin-top:0.35rem;">Contributor: <strong>{actor_name}</strong> ({std_role})</div>'
                                f'</div>',
                                unsafe_allow_html=True
                            )
                        with col_ov:
                            # Admin oversight: Edit correction & removal
                            col_ae, col_ad = st.columns(2)
                            with col_ae:
                                if st.button("✏️", key=f"adm_edit_{event['id']}", help="Administrative correction"):
                                    render_edit_journey_dialog(event, admin_id, "admin")
                            with col_ad:
                                if st.button("🗑️", key=f"adm_del_{event['id']}", help="Administrative removal (Soft Delete)"):
                                    ok, err = soft_delete_event(event["id"], admin_id, "admin")
                                    if ok:
                                        st.session_state["del_event_success"] = "Journey entry removed."
                                    else:
                                        st.session_state["del_event_err"] = err or "Could not remove entry."
                                    st.rerun()

    # ─────────────────────────────────────────────────────────────
    # TAB 2: GUIDES MANAGEMENT & PROVISIONING
    # ─────────────────────────────────────────────────────────────
    with tabs[1]:
        st.subheader("Guides Roster & Account Provisioning")
        st.markdown("<p style='color:#64748B; font-size:0.9rem;'>Guides can ONLY be created by the Admin. Public signup is disabled.</p>", unsafe_allow_html=True)

        with st.expander("➕ Provision New Guide Account", expanded=False):
            if "admin_guide_create_success" in st.session_state:
                _gc_msg = st.session_state.pop("admin_guide_create_success")
                st.success(_gc_msg)
                try:
                    st.toast(_gc_msg, icon="✅")
                except Exception:
                    pass
            with st.form("form_create_guide"):
                col_cg1, col_cg2 = st.columns(2)
                with col_cg1:
                    cg_name = st.text_input("Full Name *", placeholder="e.g. Rajendran / Murugan S.")
                    cg_email = st.text_input("Email *", placeholder="e.g. rajendran@mentor.in")
                    cg_phone = st.text_input("Phone Number", placeholder="9876543211")
                with col_cg2:
                    cg_loc_sel = st.selectbox("Location / District", MASTER_DISTRICTS_TN, index=13, key="cg_loc")
                    cg_loc = cg_loc_sel
                    if cg_loc_sel == "Other District / Non-TN (Specify)":
                        cg_loc_custom = st.text_input("Specify Location / State *", placeholder="e.g. Bengaluru (Karnataka)", key="cg_custom_loc")
                        if cg_loc_custom and cg_loc_custom.strip():
                            cg_loc = cg_loc_custom.strip()
                    cg_exp = st.text_input("Primary Expertise *", placeholder="e.g. PMEGP Loan Specialist, Banking, Food Processing")
                    cg_pwd = st.text_input("Temporary Password", value="Guide@123")
                cg_bio = st.text_area("Professional Background", placeholder="Retired Chief Manager with 30 years experience in MSME lending.")

                if st.form_submit_button("CREATE GUIDE ACCOUNT", type="primary"):
                    if cg_name and cg_email and cg_exp:
                        g_prof, err = admin_create_mentor(
                            admin_user_id=admin_id,
                            role="guide",
                            full_name=cg_name,
                            email=cg_email,
                            phone=cg_phone,
                            location=cg_loc,
                            expertise=cg_exp,
                            temp_password=cg_pwd,
                            bio=cg_bio
                        )
                        if g_prof:
                            st.session_state["admin_guide_create_success"] = f"✅ Guide account '{cg_name}' created successfully! Credentials: {cg_email} / {cg_pwd}"
                            st.rerun()
                        else:
                            st.error(err or "Failed to create guide.")
                    else:
                        st.warning("Please fill in all required fields.")

        # Guides Table
        if not guides:
            st.info("No guides currently registered. Create one above.")
        else:
            for g in guides:
                exp_g = g.get('profile_data', {}).get('expertise', 'Mentorship')
                st.markdown(
                    f'<div style="background:#FFFFFF; border:1px solid #E2E8F0; border-left:4px solid #10b981; border-radius:0 10px 10px 0; padding:1rem; margin-bottom:0.75rem; box-shadow:0 1px 3px rgba(0,0,0,0.04);">'
                    f'<div style="display:flex; justify-content:space-between; align-items:center;">'
                    f'<div>'
                    f'<strong style="color:#0F172A; font-size:1.05rem;">{g["full_name"]}</strong>'
                    f'<span style="color:#059669; font-weight:600; font-size:0.85rem; margin-left:0.5rem;">({g.get("district", "Tamil Nadu")})</span>'
                    f'<div style="color:#475569; font-size:0.85rem; margin-top:0.2rem;">Expertise: {exp_g} | Email: {g["email"]}</div>'
                    f'</div>'
                    f'<span style="background:#ECFDF5; color:#059669; border:1px solid #A7F3D0; font-size:0.75rem; font-weight:800; padding:3px 10px; border-radius:8px;">ACTIVE GUIDE</span>'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

    # ─────────────────────────────────────────────────────────────
    # TAB 3: SMES MANAGEMENT & PROVISIONING
    # ─────────────────────────────────────────────────────────────
    with tabs[2]:
        st.subheader("Subject Matter Experts Roster")
        st.markdown("<p style='color:#64748B; font-size:0.9rem;'>SMEs provide specialized technical, legal, and compliance support (GST, FSSAI, Patents, Legal).</p>", unsafe_allow_html=True)

        with st.expander("➕ Provision New SME Account", expanded=False):
            if "admin_sme_create_success" in st.session_state:
                _sc_msg = st.session_state.pop("admin_sme_create_success")
                st.success(_sc_msg)
                try:
                    st.toast(_sc_msg, icon="✅")
                except Exception:
                    pass
            with st.form("form_create_sme"):
                col_cs1, col_cs2 = st.columns(2)
                with col_cs1:
                    cs_name = st.text_input("Full Name *", placeholder="e.g. Kumar / Priya R.")
                    cs_email = st.text_input("Email *", placeholder="e.g. kumar@sme.in")
                    cs_phone = st.text_input("Phone Number", placeholder="9876543212")
                with col_cs2:
                    cs_loc_sel = st.selectbox("Location / District", MASTER_DISTRICTS_TN, index=13, key="cs_loc")
                    cs_loc = cs_loc_sel
                    if cs_loc_sel == "Other District / Non-TN (Specify)":
                        cs_loc_custom = st.text_input("Specify Location / State *", placeholder="e.g. Mumbai (Maharashtra)", key="cs_custom_loc")
                        if cs_loc_custom and cs_loc_custom.strip():
                            cs_loc = cs_loc_custom.strip()
                    cs_exp = st.text_input("Specialization Domain *", placeholder="e.g. GST Auditing, Taxation, Corporate Compliance")
                    cs_pwd = st.text_input("Temporary Password", value="Sme@123")
                cs_ind = st.text_input("Industry Specialization", placeholder="e.g. Food Processing, Export, Manufacturing")
                cs_bio = st.text_area("Professional Summary", placeholder="Chartered Accountant and GST consultant advising MSMEs for 15 years.")

                if st.form_submit_button("CREATE SME ACCOUNT", type="primary"):
                    if cs_name and cs_email and cs_exp:
                        s_prof, err = admin_create_mentor(
                            admin_user_id=admin_id,
                            role="sme",
                            full_name=cs_name,
                            email=cs_email,
                            phone=cs_phone,
                            location=cs_loc,
                            expertise=cs_exp,
                            temp_password=cs_pwd,
                            bio=cs_bio,
                            industry=cs_ind
                        )
                        if s_prof:
                            st.session_state["admin_sme_create_success"] = f"✅ SME account '{cs_name}' created successfully! Credentials: {cs_email} / {cs_pwd}"
                            st.rerun()
                        else:
                            st.error(err or "Failed to create SME.")
                    else:
                        st.warning("Please fill in required fields.")

        # SMEs Table
        if not smes:
            st.info("No SMEs registered. Create one above.")
        else:
            for s in smes:
                exp_s = s.get('profile_data', {}).get('expertise', 'Advisory')
                st.markdown(
                    f'<div style="background:#FFFFFF; border:1px solid #E2E8F0; border-left:4px solid #f59e0b; border-radius:0 10px 10px 0; padding:1rem; margin-bottom:0.75rem; box-shadow:0 1px 3px rgba(0,0,0,0.04);">'
                    f'<div style="display:flex; justify-content:space-between; align-items:center;">'
                    f'<div>'
                    f'<strong style="color:#0F172A; font-size:1.05rem;">{s["full_name"]}</strong>'
                    f'<span style="color:#D97706; font-weight:600; font-size:0.85rem; margin-left:0.5rem;">({s.get("district", "Tamil Nadu")})</span>'
                    f'<div style="color:#475569; font-size:0.85rem; margin-top:0.2rem;">Domain: {exp_s} | Email: {s["email"]}</div>'
                    f'</div>'
                    f'<span style="background:#FFFBEB; color:#D97706; border:1px solid #FDE68A; font-size:0.75rem; font-weight:800; padding:3px 10px; border-radius:8px;">ACTIVE SME</span>'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

    # ─────────────────────────────────────────────────────────────
    # TAB 4: MENTOR ASSIGNMENTS (Admin Authority)
    # ─────────────────────────────────────────────────────────────
    with tabs[3]:
        st.subheader("🎯 Assign Mentors to Entrepreneurs")
        st.markdown("<p style='color:#64748B; font-size:0.9rem;'>The Admin is the exclusive authority for pairing Aspirants with Guides and SMEs.</p>", unsafe_allow_html=True)

        if not aspirants:
            st.info("No Aspirants available for assignment yet. When entrepreneurs register, you can assign Guides and SMEs to them here.")
        else:
            asp_dict = {a["id"]: f"{a['full_name']} ({a.get('district','Madurai')})" for a in aspirants}
            guide_dict = {g["id"]: f"{g['full_name']} — {g.get('profile_data',{}).get('expertise','Guide')}" for g in guides}
            sme_dict = {s["id"]: f"{s['full_name']} — {s.get('profile_data',{}).get('expertise','SME')}" for s in smes}

            col_as1, col_as2 = st.columns(2)

            with col_as1:
                st.markdown("#### Assign Dedicated Guide")
                if "assign_guide_success" in st.session_state:
                    _g_msg = st.session_state.pop("assign_guide_success")
                    st.success(_g_msg)
                    try:
                        st.toast(_g_msg, icon="✅")
                    except Exception:
                        pass
                with st.form("form_assign_guide"):
                    sel_asp_for_g = st.selectbox("Select Aspirant", list(asp_dict.keys()), format_func=lambda x: asp_dict[x], key="asg_asp_g")
                    if guide_dict:
                        sel_g = st.selectbox("Select Guide", list(guide_dict.keys()), format_func=lambda x: guide_dict[x], key="asg_guide")
                    else:
                        st.warning("No Guides available. Please create a Guide first.")
                        sel_g = None
                    g_notes = st.text_input("Mentorship Directive Notes", placeholder="e.g. Focus on PMEGP loan application & pricing")

                    if st.form_submit_button("ASSIGN GUIDE", type="primary"):
                        if sel_asp_for_g and sel_g:
                            ok, err = assign_guide(sel_asp_for_g, sel_g, admin_id, g_notes)
                            if ok:
                                st.session_state["assign_guide_success"] = f"✅ Guide Assigned: {guide_dict[sel_g]} has been assigned to {asp_dict[sel_asp_for_g]}! Journey event logged."
                                st.rerun()
                            else:
                                st.error(err or "Assignment failed.")

            with col_as2:
                st.markdown("#### Assign Specialized Domain SME")
                if "assign_sme_success" in st.session_state:
                    _s_msg = st.session_state.pop("assign_sme_success")
                    st.success(_s_msg)
                    try:
                        st.toast(_s_msg, icon="✅")
                    except Exception:
                        pass
                with st.form("form_assign_sme"):
                    sel_asp_for_s = st.selectbox("Select Aspirant", list(asp_dict.keys()), format_func=lambda x: asp_dict[x], key="asg_asp_s")
                    if sme_dict:
                        sel_s = st.selectbox("Select SME", list(sme_dict.keys()), format_func=lambda x: sme_dict[x], key="asg_sme")
                    else:
                        st.warning("No SMEs available. Please create an SME first.")
                        sel_s = None
                    sme_asg_mode = st.radio(
                        "Assignment Mode",
                        options=["➕ Add Specialist to Advisory Panel (Concurrent Multi-SME)", "🔄 Replace Existing Specialist"],
                        index=0,
                        help="Choose whether to add this SME alongside other specialists (e.g., GST + Legal + FSSAI) or replace the existing specialist."
                    )
                    s_notes = st.text_input("Specialist Task Notes", placeholder="e.g. Verify GST threshold and draft audit memorandum")

                    if st.form_submit_button("ASSIGN SME", type="primary"):
                        if sel_asp_for_s and sel_s:
                            mode = "add" if "Add" in sme_asg_mode else "replace"
                            ok, err = assign_sme(sel_asp_for_s, sel_s, admin_id, s_notes, mode=mode)
                            if ok:
                                action_desc = "added to advisory panel of" if mode == "add" else "assigned to"
                                st.session_state["assign_sme_success"] = f"✅ SME Assigned: Specialist {sme_dict[sel_s]} {action_desc} {asp_dict[sel_asp_for_s]}! Journey event logged."
                                st.rerun()
                            else:
                                st.error(err or "Assignment failed.")

            st.markdown("---")
            st.markdown("#### 📋 Active Mentorship Allocations & Quick Handover")
            st.markdown("<p style='color:#64748B; font-size:0.85rem;'>Review current Guide and SME allocations. Remove or replace mentors with full audit trail capture, open consultation handover, and immediate cache synchronization.</p>", unsafe_allow_html=True)

            if "unassign_mentor_msg" in st.session_state:
                _u_msg = st.session_state.pop("unassign_mentor_msg")
                st.success(_u_msg)

            active_allocations = []
            seen_alloc_aids = set()
            for a in aspirants:
                aid_curr = a.get("id")
                if not aid_curr or aid_curr in seen_alloc_aids:
                    continue
                seen_alloc_aids.add(aid_curr)
                m = get_aspirant_mentors(aid_curr)
                if m.get("guide") or m.get("sme") or m.get("guides") or m.get("smes"):
                    active_allocations.append((a, m))

            if not active_allocations:
                st.info("No active mentor allocations yet. Pair an entrepreneur using the forms above.")
            else:
                for a_idx, (asp, m) in enumerate(active_allocations):
                    aid = asp["id"]
                    aname = asp.get("full_name", "Entrepreneur")
                    adist = asp.get("district", "Tamil Nadu")

                    with st.expander(f"👤 {aname} ({adist}) — Active Mentors", expanded=False):
                        c_g, c_s = st.columns(2)
                        with c_g:
                            st.markdown("**Dedicated Guide(s)**")
                            guides_raw = m.get("guides", [])
                            if not guides_raw and m.get("guide"):
                                guides_raw = [m["guide"]]

                            # Deduplicate guides by id
                            seen_g_ids = set()
                            guides_list = []
                            for g in guides_raw:
                                if g and g.get("id") and g["id"] not in seen_g_ids:
                                    seen_g_ids.add(g["id"])
                                    guides_list.append(g)

                            if not guides_list:
                                st.caption("No dedicated Guide assigned.")
                            else:
                                for idx, g in enumerate(guides_list):
                                    gid = g.get("id")
                                    gname = g.get("full_name", "Guide")
                                    is_pri = (idx == 0)
                                    tag = "Primary" if is_pri else f"Co-Guide #{idx+1}"
                                    st.markdown(f"• **{gname}** `[{tag}]`")

                                    with st.popover(f"Actions: {gname}", use_container_width=True):
                                        st.markdown(f"**Manage Guide: {gname}**")
                                        reason_g = st.text_input(f"Reason for Removal / Replacement", placeholder="e.g. Founder requested agri-specialist", key=f"r_g_{a_idx}_{aid}_{gid}_{idx}")
                                        
                                        col_b1, col_b2 = st.columns(2)
                                        with col_b1:
                                            if st.button("Unassign Guide", key=f"btn_unassign_g_{a_idx}_{aid}_{gid}_{idx}", type="secondary", use_container_width=True):
                                                ok_u, err_u = unassign_guide(aid, gid, admin_id=admin_id, reason=reason_g)
                                                if ok_u:
                                                    st.session_state["unassign_mentor_msg"] = f"✅ Guide {gname} unassigned from {aname}."
                                                    st.rerun()
                                                else:
                                                    st.error(err_u or "Failed to unassign Guide.")
                                        with col_b2:
                                            replacement_guides = [g_opt for g_opt in list(guide_dict.keys()) if g_opt != gid]
                                            if replacement_guides:
                                                rep_g = st.selectbox("Replace with", replacement_guides, format_func=lambda x: guide_dict[x], key=f"rep_g_sel_{a_idx}_{aid}_{gid}_{idx}")
                                                if st.button("Confirm Replace", key=f"btn_rep_g_{a_idx}_{aid}_{gid}_{idx}", type="primary", use_container_width=True):
                                                    ok_r, err_r = assign_guide(aid, rep_g, admin_id=admin_id, notes=f"Replacement for {gname}. {reason_g}")
                                                    if ok_r:
                                                        st.session_state["unassign_mentor_msg"] = f"✅ Guide {gname} replaced with {guide_dict[rep_g]} for {aname}."
                                                        st.rerun()
                                                    else:
                                                        st.error(err_r or "Replacement failed.")

                        with c_s:
                            st.markdown("**Domain SME(s)**")
                            smes_raw = m.get("smes", [])
                            if not smes_raw and m.get("sme"):
                                smes_raw = [m["sme"]]

                            # Deduplicate SMEs by id
                            seen_s_ids = set()
                            smes_list = []
                            for s in smes_raw:
                                if s and s.get("id") and s["id"] not in seen_s_ids:
                                    seen_s_ids.add(s["id"])
                                    smes_list.append(s)

                            if not smes_list:
                                st.caption("No domain SME assigned.")
                            else:
                                for idx, s in enumerate(smes_list):
                                    sid = s.get("id")
                                    sname = s.get("full_name", "Specialist")
                                    st.markdown(f"• **{sname}** `[Specialist #{idx+1}]`")

                                    with st.popover(f"Actions: {sname}", use_container_width=True):
                                        st.markdown(f"**Manage SME: {sname}**")
                                        reason_s = st.text_input(f"Reason for Removal / Replacement", placeholder="e.g. Advisory milestone completed", key=f"r_s_{a_idx}_{aid}_{sid}_{idx}")

                                        col_sb1, col_sb2 = st.columns(2)
                                        with col_sb1:
                                            if st.button("Unassign SME", key=f"btn_unassign_s_{a_idx}_{aid}_{sid}_{idx}", type="secondary", use_container_width=True):
                                                ok_su, err_su = unassign_sme(aid, sid, admin_id=admin_id, reason=reason_s)
                                                if ok_su:
                                                    st.session_state["unassign_mentor_msg"] = f"✅ Specialist {sname} unassigned from {aname}."
                                                    st.rerun()
                                                else:
                                                    st.error(err_su or "Failed to unassign SME.")
                                        with col_sb2:
                                            replacement_smes = [s_opt for s_opt in list(sme_dict.keys()) if s_opt != sid]
                                            if replacement_smes:
                                                rep_s = st.selectbox("Replace with", replacement_smes, format_func=lambda x: sme_dict[x], key=f"rep_s_sel_{a_idx}_{aid}_{sid}_{idx}")
                                                if st.button("Confirm Replace", key=f"btn_rep_s_{a_idx}_{aid}_{sid}_{idx}", type="primary", use_container_width=True):
                                                    ok_sr, err_sr = assign_sme(aid, rep_s, admin_id=admin_id, notes=f"Replacement for {sname}. {reason_s}", mode="replace")
                                                    if ok_sr:
                                                        st.session_state["unassign_mentor_msg"] = f"✅ Specialist {sname} replaced with {sme_dict[rep_s]} for {aname}."
                                                        st.rerun()
                                                    else:
                                                        st.error(err_sr or "Replacement failed.")

    # ─────────────────────────────────────────────────────────────
    # TAB 5: MENTOR INQUIRIES & ADMINISTRATIVE DIRECTIVES
    # ─────────────────────────────────────────────────────────────
    with tabs[4]:
        subtab_inq, subtab_ssr = st.tabs([
            "🏛️ Mentor Directives & Inquiries",
            "📋 Scheme Support Reviews (Guide Escalations)"
        ])

        with subtab_inq:
            st.subheader("🏛️ Mentor Inquiries & Administrative Directives")
            st.markdown("<p style='color:#64748B; font-size:0.9rem;'>Official Program Directorate Governance: Guides and Domain SMEs submit institutional roadblocks on behalf of their assigned entrepreneurs. Review inquiries, issue binding Administrative Directives, or assign Co-Guides (Guide B) and specialized Domain SMEs. <em>(Strictly invisible to the entrepreneur)</em></p>", unsafe_allow_html=True)

        col_mq1, col_mq2 = st.columns([2, 2])
        with col_mq1:
            st_filter = st.selectbox("Directive Status Filter", ["ALL", "PENDING_ADMIN", "DIRECTIVE_ISSUED", "RESOLVED"], key="admin_dir_st_filter")
        with col_mq2:
            role_filter = st.selectbox("Mentor Role Filter", ["ALL", "guide", "sme"], format_func=lambda x: "All Roles" if x == "ALL" else ("Guides Only" if x == "guide" else "Domain SMEs Only"), key="admin_dir_role_filter")

        all_queries = list_mentor_admin_queries()
        if st_filter != "ALL":
            all_queries = [q for q in all_queries if q.get("status") == st_filter]
        if role_filter != "ALL":
            all_queries = [q for q in all_queries if (q.get("requester_role_actual") or q.get("requester_role")) == role_filter]

        if not all_queries:
            st.info("No mentor administrative inquiries currently recorded matching the filter criteria.")
        else:
            # Build Guide and SME lookup dictionaries for co-assignment options
            guides_list = list_profiles_by_role("guide")
            smes_list = list_profiles_by_role("sme")
            guide_options = {"NONE": "None (Keep Current Mentorship Team)"}
            for g in guides_list:
                guide_options[g["id"]] = f"{g['full_name']} ({g.get('district', 'Tamil Nadu')})"
            sme_options = {"NONE": "None (No Additional Domain SME)"}
            for s in smes_list:
                sme_options[s["id"]] = f"{s['full_name']} — {s.get('profile_data',{}).get('expertise', 'Specialist')}"

            for query in all_queries:
                q_id = query["id"]
                q_status = query.get("status", "PENDING_ADMIN")
                st_color = "#f59e0b" if q_status == "PENDING_ADMIN" else "#10b981"
                mentor_role_lbl = (query.get("requester_role_actual") or query.get("requester_role") or "guide").upper()
                mentor_name = query.get("requester_name") or "Mentor"
                asp_name = query.get("aspirant_name") or "Entrepreneur"
                q_sub = _safe_esc(query.get("subject"), default="Institutional Query")
                q_priority = query.get("priority", "MEDIUM")

                with st.expander(f"[{q_status}] For Mentee: {asp_name} | From {mentor_role_lbl}: {mentor_name} — {q_sub} ({q_priority})", expanded=(q_status == "PENDING_ADMIN")):
                    q_card_html = (
                        f'<div style="background:#F8FAFC; border:1px solid #E2E8F0; border-left:4px solid {st_color}; border-radius:0 8px 8px 0; padding:0.9rem 1.1rem; margin-bottom:0.75rem;">'
                        f'<div style="display:flex; justify-content:space-between; align-items:center;">'
                        f'<div style="font-weight:800; color:#0F172A; font-size:1.05rem;">{q_sub}</div>'
                        f'<div style="font-size:0.8rem; color:#64748B;">Submitted: {str(query.get("created_at",""))[:16]}</div>'
                        f'</div>'
                        f'<div style="font-size:0.85rem; color:#475569; margin:4px 0;">'
                        f'Submitted by: <strong>{mentor_name}</strong> ({mentor_role_lbl}) on behalf of entrepreneur: <strong style="color:#0F172A;">{asp_name}</strong>'
                        f'</div>'
                        f'<div style="font-size:0.92rem; color:#1E293B; margin-top:0.5rem; line-height:1.5;">'
                        f'{_safe_esc(query.get("message"), default="").replace(chr(10), "<br>")}'
                        f'</div>'
                        f'</div>'
                    )
                    st.markdown(q_card_html, unsafe_allow_html=True)

                    if query.get("admin_directive"):
                        ad_msg = _safe_esc(query.get("admin_directive"), default="").replace(chr(10), "<br>")
                        ad_issued = str(query.get("directive_issued_at", ""))[:16]
                        dir_card_html = (
                            f'<div style="background:#F0FDF4; border:1px solid #86EFAC; border-left:4px solid #16A34A; border-radius:0 8px 8px 0; padding:0.75rem 1rem; margin-bottom:0.75rem;">'
                            f'<div style="font-weight:800; color:#15803D; font-size:0.88rem; display:flex; justify-content:space-between;">'
                            f'<span>🏛️ Issued Directorate Directive</span>'
                            f'<span style="font-size:0.75rem; color:#166534; font-weight:600;">Issued: {ad_issued}</span>'
                            f'</div>'
                            f'<div style="font-size:0.9rem; color:#14532D; margin-top:0.35rem; line-height:1.5;">'
                            f'{ad_msg}'
                            f'</div>'
                            f'</div>'
                        )
                        st.markdown(dir_card_html, unsafe_allow_html=True)

                    if f"admin_inquiry_directive_success_{q_id}" in st.session_state:
                        _dq_msg = st.session_state.pop(f"admin_inquiry_directive_success_{q_id}")
                        st.success(_dq_msg)
                        try:
                            st.toast(_dq_msg, icon="✅")
                        except Exception:
                            pass

                    with st.form(f"form_admin_dir_{q_id}"):
                        st.markdown("##### 🏛️ Issue Official Administrative Directive")
                        st.caption("The directive will be dispatched directly to the mentor. The entrepreneur will never see this administrative communication.")

                        col_d1, col_d2 = st.columns([1, 2])
                        with col_d1:
                            status_choices = ["DIRECTIVE_ISSUED", "RESOLVED", "PENDING_ADMIN"]
                            cur_st_idx = status_choices.index(q_status) if q_status in status_choices else 0
                            new_st = st.selectbox("Directive Status", status_choices, index=cur_st_idx, key=f"dir_st_{q_id}")
                        with col_d2:
                            directive_text = st.text_area("Administrative Directive / Resolution Instructions *", value=query.get("admin_directive") or "", placeholder="e.g. Approved DIC fast-track liaison. Authorized subsidy exception. Assigned Co-Guide B to oversee bank sanction documents. Guide to communicate milestones to founder.", height=80, key=f"dir_txt_{q_id}")

                        st.markdown("###### 🤝 Operational Support Options (Assign on Behalf of Mentee)")
                        col_asg1, col_asg2 = st.columns(2)
                        with col_asg1:
                            sel_co_guide = st.selectbox("Assign / Consult Co-Guide (Guide B)", list(guide_options.keys()), format_func=lambda x: guide_options[x], key=f"dir_cog_{q_id}", help="Adds an additional Guide to the entrepreneur's roster (as Guide B) without removing primary Guide A.")
                        with col_asg2:
                            sel_add_sme = st.selectbox("Assign / Add Domain Specialist (SME)", list(sme_options.keys()), format_func=lambda x: sme_options[x], key=f"dir_sme_{q_id}", help="Adds a domain specialist (GST, Legal, FSSAI, Patents) to the entrepreneur's advisory panel.")

                        if st.form_submit_button("ISSUE DIRECTIVE & UPDATE", type="primary"):
                            if not directive_text.strip():
                                st.warning("Please enter the directive instructions for the mentor.")
                            else:
                                co_g_val = sel_co_guide if sel_co_guide != "NONE" else None
                                sme_val = sel_add_sme if sel_add_sme != "NONE" else None
                                ok, err = admin_respond_to_mentor(
                                    query_id=q_id,
                                    admin_id=admin_id,
                                    directive=directive_text.strip(),
                                    new_status=new_st,
                                    assign_co_guide_id=co_g_val,
                                    assign_sme_id=sme_val
                                )
                                if ok:
                                    st.session_state[f"admin_inquiry_directive_success_{q_id}"] = f"Directive recorded and dispatched to {mentor_name} ({mentor_role_lbl})!"
                                    st.rerun()
                                else:
                                    st.error(err or "Failed to issue directive.")

        with subtab_ssr:
            st.subheader("📋 Scheme Support Reviews & Authoritative Exceptions")
            st.markdown("<p style='color:#64748B; font-size:0.9rem;'>Caseload Guides escalate high-potential opportunities that require administrative evaluation or policy exceptions. Review guide justifications, inspect match scores, and approve or reject schemes.</p>", unsafe_allow_html=True)

            from services.scheme_reviews import list_scheme_support_reviews, decide_scheme_support_review

            ssr_list = list_scheme_support_reviews()
            ssr_pending = [r for r in ssr_list if r.get("status") == "PENDING"]
            ssr_approved = [r for r in ssr_list if r.get("status") == "APPROVED"]
            ssr_rejected = [r for r in ssr_list if r.get("status") == "REJECTED"]

            c_sr1, c_sr2, c_sr3 = st.columns(3)
            c_sr1.metric("Pending Review", len(ssr_pending))
            c_sr2.metric("Approved", len(ssr_approved))
            c_sr3.metric("Rejected", len(ssr_rejected))

            ssr_filter = st.selectbox("Review Status Filter", ["ALL", "PENDING", "APPROVED", "REJECTED"], key="adm_ssr_filter")
            filtered_reviews = ssr_list
            if ssr_filter != "ALL":
                filtered_reviews = [r for r in ssr_list if r.get("status") == ssr_filter]

            if not filtered_reviews:
                st.info("No scheme support review requests found.")
            else:
                for rev in filtered_reviews:
                    rev_id = rev["id"]
                    r_status = rev.get("status", "PENDING")
                    badge_color = "#F59E0B" if r_status == "PENDING" else ("#10B981" if r_status == "APPROVED" else "#DC2626")

                    with st.expander(f"{rev.get('scheme_name', 'Scheme')} · {rev.get('aspirant_name', 'Founder')} [{r_status}]", expanded=(r_status == "PENDING")):
                        st.markdown(f"""
                        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-left:4px solid {badge_color}; border-radius:10px; padding:1rem; margin-bottom:0.75rem;">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <div>
                                    <div style="font-weight:800; font-size:1.1rem; color:#0F172A;">{_safe_esc(rev.get('scheme_name'))}</div>
                                    <div style="font-size:0.84rem; color:#64748B;">{_safe_esc(rev.get('scheme_agency'))} · Funding: <strong>{_safe_esc(rev.get('scheme_amount'))}</strong></div>
                                </div>
                                <span style="background:{badge_color}; color:#fff; font-weight:800; font-size:0.8rem; padding:3px 10px; border-radius:10px;">{r_status}</span>
                            </div>
                            <div style="margin-top:0.6rem; font-size:0.88rem; color:#334155;">
                                <strong>Entrepreneur:</strong> {_safe_esc(rev.get('aspirant_name'))} ({_safe_esc(rev.get('aspirant_email'))})<br>
                                <strong>Requesting Guide:</strong> {_safe_esc(rev.get('guide_name'))} ({_safe_esc(rev.get('guide_email'))})<br>
                                <strong>Algorithm Match Score:</strong> {rev.get('match_score', 0)}%
                            </div>
                            <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:0.75rem; margin-top:0.6rem; font-size:0.86rem; color:#1E293B;">
                                <strong>Guide Justification:</strong><br>
                                {_safe_esc(rev.get('guide_justification'))}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        if rev.get("admin_decision_notes"):
                            st.info(f"Administrative Decision Notes: {rev.get('admin_decision_notes')}")

                        if r_status == "PENDING":
                            with st.form(f"form_decide_ssr_{rev_id}"):
                                decision = st.radio("Decision", ["APPROVED", "REJECTED"], horizontal=True, key=f"rad_dec_{rev_id}")
                                notes = st.text_area("Administrative Audit Decision Notes *", placeholder="Explain reason for approval or rejection...", height=70, key=f"notes_dec_{rev_id}")
                                if st.form_submit_button("Record Decision & Notify Guide", type="primary"):
                                    if not notes.strip() or len(notes.strip()) < 5:
                                        st.warning("Please provide decision notes (minimum 5 characters).")
                                    else:
                                        ok_d, err_d = decide_scheme_support_review(rev_id, decision, notes.strip(), admin_id)
                                        if ok_d:
                                            st.success(f"Review decision '{decision}' recorded!")
                                            st.rerun()
                                        else:
                                            st.error(err_d or "Failed to record decision.")

    # ─────────────────────────────────────────────────────────────
    # TAB 6: SCHEME CATALOGUE CRUD
    # ─────────────────────────────────────────────────────────────
    with tabs[5]:
        st.subheader(f"Scheme Catalogue Management ({len(all_schemes)} Records in Intelligence Database)")
        st.markdown("<p style='color:#64748B; font-size:0.9rem;'>Full Administrative Authority: Search, filter, add new schemes, edit existing guidelines, toggle archive status, or permanently delete schemes from both local and cloud databases.</p>", unsafe_allow_html=True)

        # ── 1. ADD NEW SCHEME EXPANDER ──
        with st.expander("➕ Add New Scheme / Fund to Catalogue", expanded=False):
            with st.form("form_add_new_scheme"):
                st.markdown("##### Basic Information & Capital Structure")
                c_ns1, c_ns2 = st.columns(2)
                with c_ns1:
                    ns_name = st.text_input("Scheme / Fund Name *", placeholder="e.g. IndiaAI Mission Compute & Startup Support")
                    ns_agency = st.text_input("Agency / Ministry / Firm *", placeholder="e.g. MeitY (Ministry of Electronics and IT)")
                    ns_amount = st.text_input("Funding Amount *", placeholder="e.g. Up to 40% compute GPU subsidy + Rs 1 Crore grant")
                    ns_type_sel = st.selectbox("Funding / Capital Type", MASTER_FUNDING_TYPES)
                    ns_custom_type = ""
                    if ns_type_sel == "Other / Blended Capital (Specify)":
                        ns_custom_type = st.text_input("Specify Custom Capital Type *", placeholder="e.g. SAFE, Revenue Share", key="ns_custom_type")
                with c_ns2:
                    ns_cat_sel = st.selectbox("Category", MASTER_CATEGORY_TYPES)
                    ns_custom_cat = ""
                    if ns_cat_sel == "Other / Consortium (Specify)":
                        ns_custom_cat = st.text_input("Specify Custom Category *", placeholder="e.g. Global Consortium", key="ns_custom_cat")
                    ns_stage_sel = st.selectbox("Eligible Stage", MASTER_STAGES)
                    ns_custom_stage = ""
                    if ns_stage_sel == "Other / Multi-Stage (Specify)":
                        ns_custom_stage = st.text_input("Specify Custom Stage *", placeholder="e.g. Commercialization Phase", key="ns_custom_stage")
                    ns_scope_sel = st.selectbox("State Scope / Geography", MASTER_GEOGRAPHIC_SCOPES)
                    ns_custom_scope = ""
                    if ns_scope_sel == "Other / Specific Region (Specify)":
                        ns_custom_scope = st.text_input("Specify Custom Geography *", placeholder="e.g. South India / Tier 2 Cities", key="ns_custom_scope")
                    ns_url = st.text_input("Official Portal URL", placeholder="https://indiaai.gov.in")

                ns_sectors_sel = st.multiselect("Eligible Sectors *", MASTER_SECTORS, default=["Cross-Sector / All Sectors"])
                ns_custom_sec = ""
                if "Other / Not Listed (Specify)" in ns_sectors_sel:
                    ns_custom_sec = st.text_input("Specify Custom Sectors (comma-separated) *", placeholder="e.g. SpaceTech, Marine Culture", key="ns_custom_sec")

                c_ns3, c_ns4 = st.columns(2)
                with c_ns3:
                    ns_brief = st.text_input("One-line Brief", placeholder="Compute infrastructure subsidies and grant support for AI startups.")
                with c_ns4:
                    ns_desc = st.text_area("Full Description / Details", placeholder="Access to 10,000+ GPUs onboarded via empaneled providers plus cohort grants for AI ventures building sovereign IP.", height=68)

                st.markdown("##### Intelligence, Red Flags & Application Prompt")
                ns_agenda = st.text_area("🤫 Insider Intelligence / Hidden Agenda (One point per line)", placeholder=">> MeitY wants SOVEREIGN AI & Indigenous IP - show how your model reduces reliance on foreign foundations.\n>> Emphasize local Indian compute residency.")
                ns_flags = st.text_area("⚠️ Red Flags / Warnings (One point per line)", placeholder="!! Do not submit wrapper apps with no unique data or IP - auto-rejected.\n!! High technical bar during empaneled panel review.")
                ns_prompt = st.text_area("🤖 AI Pitch & Application Prompt (Template for founders)", placeholder="ROLE: Senior Startup Funding & VC Consultant\nTARGET FUND: [Fund Name]...", height=120)

                if st.form_submit_button("ADD SCHEME TO CATALOGUE", type="primary"):
                    if ns_name and ns_agency:
                        import uuid
                        final_type = ns_custom_type.strip() if (ns_type_sel == "Other / Blended Capital (Specify)" and ns_custom_type.strip()) else ns_type_sel
                        final_cat = ns_custom_cat.strip() if (ns_cat_sel == "Other / Consortium (Specify)" and ns_custom_cat.strip()) else ns_cat_sel
                        final_stage = ns_custom_stage.strip() if (ns_stage_sel == "Other / Multi-Stage (Specify)" and ns_custom_stage.strip()) else ns_stage_sel
                        final_scope = ns_custom_scope.strip() if (ns_scope_sel == "Other / Specific Region (Specify)" and ns_custom_scope.strip()) else ns_scope_sel

                        final_sectors = [s for s in ns_sectors_sel if s != "Other / Not Listed (Specify)"]
                        if ns_custom_sec and ns_custom_sec.strip():
                            final_sectors.extend([x.strip() for x in ns_custom_sec.split(",") if x.strip()])
                        if not final_sectors:
                            final_sectors = ["Cross-Sector / All Sectors"]

                        new_agenda = [x.strip() for x in ns_agenda.split("\n") if x.strip()] if ns_agenda else [">> High impact venture creation."]
                        new_flags = [x.strip() for x in ns_flags.split("\n") if x.strip()] if ns_flags else ["!! Review official guidelines before applying."]
                        new_s_obj = {
                            "id": f"SCH-ADMIN-{uuid.uuid4().hex[:8].upper()}",
                            "name": ns_name,
                            "agency": ns_agency,
                            "category_type": final_cat,
                            "funding_type": final_type,
                            "scheme_type": final_type,
                            "stage": final_stage,
                            "amount": ns_amount,
                            "brief": ns_brief or ns_name,
                            "description": ns_desc or ns_brief or ns_name,
                            "sectors": final_sectors,
                            "hidden_agenda": new_agenda,
                            "red_flags": new_flags,
                            "application_prompt": ns_prompt or f"ROLE: Senior Startup Funding & VC Consultant\nTARGET FUND: {ns_name} ({ns_agency})\nFUND TYPE: {final_type}",
                            "state_scope": final_scope,
                            "geography": "National" if final_scope == "All India" else "State",
                            "application_url": ns_url,
                            "last_verified": "September 2026",
                            "is_active": True,
                            "status": "active",
                            "source_dataset": "Manual Admin Addition"
                        }
                        ok, err = upsert_scheme(new_s_obj, admin_id)
                        if ok:
                            st.success(f"Added '{ns_name}' to catalogue!")
                            st.rerun()
                        else:
                            st.error(err or "Failed to add scheme.")
                    else:
                        st.warning("Scheme Name and Agency are required.")

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        # ── 2. SEARCH & MULTI-FACET FILTERS ──
        c_f1, c_f2, c_f3, c_f4 = st.columns([2.5, 1.2, 1.2, 1.1])
        with c_f1:
            sc_search = st.text_input("🔍 Search Funds & Schemes", placeholder="Search by name, agency, keyword (e.g. IndiaAI, DLI, Accel, NEEDS, PMEGP, TANSEED)...", key="adm_sc_search")
        with c_f2:
            sc_cat = st.selectbox("Category", ["ALL"] + MASTER_CATEGORY_TYPES, key="adm_sc_cat")
        with c_f3:
            sc_stage = st.selectbox("Stage", ["ALL"] + MASTER_STAGES, key="adm_sc_stage")
        with c_f4:
            sc_status = st.selectbox("Status", ["ALL", "Active Only", "Archived Only"], key="adm_sc_status")

        active_filter = None if sc_status == "ALL" else True if sc_status == "Active Only" else False
        all_matches = list_schemes(search=sc_search, category=sc_cat, stage=sc_stage, active_only=False)

        if active_filter is not None:
            all_matches = [s for s in all_matches if s.get("is_active", True) == active_filter]

        total_count = len(all_matches)

        # ── 3. PAGINATION & PAGE SIZE ──
        c_bar1, c_bar2 = st.columns([2.5, 1.5])
        with c_bar1:
            st.markdown(f"**Found {total_count} schemes matching filter.**")
        with c_bar2:
            page_size_option = st.selectbox("Schemes per page", [15, 30, 50, 100, f"Show All ({total_count})"], index=1, key="adm_page_size")

        if str(page_size_option).startswith("Show All"):
            page_size = total_count if total_count > 0 else 1
        else:
            page_size = int(page_size_option)

        import math
        total_pages = max(1, math.ceil(total_count / page_size)) if total_count > 0 else 1

        if "adm_scheme_page" not in st.session_state:
            st.session_state.adm_scheme_page = 1
        if st.session_state.adm_scheme_page > total_pages:
            st.session_state.adm_scheme_page = 1

        c_p1, c_p2, c_p3 = st.columns([1, 2, 1])
        with c_p1:
            if st.button("◀ Previous Page", disabled=(st.session_state.adm_scheme_page <= 1), use_container_width=True, key="adm_sc_btn_prev"):
                st.session_state.adm_scheme_page -= 1
                st.rerun()
        with c_p2:
            st.markdown(f"<div style='text-align:center; padding-top:6px; font-weight:600; color:#475569;'>Page {st.session_state.adm_scheme_page} of {total_pages} ({total_count} Total Schemes)</div>", unsafe_allow_html=True)
        with c_p3:
            if st.button("Next Page ▶", disabled=(st.session_state.adm_scheme_page >= total_pages), use_container_width=True, key="adm_sc_btn_next"):
                st.session_state.adm_scheme_page += 1
                st.rerun()

        start_idx = (st.session_state.adm_scheme_page - 1) * page_size
        end_idx = start_idx + page_size
        page_schemes = all_matches[start_idx:end_idx]

        if not page_schemes:
            st.info("No schemes match your search criteria. Try clearing search keywords or resetting filters.")
        else:
            # ── 4. RICH PLAYBOOK FUND EXPLORER CARDS WITH FULL EDIT & DELETE (3-COLUMN GRID) ──
            cols_per_row = 3
            for i in range(0, len(page_schemes), cols_per_row):
                row_schemes = page_schemes[i : i + cols_per_row]
                cols = st.columns(3)
                for j, s in enumerate(row_schemes):
                    with cols[j]:
                        render_fund_explorer_card(s, is_admin=True, admin_id=admin_id, key_prefix=f"adm_sc_{s['id']}")

    # ─────────────────────────────────────────────────────────────
    # TAB 7: MULTI-ROLE GRANTS & IDENTITY
    # ─────────────────────────────────────────────────────────────
    with tabs[6]:
        if is_tab_active(tabs[6]):
            render_admin_role_grants_tab(admin_id)

    # ─────────────────────────────────────────────────────────────
    # TAB 8: LEGAL AGREEMENTS & NDA RECORDS
    # ─────────────────────────────────────────────────────────────
    with tabs[7]:
        if is_tab_active(tabs[7]):
            render_admin_legal_records_tab()

    # ─────────────────────────────────────────────────────────────
    # TAB 9: CONFIDENTIAL GUIDE COMPLAINTS
    # ─────────────────────────────────────────────────────────────
    with tabs[8]:
        if is_tab_active(tabs[8]):
            render_admin_complaints_tab(admin_id)

    # ─────────────────────────────────────────────────────────────
    # TAB 10: CASELOAD INACTIVITY MONITOR
    # ─────────────────────────────────────────────────────────────
    with tabs[9]:
        if is_tab_active(tabs[9]):
            render_admin_inactivity_tab(admin_id)

    # ─────────────────────────────────────────────────────────────
    # TAB 11: CONTACT ASPIRANTS (WHATSAPP & GMAIL ENGAGEMENT)
    # ─────────────────────────────────────────────────────────────
    with tabs[10]:
        if is_tab_active(tabs[10]):
            render_admin_contact_aspirants_tab(admin_id, aspirants)

    # ─────────────────────────────────────────────────────────────
    # TAB 12: SME CONFLICT GOVERNANCE
    # ─────────────────────────────────────────────────────────────
    with tabs[11]:
        if is_tab_active(tabs[11]):
            render_admin_sme_conflicts_tab(admin_id)
