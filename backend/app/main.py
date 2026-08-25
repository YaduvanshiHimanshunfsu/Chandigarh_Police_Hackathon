"""
PratiBimb Praman — AI Media Forensic Provenance & Origin Intelligence Platform

Main FastAPI application entry point.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, Base
from app.api import cases, analysis, reports, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    # Startup: create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Seed demo cases if database is empty
    from app.core.database import async_session_factory
    from app.models.case import Case, CaseCategory, CaseStatus, CasePriority
    from sqlalchemy import select

    async with async_session_factory() as session:
        result = await session.execute(select(Case))
        existing = result.scalars().first()
        if not existing:
            demo_cases = [
                Case(
                    case_number="CHD-2026-F89A12",
                    ncrp_complaint_number="NCRP-2026-CHD-00941",
                    title="Altered Educational Marksheet Tampering (Font Discrepancy)",
                    description="Alleged grade manipulation on official state board certificate using font substitution.",
                    category=CaseCategory.EVIDENCE_TAMPERING,
                    status=CaseStatus.COMPLETED,
                    priority=CasePriority.HIGH,
                    officer_name="Inspector R. Sharma",
                    officer_badge="CHD-8821",
                ),
                Case(
                    case_number="CHD-2026-E42C99",
                    ncrp_complaint_number="NCRP-2026-CHD-00812",
                    title="Viral Social Media Impersonation Deepfake Video",
                    description="WhatsApp circulated synthetic video clip of government official with audio cloning.",
                    category=CaseCategory.DEEPFAKE,
                    status=CaseStatus.COMPLETED,
                    priority=CasePriority.CRITICAL,
                    officer_name="DSP A. Verma",
                    officer_badge="CHD-1044",
                ),
                Case(
                    case_number="CHD-2026-A11B77",
                    ncrp_complaint_number="NCRP-2026-CHD-01054",
                    title="Fraudulent Identity Document (Aadhaar / ID Card Forgery)",
                    description="Tampered identity card with digital photo replacement and metadata scrubbing.",
                    category=CaseCategory.CYBER_FRAUD,
                    status=CaseStatus.ANALYZING,
                    priority=CasePriority.MEDIUM,
                    officer_name="Sub-Inspector M. Kaur",
                    officer_badge="CHD-4912",
                ),
            ]
            session.add_all(demo_cases)
            await session.commit()

    yield
    # Shutdown: dispose engine
    await engine.dispose()


app = FastAPI(
    title="PratiBimb Praman",
    description=(
        "AI Media Forensic Provenance & Origin Intelligence Platform. "
        "Multi-signal evidence fusion with calibrated, uncertainty-aware "
        "origin confidence — engineered for Indian law enforcement."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow frontend on port 3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        settings.FRONTEND_URL,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register API Routers ──────────────────────────────
app.include_router(health.router, tags=["Health"])
app.include_router(cases.router, prefix="/api/v1/cases", tags=["Cases"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["Analysis"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"])
