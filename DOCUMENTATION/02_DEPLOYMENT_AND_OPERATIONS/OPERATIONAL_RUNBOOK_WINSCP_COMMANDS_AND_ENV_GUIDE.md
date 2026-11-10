# FULCRUM-INDIA — OPERATIONAL RUNBOOK: WINSCP, COMMANDS & ENV GUIDE (ELI5)

**Target Audience:** System operators, DevOps, maintainers  
**Server Target:** Hostinger KVM 2 VPS (`srv2003170` / `187.126.114.81`) | Ubuntu 24.04  
**App Path:** `/opt/fulcrum/`  
**Public Domain:** `https://app.fulcrumindia.online`  
**Last Updated:** November 10, 2026  

---

## 1. WINSCP WORKFLOW (HOW TO UPDATE YOUR WEBSITE)

Whenever you have new changes on your computer and want to update the live website:

### Step 1: Open WinSCP
1. Connect to your VPS using your saved session (`root@187.126.114.81`).
2. **Left Pane (Your PC):** Navigate to:
   ```text
   C:\Users\hp\Desktop\Fulcrum-Alpha\fulcrum-cluster-b\FULCRUM_FRESH_DEPLOYMENT
   ```
3. **Right Pane (VPS):** Navigate to:
   ```text
   /opt/fulcrum/
   ```

### Step 2: Drag & Overwrite
1. In the Left Pane, select **all files and folders** inside `FULCRUM_FRESH_DEPLOYMENT`.
2. Drag them across to the Right Pane into `/opt/fulcrum/`.
3. When WinSCP asks whether to overwrite existing files, select **"Yes to All"** (or Overwrite).

> [!IMPORTANT]
> **What files are safe?**  
> `FULCRUM_FRESH_DEPLOYMENT` does **NOT** contain `.env` or `Caddyfile`. Your real live credentials and SSL certificates inside `/opt/fulcrum/.env` and `/opt/fulcrum/Caddyfile` will **never** be deleted or overwritten by dragging files.

---

## 2. HOSTINGER BLACK TERMINAL COMMANDS (CHEAT SHEET)

Open your Hostinger VPS Web Terminal (or SSH PuTTY) and run these commands:

### A. Apply Updates & Rebuild (Run this right after WinSCP transfer)
```bash
cd /opt/fulcrum
chmod +x /opt/fulcrum/scripts/*.sh
docker compose build fulcrum
docker compose up -d --no-deps --force-recreate fulcrum
docker compose ps
```

### B. Check if App is Healthy & Running
```bash
# Check container status (should show 'Up' and healthy)
docker compose ps

# Check the built-in health check endpoint
curl -f http://localhost:8501/_stcore/health
```
*(If healthy, it will output `ok`).*

### C. View Live Application Logs (For debugging)
```bash
# View recent logs and stream new logs live
docker compose logs -f fulcrum

# Press Ctrl + C to exit the log stream
```

### D. Restart the Container (Quick 5-second restart)
```bash
docker compose restart fulcrum
```

### E. Stop and Start
```bash
# Stop the app container safely
docker compose stop fulcrum

# Start the app container
docker compose start fulcrum
```

---

## 3. HOW TO VIEW AND EDIT `.env` (ENVIRONMENT VARIABLES)

The `.env` file contains your sensitive database passwords, Supabase keys, and domain URLs.

### Method 1: Edit `.env` in WinSCP (Easiest / Point-and-Click)
1. In WinSCP on the Right Pane, make sure hidden files are visible (Press `Ctrl + Alt + H` if needed).
2. Right-click on `/opt/fulcrum/.env` and choose **Edit** (or press `F4`).
3. Make your changes in the notepad editor.
4. Click **Save** (`Ctrl + S`) and close the editor.
5. In your black terminal, restart the container so it reads the new `.env`:
   ```bash
   docker compose restart fulcrum
   ```

---

### Method 2: Edit `.env` in the Black Terminal (Using `nano`)
1. In your terminal, type:
   ```bash
   nano /opt/fulcrum/.env
   ```
2. Use arrow keys to navigate to the line you want to change.
3. Edit the value.
4. Save and exit:
   * Press **`Ctrl + O`**, then hit **`Enter`** (to save).
   * Press **`Ctrl + X`** (to exit nano).
5. Restart the container to apply changes:
   ```bash
   docker compose restart fulcrum
   ```

---

### Essential Variables Explained in `.env`

```ini
# The public domain where users access the site
APP_URL=https://app.fulcrumindia.online

# Must be 'supabase' in production (or 'sqlite' for offline local testing)
DATA_BACKEND=supabase

# Your project URL from Supabase Dashboard
SUPABASE_URL=https://bhaqaawsufwtjeqfifbv.supabase.co

# Public anon/publishable key used for client authentication
SUPABASE_PUBLISHABLE_KEY=sb_publishable_...

# Secret service-role key used for administrative actions and backups
SUPABASE_SECRET_KEY=sb_secret_...
```

> [!WARNING]
> Never share your `SUPABASE_SECRET_KEY` with anyone or commit it to GitHub. It has administrative database privileges.

---

## 4. TROUBLESHOOTING & EMERGENCY ROLLBACK

### Symptom 1: "The website shows 502 Bad Gateway"
* **Cause:** The Docker container hasn't finished booting up yet, or crashed on start.
* **Fix:** Check the logs:
  ```bash
  docker compose logs fulcrum --tail=50
  ```
  Look for any syntax error or missing secret. If needed, restart:
  ```bash
  docker compose restart fulcrum
  ```

### Symptom 2: "Caddy SSL / Certificate issue"
* **Fix:** Check Caddy status:
  ```bash
  docker compose ps caddy
  docker compose logs caddy --tail=30
  ```

### Symptom 3: Emergency 45-Second Rollback
If you ever deploy an update that causes issues and you want to instantly revert back to the previous working version:
```bash
cd /opt/fulcrum
bash /opt/fulcrum/scripts/SAFE_FULCRUM_ONLY_ROLLBACK.sh
```
This automatically restores the previous Docker image backup (`fulcrum-app:pre_deploy_backup`) and brings your site back online in under 45 seconds.
