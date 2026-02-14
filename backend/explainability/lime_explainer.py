"""
LIME Explainability Module for XIDS
Provides LIME-based local explanations
"""

import numpy as np
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class LIMEExplainer:
    """LIME-based local explainer"""
    
    def __init__(self, model, feature_names: Optional[list] = None):
        """
        Initialize LIME explainer
        
        Args:
            model: Trained model with predict method
            feature_names: List of feature names
        """
        self.model = model
        self.feature_names = feature_names
        logger.info("LIME explainer initialized")
    
    def explain_prediction(
        self, 
        X_instance: np.ndarray, 
        num_features: int = 10,
        num_samples: int = 5000
    ) -> Dict[str, Any]:
        """
        Explain single prediction using LIME
        
        Args:
            X_instance: Single feature vector
            num_features: Number of features to use in explanation
            num_samples: Number of perturbed samples
            
        Returns:
            Dictionary with explanation
        """
        logger.info(f"Explaining instance with {num_samples} LIME samples...")
        
        # Get prediction
        prediction = self.model.predict(X_instance.reshape(1, -1))[0]
        prediction_proba = self.model.predict_proba(X_instance.reshape(1, -1))[0]
        
        # Generate perturbed samples
        perturbed_samples = np.random.normal(
            loc=X_instance, 
            scale=X_instance.std(),
            size=(num_samples, len(X_instance))
        )
        
        # Get predictions on perturbed samples
        perturbed_predictions = self.model.predict(perturbed_samples)
        
        # Compute feature importance based on correlation
        feature_importance = []
        for i in range(len(X_instance)):
            correlation = np.corrcoef(
                perturbed_samples[:, i], 
                perturbed_predictions
            )[0, 1]
            feature_importance.append(abs(correlation) if not np.isnan(correlation) else 0)
        
        # Normalize importance
        feature_importance = np.array(feature_importance)
        if feature_importance.sum() > 0:
            feature_importance = feature_importance / feature_importance.sum()
        
        explanation = {
            'prediction': int(prediction),
            'prediction_probabilities': prediction_proba.tolist(),
            'feature_importance': feature_importance.tolist(),
            'num_features': num_features,
            'num_samples': num_samples
        }
        
        return explanation


def explain_local(
    model, 
    X_instance: np.ndarray, 
    num_features: int = 10
) -> Dict:
    """
    Get LIME explanation for local prediction
    
    Args:
        model: Trained model
        X_instance: Single feature vector
        num_features: Number of features in explanation
        
    Returns:
        Dictionary with LIME explanation
    """
    explainer = LIMEExplainer(model)
    return explainer.explain_prediction(X_instance, num_features=num_features)
