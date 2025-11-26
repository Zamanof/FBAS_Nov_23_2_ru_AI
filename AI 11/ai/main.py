import traceback

import joblib
from fastapi import FastAPI, HTTPException
from pathlib import Path
import pandas as pd

from pydantic import BaseModel

app = FastAPI(title="Price Prediction AI service")


MODEL_PATH = Path(__file__).parent /"models"/ "model_az.pkl"

try:
    loaded = joblib.load(MODEL_PATH)
    if isinstance(loaded, dict) and 'pipeline' in loaded:
        BUNDLE = loaded
        PIPELINE = BUNDLE['pipeline']
        FEATURES = BUNDLE.get('feature_order', ["Bedrooms", "Bathrooms", "Sqm", "City"])
    print(f"Model loaded successfully {MODEL_PATH}")
except Exception as e:
    print("Model could not be loaded")
    traceback.print_exc()
    BUNDLE = None
    PIPELINE = None
    FEATURES = ["Bedrooms", "Bathrooms", "Sqm", "City"]


class PredictIn(BaseModel):
    bedrooms: float
    bathrooms: float
    sqm: float
    city: str

@app.post("/predict")
async def predict(request: PredictIn):
    print(PIPELINE)
    if PIPELINE is None:
        raise HTTPException(status_code=503, detail="Model could not be loaded")
    try:
        features = {
            "Bedrooms": [request.bedrooms],
            "Bathrooms": [request.bathrooms],
            "City": [request.city],
        }

        if "Sqm" in FEATURES:
            features["Sqm"] = [request.sqm]
        features_df = pd.DataFrame(features, columns=FEATURES)
        prediction = PIPELINE.predict(features_df)[0]
        return {"priceAZN": float(prediction)}
    except Exception as e:
        print(f"Error predicting price: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error predicting price: {e}")


@app.post("/retrain")
async def retrain():
    pass