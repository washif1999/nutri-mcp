#!/bin/sh
# entrypoint.sh — Container startup script
# SEED_ENABLED=true  → run seed.py on startup (default)
# SEED_ENABLED=false → skip seeding (for production reuse)

set -e

echo "[entrypoint] Ensuring db/ directory exists..."
mkdir -p /app/db

if [ "${SEED_ENABLED:-true}" = "true" ]; then
  echo "[entrypoint] SEED_ENABLED=true → Running database seeder..."
  python seed.py
else
  echo "[entrypoint] SEED_ENABLED=false → Skipping seed."
fi

echo "[entrypoint] Starting NutriMCP server..."
exec python server.py
