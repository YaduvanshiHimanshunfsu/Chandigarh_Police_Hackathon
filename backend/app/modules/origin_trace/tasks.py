"""
Celery task for Origin Tracing & Propagation Graph Building.
"""

import time
import uuid
from sqlalchemy import select
from app.core.celery_db import get_sync_session
from sqlalchemy.orm import Session

from app.core.celery_app import celery_app
from app.core.config import settings
from app.models.media_item import MediaItem
from app.models.analysis_result import AnalysisResult, ModuleType
from app.modules.origin_trace.retriever import retrieve_public_web_matches
from app.modules.origin_trace.graph_builder import build_propagation_graph

@celery_app.task(name="origin_trace.trace")
def task_trace_origin(media_item_id: str) -> dict:
    start_time = time.time()
    with get_sync_session() as session:
        item = session.execute(
            select(MediaItem).where(MediaItem.id == uuid.UUID(media_item_id))
        ).scalar_one_or_none()

        if not item:
            return {"status": "error", "message": "Media item not found"}

        # 1. Retrieve candidates
        # Note: In a real system, you might want to fetch from clip_embedding, we pass it here
        clip_embedding_list = None
        if hasattr(item, 'clip_embedding') and item.clip_embedding is not None:
            # clip_embedding is a pgvector Vector object, cast to list
            clip_embedding_list = list(item.clip_embedding)
            
        candidates = retrieve_public_web_matches(
            db=session,
            sha256=item.sha256_hash, 
            phash_hex=item.phash,
            clip_embedding=clip_embedding_list,
            media_item_id=media_item_id
        )

        # 2. Build propagation DAG
        graph, summary, explanation = build_propagation_graph(candidates)

        elapsed_ms = int((time.time() - start_time) * 1000)

        details = {
            "graph": graph,
            "summary": summary,
        }

        result = AnalysisResult(
            media_item_id=item.id,
            module_type=ModuleType.ORIGIN_TRACE,
            confidence=summary["earliest_source"]["source_confidence"] if summary.get("earliest_source") else 0.50,
            details=details,
            explanation=explanation,
            processing_time_ms=elapsed_ms,
        )
        session.add(result)
        session.commit()

        return {
            "module": "origin_trace",
            "earliest_source": summary.get("earliest_source"),
            "explanation": explanation,
        }
