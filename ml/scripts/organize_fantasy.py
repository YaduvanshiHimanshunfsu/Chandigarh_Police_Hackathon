import os
import shutil
import random

# ============================================
# PATHS
# ============================================
FANTASY_BASE = r"K:\DOCUMENT\FANTASYID DATASET\FantasyID"
OUTPUT_PATH  = r"K:\DOCUMENT\mobilenetV2\fantasy_dataset"

# ============================================
# CREATE OUTPUT FOLDERS
# ============================================
folders = [
    "train/genuine", "train/tampered",
    "validation/genuine", "validation/tampered",
    "test/genuine", "test/tampered"
]

print("Creating folders...")
for folder in folders:
    os.makedirs(os.path.join(OUTPUT_PATH, folder), exist_ok=True)
print("Folders created!")

# ============================================
# COLLECT ALL JPG IMAGES (recursive)
# ============================================
def collect_images(base_path):
    images = []
    if not os.path.exists(base_path):
        print(f"  WARNING: Path not found: {base_path}")
        return images
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.lower().endswith('.jpg'):
                images.append(os.path.join(root, file))
    return images

print("\nCollecting images...")

# ----------------------------------------
# GENUINE = bonafide from train AND test
# ----------------------------------------
genuine_from_train = collect_images(
    os.path.join(FANTASY_BASE, "train", "bonafide")
)
genuine_from_test  = collect_images(
    os.path.join(FANTASY_BASE, "test", "bonafide")
)
all_genuine = genuine_from_train + genuine_from_test
print(f"Genuine (train bonafide): {len(genuine_from_train)}")
print(f"Genuine (test bonafide):  {len(genuine_from_test)}")
print(f"Total genuine:            {len(all_genuine)}")

# ----------------------------------------
# TAMPERED = attack from train AND test
# train/attack: digital_1, digital_2
# test/attack: digital_3, facedancer, textdiffuserft_bfei
# ----------------------------------------
tampered_from_train = collect_images(
    os.path.join(FANTASY_BASE, "train", "attack")
)
tampered_from_test  = collect_images(
    os.path.join(FANTASY_BASE, "test", "attack")
)
all_tampered = tampered_from_train + tampered_from_test
print(f"\nTampered (train attack):  {len(tampered_from_train)}")
print(f"Tampered (test attack):   {len(tampered_from_test)}")
print(f"Total tampered:           {len(all_tampered)}")

# ============================================
# BALANCE DATASET
# ============================================
random.seed(42)
min_count    = min(len(all_genuine), len(all_tampered))
all_genuine  = random.sample(all_genuine,  min_count)
all_tampered = random.sample(all_tampered, min_count)

print(f"\nBalanced to {min_count} images each side!")

# ============================================
# SPLIT 70/15/15
# ============================================
random.shuffle(all_genuine)
random.shuffle(all_tampered)

train_count = int(min_count * 0.70)
val_count   = int(min_count * 0.15)
test_count  = min_count - train_count - val_count

print(f"\nSplit plan:")
print(f"Training:   {train_count} each side")
print(f"Validation: {val_count} each side")
print(f"Test:       {test_count} each side")

g_train = all_genuine[:train_count]
g_val   = all_genuine[train_count:train_count+val_count]
g_test  = all_genuine[train_count+val_count:]

t_train = all_tampered[:train_count]
t_val   = all_tampered[train_count:train_count+val_count]
t_test  = all_tampered[train_count+val_count:]

# ============================================
# COPY FILES
# ============================================
def copy_files(file_list, dest_folder, label):
    print(f"\nCopying {label}...")
    os.makedirs(dest_folder, exist_ok=True)
    success = 0
    for i, src in enumerate(file_list):
        filename = os.path.basename(src)
        dest     = os.path.join(dest_folder, filename)
        # Handle duplicate filenames from different subfolders
        if os.path.exists(dest):
            name, ext = os.path.splitext(filename)
            dest = os.path.join(dest_folder, f"{name}_{i}{ext}")
        try:
            shutil.copy2(src, dest)
            success += 1
        except Exception as e:
            print(f"  Failed: {filename} → {e}")
        if (i+1) % 200 == 0:
            print(f"  {i+1}/{len(file_list)} copied...")
    print(f"  Done! {success} files copied!")

copy_files(g_train, os.path.join(OUTPUT_PATH, "train/genuine"),      "Training Genuine")
copy_files(g_val,   os.path.join(OUTPUT_PATH, "validation/genuine"), "Validation Genuine")
copy_files(g_test,  os.path.join(OUTPUT_PATH, "test/genuine"),       "Test Genuine")

copy_files(t_train, os.path.join(OUTPUT_PATH, "train/tampered"),      "Training Tampered")
copy_files(t_val,   os.path.join(OUTPUT_PATH, "validation/tampered"), "Validation Tampered")
copy_files(t_test,  os.path.join(OUTPUT_PATH, "test/tampered"),       "Test Tampered")

# ============================================
# FINAL SUMMARY
# ============================================
print("\n" + "="*50)
print("FANTASYID DATASET ORGANIZED!")
print("="*50)
print(f"Training:   {train_count*2} total")
print(f"Validation: {val_count*2} total")
print(f"Test:       {test_count*2} total")
print(f"Grand Total: {min_count*2} images")
print(f"\nSaved to: {OUTPUT_PATH}")
print("\nReady for training!")