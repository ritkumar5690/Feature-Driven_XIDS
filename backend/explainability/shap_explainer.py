"""
SHAP Explainability Module for XIDS
Provides SHAP-based model explanations
"""

import numpy as np
import shap
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class SHAPExplainer:
    """SHAP-based model explainer"""
    
    def __init__(self, model, X_train: np.ndarray, model_type: str = 'tree'):
        """
        Initialize SHAP explainer
        
        Args:
            model: Trained model
            X_train: Training features for background data
            model_type: 'tree' or 'kernel'
        """
        self.model = model
        self.X_train = X_train
        self.model_type = model_type
        
        logger.info(f"Initializing SHAP explainer (type: {model_type})...")
        
        if model_type == 'tree':
            self.explainer = shap.TreeExplainer(model)
        elif model_type == 'kernel':
            self.explainer = shap.KernelExplainer(
                model.predict_proba, 
                shap.sample(X_train, 100)
            )
        else:
            logger.warning(f"Unknown model type: {model_type}, using tree")
            self.explainer = shap.TreeExplainer(model)
    
    def explain_instance(self, X_instance: np.ndarray) -> Dict[str, Any]:
        """
        Explain prediction for a single instance
        
        Args:
            X_instance: Single feature vector
            
        Returns:
            Dictionary with SHAP values and feature contributions
        """
        shap_values = self.explainer.shap_values(X_instance)
        
        # Handle multi-class case
        if isinstance(shap_values, list):
            shap_values = shap_values[0]
        
        explanation = {
            'shap_values': shap_values.tolist() if isinstance(shap_values, np.ndarray) else shap_values,
            'base_value': float(self.explainer.expected_value)
        }
        
        return explanation
    
    def explain_batch(self, X_batch: np.ndarray) -> Dict[str, Any]:
        """
        Explain predictions for a batch of instances
        
        Args:
            X_batch: Batch of feature vectors
            
        Returns:
            Dictionary with aggregated SHAP explanations
        """
        logger.info(f"Explaining batch of {len(X_batch)} instances...")
        
        shap_values = self.explainer.shap_values(X_batch)
        
        # Handle multi-class case
        if isinstance(shap_values, list):
            shap_values = shap_values[0]
        
        # Compute feature importance
        mean_abs_shap = np.mean(np.abs(shap_values), axis=0)
        feature_importance = mean_abs_shap / np.sum(mean_abs_shap)
        
        explanation = {
            'mean_shap_values': shap_values.mean(axis=0).tolist(),
            'feature_importance': feature_importance.tolist(),
            'base_value': float(self.explainer.expected_value)
        }
        
        return explanation


def explain_prediction(model, X_instance: np.ndarray, X_train: np.ndarray) -> Dict:
    """
    Get SHAP explanation for a single prediction
    
    Args:
        model: Trained model
        X_instance: Single feature vector
        X_train: Training features
        
    Returns:
        Dictionary with SHAP explanation
    """
    explainer = SHAPExplainer(model, X_train, model_type='tree')
    return explainer.explain_instance(X_instance)
