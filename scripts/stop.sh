#!/usr/bin/env bash
#
# stop.sh — Stop application services without deleting persistent data.
#
# Containers are stopped but NOT removed, and the PostgreSQL named volume
# is preserved, so no data is lost.
#
# Usage: ./scripts/stop.sh
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "============================================================"
echo "  Stopping Containerized 3-Tier Application"
echo "============================================================"

cd "$PROJECT_DIR"

if ! command -v docker >/dev/null 2>&1; then
    echo "ERROR: docker is not installed or not in PATH." >&2
    exit 1
fi

echo "INFO: Stopping services (containers are kept, data is preserved)..."
docker compose stop

echo ""
echo "============================================================"
echo "  Services stopped."
echo "============================================================"
echo "  Persistent PostgreSQL data (named volume) is PRESERVED."
echo "  To start again, run: ./scripts/start.sh"
echo "============================================================"
