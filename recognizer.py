import sys
import os
import json
import cv2

# allow imports from src
sys.path.append(os.path.abspath("src"))

from feature_extraction.embedding_extractor import extract_embedding
from similarity.cosine_similarity import cosine_similarity
from adaptive_threshold.adaptive_threshold import recognize
from condition_detection.mask_detector import detect_mask
from data_preparation.image_quality_analysis import analyze_image_quality


CONDITION_FILE = "Data/processed/condition_vectors.json"


def generate_condition_vector(img):
    """
    Dynamically generate condition vector if image
    does not exist in precomputed JSON.
    """

    mask = detect_mask(img)
    lighting, quality = analyze_image_quality(img)

    return {
        "mask": mask,
        "lighting": lighting,
        "quality": quality
    }


def merge_conditions(c1, c2):
    """
    Merge two condition vectors using worst-case conditions
    """

    mask = max(c1["mask"], c2["mask"])

    lighting_levels = ["good", "normal", "poor"]
    lighting = lighting_levels[
        max(
            lighting_levels.index(c1["lighting"]),
            lighting_levels.index(c2["lighting"])
        )
    ]

    quality_levels = ["good", "normal", "poor"]
    quality = quality_levels[
        max(
            quality_levels.index(c1["quality"]),
            quality_levels.index(c2["quality"])
        )
    ]

    return {
        "mask": mask,
        "lighting": lighting,
        "quality": quality
    }


def main():

    if len(sys.argv) != 3:
        print("Usage: python recognizer.py image1 image2")
        return

    img_path1 = sys.argv[1]
    img_path2 = sys.argv[2]

    img1 = cv2.imread(img_path1)
    img2 = cv2.imread(img_path2)

    if img1 is None or img2 is None:
        print("Error loading images")
        return

    print("Extracting embeddings...")

    emb1 = extract_embedding(img1)
    emb2 = extract_embedding(img2)

    if emb1 is None or emb2 is None:
        print("Face not detected in one of the images")
        return

    similarity = cosine_similarity(emb1, emb2)

    conditions = {}

    if os.path.exists(CONDITION_FILE):
        with open(CONDITION_FILE, "r") as f:
            conditions = json.load(f)

    # get condition vectors for both images
    condition1 = conditions.get(img_path1)
    condition2 = conditions.get(img_path2)

    if condition1 is None:
        print("Generating condition vector for image1...")
        condition1 = generate_condition_vector(img1)

    if condition2 is None:
        print("Generating condition vector for image2...")
        condition2 = generate_condition_vector(img2)

    # merge conditions
    condition = merge_conditions(condition1, condition2)

    match, threshold = recognize(similarity, condition)

    print("\n===== Recognition Result =====")
    print("Image1:", img_path1)
    print("Image2:", img_path2)
    print("Similarity:", similarity)
    print("Adaptive Threshold:", threshold)
    print("Match:", match)


if __name__ == "__main__":
    main()