import cv2
from detection.face_matching import *
from database.utils import get_face_embeddings_db
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from utils import load_yaml
#$ C:/Users/pc/AppData/Local/Programs/Python/Python312/python.exe d:/Study/DEPI/Project/test/face-detection.py
# Traceback (most recent call last):
#   File "d:\Study\DEPI\Project\test\face-detection.py", line 2, in <module>
#     from detection.face_matching import *
# ModuleNotFoundError: No module named 'detection'
################################################################
# Traceback (most recent call last):
#   File "d:\Study\DEPI\Project\test\face-detection.py", line 7, in <module>
#     from detection.face_matching import *
#   File "d:\Study\DEPI\Project\detection\__init__.py", line 1, in <module>
#     from face_matching import *
# ModuleNotFoundError: No module named 'face_matching'

config_file_path = load_yaml("configs/database.yaml")

def match_with_database(img, database):
    # Detect faces in the frame
    faces = detect_faces(img)

    for face in faces:
        try:
            # Extract features from the face
            embedding = extract_features(face)

            embedding = embedding[0]["embedding"]

            # Match the face to a face in the database
            match = match_face(embedding, database)

            if match is not None:
                print(f"Match found: {match}")
            else:
                print("No match found")
        except:
            print("No face detected")


def process_frame(frame):
    """Process each frame for face recognition"""
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
    img = cv2.imread("D:/Study/DEPI/Project/examples/images/2.png")
    faces = match_with_database(img, database)