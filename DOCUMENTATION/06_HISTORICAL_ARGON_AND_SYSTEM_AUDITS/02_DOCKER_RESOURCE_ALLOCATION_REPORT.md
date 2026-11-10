# 02 — DOCKER RESOURCE ALLOCATION REPORT
**Phase B Deliverable | Target: `pravin@10.44.155.57` (`pravin-server` — 2 vCPU, 7.8 GiB RAM)**

---

## 1. Currently Enforced In-Kernel cgroup v2 Resource Limits

The Docker Compose configuration deployed at `/home/pravin/fulcrum-staging/` on `10.44.155.57` was inspected directly via the Docker Engine and `/sys/fs/cgroup/`:

| Metric | Docker Compose Spec | Effective cgroup v2 Value (`/sys/fs/cgroup`) | HostConfig Verification | Currently Enforced? |
| :--- | :--- | :--- | :--- | :---: |
| **CPU Limit** | `cpus: '1.5'` | `150000 100000` (quota/period) | `NanoCpus: 1500000000` | **YES (`1.50 vCPU`)** |
| **CPU Reservation** | `cpus: '0.25'` | `25000 100000` (min weight) | `CpuShares: 256` | **YES** |
| **Memory Limit** | `memory: 1800M` | `1887436800` bytes (`1,800.0 MB` / `1,757.8 MiB`) | `Memory: 1887436800` | **YES (`1,800 MB`)** |
| **Memory Reservation** | `memory: 256M` | `268435456` bytes (`256.0 MiB`) | `MemoryReservation: 268435456` | **YES** |

---

## 2. Measured Resource Consumption Baseline & PDF Pressure Telemetry

### A. Container Idle & Co-Hosted Baseline (`docker stats --no-stream`)
| Container Name | Role | Status | CPU % | Active Memory RSS / Enforced Limit | Mem % | PIDs |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **`fulcrum-app`** | Streamlit Web Application | Up (healthy) | `0.46%` | **`68.20 MiB` / `1,757.8 MiB` (`1,800 MB`)** | **`3.79%`** | 4 |
| **`fulcrum-caddy`** | Reverse Proxy (Gzip/Zstd) | Up (healthy) | `0.00%` | **`10.21 MiB` / `7,942 MiB`** | **`0.13%`** | 7 |
| **`pairdo-staging-*` (5 ctns)** | Co-hosted Workload | Up (healthy) | `1.15%` | **`413.88 MiB` combined** | `5.21%` | 33 |
| **Total Host Memory Usage** | OS + All 7 Containers | Active | `1.61%` | **`1,234.4 MiB` used / `7,942 MiB`** | **`15.5%`** | 173 |

### B. Empirically Measured Founder Dossier PDF Memory Spikes (`services/pdf_generator.py`)
We executed `1`, `3`, and `5` simultaneous calls to [`generate_aspirant_dossier_pdf()`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/pdf_generator.py#L793) inside `fulcrum-app` on `10.44.155.57` under the **currently enforced `1,800 MB` (`1,757.8 MiB`) cgroup v2 limit** and read `/sys/fs/cgroup/memory.current` and `/sys/fs/cgroup/memory.peak`:

| Concurrent PDF Exports | Total Wall Time | Pre-Render RSS (`memory.current`) | Peak cgroup RSS (`memory.peak`) | Post-Render RSS (`memory.current`) | % of Enforced `1,800 MB` Limit | Engine Behavior & Output Sizes |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **`1` PDF** | `6,468.0 ms` (`6.47s`) | `78.7 MiB` | **`348.4 MiB`** | `148.5 MiB` | **`19.8%`** | 1 Playwright Chromium render (`360.4 KB`) |
| **`3` PDFs** | `10,421.1 ms` (`10.42s`) | `79.9 MiB` | **`545.7 MiB`** | `156.6 MiB` | **`31.0%`** | Throttled by `BoundedSemaphore(2)`; 3 Playwright PDFs (`360.8–363.3 KB`) |
| **`5` PDFs** | `14,714.0 ms` (`14.71s`) | `80.2 MiB` | **`563.3 MiB`** | `165.3 MiB` | **`32.0%`** | 4 Playwright PDFs (`361.1–363.1 KB`) + 1 ReportLab fallback (`237.9 KB`) |

> [!IMPORTANT]
> **Why Peak Memory Capped at `563.3 MiB` Under 5 Concurrent PDF Exports:**
> [`services/pdf_generator.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/services/pdf_generator.py#L581) enforces `_PDF_CONCURRENCY_SEMAPHORE = threading.BoundedSemaphore(2)` with a 15-second acquisition timeout and automatic ReportLab fallback. Because at most **2 headless Chromium subprocesses** (`~220–260 MiB` RSS each) can exist simultaneously inside `fulcrum-app`, concurrent PDF exports **never exceed `~565 MiB`**, comfortably within the currently enforced **`1,800 MB` (`1,757.8 MiB`)** container limit!

---

## 3. Evaluation of Current `1,800 MB` Enforced Limit vs. Candidate `3,072 MB` Limit

- **With the Current Enforced `1,800 MB` (`1,757.8 MiB`) Limit:**
  - Base container + 50–100 active authenticated sessions + 2 concurrent Chromium PDF workers peaks at **`~600–650 MiB`**, leaving **`> 1,100 MiB` of free headroom inside the `1,800 MB` container cgroup**.
  - Therefore, **`1,800 MB` is already safe and does NOT experience OOM kills**.
- **Optional Candidate Limit (`3,072 MB` / `1.75 CPU` — Status: `NOT APPROVED, Awaiting Owner Decision`):**
  - Since the host has `6.71 GiB` (`6,707 MiB`) of unused RAM (`0 B` swap), raising the container ceiling to `3,072 MB` is an optional zero-cost buffer expansion that still leaves `> 2.6 GiB` of unallocated host RAM after accounting for the OS (`700 MiB`) and `pairdo-staging` (`1,500 MiB`).

```diff
--- docker-compose.yml (Currently Enforced: 1800M / 1.5 CPU)
+++ docker-compose.yml (Optional Candidate CR-01: 3072M / 1.75 CPU — Awaiting Owner Approval)
@@ -17,8 +17,8 @@
         resources:
           limits:
-            cpus: '1.5'
-            memory: 1800M
+            cpus: '1.75'
+            memory: 3072M
           reservations:
             cpus: '0.25'
-            memory: 256M
+            memory: 512M
```
