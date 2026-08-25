"""
Celery task for Video Forensic Analysis (Spatial + Temporal + AV Sync).
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
from app.modules.video_forensic.temporal import analyze_video_temporal_consistency
from app.modules.video_forensic.av_sync import analyze_av_synchronization


@celery_app.task(name="video_forensic.analyze")
def task_analyze_video(media_item_id: str) -> dict:
    start_time = time.time()
    with get_sync_session() as session:
        item = session.execute(
            select(MediaItem).where(MediaItem.id == uuid.UUID(media_item_id))
        ).scalar_one_or_none()

        if not item:
            return {"status": "error", "message": "Media item not found"}

        if item.media_type.value != "video":
            return {"status": "skipped", "message": "Item is not a video"}

        file_path = str(Path(settings.UPLOAD_DIR) / item.stored_filename)

        # 1. Temporal Biological Consistency
        temporal_score, temp_conf, temp_details, temp_exp = analyze_video_temporal_consistency(file_path)

        # 2. Audio-Visual Lip Sync Correlation
        av_score, av_conf, av_details, av_exp = analyze_av_synchronization(file_path)

        # Combine video scores
        fused_video_score = (temporal_score * 0.6 + av_score * 0.4)
        overall_conf = (temp_conf + av_conf) / 2.0

        elapsed_ms = int((time.time() - start_time) * 1000)

        combined_details = {
            "temporal_analysis": temp_details,
            "av_sync_analysis": av_details,
            "fused_video_score": round(fused_video_score, 3),
        }
        explanation = f"{temp_exp} | {av_exp}"

        result = AnalysisResult(
            media_item_id=item.id,
            module_type=ModuleType.VIDEO_FORENSIC,
            ai_generation_score=fused_video_score,
            manipulation_score=max(temporal_score, av_score),
            details=combined_details,
            explanation=explanation,
            confidence=overall_conf,
            processing_time_ms=elapsed_ms,
            model_version="TemporalFarneback+SyncNetCorrelation-v1.0",
        )
        session.add(result)
        session.commit()

        return {
            "module": "video_forensic",
            "score": fused_video_score,
            "confidence": overall_conf,
            "explanation": explanation,
        }
