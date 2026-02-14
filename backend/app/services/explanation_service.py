"""
Explanation Service using SHAP
Provides interpretability for predictions
"""

import numpy as np
import shap
import logging
from typing import Dict, List, Tuple
from .model_loader import model_loader
from .prediction_service import prediction_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExplanationService:
    """
    Service for generating SHAP-based explanations
    """
    
    def __init__(self):
        self.model_loader = model_loader
        self.prediction_service = prediction_service
        self.explainer = None
        self._initialize_explainer()
    
    def _initialize_explainer(self):
        """
        Initialize SHAP explainer with the loaded model
        """
        try:
            if self.model_loader.is_loaded():
                model = self.model_loader.get_model()
                
                # Use TreeExplainer for tree-based models (XGBoost, RandomForest)
                logger.info("Initializing SHAP TreeExplainer...")
                self.explainer = shap.TreeExplainer(model)
                logger.info("SHAP explainer initialized successfully")
            else:
                logger.warning("Model not loaded, explainer will be initialized later")
                
        except Exception as e:
            logger.error(f"Error initializing SHAP explainer: {str(e)}")
            self.explainer = None
    
    def ensure_explainer_loaded(self):
        """
        Ensure explainer is initialized
        """
        if self.explainer is None:
            self._initialize_explainer()
        
        if self.explainer is None:
            raise ValueError("SHAP explainer could not be initialized")
    
    def explain_prediction(
        self, 
        features: Dict[str, float],
        top_n: int = 10
    ) -> Dict:
        """
        Generate SHAP explanation for a prediction
        
        Args:
            features: Dictionary of feature names to values
            top_n: Number of top features to return
            
        Returns:
            Dictionary containing explanation details
        """
        try:
            self.ensure_explainer_loaded()
            
            # Prepare features
            X = self.prediction_service.prepare_features(features)
            
            # Get prediction first
            prediction, confidence, _ = self.prediction_service.predict(features)
            
            # Calculate SHAP values
            logger.info("Calculating SHAP values...")
            shap_values = self.explainer.shap_values(X)
            
            # Get base value (expected value)
            base_value = self.explainer.expected_value
            
            # Handle multi-class output
            if isinstance(shap_values, list):
                # For multi-class, get the predicted class index
                label_encoder = self.model_loader.get_label_encoder()
                prediction_idx = list(label_encoder.classes_).index(prediction)
                shap_values_class = shap_values[prediction_idx]
                base_value_class = base_value[prediction_idx] if isinstance(base_value, np.ndarray) else base_value
            else:
                shap_values_class = shap_values
                base_value_class = base_value
            
            # Get feature names
            feature_names = self.model_loader.get_feature_columns()
            
            # Create feature importance list
            shap_values_flat = shap_values_class[0] if len(shap_values_class.shape) > 1 else shap_values_class
            
            feature_importance = [
                {
                    "feature": feature_names[i],
                    "impact": float(shap_values_flat[i])
                }
                for i in range(len(feature_names))
            ]
            
            # Sort by absolute impact
            feature_importance.sort(key=lambda x: abs(x["impact"]), reverse=True)
            
            # Get top N features
            top_features = feature_importance[:top_n]
            
            logger.info(f"Generated explanation with {len(top_features)} top features")
            
            return {
                "prediction": prediction,
                "confidence": confidence,
                "top_features": top_features,
                "base_value": float(base_value_class),
                "all_features": feature_importance
            }
            
        except Exception as e:
            logger.error(f"Error generating explanation: {str(e)}")
            raise
    
    def get_global_importance(self, sample_size: int = 100) -> List[Dict]:
        """
        Get global feature importance (not implemented for production)
        This would require a representative dataset
        
        Args:
            sample_size: Number of samples to use
            
        Returns:
            List of feature importance dictionaries
        """
        logger.warning("Global importance requires a representative dataset")
        raise NotImplementedError(
            "Global importance calculation requires access to training data. "
            "Use explain_prediction for local explanations."
        )
    
    def explain_with_visualization_data(
        self, 
        features: Dict[str, float],
        top_n: int = 10
    ) -> Dict:
        """
        Generate explanation with data formatted for visualization
        
        Args:
            features: Dictionary of feature names to values
            top_n: Number of top features to return
            
        Returns:
            Dictionary with visualization-ready data
        """
        try:
            explanation = self.explain_prediction(features, top_n)
            
            # Format for visualization
            viz_data = {
                "prediction": explanation["prediction"],
                "confidence": explanation["confidence"],
                "feature_names": [f["feature"] for f in explanation["top_features"]],
                "feature_impacts": [f["impact"] for f in explanation["top_features"]],
                "feature_values": [
                    features.get(f["feature"], 0) for f in explanation["top_features"]
                ],
                "base_value": explanation["base_value"],
                "positive_features": [
                    f for f in explanation["top_features"] if f["impact"] > 0
                ],
                "negative_features": [
                    f for f in explanation["top_features"] if f["impact"] < 0
                ]
            }
            
            return viz_data
            
        except Exception as e:
            logger.error(f"Error generating visualization data: {str(e)}")
            raise
    
    def get_feature_contribution_summary(
        self, 
        features: Dict[str, float]
    ) -> str:
        """
        Get human-readable summary of feature contributions
        
        Args:
            features: Dictionary of feature names to values
            
        Returns:
            Text summary of explanation
        """
        try:
            explanation = self.explain_prediction(features, top_n=5)
            
            summary = f"Prediction: {explanation['prediction']} (Confidence: {explanation['confidence']:.2%})\n\n"
            summary += "Top Contributing Features:\n"
            
            for i, feat in enumerate(explanation['top_features'], 1):
                impact_direction = "increases" if feat['impact'] > 0 else "decreases"
                summary += f"{i}. {feat['feature']}: {impact_direction} prediction by {abs(feat['impact']):.4f}\n"
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            raise


# Global instance
explanation_service = ExplanationService()
