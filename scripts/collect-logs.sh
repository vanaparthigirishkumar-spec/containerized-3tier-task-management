#!/usr/bin/env bash
#
# collect-logs.sh — Save timestamped logs for all services.
#
# Collects logs for frontend, backend, and db into a timestamped folder,
# plus a snapshot of `docker compose ps`.
#
# Usage: ./scripts/collect-logs.sh
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "============================================================"
echo "  Collecting Logs - Containerized 3-Tier Application"
echo "============================================================"

cd "$PROJECT_DIR"

if ! command -v docker >/dev/null 2>&1; then
    echo "ERROR: docker is not installed or not in PATH." >&2
    exit 1
fi

TIMESTAMP="$(date +"%Y%m%d_%H%M%S")"
LOG_DIR="$PROJECT_DIR/logs_$TIMESTAMP"

mkdir -p "$LOG_DIR"

echo "INFO: Saving logs to $LOG_DIR ..."
echo ""

for svc in frontend backend db; do
    echo "  -> $svc logs"
    docker compose logs "$svc" > "$LOG_DIR/$svc.log" 2>&1 || {
        echo "     WARNING: could not collect logs for $svc"
    }
done

# Snapshot of container state
docker compose ps > "$LOG_DIR/ps.log" 2>&1 || true

echo ""
echo "============================================================"
echo "  Logs collected successfully."
echo "============================================================"
echo "  Location: $LOG_DIR"
echo "  Files:"
ls -1 "$LOG_DIR"
echo "============================================================"
