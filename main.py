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
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        results = model(image)

        # Convert results to JSON-compatible format
        json_results = json.loads(results[0].tojson())
        return JSONResponse(content={"predictions": json_results})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
