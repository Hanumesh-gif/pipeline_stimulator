# Backend Deployment

This project uses Flask, Celery, and Redis for the FASTQ pipeline. The frontend can be hosted on Vercel, but the backend must run on a Python-compatible host with Redis support.

## Recommended deployment approach

### Option 1: Deploy the backend on Render

1. Sign in to https://render.com and connect your GitHub repository.
2. Add the `render.yaml` file to the repository and commit it.
3. Render should detect the manifest and create resources automatically.
4. If needed, you can also create the following services manually:
   - **Web Service**:
     - Environment: `Docker`
     - Dockerfile: `Dockerfile`
     - Start Command: `gunicorn main:app --bind 0.0.0.0:$PORT`
   - **Worker Service**:
     - Environment: `Docker`
     - Dockerfile: `Dockerfile`
     - Start Command: `celery -A worker.celery_worker.celery worker --loglevel=info`
5. Add a managed Redis instance.
6. Set environment variables for both services:
   - `CELERY_BROKER_URL` = `redis://<REDIS_HOST>:<REDIS_PORT>/0`
   - `CELERY_RESULT_BACKEND` = `redis://<REDIS_HOST>:<REDIS_PORT>/0`

> You can use the Render manifest `render.yaml` to automate these resources.

### Option 2: Deploy the backend on Railway

1. Sign in to https://railway.app and import the repository.
2. Add a Redis plugin.
3. Create two services:
   - `web` service: `gunicorn main:app --bind 0.0.0.0:$PORT`
   - `worker` service: `celery -A worker.celery_worker.celery worker --loglevel=info`
4. Map `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND` to the Redis connection URL.

## Backend configuration

- `requirements.txt` contains the Python dependencies.
- `Dockerfile` installs FastQC, samtools, and other pipeline tools.
- `Procfile` defines the `web` and `worker` processes.
- `runtime.txt` pins Python 3.10.

## Frontend integration

After backend deployment, update `index.html`:

```js
const API_BASE_URL = "https://<YOUR_BACKEND_URL>";
```

Then redeploy the frontend on Vercel.

## Notes

- The frontend on Vercel will call the backend service for `/upload`, `/status`, `/results`, and `/download`.
- The backend must be reachable via HTTPS to avoid mixed content issues.
