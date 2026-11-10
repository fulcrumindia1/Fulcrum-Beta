# FULCRUM-BETA 2.1 — PRODUCTION DEPLOYMENT RUNBOOK (HOSTINGER KVM 2)

**Document Status:** Approved Operational Runbook  
**Date:** November 10, 2026  
**Auditor:** Independent Principal Systems Forensic Engineer & Release Architect  
**Target Host:** Hostinger KVM 2 VPS (`187.126.114.81` / `srv2003170`)  
**Hardware Specifications:** Ubuntu 24.04.5 LTS | 2 vCPU | 8 GB RAM | 100 GB NVMe Disk  
**Memory Guard:** Hard 5 GB Docker limit (`deploy.resources.limits.memory: 5120M`)  

---

## 1. Pre-Deployment Transfer Instructions

The release package is compiled into a copy-only clean zip file:
- **Source File:** `FULCRUM_FRESH_DEPLOYMENT.zip` (in workspace root)
- **Manifest File:** `RELEASE_FILE_MANIFEST_SHA256.txt` (64 files)

### 1.1 Transferring via WinSCP (ELI5 Step-by-Step)
1. Open **WinSCP** and connect to `root@187.126.114.81`.
2. In the **Left Pane (Local Windows)**:
   - Navigate to: `C:\Users\hp\Desktop\Fulcrum-Alpha\fulcrum-cluster-b\`
3. In the **Right Pane (Remote VPS)**:
   - Navigate to: `/opt/fulcrum/`
4. On the left side, drag **`FULCRUM_FRESH_DEPLOYMENT.zip`** into `/opt/fulcrum/` on the right side.

---

## 2. In-VPS Deployment Execution (Single Copy-Paste Command)

Open the VPS SSH Terminal (via browser Web Terminal or PuTTY/SSH) and execute the following commands:

```bash
# 1. Navigate to target directory
cd /opt/fulcrum

# 2. Extract the fresh deployment zip over /opt/fulcrum
unzip -o FULCRUM_FRESH_DEPLOYMENT.zip -d /opt/fulcrum/

# 3. Ensure executable permissions on all shell scripts
chmod +x /opt/fulcrum/scripts/*.sh

# 4. Execute the dedicated Fulcrum container build and launch script
bash /opt/fulcrum/scripts/FRESH_FULCRUM_ONLY_DEPLOY.sh
```

---

## 3. What the Deployment Script Does Automatically

The automated deployment script (`scripts/FRESH_FULCRUM_ONLY_DEPLOY.sh`) executes with zero downtime to existing Caddy certificates:
1. **Preserves Existing Configurations:** Leaves `.env` and `Caddyfile` untouched.
2. **Backs Up Current Image:** Tags existing container image as `fulcrum-app:pre_deploy_backup`.
3. **Rebuilds Container:** Builds `fulcrum-app` inside Docker using `python:3.11-slim`.
4. **Re-creates Service:** Executes `docker compose up -d --no-deps --force-recreate fulcrum`.
5. **Verifies Health:** Performs HTTP probe against `http://localhost:8501/_stcore/health` until HTTP 200 is confirmed.

---

## 4. Post-Deployment Verification Commands

Run the following quick verification commands on the VPS:

```bash
# Check running containers and resource limits
docker compose ps
docker stats --no-stream

# View real-time application logs
docker compose logs -f fulcrum --tail=100

# Execute internal container health check
docker compose exec -T fulcrum python scripts/health_check.py
```

---

## 5. Verification Checklist

- [ ] HTTP 200 returned from `https://app.fulcrumindia.online/_stcore/health`
- [ ] Admin Portal loads with `179 Records in Intelligence Database` (Tab 6)
- [ ] Entrepreneurs Directory loads without `UnboundLocalError` (Tab 3)
- [ ] Container memory usage remains below 1.5 GB under active navigation.

