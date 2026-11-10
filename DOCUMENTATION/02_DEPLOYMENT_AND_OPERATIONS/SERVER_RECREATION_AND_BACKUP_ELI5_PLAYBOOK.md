# Server Recreation, Supabase Setup, Resend Email & Backup Playbook (ELI5)

> **When to use this guide:** If you ever get a brand-new Hostinger VPS, create a fresh Supabase database, or want a simple cheat sheet for backups, deploys, and cleaning up disk space.  
> **Written in plain English** — just follow top-to-bottom and copy-paste the commands.

---

## 1. The Big Picture (4 Pieces Only)

```text
Your Windows PC (Build package + Save backups/)
        │
        ├──▶ Upload ONLY FULCRUM_FRESH_DEPLOYMENT/ into /opt/fulcrum/
        │
        ▼
Hostinger VPS (/opt/fulcrum/)
  ├── fulcrum-caddy  (HTTPS padlock + routes app.fulcrumindia.online -> :8501)
  └── fulcrum-app    (Your Streamlit website running inside Docker)
        │
        ├──▶ Talks to Supabase Cloud (Database + Auth + Photo Storage)
        └──▶ Supabase sends emails via Resend (smtp.resend.com -> no-reply@notify.fulcrumindia.online)
```

---

## 2. Step Zero: How to Take Backups from Your Windows PC

Run these commands inside your project folder (`c:\Users\hp\Desktop\Fulcrum-Alpha\fulcrum-cluster-b`):

### Take a Full Supabase Cloud Backup (Database + Users + Uploaded Photos)
```powershell
python scripts/supabase_backup_manager.py backup
```
* **What it saves:** All 23 Supabase tables (`.json` + `.csv`), `auth_users.json`, and uploaded photos (`storage_files/`), bundled into:  
  `backups\supabase_backup_YYYY-MM-DD_HH-MM-SS.zip`

### Take an All-Inclusive Backup (Supabase Cloud + Local `cluster_a.db` + Photos)
```powershell
python scripts/create_unified_database_backup.py
```
* **What it saves:** Everything above **plus** your local `cluster_a.db` SQL dump into:  
  `backups\fulcrum_database_backup_YYYY-MM-DD_HH-MM-SS.zip`

### How to Restore a Backup to Supabase (or Offline SQLite)
```powershell
# Restore back into Supabase Cloud (from .env credentials):
python scripts/supabase_backup_manager.py restore backups\supabase_backup_YYYY-MM-DD_HH-MM-SS.zip

# OR restore into local offline SQLite (cluster_a.db):
python scripts/supabase_backup_manager.py restore-sqlite backups\supabase_backup_YYYY-MM-DD_HH-MM-SS.zip
```
> **Note about passwords:** Supabase never lets anyone download encrypted user passwords. After restoring users into a brand-new Supabase project, users simply click **Forgot Password?** on the login page to pick a password (which Resend now delivers cleanly!).

---

## 3. Setting Up a Brand-New (Fresh) Supabase Project

If you create a new Supabase project at [supabase.com](https://supabase.com):

1. **Create Project:** Choose **South Asia (Mumbai) `ap-south-1`**. Save your database password safely.
2. **Create Tables & 179 Schemes (SQL Editor):**  
   Open **SQL Editor → New Query** in Supabase, copy-paste each file from `FULCRUM_FRESH_DEPLOYMENT/` (or root `migrations/` and `seed/`), and click **Run** one by one in this **exact order**:
   1. `migrations/000_complete_beta_setup.sql` *(base tables, RLS security, signup trigger, `aspirant-profile-photos` bucket)*
   2. `migrations/008_single_admin_lock_professional_photos_and_workflow_columns.sql` *(single-admin lock, `professional-headshots` bucket, scheme releases)*
   3. `migrations/009_account_lifecycle_and_archive.sql` *(lifecycle states + protection against accidental deletions)*
   4. `seed/seed_179_schemes_idempotent.sql` *(inserts all **179** government schemes)*
3. **Check Storage Buckets (`Storage → Buckets`):**  
   Confirm both **`aspirant-profile-photos`** and **`professional-headshots`** exist and are **Private** (`Public = OFF`).
4. **Set Website Return URLs (`Authentication → URL Configuration`):**
   * **Site URL:** `https://app.fulcrumindia.online`
   * **Redirect URLs:** `https://app.fulcrumindia.online/**`
5. **Create Your Admin Account (`Authentication → Users → Add user`):**
   * Email: `fulcrumindia1@gmail.com` + strong password + check **Auto Confirm User**.
6. **Grab Your 3 API Keys (`Project Settings → API`):**  
   Copy **Project URL**, **Publishable (`anon`) Key**, and **Secret (`service_role`) Key** for Step 5 below.

---

## 4. Hostinger DNS + Resend Email Setup

### A. Point `app.fulcrumindia.online` to Your Server (`Hostinger → Domains → DNS`)
* Add or update the **`A` record**:
  * **Type:** `A` | **Name:** `app` | **Points to:** `<YOUR_NEW_VPS_IP>`
* Leave `@` and `www` untouched if your landing page is on Vercel.

### B. Connect Resend (`notify.fulcrumindia.online` + Supabase SMTP)
*(Full visual guide: [`RESEND_SMTP_AND_FORGOT_PASSWORD_ELI5_GUIDE.md`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/DOCUMENTATION/02_DEPLOYMENT_AND_OPERATIONS/RESEND_SMTP_AND_FORGOT_PASSWORD_ELI5_GUIDE.md))*

1. In **Resend → Domains → Add Domain**: add `notify.fulcrumindia.online`, Region **Tokyo**, Click Tracking **OFF**, Open Tracking **OFF**, Receiving **OFF**.
2. In **Hostinger DNS**, add the **3 records** Resend shows (Hostinger automatically adds `.fulcrumindia.online`, so enter only the short prefix):
   * `TXT` named `resend._domainkey.notify` → `p=MIGfMA...` (full DKIM value from Resend)
   * `CNAME` named `rsend.notify` → `rsend-ap...` (full value from Resend)
   * `CNAME` named `send.notify` → `send.for...` (full value from Resend)
3. Click **Verify** in Resend, then create an **API Key** (`re_...`).
4. In **Supabase → Authentication → Emails → SMTP Settings**:
   * **Enable custom SMTP:** `ON`
   * **Sender email:** `no-reply@notify.fulcrumindia.online`
   * **Sender name:** `FULCRUM-INDIA`
   * **Host:** `smtp.resend.com` | **Port:** `465` | **Username:** `resend` | **Password:** your `re_...` API key
   * Click **Save changes**.

---

## 5. Recreating the Server (`/opt/fulcrum/`) Step-by-Step

### Step 1 — Pack the Clean Release Folder on Your Windows PC
```powershell
python scripts/package_fresh_release.py
```
This creates **`FULCRUM_FRESH_DEPLOYMENT/`** and **`FULCRUM_FRESH_DEPLOYMENT.zip`** (safe copy with zero `.env`, zero `.db`, zero secret keys).

### Step 2 — Prepare a Brand-New Ubuntu 24.04 VPS (Run Once via SSH)
```bash
ssh root@YOUR_NEW_VPS_IP

apt update && apt upgrade -y
apt install -y curl ca-certificates git ufw unzip
curl -fsSL https://get.docker.com | sh

ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable

mkdir -p /opt/fulcrum
```
*(Port `8501` stays closed to the outside world — Caddy proxies `443 -> 8501` securely inside Docker.)*

### Step 3 — Which Folder Goes Into `/opt/`?
* **Target folder on VPS:** **`/opt/fulcrum/`**
* **What to copy:** Everything **inside** **`FULCRUM_FRESH_DEPLOYMENT/`** so that `/opt/fulcrum/app.py`, `/opt/fulcrum/Dockerfile`, `/opt/fulcrum/docker-compose.yml`, `/opt/fulcrum/Caddyfile`, `/opt/fulcrum/services/`, `/opt/fulcrum/views/`, and `/opt/fulcrum/scripts/` live directly inside `/opt/fulcrum/`.
  *(Do **NOT** nest it as `/opt/fulcrum/FULCRUM_FRESH_DEPLOYMENT/app.py`!)*

* **Method A (WinSCP):** Open `FULCRUM_FRESH_DEPLOYMENT\` on the left, `/opt/fulcrum/` on the right, select all files & folders on the left (`Ctrl+A`), and drag them into `/opt/fulcrum/`.
* **Method B (SSH Zip Upload):**
  ```bash
  # On VPS after uploading FULCRUM_FRESH_DEPLOYMENT.zip to /tmp/:
  python3 -m zipfile -e /tmp/FULCRUM_FRESH_DEPLOYMENT.zip /tmp/fulcrum_unpack
  cp -rf /tmp/fulcrum_unpack/FULCRUM_FRESH_DEPLOYMENT/* /opt/fulcrum/
  cp -f /tmp/fulcrum_unpack/FULCRUM_FRESH_DEPLOYMENT/.dockerignore /opt/fulcrum/.dockerignore
  cp -f /tmp/fulcrum_unpack/FULCRUM_FRESH_DEPLOYMENT/.streamlit/config.toml /opt/fulcrum/.streamlit/config.toml
  rm -rf /tmp/fulcrum_unpack /tmp/FULCRUM_FRESH_DEPLOYMENT.zip
  ```

### Step 4 — Create `/opt/fulcrum/.env` on the VPS
Create the secrets file (never tracked in Git/ZIP):
```bash
cat > /opt/fulcrum/.env << 'EOF'
DATA_BACKEND=supabase
SUPABASE_URL=https://YOUR_PROJECT_ID.supabase.co
SUPABASE_PUBLISHABLE_KEY=YOUR_PUBLISHABLE_OR_ANON_KEY
SUPABASE_SECRET_KEY=YOUR_SECRET_SERVICE_ROLE_KEY
DOMAIN=app.fulcrumindia.online
APP_URL=https://app.fulcrumindia.online
EOF
chmod 600 /opt/fulcrum/.env
```

### Step 5 — First-Time Boot on a Fresh Server (Starts Caddy + Fulcrum Together!)
```bash
cd /opt/fulcrum
chmod +x scripts/*.sh
docker compose up -d --build
```
> ⚠️ **Important:** On a **brand-new empty server**, always run `docker compose up -d --build` the **first time** so **both** `fulcrum-caddy` (HTTPS SSL) and `fulcrum-app` start together! (`FRESH_FULCRUM_ONLY_DEPLOY.sh` uses `--no-deps` intentionally so future updates never interrupt Caddy.)

Check everything came up healthy:
```bash
./scripts/status.sh
```

---

## 6. Everyday `.sh` Commands (Updates, Undo, Logs & Disk Cleanup)

Once your VPS is running, all day-to-day commands live in `/opt/fulcrum/`:

| What You Want to Do | Exact Command on VPS (`cd /opt/fulcrum`) | Plain-English What Happens |
| :--- | :--- | :--- |
| **Deploy a code update** *(after copying new files to `/opt/fulcrum/`)* | `./scripts/FRESH_FULCRUM_ONLY_DEPLOY.sh` | Saves current version as `pre_deploy_backup`, rebuilds `fulcrum-app`, checks health (`Caddy` & `.env` untouched). |
| **Undo a bad update (45s rollback)** | `./scripts/SAFE_FULCRUM_ONLY_ROLLBACK.sh` | Switches `fulcrum-app` right back to `pre_deploy_backup`. |
| **Check health & RAM/CPU** | `./scripts/status.sh` | Shows running containers, memory usage, and runs `scripts/health_check.py`. |
| **Watch live app logs** | `./scripts/logs.sh` | Shows Streamlit logs (`./scripts/logs.sh caddy` for Caddy, `all` for both). |
| **Quick restart** | `./scripts/restart.sh` | Restarts `fulcrum-app` cleanly without touching Caddy. |
| **Free wasted Docker disk space** | `docker image prune -f && docker builder prune -f` | Deletes old orphaned toolboxes & dead build cache (keeps live app + current rollback backup safe!). Check disk afterward with `df -h /`. |

---

## 7. Quick Verification After Recreating Everything
1. Visit `https://app.fulcrumindia.online/_stcore/health` → should print **`ok`**.
2. Open `https://app.fulcrumindia.online/` → login screen should load cleanly.
3. Click **🔑 Forgot Password?** → enter a test user email → verify email arrives from **`no-reply@notify.fulcrumindia.online`**, opens the password-change screen cleanly, and lets them sign back in!

