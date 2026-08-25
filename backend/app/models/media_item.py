"""
MediaItem model — a single uploaded image, video, or audio file.
Stores SHA-256 hash, perceptual hash, CLIP embedding, and file metadata.
"""

import enum
import uuid
from datetime import datetime

from sqlalchemy import String, Text, Integer, Float, Enum, DateTime, ForeignKey, func, JSON, Uuid as UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

try:
    from pgvector.sqlalchemy import Vector
except ImportError:
    Vector = lambda dim: JSON

from app.core.database import Base


class MediaType(str, enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"


class AnalysisStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class MediaItem(Base):
    """
    A single piece of media uploaded for forensic analysis.
    Stores both cryptographic (SHA-256) and perceptual (pHash) hashes
    along with CLIP embeddings for similarity search.
    """

    __tablename__ = "media_items"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    case_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cases.id"), nullable=False, index=True
    )

    # ── File Metadata ─────────────────────────────────
    original_filename: Mapped[str] = mapped_column(String(500), nullable=False)
    stored_filename: Mapped[str] = mapped_column(String(500), nullable=False)
    media_type: Mapped[MediaType] = mapped_column(Enum(MediaType), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)

    # ── Cryptographic Integrity ───────────────────────
    sha256_hash: Mapped[str] = mapped_column(
        String(64), nullable=False, index=True
    )

    # ── Perceptual Hashing (for origin tracing) ───────
    phash: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    dhash: Mapped[str | None] = mapped_column(String(64), nullable=True)

    # ── CLIP Embedding (768-dim for ViT-L/14) ────────
    # Stored as pgvector for nearest-neighbor search
    clip_embedding = mapped_column(Vector(768), nullable=True)

    # ── Media Properties ──────────────────────────────
    width: Mapped[int | None] = mapped_column(Integer, nullable=True)
    height: Mapped[int | None] = mapped_column(Integer, nullable=True)
    duration_seconds: Mapped[float | None] = mapped_column(Float, nullable=True)
    fps: Mapped[float | None] = mapped_column(Float, nullable=True)
    # Estimated JPEG quality factor (for DCT branch weighting)
    jpeg_quality_estimate: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # ── Raw EXIF/Metadata ─────────────────────────────
    exif_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # ── Analysis Status ───────────────────────────────
    analysis_status: Mapped[AnalysisStatus] = mapped_column(
        Enum(AnalysisStatus), default=AnalysisStatus.PENDING
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # ── Relationships ─────────────────────────────────
    case = relationship("Case", back_populates="media_items")
    analysis_results = relationship(
        "AnalysisResult", back_populates="media_item", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<MediaItem {self.original_filename} [{self.analysis_status.value}]>"
