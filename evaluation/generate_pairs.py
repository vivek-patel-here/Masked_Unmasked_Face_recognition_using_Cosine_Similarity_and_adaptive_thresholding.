import os
import random
import csv

# directory of this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_DIR = os.path.join(BASE_DIR, "../Data/processed/faces")
OUTPUT_FILE = os.path.join(BASE_DIR, "evaluation_pairs.csv")

MAX_PAIRS = 6000

people = os.listdir(DATASET_DIR)

positive_pairs = []
negative_pairs = []


for person in people:

    person_dir = os.path.join(DATASET_DIR, person)

    if not os.path.isdir(person_dir):
        continue

    images = os.listdir(person_dir)

    if len(images) < 2:
        continue

    for i in range(len(images)):
        for j in range(i + 1, len(images)):

            img1 = os.path.join(person, images[i])
            img2 = os.path.join(person, images[j])

            positive_pairs.append((img1, img2, 1))



while len(negative_pairs) < len(positive_pairs):

    p1, p2 = random.sample(people, 2)

    p1_dir = os.path.join(DATASET_DIR, p1)
    p2_dir = os.path.join(DATASET_DIR, p2)

    imgs1 = os.listdir(p1_dir)
    imgs2 = os.listdir(p2_dir)

    if len(imgs1) == 0 or len(imgs2) == 0:
        continue

    img1 = os.path.join(p1, random.choice(imgs1))
    img2 = os.path.join(p2, random.choice(imgs2))

    negative_pairs.append((img1, img2, 0))


pairs = positive_pairs + negative_pairs

random.shuffle(pairs)

pairs = pairs[:MAX_PAIRS]

with open(OUTPUT_FILE, "w", newline="") as f:

    writer = csv.writer(f)

    writer.writerow(["image1", "image2", "label"])

    for pair in pairs:
        writer.writerow(pair)


print("Pairs generated:", len(pairs))
print("Saved to:", OUTPUT_FILE)