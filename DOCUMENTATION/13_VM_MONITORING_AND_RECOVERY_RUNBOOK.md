# 13 — VM MONITORING AND RECOVERY RUNBOOK
**Phase J & L Deliverable | Hostinger KVM 2 / Staging VM (`10.44.155.57`)**

---

## 1. Quick Emergency Service Commands

> [!WARNING]
> **Co-Hosted Safety Rule:** The VM runs co-hosted services (`pairdo-staging-*`). Never run `docker stop $(docker ps -q)` or `docker system prune --volumes`. Always target `fulcrum-app` and `fulcrum-caddy` explicitly.

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
| **Streamlit Health Endpoint** | `curl -f http://localhost:8501/_stcore/health` | `200 ok` | HTTP 5xx or Connection Refused |
| **Reverse Proxy Health** | `curl -f http://localhost:8081/_stcore/health` | `200 ok` | Caddy Bad Gateway (502) |
| **Container Memory Usage** | `docker stats fulcrum-app --no-stream` | `< 1,200 MiB` (`< 65%`) | `> 1,600 MiB` (`> 90%` limit) |
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
   - Check logs: `docker logs fulcrum-app`
   - Verify `.env` file presence and permissions: `ls -la .env && cat .env` (confirm `SUPABASE_URL` is set).
   - Test Supabase network connectivity from host: `curl -I https://bhaqaawsufwtjeqfifbv.supabase.co/rest/v1/`
2. **If Host Runs Low on Memory:**
   - Check which process is consuming memory: `top -b -o +%MEM | head -n 15`
   - Verify `pairdo-staging` and `fulcrum` cgroups: `docker stats --no-stream`
   - Clear Linux buffer cache safely without killing processes: `sudo sysctl -w vm.drop_caches=3`
3. **If Database Connectivity Drops:**
   - Supabase status check: Visit status.supabase.com
   - The application fails closed and presents a user-friendly error banner without corrupting state. Once network restores, Streamlit auto-reconnects.
