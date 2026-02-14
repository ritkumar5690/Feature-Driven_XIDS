"""
Generate Sample CICIDS2017 Data and Train XIDS Model
"""

import pandas as pd
import numpy as np
import os
import sys

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from train import XIDSTrainer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_sample_cicids2017_data(n_samples=5000, filepath='cicids2017_sample.csv'):
    """
    Generate sample CICIDS2017 dataset with realistic features
    
    Args:
        n_samples: Number of samples to generate
        filepath: Path to save the CSV
    """
    logger.info(f"Generating {n_samples} samples of CICIDS2017-like data...")
    
    # CIC-IDS2017 feature list (80 features)
    features = [
        'Destination Port', 'Flow Duration', 'Total Fwd Packets', 'Total Backward Packets',
        'Total Length of Fwd Packets', 'Total Length of Bwd Packets', 'Fwd Packet Length Max',
        'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Fwd Packet Length Std',
        'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean',
        'Bwd Packet Length Std', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean',
        'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min', 'Fwd IAT Total', 'Fwd IAT Mean',
        'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Total', 'Bwd IAT Mean',
        'Bwd IAT Std', 'Bwd IAT Max', 'Bwd IAT Min', 'Fwd PSH Flags', 'Bwd PSH Flags',
        'Fwd URG Flags', 'Bwd URG Flags', 'Fwd Header Length', 'Bwd Header Length',
        'Fwd Packets/s', 'Bwd Packets/s', 'Min Packet Length', 'Max Packet Length',
        'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance',
        'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count',
        'ACK Flag Count', 'URG Flag Count', 'CWE Flag Count', 'ECE Flag Count',
        'Down/Up Ratio', 'Average Packet Size', 'Avg Fwd Segment Size',
        'Avg Bwd Segment Size', 'Fwd Header Length', 'Fwd Avg Bytes/Bulk',
        'Fwd Avg Packets/Bulk', 'Fwd Avg Bulk Rate', 'Bwd Avg Bytes/Bulk',
        'Bwd Avg Packets/Bulk', 'Bwd Avg Bulk Rate', 'Subflow Fwd Packets',
        'Subflow Fwd Bytes', 'Subflow Bwd Packets', 'Subflow Bwd Bytes',
        'Init Win bytes forward', 'Init Win bytes backward', 'Fwd Act Data Pkts',
        'Fwd Seg Size Min', 'Active Mean', 'Active Std', 'Active Max', 'Active Min',
        'Idle Mean', 'Idle Std', 'Idle Max', 'Idle Min'
    ]
    
    # Attack types
    attack_types = ['BENIGN', 'DoS Hulk', 'DoS SlowHTTP', 'SSH-Bruteforce', 'FTP-Bruteforce', 'Bot']
    
    # Generate random data
    np.random.seed(42)
    data = {}
    
    # Generate features
    for feature in features:
        data[feature] = np.random.exponential(100, n_samples)
    
    # Generate labels (with class imbalance like real data)
    labels = np.random.choice(
        attack_types,
        size=n_samples,
        p=[0.70, 0.10, 0.08, 0.05, 0.05, 0.02]  # Realistic distribution
    )
    data['Label'] = labels
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    df.to_csv(filepath, index=False)
    logger.info(f"Sample data saved to {filepath}")
    logger.info(f"Shape: {df.shape}")
    logger.info(f"\nLabel distribution:")
    logger.info(df['Label'].value_counts())
    
    return filepath


def train_xids_model(data_filepath, model_save_dir=None):
    """
    Train the XIDS model
    
    Args:
        data_filepath: Path to training data
        model_save_dir: Directory to save model
    """
    if model_save_dir is None:
        model_save_dir = os.path.dirname(os.path.abspath(__file__))
    
    logger.info("="*70)
    logger.info("XIDS MODEL TRAINING - CICIDS2017 DATASET")
    logger.info("="*70)
    
    # Initialize trainer
    trainer = XIDSTrainer()
    
    # Run training pipeline
    metrics = trainer.train_pipeline(
        data_filepath=data_filepath,
        save_dir=model_save_dir
    )
    
    # Print summary
    logger.info("\n" + "="*70)
    logger.info("TRAINING SUMMARY")
    logger.info("="*70)
    
    for model_name, model_metrics in metrics.items():
        logger.info(f"\n{model_name.upper()} METRICS:")
        logger.info(f"  Accuracy:  {model_metrics['accuracy']:.4f}")
        logger.info(f"  Precision: {model_metrics['precision']:.4f}")
        logger.info(f"  Recall:    {model_metrics['recall']:.4f}")
        logger.info(f"  F1-Score:  {model_metrics['f1_score']:.4f}")
    
    logger.info("\n" + "="*70)
    logger.info("Model training completed successfully!")
    logger.info(f"Model saved to: {model_save_dir}")
    logger.info("="*70)


if __name__ == "__main__":
    # Generate sample data
    sample_data_path = generate_sample_cicids2017_data(n_samples=5000)
    
    # Train model
    model_dir = os.path.dirname(os.path.abspath(__file__))
    train_xids_model(sample_data_path, model_dir)
    
    logger.info("\n✅ Model training completed!")
    logger.info("Model files are ready for use by the XIDS backend API")
