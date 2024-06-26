# main.py

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
import logging

# Add the model directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model')))

from predict import predict_image

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://template-caterpillar-cnn-fast-api.vercel.app/"],  # Adjust this to match your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.DEBUG)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file:
        logging.error("No file uploaded")
        raise HTTPException(status_code=400, detail="No file uploaded")

    try:
        contents = await file.read()
        logging.debug(f"Received file with size: {len(contents)} bytes")
        prediction = predict_image(contents)
        logging.debug(f"Prediction result: {prediction}")
        return {"prediction": prediction}
    except Exception as e:
        logging.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Welcome to the MNIST Digit Classifier API"}

