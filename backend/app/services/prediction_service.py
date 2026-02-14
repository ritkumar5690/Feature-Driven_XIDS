"""
Prediction Service
Handles prediction logic for network flows
"""

import numpy as np
import pandas as pd
import logging
from typing import Dict, Tuple, List
from .model_loader import model_loader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PredictionService:
    """
    Service for making predictions on network flows
    """
    
    def __init__(self):
        self.model_loader = model_loader
    
    def prepare_features(self, features: Dict[str, float]) -> np.ndarray:
        """
        Prepare features for prediction
        
        Args:
            features: Dictionary of feature names to values
            
        Returns:
            Prepared feature array
        """
        try:
            # Get expected feature columns
            expected_features = self.model_loader.get_feature_columns()
            
            # Create DataFrame with expected columns
            feature_df = pd.DataFrame([features])
            
            # Check for missing features
            missing_features = set(expected_features) - set(feature_df.columns)
            if missing_features:
                logger.warning(f"Missing features: {missing_features}")
                # Fill missing features with 0
                for feat in missing_features:
                    feature_df[feat] = 0
            
            # Ensure correct column order
            feature_df = feature_df[expected_features]
            
            # Scale features
            scaler = self.model_loader.get_scaler()
            features_scaled = scaler.transform(feature_df)
            
            return features_scaled
            
        except Exception as e:
            logger.error(f"Error preparing features: {str(e)}")
            raise
    
    def predict(self, features: Dict[str, float]) -> Tuple[str, float, Dict[str, float]]:
        """
        Make prediction for given features
        
        Args:
            features: Dictionary of feature names to values
            
        Returns:
            Tuple of (prediction, confidence, probabilities)
        """
        try:
            # Prepare features
            X = self.prepare_features(features)
            
            # Get model
            model = self.model_loader.get_model()
            
            # Make prediction
            prediction_encoded = model.predict(X)[0]
            
            # Get probabilities if available
            probabilities = {}
            confidence = 1.0
            
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(X)[0]
                confidence = float(np.max(proba))
                
                # Create probability dictionary
                label_encoder = self.model_loader.get_label_encoder()
                class_names = label_encoder.classes_
                probabilities = {
                    class_name: float(prob) 
                    for class_name, prob in zip(class_names, proba)
                }
            
            # Decode prediction
            label_encoder = self.model_loader.get_label_encoder()
            prediction = label_encoder.inverse_transform([prediction_encoded])[0]
            
            logger.info(f"Prediction: {prediction} (confidence: {confidence:.4f})")
            
            return prediction, confidence, probabilities
            
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise
    
    def batch_predict(self, features_list: List[Dict[str, float]]) -> List[Tuple[str, float]]:
        """
        Make predictions for multiple flows
        
        Args:
            features_list: List of feature dictionaries
            
        Returns:
            List of (prediction, confidence) tuples
        """
        results = []
        
        for features in features_list:
            try:
                prediction, confidence, _ = self.predict(features)
                results.append((prediction, confidence))
            except Exception as e:
                logger.error(f"Error in batch prediction: {str(e)}")
                results.append(("ERROR", 0.0))
        
        return results
    
    def get_prediction_details(self, features: Dict[str, float]) -> Dict:
        """
        Get detailed prediction information
        
        Args:
            features: Dictionary of feature names to values
            
        Returns:
            Dictionary with detailed prediction info
        """
        try:
            prediction, confidence, probabilities = self.predict(features)
            
            # Sort probabilities by value
            sorted_probs = dict(
                sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
            )
            
            return {
                "prediction": prediction,
                "confidence": confidence,
                "probabilities": probabilities,
                "top_3_predictions": dict(list(sorted_probs.items())[:3]),
                "is_attack": prediction != "BENIGN",
                "threat_level": self._get_threat_level(prediction, confidence)
            }
            
        except Exception as e:
            logger.error(f"Error getting prediction details: {str(e)}")
            raise
    
    def _get_threat_level(self, prediction: str, confidence: float) -> str:
        """
        Determine threat level based on prediction and confidence
        
        Args:
            prediction: Predicted class
            confidence: Confidence score
            
        Returns:
            Threat level string
        """
        if prediction == "BENIGN":
            return "NONE"
        
        if confidence >= 0.9:
            return "CRITICAL"
        elif confidence >= 0.7:
            return "HIGH"
        elif confidence >= 0.5:
            return "MEDIUM"
        else:
            return "LOW"


# Global instance
prediction_service = PredictionService()
