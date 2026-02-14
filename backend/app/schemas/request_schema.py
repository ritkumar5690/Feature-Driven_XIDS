"""
Pydantic Schemas for Request Validation
"""

from pydantic import BaseModel, Field, field_validator
from typing import Dict, List, Optional
import numpy as np


class FlowFeatures(BaseModel):
    """
    Schema for network flow features from CIC-IDS2017
    Accepts a dictionary of feature names to values
    """
    features: Dict[str, float] = Field(
        ...,
        description="Dictionary of feature names and their values",
        example={
            "Destination Port": 80,
            "Flow Duration": 120000,
            "Total Fwd Packets": 10,
            "Total Backward Packets": 8,
            "Flow Bytes/s": 1500.5,
            "Flow Packets/s": 150.0
        }
    )
    
    @field_validator('features')
    @classmethod
    def validate_features(cls, v):
        """
        Validate that features dictionary is not empty
        and contains numeric values
        """
        if not v:
            raise ValueError("Features dictionary cannot be empty")
        
        for key, value in v.items():
            if not isinstance(value, (int, float)):
                try:
                    v[key] = float(value)
                except (ValueError, TypeError):
                    raise ValueError(f"Feature '{key}' must be numeric, got {type(value)}")
        
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "features": {
                    "Destination Port": 80,
                    "Flow Duration": 120000,
                    "Total Fwd Packets": 10,
                    "Total Backward Packets": 8,
                    "Flow Bytes/s": 1500.5,
                    "Flow Packets/s": 150.0,
                    "Fwd Packet Length Mean": 512.3,
                    "Bwd Packet Length Mean": 256.7,
                    "Fwd IAT Mean": 100.5,
                    "Bwd IAT Mean": 150.2
                }
            }
        }


class PredictionResponse(BaseModel):
    """
    Schema for prediction response
    """
    prediction: str = Field(
        ...,
        description="Predicted attack class"
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Prediction confidence score"
    )
    probabilities: Optional[Dict[str, float]] = Field(
        None,
        description="Probability distribution across all classes"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "prediction": "DDoS",
                "confidence": 0.97,
                "probabilities": {
                    "BENIGN": 0.01,
                    "DoS": 0.01,
                    "DDoS": 0.97,
                    "PortScan": 0.01
                }
            }
        }


class FeatureImportance(BaseModel):
    """
    Schema for a single feature importance
    """
    feature: str = Field(..., description="Feature name")
    impact: float = Field(..., description="SHAP value impact")
    
    class Config:
        json_schema_extra = {
            "example": {
                "feature": "Flow Duration",
                "impact": 0.45
            }
        }


class ExplanationResponse(BaseModel):
    """
    Schema for SHAP explanation response
    """
    prediction: str = Field(..., description="Predicted class")
    top_features: List[FeatureImportance] = Field(
        ...,
        description="Top contributing features"
    )
    base_value: float = Field(
        ...,
        description="SHAP base value (expected value)"
    )
    shap_values: Optional[List[float]] = Field(
        None,
        description="Complete SHAP values for all features"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "prediction": "DDoS",
                "top_features": [
                    {"feature": "Flow Duration", "impact": 0.45},
                    {"feature": "Total Fwd Packets", "impact": 0.32},
                    {"feature": "Flow Bytes/s", "impact": 0.28}
                ],
                "base_value": 0.14
            }
        }


class HealthResponse(BaseModel):
    """
    Schema for health check response
    """
    status: str = Field(..., description="Service status")
    model_loaded: bool = Field(..., description="Whether model is loaded")
    model_type: Optional[str] = Field(None, description="Type of loaded model")
    feature_count: Optional[int] = Field(None, description="Number of features expected")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "model_loaded": True,
                "model_type": "XGBClassifier",
                "feature_count": 78
            }
        }


class ErrorResponse(BaseModel):
    """
    Schema for error responses
    """
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Prediction failed",
                "detail": "Missing required features: Flow Duration, Total Fwd Packets"
            }
        }
