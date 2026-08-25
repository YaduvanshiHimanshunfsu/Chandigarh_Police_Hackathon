import pytest
from app.services.ledger_service import compute_entry_hash, GENESIS_HASH

def test_compute_entry_hash():
    prev_hash = GENESIS_HASH
    action = "INGEST"
    media_sha256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    timestamp = "2026-08-20T14:32:00Z"
    details = {"file_size_bytes": 1024}
    
    hash1 = compute_entry_hash(prev_hash, action, media_sha256, timestamp, details)
    hash2 = compute_entry_hash(prev_hash, action, media_sha256, timestamp, details)
    
    # Determinism
    assert hash1 == hash2
    
    # Tamper evidence
    hash3 = compute_entry_hash(prev_hash, action, media_sha256, timestamp, {"file_size_bytes": 1025})
    assert hash1 != hash3
