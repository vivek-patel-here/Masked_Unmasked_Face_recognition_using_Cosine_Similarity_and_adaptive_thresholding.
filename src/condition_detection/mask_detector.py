import tensorflow as tf
import numpy as np
import cv2

# This script checks whether the image has mask or not . 
# It uses the mask detection model stored in models dir.

MODEL_PATH = "models/mask_detector.keras"


def load_model():
    model = tf.keras.models.load_model(MODEL_PATH)
    return model

def detect_mask(face_img):
    """
    Input: cropped face image (BGR)
    Output:
        1 -> mask
        0 -> no mask
    """
    model = load_model()
    face = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
    face = cv2.resize(face, (224, 224))
    face = face.astype("float32") / 255.0
    face = np.expand_dims(face, axis=0)

    preds = model.predict(face, verbose=0)

    label = np.argmax(preds[0])

    if label == 0:
        return 1   # mask
    else:
        return 0   # no mask