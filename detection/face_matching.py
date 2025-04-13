import cv2
from model import face_embedding_model
import numpy as np
from numpy.linalg import norm

# Load the cascade
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
# Load the model
model = face_embedding_model.get_model()

def detect_faces(img):
    '''The function `detect_faces` takes an image as input, converts it
    to grayscale, detects faces using a cascade classifier, and returns
    a list of coordinates representing the detected faces.
    
    Parameters
    ----------
    img
        The input image on which you want to detect faces.
    
    Returns
    -------
        a list of faces detected in the image.
    '''
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Display the frame

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )

    # Return the list of faces
    return faces

def is_bgr_image(img): ######################### todo: remove this function
    return (
        isinstance(img, np.ndarray) and
        img.dtype == np.uint8 and
        len(img.shape) == 3 and
        img.shape[2] == 3
    )

def extract_features(face):
    '''The function "extract_features" takes a face image as input, converts it to RGB color format,
    normalize the pixel values to [0, 1], Resize the image to (224, 224), and uses the  model to predict 
    the embedding of the face.

    Parameters
    ----------
    face
        The "face" parameter is an image of a face that you want to extract features from. It is expected
    to be in BGR color format, which is the default color format used by OpenCV.
    
    Returns
    -------
        the embedding of the face, which is a numerical representation of the face's features.

    '''
    ###################################################### remove
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


def match_face(embedding, database):
    '''The function `match_face` takes an input face embedding and a database of face embeddings, and
    returns the name of the closest matching face in the database if the distance is below a certain
    threshold, otherwise it returns None.
    
    Parameters
    ----------
    embedding
        The embedding parameter is a numerical representation of a face. It is typically a vector of
    numbers that captures the unique features of a face.
    database
        The database parameter is a dictionary that contains the embeddings of known faces. The keys of the
    dictionary are the names of the individuals and the values are the corresponding embeddings.
    
    Returns
    -------
        the name of the closest match in the database if the minimum distance is less than 0.50. Otherwise,
    it returns None.
    
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
    