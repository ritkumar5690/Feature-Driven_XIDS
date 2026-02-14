"""
Preprocessing Pipeline for XIDS
Orchestrates the complete preprocessing workflow
"""

import logging
from typing import Tuple
from sklearn.model_selection import train_test_split

from .load_data import load_data
from .clean_data import clean_data
from .encode_normalize import encode_categorical_features, normalize_numeric_features

logger = logging.getLogger(__name__)


def preprocess_pipeline(
    filepath: str,
    target_column: str = 'Label',
    test_size: float = 0.2,
    random_state: int = 42,
    normalization_method: str = 'standard'
) -> Tuple:
    """
    Complete preprocessing pipeline for XIDS
    
    Steps:
    1. Load data from file
    2. Clean data (remove duplicates, handle missing values)
    3. Encode categorical features
    4. Separate features and target
    5. Split into train/test sets
    6. Normalize features
    
    Args:
        filepath: Path to data file
        target_column: Name of target column
        test_size: Proportion of test set (0-1)
        random_state: Random seed for reproducibility
        normalization_method: 'standard' or 'minmax'
        
    Returns:
        Tuple of (X_train, X_test, y_train, y_test)
        where X_train and X_test are normalized numpy arrays
    """
    logger.info("=" * 60)
    logger.info("Starting Preprocessing Pipeline")
    logger.info("=" * 60)
    
    # Step 1: Load data
    logger.info("\nStep 1: Loading data...")
    df = load_data(filepath)
    
    # Step 2: Clean data
    logger.info("\nStep 2: Cleaning data...")
    df = clean_data(df)
    
    # Step 3: Encode categorical features
    logger.info("\nStep 3: Encoding categorical features...")
    df, encoders = encode_categorical_features(df, target_column)
    
    # Step 4: Separate features and target
    logger.info("\nStep 4: Separating features and target...")
    y = df[target_column]
    X = df.drop(columns=[target_column])
    logger.info(f"Features shape: {X.shape}")
    logger.info(f"Target shape: {y.shape}")
    
    # Step 5: Split data
    logger.info("\nStep 5: Splitting data into train/test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    logger.info(f"Train set: {X_train.shape}")
    logger.info(f"Test set: {X_test.shape}")
    
    # Step 6: Normalize features
    logger.info("\nStep 6: Normalizing features...")
    X_train_norm, X_test_norm = normalize_numeric_features(
        X_train, X_test, method=normalization_method
    )
    
    logger.info("\n" + "=" * 60)
    logger.info("Preprocessing Pipeline Completed!")
    logger.info("=" * 60)
    
    return X_train_norm, X_test_norm, y_train.values, y_test.values
