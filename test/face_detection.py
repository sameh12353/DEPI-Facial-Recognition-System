import cv2
from detection.face_matching import *
from typing import Optional
from database.utils import get_face_embeddings_db
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from utils import load_yaml

config_file_path = load_yaml("configs/database.yaml")

def match_with_database(img: np.ndarray, database: dict[str, np.ndarray]) -> Optional[str]:
    """The function detects faces in the input image, extracts their features, and compares them with
        the embeddings stored in the database. If a match is found, it returns the name of the matched

    Args:
        img (np.ndarray): Input image in BGR format (OpenCV default) with shape (height, width, 3).
        database (dict[str, np.ndarray]): Dictionary mapping student names to their pre-computed face embeddings.
                                          Format: {'name': np.array([embedding_values]), ...}

    Returns:
        Optional[str]: The name of the matched person if found (None if no match found)
    """
    # Detect faces in the frame
    faces = detect_faces(img)

    for face in faces:
        # Extract features from the face
        x, y, w, h = face
        face_img = img[y:y+h, x:x+w]

        # Ensure image is in BGR format and dtype is uint8
        if face_img.dtype != np.uint8:
            face_img = cv2.convertScaleAbs(face_img)

        embedding = extract_features(face_img)

        # Match the face to a face in the database
        match = match_face(embedding, database)

        if match is not None:
            print(f"Match found: {match}")
            return match
            
    print("No match found")
    return None


def process_frame(frame: np.ndarray) -> np.ndarray:
    """Processes a video frame for face detection and visualization.

    Performs the following operations:
    1. Detects faces in the input frame using detect_faces()
    2. Draws bounding boxes around detected faces
    3. Labels each detected face with "Face Detected" text
    4. Returns the annotated frame

    Args:
        frame (np.ndarray): Input video frame in BGR format (OpenCV default)

    Returns:
        np.ndarray: The annotated frame with face bounding boxes and labels
    """
    faces = detect_faces(frame)
    # Display the frame
    for (x, y, w, h) in faces:
        # Face recognition logic here
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, "Face Detected", (x, y-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
    return frame


# Check if Firebase is already initialized
if not firebase_admin._apps:
    # Initialize Firebase
    cred = credentials.Certificate(config_file_path["firebase"]["pathToServiceAccount"])
    firebase_admin.initialize_app(
        cred,
        {
            "databaseURL": config_file_path["firebase"]["databaseURL"]
        },
    )

# load all the face embeddings from the database
# and convert them to a dictionary with the name as the key and the embedding as the value
database = get_face_embeddings_db()
print(database)
camera_or_image = input("Enter (1) if you have camera\nEnter (2) if you have image: ")

if camera_or_image == "1":

    #define a video capture object
    cap = cv2.VideoCapture(0)
    # Check if the webcam is opened successfully
    if not cap.isOpened():
        print("Error: Could not open webcam")
        exit()

    print("Starting real-time face detection...")
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break
        # Process frame
        processed_frame = process_frame(frame)
        # Display the frame
        cv2.imshow('Real-time Face Detection', processed_frame)
        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Release resources
        cap.release()
        cv2.destroyAllWindows()
        print("Webcam stopped")

    faces = match_with_database(frame, database)


elif camera_or_image == "2":
    # Read the image from the file
    img = cv2.imread("D:/Study/DEPI/Project/examples/images/images.jpg")
    faces = match_with_database(img, database)