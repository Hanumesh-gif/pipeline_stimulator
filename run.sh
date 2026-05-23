#!/bin/bash
# Start the FASTQ Analysis Pipeline using Docker Compose

set -e

echo "🚀 Starting FASTQ Analysis Pipeline..."
echo ""

# Check if image exists
if ! docker image inspect pipeline-simulator:latest &> /dev/null; then
    echo "⚠️  Image not found. Building first..."
    docker build -t pipeline-simulator:latest .
    echo ""
fi

echo "Starting services with docker compose..."
docker compose up -d

echo ""
echo "✅ Services started!"
echo ""
echo "📊 Services status:"
docker compose ps
echo ""
echo "🌐 Web UI: http://localhost:10000"
echo "📋 Redis: localhost:6379"
echo ""
echo "📝 View logs:"
echo "  docker compose logs -f"
echo ""
echo "⛔ To stop:"
echo "  docker compose down"
