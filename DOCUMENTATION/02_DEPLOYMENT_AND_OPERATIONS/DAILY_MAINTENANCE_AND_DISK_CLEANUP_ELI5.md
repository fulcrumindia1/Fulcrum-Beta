# Daily, Weekly & Disk-Cleanup Maintenance Guide (ELI5)

> **Golden Rule:** Fulcrum runs 24/7 automatically inside Docker — you do **not** need to restart the server every day.  
> Think of this like owning a car: quick 30-second dashboard check daily, weekly backup, and clearing out old trunk junk after an update.

---

## 1. The Exact Command That Cleaned Up That Dead `2.09 GB` Backup Toolbox

Whenever you deploy a new update (`FRESH_FULCRUM_ONLY_DEPLOY.sh`), the *previous* older backup image loses its label and sits quietly in the corner as an unused orphan (`<none>`), alongside leftover build packaging.

To throw away **only the dead orphan + unused build cache** (while keeping your **live app** and **current undo backup** 100% safe):

```bash
# 1. SSH into your VPS
ssh root@187.126.114.81

# 2. Delete ONLY dead untagged Docker images (what freed 2.09 GB):
docker image prune -f

# 3. Delete leftover unused build cache (what freed the extra 3.07 GB):
docker builder prune -f

# 4. Verify how much disk space is used now:
df -h /
```

> ⚠️ **Important Warning — Do NOT casually add `-a`:**  
> Never run `docker image prune -a` or `docker system prune -a` unless you are 100% sure your latest update works and you want to erase your **undo safety backup** (`fulcrum-app:pre_deploy_backup`). Without `-a`, both your live app and your safety backup stay completely untouched!

---

## 2. Daily Check (30 Seconds — Just in Your Browser, No Commands Needed)

1. **Check the heartbeat link:**  
   Open `https://app.fulcrumindia.online/_stcore/health` → should print **`ok`**.
2. **Quick glance at Resend (`Emails` tab):**  
   Make sure password-reset / signup emails show **Delivered** (no bounce errors).
3. **Optional glance at Hostinger VPS Overview:**  
   * **Memory usage (RAM):** normal is ~`8%`–`25%` (`5 GB` container limit).
   * **Disk usage:** normal is ~`7%`–`20%` (`6–15 GB` out of `100 GB`).

---

## 3. Weekly Routine (2 Minutes — Your Data Insurance!)

Run from your **Windows PC** inside `c:\Users\hp\Desktop\Fulcrum-Alpha\fulcrum-cluster-b`:

```powershell
# Takes a full backup of Supabase tables + Auth user list + uploaded profile photos:
python scripts/supabase_backup_manager.py backup
```
*(Or use the all-in-one backup including local `cluster_a.db`: `python scripts/create_unified_database_backup.py`.)*

* Backups save into `backups\supabase_backup_YYYY-MM-DD_HH-MM-SS.zip`.
* **Best habit:** Copy that `.zip` once a week to Google Drive or an external USB drive so even if your laptop fails, your users, 179 schemes, journeys, and photos are safe.

If you also want a quick VPS health printout via SSH:
```bash
cd /opt/fulcrum && ./scripts/status.sh
```

---

## 4. Monthly Housekeeping (5 Minutes)

1. **Update Ubuntu security patches on VPS:**
   ```bash
   ssh root@187.126.114.81
   apt update && apt upgrade -y
   ```
2. **Clean old dead Docker leftovers (same commands from Section 1):**
   ```bash
   docker image prune -f && docker builder prune -f && df -h /
   ```
3. **Check `/tmp` on VPS has no leftover deployment zip/unpack folders:**
   ```bash
   ls -la /tmp/fulcrum* 2>/dev/null || echo "Clean"
   ```
4. **Check Resend quota & domain health:**  
   Verify `notify.fulcrumindia.online` stays **Verified** and monthly sends are within your plan (`3,000/month` free tier).
5. **Keep 1 copy of `FULCRUM_FRESH_DEPLOYMENT.zip` synced** whenever code changes (`python scripts/package_fresh_release.py`).

---

## 5. Emergency "If Something Looks Wrong" Cheat Sheet

| Problem | What to Run on VPS (`ssh root@187.126.114.81`, `cd /opt/fulcrum`) | What It Does |
| :--- | :--- | :--- |
| **Check if site containers are healthy** | `./scripts/status.sh` | Shows container status, RAM/CPU, and runs `health_check.py`. |
| **See live error messages** | `./scripts/logs.sh` | Streams app logs (press `Ctrl+C` to exit; use `caddy` or `all` for proxy). |
| **App is stuck / unresponsive** | `./scripts/restart.sh` | Gently restarts Fulcrum app only (`Caddy` HTTPS keeps running). |
| **New update broke something** | `./scripts/SAFE_FULCRUM_ONLY_ROLLBACK.sh` | Restores previous working version (`pre_deploy_backup`) in ~45 seconds. |
| **Disk usage climbed after deploys** | `docker image prune -f && docker builder prune -f` | Frees dead orphaned images & old build cache without stopping the site. |
| **Emails stopped delivering** | Check **Resend → Emails** & **Supabase → SMTP Settings** | Look for bounces/quota limits; verify Click & Open Tracking are **OFF**. |

