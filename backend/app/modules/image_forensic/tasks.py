"""
Celery task for Image Forensic Analysis.
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
from app.modules.image_forensic.detector import analyze_image_authenticity


@celery_app.task(name="image_forensic.analyze")
def task_analyze_image(media_item_id: str) -> dict:
    start_time = time.time()
    with get_sync_session() as session:
        item = session.execute(
            select(MediaItem).where(MediaItem.id == uuid.UUID(media_item_id))
        ).scalar_one_or_none()

        if not item:
            return {"status": "error", "message": "Media item not found"}

        if item.media_type.value != "image":
            # Video frames are handled in video_forensic
            return {"status": "skipped", "message": "Not a standalone image"}

        file_path = str(Path(settings.UPLOAD_DIR) / item.stored_filename)
        jpeg_q = item.jpeg_quality_estimate or 75

        ai_score, manip_score, details, explanation = analyze_image_authenticity(
            file_path, jpeg_quality_estimate=jpeg_q
        )

        elapsed_ms = int((time.time() - start_time) * 1000)

        result = AnalysisResult(
            media_item_id=item.id,
            module_type=ModuleType.IMAGE_FORENSIC,
            ai_generation_score=ai_score,
            manipulation_score=manip_score,
            details=details,
            explanation=explanation,
            confidence=0.92,
            processing_time_ms=elapsed_ms,
            model_version="LNCLIP-DF-ViT-L14+DCT",
        )
        session.add(result)
        session.commit()

        return {
            "module": "image_forensic",
            "ai_score": ai_score,
            "manipulation_score": manip_score,
            "explanation": explanation,
        }


@celery_app.task(name="image_forensic.mobilenet_triage")
def task_mobilenet_triage(media_item_id: str) -> dict:
    """Tier-0 fast triage via MobileNetV2-ONNX (~5ms)."""
    from app.modules.image_forensic.mobilenet_triage import run_mobilenet_triage

    start_time = time.time()
    with get_sync_session() as session:
        item = session.execute(
            select(MediaItem).where(MediaItem.id == uuid.UUID(media_item_id))
        ).scalar_one_or_none()

        if not item:
            return {"status": "error", "message": "Media item not found"}

        if item.media_type.value != "image":
            return {"status": "skipped", "message": "MobileNetV2 triage is image-only"}

        file_path = str(Path(settings.UPLOAD_DIR) / item.stored_filename)

        fake_prob, confidence, details, explanation = run_mobilenet_triage(file_path)

        elapsed_ms = int((time.time() - start_time) * 1000)

        result = AnalysisResult(
            media_item_id=item.id,
            module_type=ModuleType.MOBILENET_TRIAGE,
            ai_generation_score=fake_prob,
            confidence=confidence,
            details=details,
            explanation=explanation,
            processing_time_ms=elapsed_ms,
            model_version="MobileNetV2-ONNX-Triage-v1",
        )
        session.add(result)
        session.commit()

        return {
            "module": "mobilenet_triage",
            "fake_probability": fake_prob,
            "confidence": confidence,
            "inference_time_ms": details.get("inference_time_ms"),
            "explanation": explanation,
        }
