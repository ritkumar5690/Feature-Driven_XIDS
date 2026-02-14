"""
FastAPI Main Application for XIDS Backend
Explainable Intrusion Detection System
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import os
from pathlib import Path

from app.routes import predict, explain
from app.services.model_loader import model_loader
from app.schemas.request_schema import HealthResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events
    """
    # Startup: Load model and preprocessor
    logger.info("Starting XIDS Backend...")
    
    try:
        # Define paths
        base_dir = Path(__file__).parent.parent
        model_path = base_dir / "model" / "saved_model.pkl"
        preprocessor_path = base_dir / "model" / "preprocessor.pkl"
        
        # Check if files exist
        if not model_path.exists():
            logger.warning(f"Model file not found at {model_path}")
            logger.warning("Please train the model first using backend/model/train.py")
        else:
            # Load model and preprocessor
            model_loader.initialize(
                model_path=str(model_path),
                preprocessor_path=str(preprocessor_path)
            )
            logger.info("Model and preprocessor loaded successfully")
            
            # Log model info
            model_info = model_loader.get_model_info()
            logger.info(f"Model Type: {model_info['model_type']}")
            logger.info(f"Feature Count: {model_info['feature_count']}")
            logger.info(f"Classes: {model_info['classes']}")
        
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        logger.warning("API will start but predictions may fail until model is loaded")
    
    logger.info("XIDS Backend started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down XIDS Backend...")


# Create FastAPI application
app = FastAPI(
    title="XIDS - Explainable Intrusion Detection System",
    description="""
    Production-ready API for network intrusion detection with explainability.
    
    ## Features
    * **Prediction**: Classify network flows as benign or various attack types
    * **Explanation**: SHAP-based explanations for predictions
    * **CIC-IDS2017**: Trained on industry-standard dataset
    * **Real-time**: Fast inference for live traffic analysis
    
    ## Attack Types Detected
    * BENIGN
    * DoS (Denial of Service)
    * DDoS (Distributed Denial of Service)
    * PortScan
    * Bot
    * Brute Force
    * Web Attack
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(predict.router)
app.include_router(explain.router)


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - API information
    """
    return {
        "name": "XIDS - Explainable Intrusion Detection System",
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint
    
    Returns service status and model information
    """
    try:
        model_info = model_loader.get_model_info()
        
        return HealthResponse(
            status="healthy" if model_info["loaded"] else "degraded",
            model_loaded=model_info["loaded"],
            model_type=model_info["model_type"],
            feature_count=model_info["feature_count"]
        )
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return HealthResponse(
            status="unhealthy",
            model_loaded=False,
            model_type=None,
            feature_count=0
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler
    """
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc)
        }
    )


# Run with: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
