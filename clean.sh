#!/bin/bash
# Clean previously generated uploads, results, and Docker Compose state.

set -e

echo "🧹 Cleaning pipeline workspace..."

if [ -d "uploads" ]; then
  find uploads -mindepth 1 -maxdepth 1 -exec rm -rf {} +
fi

if [ -d "results" ]; then
  find results -mindepth 1 -maxdepth 1 -exec rm -rf {} +
fi

echo "Stopping Docker Compose services if running..."
docker compose down --volumes --remove-orphans || true

echo "✅ Clean complete."
