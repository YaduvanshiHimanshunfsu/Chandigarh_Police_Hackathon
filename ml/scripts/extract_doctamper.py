import lmdb
import os
import pickle
from PIL import Image
import io

def extract_doctamper(lmdb_path, output_folder, max_images=500):
    """
    Extracts images from DocTamper LMDB database
    max_images: start with 500 to test, then do all
    """
    os.makedirs(output_folder, exist_ok=True)
    
    env = lmdb.open(lmdb_path, readonly=True, lock=False)
    
    extracted = 0
    failed = 0
    
    with env.begin() as txn:
        cursor = txn.cursor()
        for key, value in cursor:
            if extracted >= max_images:
                break
            try:
                key_str = key.decode('utf-8')
                
                # Try direct image bytes first
                try:
                    img = Image.open(io.BytesIO(value))
                    img = img.convert('RGB')
                    save_path = os.path.join(output_folder, f"{key_str}.jpg")
                    img.save(save_path, 'JPEG', quality=95)
                    extracted += 1
                    if extracted % 50 == 0:
                        print(f"Extracted {extracted} images...")
                except Exception:
                    # Try pickle format
                    data = pickle.loads(value)
                    print(f"Pickle format detected! Type: {type(data)}")
                    if isinstance(data, dict):
                        print(f"Keys in dict: {list(data.keys())}")
                    break
                    
            except Exception as e:
                failed += 1
                if failed <= 3:
                    print(f"Failed on {key}: {e}")
    
    env.close()
    print(f"\n✅ Done! Extracted: {extracted} | Failed: {failed}")
    print(f"Saved to: {output_folder}")

# ── Run extraction ──
print("Checking TrainingSet structure...")
extract_doctamper(
    lmdb_path=r"A:\DocTamper Dataset\DocTamperV1-TrainingSet",
    output_folder=r"K:\DOCUMENT\doctamper_extracted\sample",
    max_images=10  # start with just 10 to verify
)