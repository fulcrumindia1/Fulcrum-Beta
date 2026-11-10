# 15 — OWNER APPROVAL REGISTER & ANSWERS TO THE 20 FINAL OWNER QUESTIONS
**Deliverable 15 of 15 | Mode: Comprehensive Forensic Assessment & Final Owner Report**

---

## PART 1 — DIRECT ANSWERS TO THE 20 FINAL OWNER QUESTIONS

### 1. Is the VM healthy?
**YES, exceptionally healthy.**
- **CPU Load:** `0.07` (1m), `0.26` (5m), `0.32` (15m) on a `2.0` capacity scale (`< 16%` baseline utilization).
- **Memory:** `1.2 GiB` used out of `7.8 GiB` (`6.7 GiB` available).
- **Swap:** `4.0 GiB` allocated, **`0 B` used (`0%`)**.
- **Disk:** `57 GB` root NVMe volume, `31 GB` free (`45%` used), inode utilization `15%`.
- **System Stability:** Linux `6.8.0-146-generic`, zero kernel panics, zero OOM kills (`OOMKilled=false` across all containers).

### 2. Is it correctly sized for Fulcrum?
**YES.** The measured hardware (`2 vCPUs`, `7.8 GiB RAM`) matches Hostinger KVM 2. The active `fulcrum-app` container consumes **`68.2 MiB` idle**, **`115.0–288.5 MiB` across `5–50` concurrent authenticated sessions**, and **`563.3 MiB` peak during 5 simultaneous Chromium PDF exports**, leaving over `75%` free host RAM headroom.

### 3. How much RAM and CPU are actually available?
- **Available RAM:** **`6.7 GiB` (`6,850+ MiB`) available** without touching swap.
- **Available CPU:** **`2 dedicated vCPUs`** (`Intel Core i3-3240 @ 3.40GHz`, 2 physical cores, 1 thread/core), idling at `~96%` idle capacity when no load test is running.

### 4. How much Docker memory can safely be assigned?
**`3,072 MB` (`3.0 GiB`)** is the recommended safe candidate ceiling (currently enforced: **`1,800 MB` / `1,757.8 MiB`**).
- **Current Enforced Limit Verification:** Under the currently enforced `1,800 MB` limit, 5 simultaneous Chromium PDF exports peaked at `563.3 MiB` (`32.0%` of limit) and 100 concurrent WebSocket sessions peaked at `402.6 MiB` (`22.37%` of limit).
- **Why `3,072 MB` is Safe:** Assigning `3,072 MB` to `fulcrum-app` leaves `4.87 GiB` on the host. Subtracting the OS reserve (`700 MiB`) and co-hosted `pairdo-staging` (`~415 MiB` active / `1,500 MiB` budget), the host maintains **`> 2.6 GiB` of unallocated buffer**.

### 5. What is the measured VM-to-Supabase latency?
Direct empirical measurement from inside `fulcrum-app` on `10.44.155.57` over **360 verified samples (`100%` HTTP `200`/`201`, `0` errors)** in [`03_SUPABASE_NETWORK_AND_DATABASE_LATENCY.csv`](file:///C:/Users/hp/.gemini/antigravity/brain/22e605d7-a862-4d23-bd2d-9491575ffa3a/03_SUPABASE_NETWORK_AND_DATABASE_LATENCY.csv):
- **DNS Resolution:** **`1.5 ms`** p50 (`2.4 ms` p95)
- **TCP Handshake:** **`46.0 ms`** p50 (`90.6 ms` p95) — physical geographic network floor
- **TLS 1.3 Handshake:** **`62.8 ms`** p50 (`170.3 ms` p95)
- **Cold HTTPS Request (New Connection):** **`219.9 ms`** p50 (`336.4 ms` p95)
- **Warm HTTPS Keep-Alive Request:** **`94.5 ms`** p50 (`168.4 ms` p95)
- **Single Profile Read (`public.profiles`, `1` row):** **`95.5 ms`** p50 (`191.5 ms` p95)
- **Full Scheme Catalogue Read (`public.schemes`, `179` rows):** **`146.5 ms`** p50 (`295.3 ms` p95)
- **Relationships (`17` rows) / Help Requests (`6` rows) / Journeys (`25` rows):** **`98.3 ms` / `96.6 ms` / `91.4 ms`** p50
- **Authorized Write (`INSERT public.notifications`, HTTP `201`):** **`98.0 ms`** p50 (`167.3 ms` p95)
- **Authorized Cleanup (`DELETE public.notifications`, HTTP `200`):** **`96.0 ms`** p50 (`192.6 ms` p95)

### 6. Why exactly is tab switching slow?
Tab switching was historically slow due to **two compounding architectural bottlenecks**:
1. **Eager Execution of Hidden `st.tabs()` Containers:** Streamlit executed every hidden tab's Python code and database queries on every rerun.
2. **N+1 Sequential PostgREST Queries Across the `46.0 ms` Network Floor:** [`list_users_with_multi_roles()`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/roles.py#L366) previously executed `190` sequential HTTP requests (`21,565.7 ms`), and [`list_active_profiles_for_role()`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/profiles.py#L140) executed `196` sequential HTTP requests (`18,324.1 ms`).
- **After Remediation (`DEC-01`):** Every tab across Admin (`12` tabs), Aspirant (`6` tabs), Guide (`3` tabs), and SME (`3` tabs) now switches in **`368 ms – 524 ms` warm** (`375 ms – 2,051 ms` cold) in real Chromium browser tests.

### 7. Which queries are repeated unnecessarily?
- Per-user `get_active_roles(uid)` calls inside directory listing loops (`190` sequential calls replaced by 1 bulk query).
- Repeated lookups of the single Admin UUID (`get_primary_admin_id()`).
- Repeated unmemoized reads of the 179-row `public.schemes` catalogue (`146.5 ms` per uncached read).

### 8. How fast are normal database reads and writes?
- **Single-Row / Filtered Table Reads:** **`91.4 – 98.3 ms`** median round-trip (`~46 ms` network transport + `~48 ms` PostgREST/PostgreSQL execution).
- **179-Row Scheme Catalogue Read (`public.schemes`):** **`146.5 ms`** median round-trip.
- **Authorized Write (`HTTP 201`) & Cleanup (`HTTP 200`):** **`98.0 ms`** write p50 and **`96.0 ms`** delete p50 (`0%` error rate).

### 9. How many registered users were simulated?
**`10,000 Registered Users`** were generated and benchmarked across 5 scale tiers (`100`, `500`, `1,000`, `5,000`, and `10,000` users) in an isolated benchmark database.
- Total multi-role join and directory query workload at `10,000` registered users was **`591.5 ms`** (`14.3 MB` database size, `18.1 MB` unpaginated Python memory delta).

### 10. How many genuinely concurrent authenticated browser/WebSocket users were tested?
- **Real Playwright Chromium Browser Sessions:** Tested across all 4 roles (**Admin, Aspirant, Guide, SME**) plus a **5-role simultaneous multi-browser stress test** (`2` Aspirants + `1` Guide + `1` SME + `1` Admin).
- **Real Authenticated Streamlit WebSocket (`/_stcore/stream` Protobuf) Concurrency Matrix:** Tested across **7 concurrency tiers (`5, 10, 20, 30, 50, 75, and 100` simultaneously active authenticated sessions)** executing continuous `ScriptRunner` reruns while sampling `docker stats fulcrum-app`.

### 11. What is the highest sustainable verified concurrency?
- **Sub-Second Median Interactive Capacity (`p50 < 1.0s`, `0%` errors):** **`20 Simultaneously Active Authenticated Users`** (`p50 = 925.2 ms`, `p95 = 2,205.7 ms`, `100.0%` success, `91.0%` peak CPU, `160.6 MiB` RAM).
- **Sustainable Interactive SLA Capacity (`p95 < 5.0s`, `0%` errors):** **`30 Simultaneously Active Authenticated Users`** (`p50 = 1,865.4 ms`, `p95 = 4,034.1 ms`, `100.0%` success, `105.4%` peak CPU, `215.1 MiB` RAM).
- **Maximum Zero-Error Queueing Peak (`0%` errors):** **`50 Simultaneously Active Authenticated Users`** (`p50 = 6,877.6 ms`, `p95 = 7,609.9 ms`, `100.0%` success, `109.6%` peak CPU, `288.5 MiB` RAM).
- At a typical `1:10` to `1:20` concurrency ratio, **`30–50` simultaneous active users supports a community of `300 to 1,000` registered entrepreneurs and mentors**.

### 12. What happens when that limit is exceeded?
At **`75 to 100 simultaneously active authenticated users`**, the single CPython process hits the **1-core Python Global Interpreter Lock (GIL) ceiling (`~106.9%–109.6%` CPU)**:
- Container memory remains very low (**`354.3 MiB` at 75 users, `402.6 MiB` at 100 users** — only `22.37%` of the current `1,800 MB` limit), and the container **never crashes or OOMs**.
- However, because `155+` `ScriptRunner` threads queue behind the single Python GIL lock, median rerun latency rises to **`8.50s` (75 users) and `10.48s` (100 users)**, and **`19.3%–19.8%` of concurrent reruns exceed the 25-second timeout** (`80.19%` success at 75 users; `80.72%` success at 100 users).

### 13. Which chaos scenarios passed or failed?
**All 12 Chaos Scenarios PASSED (`12/12` verified in [`08_CHAOS_ENGINEERING_REPORT.md`](file:///C:/Users/hp/.gemini/antigravity/brain/22e605d7-a862-4d23-bd2d-9491575ffa3a/08_CHAOS_ENGINEERING_REPORT.md)):**
- **Scenario 1 & 12 (Container & Caddy Restart):** `fulcrum-app` restarted in `1.86s` (`1.98s` HTTP ready); `fulcrum-caddy` restarted in `0.72s`.
- **Scenario 2 & 3 (Supabase Latency & Outage):** Verified strict **Fail-Closed** behavior (`0` silent fallback writes to local SQLite).
- **Scenario 7 (Live Open Browser Role Revocation):** Revoking a Guide's role while their Chromium browser was open on the Guide Portal evicted the user on the very next click (**`1,267.3 ms`**, `Guide Badge=False`, `Mentee Selector=False`).
- **Scenario 10 (Real Concurrent PDF Dossier Exports Under Enforced `1,800 MB` Cap):** `1, 3, and 5` simultaneous `generate_aspirant_dossier_pdf()` executions succeeded (`5/5` valid `%PDF-1.4` files) with cgroup `memory.peak` reaching **`348.4 MiB` (`1` PDF), `545.7 MiB` (`3` PDFs), and `563.3 MiB` (`5` PDFs — `32.0%` of `1,800 MB` limit)** and `OOMKilled=false`.

### 14. Did any records become duplicated, corrupted or incorrectly authorized?
**ZERO.** Across all load tiers, race-condition locks (duplicate assign, duplicate consultation request, concurrent SME claim), and 12 chaos scenarios, **zero records were duplicated, zero records were corrupted, zero authorization leaks occurred, and `0` synthetic `@test.local` records remain in Supabase**.

### 15. Would KVM 2 be sufficient after optimization?
**YES, 100% sufficient.** A single container on KVM 2 sustains `30` simultaneous active users under a `< 5s` p95 SLA (`50` simultaneous users with `0%` errors) while using `< 23%` of its memory limit. Furthermore, if traffic ever grows beyond `30–50` simultaneous active users, deploying **2 `fulcrum-app` container replicas behind Caddy on this same KVM 2 VM** unlocks the second vCPU with a second Python GIL process, doubling capacity to `60–100` active users without upgrading hardware.

### 16. Would KVM 4 provide meaningful benefits?
Only when simultaneous active users regularly exceed **`60–80` concurrent sessions across 2 container replicas** (corresponding to `1,500+` daily active users). Today, upgrading to KVM 4 is unnecessary.

### 17. Which optimization should be performed first?
**Priority P0 (`DEC-01` through `DEC-06` + Cross-Session Role Revocation Cache Invalidation):** Lazy tab evaluation, N+1 query batching, cross-session `_INVALIDATION_TIMESTAMPS` + 5s role-grant memo TTL, and bounded PDF rendering (`BoundedSemaphore(2)`). All of these are already implemented, synced, and verified on `fulcrum-staging` (`10.44.155.57:8501`).

### 18. What improvements require changes to Docker Compose?
1. **`CR-01` (Optional Headroom Increase):** Updating `/home/pravin/fulcrum-staging/docker-compose.yml` to raise `mem_limit` from `1800M` to `3072M` (`BKL-20`) and `cpus` from `1.5` to `1.75` (`BKL-21`).
2. **Future Horizontal Scale (`BKL-22`, Optional):** Running `2` `fulcrum-app` replicas behind Caddy if simultaneous active users ever exceed `30–50`.

### 19. Which proposed changes could break existing functionality?
None of the applied P0 optimizations or proposed P1/P2 backlog items break existing functionality, UI design, or business workflows. All `94` automated end-to-end and security regression tests pass (`100%`).

### 20. What exact approvals do you need from me?
1. **`CR-01` — Docker Compose Resource Ceiling Patch (`docker-compose.yml`):** Approval to change `mem_limit: 1800M` $\rightarrow$ `3072M` and `cpus: 1.5` $\rightarrow$ `1.75` on `10.44.155.57`.
2. **`CR-02` — Production Branch Promotion:** Approval to commit and merge the verified `security/phase0-containment` branch (including the lazy-tab, N+1 batching, and live role-revocation cache invalidation fixes).
3. **`CR-03` — Supabase PostgreSQL Composite Indexes (`10_DATABASE_QUERY_AND_INDEX_AUDIT.md`):** Approval to run the `CREATE INDEX CONCURRENTLY IF NOT EXISTS` statements in the Supabase SQL Editor (`BKL-01` through `BKL-05`).

---

## PART 2 — OWNER APPROVAL REGISTER (CONSISTENT WITH DELIVERABLE 14)

| ID | Backlog Ref | Proposed Change | Target | Current Status |
| :--- | :---: | :--- | :--- | :---: |
| **`CR-01`** | `BKL-20`, `BKL-21` | Update `docker-compose.yml` (`mem_limit: 3072M`, `cpus: 1.75`, `mem_reservation: 512M`) | `/home/pravin/fulcrum-staging/docker-compose.yml` | **NOT APPROVED (Awaiting Owner Decision)** |
| **`CR-02`** | `DEC-01` – `DEC-06` | Commit & merge verified `security/phase0-containment` branch to `main` | Git Repository & Staging VM | **NOT APPROVED (Awaiting Owner Decision)** |
| **`CR-03`** | `BKL-01` – `BKL-05` | Execute schema-verified `CREATE INDEX CONCURRENTLY` DDL in Supabase SQL Editor | Supabase PostgreSQL (`public` schema) | **NOT APPROVED (Awaiting Owner Decision)** |
| **`CR-04`** | `BKL-06` – `BKL-12` | Implement Phase 2 Backend Query Consolidation & Server-Side Pagination (`LIMIT 50`) | `services/*.py`, `views/admin.py` | **NOT APPROVED (Awaiting Owner Decision)** |
