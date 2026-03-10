import tensorflow as tf
import numpy as np
import cv2

# Load EfficientNetB0 without classifier
model = tf.keras.applications.EfficientNetB0(
    weights="imagenet",
    include_top=False,
    pooling="avg",
    input_shape=(224,224,3)
)

def extract_embedding(face_img):
    """
    Input: cropped face image
    Output: 1280 dimensional embedding vector
    """

    face = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
    face = cv2.resize(face, (224,224))

    face = face.astype("float32") / 255.0
    face = np.expand_dims(face, axis=0)

    embedding = model.predict(face, verbose=0)

    return embedding[0]