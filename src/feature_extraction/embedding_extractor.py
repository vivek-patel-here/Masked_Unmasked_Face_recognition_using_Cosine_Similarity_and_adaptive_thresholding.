import cv2
import numpy as np
import onnxruntime as ort

MODEL_PATH = "/Users/vivekpatel/.insightface/models/buffalo_l/w600k_r50.onnx"

session = ort.InferenceSession(
    MODEL_PATH,
    providers=["CPUExecutionProvider"]
)

input_name = session.get_inputs()[0].name


def extract_embedding(face_img):

    face = cv2.resize(face_img, (112,112))
    face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)

    face = face.astype(np.float32)
    face = (face - 127.5) / 128.0

    face = np.transpose(face, (2,0,1))
    face = np.expand_dims(face, axis=0)

    embedding = session.run(None, {input_name: face})[0]

    embedding = embedding.flatten()

    embedding = embedding / np.linalg.norm(embedding) # L2 normalization

    return embedding