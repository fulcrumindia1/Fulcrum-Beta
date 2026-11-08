# FULCRUM-BETA → AGY ARGON: 360° UX, USABILITY & COGNITIVE LAWS AUDIT
**Deliverable 4 of 10 | Mode: Read-Only UX Diagnostics & Recommendations**

---

## 1. Evaluation Against Jakob Nielsen's 10 Usability Heuristics

| # | Heuristic | Rating | Concrete Fulcrum-Beta Code Evidence & Findings |
| :- | :--- | :---: | :--- |
| **1** | **Visibility of System Status** | ⚠️ **5/10** | **Strengths:** Profile completion progress bar (`0–100%`) in [`views/aspirant.py:L59-L76`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/aspirant.py#L59-L76); live inactivity badges (`Needs Attention`, `Mentor Active Again`) in [`services/inactivity.py:L464`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/inactivity.py#L464).<br>**Failures:** (a) Clicking any tab triggers `on_change="rerun"`, freezing the UI for 1.5s–9.5s while executing hidden tabs without localized skeleton loaders. (b) Aspirants submitting confidential complaints ([`views/aspirant.py:L738`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/aspirant.py#L738)) have zero status visibility after submission. (c) Released schemes have no post-release application state (`Preparing`, `Applied`, `Sanctioned`). |
| **2** | **Match Between System and the Real World** | ✅ **8/10** | **Strengths:** Domain terminology (`Aspirant`, `Dedicated Guide`, `Domain SME`, `DPIIT Recognized`, `StartupTN`, `Udyam`) matches Indian MSME reality; schemes never claim `"Approved"` or `"Guaranteed"`, strictly using `"Potentially Eligible"` and `"Recommended"`.<br>**Failures:** Internal status codes like `PENDING_ADMIN`, `DIRECTIVE_ISSUED`, and `WAITING_ON_GUIDE_SME` are rendered raw as uppercase strings in several ticket badges ([`views/sme.py:L461`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/sme.py#L461), [`views/admin.py:L800`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/admin.py#L800)). |
| **3** | **User Control and Freedom** | ⚠️ **6/10** | **Strengths:** Journey events support modal editing (`✏️`) with revision history and soft-delete (`🗑️`); Guides can withdraw released schemes (`withdraw_scheme_release`).<br>**Failures:** (a) Once an Aspirant submits a consultation or replies, they cannot edit a typo. (b) Once an Aspirant replies to an SME ticket (`status="WAITING_ON_GUIDE_SME"`), the SME's reply form disappears ([`views/sme.py:L475`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/sme.py#L475)), trapping the ticket in a dead end! |
| **4** | **Consistency and Standards (Jakob's Law)** | ⚠️ **5/10** | **Failures:** (a) **Fake Sidebar Navigation:** [`app.py:L1061-L1101`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/app.py#L1061-L1101) renders a `"Navigation"` section in the left sidebar (`✓ Overview`, `✓ My Profile`, etc.) that looks like clickable menu items, but is actually static unclickable HTML `<div>` text while actual navigation is horizontal `st.tabs` at the top! (b) **Visual Theme Whiplash:** The app uses a light slate/white theme (`#F8FAFC` / `#FFFFFF`), except Fund Explorer cards ([`services/schemes_ui.py:L452`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/schemes_ui.py#L452)) which abruptly switch to a pitch-black obsidian-violet theme (`#11131F` with neon purple `#8B5CF6` borders). (c) Guide Consultation tab includes Case Discussions, whereas SME Consultation tab omits Case Discussions completely. |
| **5** | **Error Prevention** | ⚠️ **5/10** | **Strengths:** Scheme deletion uses a confirmation modal dialog (`open_delete_scheme_dialog`); self-assignment of hybrid mentors is blocked.<br>**Failures:** (a) **Unreactive Conditional Inputs Inside `st.form`:** Across [`views/aspirant.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/aspirant.py#L274), [`views/admin.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/admin.py#L399), [`views/guide.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/guide.py#L270), and [`views/sme.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/sme.py#L223), `if selectbox == "Other (Specify)": st.text_input(...)` is placed inside `st.form`. Because Streamlit forms do not rerun on selectbox change, selecting `"Other"` never shows the text input until *after* the user clicks Submit—saving `"Other"` instead of their custom value! (b) Journey soft-delete (`🗑️`) executes immediately on single click without confirmation. |
| **6** | **Recognition Rather Than Recall** | ✅ **7.5/10** | **Strengths:** Guide Scheme Matches subtab shows the Aspirant's criteria checklist right alongside each scheme; Admin Mentor Allocation cards show current Guide and SME badges inline.<br>**Failures:** When replying to a consultation in `All Consultations Overview` ([`views/guide.py:L1115`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/guide.py#L1115), [`views/sme.py:L624`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/sme.py#L624)), the mentor cannot see the entrepreneur's business stage or sector without leaving the tab. |
| **7** | **Flexibility and Efficiency of Use** | ⚠️ **5.5/10** | **Strengths:** Admin WhatsApp (`wa.me`) and Gmail compose links pre-populate courteous context-aware templates ([`services/external_contact.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/external_contact.py)).<br>**Failures:** (a) Admin has 12 horizontal top-level tabs (`tabs[0]`–`tabs[11]`), forcing horizontal scrolling/overflow on standard laptop screens. (b) Notifications in the sidebar ([`app.py:L1030`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/app.py#L1030)) have no deep-link action button to jump to the referenced ticket, scheme, or mentee. |
| **8** | **Aesthetic and Minimalist Design** | ⚠️ **6.5/10** | **Strengths:** Clean card typography (`Plus Jakarta Sans`), clear role color coding (Blue `#3B82F6` for Aspirant, Emerald `#10B981` for Guide, Amber `#D97706` for SME, Indigo/Rose for Admin).<br>**Failures:** Admin Tab 4 (`Mentor Directives & Escalations`) has a Python indentation defect ([`views/admin.py:L739-L856`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/admin.py#L739-L856)) where the entire Mentor Directives interface renders outside its subtab container and stacks on top of the Scheme Support Reviews subtab! |
| **9** | **Help Users Recognize, Diagnose, and Recover from Errors** | ✅ **7.5/10** | **Strengths:** Gatekeeper scheme release restriction clearly lists which mandatory statutory criteria failed (`Gatekeeper Restriction: Scheme does not meet mandatory criteria...`).<br>**Failures:** Photo rendering failures caused by missing `viewer_id` in `views/aspirant.py:L209`, `views/admin.py:L217`, and `views/admin_governance.py:L673` silently display `"No photograph uploaded currently"` even right after the user uploads a photo! |
| **10** | **Help and Documentation** | ✅ **7.5/10** | **Strengths:** Contextual subtitle descriptions on every tab; built-in AI Copilot application prompt templates on every scheme card for Guides and Admin.<br>**Failures:** No onboarding checklist on the Aspirant Overview tab explaining the 3-step sequence (1. Complete Profile >=80% -> 2. Wait for Guide Review -> 3. Apply to Released Schemes). |

---

## 2. Evaluation Against Core UX & Cognitive Laws

### 2.1 Hick's Law (Decision Time Scales Logarithmically with Choices)
- **Violation in Admin Portal (`views/admin.py:L149-L163`):** Displaying **12 top-level horizontal tabs** simultaneously (`Aspirants & Journeys`, `Create Account`, `Guides & SMEs`, `Guide & SME Assignments`, `Mentor Directives`, `Scheme Catalogue`, `Inactivity Monitor`, `Role Grants & Multi-Role`, `Confidential Complaints`, `Legal & NDA Audit`, `SME Conflict Governance`, `Aspirant Photos`) exceeds Miller's Law ($7 \pm 2$ items) and increases visual scan time.
- **Violation in Aspirant Profile Form (`views/aspirant.py:L255-L470`):** Presenting 26+ input fields inside a single monolithic `st.form` without section-level save or reactive progressive disclosure overwhelms grassroots founders.

### 2.2 Fitts's Law (Target Acquisition Depends on Distance and Size)
- **Good Practice:** Primary form submit buttons use `use_container_width=True`, creating large, easy-to-hit targets on mobile and desktop.
- **Violation:** In the Journey timeline (`views/aspirant.py:L608-L625`, `views/guide.py:L362-L374`), the Edit (`✏️`), Delete (`🗑️`), and Roadmap Pin (`📌`) icon buttons are packed into a narrow `0.8` or `1.1` fractional column where a misclick by 8 pixels immediately triggers `soft_delete_event` without confirmation!

### 2.3 Jakob's Law & Progressive Disclosure
- Users expect sidebar navigation items to be clickable links. Having static text in the sidebar (`app.py:L1061-L1101`) while real navigation lives in top tabs violates mental models.
- Guide (`views/guide.py:L152`) and SME (`views/sme.py:L115`) portals use `st.pills` for mentee sub-navigation (`Profile`, `Scheme Matches`, `Journey`, `Guidance Team`, `Consultations`), which is a strong progressive disclosure pattern because it scopes the workspace to one selected entrepreneur at a time.

---

## 3. Accessibility (WCAG 2.2 AA) & Mobile Responsiveness

1. **Color Contrast:**
   - Primary body text (`#0F172A` on `#FFFFFF`, contrast `19.1:1`) and secondary slate text (`#475569` on `#FFFFFF`, contrast `7.5:1`) pass WCAG AAA.
   - **Contrast Failure (`#94A3B8` on `#FFFFFF` / `#F8FAFC`):** Timestamp and metadata labels using `#94A3B8` on white backgrounds (`views/guide.py:L1232`, `views/sme.py:L742`) have a contrast ratio of **`2.56:1`**, failing WCAG AA (`4.5:1` minimum).
2. **Mobile & Small-Screen Responsiveness:**
   - Fixed 3-column and 4-column layouts (`st.columns([1.2, 5.2, 0.8])` in Journey timelines and `st.columns(4)` in KPI rows) compress text into narrow vertical strips on mobile viewports (`< 640px`).
   - Horizontal `st.tabs` with 12 tabs in the Admin portal overflows horizontally on tablets and 13-inch laptops.

---

## 4. Direct Answers to All 20 Required UX Assessment Questions (Part 6)

1. **Does each role immediately understand what to do after login?**
   - **Mostly Yes for Guide/SME; Partially for Aspirant.** Aspirants see 4 KPI metrics (`Profile Completion`, `Assigned Mentors`, `Released Schemes`, `Milestones`), but there is no prominent "Next Recommended Action" banner guiding a new founder with a `30%` profile to click `My Profile` first.
2. **Are primary actions obvious?**
   - **Yes within subtabs, but buried inside expanders.** Actions like `➕ Log Milestone`, `➕ Submit New Consultation Request`, and `➕ Issue Guidance Directive` use collapsed `st.expander` blocks above lists—clean for returning users, but easy for first-time users to miss when the list below is empty.
3. **Are secondary/destructive actions safely separated?**
   - **Mixed.** Scheme deletion (`open_delete_scheme_dialog`) and Mentor Unassignment (`st.popover` with reason input) are safely separated. However, Journey event deletion (`🗑️`) sits immediately next to Edit (`✏️`) with zero confirmation dialog.
4. **Are tabs named clearly for non-technical users?**
   - **Yes for Aspirant/Guide/SME; Too Dense for Admin.** Aspirant tabs (`Overview`, `My Profile`, `Scheme Matches`, `My Journey`, `My Mentors`, `Consultations`) are clear. Admin's 12 tabs have overlapping governance names (`Mentor Directives` vs `Inactivity Monitor` vs `Confidential Complaints`).
5. **Is there unnecessary cognitive load on any screen?**
   - **Yes:** (a) Admin Tab 4 (`Mentor Directives`) renders both subtabs simultaneously due to the indentation bug (`views/admin.py:L743-L856`); (b) Admin Tab 3 (`Guide & SME Assignments`) renders assignment cards and popovers for every aspirant in a single unpaginated list; (c) Aspirant Tab 1 (`My Profile`) has 26+ fields in one form.
6. **Are forms too long or poorly grouped?**
   - **Grouping is logical, but Streamlit `st.form` breaks conditional fields.** In `views/aspirant.py`, the 4 numbered sections + Section 5 (Assistance Requirement) are well-titled, but putting conditional `"Other (Specify)"` inputs inside `st.form` makes them non-functional until submission.
7. **Do forms preserve input on validation error?**
   - **Yes.** Because inputs are bound to widget state inside `st.form`, validation warnings (`st.warning` / `st.error`) preserve typed text on rerun.
8. **Are statuses consistent across roles?**
   - **No (Critical Gap).** `help_requests` uses `OPEN`, `IN_PROGRESS`, `WAITING_ON_ASPIRANT`, `WAITING_ON_GUIDE_SME`, `REPLIED`, `RESOLVED`, `PENDING_ADMIN`, and `DIRECTIVE_ISSUED`. However, `views/sme.py` only checks for `OPEN`, `IN_PROGRESS`, and `REPLIED`—completely ignoring `WAITING_ON_GUIDE_SME` and `WAITING_ON_ASPIRANT`!
9. **Does an Aspirant know who owns the next step on a consultation?**
   - **Yes on Guide/Mentor-initiated replies, but raw status labels leak.** `views/aspirant.py:L912-L919` translates `WAITING_ON_ASPIRANT` to `"ACTION REQUIRED FROM YOU"` and `WAITING_ON_GUIDE_SME` to `"AWAITING MENTOR REVIEW"`, which is excellent—but SME consultations lack the `WAITING_ON_ASPIRANT` option in `views/sme.py:L480`.
10. **Does a Guide know which Aspirants need attention first?**
    - **Partially.** The Mentee Consultations pill shows `💬 Consultations (N)` for the *currently selected* mentee (`views/guide.py:L140`), but the top `"Select Mentee to Manage"` dropdown (`views/guide.py:L100`) only shows `Full Name — Business Name (District)` with no indicator of which mentees have open tickets or days since last check-in!
11. **Does an SME know which consultations are waiting on SME action?**
    - **Broken.** When an Aspirant replies to an SME's question, the ticket status becomes `WAITING_ON_GUIDE_SME`. Because `views/sme.py:L96` only counts `["OPEN", "IN_PROGRESS", "ACTION_REQUIRED"]`, the open badge drops to `0` and the reply form disappears!
12. **Does Admin have a clean daily triage workflow?**
    - **No.** Admin must click through 6 separate tabs (`Tab 3` for unassigned aspirants, `Tab 4` for Mentor Directives & Scheme Reviews, `Tab 6` for Inactivity Alerts, `Tab 7` for Pending NDAs, `Tab 8` for Confidential Complaints, `Tab 10` for SME Conflicts) to find pending work, suffering a 3.5s–9.5s wait on every tab click.
13. **Are empty states helpful and actionable?**
    - **Yes.** Empty states across `views/aspirant.py`, `views/guide.py`, and `views/sme.py` clearly explain *why* a list is empty (e.g., `"Your Guide is currently reviewing matched schemes..."`) and what will happen next.
14. **Are loading states perceived as fast and clear?**
    - **No.** Because `is_tab_active()` is missing from `views/aspirant.py`, `views/guide.py`, `views/sme.py`, and `views/admin.py` Tabs 0–5, every tab click triggers a full-page dim/freeze while fetching data for hidden tabs.
15. **Are notifications useful and not noisy?**
    - **Useful content, but trapped in a non-clickable sidebar expander.** Notifications are only created on meaningful state changes (except missing notifications on role grants, complaint resolution, and case discussions), but clicking a notification cannot navigate the user to the relevant tab or mentee.
16. **Are tables/cards readable on laptop and mobile screens?**
    - **Good on 1080p desktop; cramped on `<1366px` laptops and mobile.** Admin's 12-tab bar overflows, and 3-column/4-column cards stack awkwardly on mobile.
17. **Are role boundaries visually unmistakable?**
    - **Yes.** Each portal has a distinct color identity and header badge (`Entrepreneur` = Blue, `Verified Guide` = Emerald, `Verified SME` = Amber, `Platform Admin` = Slate/Indigo), and the sidebar role switcher clearly indicates the active workspace.
18. **Is Admin anonymity ("Fulcrum Support") preserved everywhere Aspirants can see?**
    - **Yes.** Verified across `services/governance.py`, `services/journey.py`, `views/aspirant.py`, and `services/external_contact.py`. The Admin's name (`Fulcrum Administrator`) and email (`fulcrumindia1@gmail.com`) are never exposed to Aspirants.
19. **Are Aspirant photos shown only where authorized and useful?**
    - **Authorization is strict, but 3 authorized views are currently broken.** Unassigned mentors and other Aspirants are strictly blocked (`SEC-05`). Guides (`views/guide.py:L179`) and SMEs (`views/sme.py:L138`) see the assigned Aspirant's photo properly. However, Aspirant (`views/aspirant.py:L209`) and Admin (`views/admin.py:L217`, `views/admin_governance.py:L673`) omit `viewer_id`, causing photos to hide behind fallback initials!
20. **Are Guide/SME photos kept private according to rule?**
    - **Yes, 100% enforced.** Neither `profiles` nor `aspirant_photos` exposes Guide or SME photographs to Aspirants anywhere in the codebase.
