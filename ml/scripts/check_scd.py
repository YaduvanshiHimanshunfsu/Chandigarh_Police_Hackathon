import lmdb

scd_path = r"A:\DocTamper Dataset\DocTamperV1-SCD"
env = lmdb.open(scd_path, readonly=True, lock=False)

with env.begin() as txn:
    total = txn.stat()['entries']
    print(f"SCD total entries: {total}")
    
    cursor = txn.cursor()
    for i, (key, value) in enumerate(cursor):
        key_str = key.decode('utf-8', errors='ignore')
        print(f"\nEntry {i+1}:")
        print(f"  Key: {key_str}")
        print(f"  Value size: {len(value)} bytes")
        try:
            text = value.decode('utf-8')
            print(f"  Text: {text[:200]}")
        except:
            try:
                from PIL import Image
                import io
                img = Image.open(io.BytesIO(value))
                print(f"  Image: {img.size}, Mode: {img.mode}")
            except:
                print(f"  Binary: {value[:30]}")
        if i >= 4:
            break

env.close()