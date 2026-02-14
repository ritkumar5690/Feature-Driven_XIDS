"""
Prediction API Routes
Handles prediction requests
"""

from fastapi import APIRouter, HTTPException, status
from app.schemas.request_schema import (
    FlowFeatures, 
    PredictionResponse, 
    ErrorResponse
)
from app.services.prediction_service import prediction_service
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)


@router.post(
    "",
    response_model=PredictionResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Predict Attack Type",
    description="Predict the type of network intrusion based on flow features"
)
async def predict_attack(flow_features: FlowFeatures):
    """
    Make a prediction for given network flow features
    
    Args:
        flow_features: Network flow features
        
    Returns:
        Prediction response with class and confidence
    """
    try:
        logger.info("Received prediction request")
        
        # Make prediction
        prediction, confidence, probabilities = prediction_service.predict(
            flow_features.features
        )
        
        # Create response
        response = PredictionResponse(
            prediction=prediction,
            confidence=confidence,
            probabilities=probabilities
        )
        
        logger.info(f"Prediction successful: {prediction} ({confidence:.4f})")
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@router.post(
    "/details",
    summary="Get Detailed Prediction",
    description="Get detailed prediction including all probabilities and threat level"
)
async def predict_with_details(flow_features: FlowFeatures):
    """
    Get detailed prediction information
    
    Args:
        flow_features: Network flow features
        
    Returns:
        Detailed prediction information
    """
    try:
        logger.info("Received detailed prediction request")
        
        # Get detailed prediction
        details = prediction_service.get_prediction_details(flow_features.features)
        
        logger.info(f"Detailed prediction successful: {details['prediction']}")
        return details
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Detailed prediction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Detailed prediction failed: {str(e)}"
        )
