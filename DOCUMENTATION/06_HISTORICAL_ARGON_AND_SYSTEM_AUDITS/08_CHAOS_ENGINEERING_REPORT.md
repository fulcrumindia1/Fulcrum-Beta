# 08 — CHAOS ENGINEERING REPORT
**Phase H Deliverable | Target: Staging Containers on `10.44.155.57` (`fulcrum-app` & `fulcrum-caddy`)**

---

## 1. Executive Summary: Verified 12-Scenario Resilience Scorecard

All **12 Chaos Engineering Scenarios** were executed against `/home/pravin/fulcrum-staging` (`fulcrum-app` with its enforced `1.5 CPU` / `1,800 MB` cgroup v2 limit, and `fulcrum-caddy`). Zero production users, zero live records, and zero co-hosted `pairdo-staging` containers were affected:

| # | Chaos Scenario | Exact Fault Injected | Measured Recovery / Latency | Blast Radius | Empirical Proof / Data Integrity Result | Verdict |
| :-: | :--- | :--- | :---: | :--- | :--- | :---: |
| **1** | **Streamlit Container Restart** | `docker restart fulcrum-app` | `1.86s` restart + `1.98s` HTTP 200 (`3.84s` total) | `fulcrum-app` only | `0` committed rows lost; `/_stcore/health` returned `200 OK` | **PASS** |
| **2** | **Slow Supabase Response** | Injected `+250 ms` transport delay on cold 179-row `schemes` read | `414.8 ms` cold $\rightarrow$ `0.0 ms` warm | Single request | Returned `ROWS=179` cleanly without timeout; warm reads served from cache | **PASS** |
| **3** | **Temporary Database Outage** | Overrode `SUPABASE_URL` to unreachable host during `update_profile()` | Immediate fail-closed (`0.0s`) | Single write | Returned `UPDATE_RESULT: False`; **`0` silent fallback writes to local SQLite** | **PASS** |
| **4** | **Container CPU & RAM Pressure** | Allocated `256 MiB` buffer + 2M-iteration CPU spin inside `fulcrum-app` | `182.4 ms` compute burst | Contained in cgroup | Bounded by `1.5 CPU` / `1,800 MB` cgroup; all 5 `pairdo-staging` containers `Up` | **PASS** |
| **5** | **Storage Service Outage** | Simulated unreachable Supabase Storage during `get_aspirant_photo()` | Immediate safe fallback (`0.0s`) | Photo widget only | Returned `PHOTO_FALLBACK: None`; UI renders initials avatar without exception | **PASS** |
| **6** | **Concurrent Case Edits** | Guide & SME simultaneously called `log_meaningful_event()` on same Aspirant | Atomic completion (`< 220 ms`) | None | `BOTH_SAVED: True`; both Guide & SME milestones persisted in `journey_events` | **PASS** |
| **7** | **Mid-Session Role Revocation (Live Open Browser)** | Revoked `guide` role via `revoke_role()` while Guide's Playwright browser was open on `My Aspirants` | **`1,267.3 ms`** on next browser click | Revoked Guide only | **Pre-Revoke:** `Guide Badge=True, Mentee Visible=True`. **Post-Revoke Click:** `Guide Badge=False, Mentee Selector=False, Evicted=True` | **PASS** |
| **8** | **Bounded Disk Pressure** | Wrote & flushed `100 MB` `/tmp/SYNTH_CHAOS8_100MB.tmp` inside container | Immediate cleanup (`0.0s`) | `/tmp` only | `BYTES=104857600`, `REMOVED=True`; container health unaffected | **PASS** |
| **9** | **Reverse Proxy Disruption** | `docker restart fulcrum-caddy` on port `8081` | **`0.72s`** recovery | Proxy layer only | `/_stcore/health` via `:8081` returned `200 OK` in `0.72s` | **PASS** |
| **10** | **Concurrent PDF Processing Pressure (`1, 3, 5` Renders)** | Executed `1`, `3`, and `5` simultaneous `generate_aspirant_dossier_pdf()` calls under enforced `1,800 MB` limit | `6.47s` (1), `10.42s` (3), `14.71s` (5) | Contained in cgroup | Peak cgroup RSS (`memory.peak`): **`348.4 MiB` (1)**, **`545.7 MiB` (3)**, **`563.3 MiB` (5)** (`32.0%` of enforced `1,800 MB` limit); `0` OOM kills | **PASS** |
| **11** | **Invalid / Oversized Upload** | Passed `6.5 MB` invalid `.exe` byte stream to `validate_and_process_photo()` | `< 5 ms` in-memory rejection | None | Rejected prior to network/storage call (`processed=None`, error message returned) | **PASS** |
| **12** | **Burst Query / Rate-Limit Resilience** | 30 parallel profile queries across 15 worker threads inside `fulcrum-app` | `100%` completion | None | `BURST_OK=30/30`; zero connection pool exhaustion or dropped sockets | **PASS** |

---

## 2. Deep-Dive Proofs on Previously Questioned Scenarios

### A. Scenario 7 Proof — Already-Open Browser Loses Access Upon Mid-Session Role Revocation
1. **Setup:** A headless Playwright Chromium browser logged in as `synth_guide_*@test.local` and opened the Guide Workspace (`👥 My Aspirants`). DOM inspection confirmed:
   - `Guide Badge Visible`: **`True`** (`Role: Verified Guide`)
   - `Assigned Mentee Visible`: **`True`** (`SYNTH_TEST Aspirant Alpha` in caseload dropdown)
2. **Fault Injection:** While that Playwright browser tab remained open, `revoke_role(guide_id, "guide", reason="Chaos 7 Live Browser Eviction", revoked_by=ADMIN_ID)` was executed:
   - Updated `public.user_roles` status to `revoked`.
   - Automatically unassigned the Guide's active caseload in `public.relationships`.
   - Triggered cross-session `_INVALIDATION_TIMESTAMPS` in [`services/cache.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/cache.py) and hit the active-role guard in [`app.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/app.py#L903-L938) and [`views/guide.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/guide.py#L64-L68).
3. **Browser Verification:** On the very next click inside the still-open browser (`1,267.3 ms` rerun):
   - `Guide Badge Visible`: **`False`**
   - `Mentee Selector Visible`: **`False`** (`Select Entrepreneur to Advise` completely gone from DOM)
   - `Evicted to Aspirant / Blocked`: **`True`**

### B. Scenario 10 Proof — Real Concurrent PDF Exports Under the Enforced `1,800 MB` Limit
- Instead of estimating RAM or assuming a `3 GB` limit, we ran `1`, `3`, and `5` simultaneous executions of [`generate_aspirant_dossier_pdf()`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/pdf_generator.py#L793) inside `fulcrum-app` with its **actual enforced `1,800 MB` (`1,757.8 MiB`) cgroup v2 limit**:
  - **`1` PDF:** `6,468.0 ms` | Pre: `78.7 MiB` $\rightarrow$ Peak (`memory.peak`): **`348.4 MiB`** $\rightarrow$ Post: `148.5 MiB` | Output: `[360,427]` bytes.
  - **`3` PDFs:** `10,421.1 ms` | Pre: `79.9 MiB` $\rightarrow$ Peak (`memory.peak`): **`545.7 MiB`** $\rightarrow$ Post: `156.6 MiB` | Output: `[363,295, 360,770, 361,019]` bytes.
  - **`5` PDFs:** `14,714.0 ms` | Pre: `80.2 MiB` $\rightarrow$ Peak (`memory.peak`): **`563.3 MiB`** $\rightarrow$ Post: `165.3 MiB` | Output: `[237,918, 361,835, 361,163, 363,155, 361,343]` bytes.
- Because `BoundedSemaphore(2)` in `services/pdf_generator.py` caps concurrent Chromium subprocesses at `2` and falls back to ReportLab when saturated, container memory **never exceeded `563.3 MiB` (`32.0%` of the enforced `1,800 MB` limit)**.
