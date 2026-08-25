"""
Demo Data Seeder — populates DB with 3 pre-analyzed showcase cases for hackathon demo.

Run once before the demo:
    cd backend
    python scripts/seed_demo_data.py

Each case has realistic fusion scores, evidence bullets, and MobileNetV2 triage results.
"""

import sys
import os
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

import asyncio
import uuid
from datetime import datetime, timezone, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.case import Case, CasePriority, CaseStatus
from app.models.media_item import MediaItem, MediaType, AnalysisStatus
from app.models.analysis_result import AnalysisResult, ModuleType
from app.models.ledger import LedgerEntry, LedgerAction


DEMO_CASES = [
    {
        "case": {
            "title": "Viral Deepfake of UT Administrator",
            "category": "deepfake",
            "priority": "high",
            "officer_name": "Inspector R. Sharma",
            "ncrp_complaint_number": "NCRP-2026-CHD-00419",
        },
        "media": {
            "original_filename": "ut_admin_viral.jpg",
            "stored_filename": "e3b0c44298fc1c149afbf_ut_admin.jpg",
            "media_type": MediaType.IMAGE,
            "mime_type": "image/jpeg",
            "file_size_bytes": 1_243_560,
            "sha256_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "phash": "f8c4e03b12a7d901",
            "jpeg_quality_estimate": 42,
            "width": 1080,
            "height": 720,
        },
        "results": [
            {
                "module_type": ModuleType.IMAGE_FORENSIC,
                "ai_generation_score": 0.928,
                "manipulation_score": 0.88,
                "confidence": 0.92,
                "explanation": "Visual/frequency anomalies indicate synthetic generation (93%). DCT spectral analysis shows diffusion-model characteristic spikes.",
                "model_version": "LNCLIP-DF-ViT-L14+DCT",
            },
            {
                "module_type": ModuleType.MOBILENET_TRIAGE,
                "ai_generation_score": 0.87,
                "confidence": 0.72,
                "explanation": "MobileNetV2 Triage: 87.0% tampered likelihood (fast CNN screen, 4.2ms). Full pipeline analysis recommended.",
                "model_version": "MobileNetV2-ONNX-Triage-v1",
                "details": {
                    "raw_logit": 1.9, "raw_sigmoid": 0.87, "calibrated_score": 0.87,
                    "inference_time_ms": 4.2, "inference_backend": "onnxruntime",
                },
            },
            {
                "module_type": ModuleType.WATERMARK,
                "ai_generation_score": 0.81,
                "watermark_status": "detected",
                "confidence": 0.88,
                "explanation": "Synthetic watermark probe correlation confirmed (SynthID/Tree-Ring pattern). Spike metric: 4.8 > threshold 4.2.",
            },
            {
                "module_type": ModuleType.C2PA,
                "ai_generation_score": None,
                "c2pa_status": "no_credentials",
                "confidence": 0.4,
                "explanation": "No JUMBF C2PA credentials found. Treated as neutral per Indian social-forward design rule.",
            },
            {
                "module_type": ModuleType.METADATA,
                "manipulation_score": 0.91,
                "confidence": 0.88,
                "explanation": "AI generation software parameter signatures confirmed in XMP metadata (ComfyUI / A1111 artifacts).",
            },
            {
                "module_type": ModuleType.LOCALIZATION,
                "manipulation_score": 0.82,
                "confidence": 0.78,
                "explanation": "Manipulation localized in 2 region(s): facial boundary and neck contour (14.8% surface area).",
                "details": {"suspicious_region_count": 2, "tampered_area_pct_total": 14.8},
            },
            {
                "module_type": ModuleType.ORIGIN_TRACE,
                "details": {
                    "summary": {
                        "earliest_source": {
                            "platform": "Telegram",
                            "account": "@t.me/political_forward_2026",
                            "timestamp": "2026-08-15T07:32:00Z",
                        },
                        "propagation_count": 17,
                        "platforms_observed": ["Telegram", "WhatsApp", "X (Twitter)"],
                    }
                },
                "explanation": "Earliest indexed source traced: Telegram (@t.me/political_forward_2026) at 2026-08-15T07:32:00Z. 17 derivative re-shares.",
            },
            {
                "module_type": ModuleType.FUSION,
                "ai_generation_score": 0.914,
                "manipulation_score": 0.877,
                "provenance_score": 0.40,
                "confidence": 0.91,
                "explanation": "Forensic Assessment: HIGHLY SUSPICIOUS (Likely AI-Generated / Manipulated). AI Generation Probability: 91.4% (95% CI: 84% – 95%). Uncertainty: 11.2%.",
                "details": {
                    "verdict": "HIGHLY SUSPICIOUS (Likely AI-Generated / Manipulated)",
                    "fused_ai_probability": 0.914,
                    "confidence_interval": "84% – 95%",
                    "uncertainty_band": "11.2% uncertainty",
                    "dempster_shafer_mass": {"m_real": 0.05, "m_fake": 0.87, "m_uncertain": 0.08},
                    "max_signal_conflict_K": 0.21,
                    "conflicts": [],
                    "c2pa_summary": "No C2PA Credentials",
                    "evidence_bullets": [
                        "✓ Visual/frequency anomalies indicate synthetic generation (93%).",
                        "✓ Synthetic watermark signature detected (SynthID/Tree-Ring probe).",
                        "✓ MobileNetV2 CNN triage: 87.0% tampered (fast Tier-0 screen).",
                        "✓ AI generation software parameter signatures confirmed in metadata.",
                        "✓ Earliest indexed source traced: Telegram at 2026-08-15.",
                        "• No C2PA credentials (neutral; typical of social forwards).",
                    ],
                    "origin_summary": {
                        "earliest_source": {
                            "platform": "Telegram",
                            "account": "@t.me/political_forward_2026",
                            "timestamp": "2026-08-15T07:32:00Z",
                        }
                    },
                },
            },
        ],
    },
    {
        "case": {
            "title": "Digital Arrest Scam — Fake Police Video",
            "category": "cyber_fraud",
            "priority": "critical",
            "officer_name": "Inspector K. Mehta",
            "ncrp_complaint_number": "NCRP-2026-CHD-00387",
        },
        "media": {
            "original_filename": "fake_police_arrest.mp4",
            "stored_filename": "a2b4f88c12ee9a4d_fake_police.mp4",
            "media_type": MediaType.VIDEO,
            "mime_type": "video/mp4",
            "file_size_bytes": 12_440_000,
            "sha256_hash": "a2b4f88c12ee9a4d11b3c29da8f51b6c7e4882f9d0a5331f2b7c8dfe4a91bc20",
            "phash": "3c4f8a12b7e09d11",
            "jpeg_quality_estimate": None,
            "width": 1280,
            "height": 720,
        },
        "results": [
            {
                "module_type": ModuleType.VIDEO_FORENSIC,
                "ai_generation_score": 0.72,
                "confidence": 0.78,
                "explanation": "Temporal/AV lip-sync desynchronization detected (r=0.18). Inter-frame optical flow variance exceeds physiological limits.",
            },
            {
                "module_type": ModuleType.C2PA,
                "c2pa_status": "broken_chain",
                "confidence": 0.1,
                "explanation": "C2PA manifest present but cryptographic signature is broken — evidence of tampering.",
            },
            {
                "module_type": ModuleType.FUSION,
                "ai_generation_score": 0.718,
                "manipulation_score": 0.695,
                "provenance_score": 0.10,
                "confidence": 0.79,
                "explanation": "Forensic Assessment: UNCERTAIN / SUSPICIOUS (Partial Synthetic Anomaly). AI Generation Probability: 71.8% (95% CI: 61% – 80%).",
                "details": {
                    "verdict": "UNCERTAIN / SUSPICIOUS (Partial Synthetic Anomaly)",
                    "fused_ai_probability": 0.718,
                    "confidence_interval": "61% – 80%",
                    "uncertainty_band": "18.5% uncertainty",
                    "max_signal_conflict_K": 0.35,
                    "conflicts": [],
                    "c2pa_summary": "Broken C2PA Chain (Tampered)",
                    "evidence_bullets": [
                        "✓ Temporal/AV lip-sync desynchronization detected (r=0.18).",
                        "⚠ C2PA manifest present but cryptographic signature broken (tampering).",
                    ],
                },
            },
        ],
    },
    {
        "case": {
            "title": "Authentic Press Conference — VERIFIED",
            "category": "misinformation",
            "priority": "low",
            "officer_name": "Sub-Inspector P. Kaur",
            "ncrp_complaint_number": None,
        },
        "media": {
            "original_filename": "press_conference_authentic.jpg",
            "stored_filename": "c9d1e22f3a5b7890_press_conf.jpg",
            "media_type": MediaType.IMAGE,
            "mime_type": "image/jpeg",
            "file_size_bytes": 875_340,
            "sha256_hash": "c9d1e22f3a5b789012345678901234567890abcdef1234567890abcdef123456",
            "phash": "7a8b9c0d1e2f3456",
            "jpeg_quality_estimate": 88,
            "width": 1920,
            "height": 1080,
        },
        "results": [
            {
                "module_type": ModuleType.IMAGE_FORENSIC,
                "ai_generation_score": 0.09,
                "manipulation_score": 0.08,
                "confidence": 0.91,
                "explanation": "Natural sensor noise and authentic frequency spectra preserved. Camera noise residual consistent across frame.",
            },
            {
                "module_type": ModuleType.MOBILENET_TRIAGE,
                "ai_generation_score": 0.11,
                "confidence": 0.65,
                "explanation": "MobileNetV2 Triage: 89.0% genuine likelihood (fast CNN screen, 3.8ms).",
                "model_version": "MobileNetV2-ONNX-Triage-v1",
                "details": {
                    "raw_logit": -2.1, "raw_sigmoid": 0.11, "calibrated_score": 0.11,
                    "inference_time_ms": 3.8, "inference_backend": "onnxruntime",
                },
            },
            {
                "module_type": ModuleType.C2PA,
                "c2pa_status": "valid_provenance",
                "provenance_score": 0.95,
                "confidence": 0.95,
                "explanation": "Valid C2PA provenance signature detected. Issuer: Chandigarh Police Media Cell.",
            },
            {
                "module_type": ModuleType.FUSION,
                "ai_generation_score": 0.082,
                "manipulation_score": 0.07,
                "provenance_score": 0.95,
                "confidence": 0.93,
                "explanation": "Forensic Assessment: AUTHENTIC (Consistent Natural Acquisition Indicators). AI Generation Probability: 8.2% (95% CI: 4% – 13%).",
                "details": {
                    "verdict": "AUTHENTIC (Consistent Natural Acquisition Indicators)",
                    "fused_ai_probability": 0.082,
                    "confidence_interval": "4% – 13%",
                    "uncertainty_band": "8.0% uncertainty",
                    "max_signal_conflict_K": 0.05,
                    "conflicts": [],
                    "c2pa_summary": "Valid C2PA Signature (Intact Chain)",
                    "evidence_bullets": [
                        "✓ Cryptographic C2PA provenance verified and intact.",
                        "✓ Natural sensor noise and authentic frequency spectra preserved.",
                        "✓ MobileNetV2 CNN triage: 89.0% genuine (fast Tier-0 screen).",
                    ],
                },
            },
        ],
    },
]


def seed():
    engine = create_engine(settings.DATABASE_URL_SYNC)

    with Session(engine) as session:
        print("Seeding demo cases...")
        for i, demo in enumerate(DEMO_CASES):
            case_id = uuid.uuid4()
            media_id = uuid.uuid4()

            # Create Case
            case = Case(
                id=case_id,
                case_number=f"CHD-2026-DEMO{i+1}",
                title=demo["case"]["title"],
                category=demo["case"]["category"],
                priority=demo["case"]["priority"],
                officer_name=demo["case"]["officer_name"],
                ncrp_complaint_number=demo["case"].get("ncrp_complaint_number"),
                status=CaseStatus.COMPLETED,
            )
            session.add(case)

            # Create MediaItem
            media = MediaItem(
                id=media_id,
                case_id=case_id,
                analysis_status=AnalysisStatus.COMPLETED,
                **demo["media"],
            )
            session.add(media)

            # Create AnalysisResults
            for res_data in demo["results"]:
                res = AnalysisResult(
                    media_item_id=media_id,
                    **res_data,
                )
                session.add(res)

            print(f"  [{i+1}] Created case: {demo['case']['title'][:50]}")

        session.commit()
        print("✓ Demo data seeded successfully.\n")
        print("Start the backend and visit http://localhost:3000 to see the cases.")


if __name__ == "__main__":
    seed()
