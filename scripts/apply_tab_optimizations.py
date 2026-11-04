"""
scripts/apply_tab_optimizations.py — Safely adds tab lazy evaluation to dashboards
"""

import sys

def optimize_aspirant():
    path = "views/aspirant.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add import if missing
    if "from services.cache import is_tab_active" not in content:
        content = content.replace(
            "from services.profiles import get_profile",
            "from services.cache import is_tab_active\nfrom services.profiles import get_profile"
        )

    # 2. In Tab 3: add confidential guide complaint expander before Tab 4
    complaint_snippet = '''
        if guide:
            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            with st.expander("🛡️ Request Guide Change / Report Confidential Concern"):
                st.caption("This report is submitted directly and confidentially to Fulcrum Administration. Your assigned Guide will not see this notice.")
                with st.form("confidential_complaint_form"):
                    complaint_reason = st.selectbox(
                        "Reason for Request",
                        [
                            ("inactivity", "Guide is inactive / unresponsive"),
                            ("poor_communication", "Communication difficulties"),
                            ("conflict_of_interest", "Potential conflict of interest"),
                            ("professional_conduct", "Professional conduct / ethics"),
                            ("other", "Other reason")
                        ],
                        format_func=lambda x: x[1]
                    )
                    complaint_details = st.text_area("Detailed context / explanation (Minimum 10 characters)*", placeholder="Please share details regarding this request...")
                    submit_comp = st.form_submit_button("Submit Confidential Request")
                    if submit_comp:
                        from services.governance import submit_guide_complaint
                        ok, err = submit_guide_complaint(user_id, guide["id"], complaint_reason[0], complaint_details)
                        if ok:
                            st.success("Your request has been submitted confidentially to Fulcrum Administration for review.")
                        else:
                            st.error(err or "Failed to submit request.")
'''
    if "🛡️ Request Guide Change / Report Confidential Concern" not in content:
        target = '    # ─────────────────────────────────────────────────────────────\n    # TAB 5: SCHEME MATCHES (Gatekeeper Governed)'
        content = content.replace(target, complaint_snippet + "\n" + target)

    # 3. In Tab 6: add case discussions
    collab_snippet = '''
        st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)
        st.markdown("### 💬 Advisory Case Discussions & Collaboration")
        from services.collaboration import list_case_messages, create_case_message
        case_msgs = list_case_messages(user_id, requesting_role="aspirant")
        with st.expander(f"Case Discussion Board ({len(case_msgs)} messages)", expanded=False):
            if not case_msgs:
                st.caption("No advisory case discussion messages posted yet.")
            else:
                for m in case_msgs:
                    st.markdown(f"""
                    <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-left:3px solid #3B82F6; border-radius:8px; padding:0.8rem; margin-bottom:0.5rem;">
                        <div style="font-size:0.85rem; font-weight:700; color:#1E293B;">{_safe_esc(m.get('title'))} <span style="font-weight:400; color:#64748B; font-size:0.75rem;">by {_safe_esc(m.get('author_name', 'Mentor'))} ({_safe_esc(m.get('author_role', '').upper())}) · {m.get('created_at', '')[:10]}</span></div>
                        <div style="font-size:0.85rem; color:#334155; margin-top:4px;">{_safe_esc(m.get('message'))}</div>
                    </div>
                    """, unsafe_allow_html=True)
            with st.form("form_add_case_msg"):
                msg_title = st.text_input("Topic / Question Title*", placeholder="e.g. Question on GST filing documentation")
                msg_body = st.text_area("Discussion Message*", placeholder="Write your message to your Guide and SME panel...")
                if st.form_submit_button("Post to Discussion Board"):
                    if not msg_title.strip() or not msg_body.strip():
                        st.warning("Please enter both title and message.")
                    else:
                        ok, err = create_case_message(user_id, user_id, "aspirant", msg_title, msg_body, is_private_mentor_note=False)
                        if ok:
                            st.success("Message posted to discussion board.")
                            st.rerun()
                        else:
                            st.error(err or "Failed to post message.")
'''
    if "### 💬 Advisory Case Discussions & Collaboration" not in content:
        content = content + "\n" + collab_snippet

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Aspirant view updated.")

if __name__ == "__main__":
    optimize_aspirant()

