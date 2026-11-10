# 09 — CAPACITY AND BREAKING POINT REPORT
**Phase F Deliverable | Target: Hostinger KVM 2 (`10.44.155.57` — 2 vCPU, 7.8 GiB RAM)**

---

## 1. Verified Sustainable User Capacity

Based on empirical testing across **7 Authenticated Streamlit WebSocket Concurrency Tiers (`5` to `100` simultaneous active users via `ws://10.44.155.57:8501/_stcore/stream`)** and **5 Registered User Scale Tiers (`100` to `10,000` registered users)**:

| Capacity Dimension | Highest Verified Sustainable Level | Primary Limiting Factor | Verified Empirical Metrics |
| :--- | :---: | :--- | :--- |
| **Simultaneously Active Users (Sub-Second p50)** | **`20 Concurrent Authenticated Users`** | Single-process Python GIL approaching 1 core (`91.0%` peak CPU) | **PASS** (`p50: 925.2 ms`, `p95: 2,205.7 ms`, Success: `100.0%`, RAM: `160.6 MiB`) |
| **Simultaneously Active Users (Interactive SLA `< 5s`)** | **`30 Concurrent Authenticated Users`** | Single-process Python GIL saturation (`105.4%` peak / `89.0%` avg CPU) | **PASS** (`p50: 1,865.4 ms`, `p95: 4,034.1 ms`, Success: `100.0%`, RAM: `215.1 MiB`) |
| **Maximum Zero-Error Queueing Peak** | **`50 Concurrent Authenticated Users`** | `ScriptRunner` thread queueing behind 1-core GIL (`109.6%` peak CPU) | **TOLERABLE PEAK** (`p50: 6,877.6 ms`, `p95: 7,609.9 ms`, Success: `100.0%`, RAM: `288.5 MiB`) |
| **Single-Process Breaking Point** | **`75 – 100 Concurrent Authenticated Users`** | GIL queue wait exceeds 25s interactive rerun timeout for `~19–20%` of requests | **DEGRADED** (`75u`: `80.19%` success, `p50: 8.50s`, `354.3 MiB`; `100u`: `80.72%` success, `p50: 10.48s`, `402.6 MiB`) |
| **Registered User Accounts in Database** | **`10,000 Registered Users`** | Unpaginated directory payload size (`18.1 MB` in-memory roster) | **PASS** (Full multi-role join workload: `591.5 ms`, DB size: `14.3 MB`) |

---

## 2. Full 7-Tier Authenticated Streamlit WebSocket Load Matrix (`06_USER_LOAD_TEST_MATRIX.csv`)

Every simulated user opened a persistent Streamlit WebSocket (`/_stcore/stream`), authenticated via `login_form`, and triggered full `ScriptRunner` reruns every `1.5–2.3s` while `docker stats fulcrum-app` was sampled every `1.0s` during active load:

| Tier | Concurrent Active Sessions | Rerun Ops | Success Rate | p50 Rerun (ms) | p95 Rerun (ms) | p99 Rerun (ms) | Container CPU (`docker stats`) | Container RAM (`docker stats`) | RAM % (`1,800 MB` Cap) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Tier 1** | **`5`** | `24` | **`100.0%`** (`0` err) | `427.5` | `792.7` | `851.1` | `28.6%` (`17.8%` avg) | `115.0 MiB` | `6.39%` |
| **Tier 2** | **`10`** | `49` | **`100.0%`** (`0` err) | `596.5` | `1,215.6` | `1,339.9` | `61.3%` (`34.6%` avg) | `125.6 MiB` | `6.98%` |
| **Tier 3** | **`20`** | `88` | **`100.0%`** (`0` err) | `925.2` | `2,205.7` | `2,361.3` | `91.0%` (`61.1%` avg) | `160.6 MiB` | `8.92%` |
| **Tier 4** | **`30`** | `124` | **`100.0%`** (`0` err) | `1,865.4` | `4,034.1` | `4,054.7` | `105.4%` (`89.0%` avg) | `215.1 MiB` | `11.95%` |
| **Tier 5** | **`50`** | `99` | **`100.0%`** (`0` err) | `6,877.6` | `7,609.9` | `7,664.9` | `109.6%` (`72.9%` avg) | `288.5 MiB` | `16.03%` |
| **Tier 6** | **`75`** | `106` | **`80.19%`** (`21` err) | `8,496.2` | `9,027.0` | `9,063.6` | `108.4%` (`84.3%` avg) | `354.3 MiB` | `19.68%` |
| **Tier 7** | **`100`** | `166` | **`80.72%`** (`32` err) | `10,483.8` | `11,097.0` | `11,103.8` | `106.9%` (`87.2%` avg) | `402.6 MiB` | `22.37%` |

---

## 3. Breaking Point Forensics: Why Performance Degrades Above 30–50 Active Users

### A. Per-Session Memory Footprint (`~3.3 MiB` per Active Authenticated Session)
- **Idle Baseline:** `68.2 MiB` (`3.88%` of `1,800 MB`).
- **Active Scaling:** Container RSS grows linearly from `115.0 MiB` (`5` sessions) $\rightarrow$ `215.1 MiB` (`30` sessions) $\rightarrow$ `288.5 MiB` (`50` sessions) $\rightarrow$ `402.6 MiB` (`100` sessions).
- **When Combined with 5 Concurrent PDF Dossier Exports:** Peak memory during 5 simultaneous Chromium PDF exports (`Chaos Scenario 10`) is `563.3 MiB` (`+483 MiB` transient delta above baseline). Thus, 50 active users (`288.5 MiB`) + 5 simultaneous PDF exports (`+483 MiB`) reaches **`~771.5 MiB`** — safely inside the current `1,800 MB` limit (`43.9%`) and with >`2.2 GiB` of margin under the proposed `3,072 MB` limit.

### B. The True Bottleneck: Single-Process Python GIL Saturation (`~108%` CPU)
- Even though `fulcrum-app` is allocated `1.50 vCPUs` (proposed `1.75 vCPUs`), a single `streamlit run app.py` instance executes inside **one CPython OS process**.
- Because Python's Global Interpreter Lock (GIL) allows only **one thread to execute Python bytecode at a time**, container CPU plateaus at **`105.4% – 109.6%`** starting at **30 concurrent interacting users** (`100%` of 1 core for Python bytecode + `5–9%` on the second core for libuv/OpenSSL/socket I/O).
- At **`75–100` concurrent users**, `155+` `ScriptRunner` threads contend for that single GIL lock, causing median rerun times to reach `8.5s–10.5s` and `~19–20%` of reruns to exceed the 25-second timeout.

### C. Registered Database Scale Breaking Point (`> 5,000 Users` Without Pagination)
- At `10,000` registered users, SQL execution + bulk in-memory role join completes in **`591.5 ms`** (`14.3 MB` total SQLite/PostgREST data footprint).
- However, rendering an unpaginated directory of `10,000` profiles allocates **`18.1 MB` per admin directory render**. Adding SQL-level pagination (`LIMIT 50 OFFSET X`) is recommended before crossing `2,000` active entrepreneurs.

---

## 4. Hostinger KVM 2 vs. KVM 4 Evaluation & Horizontal Replica Unlock

### Is Hostinger KVM 2 (`2 vCPU`, `7.8 GiB RAM`) Sufficient?
**YES — 100% sufficient for Fulcrum's current and medium-term operational scale.**
1. **Single-Container Capacity (`30` SLA / `50` Peak Simultaneous Active Users):** Because typical enterprise mentoring platforms have a `1:10` to `1:20` active-to-registered concurrency ratio, `30–50` simultaneously clicking users corresponds to an active community of **`300 to 1,000 registered entrepreneurs and mentors`**.
2. **Free 2× Concurrency Unlock on Existing KVM 2 Hardware (When Needed):** Because KVM 2 has **2 vCPUs** and **`6.7 GiB` of available RAM**, if Fulcrum ever needs to support **`60 to 100` simultaneously active users** without upgrading the VPS, deploying **2 `fulcrum-app` container replicas (`1.0 vCPU`, `1,536 MB` each) behind Caddy with sticky session load balancing (`lb_policy ip_hash`)** gives 2 independent Python GIL processes across both vCPUs — doubling concurrent capacity at **\$0 additional infrastructure cost**.
3. **When to Upgrade to Hostinger KVM 4 (`4 vCPU`, `16 GB RAM`):** Only when simultaneous active concurrency regularly exceeds **`60–80` users across 2 replicas** (an active community of `1,500+` daily users).
