import os
import cv2
import json
import numpy as np

def analyze_image_quality(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # brightness
    brightness = np.mean(gray)

    if brightness > 80:
        lighting = "normal"
    else:
        lighting = "poor"

    # blur detection
    blur = cv2.Laplacian(gray, cv2.CV_64F).var()

    if blur > 100:
        quality = "good"
    else:
        quality = "poor"

    return lighting, quality



if __name__=="__main__":
    #Architectural Block 2 : Image quality Analysis and metadata generation
    INPUT_DIR = "Data/processed/faces"
    OUTPUT_FILE = "Data/processed/image_quality_metadata.json"

    metadata = {}

    for person in os.listdir(INPUT_DIR):

        person_path = os.path.join(INPUT_DIR, person)

        if not os.path.isdir(person_path):
            continue

        for img_name in os.listdir(person_path):

            img_path = os.path.join(person_path, img_name)

            image = cv2.imread(img_path)

            if image is None:
                continue

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Brightness score
            brightness = np.mean(gray)

            if brightness > 80:
                lighting = "normal"
            else:
                lighting = "poor"

            # Blur score
            blur = cv2.Laplacian(gray, cv2.CV_64F).var()

            if blur > 100:
                quality = "good"
            else:
                quality = "poor"

            metadata[img_path] = {
                "brightness": float(brightness),
                "blur": float(blur),
                "lighting": lighting,
                "quality": quality
            }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(metadata, f, indent=4)

    print("Image quality analysis complete.")