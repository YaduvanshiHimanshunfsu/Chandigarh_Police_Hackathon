"""
Case model — represents a forensic investigation case.
Links to NCRP complaint number for I4C integration.
"""

import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Text, Enum, DateTime, func, Uuid as UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class CaseCategory(str, enum.Enum):
    DEEPFAKE = "deepfake"
    IMPERSONATION = "impersonation"
    MISINFORMATION = "misinformation"
    CYBER_FRAUD = "cyber_fraud"
    EVIDENCE_TAMPERING = "evidence_tampering"
    OTHER = "other"


class CaseStatus(str, enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class CasePriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Case(Base):
    """
    A forensic investigation case created by an officer.
    Each case can contain multiple media items for analysis.
    """

    __tablename__ = "cases"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    # Human-readable case ID: CHD-2026-XXXXX
    case_number: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False, index=True
    )
    # Optional link to NCRP complaint for I4C integration
    ncrp_complaint_number: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[CaseCategory] = mapped_column(
        Enum(CaseCategory), default=CaseCategory.DEEPFAKE
    )
    status: Mapped[CaseStatus] = mapped_column(
        Enum(CaseStatus), default=CaseStatus.DRAFT
    )
    priority: Mapped[CasePriority] = mapped_column(
        Enum(CasePriority), default=CasePriority.MEDIUM
    )
    # Officer who created this case
    officer_name: Mapped[str] = mapped_column(String(100), nullable=False)
    officer_badge: Mapped[str | None] = mapped_column(String(50), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    media_items = relationship("MediaItem", back_populates="case", cascade="all, delete-orphan")
    ledger_entries = relationship("LedgerEntry", back_populates="case", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Case {self.case_number} [{self.status.value}]>"
