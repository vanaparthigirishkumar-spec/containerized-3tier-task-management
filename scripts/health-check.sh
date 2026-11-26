#!/usr/bin/env bash
#
# health-check.sh — Check container and API health.
#
# Reports docker compose container status and pings the backend /api/health
# endpoint and the frontend (Nginx) on localhost:8088.
#
# Usage: ./scripts/health-check.sh
#
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "============================================================"
echo "  Health Check - Containerized 3-Tier Application"
echo "============================================================"

cd "$PROJECT_DIR"

if ! command -v docker >/dev/null 2>&1; then
    echo "ERROR: docker is not installed or not in PATH." >&2
    exit 1
fi

# --- Container status ------------------------------------------------------
echo ""
echo "--- Container status ---"
docker compose ps

# --- Helper to check an HTTP endpoint -------------------------------------
check_endpoint() {
    local name="$1"
    local url="$2"
    if curl -sf "$url" >/dev/null 2>&1; then
        echo "  [OK]   $name: HEALTHY  ($url)"
    else
        echo "  [FAIL] $name: UNHEALTHY or not reachable ($url)"
    fi
}

# --- API health checks -----------------------------------------------------
# The backend only listens on the internal Docker network (port 8000 is not
# published to the host), so we reach it through the Nginx reverse proxy.
echo ""
echo "--- API health checks ---"
check_endpoint "Frontend (Nginx)" "http://localhost:8088/"
check_endpoint "Backend API via Nginx proxy" "http://localhost:8088/api/health"

echo ""
echo "============================================================"
echo "  Health check complete."
echo "============================================================"
