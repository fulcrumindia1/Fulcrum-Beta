# Production Browser Exception, Schema Error & Health Audit

**Target Environment:** `https://app.fulcrumindia.online/` (`187.126.114.81`)  
**Deployed App Revision:** `988127b` (`sha256:6c212f0dc623b7d783534f71767dd950b063f522b9d0c982b4950a400c2627d1`)  
**Evidence Files:** `transcript.jsonl:228,254`, `scratch/preflight_admin/baseline_report.json`, `scratch/run_08_batch_d/d2_report.json`

---

## 1. Browser Console & Uncaught Page Exceptions

| Stage | Playwright Listener Scope | `console.error` Count | `pageerror` Count | Observed Findings |
|---|---|---:|---:|---|
| **Preflight Upgrade (`988127b`)** | Initial public render | `0` | `0` | HTTP `200`, `dom_ms=3491.2`, `ready_ms=5560.6`. |
| **13-Tab Admin Baseline** | All `13` Admin tabs & subtabs | `0` | `0` | `tab_count = 13`, zero Python tracebacks in DOM (`baseline_report.json`). |
| **Final Audit (`Batch D2`)** | Admin Portal + Lifecycle + Public health checks | `0` | `0` | Clean browser execution (`console_errors = []`, `page_errors = []`). |

---

## 2. Container Runtime, Pre-Test History & Live Endpoint Health

- **Resolved Historical Crash (Verified During Preflight Prior to `988127b` Upgrade):**
  - Pre-upgrade container (`a7fd571`, image `sha256:e7eb6613...`) logged `UnboundLocalError: cannot access local variable 'active_allocations' where it is not associated with a value` at `views/admin.py:892` (`transcript.jsonl:228`).
  - Upgrading live VPS to **`988127b`** (`sha256:6c212f0dc623b7d783534f71767dd950b063f522b9d0c982b4950a400c2627d1`) resolved `active_allocations` cleanly: `0` occurrences across the entire 32-user Tab 4 campaign (`44+` assignments, empty rosters, & unassignments).
- **VPS Resource Telemetry Observed After `988127b` Deploy (`transcript.jsonl:254`):**
  - `fulcrum-app`: `healthy`, `0.25%` CPU, `62.57 MiB / 5 GiB` RAM.
  - `fulcrum-caddy`: running untouched (`StartedAt=2026-10-16T22:16:39Z`), `0.11%` CPU, `56.57 MiB` RAM.
  - Note: Interactive VPS SSH `docker logs fulcrum-app` was executed during Preflight/Deploy (`task-226`, `task-247`); post-Batch-D2 server container log inspection was not re-run via SSH as no SSH credential was stored after upgrade; live health & error monitoring post-campaign used HTTPS health checks + Supabase REST read-back + Playwright browser DOM/console listeners.
- **Final Public Endpoint Health Checks (`d2_report.json`):**
  - `GET https://app.fulcrumindia.online/healthz` -> **HTTP `200`, body `"ok"`**.
  - `GET https://app.fulcrumindia.online/_stcore/health` -> **HTTP `200`, body `"ok"`**.

---

## 3. Production Application Errors Triggered by Real Workflows (Handled vs Broken)

1. **`PGRST204` Schema Errors in `services/account_lifecycle.py` (`DEF-32-001`):**
   - `Pause Account`: `Could not find the 'lifecycle_reason' column of 'profiles' in the schema cache`
   - `Archive Account`: `Could not find the 'lifecycle_reason' column of 'profiles' in the schema cache` (+ prior unassignment side effect on `Q`!)
   - `Apply Legal Hold`: `Could not find the 'lifecycle_reason' column of 'profiles' in the schema cache`
   - `Schedule Closure (30d)`: `Could not find the 'deletion_requested_by' column of 'profiles' in the schema cache`
   - Rendered clean UI `st.error` banners (no Streamlit app crash), but **100% of Tab 13 write operations fail in Supabase**.
2. **`PGRST` / Role Authorization Alerts in Consultations (`DEF-32-002`):**
   - Rendered clean `st.error` `"Unauthorized: Only assigned Guides or Admins may respond to this consultation."` (no unhandled exception), blocking legitimate hybrid replies.
3. **Resend & Public Email Confirmation Behavior (`Batch A1`):**
   - All 26 public Aspirant signups rendered clean confirmation banner (`signup_aspirant`), while QA confirmed synthetic mailboxes (`fulcrumindia1+qa32_*`) directly via Admin API to avoid Resend bounce/rate exhaustion (unconfirmed login attempt on `F` properly rejected cleanly before confirmation).

