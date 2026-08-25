"""
Celery task for C2PA verification.
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
from app.modules.c2pa.verifier import verify_c2pa_manifest


@celery_app.task(name="c2pa.verify")
def task_verify_c2pa(media_item_id: str) -> dict:
    start_time = time.time()
    with get_sync_session() as session:
        item = session.execute(
            select(MediaItem).where(MediaItem.id == uuid.UUID(media_item_id))
        ).scalar_one_or_none()

        if not item:
            return {"status": "error", "message": "Media item not found"}

        file_path = str(Path(settings.UPLOAD_DIR) / item.stored_filename)
        status, prov_score, details, explanation = verify_c2pa_manifest(file_path)

        elapsed_ms = int((time.time() - start_time) * 1000)

        result = AnalysisResult(
            media_item_id=item.id,
            module_type=ModuleType.C2PA,
            provenance_score=prov_score,
            c2pa_status=status.value,
            details=details,
            explanation=explanation,
            confidence=0.90 if status.value != "no_credentials" else 0.50,
            processing_time_ms=elapsed_ms,
        )
        session.add(result)
        session.commit()

        return {
            "module": "c2pa",
            "status": status.value,
            "provenance_score": prov_score,
            "explanation": explanation,
        }
