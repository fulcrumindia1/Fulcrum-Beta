# 09 — CAPACITY AND BREAKING POINT REPORT
**Phase F Deliverable | Target: Hostinger KVM 2 (2 vCPU, 7.8 GiB RAM)**

---

## 1. Verified Sustainable User Capacity

Based on empirical testing across **7 Concurrency Tiers (`5` to `100` simultaneous active users)** and **5 Registered User Scale Tiers (`100` to `10,000` registered users)**:

| Capacity Dimension | Highest Verified Sustainable Level | Primary Limiting Factor | Performance / SLA Status |
| :--- | :---: | :--- | :---: |
| **Simultaneously Active Users (Sub-Second)** | **`50 Concurrent Users`** | Python Global Interpreter Lock (GIL) / CPU core concurrency | **PASS** (p50: `107.4 ms`, p95: `1,270.8 ms`, Error: `0.0%`) |
| **Simultaneously Active Users (Acceptable SLA)** | **`75 Concurrent Users`** | Streamlit Tornado event loop queuing | **PASS** (p50: `209.5 ms`, p95: `1,848.9 ms`, Error: `0.0%`) |
| **Maximum Tolerable Traffic Peak** | **`100 Concurrent Users`** | Request queuing increases p50 to `1.5s` | **TOLERABLE** (p50: `1,506 ms`, p95: `2,392 ms`, Error: `0.0%`) |
| **Registered User Accounts in Database** | **`10,000 Registered Users`** | Unpaginated memory footprint (~18 MB in-memory roster) | **PASS** (Total query workload: `591.5 ms`, DB size: `14.3 MB`) |

---

## 2. Breaking Point Analysis: Where Does Performance Break Down?

### A. The Breaking Point Threshold: `> 75 Concurrent Users`
- At **`10 to 50 concurrent users`**, Fulcrum operates comfortably in sub-second territory (`p50 < 110 ms`, `p95 < 1.3s`).
- At **`75 concurrent users`**, CPU utilization reaches `~50%` of container allocation, and p95 rises to `1.85s`.
- At **`100 concurrent users`**, zero requests fail (`100.0%` success rate, `0` HTTP 5xx errors), but median latency increases to **`1.50s`** and p99 reaches **`2.95s`**.
- **Root Cause of Latency Degradation:** The limitation is **NOT memory** (the container used only `130.5 MiB` out of its `1,800 MiB` allocation, `7.25%` memory utilization). The constraint is **CPU core saturation** on `2 vCPUs` when hundreds of WebSocket messages and Python bytecode executions compete for Tornado's single thread.

### B. Registered Database Scale Breaking Point: `> 5,000 Users` without Pagination
- When registered profiles reach `10,000`, the database index lookup is still fast (`< 600 ms` for a full multi-role join).
- However, downloading 10,000 profiles over PostgREST into a single unpaginated Python list consumes **`18.1 MB` of RAM per directory render**.
- While KVM 2 easily handles this in memory, implementing server-side SQL pagination (`LIMIT 50 OFFSET X`) is recommended before the platform crosses 2,000 active entrepreneurs to keep payload sizes under 100 KB.

---

## 3. Hostinger KVM 2 vs. KVM 4 Evaluation

### Is Hostinger KVM 2 (2 vCPU, 8 GB RAM) Sufficient?
**YES, fully sufficient for Fulcrum's current and medium-term operational needs.**
- **Memory:** Total host RAM is `8.0 GB`. Fulcrum's active baseline is only `~68–130 MiB`, with `6.7 GB` of free RAM remaining. Even with co-hosted applications (`pairdo-staging` at `~414 MiB`), the system has over `80%` free memory headroom.
- **Concurrency:** KVM 2 comfortably sustains **`50 to 75 simultaneously active entrepreneurs and mentors`** with sub-2-second response times.
- Since real-world community platforms typically have a 1:10 or 1:20 concurrency ratio (e.g., 50 simultaneous users corresponds to an active daily community of **500 to 1,000 entrepreneurs**), KVM 2 can easily support **1,000+ registered platform users**.

### Would Hostinger KVM 4 (4 vCPU, 16 GB RAM) Provide Meaningful Benefits?
- **When KVM 4 is beneficial:** If concurrent active users consistently exceed **75–100 simultaneous sessions**, the 4 vCPUs will double Tornado's compute throughput, keeping p95 latency under 1 second even during high-concurrency webinars or demo days.
- **Verdict:** An immediate upgrade to KVM 4 is **NOT required** for Phase 0 or Phase 1. KVM 2 is the ideal cost-performance tier today.
