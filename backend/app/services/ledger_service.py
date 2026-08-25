"""
Ledger Service — creates hash-chained, append-only audit trail entries.

Each entry's hash includes the previous entry's hash (Merkle chain),
making any retroactive edit to the log cryptographically detectable.
This is the foundation of BSA §63(4) compliance.
"""

import hashlib
import json
from datetime import datetime, timezone

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ledger import LedgerEntry, LedgerAction


GENESIS_HASH = "0" * 64  # Genesis block prev_hash


def compute_entry_hash(
    prev_hash: str,
    action: str,
    media_sha256: str,
    timestamp: str,
    details: dict | None,
) -> str:
    """Compute SHA-256 hash for a ledger entry, chaining to previous hash."""
    payload = f"{prev_hash}|{action}|{media_sha256}|{timestamp}|{json.dumps(details or {}, sort_keys=True)}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


async def get_last_entry(db: AsyncSession, case_id) -> LedgerEntry | None:
    """Get the most recent ledger entry for a case."""
    result = await db.execute(
        select(LedgerEntry)
        .where(LedgerEntry.case_id == case_id)
        .order_by(LedgerEntry.sequence_number.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def append_ledger_entry(
    db: AsyncSession,
    case_id,
    action: LedgerAction,
    media_sha256: str = "",
    media_item_id=None,
    actor: str = "system",
    details: dict | None = None,
) -> LedgerEntry:
    """
    Append a new entry to the hash-chained ledger.

    The entry_hash is computed as:
        SHA256(prev_hash | action | media_sha256 | timestamp | details)

    This ensures:
    - Each entry is cryptographically linked to its predecessor
    - Any retroactive modification breaks the chain
    - The full history is tamper-evident
    """
    # Get the last entry to chain from
    last_entry = await get_last_entry(db, case_id)
    prev_hash = last_entry.entry_hash if last_entry else GENESIS_HASH
    sequence = (last_entry.sequence_number + 1) if last_entry else 1

    now = datetime.now(timezone.utc)
    timestamp_str = now.isoformat()

    entry_hash = compute_entry_hash(
        prev_hash=prev_hash,
        action=action.value,
        media_sha256=media_sha256,
        timestamp=timestamp_str,
        details=details,
    )

    entry = LedgerEntry(
        case_id=case_id,
        media_item_id=media_item_id,
        sequence_number=sequence,
        prev_hash=prev_hash,
        entry_hash=entry_hash,
        action=action,
        actor=actor,
        media_sha256=media_sha256,
        details=details,
        timestamp=now,
    )
    db.add(entry)
    await db.flush()
    return entry


async def verify_chain_integrity(db: AsyncSession, case_id) -> dict:
    """
    Walk the entire ledger chain for a case and verify all hashes.
    Returns verification result with any breaks detected.
    """
    result = await db.execute(
        select(LedgerEntry)
        .where(LedgerEntry.case_id == case_id)
        .order_by(LedgerEntry.sequence_number.asc())
    )
    entries = result.scalars().all()

    if not entries:
        return {"valid": True, "entries_checked": 0, "breaks": []}

    breaks = []
    expected_prev = GENESIS_HASH

    for entry in entries:
        # Check chain linkage
        if entry.prev_hash != expected_prev:
            breaks.append({
                "sequence": entry.sequence_number,
                "expected_prev": expected_prev,
                "actual_prev": entry.prev_hash,
                "type": "chain_break",
            })

        # Recompute and verify entry hash
        recomputed = compute_entry_hash(
            prev_hash=entry.prev_hash,
            action=entry.action.value,
            media_sha256=entry.media_sha256 or "",
            timestamp=entry.timestamp.isoformat(),
            details=entry.details,
        )
        if recomputed != entry.entry_hash:
            breaks.append({
                "sequence": entry.sequence_number,
                "expected_hash": recomputed,
                "actual_hash": entry.entry_hash,
                "type": "hash_mismatch",
            })

        expected_prev = entry.entry_hash

    return {
        "valid": len(breaks) == 0,
        "entries_checked": len(entries),
        "breaks": breaks,
    }
