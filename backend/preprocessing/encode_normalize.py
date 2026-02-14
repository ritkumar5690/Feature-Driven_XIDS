"""
Encoding and Normalization Module for XIDS
Handles categorical encoding and feature normalization
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
import joblib
import logging
from typing import Tuple, Dict, List

logger = logging.getLogger(__name__)


class FeatureEncoder:
    """Handle categorical encoding"""
    
    def __init__(self):
        self.encoders: Dict[str, LabelEncoder] = {}
        self.categorical_cols: List[str] = []
    
    def fit_encode(self, df: pd.DataFrame, target_column: str = 'Label') -> pd.DataFrame:
        """
        Fit encoders and encode categorical features
        
        Args:
            df: Input dataframe
            target_column: Name of target column to exclude
            
        Returns:
            Dataframe with encoded categorical features
        """
        logger.info("Encoding categorical features...")
        
        # Identify categorical columns
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        if target_column in categorical_cols:
            categorical_cols.remove(target_column)
        
        self.categorical_cols = categorical_cols
        
        # Fit and transform each categorical column
        for col in categorical_cols:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            self.encoders[col] = le
            logger.info(f"Encoded column: {col}")
        
        return df
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform using fitted encoders"""
        for col in self.categorical_cols:
            if col in self.encoders:
                df[col] = self.encoders[col].transform(df[col].astype(str))
        return df


class FeatureNormalizer:
    """Handle feature scaling and normalization"""
    
    def __init__(self, method: str = 'standard'):
        """
        Initialize normalizer
        
        Args:
            method: 'standard' for StandardScaler or 'minmax' for MinMaxScaler
        """
        self.method = method
        if method == 'standard':
            self.scaler = StandardScaler()
        elif method == 'minmax':
            self.scaler = MinMaxScaler()
        else:
            logger.warning(f"Unknown method: {method}, using standard")
            self.scaler = StandardScaler()
    
    def fit_transform(self, X: pd.DataFrame) -> np.ndarray:
        """Fit and transform features"""
        logger.info(f"Scaling features using {self.method} normalization")
        return self.scaler.fit_transform(X)
    
    def transform(self, X: pd.DataFrame) -> np.ndarray:
        """Transform using fitted scaler"""
        return self.scaler.transform(X)


def encode_categorical_features(
    df: pd.DataFrame, 
    target_column: str = 'Label'
) -> Tuple[pd.DataFrame, Dict[str, LabelEncoder]]:
    """
    Encode all categorical features in dataframe
    
    Args:
        df: Input dataframe
        target_column: Name of target column
        
    Returns:
        Tuple of (encoded_dataframe, encoders_dict)
    """
    encoder = FeatureEncoder()
    df_encoded = encoder.fit_encode(df, target_column)
    return df_encoded, encoder.encoders


def normalize_numeric_features(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame = None,
    method: str = 'standard'
) -> Tuple[np.ndarray, np.ndarray] or np.ndarray:
    """
    Normalize numeric features
    
    Args:
        X_train: Training features
        X_test: Test features (optional)
        method: 'standard' or 'minmax'
        
    Returns:
        Normalized training features and test features (if provided)
    """
    normalizer = FeatureNormalizer(method)
    X_train_norm = normalizer.fit_transform(X_train)
    
    if X_test is not None:
        X_test_norm = normalizer.transform(X_test)
        return X_train_norm, X_test_norm
    
    return X_train_norm
