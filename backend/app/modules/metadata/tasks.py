"""
Celery task for Metadata & EXIF consistency check.
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
from app.modules.metadata.exif_check import check_metadata_consistency


@celery_app.task(name="metadata.check")
def task_check_metadata(media_item_id: str) -> dict:
    start_time = time.time()
    with get_sync_session() as session:
        item = session.execute(
            select(MediaItem).where(MediaItem.id == uuid.UUID(media_item_id))
        ).scalar_one_or_none()

        if not item:
            return {"status": "error", "message": "Media item not found"}

        if item.media_type.value != "image":
            return {"status": "skipped", "message": "Metadata check currently supports images only"}

        file_path = str(Path(settings.UPLOAD_DIR) / item.stored_filename)

        tamper_score, conf, details, explanation = check_metadata_consistency(file_path)

        elapsed_ms = int((time.time() - start_time) * 1000)

        result = AnalysisResult(
            media_item_id=item.id,
            module_type=ModuleType.METADATA,
            manipulation_score=tamper_score,
            details=details,
            explanation=explanation,
            confidence=conf,
            processing_time_ms=elapsed_ms,
        )
        session.add(result)
        session.commit()

        return {
            "module": "metadata",
            "score": tamper_score,
            "confidence": conf,
            "explanation": explanation,
        }
