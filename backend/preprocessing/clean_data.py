"""
Data Cleaning Module for XIDS
Handles data validation and cleaning operations
"""

import pandas as pd
import numpy as np
import logging
from typing import Tuple

logger = logging.getLogger(__name__)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean data by removing duplicates, NaN, and infinite values
    
    Args:
        df: Input dataframe
        
    Returns:
        Cleaned dataframe
    """
    logger.info("Starting data cleaning...")
    
    # Store original size
    original_size = len(df)
    
    # Remove duplicate rows
    df = df.drop_duplicates()
    duplicates_removed = original_size - len(df)
    if duplicates_removed > 0:
        logger.info(f"Removed {duplicates_removed} duplicate rows")
    
    # Replace infinite values with NaN
    df = df.replace([np.inf, -np.inf], np.nan)
    
    # Remove rows with NaN values
    before_nan = len(df)
    df = df.dropna()
    nan_removed = before_nan - len(df)
    if nan_removed > 0:
        logger.info(f"Removed {nan_removed} rows with NaN/Inf values")
    
    logger.info(f"Final dataset size: {len(df)} rows")
    
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows from dataframe
    
    Args:
        df: Input dataframe
        
    Returns:
        Dataframe without duplicates
    """
    initial_size = len(df)
    df = df.drop_duplicates()
    logger.info(f"Removed {initial_size - len(df)} duplicate rows")
    return df


def handle_missing_values(df: pd.DataFrame, strategy: str = 'drop') -> pd.DataFrame:
    """
    Handle missing values in dataframe
    
    Args:
        df: Input dataframe
        strategy: 'drop' or 'mean' for imputation
        
    Returns:
        Dataframe with missing values handled
    """
    if strategy == 'drop':
        return df.dropna()
    elif strategy == 'mean':
        return df.fillna(df.mean(numeric_only=True))
    else:
        logger.warning(f"Unknown strategy: {strategy}, using drop")
        return df.dropna()


def handle_infinite_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Replace infinite values with NaN and then handle
    
    Args:
        df: Input dataframe
        
    Returns:
        Dataframe without infinite values
    """
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()
    return df
