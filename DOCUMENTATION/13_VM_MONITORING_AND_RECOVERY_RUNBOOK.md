# 13 — VM MONITORING AND RECOVERY RUNBOOK
**Phase J & L Deliverable | Hostinger KVM 2 / Staging VM (`10.44.155.57`)**

---

## 1. Quick Emergency Service Commands

> [!WARNING]
> **Co-Hosted & Secret Safety Rules:**
> 1. The VM runs co-hosted services (`pairdo-staging-*`). Never run `docker stop $(docker ps -q)` or `docker system prune --volumes`. Always target `fulcrum-app` and `fulcrum-caddy` explicitly.
> 2. Never run `cat .env` or `docker inspect` commands that print secret environment variables to terminal logs. Use key-name-only checks as shown below.

### Safe Container Status Check
```bash
docker ps --filter "name=fulcrum"
docker stats fulcrum-app fulcrum-caddy --no-stream
```

### Safe Graceful Restart
```bash
cd /home/pravin/fulcrum-staging
docker compose restart fulcrum
docker compose restart caddy
```

### Emergency Rebuild & Redeploy
```bash
cd /home/pravin/fulcrum-staging
docker compose up -d --build
```

---

## 2. Health Monitoring & Triage Checkpoints

| Checkpoint | Command | Healthy Indicator | Alert Condition |
| :--- | :--- | :--- | :--- |
| **Streamlit Health Endpoint** | `curl -fsS http://localhost:8501/_stcore/health` | `ok` (HTTP 200) | HTTP 5xx or Connection Refused |
| **Reverse Proxy Health** | `curl -fsS http://localhost:8081/_stcore/health` | `ok` (HTTP 200) | Caddy Bad Gateway (502) |
| **Container Memory Usage** | `docker stats fulcrum-app --no-stream` | `< 1,200 MiB` (`< 65%` of `1,800 MB` limit) | `> 1,500 MiB` (`> 85%` of `1,800 MB` limit) |
| **Container Peak Memory (cgroup v2)** | `docker exec fulcrum-app cat /sys/fs/cgroup/memory.peak` | `< 1,500,000,000` bytes | Approaching `1,887,436,800` bytes |
| **Host System Memory** | `free -h` | `> 3.0 GiB` available | Available `< 1.0 GiB` |
| **Host Swap Activity** | `swapon --show` | `0 B` used | Active swap thrashing (`> 500 MB`) |
| **Disk Capacity** | `df -hT /` | `> 15 GB` available | Available `< 5 GB` |
| **Container Restarts** | `docker inspect fulcrum-app --format '{{.RestartCount}}'` | `0` restarts | Count incrementing |

---

## 3. Log Triage Runbook

### Inspecting Live Application Logs
```bash
# View last 100 lines of Streamlit logs
docker logs --tail 100 fulcrum-app

# Follow Streamlit logs in real time
docker logs -f fulcrum-app

# Inspect Caddy access and error logs
docker logs --tail 50 fulcrum-caddy
```

---

## 4. Disaster Recovery & Rollback Procedure

1. **If Container Crashes / Fails to Start:**
   - Check container logs: `docker logs --tail 100 fulcrum-app`
   - Verify `.env` file permissions and required key names **without printing secret values**:
     ```bash
     ls -la /home/pravin/fulcrum-staging/.env
     grep -E '^[A-Z0-9_]+=' /home/pravin/fulcrum-staging/.env | cut -d= -f1
     ```
     *(Confirm `DATA_BACKEND`, `SUPABASE_URL`, `SUPABASE_PUBLISHABLE_KEY`, and `SUPABASE_SECRET_KEY` key names are listed).*
   - Test Supabase network reachability from host:
     ```bash
     curl -I https://bhaqaawsufwtjeqfifbv.supabase.co/rest/v1/
     ```
2. **If Host or Container Runs Low on Memory:**
   - Check per-container resource usage: `docker stats --no-stream`
   - Check top host processes by memory: `ps aux --sort=-%mem | head -n 15`
   - Restart `fulcrum-app` cleanly to release any orphaned Chromium/Playwright worker processes:
     ```bash
     cd /home/pravin/fulcrum-staging && docker compose restart fulcrum
     ```
3. **If Database Connectivity Drops:**
   - Check Supabase status at `https://status.supabase.com`.
   - Fulcrum fails closed (`DATA_BACKEND=supabase`) and displays an error notice without writing to local SQLite. Once Supabase connectivity is restored, active sessions resume automatically.
