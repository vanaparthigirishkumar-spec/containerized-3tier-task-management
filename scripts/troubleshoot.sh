#!/usr/bin/env bash
#
# troubleshoot.sh — Display container status, recent logs and useful
# troubleshooting information.
#
# Usage: ./scripts/troubleshoot.sh
#
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "============================================================"
echo "  Troubleshooting - Containerized 3-Tier Application"
echo "============================================================"

cd "$PROJECT_DIR"

if ! command -v docker >/dev/null 2>&1; then
    echo "ERROR: docker is not installed or not in PATH." >&2
    exit 1
fi

echo ""
echo "--- 1. Docker version / environment ---"
docker version 2>/dev/null || true
docker compose version 2>/dev/null || true

echo ""
echo "--- 2. Container status ---"
docker compose ps 2>/dev/null || echo "  (no compose project or docker compose not available)"

echo ""
echo "--- 3. Docker networks ---"
docker network ls 2>/dev/null || true

echo ""
echo "--- 4. Backend recent logs (tail 50) ---"
docker compose logs --tail=50 backend 2>/dev/null || echo "  (backend logs unavailable)"

echo ""
echo "--- 5. Frontend recent logs (tail 50) ---"
docker compose logs --tail=50 frontend 2>/dev/null || echo "  (frontend logs unavailable)"

echo ""
echo "--- 6. Database recent logs (tail 50) ---"
docker compose logs --tail=50 db 2>/dev/null || echo "  (db logs unavailable)"

echo ""
echo "--- 7. HTTP endpoint checks ---"
echo -n "  Backend API via Nginx proxy: "
if curl -sf http://localhost:8088/api/health >/dev/null 2>&1; then
    echo "HEALTHY"
else
    echo "UNREACHABLE"
fi
echo -n "  Frontend (Nginx) : "
if curl -sf http://localhost:8088/ >/dev/null 2>&1; then
    echo "HEALTHY"
else
    echo "UNREACHABLE"
fi

echo ""
echo "--- 8. Common troubleshooting tips ---"
echo "  - Containers not running?  Run: ./scripts/start.sh"
echo "  - Backend failing?         Check: ./scripts/collect-logs.sh"
echo "  - Cannot reach frontend?   Confirm port 8088 is free."
echo "  - Database connection errors? Check DB_* env vars in .env match compose."
echo "  - Want a clean slate?      Run: ./scripts/cleanup.sh"
echo "                             (never deletes database data by default)"
echo ""
echo "============================================================"
echo "  Troubleshooting information displayed."
echo "============================================================"
