#!/bin/bash
# Stop and clean up the FASTQ Analysis Pipeline

echo "Stopping FASTQ Analysis Pipeline..."
docker compose down

echo ""
echo "✅ Services stopped and cleaned up"
