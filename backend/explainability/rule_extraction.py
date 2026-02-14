"""
Rule Extraction Module for XIDS
Provides rule-based explanations from tree models
"""

import numpy as np
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class RuleExtractor:
    """Extract rules from tree-based models"""
    
    def __init__(self, model):
        """
        Initialize rule extractor
        
        Args:
            model: Tree-based model (Decision Tree, Random Forest, XGBoost)
        """
        self.model = model
        logger.info("Rule extractor initialized")
    
    def extract_decision_path(self, X_instance: np.ndarray) -> List[str]:
        """
        Extract decision path for a prediction
        
        Args:
            X_instance: Single feature vector
            
        Returns:
            List of rules describing the decision path
        """
        logger.info("Extracting decision path...")
        
        # For sklearn tree models
        if hasattr(self.model, 'decision_path'):
            decision_path = self.model.decision_path(X_instance.reshape(1, -1))[0].toarray()[0]
            rules = self._path_to_rules(decision_path)
            return rules
        
        logger.warning("Model does not support decision path extraction")
        return []
    
    def _path_to_rules(self, path: np.ndarray) -> List[str]:
        """Convert decision path to human-readable rules"""
        rules = []
        
        # This is a placeholder - actual implementation depends on tree structure
        rules.append("Model-based classification")
        
        return rules
    
    def extract_feature_rules(self, feature_importance: np.ndarray) -> List[Dict[str, Any]]:
        """
        Extract rules based on feature importance
        
        Args:
            feature_importance: Array of feature importance scores
            
        Returns:
            List of rules based on feature importance
        """
        logger.info("Extracting feature-based rules...")
        
        # Sort features by importance
        sorted_indices = np.argsort(feature_importance)[::-1]
        
        rules = []
        for idx, feature_idx in enumerate(sorted_indices[:10]):  # Top 10 features
            rules.append({
                'rank': idx + 1,
                'feature_index': int(feature_idx),
                'importance': float(feature_importance[feature_idx]),
                'description': f"Feature {feature_idx} is important for prediction"
            })
        
        return rules


def extract_rules(model, X_instance: np.ndarray) -> List[str]:
    """
    Extract decision rules for a prediction
    
    Args:
        model: Tree-based model
        X_instance: Single feature vector
        
    Returns:
        List of extracted rules
    """
    extractor = RuleExtractor(model)
    return extractor.extract_decision_path(X_instance)


def get_feature_rules(model, feature_importance: np.ndarray) -> List[Dict]:
    """
    Get feature-based rules
    
    Args:
        model: Trained model
        feature_importance: Feature importance scores
        
    Returns:
        List of feature rules
    """
    extractor = RuleExtractor(model)
    return extractor.extract_feature_rules(feature_importance)
