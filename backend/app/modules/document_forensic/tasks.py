"""
Celery task for Document Forensic Font/Text Consistency analysis.
Follows the same pattern as all other module tasks in this project.
"""

import time
import uuid
from pathlib import Path
from sqlalchemy import select

from app.core.celery_app import celery_app
from app.core.celery_db import get_sync_session
from app.core.config import settings
from app.models.media_item import MediaItem
from app.models.analysis_result import AnalysisResult, ModuleType
from app.modules.document_forensic.font_analysis import analyze_document_font_consistency


@celery_app.task(name="document_forensic.analyze")
def task_analyze_document(media_item_id: str) -> dict:
    """
    Celery task: Run font/text stroke consistency analysis on an image.

    Only meaningful for images. Gracefully skips non-text images (score=0).
    """
    start_time = time.time()
    with get_sync_session() as session:
        item = session.execute(
            select(MediaItem).where(MediaItem.id == uuid.UUID(media_item_id))
        ).scalar_one_or_none()

        if not item:
            return {"status": "error", "message": "Media item not found"}

        # Document forensic is image-only
        if item.media_type.value != "image":
            return {"status": "skipped", "message": "Document forensic supports images only"}

        file_path = str(Path(settings.UPLOAD_DIR) / item.stored_filename)

        manip_score, confidence, details, explanation = analyze_document_font_consistency(
            file_path
        )

        elapsed_ms = int((time.time() - start_time) * 1000)

        result = AnalysisResult(
            media_item_id=item.id,
            module_type=ModuleType.DOCUMENT_FORENSIC,
            manipulation_score=manip_score,
            confidence=confidence,
            details=details,
            explanation=explanation,
            processing_time_ms=elapsed_ms,
        )
        session.add(result)
        session.commit()

        return {
            "module": "document_forensic",
            "score": manip_score,
            "confidence": confidence,
            "explanation": explanation,
        }
