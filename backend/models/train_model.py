"""
Model Training Module for XIDS
Trains XGBoost and Random Forest models on CIC-IDS2017 dataset
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score,
    confusion_matrix,
    classification_report
)
import xgboost as xgb
import joblib
import logging
from typing import Dict, Any
import os
from preprocessing import DataPreprocessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class XIDSTrainer:
    """
    Trains and evaluates intrusion detection models
    """
    
    def __init__(self):
        self.xgb_model = None
        self.rf_model = None
        self.preprocessor = DataPreprocessor()
        self.best_model = None
        self.model_metrics = {}
        
    def train_xgboost(
        self, 
        X_train: np.ndarray, 
        y_train: np.ndarray,
        params: Dict = None
    ) -> xgb.XGBClassifier:
        """
        Train XGBoost classifier
        
        Args:
            X_train: Training features
            y_train: Training labels
            params: XGBoost parameters
            
        Returns:
            Trained XGBoost model
        """
        logger.info("Training XGBoost model...")
        
        # Default parameters optimized for intrusion detection
        if params is None:
            params = {
                'objective': 'multi:softmax',
                'num_class': len(np.unique(y_train)),
                'max_depth': 10,
                'learning_rate': 0.1,
                'n_estimators': 200,
                'subsample': 0.8,
                'colsample_bytree': 0.8,
                'random_state': 42,
                'tree_method': 'hist',
                'eval_metric': 'mlogloss'
            }
        
        # Initialize and train model
        self.xgb_model = xgb.XGBClassifier(**params)
        self.xgb_model.fit(X_train, y_train)
        
        logger.info("XGBoost training completed")
        return self.xgb_model
    
    def train_random_forest(
        self, 
        X_train: np.ndarray, 
        y_train: np.ndarray,
        params: Dict = None
    ) -> RandomForestClassifier:
        """
        Train Random Forest classifier (baseline)
        
        Args:
            X_train: Training features
            y_train: Training labels
            params: RandomForest parameters
            
        Returns:
            Trained RandomForest model
        """
        logger.info("Training Random Forest model...")
        
        # Default parameters
        if params is None:
            params = {
                'n_estimators': 100,
                'max_depth': 20,
                'min_samples_split': 5,
                'min_samples_leaf': 2,
                'random_state': 42,
                'n_jobs': -1
            }
        
        # Initialize and train model
        self.rf_model = RandomForestClassifier(**params)
        self.rf_model.fit(X_train, y_train)
        
        logger.info("Random Forest training completed")
        return self.rf_model
    
    def evaluate_model(
        self, 
        model: Any, 
        X_test: np.ndarray, 
        y_test: np.ndarray,
        model_name: str
    ) -> Dict:
        """
        Evaluate model performance
        
        Args:
            model: Trained model
            X_test: Test features
            y_test: Test labels
            model_name: Name of the model
            
        Returns:
            Dictionary containing evaluation metrics
        """
        logger.info(f"Evaluating {model_name}...")
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        metrics = {
            'model_name': model_name,
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_test, y_pred, average='weighted', zero_division=0),
            'f1_score': f1_score(y_test, y_pred, average='weighted', zero_division=0),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
        }
        
        # Log metrics
        logger.info(f"\n{model_name} Performance:")
        logger.info(f"Accuracy:  {metrics['accuracy']:.4f}")
        logger.info(f"Precision: {metrics['precision']:.4f}")
        logger.info(f"Recall:    {metrics['recall']:.4f}")
        logger.info(f"F1-Score:  {metrics['f1_score']:.4f}")
        
        # Detailed classification report
        class_names = self.preprocessor.label_encoder.classes_
        logger.info(f"\n{classification_report(y_test, y_pred, target_names=class_names)}")
        
        return metrics
    
    def select_best_model(self) -> Any:
        """
        Select best model based on F1-score
        
        Returns:
            Best performing model
        """
        xgb_f1 = self.model_metrics.get('xgboost', {}).get('f1_score', 0)
        rf_f1 = self.model_metrics.get('random_forest', {}).get('f1_score', 0)
        
        if xgb_f1 >= rf_f1:
            logger.info(f"XGBoost selected as best model (F1: {xgb_f1:.4f})")
            self.best_model = self.xgb_model
            return self.xgb_model
        else:
            logger.info(f"Random Forest selected as best model (F1: {rf_f1:.4f})")
            self.best_model = self.rf_model
            return self.rf_model
    
    def save_model(self, filepath: str = 'saved_model.pkl'):
        """
        Save the best model
        
        Args:
            filepath: Path to save model
        """
        if self.best_model is None:
            raise ValueError("No model to save. Train a model first.")
        
        model_package = {
            'model': self.best_model,
            'metrics': self.model_metrics,
            'feature_columns': self.preprocessor.feature_columns
        }
        
        joblib.dump(model_package, filepath)
        logger.info(f"Model saved to {filepath}")
    
    def train_pipeline(
        self, 
        data_filepath: str,
        save_dir: str = '.'
    ):
        """
        Complete training pipeline
        
        Args:
            data_filepath: Path to CIC-IDS2017 CSV file
            save_dir: Directory to save models
        """
        logger.info("=" * 60)
        logger.info("Starting XIDS Training Pipeline")
        logger.info("=" * 60)
        
        # Step 1: Preprocess data
        logger.info("\nStep 1: Data Preprocessing")
        X_train, X_test, y_train, y_test = self.preprocessor.preprocess_pipeline(
            data_filepath
        )
        
        # Step 2: Train XGBoost
        logger.info("\nStep 2: Training XGBoost")
        self.train_xgboost(X_train, y_train)
        xgb_metrics = self.evaluate_model(
            self.xgb_model, X_test, y_test, 'XGBoost'
        )
        self.model_metrics['xgboost'] = xgb_metrics
        
        # Step 3: Train Random Forest (baseline)
        logger.info("\nStep 3: Training Random Forest (Baseline)")
        self.train_random_forest(X_train, y_train)
        rf_metrics = self.evaluate_model(
            self.rf_model, X_test, y_test, 'Random Forest'
        )
        self.model_metrics['random_forest'] = rf_metrics
        
        # Step 4: Select best model
        logger.info("\nStep 4: Model Selection")
        self.select_best_model()
        
        # Step 5: Save models and preprocessor
        logger.info("\nStep 5: Saving Models")
        model_path = os.path.join(save_dir, 'saved_model.pkl')
        preprocessor_path = os.path.join(save_dir, 'preprocessor.pkl')
        
        self.save_model(model_path)
        self.preprocessor.save_preprocessor(preprocessor_path)
        
        logger.info("\n" + "=" * 60)
        logger.info("Training Pipeline Completed Successfully!")
        logger.info("=" * 60)
        
        return self.model_metrics


def main():
    """
    Main training function
    """
    # Example usage - Update with your dataset path
    DATA_PATH = "path/to/CIC-IDS2017.csv"  # Update this path
    SAVE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Check if data file exists
    if not os.path.exists(DATA_PATH):
        logger.error(f"Dataset not found at {DATA_PATH}")
        logger.info("Please download CIC-IDS2017 dataset and update DATA_PATH")
        logger.info("Dataset: https://www.unb.ca/cic/datasets/ids-2017.html")
        return
    
    # Initialize trainer
    trainer = XIDSTrainer()
    
    # Run training pipeline
    metrics = trainer.train_pipeline(DATA_PATH, SAVE_DIR)
    
    # Print final summary
    print("\n" + "=" * 60)
    print("FINAL MODEL COMPARISON")
    print("=" * 60)
    for model_name, model_metrics in metrics.items():
        print(f"\n{model_name.upper()}:")
        print(f"  Accuracy:  {model_metrics['accuracy']:.4f}")
        print(f"  Precision: {model_metrics['precision']:.4f}")
        print(f"  Recall:    {model_metrics['recall']:.4f}")
        print(f"  F1-Score:  {model_metrics['f1_score']:.4f}")


if __name__ == "__main__":
    main()
