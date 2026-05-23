#!/bin/bash
# Build the Docker image for the FASTQ Analysis Pipeline

set -e

echo "🔨 Building Docker image..."
docker build -t pipeline-simulator:latest .

echo "✅ Build complete!"
echo ""
echo "To start the application, run:"
echo "  docker-compose up -d"
echo ""
echo "Access the web UI at: http://localhost:10000"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop:"
echo "  docker-compose down"
