"""
Evidence Graph models — nodes and edges for origin tracing / propagation mapping.

Nodes = each located instance of the media (or derivative) found on the web.
Edges = inferred transformation between instances (crop, screenshot, re-encode, etc.).

Stored in Postgres adjacency tables (not Neo4j — faster to build under hackathon time).
"""

import enum
import uuid
from datetime import datetime

from sqlalchemy import String, Float, Integer, Enum, DateTime, ForeignKey, func, JSON, Uuid as UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class TransformationType(str, enum.Enum):
    EXACT_COPY = "exact_copy"
    REPOST = "repost"
    SCREENSHOT = "screenshot"
    CROP = "crop"
    RE_ENCODE = "re_encode"
    RE_UPLOAD = "re_upload"
    EDIT = "edit"
    COMPOSITE = "composite"
    UNKNOWN = "unknown"


class EvidenceNode(Base):
    """
    A single located instance of media found during origin tracing.
    Each node represents one occurrence of the media (or a derivative)
    found on the indexable web.
    """

    __tablename__ = "evidence_nodes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    media_item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("media_items.id"), nullable=False, index=True
    )

    # ── Source Information ────────────────────────────
    source_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    platform: Mapped[str | None] = mapped_column(String(100), nullable=True)
    account_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    # Self-reported timestamp from the platform
    platform_timestamp: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    # Whether the timestamp is independently verifiable (crypto-signed vs self-reported)
    timestamp_verified: Mapped[bool] = mapped_column(default=False)

    # ── Matching Metrics ──────────────────────────────
    sha256_match: Mapped[bool] = mapped_column(default=False)
    phash_distance: Mapped[int | None] = mapped_column(Integer, nullable=True)
    clip_similarity: Mapped[float | None] = mapped_column(Float, nullable=True)

    # ── Node Properties ───────────────────────────────
    # Is this node the earliest known source?
    is_earliest_known: Mapped[bool] = mapped_column(default=False)
    # C2PA status of this specific instance
    c2pa_status: Mapped[str | None] = mapped_column(String(30), nullable=True)
    # Additional metadata
    node_metadata: Mapped[dict | None] = mapped_column("metadata", JSON, nullable=True)

    discovered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class EvidenceEdge(Base):
    """
    A directed edge between two evidence nodes, representing an inferred
    transformation (crop, screenshot, re-encode, etc.) in the propagation graph.
    """

    __tablename__ = "evidence_edges"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    source_node_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("evidence_nodes.id"), nullable=False
    )
    target_node_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("evidence_nodes.id"), nullable=False
    )

    # ── Edge Properties ───────────────────────────────
    transformation_type: Mapped[TransformationType] = mapped_column(
        Enum(TransformationType), default=TransformationType.UNKNOWN
    )
    # Similarity score between source and target
    similarity_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    # Confidence that this edge/transformation is correctly inferred
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
