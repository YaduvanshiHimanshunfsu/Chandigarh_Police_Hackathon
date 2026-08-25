"""
Analysis Pipeline Orchestration Service.

Uses Celery Chords/Groups to run all forensic modules in parallel,
and upon completion, automatically triggers the Evidence Fusion Engine.
"""

import logging
import uuid
from celery import chord, group
from sqlalchemy import select

from app.core.celery_app import celery_app
from app.core.celery_db import get_sync_session
from app.models.media_item import MediaItem, AnalysisStatus

logger = logging.getLogger(__name__)


@celery_app.task(name="pipeline.on_error")
def task_handle_pipeline_failure(request, exc, traceback, media_item_id: str):
    """Fallback handler to mark media item as failed if pipeline crashes."""
    logger.error(f"Pipeline failed for {media_item_id}: {exc}")
    try:
        with get_sync_session() as session:
            item = session.execute(
                select(MediaItem).where(MediaItem.id == uuid.UUID(media_item_id))
            ).scalar_one_or_none()
            if item:
                item.analysis_status = AnalysisStatus.FAILED
                session.commit()
    except Exception as e:
        logger.error(f"Failed to update status on error: {e}")

def trigger_analysis_pipeline(media_item_id: str) -> None:
    """
    Launches asynchronous forensic analysis across all available analyzers.
    When all analyzers finish, the Fusion Engine task is automatically invoked.
    """
    try:
        # Import celery task signatures
        from app.modules.c2pa.tasks import task_verify_c2pa
        from app.modules.watermark.tasks import task_detect_watermark
        from app.modules.image_forensic.tasks import task_analyze_image, task_mobilenet_triage
        from app.modules.video_forensic.tasks import task_analyze_video
        from app.modules.localization.tasks import task_localize_manipulation
        from app.modules.metadata.tasks import task_check_metadata
        from app.modules.origin_trace.tasks import task_trace_origin
        from app.modules.document_forensic.tasks import task_analyze_document
        from app.modules.fusion.tasks import task_run_evidence_fusion

        # Group parallel tasks (all run concurrently, fusion fires on completion)
        parallel_forensics = group(
            task_verify_c2pa.s(media_item_id),
            task_detect_watermark.s(media_item_id),
            task_analyze_image.s(media_item_id),
            task_mobilenet_triage.s(media_item_id),      # Tier-0 fast CNN triage (MobileNetV2 ONNX)
            task_analyze_video.s(media_item_id),
            task_localize_manipulation.s(media_item_id),
            task_check_metadata.s(media_item_id),
            task_trace_origin.s(media_item_id),
            task_analyze_document.s(media_item_id),      # Font/text consistency (ported from mobilenetV2)
        )

        # Chord: Run parallel group → then run fusion engine callback
        callback = task_run_evidence_fusion.s(media_item_id=media_item_id)
        callback.link_error(task_handle_pipeline_failure.s(media_item_id=media_item_id))
        
        workflow = chord(parallel_forensics)(callback)
        logger.info(f"Triggered analysis pipeline chord for media_item: {media_item_id}")
        return workflow

    except Exception as e:
        logger.warning(f"Celery dispatch unavailable ({e}); falling back to in-process direct execution...")
        try:
            from concurrent.futures import ThreadPoolExecutor
            
            from app.modules.c2pa.tasks import task_verify_c2pa
            from app.modules.watermark.tasks import task_detect_watermark
            from app.modules.image_forensic.tasks import task_analyze_image, task_mobilenet_triage
            from app.modules.video_forensic.tasks import task_analyze_video
            from app.modules.localization.tasks import task_localize_manipulation
            from app.modules.metadata.tasks import task_check_metadata
            from app.modules.origin_trace.tasks import task_trace_origin
            from app.modules.document_forensic.tasks import task_analyze_document
            from app.modules.fusion.tasks import task_run_evidence_fusion

            tasks_to_run = [
                task_verify_c2pa,
                task_detect_watermark,
                task_analyze_image,
                task_mobilenet_triage,
                task_analyze_video,
                task_localize_manipulation,
                task_check_metadata,
                task_trace_origin,
                task_analyze_document,
            ]

            # Execute all forensic analyzers
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = [executor.submit(t, media_item_id) for t in tasks_to_run]
                for f in futures:
                    try:
                        f.result()
                    except Exception as mod_err:
                        logger.error(f"Module task error: {mod_err}")

            # Run Evidence Fusion Engine
            task_run_evidence_fusion(media_item_id=media_item_id)
            logger.info(f"Direct in-process forensic analysis & fusion completed for {media_item_id}")
            return True
        except Exception as direct_err:
            logger.error(f"In-process direct analysis failed for {media_item_id}: {direct_err}")
            return None
