"""
Model Loader Service
Handles loading and caching of ML models and preprocessors
"""

import joblib
import logging
from pathlib import Path
from typing import Any, Dict, Optional
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelLoader:
    """
    Singleton class for loading and caching models
    """
    _instance = None
    _model = None
    _preprocessor = None
    _feature_columns = None
    _label_encoder = None
    _scaler = None
    
    def __new__(cls):
        """
        Implement singleton pattern
        """
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
        return cls._instance
    
    def load_model(self, model_path: str) -> Any:
        """
        Load the trained model
        
        Args:
            model_path: Path to saved model file
            
        Returns:
            Loaded model object
        """
        if self._model is None:
            try:
                logger.info(f"Loading model from {model_path}")
                model_package = joblib.load(model_path)
                
                # Extract components from package
                self._model = model_package['model']
                self._feature_columns = model_package.get('feature_columns', [])
                
                logger.info(f"Model loaded successfully: {type(self._model).__name__}")
                logger.info(f"Expected features: {len(self._feature_columns)}")
                
            except FileNotFoundError:
                logger.error(f"Model file not found at {model_path}")
                raise
            except Exception as e:
                logger.error(f"Error loading model: {str(e)}")
                raise
        
        return self._model
    
    def load_preprocessor(self, preprocessor_path: str) -> Dict:
        """
        Load the preprocessor components
        
        Args:
            preprocessor_path: Path to saved preprocessor file
            
        Returns:
            Dictionary containing preprocessor components
        """
        if self._preprocessor is None:
            try:
                logger.info(f"Loading preprocessor from {preprocessor_path}")
                self._preprocessor = joblib.load(preprocessor_path)
                
                # Extract components
                self._label_encoder = self._preprocessor['label_encoder']
                self._scaler = self._preprocessor['scaler']
                
                # Use feature columns from preprocessor if not already set
                if not self._feature_columns:
                    self._feature_columns = self._preprocessor['feature_columns']
                
                logger.info(f"Preprocessor loaded successfully")
                logger.info(f"Available classes: {self._label_encoder.classes_}")
                
            except FileNotFoundError:
                logger.error(f"Preprocessor file not found at {preprocessor_path}")
                raise
            except Exception as e:
                logger.error(f"Error loading preprocessor: {str(e)}")
                raise
        
        return self._preprocessor
    
    def get_model(self) -> Any:
        """
        Get cached model
        
        Returns:
            Loaded model
        """
        if self._model is None:
            raise ValueError("Model not loaded. Call load_model() first.")
        return self._model
    
    def get_label_encoder(self):
        """
        Get label encoder
        
        Returns:
            Label encoder object
        """
        if self._label_encoder is None:
            raise ValueError("Preprocessor not loaded. Call load_preprocessor() first.")
        return self._label_encoder
    
    def get_scaler(self):
        """
        Get feature scaler
        
        Returns:
            Scaler object
        """
        if self._scaler is None:
            raise ValueError("Preprocessor not loaded. Call load_preprocessor() first.")
        return self._scaler
    
    def get_feature_columns(self) -> list:
        """
        Get expected feature columns
        
        Returns:
            List of feature names
        """
        if self._feature_columns is None:
            raise ValueError("Feature columns not available. Load model or preprocessor first.")
        return self._feature_columns
    
    def is_loaded(self) -> bool:
        """
        Check if model and preprocessor are loaded
        
        Returns:
            True if both are loaded
        """
        return self._model is not None and self._preprocessor is not None
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about loaded model
        
        Returns:
            Dictionary with model information
        """
        if not self.is_loaded():
            return {
                "loaded": False,
                "model_type": None,
                "feature_count": 0,
                "classes": []
            }
        
        return {
            "loaded": True,
            "model_type": type(self._model).__name__,
            "feature_count": len(self._feature_columns),
            "classes": self._label_encoder.classes_.tolist()
        }
    
    def initialize(
        self, 
        model_path: Optional[str] = None, 
        preprocessor_path: Optional[str] = None
    ):
        """
        Initialize by loading both model and preprocessor
        
        Args:
            model_path: Path to model file
            preprocessor_path: Path to preprocessor file
        """
        # Set default paths if not provided
        if model_path is None:
            model_path = Path(__file__).parent.parent.parent / "model" / "saved_model.pkl"
        
        if preprocessor_path is None:
            preprocessor_path = Path(__file__).parent.parent.parent / "model" / "preprocessor.pkl"
        
        # Convert to strings
        model_path = str(model_path)
        preprocessor_path = str(preprocessor_path)
        
        # Load components
        self.load_model(model_path)
        self.load_preprocessor(preprocessor_path)
        
        logger.info("Model loader initialized successfully")
    
    def reload(self):
        """
        Force reload of model and preprocessor
        """
        logger.info("Reloading model and preprocessor...")
        self._model = None
        self._preprocessor = None
        self._feature_columns = None
        self._label_encoder = None
        self._scaler = None
        self.initialize()


# Global instance
model_loader = ModelLoader()
