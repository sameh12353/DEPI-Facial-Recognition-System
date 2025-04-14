import cv2
from model import face_embedding_model
import numpy as np
from numpy.linalg import norm
from typing import Optional

# Load the cascade
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
# Load the model
model = face_embedding_model.get_model()

def detect_faces(img :np.ndarray) -> list:
    '''Detects faces in an input image using Haar Cascade classifier.
    
    Parameters
    ----------
    img : np.ndarray
        The input image on which you want to detect faces.
    
    Returns
    -------
    list[tuple[int, int, int, int]]
        List of face bounding boxes where each box is represented as:
        (x, y, width, height) - coordinates of top-left corner and dimensions
    '''
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )

    # Return the list of faces
    return faces

def is_bgr_image(img :np.ndarray): ######################### todo: remove this function
    return (
        isinstance(img, np.ndarray) and
        img.dtype == np.uint8 and
        len(img.shape) == 3 and
        img.shape[2] == 3
    )

def extract_features(face :np.ndarray) -> np.ndarray:
    '''Extracts facial features/embeddings from a face image using a pre-trained model.

    Parameters
    ----------
    face : np.ndarray
        Input face image in OpenCV BGR format 
    
    Returns
    -------
    np.ndarray
        A 1D numpy array representing the face embedding (feature vector).

    '''
    ###################################################### todo: remove
    if not is_bgr_image(face):
        print("❌ Not a valid BGR image")
    else:
        print("✅ Image is in BGR format")
    ######################################################
    # Convert the face to RGB color format
    image = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
    # normalize the pixel values to [0, 1]
    image = (image / 255.).astype(np.float32)
    # Resize the image to (224, 224)
    image = cv2.resize(image, dsize = (224,224))
    # Use the model to predict the embedding
    embedding = face_embedding_model.get_embedding(image, model)

    return embedding


def match_face(embedding: np.ndarray, database: dict[str, np.ndarray]) -> Optional[str]:
    '''Finds the closest matching face in a database for a given face embedding using cosine similarity.

    The function compares an input face embedding against all embeddings in the database
    and returns the name of the closest match if the similarity distance is below
    the specified threshold.
    
    Parameters
    ----------
    embedding : np.ndarray
        A 1D numpy array representing the face embedding (feature vector)
    database : dict[str, np.ndarray]
        A dictionary mapping names (strings) to their corresponding face embeddings.
    
    Returns
    -------
    Optional[str]
        The name of the closest matching face if the distance is below threshold,
        otherwise None.
    
    '''
    min_distance = 100  # Initialize min_distance with a large number
    match = None  # Initialize match with None

    # Loop over all faces in the database
    for name, db_embedding in database.items():
        # Calculate the Cosine similarity distance between the
        # input embedding and the database embedding
        distance = 1 - np.dot(embedding, db_embedding) / (norm(embedding) * norm(db_embedding))

        # If the distance is less than the min_distance, update
        # the min_distance and match
        if distance < min_distance:
            min_distance = distance
            match = name
            

    # If the min_distance is less than a threshold, return the match
    if min_distance < 0.30:
        return match
    else:
        return None
    