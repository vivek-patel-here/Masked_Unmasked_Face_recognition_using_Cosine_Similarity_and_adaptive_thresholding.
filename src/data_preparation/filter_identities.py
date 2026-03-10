import os
import shutil

# This script filters the lfw dataset and keeps only those person's identity who has three or more images.
SOURCE_DIR = "Data/raw/lfw"
DEST_DIR = "Data/processed/lfw_clean"

MIN_IMAGES = 3

os.makedirs(DEST_DIR, exist_ok=True)

for person in os.listdir(SOURCE_DIR):

    person_path = os.path.join(SOURCE_DIR, person)

    if not os.path.isdir(person_path):
        continue

    images = os.listdir(person_path)

    if len(images) >= MIN_IMAGES:

        dest_person = os.path.join(DEST_DIR, person)

        shutil.copytree(person_path, dest_person)

print("Filtering complete.")