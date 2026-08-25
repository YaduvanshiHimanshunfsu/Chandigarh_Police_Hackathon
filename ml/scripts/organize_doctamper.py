import lmdb
import os
import numpy as np
from PIL import Image
import io
import shutil

# ── PATHS ──────────────────────────────────────
TRAIN_LMDB  = r"A:\DocTamper Dataset\DocTamperV1-TrainingSet"
TEST_LMDB   = r"A:\DocTamper Dataset\DocTamperV1-TestingSet"
SCD_LMDB    = r"A:\DocTamper Dataset\DocTamperV1-SCD"

OUTPUT_DIR  = r"K:\DOCUMENT\doctamper_organized"

# How many images to extract (start small to test)
# Change to None to extract ALL
MAX_TAMPERED = 36000   # we need balanced dataset
MAX_GENUINE  = 36000   # same number as tampered

# ── CREATE OUTPUT FOLDERS ───────────────────────
for split in ['train', 'validation', 'test']:
    for cls in ['genuine', 'tampered']:
        os.makedirs(f'{OUTPUT_DIR}/{split}/{cls}', exist_ok=True)

print("✅ Output folders created")

# ── STEP 1: Get all SCD keys (these are tampered) ──
print("\nReading SCD keys (tampered image list)...")
scd_env = lmdb.open(SCD_LMDB, readonly=True, lock=False)
tampered_keys = set()
with scd_env.begin() as txn:
    cursor = txn.cursor()
    for key, _ in cursor:
        tampered_keys.add(key.decode('utf-8'))
scd_env.close()
print(f"  Found {len(tampered_keys)} tampered image keys")

# ── STEP 2: Extract from TrainingSet ────────────
print("\nExtracting training images...")

train_env = lmdb.open(TRAIN_LMDB, readonly=True, lock=False)

tampered_extracted = 0
genuine_extracted  = 0

with train_env.begin() as txn:
    cursor = txn.cursor()
    for key, value in cursor:

        key_str = key.decode('utf-8')
        is_tampered = key_str in tampered_keys

        # Check limits
        if is_tampered and tampered_extracted >= MAX_TAMPERED:
            continue
        if not is_tampered and genuine_extracted >= MAX_GENUINE:
            continue
        if tampered_extracted >= MAX_TAMPERED and genuine_extracted >= MAX_GENUINE:
            break

        try:
            img = Image.open(io.BytesIO(value)).convert('RGB')

            if is_tampered:
                # 80% train, 10% val, 10% test
                idx = tampered_extracted
                if idx < MAX_TAMPERED * 0.8:
                    split = 'train'
                elif idx < MAX_TAMPERED * 0.9:
                    split = 'validation'
                else:
                    split = 'test'
                save_path = f'{OUTPUT_DIR}/{split}/tampered/{key_str}.jpg'
                tampered_extracted += 1
            else:
                idx = genuine_extracted
                if idx < MAX_GENUINE * 0.8:
                    split = 'train'
                elif idx < MAX_GENUINE * 0.9:
                    split = 'validation'
                else:
                    split = 'test'
                save_path = f'{OUTPUT_DIR}/{split}/genuine/{key_str}.jpg'
                genuine_extracted += 1

            img.save(save_path, 'JPEG', quality=95)

            total = tampered_extracted + genuine_extracted
            if total % 500 == 0:
                print(f"  Progress: {total} images "
                      f"(tampered={tampered_extracted}, "
                      f"genuine={genuine_extracted})")

        except Exception as e:
            print(f"  Error on {key_str}: {e}")

train_env.close()

# ── STEP 3: Final count ─────────────────────────
print("\n✅ EXTRACTION COMPLETE!")
print("="*50)
for split in ['train', 'validation', 'test']:
    for cls in ['genuine', 'tampered']:
        path = f'{OUTPUT_DIR}/{split}/{cls}'
        count = len(os.listdir(path))
        print(f"  {split}/{cls}: {count} images")