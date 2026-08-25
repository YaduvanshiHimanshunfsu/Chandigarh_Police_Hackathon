"""
Two-Stage Origin & Near-Duplicate Media Retrieval Engine.

Pipeline:
1. Stage 1 (Fast Filter): Perceptual Hash (pHash/dHash) Hamming distance thresholding.
   - Resilient to recompression and modest scaling.
2. Stage 2 (Semantic Matching): CLIP ViT-L/14 embedding cosine similarity (FAISS / pgvector).
   - Survives extreme crops, color filters, mirroring/flips, and text overlays.
"""

from typing import List, Dict, Any, Optional
import numpy as np
import imagehash


def compute_phash_hamming_distance(hash1_hex: str, hash2_hex: str) -> int:
    """Calculates bitwise Hamming distance between two hex pHash strings."""
    try:
        h1 = imagehash.hex_to_hash(hash1_hex)
        h2 = imagehash.hex_to_hash(hash2_hex)
        return int(h1 - h2)
    except Exception:
        return 64


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Computes cosine similarity between two dense embedding vectors."""
    a = np.array(v1, dtype=np.float32)
    b = np.array(v2, dtype=np.float32)
    dot = np.dot(a, b)
    norm = (np.linalg.norm(a) * np.linalg.norm(b)) + 1e-7
    return float(dot / norm)


from app.modules.origin_trace.retriever_internal import search_internal_database
from app.modules.origin_trace.retriever_google import google_reverse_image_search, serpapi_visual_search

from sqlalchemy.orm import Session

def retrieve_public_web_matches(
    db: Session,
    sha256: str,
    phash_hex: Optional[str],
    clip_embedding: Optional[List[float]],
    media_item_id: str = None
) -> List[Dict[str, Any]]:
    """
    Retrieves matching media from both the internal pgvector database
    and external public sources via APIs.
    """
    candidates = []
    
    # Tier 1: Internal Database similarity search
    internal_matches = search_internal_database(
        db=db,
        phash_hex=phash_hex,
        clip_embedding=clip_embedding,
        media_item_id_to_exclude=media_item_id
    )
    candidates.extend(internal_matches)
    
    # Tier 2 & 3 would go here, fetching external results
    # google_matches = await google_reverse_image_search(image_url)
    # candidates.extend(google_matches)
    
    # Deduplicate by URL
    seen_urls = set()
    unique_candidates = []
    for c in candidates:
        if c["source_url"] not in seen_urls:
            seen_urls.add(c["source_url"])
            unique_candidates.append(c)
            
    return unique_candidates
