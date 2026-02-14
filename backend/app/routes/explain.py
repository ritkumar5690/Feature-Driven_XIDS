"""
Explanation API Routes
Handles SHAP explanation requests
"""

from fastapi import APIRouter, HTTPException, status, Query
from app.schemas.request_schema import (
    FlowFeatures, 
    ExplanationResponse, 
    ErrorResponse
)
from app.services.explanation_service import explanation_service
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/explain",
    tags=["Explanation"]
)


@router.post(
    "",
    response_model=ExplanationResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Explain Prediction",
    description="Generate SHAP-based explanation for a prediction"
)
async def explain_prediction(
    flow_features: FlowFeatures,
    top_n: int = Query(10, ge=1, le=50, description="Number of top features to return")
):
    """
    Generate SHAP explanation for given network flow features
    
    Args:
        flow_features: Network flow features
        top_n: Number of top features to return (1-50)
        
    Returns:
        Explanation response with feature impacts
    """
    try:
        logger.info(f"Received explanation request (top_n={top_n})")
        
        # Generate explanation
        explanation = explanation_service.explain_prediction(
            flow_features.features,
            top_n=top_n
        )
        
        # Create response
        response = ExplanationResponse(
            prediction=explanation["prediction"],
            top_features=explanation["top_features"],
            base_value=explanation["base_value"]
        )
        
        logger.info(f"Explanation generated successfully for: {explanation['prediction']}")
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Explanation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Explanation generation failed: {str(e)}"
        )


@router.post(
    "/visualization",
    summary="Get Visualization Data",
    description="Get explanation data formatted for visualization"
)
async def get_visualization_data(
    flow_features: FlowFeatures,
    top_n: int = Query(10, ge=1, le=50, description="Number of top features to return")
):
    """
    Get explanation data formatted for frontend visualization
    
    Args:
        flow_features: Network flow features
        top_n: Number of top features to return
        
    Returns:
        Visualization-ready explanation data
    """
    try:
        logger.info(f"Received visualization data request (top_n={top_n})")
        
        # Generate visualization data
        viz_data = explanation_service.explain_with_visualization_data(
            flow_features.features,
            top_n=top_n
        )
        
        logger.info("Visualization data generated successfully")
        return viz_data
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Visualization data error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Visualization data generation failed: {str(e)}"
        )


@router.post(
    "/summary",
    summary="Get Text Summary",
    description="Get human-readable explanation summary"
)
async def get_explanation_summary(flow_features: FlowFeatures):
    """
    Get human-readable summary of explanation
    
    Args:
        flow_features: Network flow features
        
    Returns:
        Text summary of feature contributions
    """
    try:
        logger.info("Received explanation summary request")
        
        # Generate summary
        summary = explanation_service.get_feature_contribution_summary(
            flow_features.features
        )
        
        logger.info("Summary generated successfully")
        return {"summary": summary}
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Summary generation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Summary generation failed: {str(e)}"
        )
