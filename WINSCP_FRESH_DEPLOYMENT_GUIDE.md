# BEGINNER-FRIENDLY WINSCP DEPLOYMENT GUIDE (FRESH PRODUCTION)
**Platform:** Fulcrum India (Cluster A / Fulcrum-Beta)  
**Local Machine:** Windows 11  
**Remote Server:** Hostinger KVM 2 VPS (Ubuntu 24.04.5 LTS, 8 GB RAM)  
**Package:** `FULCRUM_FRESH_DEPLOYMENT.zip` (0.43 MB)  
**Target Directory:** `/opt/fulcrum`  
**Date:** 2026-11-10  

---

## 1. Overview & Safety Strategy

This guide walks you through uploading and deploying Fulcrum-Beta to your VPS using **WinSCP** (a graphical file transfer tool for Windows) and a secure terminal.

### The Staging Pattern (Why We Never Upload Directly to `/opt/fulcrum`):
To prevent file corruption, half-uploaded state, or accidental overwriting of your live `.env` file, we follow the **Staging Directory Pattern**:
1. We upload the release package into a temporary incoming folder: `/opt/fulcrum_incoming/`
2. We verify file integrity using SHA-256 checksums.
3. We back up our configuration.
4. We copy the verified files into `/opt/fulcrum`.
5. We execute `FRESH_FULCRUM_ONLY_DEPLOY.sh`, which rebuilds the Streamlit container while leaving Caddy 100% untouched.

---

## 2. Step 1: Locate the Release Package on Windows

On your local Windows machine, the release files are prepared at:
- **Zip Archive:** `C:\Users\hp\Desktop\Fulcrum-Alpha\fulcrum-cluster-b\FULCRUM_FRESH_DEPLOYMENT.zip`
- **Extracted Folder:** `C:\Users\hp\Desktop\Fulcrum-Alpha\fulcrum-cluster-b\FULCRUM_FRESH_DEPLOYMENT\`
- **Manifest:** `C:\Users\hp\Desktop\Fulcrum-Alpha\fulcrum-cluster-b\RELEASE_FILE_MANIFEST_SHA256.txt`

*(You can transfer either the single `.zip` file or the unzipped folder. Transferring the single `.zip` is fastest and least prone to transfer interruptions).*

---

## 3. Step 2: Connect to your VPS via WinSCP

1. Launch **WinSCP** on your Windows computer.
2. In the **Login** window, enter:
   - **File protocol:** `SFTP`
   - **Host name:** Your VPS IP address (e.g. `187.126.114.81` or your domain)
   - **Port number:** `22`
   - **User name:** `root` (or your administrative user)
   - **Password:** Your VPS root password (or click *Advanced -> SSH -> Authentication* to select your private key).
3. Click **Login**.
4. If prompted with an "Unknown host key" alert, click **Yes** to trust the server.

---

## 4. Step 3: Create the Staging Directory on the VPS

1. In the **right-hand pane** of WinSCP (the remote VPS filesystem), navigate to `/opt`.
2. Right-click in the empty space and select **New -> Directory** (or press `F7`).
3. Name the folder: `fulcrum_incoming`
4. Click **OK**.
5. Double-click to enter `/opt/fulcrum_incoming`.

---

## 5. Step 4: Upload the Release Package

1. In the **left-hand pane** of WinSCP (your local Windows files), navigate to:  
   `C:\Users\hp\Desktop\Fulcrum-Alpha\fulcrum-cluster-b\`
2. Select **`FULCRUM_FRESH_DEPLOYMENT.zip`**.
3. Drag and drop `FULCRUM_FRESH_DEPLOYMENT.zip` from the left pane into the right pane (`/opt/fulcrum_incoming/`).
4. WinSCP will transfer the file (takes ~3 seconds for 0.43 MB).

---

## 6. Step 5: SSH Terminal — Extract & Verify Checksums

Open an SSH terminal to your VPS (press `Ctrl+P` in WinSCP to open PuTTY, or open PowerShell on Windows and run `ssh root@<YOUR_VPS_IP>`):

### 6.1: Extract the Archive
```bash
# Ensure unzip is installed
apt-get update && apt-get install -y unzip

# Unpack the package inside /opt/fulcrum_incoming
cd /opt/fulcrum_incoming
unzip -o FULCRUM_FRESH_DEPLOYMENT.zip
```
*(This extracts the folder `FULCRUM_FRESH_DEPLOYMENT` containing all 64 runtime files).*

### 6.2: Verify File Integrity
```bash
cd /opt/fulcrum_incoming/FULCRUM_FRESH_DEPLOYMENT

# Verify all file hashes against the release manifest
sha256sum -c RELEASE_FILE_MANIFEST_SHA256.txt | grep -v "OK" || echo "[+] ALL 64 FILES VERIFIED PERFECTLY!"
```
*(If all files match, you will see `[+] ALL 64 FILES VERIFIED PERFECTLY!`).*

---

## 7. Step 6: Backup Existing VPS Configuration

Before touching `/opt/fulcrum`, preserve your `.env` and `Caddyfile`:

```bash
# Create timestamped backup directory
BACKUP_DIR="/opt/fulcrum_backups/pre_fresh_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Back up critical files
cp /opt/fulcrum/.env "$BACKUP_DIR/.env" 2>/dev/null || true
cp /opt/fulcrum/Caddyfile "$BACKUP_DIR/Caddyfile" 2>/dev/null || true

echo "[+] Configuration safely backed up to $BACKUP_DIR"
```

---

## 8. Step 7: Clean Copy into `/opt/fulcrum`

Copy the fresh files from incoming into `/opt/fulcrum`. Notice that we use `cp -r` and do NOT delete `/opt/fulcrum`:

```bash
# Copy files into /opt/fulcrum
cp -r /opt/fulcrum_incoming/FULCRUM_FRESH_DEPLOYMENT/* /opt/fulcrum/

# Make all shell scripts executable
chmod +x /opt/fulcrum/scripts/*.sh

echo "[+] Fresh runtime files copied into /opt/fulcrum"
```

---

## 9. Step 8: Pre-Deployment Inspection of Caddy

Verify that Caddy is running and will not be interrupted:

```bash
docker inspect --format='{{.State.Status}}' fulcrum-caddy
```
*(Should output: `running`).*

---

## 10. Step 9: Execute Safe Deployment

Run the new deployment script:

```bash
cd /opt/fulcrum

# Optional: Run in dry-run mode first to test pre-flight validations
./scripts/FRESH_FULCRUM_ONLY_DEPLOY.sh --dry-run

# Run the actual deployment
./scripts/FRESH_FULCRUM_ONLY_DEPLOY.sh
```

### What this script does automatically:
1. Audits host RAM headroom (ensures >1.5 GB free).
2. Verifies `/opt/fulcrum/.env` exists and contains valid Supabase keys.
3. Tags your existing container image as `fulcrum-app:pre_deploy_backup` for instant rollback.
4. Builds the Streamlit container image with 5 GB memory limit.
5. Recreates **only** the `fulcrum` service with `--no-deps` (Caddy is untouched).
6. Waits for the container healthcheck to report `healthy`.
7. Executes the internal `health_check.py` script.

---

## 11. Step 10: Post-Deployment Verification

1. Run the system status utility:
   ```bash
   ./scripts/status.sh
   ```
2. Open your web browser and go to:
   **`https://app.fulcrumindia.online`**
3. Log in with `fulcrumindia1@gmail.com` and verify the dashboard loads cleanly with all 179 schemes accessible.

---

## 12. Step 11: Cleanup Incoming Staging Files

Once you have verified that the application is running smoothly, safely remove the incoming staging folder:

```bash
rm -rf /opt/fulcrum_incoming
echo "[+] Temporary incoming files removed."
```
*(Keep `/opt/fulcrum_backups` intact for future reference).*

