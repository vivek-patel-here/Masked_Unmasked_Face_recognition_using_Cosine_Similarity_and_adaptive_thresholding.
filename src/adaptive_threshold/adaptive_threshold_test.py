import sys
import os

sys.path.append(os.path.abspath("src"))

from adaptive_threshold import recognize

similarity = 0.52

condition = {
    "mask": 1,
    "lighting": "normal",
    "quality": "poor"
}

result, threshold = recognize(similarity, condition)

print("Similarity:", similarity)
print("Threshold:", threshold)
print("Match:", result)