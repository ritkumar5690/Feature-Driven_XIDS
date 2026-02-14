"""
Feature Selection Module for XIDS
Handles feature selection and dimensionality reduction
"""

import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
from sklearn.ensemble import RandomForestClassifier
import logging
from typing import List

logger = logging.getLogger(__name__)


def select_kbest_features(X: np.ndarray, y: np.ndarray, k: int = 20) -> List[int]:
    """
    Select K best features using ANOVA F-score
    
    Args:
        X: Feature matrix
        y: Target vector
        k: Number of features to select
        
    Returns:
        List of selected feature indices
    """
    logger.info(f"Selecting top {k} features using SelectKBest...")
    
    selector = SelectKBest(score_func=f_classif, k=k)
    selector.fit(X, y)
    
    selected_indices = selector.get_support(indices=True)
    logger.info(f"Selected {len(selected_indices)} features")
    
    return selected_indices.tolist()


def select_mutual_information_features(X: np.ndarray, y: np.ndarray, k: int = 20) -> List[int]:
    """
    Select K best features using mutual information
    
    Args:
        X: Feature matrix
        y: Target vector
        k: Number of features to select
        
    Returns:
        List of selected feature indices
    """
    logger.info(f"Selecting top {k} features using Mutual Information...")
    
    selector = SelectKBest(score_func=mutual_info_classif, k=k)
    selector.fit(X, y)
    
    selected_indices = selector.get_support(indices=True)
    logger.info(f"Selected {len(selected_indices)} features")
    
    return selected_indices.tolist()


def select_forest_features(X: np.ndarray, y: np.ndarray, k: int = 20) -> List[int]:
    """
    Select features based on Random Forest feature importance
    
    Args:
        X: Feature matrix
        y: Target vector
        k: Number of features to select
        
    Returns:
        List of selected feature indices
    """
    logger.info(f"Selecting top {k} features using Random Forest importance...")
    
    rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X, y)
    
    importances = rf.feature_importances_
    selected_indices = np.argsort(importances)[-k:][::-1].tolist()
    
    logger.info(f"Selected {len(selected_indices)} features")
    
    return selected_indices


def get_feature_importance_scores(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Get feature importance scores using Random Forest
    
    Args:
        X: Feature matrix
        y: Target vector
        
    Returns:
        Array of importance scores for each feature
    """
    logger.info("Computing feature importance scores...")
    
    rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X, y)
    
    return rf.feature_importances_
