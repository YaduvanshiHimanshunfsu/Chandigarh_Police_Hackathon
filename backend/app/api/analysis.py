"""
Analysis API — handles media upload, triggers forensic analysis pipeline,
and returns analysis results.
"""

import hashlib
import os
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.core.database import get_db
from app.models.case import Case, CaseStatus
from app.models.media_item import MediaItem, MediaType, AnalysisStatus
from app.models.analysis_result import AnalysisResult, ModuleType
from app.services.ingestion import ingest_media
from app.services.pipeline import trigger_analysis_pipeline

router = APIRouter()


# ── Schemas ───────────────────────────────────────────

class MediaUploadResponse(BaseModel):
    media_item_id: uuid.UUID
    sha256_hash: str
    original_filename: str
    media_type: str
    analysis_status: str
    message: str


class AnalysisResultResponse(BaseModel):
    module_type: str
    ai_generation_score: float | None
    manipulation_score: float | None
    provenance_score: float | None
    confidence: float | None
    c2pa_status: str | None
    watermark_status: str | None
    explanation: str | None
    heatmap_path: str | None
    details: dict | None
    processing_time_ms: int | None
    created_at: datetime

    class Config:
        from_attributes = True


class FullAnalysisResponse(BaseModel):
    media_item_id: uuid.UUID
    original_filename: str
    sha256_hash: str
    media_type: str
    analysis_status: str
    results: list[AnalysisResultResponse]
    fusion_summary: dict | None = None


# ── Endpoints ─────────────────────────────────────────

@router.post("/upload/{case_id}", response_model=MediaUploadResponse)
async def upload_media(
    case_id: uuid.UUID,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload a media file for forensic analysis.

    This endpoint:
    1. Validates the case exists
    2. Computes SHA-256 hash
    3. Stores the file
    4. Creates a MediaItem record
    5. Writes the first chain-of-custody ledger entry
    6. Triggers the parallel forensic analysis pipeline
    """
    # Validate case exists
    result = await db.execute(select(Case).where(Case.id == case_id))
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    # Validate file size
    contents = await file.read()
    if len(contents) > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Max size: {settings.MAX_UPLOAD_SIZE_MB} MB",
        )

    # Determine media type from MIME
    mime = file.content_type or "application/octet-stream"
    if mime.startswith("image/"):
        media_type = MediaType.IMAGE
        # Basic magic byte check for images (JPEG, PNG, WEBP)
        if not (contents.startswith(b"\xff\xd8\xff") or contents.startswith(b"\x89PNG\r\n\x1a\n") or contents[8:12] == b"WEBP"):
            raise HTTPException(status_code=400, detail="Invalid image file content")
    elif mime.startswith("video/"):
        media_type = MediaType.VIDEO
    elif mime.startswith("audio/"):
        media_type = MediaType.AUDIO
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported media type: {mime}. Supported: image/*, video/*, audio/*",
        )
        
    # Sanitize filename
    safe_filename = "".join(c for c in (file.filename or "unnamed") if c.isalnum() or c in " ._-")
    if not safe_filename:
        safe_filename = "unnamed.bin"

    # Ingest: hash, store, create records, write ledger entry
    media_item = await ingest_media(
        db=db,
        case_id=case_id,
        file_contents=contents,
        original_filename=safe_filename,
        mime_type=mime,
        media_type=media_type,
    )

    # Update case status
    case.status = CaseStatus.ANALYZING
    await db.commit()

    # Trigger parallel forensic analysis (Celery tasks)
    trigger_analysis_pipeline(str(media_item.id))

    return MediaUploadResponse(
        media_item_id=media_item.id,
        sha256_hash=media_item.sha256_hash,
        original_filename=media_item.original_filename,
        media_type=media_type.value,
        analysis_status=AnalysisStatus.PROCESSING.value,
        message="Media ingested successfully. Forensic analysis pipeline triggered.",
    )


@router.get("/status/{media_item_id}")
async def get_analysis_status(
    media_item_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Check the analysis status of a media item."""
    result = await db.execute(
        select(MediaItem).where(MediaItem.id == media_item_id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Media item not found")

    # Count completed modules
    results = await db.execute(
        select(AnalysisResult).where(AnalysisResult.media_item_id == media_item_id)
    )
    completed_modules = [r.module_type.value for r in results.scalars().all()]

    all_modules = [m.value for m in ModuleType if m != ModuleType.FUSION]
    pending_modules = [m for m in all_modules if m not in completed_modules]

    return {
        "media_item_id": str(media_item_id),
        "analysis_status": item.analysis_status.value,
        "completed_modules": completed_modules,
        "pending_modules": pending_modules,
        "progress_percent": round(
            len(completed_modules) / max(len(all_modules), 1) * 100
        ),
    }


@router.get("/results/{media_item_id}", response_model=FullAnalysisResponse)
async def get_analysis_results(
    media_item_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get all forensic analysis results for a media item."""
    result = await db.execute(
        select(MediaItem)
        .options(selectinload(MediaItem.analysis_results))
        .where(MediaItem.id == media_item_id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Media item not found")

    # Extract fusion summary if available
    fusion_result = next(
        (r for r in item.analysis_results if r.module_type == ModuleType.FUSION),
        None,
    )
    fusion_summary = fusion_result.details if fusion_result else None

    return FullAnalysisResponse(
        media_item_id=item.id,
        original_filename=item.original_filename,
        sha256_hash=item.sha256_hash,
        media_type=item.media_type.value,
        analysis_status=item.analysis_status.value,
        results=[
            AnalysisResultResponse.model_validate(r) for r in item.analysis_results
        ],
        fusion_summary=fusion_summary,
    )

@router.get("/case/{case_id}/media")
async def get_media_items_for_case(case_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Get all media items for a given case."""
    result = await db.execute(
        select(MediaItem).where(MediaItem.case_id == case_id)
    )
    items = result.scalars().all()
    return [
        {
            "id": str(m.id),
            "original_filename": m.original_filename,
            "media_type": m.media_type.value,
            "analysis_status": m.analysis_status.value
        }
        for m in items
    ]
