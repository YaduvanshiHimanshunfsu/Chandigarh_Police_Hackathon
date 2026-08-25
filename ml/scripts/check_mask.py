import lmdb
import numpy as np
from PIL import Image
import io

# Check if FCD mask tells us genuine vs tampered
fcd_path = r"A:\DocTamper Dataset\DocTamperV1-FCD"

env = lmdb.open(fcd_path, readonly=True, lock=False)

genuine_count  = 0
tampered_count = 0

with env.begin() as txn:
    cursor = txn.cursor()
    for i, (key, value) in enumerate(cursor):
        if i >= 200:  # check first 200 masks
            break
        
        img = Image.open(io.BytesIO(value)).convert('L')  # grayscale
        arr = np.array(img)
        
        white_pixels = np.sum(arr > 10)  # non-black pixels
        
        if white_pixels == 0:
            genuine_count += 1
        else:
            tampered_count += 1

env.close()

print(f"In first 200 FCD masks:")
print(f"  All-black (genuine):  {genuine_count}")
print(f"  Has white (tampered): {tampered_count}")
print(f"  Ratio: {tampered_count}/{genuine_count+tampered_count} are tampered")