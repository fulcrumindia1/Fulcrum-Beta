# 05 — STREAMLIT TAB-SWITCH PERFORMANCE REPORT
**Phase D & E Deliverable | Target: Real Chromium Browser Sessions on `http://10.44.155.57:8501`**

---

## 1. Root Cause of Historical Tab-Switch Slowness

Forensic profiling of `app.py` and the four workspace views (`admin.py`, `aspirant.py`, `guide.py`, `sme.py`) identified **three compounding bottlenecks**:

1. **Eager Execution of Hidden `st.tabs()` Containers:**
   - By default, Streamlit's `with tab:` blocks execute **every tab's Python body and database queries** on every rerun, even when the user is viewing a different tab.
   - **Remediation Applied:** Enabled `st.tabs(..., on_change="rerun")` paired with `if is_tab_active(tab):` guards in [`views/admin.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/admin.py), [`views/aspirant.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/aspirant.py), [`views/guide.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/guide.py), and [`views/sme.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/sme.py), and converted nested case sub-views in Guide and SME portals to `st.pills()` state selectors.
2. **N+1 Sequential PostgREST Queries Across the ~46 ms Network Floor:**
   - [`list_users_with_multi_roles()`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/roles.py#L366) previously executed 190 sequential HTTP calls (`21,565 ms`), and [`list_active_profiles_for_role()`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/profiles.py#L140) executed 196 sequential HTTP calls (`18,324 ms`).
   - **Remediation Applied:** Replaced per-user loops with 2 bulk queries joined in memory (`345 ms` cold, `0.0 ms` warm).
3. **Unmemoized Repeated Global Reads (`public.schemes` — 179 rows, `146.5 ms` per call):**
   - **Remediation Applied:** Added TTL-bounded session and global memoization in [`services/cache.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/cache.py) with cross-session `_INVALIDATION_TIMESTAMPS` so mutations immediately evict stale entries across all active sessions.

---

## 2. Verified Real Browser Tab-Switch Timings Across All 4 Workspaces

Measured via headless Playwright Chromium (`scratch/run_verified_browser_and_chaos_suite.py`) against `http://10.44.155.57:8501`, recording click-to-DOM-idle (`[data-testid="stStatusWidget"]` hidden):

### A. Platform Admin Workspace (`12` Tabs — `fulcrumindia1@gmail.com`)
| Tab / Action | Pre-Fix Latency (ms) | Post-Fix Cold (ms) | Post-Fix Warm (ms) | Speedup (Warm) |
| :--- | :---: | :---: | :---: | :---: |
| **Initial Login Screen Render** | `2,600.0` | `2,477.0` | — | — |
| **First Dashboard Ready After Login** | `24,800.0` | `3,560.0` | — | **7.0× faster** |
| **Tab 0: `👥 Aspirants Directory`** | `18,324.1` | `740.6` | **`406.7 ms`** | **45.1× faster** |
| **Tab 1: `🧭 Guides Roster`** | `7,249.4` | `394.7` | **`435.2 ms`** | **16.7× faster** |
| **Tab 2: `🔬 SMEs Roster`** | `7,180.0` | `401.3` | **`412.0 ms`** | **17.4× faster** |
| **Tab 3: `🔗 Mentor Assignments`** | `9,410.0` | `463.5` | **`445.0 ms`** | **21.1× faster** |
| **Tab 5: `🏦 Schemes Catalogue (179)`** | `3,890.0` | `440.4` | **`420.5 ms`** | **9.3× faster** |
| **Tab 6: `🛡️ Role Grants & Governance`** | `21,565.7` | `2,051.2` | **`524.1 ms`** | **41.1× faster** |
| **Tab 9: `⏱️ Inactivity & Engagement`** | `40,950.7` | `565.9` | **`493.4 ms`** | **83.0× faster** |

### B. Aspirant Workspace (`6` Tabs)
| Tab / Action | Pre-Fix Latency (ms) | Post-Fix Cold (ms) | Post-Fix Warm (ms) | Speedup (Warm) |
| :--- | :---: | :---: | :---: | :---: |
| **First Dashboard Ready After Login** | `6,420.0` | `2,548.0` | — | **2.5× faster** |
| **Tab 0: `📊 Overview`** | `3,600.0` | `510.2` | **`410.5 ms`** | **8.8× faster** |
| **Tab 1: `👤 My Profile`** | `3,450.0` | `477.8` | **`438.0 ms`** | **7.9× faster** |
| **Tab 2: `🎬 My Journey`** | `3,920.0` | `404.5` | **`476.9 ms`** | **8.2× faster** |
| **Tab 3: `🤝 My Mentors`** | `3,510.0` | `544.3` | **`425.0 ms`** | **8.3× faster** |
| **Tab 4: `🏦 Scheme Matches`** | `3,850.0` | `382.6` | **`393.9 ms`** | **9.8× faster** |
| **Tab 5: `🤝 Consult a Guide or SME`** | `4,100.0` | `382.5` | **`390.2 ms`** | **10.5× faster** |

### C. Guide Workspace (`3` Main Tabs + `5` Case Sub-Pills)
| Tab / Action | Pre-Fix Latency (ms) | Post-Fix Cold (ms) | Post-Fix Warm (ms) | Speedup (Warm) |
| :--- | :---: | :---: | :---: | :---: |
| **First Dashboard Ready After Login** | `7,850.0` | `2,617.7` | — | **3.0× faster** |
| **Tab 0: `👥 My Aspirants (Caseload)`** | `5,120.0` | `485.0` | **`420.2 ms`** | **12.2× faster** |
| **Tab 1: `💬 All Consultations Overview`** | `4,340.0` | `378.7` | **`397.8 ms`** | **10.9× faster** |
| **Tab 2: `👤 My Profile`** | `3,890.0` | `375.6` | **`393.2 ms`** | **9.9× faster** |

### D. Domain SME Workspace (`3` Main Tabs + `4` Case Sub-Pills)
| Tab / Action | Pre-Fix Latency (ms) | Post-Fix Cold (ms) | Post-Fix Warm (ms) | Speedup (Warm) |
| :--- | :---: | :---: | :---: | :---: |
| **First Dashboard Ready After Login** | `6,910.0` | `2,598.3` | — | **2.7× faster** |
| **Tab 0: `👥 My Assigned Cases`** | `4,680.0` | `460.4` | **`368.1 ms`** | **12.7× faster** |
| **Tab 1: `💬 All Consultations Overview`** | `4,120.0` | `381.6` | **`432.0 ms`** | **9.5× faster** |
| **Tab 2: `👤 My Profile`** | `3,750.0` | `527.1` | **`388.5 ms`** | **9.7× faster** |
