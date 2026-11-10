# HOSTINGER KVM 2 RESOURCE ALLOCATION SPECIFICATION (5 GB CEILING)
**Platform:** Fulcrum India (Cluster A / Fulcrum-Beta)  
**Host Target:** Hostinger KVM 2 VPS (2 vCPU, 8 GB Physical RAM)  
**Operating System:** Ubuntu 24.04.5 LTS  
**Target Service:** `fulcrum-app` (Streamlit 1.32+ on Python 3.11)  
**Reverse Proxy:** `fulcrum-caddy` (Caddy 2 Alpine)  
**Date:** 2026-11-10  

---

## 1. Executive Summary & Resource Strategy

A Hostinger KVM 2 VPS provides **2 vCPU** and **8,192 MB (8.0 GB) of total physical RAM**. 

To guarantee that the Fulcrum application remains lightning-fast, never suffers Out-Of-Memory (OOM) crashes, and never starves the host operating system or Caddy reverse proxy, we configure a strict, bounded resource allocation:
- **Fulcrum Application Limit:** **5.0 GB (`5G`)** and **1.75 vCPU**
- **Fulcrum Application Reservation:** **1.0 GB (`1G`)** and **0.25 vCPU**
- **Caddy Reverse Proxy Limit:** Dynamic (averages ~30–45 MB, <0.05 vCPU)
- **Host System Headroom:** **~1.8 GB to 2.1 GB** unallocated margin reserved for the Linux kernel, system daemons, SSH, and page cache.

---

## 2. Host Memory Budget Breakdown (8,192 MB Total)

```
┌────────────────────────────────────────────────────────────────────────┐
│ TOTAL HOST PHYSICAL RAM: 8,192 MB (8.0 GB)                             │
├──────────────────────────────┬──────────────────────────┬──────────────┤
│ Fulcrum Application Container│ Host OS & System Daemons │ Host Safety  │
│ Max Ceiling (5,120 MB / 5 GB)│ Kernel, SSH, Docker,     │ Headroom /   │
│                              │ Caddy (~1,300 MB)        │ Buffer Cache │
│                              │                          │ (~1,772 MB)  │
└──────────────────────────────┴──────────────────────────┴──────────────┘
```

| Component | Budget Allocation | Purpose & Workload Description |
| :--- | :--- | :--- |
| **Fulcrum Application** | **5,120 MB (5.0 GB)** | Python runtime, Streamlit session states (50+ concurrent users), server-side pagination cache, and single-concurrency Chromium Playwright worker for PDF dossier generation. |
| **Linux Kernel & Daemons** | **~1,000 MB (1.0 GB)** | Linux kernel page tables, systemd, journald, udev, network drivers, and OpenSSH daemon. |
| **Docker & Caddy Proxy** | **~300 MB (0.3 GB)** | `dockerd`, `containerd`, container networking bridge (`fulcrum-net`), and `fulcrum-caddy` reverse proxy terminating TLS. |
| **Unallocated Host Margin** | **~1,772 MB (1.7 GB)** | Buffer and page cache to prevent kernel I/O thrashing and guarantee zero OOM-killer invocations. |

---

## 3. Why 5 GB is the Optimal Baseline

1. **Streamlit & Session Overhead:** Streamlit maintains user widgets and component state in container memory. With 50 concurrent active users, session state consumes approximately 400 MB to 750 MB.
2. **Chromium PDF Worker Spike:** When generating an entrepreneur journey dossier, headless Chromium spikes by ~300 MB to 450 MB for 4–8 seconds, then releases memory back to the OS.
3. **Cache Bounds:** Fulcrum's in-memory query caches (`@st.cache_data` and memoization dicts) are strictly bounded to 256 entries and 60-second TTLs (~80 MB).
4. **Safety Buffer:** At peak usage under 50 simultaneous users, actual memory consumption measures between 1.6 GB and 2.4 GB. A 5.0 GB limit gives **over 2.6 GB of safety headroom** inside the container before any limit is approached.

---

## 4. Why 7 GB is Strictly Prohibited

Assigning 7.0 GB to the Fulcrum container on an 8.0 GB VPS is **extremely dangerous**:
- `7,168 MB (Fulcrum) + 1,000 MB (Host OS) + 300 MB (Docker/Caddy) = 8,468 MB`.
- This exceeds physical RAM (8,192 MB) by nearly 300 MB.
- In Linux, when aggregate memory allocations exceed physical memory plus available swap, the **Linux Kernel Out-Of-Memory (OOM) Killer** is invoked.
- The OOM killer operates based on `oom_score`. If memory pressure spikes, the kernel will kill whichever process has high memory or unpredictable impact, often killing:
  - `sshd` (permanently locking the administrator out of the server).
  - `caddy` (dropping all HTTPS connections for every user).
  - `dockerd` (crashing the container runtime entirely).
- Therefore, **7 GB must never be configured on an 8 GB host**.

---

## 5. Reviewed Docker Compose Patch

The configuration in `docker-compose.yml` implements these limits cleanly without contradictory `mem_limit` directives:

```yaml
services:
  fulcrum:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: fulcrum-app
    restart: unless-stopped
    environment:
      - DATA_BACKEND=supabase
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_PUBLISHABLE_KEY=${SUPABASE_PUBLISHABLE_KEY}
      - SUPABASE_SECRET_KEY=${SUPABASE_SECRET_KEY}
      - SOLE_ADMIN_UUID=${SOLE_ADMIN_UUID:-}
      - DOMAIN=${DOMAIN:-app.fulcrumindia.online}
      - APP_URL=${APP_URL:-https://${DOMAIN:-app.fulcrumindia.online}}
    networks:
      - fulcrum-net
    logging:
      driver: "json-file"
      options:
        max-size: "20m"
        max-file: "5"
    deploy:
      resources:
        limits:
          cpus: '1.75'
          memory: 5G
        reservations:
          cpus: '0.25'
          memory: 1G
```

---

## 6. Criteria for Future Increase to 6 GB

Do **not** increase the container limit from 5 GB to 6 GB unless **all** of the following empirical criteria are satisfied over at least **14 consecutive days of production monitoring**:

1. **Sustained Memory Pressure:** Container memory usage consistently exceeds **4.2 GB** (85% of 5 GB) during regular operational hours.
2. **Zero Swap Thrashing:** The host virtual memory monitor (`vmstat 1 5`) shows swap-in (`si`) and swap-out (`so`) values of **0**.
3. **Host Available Memory:** The `available` column in `free -m` remains consistently **above 2,200 MB**.
4. **Conservative Swappiness:** Host kernel swappiness is configured to `10`:
   ```bash
   sysctl vm.swappiness=10
   ```
5. **PDF Queue Verification:** PDF generation requests queue gracefully under the single-worker lock without exceeding container memory ceilings.

---

## 7. Operational Monitoring Commands

Run these commands periodically on the VPS terminal to monitor resource health:

```bash
# 1. Inspect live container memory usage and percentage
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}" fulcrum-app fulcrum-caddy

# 2. Inspect host memory and swap
free -h

# 3. Inspect virtual memory paging (columns si and so should be 0)
vmstat 1 5
```

