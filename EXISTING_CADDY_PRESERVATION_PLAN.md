# EXISTING CADDY CONTAINER PRESERVATION & ZERO-DOWNTIME REVERSE PROXY PLAN
**Platform:** Fulcrum India (Cluster A / Fulcrum-Beta)  
**Host Target:** Hostinger KVM 2 VPS (Ubuntu 24.04.5 LTS)  
**Container Target:** `fulcrum-caddy` (Caddy 2 Alpine)  
**Ports:** 80 (HTTP) & 443 (HTTPS)  
**Date:** 2026-11-10  

---

## 1. Architectural Invariant: Never Interfere with Caddy

On your Hostinger KVM 2 VPS, **Caddy is already installed, configured, actively proxying, and maintaining live TLS certificates**.

### Critical Production Rules:
1. **Never run `docker compose down`**: This stops both Fulcrum and Caddy, tearing down the Docker bridge network and dropping all active public connections.
2. **Never run generic `docker compose up -d` without `--no-deps`**: Compose might detect configuration changes and attempt to recreate the `caddy` service, risking Let's Encrypt rate-limiting and dropping TLS sessions.
3. **Never overwrite the VPS `/opt/fulcrum/Caddyfile` blindly**: If you customized your production Caddyfile on the VPS (e.g. gzip compression, custom headers, rate limits), an unreviewed overwrite would wipe those changes.
4. **Never expose Streamlit port 8501 to the public internet**: Port 8501 must remain private to the internal Docker network `fulcrum-net`. All external web traffic must enter through Caddy on port 443.

---

## 2. Current Architecture & Volume Bindings

```
[ Public Internet Users ]
            │ (Ports 80 / 443 HTTPS)
            ▼
┌────────────────────────────────────────────────────────┐
│  Hostinger KVM 2 VPS Host                              │
│                                                        │
│  ┌──────────────────────────────────────────────────┐  │
│  │  fulcrum-caddy (Caddy 2 Alpine)                  │  │
│  │  - Volumes: caddy_data (SSL Certs), caddy_config │  │
│  │  - Terminating TLS / Let's Encrypt               │  │
│  └──────────────────────┬───────────────────────────┘  │
│                         │ (Internal HTTP over fulcrum-net)
│                         ▼                              │
│  ┌──────────────────────────────────────────────────┐  │
│  │  fulcrum-app (Streamlit 1.32+ on Python 3.11)    │  │
│  │  - Internal Port: 8501 (Not exposed on host)     │  │
│  │  - Memory Limit: 5 GB                            │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
```

### Docker Volume Persistence
- `caddy_data`: Stores ACME account keys, Let's Encrypt certificates, and OCSP staples. **Preserving this volume avoids hitting Let's Encrypt 5-certificate-per-week rate limits.**
- `caddy_config`: Stores compiled Caddy JSON configurations.

---

## 3. Step-by-Step Safe Deployment Procedure (Caddy Untouched)

To rebuild and deploy the Streamlit application while Caddy remains continuously running:

### Step 3.1: Pre-Deploy Inspection
Verify Caddy's current operational health before making any changes:

```bash
# Check Caddy container status
docker inspect --format='{{.State.Status}}' fulcrum-caddy

# Check Caddy SSL log stream
docker logs --tail=30 fulcrum-caddy
```
*(Caddy should report `running` with active certificate management).*

### Step 3.2: Rebuild ONLY the Fulcrum Application Image
Build only the `fulcrum` service from the release package:

```bash
cd /opt/fulcrum
docker compose build fulcrum
```
*(This compiles the Python 3.11 image and downloads Chromium for Playwright. Caddy continues serving web requests uninterrupted).*

### Step 3.3: Recreate ONLY the Fulcrum Container
Use the `--no-deps` flag to instruct Docker Compose that dependent services (`caddy`) must NOT be touched or restarted:

```bash
docker compose up -d --no-deps --force-recreate fulcrum
```

### Step 3.4: Await Healthcheck Verification
Watch the Streamlit health status transition from `starting` to `healthy`:

```bash
docker inspect --format='{{json .State.Health.Status}}' fulcrum-app
```

Once healthy, Caddy immediately routes incoming HTTPS requests to the upgraded Streamlit container without any manual Caddy reload.

---

## 4. Verification & Diagnostics

### Test 1: External HTTPS Header Check
From your local terminal or VPS, check that Caddy returns HTTP 200 with valid TLS headers:

```bash
curl -I https://app.fulcrumindia.online
```
**Expected Output:**
```http
HTTP/2 200
server: Caddy
content-type: text/html; charset=utf-8
...
```

### Test 2: Internal Bridge Proxy Connectivity
Test that Caddy can reach Streamlit port 8501 over `fulcrum-net`:

```bash
docker exec -it fulcrum-caddy wget -qO- http://fulcrum:8501/_stcore/health
```
**Expected Output:**
```
ok
```

### Test 3: Caddy Resource Footprint Verification
Confirm Caddy remains lightweight and within budget:

```bash
docker stats --no-stream fulcrum-caddy
```
**Expected Memory Usage:** ~20 MB to 45 MB (well within the 300 MB system allocation).

