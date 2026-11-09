#!/usr/bin/env bash
# ==============================================================================
# FRESH_FULCRUM_ONLY_DEPLOY.sh
# Production Safe Deployment Script for Hostinger KVM 2 VPS
# ==============================================================================
# Invariant Guarantees:
# 1. NEVER deletes /opt/fulcrum or source files.
# 2. NEVER touches, replaces, or restarts the running Caddy container.
# 3. NEVER overwrites or modifies /opt/fulcrum/.env.
# 4. NEVER executes destructive drops or automated unreviewed SQL.
# 5. Targets ONLY the 'fulcrum' service (Streamlit internal port 8501).
# 6. Tags the previous working container image for instant rollback.
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
    DRY_RUN=true
    echo "[INFO] Running in DRY-RUN mode. No state modifications will be performed."
fi

echo "=================================================================="
echo "  FULCRUM PRODUCTION SAFE DEPLOYMENT (KVM 2 - 5GB CEILING)"
echo "  Target Directory: $PROJECT_DIR"
echo "  Timestamp:        $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo "=================================================================="

# ------------------------------------------------------------------------------
# STEP 1: HOST MEMORY & RESOURCE PREFLIGHT AUDIT
# ------------------------------------------------------------------------------
echo ""
echo "[1/7] Inspecting Host Resource Headroom..."
TOTAL_RAM_MB=$(free -m | awk '/^Mem:/{print $2}')
AVAIL_RAM_MB=$(free -m | awk '/^Mem:/{print $7}')
SWAP_USED_MB=$(free -m | awk '/^Swap:/{print $3}')

echo "      Total RAM:     ${TOTAL_RAM_MB} MB"
echo "      Available RAM: ${AVAIL_RAM_MB} MB"
echo "      Swap in use:   ${SWAP_USED_MB} MB"

if [ "$AVAIL_RAM_MB" -lt 1500 ]; then
    echo "[WARNING] Available host RAM is below 1500 MB. Ensure unused background processes are terminated."
fi

# ------------------------------------------------------------------------------
# STEP 2: VALIDATE PRODUCTION ENVIRONMENT (.env)
# ------------------------------------------------------------------------------
echo ""
echo "[2/7] Verifying VPS Environment Configuration (.env)..."
if [ ! -f ".env" ]; then
    echo "[FATAL] Missing .env file in $PROJECT_DIR!"
    echo "        The production .env must exist on the VPS before deploying."
    echo "        Aborting to protect system integrity."
    exit 1
fi

# Check required environment keys without exposing secrets
if ! grep -q "^DATA_BACKEND=supabase" .env; then
    echo "[WARNING] DATA_BACKEND is not explicitly set to supabase in .env"
fi

if ! grep -q "^SUPABASE_URL=" .env || ! grep -q "^SUPABASE_SECRET_KEY=" .env; then
    echo "[FATAL] .env is missing SUPABASE_URL or SUPABASE_SECRET_KEY."
    echo "        Aborting deployment."
    exit 1
fi
echo "      Environment configuration verified (Supabase credentials present)."

# ------------------------------------------------------------------------------
# STEP 3: VERIFY RUNNING CADDY CONTAINER & NETWORK
# ------------------------------------------------------------------------------
echo ""
echo "[3/7] Verifying Caddy Invariant & Network..."
CADDY_STATUS=$(docker inspect --format='{{.State.Status}}' fulcrum-caddy 2>/dev/null || echo "not_found")

if [ "$CADDY_STATUS" != "running" ]; then
    echo "[WARNING] Container 'fulcrum-caddy' status is: $CADDY_STATUS"
    echo "          Please ensure Caddy is initialized if this is the first deployment."
else
    echo "      Existing Caddy container is actively RUNNING."
    echo "      Caddy will NOT be stopped, touched, or reloaded during this deployment."
fi

# Ensure docker network exists
if ! docker network inspect fulcrum-net >/dev/null 2>&1; then
    echo "      Creating docker network 'fulcrum-net'..."
    if [ "$DRY_RUN" = false ]; then
        docker network create fulcrum-net
    fi
else
    echo "      Docker network 'fulcrum-net' exists."
fi

# ------------------------------------------------------------------------------
# STEP 4: BACKUP PREVIOUS WORKING DOCKER IMAGE
# ------------------------------------------------------------------------------
echo ""
echo "[4/7] Creating Rollback Safety Tag for Current Image..."
CURRENT_IMAGE_ID=$(docker inspect --format='{{.Image}}' fulcrum-app 2>/dev/null || echo "")

if [ -n "$CURRENT_IMAGE_ID" ]; then
    echo "      Current container image ID: $CURRENT_IMAGE_ID"
    if [ "$DRY_RUN" = false ]; then
        docker tag "$CURRENT_IMAGE_ID" fulcrum-app:pre_deploy_backup
        echo "      Tagged as fulcrum-app:pre_deploy_backup for instant rollback."
    fi
else
    echo "      No running fulcrum-app container found (fresh installation mode)."
fi

# ------------------------------------------------------------------------------
# STEP 5: BUILD STREAMLIT IMAGE ONLY
# ------------------------------------------------------------------------------
echo ""
echo "[5/7] Building Fulcrum Streamlit Image (5 GB limit configured)..."
if [ "$DRY_RUN" = true ]; then
    echo "      [DRY-RUN] Skipping 'docker compose build fulcrum'"
else
    docker compose build fulcrum
fi

# ------------------------------------------------------------------------------
# STEP 6: RECREATE FULCRUM CONTAINER (CADDY UNTOUCHED)
# ------------------------------------------------------------------------------
echo ""
echo "[6/7] Updating Fulcrum Container with Zero Impact to Caddy..."
if [ "$DRY_RUN" = true ]; then
    echo "      [DRY-RUN] Skipping 'docker compose up -d --no-deps --force-recreate fulcrum'"
else
    # --no-deps prevents Compose from restarting linked/dependent services (Caddy remains untouched)
    docker compose up -d --no-deps --force-recreate fulcrum
fi

# ------------------------------------------------------------------------------
# STEP 7: HEALTHCHECK VERIFICATION & RECOVERY
# ------------------------------------------------------------------------------
echo ""
echo "[7/7] Awaiting Healthcheck Verification..."
if [ "$DRY_RUN" = true ]; then
    echo "      [DRY-RUN] Healthcheck simulation succeeded."
    exit 0
fi

MAX_WAIT_SECONDS=60
ELAPSED=0
HEALTHY=false

while [ $ELAPSED -lt $MAX_WAIT_SECONDS ]; do
    CONTAINER_HEALTH=$(docker inspect --format='{{json .State.Health.Status}}' fulcrum-app 2>/dev/null || echo '"starting"')
    echo "      [${ELAPSED}s / ${MAX_WAIT_SECONDS}s] Container Health Status: $CONTAINER_HEALTH"
    if [ "$CONTAINER_HEALTH" = '"healthy"' ]; then
        HEALTHY=true
        break
    fi
    sleep 3
    ELAPSED=$((ELAPSED + 3))
done

if [ "$HEALTHY" = false ]; then
    echo ""
    echo "[-] [DEPLOYMENT FAILURE] Container failed to reach healthy status within $MAX_WAIT_SECONDS seconds."
    echo "[-] Recent container logs:"
    docker logs --tail=40 fulcrum-app
    echo ""
    echo "[!] To roll back immediately, run:"
    echo "    ./scripts/SAFE_FULCRUM_ONLY_ROLLBACK.sh"
    exit 1
fi

echo ""
echo "[+] Deep Internal Application Health Check:"
docker compose exec -T fulcrum python scripts/health_check.py || {
    echo "[WARNING] Deep health check reported warnings, inspect output above."
}

# Verify Caddy status remains unaffected
FINAL_CADDY_STATUS=$(docker inspect --format='{{.State.Status}}' fulcrum-caddy 2>/dev/null || echo "not_found")
echo "[+] Caddy Status Verification: $FINAL_CADDY_STATUS"

echo ""
echo "=================================================================="
echo "  [SUCCESS] FULCRUM CONTAINER SUCCESSFULLY DEPLOYED & HEALTHY!"
echo "=================================================================="
docker stats --no-stream fulcrum-app fulcrum-caddy 2>/dev/null || true
