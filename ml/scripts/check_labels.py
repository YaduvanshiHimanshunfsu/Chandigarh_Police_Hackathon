import lmdb
import os

# Check FCD folder - this likely has the labels
fcd_path = r"A:\DocTamper Dataset\DocTamperV1-FCD"

env = lmdb.open(fcd_path, readonly=True, lock=False)

with env.begin() as txn:
    total = txn.stat()['entries']
    print(f"FCD total entries: {total}")
    
    cursor = txn.cursor()
    for i, (key, value) in enumerate(cursor):
        print(f"\nEntry {i+1}:")
        print(f"  Key: {key.decode('utf-8', errors='ignore')}")
        print(f"  Value size: {len(value)} bytes")
        
        # Try to open as image
        try:
            from PIL import Image
            import io
            img = Image.open(io.BytesIO(value))
            print(f"  Image size: {img.size}, Mode: {img.mode}")
        except:
            # Try as text/label
            try:
                text = value.decode('utf-8')
                print(f"  Text value: {text[:100]}")
            except:
                print(f"  Binary data (first 20 bytes): {value[:20]}")
        
        if i >= 4:
            break

env.close()