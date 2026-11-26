#!/usr/bin/env bash
#
# restart.sh — Restart application services.
#
# Stops and starts containers in place. Persistent data is preserved.
#
# Usage: ./scripts/restart.sh
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "============================================================"
echo "  Restarting Containerized 3-Tier Application"
echo "============================================================"

cd "$PROJECT_DIR"

if ! command -v docker >/dev/null 2>&1; then
    echo "ERROR: docker is not installed or not in PATH." >&2
    exit 1
fi

echo "INFO: Restarting services..."
docker compose restart

echo ""
echo "============================================================"
echo "  Services restarted."
echo "============================================================"
echo "  Persistent PostgreSQL data (named volume) is PRESERVED."
echo "  Frontend: http://localhost:8088"
echo "============================================================"
