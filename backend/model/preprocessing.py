"""
Data Preprocessing Module for CIC-IDS2017 Dataset
Handles data cleaning, encoding, and scaling
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import logging
from typing import Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataPreprocessor:
    """
    Handles all preprocessing steps for CIC-IDS2017 dataset
    """
    
    def __init__(self):
        self.label_encoder = LabelEncoder()
        self.scaler = StandardScaler()
        self.feature_columns = None
        
    def load_data(self, filepath: str) -> pd.DataFrame:
        """
        Load CSV data from file
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            Loaded dataframe
        """
        logger.info(f"Loading data from {filepath}")
        df = pd.read_csv(filepath)
        logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
        return df
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
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
        logger.info(f"Removed {original_size - len(df)} duplicate rows")
        
        # Replace infinite values with NaN
        df = df.replace([np.inf, -np.inf], np.nan)
        
        # Remove rows with NaN values
        before_nan = len(df)
        df = df.dropna()
        logger.info(f"Removed {before_nan - len(df)} rows with NaN/Inf values")
        
        logger.info(f"Final dataset size: {len(df)} rows")
        return df
    
    def encode_features(self, df: pd.DataFrame, target_column: str = 'Label') -> pd.DataFrame:
        """
        Encode categorical features
        
        Args:
            df: Input dataframe
            target_column: Name of target column
            
        Returns:
            Dataframe with encoded features
        """
        logger.info("Encoding categorical features...")
        
        # Identify categorical columns (excluding target)
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        if target_column in categorical_cols:
            categorical_cols.remove(target_column)
        
        # Encode each categorical column
        for col in categorical_cols:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            logger.info(f"Encoded column: {col}")
        
        return df
    
    def prepare_features_target(
        self, 
        df: pd.DataFrame, 
        target_column: str = 'Label'
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Separate features and target
        
        Args:
            df: Input dataframe
            target_column: Name of target column
            
        Returns:
            Tuple of (features, target)
        """
        logger.info("Separating features and target...")
        
        # Encode target variable
        y = self.label_encoder.fit_transform(df[target_column])
        
        # Get feature columns
        X = df.drop(columns=[target_column])
        self.feature_columns = X.columns.tolist()
        
        logger.info(f"Features shape: {X.shape}")
        logger.info(f"Target classes: {self.label_encoder.classes_}")
        
        return X, y
    
    def scale_features(self, X_train: pd.DataFrame, X_test: pd.DataFrame = None) -> Tuple:
        """
        Scale numeric features using StandardScaler
        
        Args:
            X_train: Training features
            X_test: Testing features (optional)
            
        Returns:
            Scaled features
        """
        logger.info("Scaling features...")
        
        # Fit and transform training data
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        if X_test is not None:
            # Transform test data
            X_test_scaled = self.scaler.transform(X_test)
            return X_train_scaled, X_test_scaled
        
        return X_train_scaled
    
    def preprocess_pipeline(
        self, 
        filepath: str, 
        target_column: str = 'Label',
        test_size: float = 0.2,
        random_state: int = 42
    ) -> Tuple:
        """
        Complete preprocessing pipeline
        
        Args:
            filepath: Path to CSV file
            target_column: Name of target column
            test_size: Proportion of test set
            random_state: Random seed
            
        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
        """
        # Load data
        df = self.load_data(filepath)
        
        # Clean data
        df = self.clean_data(df)
        
        # Encode categorical features
        df = self.encode_features(df, target_column)
        
        # Prepare features and target
        X, y = self.prepare_features_target(df, target_column)
        
        # Split data
        logger.info(f"Splitting data with test_size={test_size}")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Scale features
        X_train_scaled, X_test_scaled = self.scale_features(X_train, X_test)
        
        return X_train_scaled, X_test_scaled, y_train, y_test
    
    def save_preprocessor(self, filepath: str = 'preprocessor.pkl'):
        """
        Save preprocessor objects
        
        Args:
            filepath: Path to save file
        """
        preprocessor_dict = {
            'label_encoder': self.label_encoder,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns
        }
        joblib.dump(preprocessor_dict, filepath)
        logger.info(f"Preprocessor saved to {filepath}")
    
    def load_preprocessor(self, filepath: str = 'preprocessor.pkl'):
        """
        Load preprocessor objects
        
        Args:
            filepath: Path to load file
        """
        preprocessor_dict = joblib.load(filepath)
        self.label_encoder = preprocessor_dict['label_encoder']
        self.scaler = preprocessor_dict['scaler']
        self.feature_columns = preprocessor_dict['feature_columns']
        logger.info(f"Preprocessor loaded from {filepath}")
