"""
Reports API — generates forensic reports and BSA §63(4) certificates.
"""

import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.case import Case
from app.models.media_item import MediaItem
from app.models.analysis_result import AnalysisResult, ModuleType
from app.services.report_generator import generate_forensic_report, generate_bsa_certificate
from app.services.ncrp_export import generate_ncrp_json

router = APIRouter()


class ReportRequest(BaseModel):
    media_item_id: uuid.UUID
    report_type: str = "full"  # "full", "bsa_certificate", "ncrp_json"
    officer_name: str = ""
    officer_designation: str = ""


@router.post("/generate")
async def generate_report(
    request: ReportRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Generate a forensic report or BSA §63(4) certificate.

    Report types:
    - "full": Complete forensic analysis report (PDF)
    - "bsa_certificate": BSA Section 63(4) dual-certification certificate (PDF)
    - "ncrp_json": NCRP-compatible I4C evidence package (JSON)
    """
    # Fetch media item with all analysis results
    result = await db.execute(
        select(MediaItem)
        .options(selectinload(MediaItem.analysis_results))
        .where(MediaItem.id == request.media_item_id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Media item not found")

    # Fetch parent case
    case_result = await db.execute(select(Case).where(Case.id == item.case_id))
    case = case_result.scalar_one_or_none()

    # Separate fusion result from individual module results
    fusion_result = next(
        (r for r in item.analysis_results if r.module_type == ModuleType.FUSION),
        None,
    )
    module_results = [r for r in item.analysis_results if r.module_type != ModuleType.FUSION]

    if request.report_type == "full":
        report_path = await generate_forensic_report(
            media_item=item,
            analysis_results=item.analysis_results,
            fusion_result=fusion_result,
            officer_name=request.officer_name,
        )
        return FileResponse(
            report_path,
            media_type="application/pdf",
            filename=f"forensic_report_{item.sha256_hash[:16]}.pdf",
        )

    elif request.report_type == "bsa_certificate":
        cert_path = await generate_bsa_certificate(
            media_item=item,
            fusion_result=fusion_result,
            officer_name=request.officer_name,
            officer_designation=request.officer_designation,
        )
        return FileResponse(
            cert_path,
            media_type="application/pdf",
            filename=f"BSA_63_certificate_{item.sha256_hash[:16]}.pdf",
        )

    elif request.report_type == "ncrp_json":
        if not case:
            raise HTTPException(status_code=404, detail="Parent case not found")
        ncrp_data = generate_ncrp_json(
            case=case,
            media_item=item,
            fusion_result=fusion_result,
            analysis_results=module_results,
        )
        return JSONResponse(content=ncrp_data)

    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown report type: {request.report_type}. Use: full, bsa_certificate, ncrp_json",
        )

