# FULCRUM-BETA → AGY ARGON: PROPOSED FEATURES WITHIN EXISTING TABS
**Deliverable 8 of 10 | Mode: Read-Only Product Enhancement Proposals (No New Top-Level Pages)**

---

## Design Constraint & Anti-Bloat Principle

In strict compliance with **Non-Negotiable Invariant 4** and **Invariant 6**:
- **Zero new top-level pages or tabs** are proposed. Every enhancement embeds compactly inside an existing tab.
- **Explicitly Rejected Feature Bloat:** We explicitly **reject** adding a Document Vault, file attachment repositories, real-time WebSocket chat rooms, automated WhatsApp/email background daemons, secondary/district Admin hierarchies, payment gateways, or social feeds.

---

## Proposed Enhancement 1: Post-Release Scheme Application Tracker (Inside Aspirant `Scheme Matches` & Guide `Scheme Matches`)

| # | Evaluation Criterion | Specification |
| :- | :--- | :--- |
| **1** | **Existing tab where it belongs** | Aspirant Tab 2 (`Scheme Matches`, [`views/aspirant.py:L472`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/aspirant.py#L472)) & Guide Tab 0 $\rightarrow$ Subtab 2 (`Scheme Matches`, [`views/guide.py:L202`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/guide.py#L202)). |
| **2** | **Problem it solves** | Currently, once a Guide releases a scheme (`status = 'RELEASED'`), the workflow dead-ends. Neither the Aspirant, the Guide, nor the Admin knows whether the founder is preparing their DPR, has applied on the government portal, or received sanction/rejection. |
| **3** | **Who benefits** | Aspirant (tracks their grant pipeline), Guide (knows which applications need DPR review), Admin (measures real funding conversion). |
| **4** | **Exact user flow** | On each released scheme card in `views/aspirant.py`, a compact status pill + dropdown allows the Aspirant (or assigned Guide) to update `application_stage`: `Recommended` $\rightarrow$ `Preparing Application / DPR` $\rightarrow$ `Submitted on Portal` $\rightarrow$ `Sanctioned / Funded` (or `Not Pursuing` / `Rejected`), with an optional reference note. |
| **5** | **UI placement** | Compact 1-line footer bar inside the existing `Released to Aspirant` card container. |
| **6** | **Data model / table impact** | Uses existing `scheme_releases` table (either storing `application_stage` inside an optional column or logging stage updates via `journey_events` if zero-DDL is preferred). |
| **7** | **Service-layer logic** | `update_scheme_application_stage(aspirant_id, scheme_id, actor_id, actor_role, new_stage, note)` in [`services/schemes.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/schemes.py). |
| **8** | **Security & authorization rules** | Only the owning `aspirant`, an active assigned `guide`, or `admin` can update the application stage. |
| **9** | **Notification behavior** | When Aspirant marks a scheme `Submitted on Portal` or `Sanctioned`, notifies the assigned Guide. |
| **10** | **Journey / audit impact** | Automatically logs a Journey milestone (`"Applied for Scheme: {name}"` or `"Funding Sanctioned: {name}"`) on the chronological spine! |
| **11** | **Performance impact** | Zero extra queries (rides on existing `get_released_schemes_for_aspirant` payload). |
| **12** | **Why it fits Fulcrum without bloat** | Completes the core mission of Fulcrum (helping entrepreneurs obtain government funding) without adding any document uploads or external portal scraping. |

---

## Proposed Enhancement 2: Mentee Attention Badges in Guide & SME Selector Dropdowns

| # | Evaluation Criterion | Specification |
| :- | :--- | :--- |
| **1** | **Existing tab where it belongs** | Guide Tab 0 (`My Assigned Aspirants`, [`views/guide.py:L100`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/guide.py#L100)) & SME Tab 0 (`My Assigned Cases`, [`views/sme.py:L80`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/sme.py#L80)). |
| **2** | **Problem it solves** | When a Guide or SME has 10+ assigned entrepreneurs, the `"Select Mentee to Manage"` dropdown only shows `Name — Business (District)`. Mentors have to click through mentees one by one to discover who has an unanswered consultation or needs scheme review. |
| **3** | **Who benefits** | Guides and SMEs (instant caseload triage). |
| **4** | **Exact user flow** | The existing `asp_options` formatter appends a concise status indicator to each mentee in the dropdown: e.g., `Pravin A Mathew — Millet Foods (Chennai) [🔴 1 Reply Needed]` or `[🟡 0 Schemes Released]` or `[🟢 Up to Date]`. |
| **5** | **UI placement** | Directly inside the existing `format_func` of `st.selectbox("Select Mentee to Manage")` (`views/guide.py:L103`, `views/sme.py:L83`). Zero new widgets! |
| **6** | **Data model / table impact** | Zero schema changes. |
| **7** | **Service-layer logic** | Computed in memory from `list_guide_requests(guide_id)` / `list_sme_requests(sme_id)`, which is already fetched right below the dropdown! |
| **8** | **Security & authorization rules** | Scoped strictly to the mentor's authorized, NDA-gated caseload. |
| **9** | **Notification behavior** | None required. |
| **10** | **Journey / audit impact** | None required. |
| **11** | **Performance impact** | `0 ms` / `0` extra queries (reuses `all_guide_tickets` already in memory at `views/guide.py:L113`). |
| **12** | **Why it fits Fulcrum without bloat** | Applies Nielsen's **Recognition Rather Than Recall** heuristic using zero screen space. |

---

## Proposed Enhancement 3:SME Case Collaboration & Conflict Self-Declaration (Inside SME `Consultations` Subtab)

| # | Evaluation Criterion | Specification |
| :- | :--- | :--- |
| **1** | **Existing tab where it belongs** | SME Tab 0 $\rightarrow$ Subtab 4 (`Consultations`, [`views/sme.py:L373`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/sme.py#L373)). |
| **2** | **Problem it solves** | Backend services in [`services/collaboration.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/collaboration.py) and [`services/governance.py:declare_sme_conflict`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/governance.py#L188) were built for SMEs, but never wired into `views/sme.py`. SMEs currently cannot read/post private mentor notes with the Guide and cannot self-declare a Conflict of Interest as required by NDA Clause 3. |
| **3** | **Who benefits** | SMEs, Guides (shared private case notes), and Admin (conflict compliance). |
| **4** | **Exact user flow** | At the bottom of SME Subtab 4 (`Consultations`), render the same **Case Discussions & Private Mentor Notes** feed used in `views/guide.py:L975-L1010`, plus a compact `⚖️ Declare Conflict of Interest` expander calling `declare_sme_conflict`. |
| **5** | **UI placement** | Inside `views/sme.py` Subtab 4 (`Consultations`). |
| **6** | **Data model / table impact** | Zero schema changes (`case_discussions` and `sme_conflict_declarations` already exist). |
| **7** | **Service-layer logic** | Calls existing `list_case_messages(selected_asp_id, requesting_role="sme", viewer_id=sme_id)`, `create_case_message(...)`, and `declare_sme_conflict(...)`. |
| **8** | **Security & authorization rules** | Enforces NDA and active SME assignment via `collaboration.py`. |
| **9** | **Notification behavior** | Notifies Admin if an SME declares `has_conflict=True`; notifies Guide/Aspirant on new case discussion message. |
| **10** | **Journey / audit impact** | Records conflict declaration in `sme_conflict_declarations`. |
| **11** | **Performance impact** | Only executes when SME explicitly clicks the `Consultations` pill (`active_sme_sub == "consultations"`). |
| **12** | **Why it fits Fulcrum without bloat** | Wires up already-written backend governance and collaboration logic that was left disconnected in the SME UI. |

---

## Proposed Enhancement 4: Aspirant Confidential Report Status Tracker (Inside Aspirant `My Mentors` Tab)

| # | Evaluation Criterion | Specification |
| :- | :--- | :--- |
| **1** | **Existing tab where it belongs** | Aspirant Tab 4 (`My Mentors`, [`views/aspirant.py:L730`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/aspirant.py#L730)). |
| **2** | **Problem it solves** | When an Aspirant files a confidential complaint or Guide reassignment request to Fulcrum Support, it vanishes into a black hole—the Aspirant cannot see their past submissions or whether Fulcrum Support has reviewed/resolved it. |
| **3** | **Who benefits** | Aspirants (trust and transparency) and Admin (closes the feedback loop as `"Fulcrum Support"`). |
| **4** | **Exact user flow** | Inside the existing `🛡️ Confidential Support & Reassignment Request` expander (`views/aspirant.py:L734`), display a compact history of the Aspirant's own submitted reports showing Status (`PENDING`, `UNDER_REVIEW`, `RESOLVED`) and Fulcrum Support's resolution message. |
| **5** | **UI placement** | Directly below the submission form inside the existing expander in `views/aspirant.py:L788`. |
| **6** | **Data model / table impact** | Zero schema changes (`guide_complaints` already stores `status` and `resolution_notes`). |
| **7** | **Service-layer logic** | Filter `list_guide_complaints()` by `aspirant_id == user_profile["id"]` and dispatch a notification from `"Fulcrum Support"` inside `resolve_guide_complaint()`. |
| **8** | **Security & authorization rules** | Strictly scoped to `aspirant_id == session_user_id`; Guides and SMEs remain 100% blocked from seeing `guide_complaints`. |
| **9** | **Notification behavior** | When Admin resolves/updates a complaint in Tab 8, dispatches an in-app notification to the Aspirant from `"Fulcrum Support"`. |
| **10** | **Journey / audit impact** | Never logged on the public Journey timeline (preserves strict confidentiality from Guides/SMEs). |
| **11** | **Performance impact** | Memoized per aspirant (`60s` TTL). |
| **12** | **Why it fits Fulcrum without bloat** | Closes a broken communication loop using existing database columns. |

---

## Proposed Enhancement 5: Admin Action-Required Triage Strip (Top of Admin `Aspirants & Journeys` Tab 0)

| # | Evaluation Criterion | Specification |
| :- | :--- | :--- |
| **1** | **Existing tab where it belongs** | Top of Admin Tab 0 (`Aspirants & Journeys`, [`views/admin.py:L166`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/admin.py#L166)). |
| **2** | **Problem it solves** | With 12 horizontal tabs, the Single Admin has to hunt across Tabs 3, 4, 6, 7, 8, and 10 to see if there are unassigned Aspirants, pending Mentor Directives, pending Scheme Support Reviews, 14-day Inactivity Escalations, pending NDAs, or unresolved Confidential Complaints. |
| **3** | **Who benefits** | Single Platform Admin (`fulcrumindia1@gmail.com`). |
| **4** | **Exact user flow** | A compact 1-row "Pending Governance Triage" pill bar at the top of Tab 0 showing live counts only for queues with `count > 0` (e.g., `⚠️ 2 Unassigned Aspirants`, `🏛️ 1 Mentor Directive Pending`, `🛡️ 1 Confidential Report`, `⏳ 1 Pending NDA`). |
| **5** | **UI placement** | Compact alert strip at the top of Admin Tab 0. |
| **6** | **Data model / table impact** | Zero schema changes. |
| **7** | **Service-layer logic** | Uses lightweight cached counts (`ttl_seconds=60`). |
| **8** | **Security & authorization rules** | Admin-only. |
| **9** | **Notification behavior** | None. |
| **10** | **Journey / audit impact** | None. |
| **11** | **Performance impact** | Negligible (`< 10 ms` from memoized batch state). |
| **12** | **Why it fits Fulcrum without bloat** | Eliminates daily tab-hunting across 12 tabs for the Single Admin. |
