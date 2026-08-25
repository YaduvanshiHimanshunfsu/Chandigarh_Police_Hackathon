"""
LedgerEntry model — append-only, hash-chained chain-of-custody log.

Each entry's hash includes the previous entry's hash, forming a Merkle chain.
Any retroactive edit to the log is detectable by hash verification.
This is what makes the forensic report legally defensible under BSA §63.
"""

import enum
import uuid
from datetime import datetime

from sqlalchemy import String, Text, Enum, DateTime, ForeignKey, func, JSON, Uuid as UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class LedgerAction(str, enum.Enum):
    INGEST = "ingest"
    NORMALIZE = "normalize"
    ANALYSIS_START = "analysis_start"
    ANALYSIS_COMPLETE = "analysis_complete"
    C2PA_CHECK = "c2pa_check"
    WATERMARK_CHECK = "watermark_check"
    IMAGE_FORENSIC = "image_forensic"
    VIDEO_FORENSIC = "video_forensic"
    LOCALIZATION = "localization"
    METADATA_CHECK = "metadata_check"
    ORIGIN_TRACE = "origin_trace"
    FUSION = "fusion"
    REPORT_GENERATED = "report_generated"
    EXPORT = "export"


class LedgerEntry(Base):
    """
    Append-only, hash-chained audit log entry.

    Hash chain structure:
        entry_hash = SHA256(prev_hash + action + media_sha256 + timestamp + details)

    Verification: walk the chain from genesis, recompute each hash,
    compare against stored hash. Any mismatch = tampering detected.
    """

    __tablename__ = "ledger_entries"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    case_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cases.id"), nullable=False, index=True
    )
    media_item_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("media_items.id"), nullable=True
    )

    # ── Chain Links ───────────────────────────────────
    sequence_number: Mapped[int] = mapped_column(nullable=False)
    prev_hash: Mapped[str] = mapped_column(
        String(64), nullable=False, default="0" * 64  # Genesis block
    )
    entry_hash: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True
    )

    # ── Entry Content ─────────────────────────────────
    action: Mapped[LedgerAction] = mapped_column(Enum(LedgerAction), nullable=False)
    actor: Mapped[str] = mapped_column(
        String(100), nullable=False, default="system"
    )
    media_sha256: Mapped[str | None] = mapped_column(String(64), nullable=True)
    tool_version: Mapped[str] = mapped_column(
        String(50), nullable=False, default="PratiBimb v1.0.0"
    )
    details: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # ── Relationships ─────────────────────────────────
    case = relationship("Case", back_populates="ledger_entries")

    def __repr__(self) -> str:
        return f"<Ledger #{self.sequence_number} [{self.action.value}] hash={self.entry_hash[:12]}...>"
