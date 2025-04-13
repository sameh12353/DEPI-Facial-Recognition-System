from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi import APIRouter
from detection.face_matching import *
from database.utils import get_face_embeddings_db

import numpy as np
import cv2


def match_with_database(img, database):
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
        else:
            print("No match found") 

router = APIRouter()
app = FastAPI(version="1.0.0")

@router.post("/match_face")
async def match_face_endpoint(file: UploadFile = File(...)):
    try:
        # Read and decode the uploaded image file
        contents = await file.read()
        np_arr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image file.")

        # Perform face matching
        result = match_with_database(img, get_face_embeddings_db())

        return {"match_result": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


app.include_router(router)

    
    #D:/Study/DEPI/Project
    #fastapi dev main.py
    # pip install fastapi[all]
    #Internal Server Error
    #uvicorn main:app --reload
    # 127.0.0.1:8000/docs
    #No operations defined in spec!
