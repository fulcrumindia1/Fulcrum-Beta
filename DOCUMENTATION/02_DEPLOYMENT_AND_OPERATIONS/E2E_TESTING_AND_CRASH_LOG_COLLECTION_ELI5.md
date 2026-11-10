# E2E Tests, Crash Readiness & Sending Crash Logs to AGY (ELI5)

> **Plain-English Goal:** Know what automated tests exist, how to run the safe offline ones without ever touching live users, whether Fulcrum will crash, and the exact 1-line command to grab crash logs for AGY if anything ever goes wrong.

---

## 1. "Will There Be Any Crash?" — The Honest Answer

No software on Earth can promise *100% zero bugs forever*, **but here is why Fulcrum is in a clean, stable state right now:**

1. **Zero syntax or broken-import traps:** All **42** Python modules (`app.py`, `services/`, `views/`) passed [`FULCRUM_PREDEPLOY_CONTRACT_CHECK.py`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/FULCRUM_PREDEPLOY_CONTRACT_CHECK.py) inside the live `fulcrum-app` Docker `Python 3.11.18` runtime (`0` blockers).
2. **Plenty of server breathing room:** Live `fulcrum-app` uses ~`62.6 MiB` out of `5 GB` RAM, VPS disk is `6.6 GB / 96 GB` (`90 GB` free), and `https://app.fulcrumindia.online/_stcore/health` reports **`ok`**.
3. **Offline workflows & security checks passed:** Core lifecycle, multi-role promotions, 179 scheme matching/release, photo permissions, and password-recovery tests all ran and passed locally (`DATA_BACKEND=sqlite` + `FULCRUM_FORBID_PRODUCTION=1`).
4. **Even if a rare crash ever happens:** Your real data lives safely in Supabase Cloud (not inside the container), you can roll back any update in **45 seconds** (`./scripts/SAFE_FULCRUM_ONLY_ROLLBACK.sh`), and you can copy the exact crash log for AGY with one command below.

*(Honest note: After today's fixes, we verified the live login/speed benchmark, Forgot Password request, your live email reset test, static Python 3.11 checks, and offline SQLite E2E suites — not an exhaustive live browser click-through of every Guide/SME/Admin screen on production.)*

---

## 2. E2E Tests Explained Simply ("Mystery Shopper Robots")

Think of an **E2E (End-to-End) test** like a robot mystery shopper that automatically pretends to be an Aspirant, Guide, SME, and Admin — testing signup, Terms/NDA acceptance, matching 179 schemes, uploading photos, and checking privacy locks.

There are **two completely different kinds** of test scripts in this project — know which is safe!

### Type A — 100% Safe Offline Tests (Touch ONLY Your Local Test File `cluster_a.db`)
Run these anytime from PowerShell inside `c:\Users\hp\Desktop\Fulcrum-Alpha\fulcrum-cluster-b`.  
Notice the **`FULCRUM_FORBID_PRODUCTION=1`** safety lock — it **blocks** any accidental connection to live Supabase:

```powershell
# 1. Safe Offline E2E + Workflows + Photos + 179 Schemes Suite (~50s):
$env:FULCRUM_DATA_BACKEND='sqlite'; $env:DATA_BACKEND='sqlite'; $env:FULCRUM_FORBID_PRODUCTION='1'; python -m pytest tests/test_single_admin_master_e2e.py tests/test_multi_role_e2e_workflows.py tests/test_account_lifecycle_and_handover_chaos.py tests/test_aspirant_photo_dashboard_visibility.py tests/test_scheme_relevance_synthetic.py -v

# 2. Safe Password Recovery Security Suite (7 passed, 1 skipped without staging):
$env:FULCRUM_FORBID_PRODUCTION='1'; python -m pytest tests/test_password_recovery_suite.py -v

# 3. Pre-Deploy Static "Spellcheck" (42 files vs SQL contracts, zero DB writes):
python FULCRUM_PREDEPLOY_CONTRACT_CHECK.py .
```

### Type B — Staging-Only Scripts (DO NOT Run Against Live `.env`!)
> ⚠️ **Never run these while `.env` points to production (`bhaqaawsufwtjeqfifbv`):**  
> Scripts like `scripts/run_circular_e2e_master_suite.py`, `scripts/run_advanced_institutional_e2e_suite.py`, `tests/test_concurrency_load.py`, `tests/test_cross_session_isolation.py`, and `tests/test_failure_isolation.py` call `dotenv.load_dotenv(override=True)` and create multi-role test accounts in whatever Supabase project `.env` points to. Only use those when `.env` points to a separate **staging** Supabase project!

---

## 3. If a Crash Happens: Exact Commands to Check & Copy Logs to AGY

### Step 1 — Copy Logs Straight From Windows PowerShell to Send to AGY

Run **one** of these commands on your Windows PC PowerShell (it saves the crash trace cleanly without touching your `.env` secrets):

**Option A — Save into a text file (`fulcrum_crash_logs.txt`) to attach or paste:**
```powershell
ssh root@187.126.114.81 "echo '=== STATUS ==='; docker ps -a --filter name=fulcrum-; echo '=== STATE ==='; docker inspect fulcrum-app --format='Status={{.State.Status}} ExitCode={{.State.ExitCode}} OOMKilled={{.State.OOMKilled}} Error={{.State.Error}}'; echo '=== APP LOGS (LAST 250) ==='; docker logs --tail=250 fulcrum-app 2>&1; echo '=== CADDY LOGS (LAST 80) ==='; docker logs --tail=80 fulcrum-caddy 2>&1" > fulcrum_crash_logs.txt
```

**Option B — Copy directly to your Windows Clipboard (then just press `Ctrl+V` into AGY chat):**
```powershell
ssh root@187.126.114.81 "docker ps -a --filter name=fulcrum-; docker inspect fulcrum-app --format='Status={{.State.Status}} ExitCode={{.State.ExitCode}} OOMKilled={{.State.OOMKilled}} Error={{.State.Error}}'; docker logs --tail=250 fulcrum-app 2>&1" | Set-Clipboard
```

---

### Step 2 — Commands If You Are Already Logged Into the VPS via SSH (`ssh root@187.126.114.81`)

```bash
# 1. Quick health overview (containers + memory + health_check.py)
cd /opt/fulcrum && ./scripts/status.sh

# 2. Check why container stopped / if it ran out of RAM (OOMKilled)
docker inspect fulcrum-app --format='Status={{.State.Status}} ExitCode={{.State.ExitCode}} OOMKilled={{.State.OOMKilled}} Error={{.State.Error}}'

# 3. Print last 250 lines of Fulcrum Python error logs (and save to /tmp/crash.txt)
docker logs --tail=250 fulcrum-app 2>&1 | tee /tmp/crash.txt

# 4. Watch live logs while reproducing an error (press Ctrl+C to stop)
cd /opt/fulcrum && ./scripts/logs.sh
```

> 🔒 **Privacy reminder:** `docker logs` does **not** print your Supabase secret keys, so it is safe to share with AGY. Just never copy-paste `/opt/fulcrum/.env` into chat!

---

### Step 3 — Quick Self-Rescue While Sending Logs to AGY
* **Site froze once (stale process):** `cd /opt/fulcrum && ./scripts/restart.sh` *(restarts app only, keeps HTTPS Caddy online)*
* **Just deployed an update and it broke:** `cd /opt/fulcrum && ./scripts/SAFE_FULCRUM_ONLY_ROLLBACK.sh` *(restores previous working image in ~45 seconds)*

