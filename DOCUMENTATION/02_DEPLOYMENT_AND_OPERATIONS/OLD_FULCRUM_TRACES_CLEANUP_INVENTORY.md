# OLD FULCRUM TRACES & CLEANUP INVENTORY
**Platform:** Fulcrum India (Cluster A / Fulcrum-Beta)  
**Host Target:** Hostinger KVM 2 VPS (`/opt/fulcrum`)  
**Deployment Model:** Fresh Clean-Slate Deployment  
**Date:** 2026-11-10  

---

## 1. Executive Summary

Because this release is a **clean-slate deployment** connecting to a fresh Supabase instance with zero legacy user accounts, the existing `/opt/fulcrum` directory on the VPS contains artifacts, scripts, and temporary databases that are obsolete, unnecessary, or potentially dangerous.

This inventory provides a **rigorous KEEP / REPLACE / DELETE categorization** to ensure:
1. Production credentials (`.env`) and Caddy configurations are never deleted.
2. The core application files are replaced cleanly from `FULCRUM_FRESH_DEPLOYMENT`.
3. Outdated SQLite files, test scripts, and risky deployment scripts are safely archived and purged.

---

## 2. Complete Inventory & Action Register

| File / Directory Path in `/opt/fulcrum` | Classification | Action Required | Reason & Risk Assessment |
| :--- | :--- | :--- | :--- |
| **`.env`** | **KEEP (CRITICAL)** | **DO NOT TOUCH** | Holds VPS Supabase credentials and domain config. Never delete or overwrite. |
| **`Caddyfile`** | **KEEP (CRITICAL)** | **DO NOT TOUCH** | Holds live reverse-proxy routing. Must not be replaced blindly. |
| **`docker volumes` (`caddy_data`)** | **KEEP (CRITICAL)** | **DO NOT TOUCH** | Holds live Let's Encrypt TLS certificates. Must not be pruned. |
| **`app.py`** | **REPLACE** | Update from release package | Upgraded with lazy tab execution and optimized state tracking. |
| **`docker-compose.yml`** | **REPLACE** | Update from release package | Updated with 5 GB memory limit and `SOLE_ADMIN_UUID` pass-through. |
| **`Dockerfile`** | **REPLACE** | Update from release package | Updated with build-time Chromium browser dependencies. |
| **`requirements.txt`** | **REPLACE** | Update from release package | Production-locked Python dependencies. |
| **`.dockerignore`** | **REPLACE** | Update from release package | Excludes secret files, tests, and documentation from build context. |
| **`.streamlit/config.toml`** | **REPLACE** | Update from release package | Streamlit light theme, headless mode, and CSRF protection settings. |
| **`services/`** | **REPLACE** | Replace entire directory | Contains all 29 security-hardened and query-optimized service modules. |
| **`views/`** | **REPLACE** | Replace entire directory | Contains all 10 views with server-side pagination and lazy rendering. |
| **`scripts/health_check.py`** | **REPLACE** | Update from release package | Non-destructive deep health check for Streamlit and Supabase ping. |
| **`scripts/FRESH_FULCRUM_ONLY_DEPLOY.sh`** | **ADD** | Install from release package | Safe deployment script targeting only the Fulcrum container. |
| **`scripts/SAFE_FULCRUM_ONLY_ROLLBACK.sh`** | **ADD** | Install from release package | Instant rollback script restoring tagged pre-deploy image. |
| **`scripts/status.sh`** | **ADD / UPDATE** | Install from release package | Safe container resource and health inspector. |
| **`scripts/logs.sh`** | **ADD / UPDATE** | Install from release package | Streamlined container logging utility. |
| **`scripts/restart.sh`** | **REPLACE** | Update from release package | Updated to restart Fulcrum only, leaving Caddy untouched. |
| **`seed/`** | **ADD / UPDATE** | Install from release package | Canonical 179 government schemes catalogue. |
| **`migrations/`** | **ADD / UPDATE** | Install from release package | SQL migration reference files for Supabase SQL Editor. |
| **`cluster_a.db` & `*.db*`** | **SAFE DELETE** | Archive then remove | Old local SQLite test databases. Fresh production uses Supabase exclusively. |
| **`scripts/deploy_to_server.py`** | **SAFE DELETE** | Remove immediately | High-risk legacy script containing `rm -rf /opt/fulcrum` command. |
| **`scripts/deploy.sh` (old)** | **SAFE DELETE** | Replace with new deploy script | Ran `--remove-orphans` and restarted Caddy. |
| **`tests/`** | **SAFE DELETE** | Remove from production host | Test suites belong in CI/CD and staging, not on production host. |
| **`scratch/`, `backups/`** | **SAFE DELETE** | Archive then remove | Temporary local development artifacts. |
| **`*.pyc`, `__pycache__/`** | **SAFE DELETE** | Purge | Stale bytecode caches from previous Python runs. |
| **`*.pdf`, `*.log`** | **SAFE DELETE** | Purge | Temporary test output and old log dumps. |

---

## 3. Step-by-Step Archival & Cleanup Runbook

Execute these commands on your VPS terminal before copying the new release files into `/opt/fulcrum`.

### Step 3.1: Create Immutable Pre-Deployment Safety Backup
Back up the existing configuration, `.env`, and Caddyfile to an independent directory:

```bash
# 1. Create a timestamped backup directory outside /opt/fulcrum
BACKUP_DIR="/opt/fulcrum_backups/backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# 2. Back up environment secrets and web server configs
cp /opt/fulcrum/.env "$BACKUP_DIR/.env.bak"
cp /opt/fulcrum/Caddyfile "$BACKUP_DIR/Caddyfile.bak"
cp /opt/fulcrum/docker-compose.yml "$BACKUP_DIR/docker-compose.yml.bak" 2>/dev/null || true

echo "[+] Configuration safely backed up to: $BACKUP_DIR"
```

### Step 3.2: Archive and Remove Obsolete Local SQLite Databases
Safely move legacy SQLite databases out of `/opt/fulcrum` into the backup directory:

```bash
# Move any existing SQLite database files to backup
mv /opt/fulcrum/*.db "$BACKUP_DIR/" 2>/dev/null || true
mv /opt/fulcrum/*.db-journal "$BACKUP_DIR/" 2>/dev/null || true
mv /opt/fulcrum/*.bak "$BACKUP_DIR/" 2>/dev/null || true

echo "[+] Legacy SQLite databases archived to: $BACKUP_DIR"
```

### Step 3.3: Remove Risky Legacy Deployment Scripts
Purge old scripts that contained dangerous commands:

```bash
# Remove dangerous legacy scripts
rm -f /opt/fulcrum/scripts/deploy_to_server.py
rm -f /opt/fulcrum/scripts/deploy.sh
rm -rf /opt/fulcrum/scratch
rm -rf /opt/fulcrum/tests
rm -rf /opt/fulcrum/__pycache__
rm -rf /opt/fulcrum/*/__pycache__
rm -f /opt/fulcrum/*.pdf
rm -f /opt/fulcrum/*.log

echo "[+] Risky scripts and temporary caches purged."
```

### Step 3.4: Verify Integrity of Preserved Files
Ensure that `.env` and `Caddyfile` are present and intact in `/opt/fulcrum`:

```bash
ls -la /opt/fulcrum/.env /opt/fulcrum/Caddyfile
```
*(Both files must appear with non-zero file sizes).*

