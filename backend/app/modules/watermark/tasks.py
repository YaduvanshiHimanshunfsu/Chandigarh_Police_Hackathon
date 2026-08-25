"""
Celery task for invisible watermark detection.
"""

import time
import uuid
from pathlib import Path
from sqlalchemy import select
from app.core.celery_db import get_sync_session
from sqlalchemy.orm import Session

from app.core.celery_app import celery_app
from app.core.config import settings
from app.models.media_item import MediaItem
from app.models.analysis_result import AnalysisResult, ModuleType
from app.modules.watermark.detector import detect_watermark_signatures


@celery_app.task(name="watermark.detect")
def task_detect_watermark(media_item_id: str) -> dict:
    start_time = time.time()
    with get_sync_session() as session:
        item = session.execute(
            select(MediaItem).where(MediaItem.id == uuid.UUID(media_item_id))
        ).scalar_one_or_none()

        if not item:
            return {"status": "error", "message": "Media item not found"}

        if item.media_type.value != "image":
            return {"status": "skipped", "message": "Watermark detection is image-only"}

        file_path = str(Path(settings.UPLOAD_DIR) / item.stored_filename)
        status, ai_prob, details, explanation = detect_watermark_signatures(file_path)

        elapsed_ms = int((time.time() - start_time) * 1000)

        result = AnalysisResult(
            media_item_id=item.id,
            module_type=ModuleType.WATERMARK,
            ai_generation_score=ai_prob if status.value == "detected" else 0.15,
            watermark_status=status.value,
            details=details,
            explanation=explanation,
            confidence=0.88 if status.value == "detected" else 0.60,
            processing_time_ms=elapsed_ms,
        )
        session.add(result)
        session.commit()

        return {
            "module": "watermark",
            "status": status.value,
            "ai_score": ai_prob,
            "explanation": explanation,
        }
