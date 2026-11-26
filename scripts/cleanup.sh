#!/usr/bin/env bash
#
# cleanup.sh — Clean up project containers and resources safely.
#
# By default this ONLY removes containers, networks, and locally-built
# images. The PostgreSQL named volume (persistent data) is NEVER deleted
# by default.
#
# To delete the PostgreSQL volume too, pass --delete-volumes and confirm.
#
# Usage:
#   ./scripts/cleanup.sh                 # safe: keeps database data
#   ./scripts/cleanup.sh --delete-volumes # deletes everything incl. volume
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

PROJECT_NAME="$(basename "$PROJECT_DIR")"
POSTGRES_VOLUME="${PROJECT_NAME}_postgres_data"

DELETE_VOLUMES=0

for arg in "$@"; do
    case "$arg" in
        --delete-volumes) DELETE_VOLUMES=1 ;;
        -h|--help)
            echo "Usage: $0 [--delete-volumes]"
            echo ""
            echo "  (default) Stop and remove containers, networks, and local images."
            echo "            The PostgreSQL named volume is preserved."
            echo ""
            echo "  --delete-volumes  Also delete the PostgreSQL data volume."
            echo "                    Requires explicit confirmation. Data loss!"
            exit 0
            ;;
        *)
            echo "WARNING: unknown argument '$arg' ignored."
            ;;
    esac
done

echo "============================================================"
echo "  Cleanup - Containerized 3-Tier Application"
echo "============================================================"

cd "$PROJECT_DIR"

if ! command -v docker >/dev/null 2>&1; then
    echo "ERROR: docker is not installed or not in PATH." >&2
    exit 1
fi

echo "INFO: This will stop and remove:"
echo "      - containers (frontend, backend, db)"
echo "      - the app-network bridge network"
echo "      - locally built images for this project"
echo ""
echo "  Persistent PostgreSQL data (named volume: $POSTGRES_VOLUME)"
echo "  will NOT be deleted by default."
echo ""

# Handle volume deletion with explicit confirmation
if [ "$DELETE_VOLUMES" -eq 1 ]; then
    echo "!!! WARNING !!!"
    echo "  --delete-volumes was provided. The PostgreSQL data volume will be"
    echo "  DELETED. All stored tasks will be LOST FOREVER. This cannot be undone."
    echo ""
    read -p "Type 'yes' to confirm volume deletion: " confirm
    echo ""
    if [ "$confirm" != "yes" ]; then
        echo "INFO: Volume deletion cancelled by user. Continuing without volume removal."
        DELETE_VOLUMES=0
    fi
fi

# Stop and remove containers, networks, and local images
echo "INFO: Running 'docker compose down --rmi local --remove-orphans' ..."
docker compose down --rmi local --remove-orphans

# Optionally delete the named volume
if [ "$DELETE_VOLUMES" -eq 1 ]; then
    echo "INFO: Deleting PostgreSQL data volume: $POSTGRES_VOLUME"
    if docker volume rm "$POSTGRES_VOLUME" 2>/dev/null; then
        echo "  [OK] Volume deleted."
    else
        echo "  [WARN] Volume not found or could not be removed (may already be gone)."
    fi
fi

echo ""
echo "============================================================"
echo "  Cleanup complete."
echo "============================================================"
if [ "$DELETE_VOLUMES" -eq 1 ]; then
    echo "  The PostgreSQL data volume was deleted."
else
    echo "  Persistent PostgreSQL data was PRESERVED."
fi
echo "============================================================"
