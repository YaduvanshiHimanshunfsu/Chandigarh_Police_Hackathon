import os
import random
import shutil

# ============================================
# PATHS
# ============================================
AU_PATH     = r"K:\DOCUMENT\CASIADATASET\CASIA2\Au"
TP_PATH     = r"K:\DOCUMENT\CASIADATASET\CASIA2\Tp"
OUTPUT_PATH = r"K:\DOCUMENT\mobilenetV2\dataset"

# ============================================
# STEP 1 - CREATE FOLDER STRUCTURE
# ============================================
folders = [
    "train/genuine",
    "train/tampered",
    "validation/genuine",
    "validation/tampered",
    "test/genuine",
    "test/tampered"
]

print("Creating folders...")
for folder in folders:
    os.makedirs(os.path.join(OUTPUT_PATH, folder), exist_ok=True)
print("Folders created successfully!")

# ============================================
# STEP 2 - COLLECT ALL IMAGES
# ============================================
print("\nCollecting images...")

au_images = [
    f for f in os.listdir(AU_PATH)
    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.tif'))
]

tp_images = [
    f for f in os.listdir(TP_PATH)
    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.tif'))
]

print(f"Found {len(au_images)} genuine images")
print(f"Found {len(tp_images)} tampered images")

# ============================================
# STEP 3 - BALANCE DATASET
# ============================================
random.seed(42)
au_images = random.sample(au_images, len(tp_images))

print(f"\nAfter balancing:")
print(f"Genuine images:  {len(au_images)}")
print(f"Tampered images: {len(tp_images)}")

# ============================================
# STEP 4 - CALCULATE SPLIT
# ============================================
total = len(au_images)

train_count      = int(total * 0.70)
validation_count = int(total * 0.15)
test_count       = total - train_count - validation_count

print(f"\nSplit plan:")
print(f"Training:   {train_count} images each side")
print(f"Validation: {validation_count} images each side")
print(f"Test:       {test_count} images each side")

# ============================================
# STEP 5 - SHUFFLE AND SPLIT
# ============================================
random.shuffle(au_images)
random.shuffle(tp_images)

# Genuine splits
au_train      = au_images[:train_count]
au_validation = au_images[train_count:train_count + validation_count]
au_test       = au_images[train_count + validation_count:]

# Tampered splits
tp_train      = tp_images[:train_count]
tp_validation = tp_images[train_count:train_count + validation_count]
tp_test       = tp_images[train_count + validation_count:]

# ============================================
# STEP 6 - COPY FILES
# ============================================
def copy_files(file_list, source_path, dest_path, label):
    print(f"\nCopying {label}...")
    success = 0
    failed  = 0
    for i, filename in enumerate(file_list):
        src  = os.path.join(source_path, filename)
        dest = os.path.join(dest_path, filename)
        try:
            shutil.copy2(src, dest)
            success += 1
        except Exception as e:
            failed += 1
            print(f"  Failed: {filename} → {e}")

        if (i + 1) % 500 == 0:
            print(f"  Progress: {i+1}/{len(file_list)} copied...")

    print(f"  Done! {success} copied, {failed} failed!")

# Copy genuine
copy_files(
    au_train,
    AU_PATH,
    os.path.join(OUTPUT_PATH, "train/genuine"),
    "Training Genuine"
)
copy_files(
    au_validation,
    AU_PATH,
    os.path.join(OUTPUT_PATH, "validation/genuine"),
    "Validation Genuine"
)
copy_files(
    au_test,
    AU_PATH,
    os.path.join(OUTPUT_PATH, "test/genuine"),
    "Test Genuine"
)

# Copy tampered
copy_files(
    tp_train,
    TP_PATH,
    os.path.join(OUTPUT_PATH, "train/tampered"),
    "Training Tampered"
)
copy_files(
    tp_validation,
    TP_PATH,
    os.path.join(OUTPUT_PATH, "validation/tampered"),
    "Validation Tampered"
)
copy_files(
    tp_test,
    TP_PATH,
    os.path.join(OUTPUT_PATH, "test/tampered"),
    "Test Tampered"
)

# ============================================
# STEP 7 - FINAL SUMMARY
# ============================================
print("\n" + "="*50)
print("DATASET ORGANIZED SUCCESSFULLY!")
print("="*50)
print(f"\nTraining:   {train_count} genuine + {train_count} tampered = {train_count*2} total")
print(f"Validation: {validation_count} genuine + {validation_count} tampered = {validation_count*2} total")
print(f"Test:       {test_count} genuine + {test_count} tampered = {test_count*2} total")
print(f"\nGrand Total: {(train_count + validation_count + test_count)*2} images")
print(f"\nDataset saved to: {OUTPUT_PATH}")
print("\nYou are ready for training!")