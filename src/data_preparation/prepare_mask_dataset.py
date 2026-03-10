import os
import shutil
from tqdm import tqdm

# Source datasets
RMFRD_MASKED = "Data/raw/rmfrd/AFDB_masked_face_dataset"
RMFRD_UNMASKED = "Data/raw/rmfrd/AFDB_face_dataset"
SMFRD_TRAIN = "Data/raw/smfrd/lfw_train"
SMFRD_TEST = "Data/raw/smfrd/lfw_test"
LFW_CLEAN = "Data/processed/lfw_clean"

# Destination dataset
MASK_DIR = "Data/mask_dataset/mask"
NO_MASK_DIR = "Data/mask_dataset/no_mask"

os.makedirs(MASK_DIR, exist_ok=True)
os.makedirs(NO_MASK_DIR, exist_ok=True)


def copy_images(source_folder, destination_folder, prefix):

    count = 0

    for root, dirs, files in os.walk(source_folder):

        for file in files:

            if file.lower().endswith((".jpg", ".png", ".jpeg")):

                src = os.path.join(root, file)

                new_name = f"{prefix}_{count}.jpg"

                dst = os.path.join(destination_folder, new_name)

                shutil.copy(src, dst)

                count += 1


print("Copying RMFRD masked images...")
copy_images(RMFRD_MASKED, MASK_DIR, "rmfrd_mask")

print("Copying SMFRD train images...")
copy_images(SMFRD_TRAIN, MASK_DIR, "smfrd_train")

print("Copying SMFRD test images...")
copy_images(SMFRD_TEST, MASK_DIR, "smfrd_test")

print("Copying RMFRD unmasked images...")
copy_images(RMFRD_UNMASKED, NO_MASK_DIR, "rmfrd_nomask")

print("Copying LFW images...")
copy_images(LFW_CLEAN, NO_MASK_DIR, "lfw_nomask")

print("Mask dataset preparation complete.")