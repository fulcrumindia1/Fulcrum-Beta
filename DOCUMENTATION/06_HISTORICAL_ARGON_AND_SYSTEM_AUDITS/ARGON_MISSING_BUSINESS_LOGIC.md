# FULCRUM-BETA → AGY ARGON: MISSING BUSINESS LOGIC & STATE-TRANSITION AUDIT
**Deliverable 5 of 10 | Mode: Read-Only Business Logic & Workflow Completeness Analysis**

---

## Executive Summary of Logic Gaps

Fulcrum-Beta's core data model and two-tier governance architecture are well-conceived, but static and runtime trace analysis across **Workflows A–F** revealed **16 concrete business-logic and state-transition gaps** where real-world mentorship, consultation, scheme tracking, or role-management workflows either dead-end, silently drop state, or leave users without next-step accountability.

---

## Workflow A: Aspirant Onboarding to First Value

### Current Implemented Flow
`Signup` $\rightarrow$ `Accept Terms & Conditions` $\rightarrow$ `Land on Aspirant Overview (0–30% Profile Completion)` $\rightarrow$ `Fill 4-Section Profile + Assistance Need` $\rightarrow$ `Wait for Admin to Assign Guide` $\rightarrow$ `Wait for Guide to Release Schemes`.

### Missing Business Logic & Edge Cases
1. **No Onboarding Readiness Gate or Admin Alert When Profile Reaches Match-Ready Threshold (`>= 70%`):**
   - **Evidence:** [`services/profiles.py:update_aspirant_profile` (L256–L396)](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/profiles.py#L256-L396) calculates `completion_pct` and logs a `profile_updated` Journey event, but **never notifies the Admin** (if the Aspirant has no Guide yet) or the **assigned Guide** (if the Aspirant just completed their business/demographics profile for the first time).
   - **Real-World Consequence:** An entrepreneur signs up, completes 100% of their venture dossier, and sits waiting with `0` assigned mentors or `0` released schemes because neither Admin nor Guide was alerted that the profile is ready for scheme evaluation.
2. **Broken Self-Photo Verification After Upload (`SEC-05` Call-Site Mismatch):**
   - **Evidence:** [`views/aspirant.py:L209`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/aspirant.py#L209) calls `get_aspirant_photo(user_asp_id)` without passing `viewer_id=user_asp_id, viewer_role="aspirant"`. Because `get_aspirant_photo` fails closed when `viewer_id is None` ([`services/aspirant_photos.py:L218`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/aspirant_photos.py#L218)), the Aspirant uploads a photograph, receives `"Photograph updated successfully!"`, and after `st.rerun()` still sees `"No photograph uploaded"`! (The exact same bug occurs for Admin in [`views/admin.py:L217`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/admin.py#L217) and [`views/admin_governance.py:L673`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/admin_governance.py#L673)).
3. **Silent Loss of `"Other (Specify)"` Custom Profile Values Inside `st.form`:**
   - **Evidence:** [`views/aspirant.py:L274, L301, L323, L340, L358, L370`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/aspirant.py#L274-L370) and [`L399-L411`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/aspirant.py#L399-L411).
   - **Real-World Consequence:** When an Aspirant selects `"Other / Not Listed (Specify)"` for Sector, Qualification, or Stage inside `st.form`, Streamlit does not rerun the script until `SAVE & UPDATE FULL DOSSIER` is clicked. Thus, the custom text box never appears before submission, and the literal placeholder `"Other / Not Listed (Specify)"` is saved to the database, degrading scheme matching accuracy.

---

## Workflow B: Scheme Matching $\rightarrow$ Release $\rightarrow$ Application Outcome

### Current Implemented Flow
`Profile Saved` $\rightarrow$ `match_schemes_for_aspirant()` $\rightarrow$ `Guide Evaluates Checklist` $\rightarrow$ `(Optional) Guide Submits Scheme Support Review to Admin` $\rightarrow$ `Guide Releases Scheme (status='RELEASED') or Withdraws (status='WITHDRAWN')`.

### Missing Business Logic & Edge Cases
4. **Co-Guides (`Guide B`) Are Blocked from Releasing or Withdrawing Schemes:**
   - **Evidence:** [`services/schemes.py:release_scheme_to_aspirant` (L385–L391)](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/schemes.py#L385-L391) and [`withdraw_scheme_release` (L509–L515)](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/schemes.py#L509-L515) check:
     ```python
     assigned_guide = mentors.get("guide")
     if not is_admin and (not assigned_guide or str(assigned_guide.get("id")) != str(guide_id)):
         return False, "You are not authorized to release schemes to this Aspirant."
     ```
   - **Real-World Consequence:** When Admin assigns a Co-Guide (`Guide B`) via Tab 3 or Tab 4 (`assign_guide(..., mode="add")`), `Guide B` can view the Aspirant's Scheme Matches subtab in `views/guide.py`, but clicking **Release Scheme to Aspirant** fails with `"You are not authorized to release schemes to this Aspirant"` because only `mentors.get("guide")` (the primary Guide) is checked instead of `mentors.get("guides")`!
5. **Admin Approval of a `Scheme Support Review` Does Not Unlock the Gatekeeper Override Automatically:**
   - **Evidence:** When a Guide escalates a disqualified scheme (`is_disqualified=True`) via [`submit_scheme_support_review`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/scheme_reviews.py#L18) and the Admin approves it (`status="APPROVED"`) via [`decide_scheme_support_review`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/scheme_reviews.py#L154), the notification tells the Guide: *"You may now release this scheme to their venture dashboard."* However, [`release_scheme_to_aspirant`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/schemes.py#L400) does not check `scheme_support_reviews` for an `APPROVED` decision—it still blocks release unless the Guide manually ticks the override checkbox!
6. **Missing Post-Release Application Lifecycle (`RELEASED` $\rightarrow$ `APPLIED` $\rightarrow$ `OUTCOME`):**
   - **Evidence:** `scheme_releases` only has two statuses: `RELEASED` and `WITHDRAWN` ([`services/schemes.py:L423, L532`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/schemes.py#L423)).
   - **Real-World Consequence:** After a Guide releases 5 schemes to an Aspirant, neither the Aspirant, the Guide, nor the Admin can track which schemes the entrepreneur is actively preparing (`PREPARING_DPR`), has submitted (`APPLIED`), was approved/sanctioned (`SANCTIONED`), or was rejected (`NOT_ELIGIBLE` / `REJECTED`). The workflow stops at "Release".
7. **Missing Global Cache Invalidation on Admin Scheme Edits/Archives:**
   - **Evidence:** [`services/schemes.py:list_schemes` (L74, L96)](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/schemes.py#L74) caches all active schemes in `_GLOBAL_CACHE["schemes:all_active"]` for `ttl_seconds=300`. However, [`upsert_scheme` (L157)](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/schemes.py#L157), [`toggle_archive_scheme` (L185)](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/schemes.py#L185), and [`delete_scheme` (L217)](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/schemes.py#L217) never call `invalidate_global_cache("schemes:all_active")`.

---

## Workflow C: Consultation, Mentor Directive & Case Discussion Lifecycle

### Current Implemented Flow
`Aspirant Creates Request (OPEN)` OR `Mentor Initiates Directive (OPEN)` $\rightarrow$ `Guide/SME Responds (IN_PROGRESS / WAITING_ON_ASPIRANT / RESOLVED)` $\rightarrow$ `Aspirant Replies (WAITING_ON_GUIDE_SME)`.

### Missing Business Logic & Edge Cases
8. **CRITICAL DEAD-END: SME Cannot Reply After Aspirant Responds (`WAITING_ON_GUIDE_SME` Lockout):**
   - **Evidence:** When an Aspirant replies to any consultation via [`aspirant_respond_request` (`services/help_requests.py:L1110`)](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/help_requests.py#L1110), the ticket status is updated to `"WAITING_ON_GUIDE_SME"`.
   - In [`views/guide.py:L554` & `L1114`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/guide.py#L554), the Guide response form checks `if t_status != "RESOLVED":`, so the Guide can reply.
   - **However, in [`views/sme.py:L475`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/sme.py#L475), the SME response form checks `if t_status in ["OPEN", "IN_PROGRESS", "REPLIED"]:` and in [`views/sme.py:L623`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/sme.py#L623) it checks `if t_status in ["OPEN", "IN_PROGRESS"]:`!**
   - Furthermore, [`views/sme.py:L96`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/sme.py#L96) calculates `open_cnt` using `["OPEN", "IN_PROGRESS", "ACTION_REQUIRED"]` and [`views/sme.py:L578`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/sme.py#L578) only filters `["ALL", "OPEN", "IN_PROGRESS", "RESOLVED"]`.
   - **Real-World Consequence:** The moment an Aspirant answers an SME's question, the ticket transitions to `WAITING_ON_GUIDE_SME` and **the SME is completely locked out of responding or resolving the ticket!**
9. **SME Cannot Set Ticket Status to `WAITING_ON_ASPIRANT`:**
   - **Evidence:** [`views/guide.py:L560`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/guide.py#L560) gives Guides three status choices: `["WAITING_ON_ASPIRANT", "IN_PROGRESS", "RESOLVED"]`. [`views/sme.py:L480` & `L628`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/sme.py#L480) only gives SMEs `["IN_PROGRESS", "RESOLVED"]`, and [`services/help_requests.py:sme_respond_request` (L556)](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/help_requests.py#L556) only recognizes `("OPEN", "IN_PROGRESS", "RESOLVED", "ESCALATED")`—omitting `WAITING_ON_ASPIRANT`!
10. **Single-Column Response Overwrite Destroys Multi-Turn Consultation History:**
    - **Evidence:** `help_requests` stores `guide_response`, `sme_response`, and `aspirant_response` as single text columns ([`services/help_requests.py:L430, L600, L1111`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/help_requests.py#L430)). If a Guide replies on Monday, the Aspirant replies on Tuesday, and the Guide replies again on Wednesday, Monday's `guide_response` is overwritten in place!
11. **SME Portal Is Missing the Case Discussions & Private Mentor Notes Component:**
    - **Evidence:** [`services/collaboration.py:create_case_message` (L33–L65)](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/collaboration.py#L33-L65) and [`list_case_messages` (L152)](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/collaboration.py#L152) explicitly implement authorization for `author_role="sme"` so Guides and SMEs can collaborate via `case_discussions` (including `is_private_mentor_note=True`). Yet `views/sme.py` never imports or renders `list_case_messages` / `create_case_message`!

---

## Workflow D: Guide & SME Assignment, Co-Guides & Handover Lifecycle

### Current Implemented Flow
`Admin Assigns Guide / Co-Guide / SME` $\rightarrow$ `Relationship Upserted` $\rightarrow$ `Assignment History Logged` $\rightarrow$ `On Replacement/Unassignment, OPEN/IN_PROGRESS Tickets Transferred`.

### Missing Business Logic & Edge Cases
12. **Ticket Handover on Mentor Replacement/Unassignment Orphans `WAITING_ON_*` Tickets:**
    - **Evidence:** [`services/relationships.py:L269, L319, L633, L660, L774, L800`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/relationships.py#L269) only updates `help_requests` where `status IN ('OPEN', 'IN_PROGRESS')`.
    - **Real-World Consequence:** Any active consultation in `WAITING_ON_ASPIRANT` or `WAITING_ON_GUIDE_SME` status remains assigned to the old/unassigned Guide or SME! When the Aspirant replies to that ticket, the notification goes to the former mentor who no longer has access to the Aspirant's case!
13. **Co-Guides (`Guide B`) Are Invisible in Aspirant, Guide, and SME "Guidance Team" Screens:**
    - **Evidence:** [`services/relationships.py:get_aspirant_mentors` (L111–L118)](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/relationships.py#L111-L118) returns `"guide"`, `"guide_b"`, and `"guides"` (the full list). However, [`views/aspirant.py:L642`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/aspirant.py#L642), [`views/guide.py:L381`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/guide.py#L381), and [`views/sme.py:L326`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/sme.py#L326) only read `mentors.get("guide")` and never render `mentors.get("guides")[1:]`. Furthermore, the Aspirant Consultation recipient dropdown ([`views/aspirant.py:L808`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/aspirant.py#L808)) only includes the primary `m_guide` and `m_smes`—so an Aspirant can never direct a consultation to their Co-Guide!

---

## Workflow E: Multi-Role Identity, Suspension & NDA Lifecycle

### Current Implemented Flow
`Admin Grants Role (pending_nda)` $\rightarrow$ `User Switches to Role` $\rightarrow$ `Signs NDA (active)` $\rightarrow$ `Admin Can Suspend (suspended) / Reinstate (active) / Revoke (revoked)`.

### Missing Business Logic & Edge Cases
14. **Standalone Guides & SMEs Cannot Have Their Primary Role Suspended or Revoked by Admin:**
    - **Evidence:** In [`views/admin_governance.py:L137-L138`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/admin_governance.py#L137-L138):
      ```python
      primary_r = u.get("primary_role", "aspirant")
      grants = [r for r in u.get("role_grants", []) if r.get("role") != primary_r]
      ```
    - **Real-World Consequence:** If a user was created via Admin Tab 1 (`Create Account`) as a `Guide` (`profiles.role = 'guide'`) or `SME` (`profiles.role = 'sme'`), their `primary_r` is `'guide'` or `'sme'`. Because Tab 7 filters out `r.get("role") != primary_r`, the UI displays `"No secondary role grants to manage"` and provides **zero buttons to suspend, reinstate, or revoke a standalone Guide or SME**! Only hybrid `Aspirant + Guide` users have manage buttons.
15. **Role Suspension Leaves Mentors Looking "Active" to Aspirants & Does Not Re-Route Open Tickets:**
    - **Evidence:** [`services/roles.py:suspend_role` (L273–L305)](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/roles.py#L273-L305) sets `user_roles.status = 'suspended'`. While `get_assigned_aspirants_for_guide` blocks the suspended Guide from viewing their caseload, `get_aspirant_mentors(aspirant_id)` ([`services/relationships.py:L43`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/relationships.py#L43)) does **not** check whether each mentor's role is currently suspended. Thus, the Aspirant still sees the suspended Guide as their active mentor and can submit urgent consultations to a suspended mentor who cannot log in to read them!

---

## Workflow F: Inactivity Monitoring, Confidential Complaints & Conflict Governance

### Current Implemented Flow
`Mentor Assigned` $\rightarrow$ `Day 7 Reminder (Mentor)` $\rightarrow$ `Day 10 Alert (Admin)` $\rightarrow$ `Day 14 Critical Escalation (Admin)` $\rightarrow$ `Admin WhatsApp/Gmail Follow-up`.

### Missing Business Logic & Edge Cases
16. **Closed-Loop Governance Gaps in Complaints & SME Conflicts:**
    - **Confidential Complaints (`guide_complaints`):** When an Aspirant submits a confidential report ([`views/aspirant.py:L738`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/aspirant.py#L738)), they cannot see their submitted complaints on their dashboard, and when Admin resolves the complaint via [`resolve_guide_complaint` (`services/governance.py:L151`)](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/governance.py#L151), **no notification is sent to the Aspirant** and no resolution note is ever shown to the Aspirant.
    - **SME Conflict Declarations (`sme_conflict_declarations`):** SMEs have no UI in [`views/sme.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/sme.py) to declare a conflict of interest (`declare_sme_conflict`), and when a conflict (`has_conflict=True`) is recorded in Tab 10, `assign_sme` ([`services/relationships.py:L403`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/relationships.py#L403)) does not block assigning a conflicted SME at the service layer (only shows a warning in the Admin UI).
