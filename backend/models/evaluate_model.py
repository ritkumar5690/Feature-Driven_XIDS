"""
Model Evaluation Module for XIDS
Provides comprehensive model evaluation metrics
"""

import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score,
    roc_curve, auc
)
import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)


def evaluate_model(y_true: np.ndarray, y_pred: np.ndarray) -> Dict:
    """
    Comprehensive model evaluation
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        
    Returns:
        Dictionary with evaluation metrics
    """
    logger.info("Evaluating model performance...")
    
    metrics = {
        'accuracy': float(accuracy_score(y_true, y_pred)),
        'precision': float(precision_score(y_true, y_pred, average='weighted', zero_division=0)),
        'recall': float(recall_score(y_true, y_pred, average='weighted', zero_division=0)),
        'f1_score': float(f1_score(y_true, y_pred, average='weighted', zero_division=0)),
    }
    
    logger.info(f"Metrics: {metrics}")
    
    return metrics


def get_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """
    Get confusion matrix
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        
    Returns:
        Confusion matrix
    """
    cm = confusion_matrix(y_true, y_pred)
    logger.info("Confusion matrix computed")
    return cm


def get_classification_report(y_true: np.ndarray, y_pred: np.ndarray, labels: list = None) -> str:
    """
    Get detailed classification report
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        labels: List of label names
        
    Returns:
        Classification report as string
    """
    report = classification_report(y_true, y_pred, labels=labels, zero_division=0)
    logger.info("Classification report generated")
    return report


def evaluate_multiclass(y_true: np.ndarray, y_pred: np.ndarray) -> Dict:
    """
    Evaluate multiclass classification
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        
    Returns:
        Dictionary with detailed evaluation metrics
    """
    logger.info("Evaluating multiclass classification...")
    
    unique_classes = np.unique(y_true)
    
    evaluation = {
        'overall_accuracy': float(accuracy_score(y_true, y_pred)),
        'num_classes': len(unique_classes),
        'class_metrics': {}
    }
    
    # Per-class metrics
    for cls in unique_classes:
        cls_mask = (y_true == cls)
        pred_mask = (y_pred == cls)
        
        tp = np.sum(cls_mask & pred_mask)
        fp = np.sum(pred_mask & ~cls_mask)
        fn = np.sum(cls_mask & ~pred_mask)
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        evaluation['class_metrics'][str(cls)] = {
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1),
            'support': int(np.sum(cls_mask))
        }
    
    return evaluation


def compare_models(models_results: Dict[str, Dict]) -> Dict:
    """
    Compare multiple model results
    
    Args:
        models_results: Dictionary of model names to evaluation results
        
    Returns:
        Comparison dictionary
    """
    logger.info("Comparing models...")
    
    comparison = {}
    best_f1 = -1
    best_model = None
    
    for model_name, metrics in models_results.items():
        f1 = metrics.get('f1_score', 0)
        comparison[model_name] = metrics
        
        if f1 > best_f1:
            best_f1 = f1
            best_model = model_name
    
    comparison['best_model'] = best_model
    comparison['best_f1_score'] = best_f1
    
    logger.info(f"Best model: {best_model} (F1: {best_f1:.4f})")
    
    return comparison
