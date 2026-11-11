import logging

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from model.predict import predict_output, model, MODEL_VERSION
from schema.user_input import UserInput
from schema.prediction_response import PredictionResponse, HealthResponse

logger = logging.getLogger("insurance_api")

app = FastAPI(title="Insurance Premium Prediction")


@app.get("/")
def home():
    return {"message": "Welcome to Insurance Premium Prediction"}


# Fixed: the @ decorator was missing, and MODEL_VERSION was returned as a string
@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="OK",
        version=MODEL_VERSION,
        model_loaded=model is not None,
    )


@app.post("/predict", response_model=PredictionResponse)
def predict_premium(data: UserInput):
    try:
        # Keys must match exactly what the model was trained on.
        input_data = {
            "bmi": data.bmi,
            "age_group": data.age_group,
            "lifestyle_risk": data.lifestyle_risk,
            "city_tier": data.city_tier,
            "income_lpa": data.income_lpa,
            "occupation": data.occupation,
        }

        return predict_output(input_data)

    except (ValueError, KeyError) as e:
        # Bad / unexpected input reaching the model
        logger.warning("Invalid input for prediction: %s", e)
        raise HTTPException(status_code=422, detail=f"Invalid input: {e}")

    except Exception as e:
        # Anything else is a server-side problem
        logger.exception("Prediction failed")
        raise HTTPException(status_code=500, detail="Prediction failed. Please try again later.")