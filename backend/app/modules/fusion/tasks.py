"""
Celery Task for the Master Evidence Fusion Engine.

Triggered as the callback chord after all parallel forensic analyzers complete.
Finalizes the MediaItem analysis status and writes the FUSION ledger entry.
"""

import time
import uuid
from sqlalchemy import select
from app.core.celery_db import get_sync_session
from sqlalchemy.orm import Session

from app.core.celery_app import celery_app
from app.core.config import settings
from app.models.media_item import MediaItem, AnalysisStatus
from app.models.analysis_result import AnalysisResult, ModuleType
from app.models.ledger import LedgerAction
from app.modules.fusion.engine import run_evidence_fusion_engine


@celery_app.task(name="fusion.run")
def task_run_evidence_fusion(results: list, media_item_id: str) -> dict:
    start_time = time.time()
    with get_sync_session() as session:
        item = session.execute(
            select(MediaItem).where(MediaItem.id == uuid.UUID(media_item_id))
        ).scalar_one_or_none()

        if not item:
            return {"status": "error", "message": "Media item not found"}

        # Fetch all module results
        res_query = session.execute(
            select(AnalysisResult).where(AnalysisResult.media_item_id == item.id)
        )
        module_results = res_query.scalars().all()

        ai_score, manip_score, prov_score, details, explanation = run_evidence_fusion_engine(module_results)

        elapsed_ms = int((time.time() - start_time) * 1000)

        fusion_entry = AnalysisResult(
            media_item_id=item.id,
            module_type=ModuleType.FUSION,
            ai_generation_score=ai_score,
            manipulation_score=manip_score,
            provenance_score=prov_score,
            confidence=1.0 - (details.get("dempster_shafer_mass", {}).get("m_uncertain", 0.15)),
            details=details,
            explanation=explanation,
            processing_time_ms=elapsed_ms,
            model_version="DempsterShafer-PlattCalibrated-v1.0",
        )
        session.add(fusion_entry)

        # Mark MediaItem as COMPLETED
        item.analysis_status = AnalysisStatus.COMPLETED

        session.commit()

        return {
            "status": "completed",
            "fused_ai_score": ai_score,
            "verdict": details.get("verdict"),
            "explanation": explanation,
        }
