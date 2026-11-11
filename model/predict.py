import pickle
import pandas as pd
from pathlib import Path

# Load the model from the same folder as this file, so it works
# no matter which directory you start uvicorn from.
MODEL_PATH = Path(__file__).parent / "model.pkl"

MODEL_VERSION = "1.0.0"

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)


def predict_output(user_input: dict) -> dict:
    """Takes a single record (dict) and returns the prediction with confidence."""
    input_df = pd.DataFrame([user_input])

    # [0] because the model returns an array with one element
    predicted_class = model.predict(input_df)[0]

    confidence = None
    class_probabilities = {}

    # Not every model supports predict_proba, so check first
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(input_df)[0]
        class_probabilities = {
            str(cls): round(float(p), 4) for cls, p in zip(model.classes_, probs)
        }
        confidence = round(float(max(probs)), 4)

    return {
        "predicted_category": str(predicted_class),
        "confidence": confidence,
        "class_probabilities": class_probabilities,
    }