import os
from celery import Celery
from pipeline import run_pipeline as pipeline_run

redis_url = os.environ.get("CELERY_BROKER_URL") or os.environ.get("REDIS_URL") or "memory://"
backend_url = os.environ.get("CELERY_RESULT_BACKEND") or redis_url

celery = Celery(
    "pipeline",
    broker=redis_url,
    backend=backend_url
)

@celery.task(bind=True)
def run_pipeline(self, upload_path):
    return pipeline_run(upload_path, self.request.id, update_state=self.update_state)
