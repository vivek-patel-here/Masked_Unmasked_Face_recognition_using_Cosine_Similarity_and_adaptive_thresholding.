import sys
import os
import csv
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

sys.path.append(os.path.abspath("src"))

from feature_extraction.embedding_extractor import extract_embedding
from similarity.cosine_similarity import cosine_similarity


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAIR_FILE = os.path.join(BASE_DIR, "evaluation_pairs.csv")
DATASET_DIR = os.path.join(BASE_DIR, "../Data/processed/faces")


similarities = []
labels = []

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


print("Computing similarities...")

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

        sim = cosine_similarity(emb1, emb2)

        similarities.append(sim)
        labels.append(label)


similarities = np.array(similarities)
labels = np.array(labels)

print("Total pairs:", len(labels))


# ================= Accuracy vs Threshold =================

thresholds = np.linspace(0.2, 0.8, 60)

accuracies = []
precisions = []
recalls = []

for t in thresholds:

    preds = (similarities >= t).astype(int)

    tp = np.sum((preds == 1) & (labels == 1))
    tn = np.sum((preds == 0) & (labels == 0))
    fp = np.sum((preds == 1) & (labels == 0))
    fn = np.sum((preds == 0) & (labels == 1))

    acc = (tp + tn) / len(labels)
    prec = tp / (tp + fp + 1e-8)
    rec = tp / (tp + fn + 1e-8)

    accuracies.append(acc)
    precisions.append(prec)
    recalls.append(rec)


plt.figure()
plt.plot(thresholds, accuracies)
plt.xlabel("Threshold")
plt.ylabel("Accuracy")
plt.title("Accuracy vs Threshold")
plt.grid()
plt.savefig("accuracy_vs_threshold.png")
plt.close()


# ================= Precision Recall Plot =================

plt.figure()
plt.plot(thresholds, precisions, label="Precision")
plt.plot(thresholds, recalls, label="Recall")
plt.xlabel("Threshold")
plt.ylabel("Score")
plt.title("Precision & Recall vs Threshold")
plt.legend()
plt.grid()
plt.savefig("precision_recall_vs_threshold.png")
plt.close()


# ================= Similarity Distribution =================

same = similarities[labels == 1]
diff = similarities[labels == 0]

plt.figure()
plt.hist(same, bins=40, alpha=0.6, label="Same Person")
plt.hist(diff, bins=40, alpha=0.6, label="Different Person")
plt.xlabel("Cosine Similarity")
plt.ylabel("Frequency")
plt.title("Similarity Distribution")
plt.legend()
plt.grid()
plt.savefig("similarity_distribution.png")
plt.close()


# ================= Confusion Matrix Heatmap =================

best_threshold = 0.3   # you can change if needed

preds = (similarities >= best_threshold).astype(int)

cm = confusion_matrix(labels, preds)

plt.figure()
plt.imshow(cm)
plt.title("Confusion Matrix")
plt.colorbar()

for i in range(2):
    for j in range(2):
        plt.text(j, i, cm[i, j], ha="center", va="center")

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.savefig("confusion_matrix.png")
plt.close()


print("All graphs saved.")