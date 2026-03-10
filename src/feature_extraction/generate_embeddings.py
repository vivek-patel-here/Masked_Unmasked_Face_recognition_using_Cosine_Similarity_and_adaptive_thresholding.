import sys
import os

sys.path.append(os.path.abspath("src"))

import json
import cv2

from feature_extraction.embedding_extractor import extract_embedding

FACES_DIR = "Data/processed/faces"
OUTPUT_FILE = "Data/processed/face_embeddings.json"

embeddings = {}

count = 0
skipped = 0

for root, dirs, files in os.walk(FACES_DIR):

    for file in files:

        if not file.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        img_path = os.path.join(root, file)

        img = cv2.imread(img_path)

        if img is None:
            skipped += 1
            continue

        emb = extract_embedding(img)

        if emb is None:
            skipped += 1
            continue

        embeddings[img_path] = emb.tolist()

        count += 1

        if count % 100 == 0:
            print(f"Processed {count} images")

# ensure directory exists
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

with open(OUTPUT_FILE, "w") as f:
    json.dump(embeddings, f)

print("\nEmbeddings generated.")
print("Total embeddings:", count)
print("Skipped images:", skipped)