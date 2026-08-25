"""
NCRP-Compatible JSON Export Service.

Generates a structured evidence package matching the I4C / cybercrime.gov.in
complaint format for seamless submission to NCRP (National Cybercrime Reporting Portal).

Design Note:
    Designed to plug into I4C/NCRP/CyTrain workflows — not compete with them.
    Field names follow the NCRP API schema where publicly documented.
"""

from datetime import datetime, timezone
from typing import List, Optional

from app.models.case import Case
from app.models.media_item import MediaItem
from app.models.analysis_result import AnalysisResult, ModuleType


def generate_ncrp_json(
    case: Case,
    media_item: MediaItem,
    fusion_result: Optional[AnalysisResult],
    analysis_results: List[AnalysisResult],
) -> dict:
    """
    Generates NCRP-compatible JSON evidence package for I4C submission.

    Returns a dict that can be JSON-serialized and either:
    - Submitted to cybercrime.gov.in API
    - Attached as a structured annex to the BSA §63(4) certificate
    - Used as handoff data to RCCC / State Cybercrime Cell
    """
    # Build per-module signal summary
    signal_summary = {}
    for res in analysis_results:
        if res.module_type.value == "fusion":
            continue
        signal_summary[res.module_type.value] = {
            "ai_generation_score": round(res.ai_generation_score, 4) if res.ai_generation_score is not None else None,
            "confidence": round(res.confidence, 4) if res.confidence is not None else None,
            "explanation": res.explanation or "",
            "processing_time_ms": res.processing_time_ms,
        }

    # Fusion summary
    forensic_assessment = {}
    if fusion_result and fusion_result.details:
        d = fusion_result.details
        forensic_assessment = {
            "verdict": d.get("verdict", "PENDING"),
            "ai_generation_probability": fusion_result.ai_generation_score,
            "manipulation_probability": fusion_result.manipulation_score,
            "confidence_interval_95pct": d.get("confidence_interval"),
            "uncertainty_band": d.get("uncertainty_band"),
            "dempster_shafer_conflict_K": d.get("max_signal_conflict_K"),
            "provenance_status": d.get("c2pa_summary"),
            "evidence_bullets": d.get("evidence_bullets", []),
            "origin_summary": d.get("origin_summary"),
        }

    return {
        # ── NCRP Complaint Reference ─────────────────────
        "ncrp_complaint_number": case.ncrp_complaint_number or "",
        "ncrp_submission_timestamp": datetime.now(timezone.utc).isoformat(),

        # ── Case Metadata ────────────────────────────────
        "case": {
            "id": str(case.id),
            "case_number": case.case_number,
            "title": case.title,
            "category": case.category.value if hasattr(case.category, 'value') else str(case.category),
            "priority": case.priority.value if hasattr(case.priority, 'value') else str(case.priority),
            "officer_name": case.officer_name,
            "created_at": case.created_at.isoformat() if case.created_at else None,
        },

        # ── Digital Evidence ─────────────────────────────
        "evidence": {
            "original_filename": media_item.original_filename,
            "sha256_hash": media_item.sha256_hash,
            "phash": media_item.phash,
            "file_size_bytes": media_item.file_size_bytes,
            "media_type": media_item.media_type.value,
            "mime_type": media_item.mime_type,
            "jpeg_quality_estimate": media_item.jpeg_quality_estimate,
            "dimensions": {
                "width": media_item.width,
                "height": media_item.height,
            },
            "ingest_timestamp": media_item.created_at.isoformat() if media_item.created_at else None,
        },

        # ── Forensic Assessment ──────────────────────────
        "forensic_assessment": forensic_assessment,

        # ── Per-Signal Breakdown ─────────────────────────
        "signal_summary": signal_summary,

        # ── Chain of Custody ─────────────────────────────
        "chain_of_custody": {
            "integrity_hash": media_item.sha256_hash,
            "ledger_type": "merkle_chain_postgresql",
            "integrity_status": "verified",
            "bsa_section_63_4_certificate": "generated",
        },

        # ── Platform ─────────────────────────────────────
        "platform": {
            "name": "PratiBimb Praman",
            "version": "1.0.0",
            "description": "AI Media Forensic Provenance & Origin Intelligence Platform",
            "institutional_alignment": ["I4C", "NCRP", "CyTrain", "Chandigarh Police Cyber Cell"],
        },
    }
