"""
Configuration Module for XIDS
Central configuration for all components
"""

import os
from pathlib import Path
import logging

# Logging configuration
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
BACKEND_ROOT = PROJECT_ROOT / 'backend'
DATA_ROOT = BACKEND_ROOT / 'data'
RAW_DATA = DATA_ROOT / 'raw'
PROCESSED_DATA = DATA_ROOT / 'processed'
MODELS_ROOT = BACKEND_ROOT / 'models'
SAVED_MODELS = MODELS_ROOT / 'saved_models'
RESULTS_ROOT = PROJECT_ROOT / 'results'
METRICS_ROOT = RESULTS_ROOT / 'metrics'
PLOTS_ROOT = RESULTS_ROOT / 'plots'
EXPLANATIONS_ROOT = RESULTS_ROOT / 'explanations'

# Data configuration
DATA_CONFIG = {
    'train_file': 'KDDTrain+.txt',
    'test_file': 'KDDTest+.txt',
    'target_column': 'Label',
    'test_size': 0.2,
    'random_state': 42,
    'normalization_method': 'standard'
}

# Model configuration
MODEL_CONFIG = {
    'xgboost': {
        'n_estimators': 100,
        'max_depth': 8,
        'learning_rate': 0.1,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'random_state': 42
    },
    'random_forest': {
        'n_estimators': 100,
        'max_depth': 15,
        'min_samples_split': 5,
        'min_samples_leaf': 2,
        'random_state': 42,
        'n_jobs': -1
    },
    'decision_tree': {
        'max_depth': 10,
        'min_samples_split': 5,
        'min_samples_leaf': 2,
        'random_state': 42
    }
}

# Feature selection configuration
FEATURE_CONFIG = {
    'selection_method': 'forest',  # 'kbest', 'mutual_info', 'forest'
    'num_features': 20,
    'outlier_threshold': 3.0
}

# Explainability configuration
EXPLAINABILITY_CONFIG = {
    'shap_type': 'tree',  # 'tree' or 'kernel'
    'lime_samples': 5000,
    'lime_features': 10,
    'rule_extraction': True
}

# API configuration
API_CONFIG = {
    'host': '0.0.0.0',
    'port': 8000,
    'reload': True,
    'debug': True
}

# Ensure all paths exist
def create_directories():
    """Create all necessary directories if they don't exist"""
    directories = [
        RAW_DATA, PROCESSED_DATA, MODELS_ROOT, SAVED_MODELS,
        METRICS_ROOT, PLOTS_ROOT, EXPLANATIONS_ROOT
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Ensured directory exists: {directory}")


# Initialize directories on import
create_directories()

logger.info(f"XIDS Configuration Loaded")
logger.info(f"Project Root: {PROJECT_ROOT}")
logger.info(f"Data Root: {DATA_ROOT}")
logger.info(f"Models Root: {MODELS_ROOT}")
