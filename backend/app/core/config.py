"""
Application configuration — loaded from environment variables.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Global configuration loaded from env vars or .env file."""

    # ── Application ───────────────────────────────────
    APP_NAME: str = "PratiBimb Praman"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    SECRET_KEY: str = "CHANGE-ME-IN-PRODUCTION"
    API_KEY_REQUIRED: bool = False
    API_KEY: str = ""

    # ── Database Configuration (Defaults to SQLite for zero-config local run) ──
    DATABASE_URL: str = "sqlite+aiosqlite:///./pratibimb_local.db"
    DATABASE_URL_SYNC: str = "sqlite:///./pratibimb_local.db"

    # ── Redis / Celery (Defaults to in-memory broker for zero-config local run) ─
    REDIS_URL: str = "memory://localhost/"

    # ── File Storage ──────────────────────────────────
    UPLOAD_DIR: str = "./uploads"
    REPORTS_DIR: str = "./reports"
    MAX_UPLOAD_SIZE_MB: int = 500

    # ── Frontend ──────────────────────────────────────
    FRONTEND_URL: str = "http://localhost:3000"

    # ── External APIs (for origin tracing) ────────────
    GOOGLE_SEARCH_API_KEY: str = ""
    GOOGLE_SEARCH_ENGINE_ID: str = ""
    BING_SEARCH_API_KEY: str = ""
    SERPAPI_KEY: str = ""

    # ── ML Model Configuration ────────────────────────
    CLIP_MODEL_NAME: str = "ViT-L-14"
    CLIP_PRETRAINED: str = "openai"
    DEVICE: str = "cpu"  # Set to "cuda" on GPU machine
    BATCH_SIZE: int = 8
    FORENSIC_HEAD_CHECKPOINT: str = "./models/univfd_clip.pth"

    # ── Forensic Analysis ─────────────────────────────
    PHASH_THRESHOLD: int = 10        # Hamming distance for pHash near-duplicate
    CLIP_SIMILARITY_THRESHOLD: float = 0.85  # Cosine similarity for CLIP matching
    FACE_QUALITY_MIN_SIZE: int = 80  # Min face pixel dimension for temporal analysis
    JPEG_QUALITY_THRESHOLD: int = 50 # Below this, DCT branch is downweighted

    # ── MobileNetV2 Triage ────────────────────────────
    MOBILENET_ONNX_PATH: str = "./models/mobilenet_v2_triage.onnx"
    MOBILENET_ENABLED: bool = True
    MOBILENET_HIGH_CONFIDENCE_THRESHOLD: float = 0.98

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
