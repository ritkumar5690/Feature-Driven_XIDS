"""
Data Loading Module for XIDS
Handles loading data from various sources
"""

import pandas as pd
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load CSV or TXT data from file
    
    Args:
        filepath: Path to data file (CSV or TXT)
        
    Returns:
        Loaded dataframe
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file format is unsupported
    """
    file_path = Path(filepath)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found: {filepath}")
    
    logger.info(f"Loading data from {filepath}")
    
    if file_path.suffix.lower() == '.csv':
        df = pd.read_csv(filepath)
    elif file_path.suffix.lower() in ['.txt', '.data']:
        # Handle space/comma separated files
        df = pd.read_csv(filepath, sep=None, engine='python')
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")
    
    logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
    
    return df


def load_kdd_train_data(filepath: str = 'data/raw/KDDTrain+.txt') -> pd.DataFrame:
    """
    Load KDD Train dataset
    
    Args:
        filepath: Path to KDDTrain+.txt
        
    Returns:
        Loaded KDD Train dataframe
    """
    return load_data(filepath)


def load_kdd_test_data(filepath: str = 'data/raw/KDDTest+.txt') -> pd.DataFrame:
    """
    Load KDD Test dataset
    
    Args:
        filepath: Path to KDDTest+.txt
        
    Returns:
        Loaded KDD Test dataframe
    """
    return load_data(filepath)
