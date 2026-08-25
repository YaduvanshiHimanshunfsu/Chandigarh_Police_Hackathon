"""
Celery application configuration.
Each forensic analysis module runs as an independent Celery task.
"""

from celery import Celery

from app.core.config import settings

broker_url = settings.REDIS_URL
if broker_url.startswith("memory"):
    backend_url = "cache+memory://"
else:
    backend_url = settings.REDIS_URL

celery_app = Celery(
    "pratibimb_praman",
    broker=broker_url,
    backend=backend_url,
    include=[
        "app.modules.c2pa.tasks",
        "app.modules.watermark.tasks",
        "app.modules.image_forensic.tasks",
        "app.modules.video_forensic.tasks",
        "app.modules.localization.tasks",
        "app.modules.metadata.tasks",
        "app.modules.origin_trace.tasks",
        "app.modules.document_forensic.tasks",
        "app.modules.fusion.tasks",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    # Soft/hard time limits per task (seconds)
    task_soft_time_limit=300,
    task_time_limit=600,
)
