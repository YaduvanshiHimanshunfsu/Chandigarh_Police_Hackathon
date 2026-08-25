"""
Cases API — CRUD for forensic investigation cases.
"""

import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.case import Case, CaseCategory, CaseStatus, CasePriority

router = APIRouter()


# ── Schemas ───────────────────────────────────────────

class CaseCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: str | None = None
    category: CaseCategory = CaseCategory.DEEPFAKE
    priority: CasePriority = CasePriority.MEDIUM
    officer_name: str = Field(..., min_length=2, max_length=100)
    officer_badge: str | None = None
    ncrp_complaint_number: str | None = None


class CaseResponse(BaseModel):
    id: uuid.UUID
    case_number: str
    title: str
    description: str | None
    category: CaseCategory
    status: CaseStatus
    priority: CasePriority
    officer_name: str
    officer_badge: str | None
    ncrp_complaint_number: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CaseListResponse(BaseModel):
    cases: list[CaseResponse]
    total: int


# ── Helper ────────────────────────────────────────────

def generate_case_number() -> str:
    """Generate a human-readable case number: CHD-2026-XXXXX."""
    short_id = uuid.uuid4().hex[:6].upper()
    return f"CHD-2026-{short_id}"


# ── Endpoints ─────────────────────────────────────────

@router.post("/", response_model=CaseResponse, status_code=status.HTTP_201_CREATED)
async def create_case(data: CaseCreate, db: AsyncSession = Depends(get_db)):
    """Create a new forensic investigation case."""
    case = Case(
        case_number=generate_case_number(),
        title=data.title,
        description=data.description,
        category=data.category,
        priority=data.priority,
        officer_name=data.officer_name,
        officer_badge=data.officer_badge,
        ncrp_complaint_number=data.ncrp_complaint_number,
    )
    db.add(case)
    await db.commit()
    await db.refresh(case)
    return case


@router.get("/", response_model=CaseListResponse)
async def list_cases(
    status_filter: CaseStatus | None = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    """List all cases, optionally filtered by status."""
    query = select(Case).order_by(Case.created_at.desc())
    if status_filter:
        query = query.where(Case.status == status_filter)
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    cases = result.scalars().all()

    # Count total
    from sqlalchemy import func
    count_query = select(func.count(Case.id))
    if status_filter:
        count_query = count_query.where(Case.status == status_filter)
    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0

    return CaseListResponse(cases=cases, total=total)


@router.get("/{case_id}", response_model=CaseResponse)
async def get_case(case_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Get a single case by ID."""
    result = await db.execute(select(Case).where(Case.id == case_id))
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@router.patch("/{case_id}/status")
async def update_case_status(
    case_id: uuid.UUID,
    new_status: CaseStatus,
    db: AsyncSession = Depends(get_db),
):
    """Update a case's status."""
    result = await db.execute(select(Case).where(Case.id == case_id))
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    case.status = new_status
    await db.flush()
    return {"status": "updated", "new_status": new_status.value}
