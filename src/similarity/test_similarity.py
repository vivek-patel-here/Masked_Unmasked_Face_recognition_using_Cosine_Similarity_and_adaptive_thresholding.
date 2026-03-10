import sys
import os
sys.path.append(os.path.abspath("src"))

import json
import random
from similarity.cosine_similarity import cosine_similarity

with open("Data/processed/face_embeddings.json") as f:
    embeddings = json.load(f)

keys = list(embeddings.keys())

# pick two random images from different people
while True:
    img1 = keys[0];
    img2 = keys[500];

    person1 = img1.split("/")[-2]
    person2 = img2.split("/")[-2]
    break

vec1 = embeddings[img1]
vec2 = embeddings[img2]

sim = cosine_similarity(vec1, vec2)

print("Image1:", person1)
print("Image2:", person2)
print("Similarity:", sim)