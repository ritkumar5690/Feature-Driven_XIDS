"""
Sample Data Generator for XIDS
Generates synthetic network flow data for testing purposes
"""

import pandas as pd
import numpy as np
from typing import List, Dict
import random


class SampleDataGenerator:
    """
    Generates sample network flow data for testing
    """
    
    def __init__(self, seed: int = 42):
        np.random.seed(seed)
        random.seed(seed)
        
        # Define attack patterns
        self.attack_patterns = {
            'BENIGN': {
                'Flow Duration': (10000, 500000),
                'Total Fwd Packets': (5, 50),
                'Total Backward Packets': (5, 50),
                'Flow Bytes/s': (100, 10000),
                'Flow Packets/s': (10, 100),
                'Destination Port': [80, 443, 22, 21, 25, 53]
            },
            'DoS': {
                'Flow Duration': (100000, 5000000),
                'Total Fwd Packets': (100, 10000),
                'Total Backward Packets': (0, 10),
                'Flow Bytes/s': (50000, 500000),
                'Flow Packets/s': (500, 5000),
                'Destination Port': [80, 443]
            },
            'DDoS': {
                'Flow Duration': (50000, 2000000),
                'Total Fwd Packets': (50, 5000),
                'Total Backward Packets': (0, 5),
                'Flow Bytes/s': (100000, 1000000),
                'Flow Packets/s': (1000, 10000),
                'Destination Port': [80, 443, 53]
            },
            'PortScan': {
                'Flow Duration': (1000, 100000),
                'Total Fwd Packets': (1, 10),
                'Total Backward Packets': (0, 5),
                'Flow Bytes/s': (10, 1000),
                'Flow Packets/s': (1, 50),
                'Destination Port': list(range(1, 65535, 100))
            },
            'Bot': {
                'Flow Duration': (100000, 1000000),
                'Total Fwd Packets': (10, 100),
                'Total Backward Packets': (10, 100),
                'Flow Bytes/s': (1000, 50000),
                'Flow Packets/s': (50, 500),
                'Destination Port': [80, 443, 8080, 8888]
            }
        }
    
    def generate_flow(self, attack_type: str) -> Dict[str, float]:
        """
        Generate a single network flow
        
        Args:
            attack_type: Type of attack or BENIGN
            
        Returns:
            Dictionary of flow features
        """
        pattern = self.attack_patterns.get(attack_type, self.attack_patterns['BENIGN'])
        
        # Generate basic features
        flow = {
            'Destination Port': random.choice(pattern['Destination Port']),
            'Flow Duration': np.random.uniform(*pattern['Flow Duration']),
            'Total Fwd Packets': np.random.uniform(*pattern['Total Fwd Packets']),
            'Total Backward Packets': np.random.uniform(*pattern['Total Backward Packets']),
            'Flow Bytes/s': np.random.uniform(*pattern['Flow Bytes/s']),
            'Flow Packets/s': np.random.uniform(*pattern['Flow Packets/s'])
        }
        
        # Generate derived features
        total_packets = flow['Total Fwd Packets'] + flow['Total Backward Packets']
        
        flow.update({
            'Total Length of Fwd Packets': flow['Total Fwd Packets'] * np.random.uniform(64, 1500),
            'Total Length of Bwd Packets': flow['Total Backward Packets'] * np.random.uniform(64, 1500),
            'Fwd Packet Length Max': np.random.uniform(64, 1500),
            'Fwd Packet Length Min': np.random.uniform(40, 100),
            'Fwd Packet Length Mean': np.random.uniform(100, 800),
            'Fwd Packet Length Std': np.random.uniform(50, 300),
            'Bwd Packet Length Max': np.random.uniform(64, 1500),
            'Bwd Packet Length Min': np.random.uniform(40, 100),
            'Bwd Packet Length Mean': np.random.uniform(100, 800),
            'Bwd Packet Length Std': np.random.uniform(50, 300),
            'Flow IAT Mean': flow['Flow Duration'] / (total_packets + 1),
            'Flow IAT Std': np.random.uniform(100, 10000),
            'Flow IAT Max': np.random.uniform(1000, 100000),
            'Flow IAT Min': np.random.uniform(1, 1000),
            'Fwd IAT Total': flow['Flow Duration'] * 0.5,
            'Fwd IAT Mean': flow['Flow Duration'] / (flow['Total Fwd Packets'] + 1),
            'Fwd IAT Std': np.random.uniform(100, 5000),
            'Fwd IAT Max': np.random.uniform(1000, 50000),
            'Fwd IAT Min': np.random.uniform(1, 500),
            'Bwd IAT Total': flow['Flow Duration'] * 0.5,
            'Bwd IAT Mean': flow['Flow Duration'] / (flow['Total Backward Packets'] + 1),
            'Bwd IAT Std': np.random.uniform(100, 5000),
            'Bwd IAT Max': np.random.uniform(1000, 50000),
            'Bwd IAT Min': np.random.uniform(1, 500)
        })
        
        # Add label
        flow['Label'] = attack_type
        
        return flow
    
    def generate_dataset(
        self, 
        n_samples: int = 1000,
        class_distribution: Dict[str, float] = None
    ) -> pd.DataFrame:
        """
        Generate a complete dataset
        
        Args:
            n_samples: Total number of samples
            class_distribution: Distribution of classes (optional)
            
        Returns:
            DataFrame with generated samples
        """
        if class_distribution is None:
            # Default balanced distribution
            class_distribution = {
                'BENIGN': 0.5,
                'DoS': 0.15,
                'DDoS': 0.15,
                'PortScan': 0.1,
                'Bot': 0.1
            }
        
        # Generate samples for each class
        samples = []
        for attack_type, proportion in class_distribution.items():
            n_class_samples = int(n_samples * proportion)
            for _ in range(n_class_samples):
                samples.append(self.generate_flow(attack_type))
        
        # Create DataFrame
        df = pd.DataFrame(samples)
        
        # Shuffle
        df = df.sample(frac=1).reset_index(drop=True)
        
        return df
    
    def save_dataset(self, filepath: str, n_samples: int = 1000):
        """
        Generate and save dataset to CSV
        
        Args:
            filepath: Path to save CSV
            n_samples: Number of samples to generate
        """
        df = self.generate_dataset(n_samples)
        df.to_csv(filepath, index=False)
        print(f"Generated {len(df)} samples and saved to {filepath}")
        print(f"\nClass distribution:")
        print(df['Label'].value_counts())


def main():
    """
    Generate sample data for testing
    """
    generator = SampleDataGenerator()
    
    # Generate small test dataset
    print("Generating test dataset...")
    generator.save_dataset('sample_data.csv', n_samples=1000)
    
    # Generate single sample for API testing
    print("\n" + "="*60)
    print("Sample flow for API testing:")
    print("="*60)
    sample = generator.generate_flow('DDoS')
    
    # Remove label for API request
    label = sample.pop('Label')
    
    print(f"\nTrue Label: {label}")
    print(f"\nFeatures:")
    for key, value in sample.items():
        print(f"  {key}: {value:.2f}")
    
    # Create JSON format
    import json
    print(f"\nJSON format for API:")
    print(json.dumps({"features": sample}, indent=2))


if __name__ == "__main__":
    main()
