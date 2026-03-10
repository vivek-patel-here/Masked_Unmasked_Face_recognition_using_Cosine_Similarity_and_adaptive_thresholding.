import sys
import os

sys.path.append(os.path.abspath("src"))

import json
import cv2
from condition_detection.mask_detector import detect_mask

# This script will prepare vector set :
# { mask = 1 ,
# lighting = normal ,
# quality = poor }

QUALITY_FILE = "Data/processed/image_quality_metadata.json"
OUTPUT_FILE = "Data/processed/condition_vectors.json"

with open(QUALITY_FILE,"r") as f:
    quality_data = json.load(f)

condition_vectors = {}

for img_path, quality_info in quality_data.items():

    image = cv2.imread(img_path)

    if image is None:
        continue

    mask = detect_mask(image)

    lighting = quality_info["lighting"]
    quality = quality_info["quality"]

    condition_vectors[img_path] = {
        "mask": mask,
        "lighting": lighting,
        "quality": quality
    }

with open(OUTPUT_FILE,"w") as f:
    json.dump(condition_vectors,f,indent=4)

print("Condition vectors generated.")