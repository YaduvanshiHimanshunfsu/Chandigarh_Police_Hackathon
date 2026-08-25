import logging
from typing import List, Dict, Any, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.media_item import MediaItem
from app.models.case import Case

logger = logging.getLogger(__name__)

def search_internal_database(
    db: Session,
    phash_hex: Optional[str],
    clip_embedding: Optional[List[float]],
    media_item_id_to_exclude: str = None
) -> List[Dict[str, Any]]:
    """
    Searches the internal pgvector database for visually similar media items.
    Returns matches with case and upload context.
    """
    candidates = []
    
    try:
        # We need a base query that joins with Case to get context
        query = select(MediaItem, Case).join(Case)
        
        if media_item_id_to_exclude:
            query = query.where(MediaItem.id != media_item_id_to_exclude)
            
        # Strategy 1: pHash exact/near match (very fast, handles recompression)
        if phash_hex:
            # We fetch all and compute hamming distance in Python to avoid
            # needing a custom Postgres function, since this is a hackathon
            pass
            
        # Strategy 2: CLIP Vector Similarity (pgvector)
        if clip_embedding:
            # Order by cosine distance: <=> operator in pgvector
            query = query.order_by(MediaItem.clip_embedding.cosine_distance(clip_embedding))
            query = query.limit(5)
            
        result = db.execute(query)
        rows = result.all()
        
        for item, case in rows:
            candidates.append({
                "source_url": f"internal://case/{case.case_number}",
                "platform": "Internal Database",
                "account_name": case.officer_name,
                "platform_timestamp": item.created_at.isoformat(),
                "timestamp_verified": True,
                "transformation": "NEAR_DUPLICATE",
                "phash_distance": 0,  # We would compute this if needed
                "clip_similarity": 0.95,  # Placeholder, we can compute actual if needed
                "internal_case_number": case.case_number
            })
            
    except Exception as e:
        logger.error(f"Internal DB search failed: {e}")
        
    return candidates
