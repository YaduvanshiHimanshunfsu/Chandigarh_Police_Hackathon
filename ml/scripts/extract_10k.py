import lmdb
import os
import io
import shutil
from PIL import Image

TRAIN_LMDB  = r"A:\DocTamper Dataset\DocTamperV1-TrainingSet"
SCD_LMDB    = r"A:\DocTamper Dataset\DocTamperV1-SCD"
OUTPUT_DIR  = r"K:\DOCUMENT\doctamper_10k"

MAX_TAMPERED = 10000
MAX_GENUINE  = 10000

# Create folders
for split in ['train', 'validation', 'test']:
    for cls in ['genuine', 'tampered']:
        os.makedirs(f'{OUTPUT_DIR}/{split}/{cls}', exist_ok=True)

print("✅ Folders created")

# Get tampered keys from SCD
print("Reading tampered keys...")
scd_env = lmdb.open(SCD_LMDB, readonly=True, lock=False)
tampered_keys = set()
with scd_env.begin() as txn:
    for key, _ in txn.cursor():
        tampered_keys.add(key.decode('utf-8'))
scd_env.close()
print(f"Found {len(tampered_keys)} tampered keys")

# Extract images
print("\nExtracting images...")
train_env = lmdb.open(TRAIN_LMDB, readonly=True, lock=False)

tampered_extracted = 0
genuine_extracted  = 0

with train_env.begin() as txn:
    cursor = txn.cursor()
    for key, value in cursor:

        # Stop when both limits reached
        if tampered_extracted >= MAX_TAMPERED and genuine_extracted >= MAX_GENUINE:
            break

        key_str     = key.decode('utf-8')
        is_tampered = key_str in tampered_keys

        if is_tampered and tampered_extracted >= MAX_TAMPERED:
            continue
        if not is_tampered and genuine_extracted >= MAX_GENUINE:
            continue

        try:
            img = Image.open(io.BytesIO(value)).convert('RGB')

            if is_tampered:
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

            img.save(save_path, 'JPEG', quality=90)

            total = tampered_extracted + genuine_extracted
            if total % 1000 == 0:
                print(f"  Progress: {total}/20000 "
                      f"(tampered={tampered_extracted}, "
                      f"genuine={genuine_extracted})")

        except Exception as e:
            print(f"Error on {key_str}: {e}")

train_env.close()

# Final count
print("\n✅ EXTRACTION COMPLETE!")
print("="*40)
for split in ['train', 'validation', 'test']:
    for cls in ['genuine', 'tampered']:
        path  = f'{OUTPUT_DIR}/{split}/{cls}'
        count = len(os.listdir(path))
        print(f"  {split}/{cls}: {count}")