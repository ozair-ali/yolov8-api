from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from ultralytics import YOLO
from PIL import Image
import io
import json

app = FastAPI()

# Load the YOLO model
model = YOLO("model.pt")  # Ensure model.pt is included in your repo or deployed

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    results = model(image)

    result = results[0]

    # If no boxes are detected, return message
    if result.boxes is None or result.boxes.xyxy.shape[0] == 0:
        return {"message": "No objects detected."}

    # Return structured detection results
    return {
        "boxes": result.boxes.xyxy.tolist(),         # bounding box coordinates
        "confidences": result.boxes.conf.tolist(),   # confidence scores
        "classes": result.boxes.cls.tolist(),        # class indices
        "names": result.names                        # class name mapping
    }
