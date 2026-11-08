# FULCRUM-BETA → AGY ARGON: TAB-SWITCHING LATENCY & PERFORMANCE ROOT-CAUSE AUDIT
**Deliverable 3 of 10 | Mode: Read-Only Empirical Profiling & Root-Cause Analysis**  
**Benchmark Script:** [`scratch/benchmark_argon_audit.py`](file:///C:/Users/hp/.gemini/antigravity/brain/22e605d7-a862-4d23-bd2d-9491575ffa3a/scratch/benchmark_argon_audit.py) | **Raw Telemetry:** [`scratch/benchmark_results.json`](file:///C:/Users/hp/.gemini/antigravity/brain/22e605d7-a862-4d23-bd2d-9491575ffa3a/scratch/benchmark_results.json)

---

## 1. Executive Summary: Why Every Tab Click Feels Slow

In Streamlit (`>= 1.38`), passing `on_change="rerun"` to `st.tabs()` causes the entire Python script (`app.py` $\rightarrow$ `render_*_portal()`) to re-execute from top to bottom whenever the user clicks a tab. That optimization **only** speeds up an application if two strict conditions hold:
1. Every tab block (`with tabs[i]:`) is gated by `if is_tab_active(tabs[i]):` so inactive tabs are skipped.
2. Heavy database queries are **not** executed globally above `st.tabs()` or inside uncached $O(N)$ loops on every rerun.

**In Fulcrum-Beta today, both rules are violated across all four portals:**
- **With just 32 Aspirants, 10 Guides, and 8 SMEs** in the live Supabase database:
  - A **cold Admin load / tab switch** fires **306 to 330 sequential HTTPS queries to Supabase**, downloading **1,291 to 1,406 rows** and freezing the browser for **29.7 to 40.9 seconds**!
  - Even a **warm Admin tab switch** (within the 60s memo TTL) still fires **86 to 110 uncached Supabase HTTPS queries** and takes **7.25 to 17.46 seconds** per click!
  - An **Aspirant tab switch** fires **25 Supabase queries (5.19s cold)** and **13 Supabase queries (1.01s warm)** on every click because [`views/aspirant.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/aspirant.py) never calls `is_tab_active()` at all!

---

## 2. Root-Cause Diagnosis (Issues A through D)

### Issue A: Incomplete or Non-Existent `is_tab_active()` Guards Across All 4 Portals

| Portal View File | `on_change="rerun"` Set? | `is_tab_active` Imported? | Tabs Guarded by `if is_tab_active(...)` | Tabs Executed Unconditionally on EVERY Click |
| :--- | :---: | :---: | :---: | :--- |
| [`views/aspirant.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/aspirant.py#L24-L86) | ✅ Yes (`L86`) | ✅ Yes (`L24`) | **0 of 6 (`0%`)** | **All 6 tabs (`tabs[0]`–`tabs[5]`)** run on every tab switch! |
| [`views/guide.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/guide.py#L34-L79) | ✅ Yes (`L79`) | ✅ Yes (`L34`) | **0 of 3 (`0%`)** | **All 3 main tabs (`main_tabs[0]`–`main_tabs[2]`)** run on every tab switch! (Only the inner `st.pills` subtabs in `main_tabs[0]` branch via `if/elif`). |
| [`views/sme.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/sme.py#L22-L62) | ✅ Yes (`L62`) | ✅ Yes (`L22`) | **0 of 3 (`0%`)** | **All 3 main tabs (`tabs[0]`–`tabs[2]`)** run on every tab switch! (Only the inner `st.pills` subtabs in `tabs[0]` branch via `if/elif`). |
| [`views/admin.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/admin.py#L20-L1135) | ✅ Yes (`L163`) | ✅ Yes (`L20`) | **6 of 12 (`50%`)** (`tabs[6]`–`tabs[11]` at `L1099–L1134`) | **First 6 tabs (`tabs[0]`–`tabs[5]`, lines `166–1095`)** have **ZERO `is_tab_active()` guards** and execute on every single Admin tab click! |

> [!CAUTION]
> Setting `on_change="rerun"` on `st.tabs` **without** wrapping each tab body in `if is_tab_active(tabs[i]):` gives you the **worst of both worlds**: before `on_change="rerun"`, Streamlit switched tabs purely client-side in `0 ms` without a server round-trip; adding `on_change="rerun"` forced a full server rerun on every click while still executing all the unguarded tabs!

---

### Issue B: Global Pre-Tab Queries Executed on Every Rerun

1. **Global App Shell Overhead ([`app.py:L888–L1168`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/app.py#L888-L1168)):**
   On every single click anywhere in the app, before any portal view is even reached, `app.py` executes:
   - [`get_primary_admin_id()`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/governance.py#L26-L38) (`L888`) $\rightarrow$ **Uncached!** Calls `list_profiles_by_role("admin")`, which fires **2 Supabase HTTP queries** (`user_roles` + `profiles`).
   - [`get_active_roles(user_id)`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/roles.py#L101) (`L903`) & [`get_pending_nda_roles(user_id)`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/roles.py#L107) (`L904`).
   - [`get_unread_count(user_id)`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/notifications.py#L254) (`L1025`) $\rightarrow$ **Uncached!** Fires 1 Supabase HTTP query.
   - [`list_notifications(user_id, unread_only=False)`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/notifications.py#L148) (`L1031`) $\rightarrow$ **Uncached!** Downloads up to 50 notification rows on every rerun **even when the `"🔔 Notifications"` expander in the sidebar is collapsed!**
   - [`render_terms_and_conditions_gate(user)`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/legal_ui.py#L19) (`L1163`) & [`render_nda_gate(user, role)`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/legal_ui.py#L93) (`L1168`).

2. **Admin Portal Pre-Tab Queries ([`views/admin.py:L93–L99`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/admin.py#L93-L99)):**
   Before `st.tabs()` is even rendered on line 149, `render_admin_portal()` unconditionally runs:
   ```python
   aspirants = list_active_profiles_for_role("aspirant")
   guides = list_active_profiles_for_role("guide")
   smes = list_active_profiles_for_role("sme")
   all_schemes = list_schemes(active_only=False)
   all_admin_queries = list_mentor_admin_queries()
   active_journeys_count = count_active_journeys()
   ```
   - Plus `list_schemes(active_only=False)` bypasses the `_GLOBAL_CACHE["schemes:all_active"]` cache (`services/schemes.py:L43` only caches when `active_only=True`!), downloading all **179 full scheme objects** from Supabase on every Admin rerun—and then **calls `list_schemes()` a second time on line 1040**!

---

### Issue C: Catastrophic $O(U)$ N+1 Query Cascade Inside `list_users_with_multi_roles()` & `list_active_profiles_for_role()`

This is the single biggest performance bottleneck in the entire codebase ([`services/roles.py:L366–L447`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/roles.py#L366-L447)):
1. `list_active_profiles_for_role(target_role)` is called **5 times per Admin rerun** (`L94, L95, L96` at top of `views/admin.py`, and `L759, L760` in Tab 4).
2. Each call to `list_active_profiles_for_role()` calls `list_users_with_multi_roles()` (`L429`), which is **not memoized**.
3. Inside `list_users_with_multi_roles()`:
   - Calls `get_primary_admin_id()` (`2` uncached Supabase queries).
   - Loops `for r in ("aspirant", "guide", "sme"): list_profiles_by_role(r)` (`7` uncached Supabase queries: `user_roles`, `journeys`, `profiles` for aspirant + `user_roles`, `profiles` for guide + `user_roles`, `profiles` for sme).
   - Loops over all $U$ users (`38` distinct non-admin users currently) and calls `get_user_roles(uid)`:
     - On a cold load, `get_user_roles(uid)` queries `user_roles` for `uid` (`1` query), calls `get_profile(uid)` (`1` query), and calls `get_primary_admin_id()` (`2` queries) = **4 queries per user $\times 38$ users = 152 Supabase HTTP round-trips!**
   - Even on a warm load (when `user_roles:{uid}` is cached in `st.session_state`), `list_active_profiles_for_role()` still executes the **9 uncached table scans** in `list_users_with_multi_roles()` + `list_profiles_by_role(target_role)` (`2` queries) + `get_primary_admin_id()` (`2` queries) = **13 Supabase HTTP round-trips per call $\times 5$ calls = 65 redundant HTTP queries on every warm Admin tab click!**

---

### Issue D: Heavy Hidden Widget & DOM Explosion on Every Rerun

- In [`views/admin.py` Tab 5 (`L1040–L1093`)](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/admin.py#L1040-L1093), because `with tabs[5]:` has no `is_tab_active(tabs[5])` guard, Streamlit renders **30 Fund Explorer cards** (`render_fund_explorer_card`), each with an AI Pitch Prompt expander, `st.code` block, and 3 action buttons (`Edit`, `Archive`, `Delete`), plus the `Add New Scheme` form (`20+` inputs) into the WebSocket delta payload on every Admin tab switch.
- In [`views/admin.py` Tab 3 (`L615–L712`)](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/admin.py#L615-L712), because `with tabs[3]:` has no `is_tab_active(tabs[3])` guard, Streamlit loops through all **32 Aspirants** and creates `st.popover("🔄 Replace")` and `st.popover("✖ Unassign")` widgets with nested selectboxes and text inputs for every assigned Guide and SME on every rerun.

---

## 3. Empirical Measurements Across All 17 Workflows (Part 3 — Issue E)

Measured against the live Supabase backend (`32` Aspirants, `10` Guides, `8` SMEs, `179` Schemes, `44` Journey events for `pravindev666@gmail.com`):

| # | Tab-Switch Workflow | Cold Time (`ms`) | Warm Median `p50` (`ms`) | Warm `p95` (`ms`) | Cold Supabase Queries | Warm Supabase Queries | Rows Downloaded (Cold / Warm) | Cache Hits / Misses (Cold) | Peak Memory (`KB`) |
| :- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Aspirant: Dashboard $\rightarrow$ Profile** | `5,190.7 ms` | `1,010.0 ms` | `1,036.7 ms` | `25` | `13` | `241` / `12` | `5` / `12` | `2,311.7 KB` |
| **2** | **Aspirant: Profile $\rightarrow$ Schemes** | `5,190.7 ms` | `1,010.0 ms` | `1,036.7 ms` | `25` | `13` | `241` / `12` | `5` / `12` | `2,311.7 KB` |
| **3** | **Aspirant: Schemes $\rightarrow$ Journey** | `5,190.7 ms` | `1,010.0 ms` | `1,036.7 ms` | `25` | `13` | `241` / `12` | `5` / `12` | `2,311.7 KB` |
| **4** | **Aspirant: Journey $\rightarrow$ My Mentors** | `5,190.7 ms` | `1,010.0 ms` | `1,036.7 ms` | `25` | `13` | `241` / `12` | `5` / `12` | `2,311.7 KB` |
| **5** | **Aspirant: My Mentors $\rightarrow$ Consultations** | `5,190.7 ms` | `1,010.0 ms` | `1,036.7 ms` | `25` | `13` | `241` / `12` | `5` / `12` | `2,311.7 KB` |
| **6** | **Guide: Assigned Aspirants $\rightarrow$ Consultations** | `4,328.7 ms` | `889.6 ms` | `919.7 ms` | `20` | `11` | `9` / `4` | `6` / `5` | `346.4 KB` |
| **7** | **Guide: Consultations $\rightarrow$ My Profile** | `4,328.7 ms` | `889.6 ms` | `919.7 ms` | `20` | `11` | `9` / `4` | `6` / `5` | `346.4 KB` |
| **8** | **Guide: Mentee Profile $\rightarrow$ Scheme Matches** | `4,767.6 ms` | `975.5 ms` | `977.3 ms` | `22` | `12` | `186` / `2` | `5` / `8` | `1,919.3 KB` |
| **9** | **Guide: Scheme Matches $\rightarrow$ Journey** | `4,110.0 ms` | `727.4 ms` | `735.7 ms` | `18` | `9` | `50` / `2` | `3` / `5` | `385.4 KB` |
| **10** | **SME: Assigned Cases $\rightarrow$ Consultations** | `3,984.5 ms` | `790.8 ms` | `805.7 ms` | `17` | `10` | `6` / `2` | `3` / `4` | `291.2 KB` |
| **11** | **SME: Consultations $\rightarrow$ My Profile** | `4,113.7 ms` | `877.1 ms` | `891.7 ms` | `20` | `11` | `9` / `4` | `6` / `5` | `341.6 KB` |
| **12** | **Admin: Overview $\rightarrow$ Create Account** | `29,731.2 ms` | `7,249.4 ms` | `7,687.8 ms` | `306` | `86` | `1,291` / `1,125` | `181` / `108` | `5,706.5 KB` |
| **13** | **Admin: Create Account $\rightarrow$ Guide Assignments** | `29,731.2 ms` | `7,249.4 ms` | `7,687.8 ms` | `306` | `86` | `1,291` / `1,125` | `181` / `108` | `5,706.5 KB` |
| **14** | **Admin: Guide Assignments $\rightarrow$ Mentor Directives** | `29,731.2 ms` | `7,249.4 ms` | `7,687.8 ms` | `306` | `86` | `1,291` / `1,125` | `181` / `108` | `5,706.5 KB` |
| **15** | **Admin: Mentor Directives $\rightarrow$ Scheme Catalogue** | `29,731.2 ms` | `7,249.4 ms` | `7,687.8 ms` | `306` | `86` | `1,291` / `1,125` | `181` / `108` | `5,706.5 KB` |
| **16** | **Admin: Scheme Catalogue $\rightarrow$ Inactivity Monitor** | `40,950.7 ms` | `16,679.3 ms` | `17,464.6 ms` | `330` | `110` | `1,308` / `1,142` | `181` / `152` | `6,344.4 KB` |
| **17** | **Admin: Inactivity Monitor $\rightarrow$ Role Grants** | `30,016.4 ms` | `7,855.8 ms` | `7,955.0 ms` | `316` | `96` | `1,406` / `1,240` | `217` / `108` | `5,749.7 KB` |

*(Note: Workflows 1–5 have identical metrics because `views/aspirant.py` executes all 6 tabs on every click; Workflows 12–15 have identical metrics because `views/admin.py` executes Tabs 0–5 unconditionally on every click).*

---

## 4. Top 10 Slowest Functions / Queries (Cold Execution)

| Rank | Function Call | Cold Time (`ms`) | Supabase HTTP Queries | Rows Fetched | Root Cause of Latency |
| :-: | :--- | :---: | :---: | :---: | :--- |
| **1** | [`list_users_with_multi_roles()`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/roles.py#L366) | **`21,565.7 ms`** | `190` | `259` | Uncached loop calling `get_user_roles(uid)` $\rightarrow$ `get_profile(uid)` $\rightarrow$ `get_primary_admin_id()` per user. |
| **2** | [`list_active_profiles_for_role('aspirant')`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/roles.py#L408) | **`18,324.1 ms`** | `196` | `343` | Calls `list_profiles_by_role` + `list_users_with_multi_roles()` without batching or memoization. |
| **3** | [`get_assigned_aspirants_for_guide(guide_id)`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/relationships.py#L887) | **`2,645.4 ms`** | `5` | `4` | Performs `user_has_active_role` + `check_user_nda_accepted` + `relationships` scan + `get_profiles_batch`. |
| **4** | [`list_requests(aspirant_id)`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/help_requests.py#L258) | **`2,463.9 ms`** | `2` | `6` | Unauthenticated user client falls back to `admin_client` after RLS check + `_enrich_mentor_names`. |
| **5** | [`get_aspirant_mentors(asp_id)`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/relationships.py#L43) | **`2,373.5 ms`** | `2` | `1` | Initial TLS connection + `relationships` query + `get_profiles_batch`. |
| **6** | [`get_journey_timeline(asp_id)`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/journey.py#L156) | **`2,340.4 ms`** | `2` | `44` | User client query falls back to `admin_client` on `journey_events` join. |
| **7** | [`list_schemes(active_only=False)`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/schemes.py#L32) | **`1,379.9 ms`** | `1` | `179` | Bypasses `_GLOBAL_CACHE["schemes:all_active"]` when `active_only=False`; downloads 179 full JSON rows. |
| **8** | [`match_schemes_for_aspirant(asp_id)`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/schemes.py#L236) | **`1,360.7 ms`** | `1` | `179` | Downloads 179 schemes on cold cache + runs `match_aspirant_schemes_intelligent` across 179 schemes. |
| **9** | [`get_primary_admin_id()`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/governance.py#L26) | **`212.4 ms`** | `2` | `2` | **Completely uncached!** Called 40+ times during a cold Admin load, adding `~8.5 seconds` of pure waste. |
| **10** | [`count_active_journeys()`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/journey.py) | **`122.0 ms`** | `1` | `32` | Uncached table scan run on every Admin rerun before `st.tabs`. |

---

## 5. Scaling Behavior Analysis at 100, 1,000, and 10,000 Users

Using the measured empirical query complexity formulas ($Q_{\text{cold}} = 4U_{\text{total}} + 2A + 62$ for Admin cold load, $Q_{\text{warm}} = 86 + A_{\text{uncached}}$ for Admin warm tab switch, at the measured mean Supabase round-trip of `88.5 ms/query`):

| User Scale ($U$ Total Users / $A$ Aspirants) | Admin Cold Load Queries | Admin Cold Load Time | Admin Warm Tab Switch Time | Tab 3 Mentor Allocation Queries | Scaling Verdict (Current Code) |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Current Baseline ($U=50, A=32$)** | `306 queries` | **`29.7 sec`** | **`7.25 sec`** | `64 queries` (cold) | ⚠️ Already unacceptable UX (`>7s` per click) |
| **100 Users ($U=100, A=75$)** | `~612 queries` | **`~54.1 sec`** | **`~8.8 sec`** | `150 queries` (cold) | ❌ Severe browser freeze & rate-limit risk |
| **1,000 Users ($U=1,000, A=800$)** | `~5,660 queries` | **`~501 sec (8.3 min)`** | **`~19.5 sec`** | `1,600 queries` (cold) | ❌ Complete failure (HTTP connection pool exhaustion & Streamlit timeout) |
| **10,000 Users ($U=10,000, A=8,500$)** | `~57,000 queries` | **`~84 minutes`** | **`~140 sec`** | `17,000 queries` (cold) | ❌ Total platform outage |

---

## 6. Safe, Non-Breaking Performance Remediation Plan (Issue F)

Without changing any business rules, database schemas, or visual layouts, we can reduce **warm tab switching from `1,010–16,679 ms` down to `< 80 ms` (`0` Supabase queries)** and **cold Admin load from `29.7s` (`306` queries) down to `< 1.2s` (`6` batched queries)** via five surgical fixes:

1. **Enforce `if is_tab_active(tabs[i]):` Across All 4 Portals (`P0`):**
   - Wrap `tabs[0]`–`tabs[5]` in [`views/aspirant.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/aspirant.py#L88-L1004).
   - Wrap `main_tabs[0]`–`main_tabs[2]` in [`views/guide.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/guide.py#L85-L1234).
   - Wrap `tabs[0]`–`tabs[2]` in [`views/sme.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/sme.py#L67-L744).
   - Wrap `tabs[0]`–`tabs[5]` in [`views/admin.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/admin.py#L166-L1095).
2. **Cache `get_primary_admin_id()` Globally (`P0`):**
   - In [`services/governance.py:get_primary_admin_id()`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/governance.py#L26-L38), cache the resolved UUID in `_GLOBAL_CACHE["primary_admin_id"]` (`ttl_seconds=3600`). Eliminates `40+` Supabase queries per cold load and `12+` queries per warm rerun immediately.
3. **Eliminate the N+1 Loop in `list_users_with_multi_roles()` & Memoize `list_active_profiles_for_role()` (`P0`):**
   - In [`services/roles.py:list_users_with_multi_roles()`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/roles.py#L366-L405), fetch all `profiles` and all `user_roles` in **2 single batch queries** (`client.table("profiles").select("*").neq("is_active", False)` and `client.table("user_roles").select("*")`), join them in Python memory in `< 2 ms`, and memoize the result for `60s`.
   - Reduces `list_users_with_multi_roles()` from **`190 queries` (`21.5s`) $\rightarrow$ `2 queries` (`~180 ms`)** — a **100x speedup** that scales to 10,000 users!
4. **Cache All Schemes (`schemes:all`) & Memoize Sidebar Notifications (`P1`):**
   - In [`services/schemes.py:list_schemes()`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/schemes.py#L43), cache `schemes:all` (including archived schemes, filtering `is_active` in memory) with `ttl_seconds=300`, and call `invalidate_global_cache("schemes:all")` inside `upsert_scheme`, `toggle_archive_scheme`, and `delete_scheme`.
   - In [`services/notifications.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/notifications.py), memoize `get_unread_count(user_id)` and `list_notifications(user_id)` for `30s` (invalidating on `create_notification`, `mark_as_read`, and `mark_all_as_read`).
5. **Batch `get_all_relationships()` in Admin Tab 3 & Defer Pre-Tab Queries (`P1`):**
   - In [`views/admin.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/admin.py#L93-L99), memoize header KPI counts (`60s` TTL) and only fetch full lists inside the active tab.
   - In Admin Tab 3 (`Guide & SME Assignments`), use a single `get_all_relationships()` + `get_profiles_batch()` lookup instead of calling `get_aspirant_mentors(aid)` 32 times in a loop.

### Projected Performance After Remediation

| Workflow | Current Cold / Warm `p50` | Post-Fix Cold / Warm `p50` | Query Reduction |
| :--- | :---: | :---: | :---: |
| **Aspirant Tab Switch** | `5,191 ms` / `1,010 ms` (`25` / `13` queries) | **`~380 ms` / `< 35 ms` (`3` / `0` queries)** | **-100% warm queries** |
| **Guide / SME Tab Switch** | `4,329 ms` / `890 ms` (`20` / `11` queries) | **`~410 ms` / `< 35 ms` (`4` / `0` queries)** | **-100% warm queries** |
| **Admin Tab Switch (Tabs 0–5)** | `29,731 ms` / `7,249 ms` (`306` / `86` queries) | **`~850 ms` / `< 60 ms` (`6` / `0` queries)** | **-98% cold / -100% warm** |
| **Admin Tab 6 (Inactivity)** | `40,951 ms` / `16,679 ms` (`330` / `110` queries) | **`~950 ms` / `< 80 ms` (`7` / `0` queries)** | **-98% cold / -100% warm** |
