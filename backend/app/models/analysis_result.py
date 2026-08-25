"""
AnalysisResult model — stores output from each forensic analysis module.
Each module writes its results as a separate row, all linked to the same media item.
The fusion engine reads all module results and produces the final combined output.
"""

import enum
import uuid
from datetime import datetime

from sqlalchemy import String, Float, Enum, DateTime, ForeignKey, func, JSON, Uuid as UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ModuleType(str, enum.Enum):
    C2PA = "c2pa"
    WATERMARK = "watermark"
    IMAGE_FORENSIC = "image_forensic"
    MOBILENET_TRIAGE = "mobilenet_triage"
    VIDEO_FORENSIC = "video_forensic"
    LOCALIZATION = "localization"
    METADATA = "metadata"
    ORIGIN_TRACE = "origin_trace"
    DOCUMENT_FORENSIC = "document_forensic"  # Font/text consistency (ported from mobilenetV2)
    FUSION = "fusion"  # The combined/final result


class C2PAStatus(str, enum.Enum):
    VALID_PROVENANCE = "valid_provenance"
    BROKEN_CHAIN = "broken_chain"
    NO_CREDENTIALS = "no_credentials"
    UNSUPPORTED_FORMAT = "unsupported_format"


class WatermarkStatus(str, enum.Enum):
    DETECTED = "detected"
    NOT_DETECTED = "not_detected"
    VERIFICATION_FAILED = "verification_failed"


class AnalysisResult(Base):
    """
    Per-module forensic analysis result.

    Each forensic module (C2PA, watermark, image forensic, etc.) writes one
    AnalysisResult per media item. The fusion engine reads all results for a
    media item and produces the final combined AnalysisResult with module_type=FUSION.
    """

    __tablename__ = "analysis_results"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    media_item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("media_items.id"), nullable=False, index=True
    )
    module_type: Mapped[ModuleType] = mapped_column(
        Enum(ModuleType), nullable=False
    )

    # ── Scores (calibrated 0.0 – 1.0) ────────────────
    # Probability that the media is AI-generated
    ai_generation_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    # Probability that the media has been manipulated
    manipulation_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    # Provenance integrity (1.0 = fully verified chain)
    provenance_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    # Confidence in the module's own output (for fusion weighting)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)

    # ── Categorical Outputs ───────────────────────────
    c2pa_status: Mapped[str | None] = mapped_column(String(30), nullable=True)
    watermark_status: Mapped[str | None] = mapped_column(String(30), nullable=True)

    # ── Detailed Results (module-specific) ────────────
    # Flexible JSONB for module-specific outputs:
    # - Image forensic: {ensemble_votes, dct_weight, jpeg_quality, ...}
    # - Video forensic: {blink_rate, head_pose_jitter, lip_sync_score, face_quality, ...}
    # - Localization: {heatmap_path, suspicious_regions: [...], ...}
    # - Origin trace: {earliest_source, propagation_count, graph_edges: [...], ...}
    # - Fusion: {per_signal_weights, conflict_detected, dempster_shafer_mass, ...}
    details: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # ── Explainability ────────────────────────────────
    # Human-readable explanation for this module's finding
    explanation: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    # Path to Grad-CAM/heatmap image (if applicable)
    heatmap_path: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # ── Metadata ──────────────────────────────────────
    processing_time_ms: Mapped[int | None] = mapped_column(nullable=True)
    model_version: Mapped[str | None] = mapped_column(String(100), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # ── Relationships ─────────────────────────────────
    media_item = relationship("MediaItem", back_populates="analysis_results")

    def __repr__(self) -> str:
        return f"<AnalysisResult {self.module_type.value} score={self.ai_generation_score}>"
