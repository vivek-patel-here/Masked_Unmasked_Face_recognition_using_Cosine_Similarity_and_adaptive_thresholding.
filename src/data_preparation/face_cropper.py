import os
import cv2
from mtcnn import MTCNN

detector = MTCNN()
def crop_face(image):
    """
    Detect and crop the largest face in an image.
    Returns a 112x112 cropped face or None.
    """

    if image is None:
        return None

    try:
        faces = detector.detect_faces(image)
    except:
        return None

    if len(faces) == 0:
        return None

    x, y, w, h = faces[0]['box']

    x = max(0, x)
    y = max(0, y)

    margin = int(0.2 * w)

    x1 = max(0, x - margin)
    y1 = max(0, y - margin)
    x2 = min(image.shape[1], x + w + margin)
    y2 = min(image.shape[0], y + h + margin)

    face = image[y1:y2, x1:x2]

    if face.size == 0:
        return None

    face = cv2.resize(face, (112, 112))

    return face

if __name__=="__main__":
    # This script resize the filtered image 
    INPUT_DIR = "Data/processed/lfw_clean"
    OUTPUT_DIR = "Data/processed/faces"

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    detector = MTCNN()

    for person in os.listdir(INPUT_DIR):

        person_path = os.path.join(INPUT_DIR, person)

        if not os.path.isdir(person_path):
            continue

        save_person = os.path.join(OUTPUT_DIR, person)
        os.makedirs(save_person, exist_ok=True)

        for img_name in os.listdir(person_path):

            img_path = os.path.join(person_path, img_name)

            image = cv2.imread(img_path)

            if image is None:
                continue

            if image.shape[0] < 80 or image.shape[1] < 80:
                continue

            try:
                faces = detector.detect_faces(image)
            except:
                continue

            if len(faces) == 0:
                continue

            x, y, w, h = faces[0]['box']

            x = max(0, x)
            y = max(0, y)

            face = image[y:y+h, x:x+w]

            if face.size == 0:
                continue

            face = cv2.resize(face, (224,224))

            save_path = os.path.join(save_person, img_name)

            cv2.imwrite(save_path, face)

    print("Face cropping completed.")