from typing import Dict, Optional
from pydantic import BaseModel, Field
 
 
class PredictionResponse(BaseModel):
    predicted_category: str = Field(..., description="Predicted insurance premium category")
    confidence: Optional[float] = Field(
        None, ge=0, le=1, description="Probability of the predicted class (0 to 1)"
    )
    class_probabilities: Dict[str, float] = Field(
        default_factory=dict, description="Probability for every class"
    )
 
 
class HealthResponse(BaseModel):
    status: str
    version: str
    model_loaded: bool