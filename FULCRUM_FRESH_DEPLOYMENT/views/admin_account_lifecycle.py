"""
views/admin_account_lifecycle.py — Account Lifecycle & Archive Administration Surface
======================================================================================
Canonical implementation of the 13th Administrative Governance Area for FULCRUM-INDIA:
- Subtab 1: Active Accounts (Search, Role/District filters, Impact Preview, Pause, Archive, Closure)
- Subtab 2: Archived Accounts (Identity, Preserved Case Counts, Safe Restore under original UUID)
- Subtab 3: Pending Deletion (30-Day Cancellation Grace Window, Retention Blockers, Legal Hold)
- Subtab 4: Account Action History (Immutable, Chronological Audit Timeline)
"""

import streamlit as st
from datetime import datetime, timezone
from typing import Optional, List, Dict

from services.cache import is_tab_active, get_memo, set_memo, invalidate_memo
from services.roles import (
    is_strict_admin,
    require_sole_admin,
    get_user_roles,
    get_active_roles,
    list_users_with_multi_roles,
    SOLE_ADMIN_EMAIL,
    SOLE_ADMIN_UUID,
)
from services.account_lifecycle import (
    get_account_status,
    is_account_active,
    suspend_account,
    resume_account,
    get_archive_impact_preview,
    archive_account,
    restore_account,
    request_account_deletion,
    cancel_account_deletion,
    set_legal_hold,
    list_account_lifecycle_logs,
    list_accounts_by_status,
)
from services.profiles import get_profile
from services.legal import check_user_nda_accepted


def render_admin_account_lifecycle_tab(admin_id: str):
    """
    Renders Tab 13: Account Lifecycle & Archive governance console.
    Strictly restricted to Sole Platform Administrator (fulcrumindia1@gmail.com).
    """
    st.subheader("🗄️ Account Lifecycle & Archive Management")
    st.markdown("""
    <p style='color: #475569; font-size: 0.92rem; margin-bottom: 1.25rem;'>
        Authoritative Account Lifecycle Administration: Pause active accounts, perform safe mentor handovers before archival,
        manage 30-day closure review windows, apply institutional legal holds, and safely restore accounts under their original immutable UUIDs.
        <em>Historical Journeys, Consultations, and Legal records are perpetually preserved.</em>
    </p>
    """, unsafe_allow_html=True)

    # Server-side sole admin verification gate
    ok_admin, err_admin = require_sole_admin(actor_id=admin_id)
    if not ok_admin:
        st.error(err_admin or "Unauthorized access.")
        return

    # Subtabs
    sub_active, sub_archived, sub_pending, sub_history = st.tabs([
        "🟢 Active Accounts",
        "🗄️ Archived Accounts",
        "⏳ Pending Deletion (Grace Review)",
        "📜 Account Action History"
    ], on_change="rerun", key="admin_lifecycle_subtabs")

    # ─────────────────────────────────────────────────────────────────────────
    # SUBTAB 1: ACTIVE ACCOUNTS (Lazy rendered)
    # ─────────────────────────────────────────────────────────────────────────
    with sub_active:
        if is_tab_active(sub_active):
            render_subtab_active_accounts(admin_id)

    # ─────────────────────────────────────────────────────────────────────────
    # SUBTAB 2: ARCHIVED ACCOUNTS (Lazy rendered)
    # ─────────────────────────────────────────────────────────────────────────
    with sub_archived:
        if is_tab_active(sub_archived):
            render_subtab_archived_accounts(admin_id)

    # ─────────────────────────────────────────────────────────────────────────
    # SUBTAB 3: PENDING DELETION (Lazy rendered)
    # ─────────────────────────────────────────────────────────────────────────
    with sub_pending:
        if is_tab_active(sub_pending):
            render_subtab_pending_deletion(admin_id)

    # ─────────────────────────────────────────────────────────────────────────
    # SUBTAB 4: ACCOUNT ACTION HISTORY (Lazy rendered)
    # ─────────────────────────────────────────────────────────────────────────
    with sub_history:
        if is_tab_active(sub_history):
            render_subtab_action_history(admin_id)


def render_subtab_active_accounts(admin_id: str):
    st.markdown("### 🟢 Active & Paused Accounts Directory")

    from services.pagination import paginate_accounts, render_pagination_controls

    cur_page = st.session_state.get("alc_act_page", 1)

    # Filters
    col_f1, col_f2 = st.columns([3, 1])
    with col_f1:
        search_query = st.text_input("🔍 Search by Name or Email", placeholder="e.g. Pravin, Madurai, email@domain.in", key="alc_search_active")
    with col_f2:
        status_filter = st.selectbox("Status Filter", ["active_and_paused", "ACTIVE", "TEMPORARILY_SUSPENDED"], format_func=lambda x: "All Active & Paused" if x == "active_and_paused" else x, key="alc_status_active")

    filtered, total_count = paginate_accounts(status=status_filter, page=cur_page, page_size=25, search=search_query)

    st.caption(f"Showing page {cur_page} ({len(filtered)} of {total_count} accounts matching filters).")

    if not filtered and total_count == 0:
        st.info("No accounts match your criteria.")
        return

    for u in filtered:
        uid = u["id"]
        uname = u.get("full_name") or "User"
        uemail = u.get("email") or ""
        udist = u.get("district") or "Tamil Nadu"
        ustatus = str(u.get("account_status", "ACTIVE")).upper()
        uheld = bool(u.get("legal_hold", False))
        is_sole_admin = is_strict_admin(user_id=uid, email=uemail)

        # Card container
        border_color = "#3B82F6" if ustatus == "ACTIVE" else "#F59E0B"
        badge_html = f'<span style="background:{"#DCFCE7" if ustatus == "ACTIVE" else "#FEF3C7"}; color:{"#15803D" if ustatus == "ACTIVE" else "#B45309"}; font-size:0.75rem; font-weight:700; padding:2px 8px; border-radius:6px;">{"🟢 ACTIVE" if ustatus == "ACTIVE" else "⏸️ SUSPENDED"}</span>'
        hold_html = '<span style="background:#FEE2E2; color:#B91C1C; font-size:0.75rem; font-weight:700; padding:2px 8px; border-radius:6px;">⚖️ LEGAL HOLD</span>' if uheld else ''
        card_html = (
            f'<div style="background:#FFFFFF; border:1px solid #E2E8F0; border-left:4px solid {border_color}; border-radius:10px; padding:1.1rem 1.3rem; margin-bottom:1rem; box-shadow:0 1px 3px rgba(0,0,0,0.04);">'
            f'<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">'
            f'<div><span style="font-weight:800; color:#0F172A; font-size:1.05rem;">{uname}</span>'
            f'<span style="color:#64748B; font-size:0.86rem; margin-left:8px;">({uemail})</span>'
            f'<span style="color:#94A3B8; font-size:0.82rem; margin-left:8px;">📍 {udist}</span></div>'
            f'<div style="display:flex; gap:6px; align-items:center;">{badge_html}{hold_html}</div>'
            f'</div></div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)

        with st.expander(f"⚙️ Manage Lifecycle: {uname}", expanded=False):
            if is_sole_admin:
                st.info("🛡️ This is the Sole Platform Administrator account. Administrative safeguards prevent suspension or archival of this root identity.")
                continue

            preview = get_archive_impact_preview(uid)
            c_p1, c_p2, c_p3 = st.columns(3)
            with c_p1:
                st.caption(f"**Guide Caseload:** {preview.get('assigned_guide_cases_count', 0)} Cases")
                if preview.get("orphaned_guide_cases_count", 0) > 0:
                    st.warning(f"⚠️ {preview['orphaned_guide_cases_count']} case(s) have no remaining co-guide!")
            with c_p2:
                st.caption(f"**SME Advisories:** {preview.get('assigned_sme_cases_count', 0)} Panels")
            with c_p3:
                st.caption(f"**Open Consultations:** {preview.get('open_consultations_count', 0)} Pending")

            st.write("")
            col_act1, col_act2, col_act3, col_act4 = st.columns(4)

            # 1. Pause / Resume Button
            with col_act1:
                if ustatus == "ACTIVE":
                    pause_reason = st.text_input("Suspension Reason", key=f"pause_rsn_{uid}", placeholder="e.g. Conduct review, leave")
                    if st.button("⏸️ Pause Account", key=f"btn_pause_{uid}", use_container_width=True):
                        if not pause_reason.strip():
                            st.warning("Please provide a suspension reason.")
                        else:
                            ok_s, err_s = suspend_account(uid, pause_reason.strip(), actor_id=admin_id)
                            if ok_s:
                                st.success("Account temporarily suspended.")
                                st.rerun()
                            else:
                                st.error(err_s or "Failed to suspend account.")
                else:
                    resume_reason = st.text_input("Resumption Note", key=f"res_rsn_{uid}", placeholder="e.g. Cleared for return")
                    if st.button("▶️ Resume Account", key=f"btn_res_{uid}", type="primary", use_container_width=True):
                        ok_r, err_r = resume_account(uid, actor_id=admin_id, reason=resume_reason.strip())
                        if ok_r:
                            st.success("Account resumed to active status.")
                            st.rerun()
                        else:
                            st.error(err_r or "Failed to resume account.")

            # 2. Archive Account Button
            with col_act2:
                arc_reason = st.text_input("Archival Reason", key=f"arc_rsn_{uid}", placeholder="e.g. Departure, inactive >180d")
                if st.button("🗄️ Archive Account", key=f"btn_arc_{uid}", use_container_width=True):
                    if not arc_reason.strip():
                        st.warning("Please provide an archival reason.")
                    else:
                        ok_a, err_a = archive_account(uid, arc_reason.strip(), actor_id=admin_id)
                        if ok_a:
                            st.success(f"Account for {uname} archived. Active cases safely handed over.")
                            st.rerun()
                        else:
                            st.error(err_a or "Failed to archive account.")

            # 3. Schedule Deletion (30-day review period)
            with col_act3:
                del_reason = st.text_input("Closure Reason", key=f"del_rsn_{uid}", placeholder="e.g. Requested account closure")
                if st.button("📅 Schedule Closure (30d)", key=f"btn_del_{uid}", use_container_width=True):
                    if not del_reason.strip():
                        st.warning("Please provide a closure reason.")
                    else:
                        ok_d, err_d = request_account_deletion(uid, actor_id=admin_id, reason=del_reason.strip(), grace_days=30)
                        if ok_d:
                            st.success(f"Closure scheduled with 30-day review period. Permanent purge is not automatic.")
                            st.rerun()
                        else:
                            st.error(err_d or "Failed to schedule closure.")

            # 4. Legal Hold Toggle
            with col_act4:
                hold_reason = st.text_input("Legal Hold Note", key=f"hold_rsn_{uid}", placeholder="e.g. Formal audit hold")
                btn_hold_label = "⚖️ Release Legal Hold" if uheld else "⚖️ Apply Legal Hold"
                if st.button(btn_hold_label, key=f"btn_hold_{uid}", use_container_width=True):
                    if not hold_reason.strip():
                        st.warning("Please provide a legal hold note.")
                    else:
                        ok_h, err_h = set_legal_hold(uid, enabled=(not uheld), reason=hold_reason.strip(), actor_id=admin_id)
                        if ok_h:
                            st.success("Legal hold status updated.")
                            st.rerun()
                        else:
                            st.error(err_h or "Failed to update legal hold.")

    if total_count > 25:
        render_pagination_controls(total_count, cur_page, page_size=25, key_prefix="alc_act")


def render_subtab_archived_accounts(admin_id: str):
    st.markdown("### 🗄️ Archived Accounts Registry")
    st.markdown("""
    <p style='color:#64748B; font-size:0.88rem;'>
        Archived accounts are dormant and blocked from logging in.
        All historical Journey records, past consultations, and verified legal attestations are preserved.
        <strong>Restoration preserves the user's original UUID and identity, without automatically reclaiming old caseloads or restoring revoked roles.</strong>
    </p>
    """, unsafe_allow_html=True)

    from services.pagination import paginate_accounts, render_pagination_controls

    cur_arc_page = st.session_state.get("alc_arc_page", 1)
    arc_search = st.text_input("🔍 Search Archived Accounts", placeholder="Search by name or email...", key="alc_search_archived")

    archived_users, total_archived = paginate_accounts(status="ARCHIVED", page=cur_arc_page, page_size=25, search=arc_search)
    st.metric("Total Archived Accounts", total_archived)

    if not archived_users and total_archived == 0:
        st.info("No accounts are currently archived.")
        return

    for u in archived_users:
        uid = u["id"]
        uname = u.get("full_name") or "User"
        uemail = u.get("email") or ""
        udate = (u.get("status_updated_at") or u.get("updated_at") or "")[:10]
        ureason = u.get("lifecycle_reason") or "Archived by Administration"

        card_archived = (
            f'<div style="background:#FFFFFF; border:1px solid #E2E8F0; border-left:4px solid #64748B; border-radius:10px; padding:1.1rem 1.3rem; margin-bottom:1rem;">'
            f'<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">'
            f'<div><span style="font-weight:800; color:#0F172A; font-size:1.05rem;">{uname}</span>'
            f'<span style="color:#64748B; font-size:0.86rem; margin-left:8px;">({uemail})</span>'
            f'<div style="color:#64748B; font-size:0.82rem; margin-top:4px;">'
            f'Archived Date: <strong>{udate or "Recorded"}</strong> | Reason: <em>{ureason}</em></div></div>'
            f'<div><span style="background:#F1F5F9; color:#475569; font-size:0.75rem; font-weight:700; padding:3px 10px; border-radius:6px;">🗄️ ARCHIVED</span></div>'
            f'</div></div>'
        )
        st.markdown(card_archived, unsafe_allow_html=True)

        col_r1, col_r2 = st.columns([3, 1])
        with col_r1:
            rest_reason = st.text_input("Restoration Note", placeholder="e.g. Entrepreneur returned to active incubation", key=f"rest_rsn_{uid}")
        with col_r2:
            st.write("")
            st.write("")
            if st.button("🔄 Restore Account", key=f"btn_restore_{uid}", type="primary", use_container_width=True):
                ok_res, err_res = restore_account(uid, actor_id=admin_id, reason=rest_reason.strip())
                if ok_res:
                    st.success(f"Account for {uname} restored under original UUID {uid}. Old caseloads remain unassigned for deliberate reassignment.")
                    st.rerun()
                else:
                    st.error(err_res or "Failed to restore account.")

    if total_archived > 25:
        render_pagination_controls(total_archived, cur_arc_page, page_size=25, key_prefix="alc_arc")


def render_subtab_pending_deletion(admin_id: str):
    st.markdown("### ⏳ Accounts Pending Deletion Review")
    st.markdown(
        '<div style="background:#FEF3C7; border:1px solid #FDE68A; border-left:4px solid #D97706; border-radius:10px; padding:0.9rem 1.2rem; margin-bottom:1.25rem;">'
        '<span style="font-weight:800; color:#92400E; font-size:0.9rem;">Institutional Policy on Permanent Erasure:</span>'
        '<div style="color:#B45309; font-size:0.84rem; margin-top:3px;">'
        'A 30-day grace period is enforced on all account closure requests. '
        '<strong>There is NO automatic permanent purge during this phase.</strong> '
        'Erasing accounts requires explicit, verified lawful erasure protocol execution with legal hold clearance.'
        '</div></div>',
        unsafe_allow_html=True
    )

    from services.pagination import paginate_accounts, render_pagination_controls

    cur_del_page = st.session_state.get("alc_del_page", 1)
    del_search = st.text_input("🔍 Search Pending Closures", placeholder="Search by name or email...", key="alc_search_pending")

    pending_users, total_pending = paginate_accounts(status="PENDING_DELETION", page=cur_del_page, page_size=25, search=del_search)
    st.metric("Accounts in Grace Window", total_pending)

    if not pending_users and total_pending == 0:
        st.info("No accounts are currently pending deletion review.")
        return

    for u in pending_users:
        uid = u["id"]
        uname = u.get("full_name") or "User"
        uemail = u.get("email") or ""
        ureq_at = (u.get("deletion_requested_at") or "")[:10]
        usched_at = (u.get("deletion_scheduled_for") or "")[:10]
        uheld = bool(u.get("legal_hold", False))
        ureason = u.get("lifecycle_reason") or "Account closure requested"

        hold_span = '<span style="background:#FEE2E2; color:#B91C1C; font-size:0.75rem; font-weight:700; padding:2px 8px; border-radius:6px;">⚖️ LEGAL HOLD</span>' if uheld else ''
        card_pending = (
            f'<div style="background:#FFFFFF; border:1px solid #FDE68A; border-left:4px solid #EAB308; border-radius:10px; padding:1.1rem 1.3rem; margin-bottom:1rem;">'
            f'<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">'
            f'<div><span style="font-weight:800; color:#0F172A; font-size:1.05rem;">{uname}</span>'
            f'<span style="color:#64748B; font-size:0.86rem; margin-left:8px;">({uemail})</span>'
            f'<div style="color:#64748B; font-size:0.82rem; margin-top:4px;">'
            f'Requested: <strong>{ureq_at or "Recent"}</strong> | Scheduled Review: <strong>{usched_at or "30 Days"}</strong> | Reason: <em>{ureason}</em></div></div>'
            f'<div style="display:flex; gap:6px;">'
            f'<span style="background:#FEF3C7; color:#B45309; font-size:0.75rem; font-weight:700; padding:2px 8px; border-radius:6px;">⏳ PENDING DELETION</span>'
            f'{hold_span}</div>'
            f'</div></div>'
        )
        st.markdown(card_pending, unsafe_allow_html=True)

        col_c1, col_c2 = st.columns([3, 1])
        with col_c1:
            cancel_note = st.text_input("Cancellation Note", placeholder="e.g. Closure cancelled by administration", key=f"canc_rsn_{uid}")
        with col_c2:
            st.write("")
            st.write("")
            if st.button("↩️ Cancel Deletion", key=f"btn_canc_del_{uid}", type="primary", use_container_width=True):
                ok_c, err_c = cancel_account_deletion(uid, actor_id=admin_id, reason=cancel_note.strip())
                if ok_c:
                    st.success(f"Closure request cancelled. {uname}'s account is active.")
                    st.rerun()
                else:
                    st.error(err_c or "Failed to cancel closure.")

    if total_pending > 25:
        render_pagination_controls(total_pending, cur_del_page, page_size=25, key_prefix="alc_del")


def render_subtab_action_history(admin_id: str):
    st.markdown("### 📜 Account Action History & Audit Timeline")
    st.markdown("<p style='color:#64748B; font-size:0.86rem;'>Chronological, tamper-evident log of all administrative lifecycle operations across the institution.</p>", unsafe_allow_html=True)

    logs = list_account_lifecycle_logs(limit=100)

    if not logs:
        st.info("No account lifecycle events recorded yet.")
        return

    # Render as institutional audit table
    import pandas as pd
    rows_display = []
    for l in logs:
        ts = (l.get("created_at") or "")[:19].replace("T", " ")
        action = l.get("action", "")
        uid = l.get("user_id", "")
        act_id = l.get("actor_id", "")
        p_st = l.get("previous_status") or "ACTIVE"
        n_st = l.get("new_status") or "-"
        reason = l.get("reason", "")

        rows_display.append({
            "Timestamp (UTC)": ts,
            "Action": action,
            "Previous Status": p_st,
            "New Status": n_st,
            "Target User UUID": uid[:12] + "...",
            "Authorized By": "Admin" if act_id == SOLE_ADMIN_UUID else act_id[:12] + "...",
            "Reason": reason
        })

    df = pd.DataFrame(rows_display)
    st.dataframe(df, use_container_width=True, hide_index=True)

