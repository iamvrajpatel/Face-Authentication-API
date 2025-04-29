import json
import os
import cv2
import requests
import numpy as np
import asyncio
from fastapi import FastAPI, HTTPException
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from mtcnn import MTCNN
from deepface import DeepFace
import time

# Create a global MTCNN detector instance
detector = MTCNN()

app = FastAPI()

def download_image(url: str):
    """Download image from URL and convert it into a CV2 image."""
    response = requests.get(url)
    response.raise_for_status()
    img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

@app.post("/")
async def check_avail():
    return {"message": "FaceAuth Service is Available"}

@app.post("/face-verification")
async def check_face(data: dict):
    start = time.time()
    reg_image_url = data.get("reg_image_url")
    test_image_url = data.get("test_image_url")
    criteria = data.get("criteria", 75)  # Default to 75 if not provided

    if not reg_image_url or not test_image_url:
        raise HTTPException(status_code=400, detail="Both image URLs are required")

    try:
        # Download both images concurrently using asyncio.to_thread
        reg_img, test_img = await asyncio.gather(
            asyncio.to_thread(download_image, reg_image_url),
            asyncio.to_thread(download_image, test_image_url)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to load images: {str(e)}")

    # Convert images from BGR to RGB
    reg_rgb = cv2.cvtColor(reg_img, cv2.COLOR_BGR2RGB)
    test_rgb = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)

    try:
        # Run face detection concurrently on both images
        reg_faces_future = asyncio.to_thread(detector.detect_faces, reg_rgb)
        test_faces_future = asyncio.to_thread(detector.detect_faces, test_rgb)
        reg_faces, test_faces = await asyncio.gather(reg_faces_future, test_faces_future)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during face detection: {str(e)}")

    if not reg_faces:
        raise HTTPException(status_code=400, detail="No face detected in the registration image")
    if not test_faces:
        raise HTTPException(status_code=400, detail="No face detected in the test image")

    try:
        # Run DeepFace.verify concurrently to avoid blocking the event loop
        result = await asyncio.to_thread(
            DeepFace.verify,
            reg_rgb,
            test_rgb,
            model_name="Facenet",
            enforce_detection=False
        )
        similarity = 1 - result['distance']  # Convert distance to similarity
        accuracy = round(similarity * 100, 2)  # Convert to percentage
        match = accuracy > criteria
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to verify faces: {str(e)}")

    end = time.time()
    print(f"Time taken: {end - start}")

    return json.dumps({
        'match': match,
        'confidence_percent': accuracy
    })
