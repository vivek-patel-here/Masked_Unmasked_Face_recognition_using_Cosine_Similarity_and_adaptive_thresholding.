from flask import Flask,request
import sys
import os
import json
import cv2
import PIL
from flask_cors import CORS
import numpy as np

# Flask app init
app = Flask(__name__)
CORS(app)

# dependencies
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

def read_image(file):
    file_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    return img


@app.route("/")
def index_route():
    if(extract_embedding and cosine_similarity and recognize and detect_mask and analyze_image_quality):
        return "Healty Server"
    else :
        return "Upset Server"


@app.route("/analyze" , methods=["POST"])
def analyse_Image():

    file1 = request.files["image1"]
    file2 = request.files["image2"]

    if file1 is None or file2 is None:
        print("Image not received")
        return {
            "Success" : False,
            "Message" : "Image not received!"
        }

    img1 = read_image(file1)
    img2 = read_image(file2)

    if img1 is None or img2 is None:
        print("Error loading images")
        return {
            "Success" : False,
            "Message" : "Unable to read the image, pleas make sure image is in .png/.jpeg/.webp format only!"
        }

    print("Extracting embeddings...")

    emb1 = extract_embedding(img1)
    emb2 = extract_embedding(img2)

    if emb1 is None or emb2 is None:
        print("Face not detected in one of the images")
        return

    similarity = cosine_similarity(emb1, emb2)

    condition1 = generate_condition_vector(img1)
    condition2 = generate_condition_vector(img2)

    # merge conditions
    condition = merge_conditions(condition1, condition2)
    match, threshold = recognize(similarity, condition)

    print("Recognition completed")

    return {
        "Success" : True,
        "Similarity" : similarity,
        "Adaptive Threshold" : threshold,
        "Match" : match
    }


if __name__ == "__main__":
    app.run(debug=False)



