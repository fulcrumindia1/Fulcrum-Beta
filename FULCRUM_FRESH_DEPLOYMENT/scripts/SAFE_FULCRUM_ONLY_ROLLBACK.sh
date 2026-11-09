#!/usr/bin/env bash
# ==============================================================================
# SAFE_FULCRUM_ONLY_ROLLBACK.sh
# Instant Rollback Script for Hostinger KVM 2 VPS
# ==============================================================================
# Invariant Guarantees:
# 1. Rolls back ONLY the 'fulcrum-app' container to the pre_deploy_backup image.
# 2. NEVER touches, restarts, or modifies Caddy or its SSL certificates.
# 3. NEVER touches or deletes /opt/fulcrum/.env.
# 4. Zero downtime for Caddy reverse proxy.
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

echo "=================================================================="
echo "  FULCRUM PRODUCTION SAFE ROLLBACK"
echo "  Target Directory: $PROJECT_DIR"
echo "  Timestamp:        $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo "=================================================================="

# Check if backup image exists
if ! docker image inspect fulcrum-app:pre_deploy_backup >/dev/null 2>&1; then
    echo "[FATAL] No rollback image 'fulcrum-app:pre_deploy_backup' found!"
    echo "        Listing available images:"
    docker images | grep fulcrum || true
    echo "        Please inspect logs to diagnose the issue before manual intervention."
    exit 1
fi

echo "[1/4] Found pre-deployment safety backup image."
BACKUP_IMAGE_ID=$(docker inspect --format='{{.Id}}' fulcrum-app:pre_deploy_backup)
echo "      Backup Image ID: $BACKUP_IMAGE_ID"

# Identify current image tag used by docker-compose
COMPOSE_IMAGE_NAME=$(docker compose images fulcrum --format '{{.Repository}}:{{.Tag}}' 2>/dev/null | head -n1 || echo "")
if [ -z "$COMPOSE_IMAGE_NAME" ] || [ "$COMPOSE_IMAGE_NAME" = ":" ]; then
    # Default compose tag pattern: <dirname>_fulcrum:latest or <dirname>-fulcrum:latest
    DIR_NAME=$(basename "$PROJECT_DIR" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]//g')
    COMPOSE_IMAGE_NAME="${DIR_NAME}_fulcrum:latest"
fi

echo "[2/4] Retagging pre_deploy_backup as $COMPOSE_IMAGE_NAME..."
docker tag fulcrum-app:pre_deploy_backup "$COMPOSE_IMAGE_NAME"

echo "[3/4] Recreating Fulcrum container from backup image (Caddy untouched)..."
docker compose up -d --no-deps --force-recreate fulcrum

echo "[4/4] Verifying rolled-back container health..."
MAX_WAIT_SECONDS=45
ELAPSED=0
HEALTHY=false

while [ $ELAPSED -lt $MAX_WAIT_SECONDS ]; do
    CONTAINER_HEALTH=$(docker inspect --format='{{json .State.Health.Status}}' fulcrum-app 2>/dev/null || echo '"starting"')
    echo "      [${ELAPSED}s / ${MAX_WAIT_SECONDS}s] Status: $CONTAINER_HEALTH"
    if [ "$CONTAINER_HEALTH" = '"healthy"' ]; then
        HEALTHY=true
        break
    fi
    sleep 3
    ELAPSED=$((ELAPSED + 3))
done

if [ "$HEALTHY" = true ]; then
    echo ""
    echo "=================================================================="
    echo "  [SUCCESS] ROLLBACK COMPLETED! FULCRUM RESTORED AND HEALTHY."
    echo "=================================================================="
    CADDY_STATUS=$(docker inspect --format='{{.State.Status}}' fulcrum-caddy 2>/dev/null || echo "not_found")
    echo "  Caddy Reverse Proxy Status: $CADDY_STATUS"
else
    echo "[-] [WARNING] Rolled-back container did not report healthy in $MAX_WAIT_SECONDS seconds."
    echo "[-] Container logs:"
    docker logs --tail=30 fulcrum-app
    exit 1
fi
