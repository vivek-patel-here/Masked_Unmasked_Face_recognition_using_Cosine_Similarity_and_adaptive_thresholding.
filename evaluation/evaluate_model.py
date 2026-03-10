import sys
import os
import csv
import cv2
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

sys.path.append(os.path.abspath("src"))

from feature_extraction.embedding_extractor import extract_embedding
from similarity.cosine_similarity import cosine_similarity
from adaptive_threshold.adaptive_threshold import recognize


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAIR_FILE = os.path.join(BASE_DIR, "evaluation_pairs.csv")
DATASET_DIR = os.path.join(BASE_DIR, "../Data/processed/faces")


labels = []
predictions = []

# cache for embeddings
embedding_cache = {}


def get_embedding(img_path):

    if img_path in embedding_cache:
        return embedding_cache[img_path]

    img = cv2.imread(img_path)

    if img is None:
        return None

    emb = extract_embedding(img)

    embedding_cache[img_path] = emb

    return emb


with open(PAIR_FILE, "r") as f:

    reader = csv.DictReader(f)

    for row in reader:

        img1_path = os.path.join(DATASET_DIR, row["image1"])
        img2_path = os.path.join(DATASET_DIR, row["image2"])

        label = int(row["label"])

        emb1 = get_embedding(img1_path)
        emb2 = get_embedding(img2_path)

        if emb1 is None or emb2 is None:
            continue

        similarity = cosine_similarity(emb1, emb2)

        condition = {
            "mask": 0,
            "lighting": "normal",
            "quality": "normal"
        }

        match, _ = recognize(similarity, condition)

        prediction = 1 if match else 0

        labels.append(label)
        predictions.append(prediction)


accuracy = accuracy_score(labels, predictions)
precision = precision_score(labels, predictions)
recall = recall_score(labels, predictions)
f1 = f1_score(labels, predictions)

cm = confusion_matrix(labels, predictions)

print("\n===== Evaluation Results =====")
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)

print("\nConfusion Matrix")
print(cm)