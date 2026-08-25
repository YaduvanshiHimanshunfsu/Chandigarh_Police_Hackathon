"""
Media Ingestion & Normalization Service.

Handles:
1. Cryptographic hashing (SHA-256)
2. Perceptual hashing (pHash & dHash)
3. Container/metadata normalization & JPEG quality estimation
4. Secure disk storage
5. Database record creation & first chain-of-custody ledger entry
"""

import hashlib
import io
import os
import uuid
from pathlib import Path
from PIL import Image, ExifTags
import imagehash

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.media_item import MediaItem, MediaType, AnalysisStatus
from app.models.ledger import LedgerAction
from app.services.ledger_service import append_ledger_entry


def estimate_jpeg_quality(image_bytes: bytes) -> int:
    """
    Estimate JPEG quality factor from image bytes.
    Useful for down-weighting DCT frequency analysis if the image has suffered
    severe recompression (e.g. repeated WhatsApp forwards).
    """
    try:
        img = Image.open(io.BytesIO(image_bytes))
        if hasattr(img, "quantization") and img.quantization:
            # Common heuristic: approximate quality from luminance quantization table
            q_tables = img.quantization
            if 0 in q_tables:
                avg_q = sum(q_tables[0]) / len(q_tables[0])
                # Lower quantization values mean higher quality (approx mapping)
                estimated_q = max(1, min(100, int(100 - (avg_q * 0.8))))
                return estimated_q
    except Exception:
        pass
    return 75  # Default reasonable assumption


def compute_perceptual_hashes(image_bytes: bytes) -> tuple[str | None, str | None]:
    """Compute pHash (perceptual DCT hash) and dHash (difference hash)."""
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        ph = str(imagehash.phash(img))
        dh = str(imagehash.dhash(img))
        return ph, dh
    except Exception:
        return None, None

def extract_exif(img: Image.Image) -> dict | None:
    """Extract basic EXIF metadata tags as a dict."""
    try:
        exif = img.getexif()
        if not exif:
            return None
        extracted = {}
        for tag_id, val in exif.items():
            tag_name = ExifTags.TAGS.get(tag_id, str(tag_id))
            if isinstance(val, (str, int, float)) and len(str(val)) < 200:
                extracted[tag_name] = str(val)
        return extracted
    except Exception:
        return None

def compute_clip_embedding(img: Image.Image) -> list[float] | None:
    """Compute 768-d CLIP embedding for nearest-neighbor search."""
    try:
        from app.modules.image_forensic.detector import get_or_load_models
        encoder, preprocess, _ = get_or_load_models()
        if encoder and preprocess:
            # We don't import _MODEL_CACHE directly to avoid circular imports, but get_or_load_models caches
            device = "cuda" if (torch.cuda.is_available()) else "cpu"
            tensor_img = preprocess(img).unsqueeze(0).to(device)
            with torch.no_grad():
                features = encoder.encode_image(tensor_img)
                return features.cpu().squeeze(0).numpy().tolist()
    except Exception as e:
        print(f"Failed to compute CLIP embedding: {e}")
    return None


async def ingest_media(
    db: AsyncSession,
    case_id: uuid.UUID,
    file_contents: bytes,
    original_filename: str,
    mime_type: str,
    media_type: MediaType,
) -> MediaItem:
    """
    Ingests uploaded media into storage, computes cryptographic/perceptual hashes,
    initializes DB models, and records the initial chain-of-custody ledger entry.
    """
    # 1. Compute Cryptographic SHA-256
    sha256_hash = hashlib.sha256(file_contents).hexdigest()

    # 2. Prepare Storage Directory
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_ext = Path(original_filename).suffix.lower() or ".bin"
    stored_filename = f"{sha256_hash}{file_ext}"
    target_path = upload_dir / stored_filename

    # Save to disk
    with open(target_path, "wb") as f:
        f.write(file_contents)

    phash_val, dhash_val = None, None
    width, height = None, None
    jpeg_q = None
    clip_embedding = None
    exif_data = None

    if media_type == MediaType.IMAGE:
        phash_val, dhash_val = compute_perceptual_hashes(file_contents)
        jpeg_q = estimate_jpeg_quality(file_contents)
        try:
            with Image.open(io.BytesIO(file_contents)) as img:
                width, height = img.size
                exif_data = extract_exif(img)
                clip_embedding = compute_clip_embedding(img.convert("RGB"))
        except Exception:
            pass

    # 4. Create MediaItem DB Record
    media_item = MediaItem(
        case_id=case_id,
        original_filename=original_filename,
        stored_filename=stored_filename,
        media_type=media_type,
        mime_type=mime_type,
        file_size_bytes=len(file_contents),
        sha256_hash=sha256_hash,
        phash=phash_val,
        dhash=dhash_val,
        width=width,
        height=height,
        jpeg_quality_estimate=jpeg_q,
        clip_embedding=clip_embedding,
        exif_data=exif_data,
        analysis_status=AnalysisStatus.PROCESSING,
    )
    db.add(media_item)
    await db.flush()
    await db.refresh(media_item)

    # 5. Append Chain-of-Custody Genesis/Ingestion Entry
    await append_ledger_entry(
        db=db,
        case_id=case_id,
        media_item_id=media_item.id,
        action=LedgerAction.INGEST,
        media_sha256=sha256_hash,
        actor="Investigator Intake API",
        details={
            "original_filename": original_filename,
            "file_size_bytes": len(file_contents),
            "mime_type": mime_type,
            "phash": phash_val,
            "jpeg_quality_estimate": jpeg_q,
        },
    )

    return media_item
