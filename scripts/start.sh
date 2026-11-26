#!/usr/bin/env bash
#
# start.sh — Start the Containerized 3-Tier Application.
#
# - Copies .env.example to .env if .env is missing (developer convenience).
# - Builds (if needed) and starts frontend, backend, and PostgreSQL.
# - Prints useful URLs when complete.
#
# Usage: ./scripts/start.sh
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "============================================================"
echo "  Starting Containerized 3-Tier Application"
echo "============================================================"

cd "$PROJECT_DIR"

# --- Check that docker compose is available --------------------------------
if ! command -v docker >/dev/null 2>&1; then
    echo "ERROR: docker is not installed or not in PATH." >&2
    exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
    echo "ERROR: docker compose is not available." >&2
    exit 1
fi

# --- Ensure an .env file exists --------------------------------------------
if [ ! -f .env ]; then
    echo "INFO: .env not found. Creating one from .env.example."
    echo "      Review .env before using this in production."
    cp .env.example .env
else
    echo "INFO: .env found. Using existing configuration."
fi

# --- Start services --------------------------------------------------------
echo "INFO: Building and starting services with docker compose..."
docker compose up -d --build

echo ""
echo "============================================================"
echo "  Application started successfully!"
echo "============================================================"
echo "  Frontend (Nginx):        http://localhost:8088"
echo "  Backend API (FastAPI):   http://localhost:8000/api"
echo "  API docs (Swagger UI):   http://localhost:8000/docs"
echo "  PostgreSQL:              localhost:5432 (inside compose network)"
echo ""
echo "  Run ./scripts/health-check.sh to verify all services."
echo "============================================================"
