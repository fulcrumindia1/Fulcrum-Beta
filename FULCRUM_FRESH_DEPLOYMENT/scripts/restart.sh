#!/usr/bin/env bash
# ==============================================================================
# scripts/restart.sh — Safe Container Restart for Fulcrum India
# ==============================================================================
# Usage:
#   ./scripts/restart.sh          (Safe restart of fulcrum application only)
#   ./scripts/restart.sh caddy    (Restart caddy reverse proxy only)
#   ./scripts/restart.sh all      (Restart both fulcrum and caddy)
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

TARGET="${1:-fulcrum}"

if [ "$TARGET" = "all" ]; then
    echo "[*] Restarting both Fulcrum and Caddy services..."
    docker compose restart
elif [ "$TARGET" = "caddy" ]; then
    echo "[*] Restarting Caddy reverse proxy only..."
    docker compose restart caddy
else
    echo "[*] Restarting Fulcrum Streamlit container only (Caddy untouched)..."
    docker compose restart fulcrum
fi

echo "[*] Waiting for service to stabilize..."
sleep 4

docker compose ps
echo "[+] Service status updated. Run ./scripts/status.sh to check health."
