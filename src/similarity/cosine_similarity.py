import numpy as np

def cosine_similarity(vec1, vec2):
    """
    Compute cosine similarity between two embedding vectors
    """

    v1 = np.array(vec1)
    v2 = np.array(vec2)

    dot_product = np.dot(v1, v2)

    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)

    similarity = dot_product / (norm1 * norm2)

    return float(similarity)