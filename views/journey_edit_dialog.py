"""
views/journey_edit_dialog.py
=============================================================================
Reusable Modal Dialog for Editing Journey Entries
Provides modal dialog with prepopulated title, description, link, date,
roadmap status, optimistic concurrency check, and audit revision history.
=============================================================================
"""

import streamlit as st
from datetime import datetime
from typing import Optional, Dict
from services.journey import update_journey_event, can_user_edit_event

@st.dialog("Edit Journey Entry")
def render_edit_journey_dialog(event: Dict, user_id: str, active_role: str):
    """Renders a modal dialog for editing an existing journey event."""
    if not event:
        st.error("No journey entry selected.")
        return

    ev_data = event.get("event_data", {}) if isinstance(event.get("event_data"), dict) else {}
    raw_title = ev_data.get("title") or ev_data.get("event_title") or event.get("event_type") or "Milestone"
    raw_desc = ev_data.get("description", "")
    current_link = ev_data.get("link", "")

    # Try parsing current event date
    raw_date = str(event.get("event_date", ""))[:10]
    try:
        current_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
    except Exception:
        current_date = datetime.now().date()

    current_roadmap = event.get("included_in_roadmap", True) is not False

    st.markdown("""
    <p style='color:#64748B; font-size:0.9rem; margin-top:-0.5rem; margin-bottom:1rem;'>
        Update details for this journey milestone. Changes are saved with an immutable audit revision history.
    </p>
    """, unsafe_allow_html=True)

    with st.form(key=f"form_edit_event_{event['id']}"):
        new_title = st.text_input("Entry Title *", value=raw_title, help="Short summary of this milestone or update")
        new_desc = st.text_area("Description *", value=raw_desc, height=120, help="Detailed progress, outcome, or advisory recommendation")
        new_link = st.text_input("Website / Project Link (Optional)", value=current_link, placeholder="https://example.com")

        col_d1, col_d2 = st.columns(2)
        with col_d1:
            new_date = st.date_input("Milestone Date", value=current_date)
        with col_d2:
            st.write("")
            st.write("")
            new_roadmap = st.checkbox("Active on Roadmap", value=current_roadmap, help="Include in the primary roadmap timeline")

        change_reason = st.text_input("Reason for Edit (Optional)", placeholder="e.g., Updated project link and launch description")

        col_save, col_cancel = st.columns([1, 1])
        with col_save:
            btn_save = st.form_submit_button("💾 Save Changes", use_container_width=True, type="primary")
        with col_cancel:
            btn_cancel = st.form_submit_button("Cancel", use_container_width=True)

        if btn_cancel:
            st.rerun()

        if btn_save:
            if not new_title.strip():
                st.error("Title cannot be empty.")
            else:
                ok, err = update_journey_event(
                    event_id=event["id"],
                    editor_id=user_id,
                    editor_role=active_role,
                    new_title=new_title,
                    new_description=new_desc,
                    new_link=new_link,
                    new_date=new_date.strftime("%Y-%m-%d"),
                    new_included_in_roadmap=new_roadmap,
                    expected_updated_at=event.get("updated_at"),
                    change_reason=change_reason
                )
                if ok:
                    st.session_state["edit_event_success"] = f"Journey entry '{new_title.strip()}' updated successfully."
                    st.rerun()
                else:
                    st.error(err or "Failed to update entry.")

