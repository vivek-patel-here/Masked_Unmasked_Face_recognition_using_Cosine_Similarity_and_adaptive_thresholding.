import numpy as np


# BASE_THRESHOLD = 0.4
BASE_THRESHOLD = 0.6


def get_adaptive_threshold(condition):

    threshold = BASE_THRESHOLD

    # mask impact
    if condition["mask"] == 1:
        threshold -= 0.10

    # lighting impact
    lighting_weights = {
        "good": 0.0,
        "normal": 0.02,
        "poor": 0.05
    }

    threshold -= lighting_weights.get(condition["lighting"], 0.02)

    # quality impact
    quality_weights = {
        "good": 0.0,
        "normal": 0.03,
        "poor": 0.06
    }

    threshold -= quality_weights.get(condition["quality"], 0.03)

    return max(threshold, 0.3)
    # return max(threshold, 0.45)

def recognize(similarity, condition):

    threshold = get_adaptive_threshold(condition)

    match = similarity >= threshold

    return match, threshold