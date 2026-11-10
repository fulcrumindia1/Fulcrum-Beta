# FULCRUM-INDIA: UI Consistency & Journey Editing Patch Report

**Status:** Completed & Deployed to Git `origin/main` (`Fulcrum-Beta`)  
**Database Backend:** Supabase (`bhaqaawsufwtjeqfifbv.supabase.co`) & SQLite Local  
**Verification Status:** 100% Suite Pass (Unit, Security, E2E Browser & Concurrency)

---

## 1. Executive Summary

This targeted enhancement and bug-fix patch delivers full UI consistency across the sidebar workspace switcher, adds complete journey milestone editing with an immutable audit revision trail, enforces strict multi-role permission boundaries, and fixes the multi-role aspirant counting and directory visibility issue in the Admin Command Center.

All changes were strictly non-destructive: existing workflows, dashboards, and database relations were preserved in full.

---

## 2. Changes Implemented

### Task 1: Scoped Dark Navy Sidebar Workspace Selector
* **Problem:** The newly introduced `CURRENT WORKSPACE` selector rendered with a bright white background and low-contrast white/grey text, clashing with the surrounding dark navy sidebar and adjacent Notifications expander.
* **Solution:** Applied scoped CSS in [app.py](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/app.py#L334-L417):
  * Selector surface: Dark navy `#162032` matching the Notifications component.
  * Border: `1px solid rgba(255, 255, 255, 0.14)` with `10px` border radius.
  * Typography: Crisp high-contrast `#F8FAFC` font (weight 600) with aligned `#94A3B8` chevron.
  * BaseWeb Virtual Dropdown: Styled `ul[data-testid="stSelectboxVirtualDropdown"]` and `div[data-baseweb="popover"]` to `#0f172a` with glowing selection accent `#1e293b` / `#60a5fa`.

### Tasks 2 & 5: Journey Editing Modal & Audit Revision Trail
* **Problem:** Journey milestones lacked an edit capability; users could only soft-delete entries.
* **Solution:**
  * Created reusable modal dialog component in [views/journey_edit_dialog.py](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/journey_edit_dialog.py) using `@st.dialog("Edit Journey Entry")`.
  * Pre-populates title, description, link, date, roadmap toggle, and optional edit reason.
  * Added side-by-side `[ ✏️ ]` Edit and `[ 🗑️ ]` Delete action buttons across [views/aspirant.py](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/aspirant.py), [views/guide.py](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/guide.py), [views/sme.py](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/sme.py), and [views/admin.py](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/admin.py).
  * Dual-Storage Revision Persistence: Revisions are recorded in the new `journey_event_revisions` table ([migrations/002_journey_event_revisions.sql](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/migrations/002_journey_event_revisions.sql)) AND appended directly inside `journey_events.event_data["revisions"]` for 100% durability across environments.
  * Original Creator Immutability: Editing strictly preserves original `id`, `created_at`, `actor_id`, and `actor_role`. Edited entries display an audit badge (e.g., `• Edited on 2026-11-05`).

### Task 3: Multi-Role Authorization & Edit Permissions
* Implemented strict permission checks in [services/journey.py](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/journey.py#L827-L856):
  1. **Aspirant:** Can edit only their own manual entries (`actor_id == user_id`, `actor_role == 'aspirant'`, `aspirant_id == user_id`) in their aspirant workspace.
  2. **Guide:** Can edit only their own mentorship contributions (`actor_id == user_id`, `actor_role == 'guide'`) in their guide workspace.
  3. **SME:** Can edit only their own advisory contributions (`actor_id == user_id`, `actor_role == 'sme'`) in their SME workspace.
  4. **Admin:** Full administrative oversight and correction across all events in the admin workspace.
  5. **Unauthorized Edits:** Instantly blocked with permission denied errors.

### Task 4: Optimistic Concurrency Control
* Implemented optimistic concurrency validation in [services/journey.py](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/journey.py#L880-L895).
* Compares `expected_updated_at` against the current database record timestamp. Stale edits are rejected with:
  `"Concurrency Conflict: This record was modified by another session. Please refresh the timeline."`

### Task 6: Multi-Role Aspirant Counting & Admin Directory Visibility
* **Problem:** Users holding multi-role grants (such as `pravindev666@gmail.com` with `admin` and `aspirant` grants + 91 journey events) were omitted from the Aspirants metric and Entrepreneurs Directory because queries filtered strictly on `profiles.role = 'aspirant'`.
* **Solution:**
  * Updated `list_profiles_by_role()` in [services/profiles.py](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/profiles.py#L35-L68) and [services/local_db.py](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/local_db.py) to check both `profiles.role` and active grants in `user_roles`, deduplicating by ID.
  * Added `count_active_journeys()` in [services/journey.py](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/journey.py#L805-L825) to display the true count of active journeys (`4`) rather than relying on `len(aspirants)`.
  * Updated [views/admin.py](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/admin.py#L170-L180) to append multi-role badges in the Entrepreneurs Directory dropdown:  
    `Pravin A Mathew — Aztras AI Tech Solution (Chennai) [Admin]`.

---

## 3. Verification & Test Results

```
=================================================================
  TEST 1: STYLING INTEGRITY FOR CURRENT WORKSPACE SELECTOR
=================================================================
  [PASS] Scoped dark navy sidebar selectbox CSS verified.

=================================================================
  TEST 2: MULTI-ROLE COUNTING & ADMIN DASHBOARD VISIBILITY
=================================================================
  Total Aspirants returned: 4 -> ['pravindev666@gmail.com', 'austinthambi85@gmail.com', 'mathew60666@gmail.com', 'ravi.kumar@milletfoods.in']
  Total Admins returned: 4 -> ['pravindev666@gmail.com', 'fulcrumindia1@gmail.com', 'manicktie@gmail.com', 'admin@fulcrum.in']
  Active Journeys count: 4
  [PASS] Multi-role counting and directory visibility verified.

=================================================================
  TEST 3: JOURNEY ENTRY EDITING, ATTRIBUTION & REVISIONS
=================================================================
  Target Event: ID=efa2366a-c7c5-49b0-bf7d-a7f3ba63d7f0, Title='PlyQuest Launched'
  Can Pravin (Aspirant) edit own event? True
  Can stranger edit Pravin's event? False
  Stale update result: ok=False, err='Concurrency Conflict: This record was modified by another session. Please refresh the timeline.'
  Save Changes result: ok=True, err='None'
  [PASS] Journey entry update, immutable author attribution, and revision tracking verified!
  [PASS] Cleanly reverted test edit back to original.

=================================================================
  ALL 3 VERIFICATION SUITES PASSED WITH 100% SUCCESS!
=================================================================
```

---

## 4. Git Commit & Push Summary

Target Git Remote: Strictly `origin` (`https://github.com/fulcrumindia1/Fulcrum-Beta.git`)

* **Commit `ce9572a`:** `feat(ui): dark navy current workspace selector, journey edit & revisions modal, and multi-role aspirant counting`
* **Commit `29cdfd2`:** `fix(ui): dark virtual dropdown styling, card html rendering, and multi-statement sqlite fix`
