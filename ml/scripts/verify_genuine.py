import lmdb
import io
from PIL import Image
import numpy as np

# Check image 000050000 - should be genuine if our assumption is right
TRAIN_LMDB = r"A:\DocTamper Dataset\DocTamperV1-TrainingSet"
SCD_LMDB   = r"A:\DocTamper Dataset\DocTamperV1-SCD"

# Get all SCD keys
scd_env = lmdb.open(SCD_LMDB, readonly=True, lock=False)
tampered_keys = set()
with scd_env.begin() as txn:
    for key, _ in txn.cursor():
        tampered_keys.add(key.decode('utf-8'))
scd_env.close()

# Check 10 images from the "genuine" zone
train_env = lmdb.open(TRAIN_LMDB, readonly=True, lock=False)
with train_env.begin() as txn:
    cursor = txn.cursor()
    checked = 0
    skipped = 0
    for key, value in cursor:
        key_str = key.decode('utf-8')
        
        # Only look at images NOT in tampered keys
        if key_str in tampered_keys:
            skipped += 1
            continue
            
        img = Image.open(io.BytesIO(value)).convert('RGB')
        arr = np.array(img)
        
        print(f"Key: {key_str}")
        print(f"  Size: {img.size}")
        print(f"  Is in SCD (tampered): {key_str in tampered_keys}")
        print(f"  Avg brightness: {arr.mean():.1f}")
        print()
        
        checked += 1
        if checked >= 5:
            break

train_env.close()
print(f"Skipped {skipped} tampered images to find 5 genuine ones")