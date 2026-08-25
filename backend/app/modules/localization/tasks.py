"""
Celery task for Manipulation Localization Heatmap Generation.
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
from app.modules.localization.gradcam import generate_manipulation_heatmap


@celery_app.task(name="localization.analyze")
def task_localize_manipulation(media_item_id: str) -> dict:
    start_time = time.time()
    with get_sync_session() as session:
        item = session.execute(
            select(MediaItem).where(MediaItem.id == uuid.UUID(media_item_id))
        ).scalar_one_or_none()

        if not item:
            return {"status": "error", "message": "Media item not found"}

        if item.media_type.value != "image":
            return {"status": "skipped", "message": "Localization is image-only"}

        file_path = str(Path(settings.UPLOAD_DIR) / item.stored_filename)

        heatmap_path, manip_score, regions, details, explanation = generate_manipulation_heatmap(file_path)

        elapsed_ms = int((time.time() - start_time) * 1000)

        result = AnalysisResult(
            media_item_id=item.id,
            module_type=ModuleType.LOCALIZATION,
            manipulation_score=manip_score,
            heatmap_path=heatmap_path,
            details=details,
            explanation=explanation,
            confidence=0.85 if regions else 0.70,
            processing_time_ms=elapsed_ms,
            model_version="SRM-ELA-GradCAM++-v1.0",
        )
        session.add(result)
        session.commit()

        return {
            "module": "localization",
            "manipulation_score": manip_score,
            "region_count": len(regions),
            "explanation": explanation,
        }
