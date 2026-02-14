"""
Feature Analysis Module for XIDS
Provides statistical analysis and visualization utilities for features
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


def compute_feature_statistics(X: pd.DataFrame) -> pd.DataFrame:
    """
    Compute statistical summary for features
    
    Args:
        X: Feature dataframe
        
    Returns:
        DataFrame with statistics (count, mean, std, min, max, quartiles)
    """
    logger.info("Computing feature statistics...")
    
    stats = X.describe()
    logger.info("Statistics computed for all features")
    
    return stats


def analyze_feature_distribution(X: pd.DataFrame) -> Dict[str, Dict]:
    """
    Analyze distribution characteristics of features
    
    Args:
        X: Feature dataframe
        
    Returns:
        Dictionary with distribution info for each feature
    """
    logger.info("Analyzing feature distributions...")
    
    distribution_info = {}
    
    for col in X.columns:
        distribution_info[col] = {
            'mean': X[col].mean(),
            'median': X[col].median(),
            'std': X[col].std(),
            'skewness': X[col].skew(),
            'kurtosis': X[col].kurtosis(),
            'min': X[col].min(),
            'max': X[col].max(),
            'q25': X[col].quantile(0.25),
            'q75': X[col].quantile(0.75)
        }
    
    return distribution_info


def detect_outliers(X: pd.DataFrame, threshold: float = 3.0) -> Dict[str, List[int]]:
    """
    Detect outliers using z-score method
    
    Args:
        X: Feature dataframe
        threshold: Z-score threshold for outlier detection
        
    Returns:
        Dictionary mapping feature names to indices of outliers
    """
    logger.info(f"Detecting outliers with z-score threshold={threshold}...")
    
    outliers = {}
    
    for col in X.columns:
        z_scores = np.abs((X[col] - X[col].mean()) / X[col].std())
        outlier_indices = np.where(z_scores > threshold)[0].tolist()
        
        if outlier_indices:
            outliers[col] = outlier_indices
            logger.info(f"Found {len(outlier_indices)} outliers in {col}")
    
    return outliers


def analyze_class_distribution(y: np.ndarray) -> Dict:
    """
    Analyze class distribution in target variable
    
    Args:
        y: Target array
        
    Returns:
        Dictionary with class distribution statistics
    """
    logger.info("Analyzing class distribution...")
    
    unique, counts = np.unique(y, return_counts=True)
    
    distribution = {}
    for u, c in zip(unique, counts):
        distribution[str(u)] = {
            'count': int(c),
            'percentage': float(c / len(y) * 100)
        }
    
    logger.info(f"Class distribution: {distribution}")
    
    return distribution
