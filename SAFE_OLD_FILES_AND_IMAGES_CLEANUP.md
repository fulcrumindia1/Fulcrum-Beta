# SAFE OLD FILES & DOCKER IMAGES CLEANUP RUNBOOK
**Platform:** Fulcrum India (Cluster A / Fulcrum-Beta)  
**Host Target:** Hostinger KVM 2 VPS (Ubuntu 24.04.5 LTS)  
**Safety Classification:** Strictly Guarded / Allowlist-Only  
**Date:** 2026-11-10  

---

## 1. Safety Objectives & Warning

Over weeks of deployments, Docker and Linux can accumulate unused image layers, build caches, and temporary files that slowly consume disk space on your KVM 2 VPS.

> [!CAUTION]
> **NEVER run `docker system prune -a --volumes` or `docker volume prune`!**  
> Running broad prune commands will delete the `caddy_data` volume containing your active Let's Encrypt TLS certificates, causing downtime and triggering rate-limit lockouts.

This runbook provides **strictly allowlisted commands** that reclaim disk space safely without touching running containers, SSL certificates, or production environment files.

---

## 2. Forbidden Commands (Blacklist)

Do **NOT** execute any of the following dangerous commands on your VPS:

| Forbidden Command | Catastrophic Consequence |
| :--- | :--- |
| `docker system prune -a` | Deletes base images for Caddy and Python, forcing long downloads. |
| `docker system prune --volumes` | **Destroys `caddy_data`**, wiping active Let's Encrypt certificates. |
| `docker volume rm $(docker volume ls -q)` | Destroys all persistent state across all Docker containers. |
| `rm -rf /opt/fulcrum` | Destroys production `.env` and application configuration. |
| `docker rm -f $(docker ps -aq)` | Terminates both Caddy and Fulcrum, taking the entire site offline. |

---

## 3. Safe Allowlisted Cleanup Sequence

Execute these safe commands in order:

### Step 3.1: Check Current Disk Usage
Inspect your VPS disk partitions to understand available space:

```bash
df -h /
```
*(Aim to keep root partition usage below 80%).*

### Step 3.2: Inspect Docker Disk Footprint
See how much space Docker images, containers, and build cache are consuming:

```bash
docker system df
```

### Step 3.3: Prune ONLY Dangling Docker Images (Safe)
Dangling images are untagged layers (`<none>:<none>`) left behind after a new image is built. Removing them is 100% safe:

```bash
# Preview what would be removed (without deleting)
docker images -f "dangling=true"

# Safely prune ONLY dangling untagged images
docker image prune -f
```
*(This does NOT touch `caddy:2-alpine` or `fulcrum-app:pre_deploy_backup`).*

### Step 3.4: Prune Stale Docker Build Cache (Older than 48 Hours)
Reclaim space from multi-stage Docker builds without forcing a complete rebuild from scratch:

```bash
# Prune build caches older than 48 hours
docker builder prune --filter "until=48h" -f
```

### Step 3.5: Remove Temporary WinSCP Upload Staging Directory
After a successful deployment, verify `/opt/fulcrum_incoming` is no longer needed and remove it:

```bash
if [ -d "/opt/fulcrum_incoming" ]; then
    rm -rf /opt/fulcrum_incoming
    echo "[+] Cleaned temporary upload directory: /opt/fulcrum_incoming"
fi
```

### Step 3.6: Rotate Old Pre-Deployment Backups (Keep Last 5)
If you have created multiple backup snapshots in `/opt/fulcrum_backups`, retain the 5 most recent and delete older ones:

```bash
mkdir -p /opt/fulcrum_backups
cd /opt/fulcrum_backups

# List all backups
ls -lt

# Keep the 5 most recent directories and safely remove older ones
ls -dt /opt/fulcrum_backups/* | tail -n +6 | xargs -r rm -rf
echo "[+] Retained 5 most recent backups in /opt/fulcrum_backups."
```

### Step 3.7: Purge Stale Systemd Journal Logs
Ubuntu systemd logs can accumulate over months. Cap journal log retention to 100 MB:

```bash
journalctl --vacuum-size=100M
```

---

## 4. Post-Cleanup Verification

Verify that Caddy and Fulcrum are still completely healthy and serving traffic:

```bash
# 1. Verify container status
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 2. Check disk space reclaimed
df -h /
```
*(Both `fulcrum-caddy` and `fulcrum-app` must report active running status).*

