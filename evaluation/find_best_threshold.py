import sys
import os
import pandas as pd
import numpy as np
import cv2
from sklearn.metrics import accuracy_score

sys.path.append(os.path.abspath("src"))

from feature_extraction.embedding_extractor import extract_embedding
from similarity.cosine_similarity import cosine_similarity


CSV_PATH = "evaluation/evaluation_pairs.csv"
DATASET_ROOT = "Data/processed/faces"  


df = pd.read_csv(CSV_PATH)

similarities = []
labels = []

print("Computing similarities...")

for _, row in df.iterrows():

    img1_path = os.path.join(DATASET_ROOT, row.iloc[0])
    img2_path = os.path.join(DATASET_ROOT, row.iloc[1])
    label = int(row.iloc[2])

    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    if img1 is None or img2 is None:
        continue

    emb1 = extract_embedding(img1)
    emb2 = extract_embedding(img2)

    if emb1 is None or emb2 is None:
        continue

    sim = cosine_similarity(emb1, emb2)

    similarities.append(sim)
    labels.append(label)


similarities = np.array(similarities)
labels = np.array(labels)

same = similarities[labels == 1]
diff = similarities[labels == 0]

print("Same person similarity mean:", same.mean())
print("Different person similarity mean:", diff.mean())

print("Same min/max:", same.min(), same.max())
print("Diff min/max:", diff.min(), diff.max())

print("Total valid pairs:", len(similarities))

print("Searching best threshold...")

thresholds = np.arange(0.3, 0.9, 0.01)

best_acc = 0
best_threshold = 0

for t in thresholds:

    preds = (similarities >= t).astype(int)

    acc = accuracy_score(labels, preds)

    if acc > best_acc:
        best_acc = acc
        best_threshold = t


print("\n===== Best Threshold =====")
print("Threshold:", best_threshold)
print("Accuracy:", best_acc)