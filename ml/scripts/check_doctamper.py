import lmdb
import os
import pickle
from PIL import Image
import io

# Check one folder first
lmdb_path = r"A:\DocTamper Dataset\DocTamperV1-TrainingSet"

env = lmdb.open(lmdb_path, readonly=True, lock=False)

with env.begin() as txn:
    # Count total entries
    total = txn.stat()['entries']
    print(f"Total entries in database: {total}")
    
    # Look at first 3 entries to understand structure
    cursor = txn.cursor()
    for i, (key, value) in enumerate(cursor):
        print(f"\nEntry {i+1}:")
        print(f"  Key: {key.decode('utf-8', errors='ignore')}")
        print(f"  Value size: {len(value)} bytes")
        if i >= 2:
            break

env.close()