# FASTQ Analysis Pipeline - Setup & Deployment

## Project Structure

```
pipeline_stimulator/
├── main.py                  # Flask web app with upload/status/results endpoints
├── pipeline.py              # Core pipeline logic (FastQC, trimming, alignment)
├── worker/
│   └── celery_worker.py     # Celery task executor
├── tests/
│   └── test_basic.py        # Test suite
├── templates/
│   └── upload.html          # Web UI for file upload
├── docker-compose.yml       # Docker services (app, worker, redis)
├── Dockerfile               # Container with bioinformatics tools
├── requirements.txt         # Python dependencies
├── .gitignore              # Git exclusions
└── .dockerignore           # Docker build exclusions
```

---

## Quick Start (Local Development)

### Prerequisites
- Python 3.10+
- Redis (for Celery)
- System tools: Java (for FastQC), samtools, cutadapt (optional)

### Setup

```bash
# Clone or navigate to the project
cd pipeline_stimulator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Redis (in a separate terminal)
redis-server

# Start Celery worker (in a separate terminal)
celery -A worker.celery_worker.celery worker --loglevel=info

# Run Flask app
python main.py
```

> If Redis or Celery is not available, the app now falls back to synchronous processing so uploads can still complete immediately.

### Cleanup

```bash
./clean.sh
```

**Access the app:** http://localhost:5000 (or http://localhost:10000 with gunicorn)

---

## Vercel Deployment

This repository includes a Vercel configuration for static deployment of `index.html`.

- `vercel.json` defines the static site build.
- `.vercelignore` keeps local results and generated files out of the deployment.
- `VERCEL.md` explains how to connect the GitHub repository to Vercel for continuous deployment.

> Note: The current backend pipeline uses Flask, Celery, Redis, and bioinformatics tools, which cannot be fully hosted as a Vercel serverless deployment. Vercel is best used here for the front-end static site, while the pipeline backend should run on a separate Python server or container host.

---

## Docker Deployment

### 1. Build the Docker Image

```bash
docker build -t pipeline-simulator:latest .
```

**What this includes:**
- Python 3.10 base image
- FastQC v0.11.9 (quality assessment)
- Samtools (BAM/SAM file handling)
- Cutadapt (sequence trimming)
- Flask, Celery, Redis client

### 2. Run with Docker Compose (Recommended)

```bash
# Start all services (app, worker, redis)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Services started:**
- **app** → Flask API on port 10000
- **worker** → Celery task processor
- **redis** → Message broker and result backend on port 6379

**Access the UI:** http://localhost:10000

### 3. Manual Docker Run (Single Container Test)

```bash
# Run without Celery (testing only)
docker run -d \
  -p 10000:10000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/results:/app/results \
  --name pipeline-app \
  pipeline-simulator:latest

# Check logs
docker logs pipeline-app

# Stop
docker stop pipeline-app
docker rm pipeline-app
```

---

## API Endpoints

### 1. **GET /** 
Web UI for uploading FASTQ files

### 2. **POST /upload**
Upload a FASTQ file and start processing

**Request:**
```bash
curl -X POST -F "file=@sample.fastq.gz" http://localhost:10000/upload
```

**Response:**
```json
{
  "message": "Upload received",
  "task_id": "abc123def456",
  "status_url": "/status/abc123def456",
  "results_url": "/results/abc123def456"
}
```

### 3. **GET /status/<task_id>**
Check task processing status

**Response (Pending):**
```json
{"status": "pending"}
```

**Response (Success):**
```json
{
  "status": "success",
  "task_id": "abc123def456",
  "input_file": "sample.fastq.gz",
  "output_files": [
    "sample_fastqc.html",
    "sample_trimmed.fastq.gz",
    "sample_aligned.sam",
    "sample_aligned.bam"
  ],
  "result_directory": "results/abc123def456"
}
```

### 4. **GET /results/<task_id>**
List output files for a task

**Response:**
```json
{
  "task_id": "abc123def456",
  "files": ["sample_fastqc.html", "sample_trimmed.fastq.gz", ...],
  "download_urls": ["/download/abc123def456/sample_fastqc.html", ...]
}
```

### 5. **GET /download/<task_id>/<filename>**
Download a result file

```bash
curl -O http://localhost:10000/download/abc123def456/sample_fastqc.html
```

---

## Running Tests

### Local Tests
```bash
pytest -q
# Output: 2 passed
```

### Docker Tests
```bash
docker-compose exec app pytest -q
```

---

## Pipeline Workflow

### Input
- Upload `.fastq.gz` or `.fq.gz` file via web UI

### Processing Steps
1. **FastQC** - Quality assessment report (HTML)
2. **Trimming** - Quality/adapter trimming → `*_trimmed.fastq.gz`
3. **Alignment** - Sequence alignment → `*_aligned.sam`, `*_aligned.bam`

### Output
- `sample_fastqc.html` - Quality report
- `sample_trimmed.fastq.gz` - Trimmed reads
- `sample_aligned.sam` - SAM format alignment
- `sample_aligned.bam` - BAM format alignment

---

## Environment Variables

When using Docker Compose, these are set automatically:

```yaml
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

For custom Redis instance:
```bash
docker run -e CELERY_BROKER_URL=redis://custom-redis:6379/0 ...
```

---

## Troubleshooting

### "Connection refused" error
- Ensure Redis is running
- Check docker-compose services: `docker-compose ps`

### Task stuck in "PENDING"
- Check Celery worker: `docker-compose logs worker`
- Verify Celery and Redis are connected

### FastQC/Samtools not found
- The Docker image installs these automatically
- For local dev, install: `apt-get install fastqc samtools cutadapt`

### Upload size too large
- Increase timeout and worker settings in docker-compose.yml:
  ```yaml
  services:
    worker:
      environment:
        CELERYD_POOL: solo
        CELERYD_TIME_LIMIT: 3600
  ```

---

## Advanced: Building for Production

### Custom Dockerfile for optimization
```dockerfile
FROM pipeline-simulator:latest as builder
# Add custom logic, ML models, etc.
```

### Push to Docker Hub
```bash
docker tag pipeline-simulator:latest myusername/pipeline-simulator:latest
docker push myusername/pipeline-simulator:latest
```

### Kubernetes Deployment
See `k8s-deployment.yaml` (if available) for cloud deployment.

---

## Support & Debugging

### Enable debug mode
```bash
# In main.py
app.run(debug=True)
```

### Verbose Celery logging
```bash
celery -A worker.celery_worker.celery worker --loglevel=debug
```

### Check container health
```bash
docker-compose ps
docker stats
```

---

**For questions or issues, check logs or submit an issue.**
