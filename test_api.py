"""
Sample Test Script for XIDS API
Tests prediction and explanation endpoints
"""

import requests
import json

# API Base URL
API_URL = "http://localhost:8000"

# Sample network flow features
sample_features = {
    "Destination Port": 80,
    "Flow Duration": 120000,
    "Total Fwd Packets": 10,
    "Total Backward Packets": 8,
    "Total Length of Fwd Packets": 5120,
    "Total Length of Bwd Packets": 2048,
    "Fwd Packet Length Max": 1024,
    "Fwd Packet Length Min": 64,
    "Fwd Packet Length Mean": 512.0,
    "Fwd Packet Length Std": 128.5,
    "Bwd Packet Length Max": 512,
    "Bwd Packet Length Min": 64,
    "Bwd Packet Length Mean": 256.0,
    "Bwd Packet Length Std": 64.2,
    "Flow Bytes/s": 1500.5,
    "Flow Packets/s": 150.0,
    "Flow IAT Mean": 100.5,
    "Flow IAT Std": 50.2,
    "Flow IAT Max": 200,
    "Flow IAT Min": 10
}


def test_health():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("Testing Health Endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def test_prediction():
    """Test prediction endpoint"""
    print("\n" + "="*60)
    print("Testing Prediction Endpoint")
    print("="*60)
    
    try:
        payload = {"features": sample_features}
        response = requests.post(
            f"{API_URL}/predict",
            json=payload,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\nPrediction: {result['prediction']}")
            print(f"Confidence: {result['confidence']*100:.2f}%")
            print(f"\nProbabilities:")
            for class_name, prob in result.get('probabilities', {}).items():
                print(f"  {class_name}: {prob*100:.2f}%")
            return True
        else:
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def test_explanation():
    """Test explanation endpoint"""
    print("\n" + "="*60)
    print("Testing Explanation Endpoint")
    print("="*60)
    
    try:
        payload = {"features": sample_features}
        response = requests.post(
            f"{API_URL}/explain",
            json=payload,
            params={"top_n": 5},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\nPrediction: {result['prediction']}")
            print(f"Base Value: {result['base_value']:.6f}")
            print(f"\nTop 5 Contributing Features:")
            for i, feat in enumerate(result['top_features'], 1):
                impact = "+" if feat['impact'] > 0 else ""
                print(f"  {i}. {feat['feature']}: {impact}{feat['impact']:.6f}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def test_detailed_prediction():
    """Test detailed prediction endpoint"""
    print("\n" + "="*60)
    print("Testing Detailed Prediction Endpoint")
    print("="*60)
    
    try:
        payload = {"features": sample_features}
        response = requests.post(
            f"{API_URL}/predict/details",
            json=payload,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\nPrediction: {result['prediction']}")
            print(f"Confidence: {result['confidence']*100:.2f}%")
            print(f"Is Attack: {result['is_attack']}")
            print(f"Threat Level: {result['threat_level']}")
            print(f"\nTop 3 Predictions:")
            for class_name, prob in result.get('top_3_predictions', {}).items():
                print(f"  {class_name}: {prob*100:.2f}%")
            return True
        else:
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("XIDS API Test Suite")
    print("="*60)
    print(f"Testing API at: {API_URL}")
    
    results = {
        "Health Check": test_health(),
        "Prediction": test_prediction(),
        "Detailed Prediction": test_detailed_prediction(),
        "Explanation": test_explanation()
    }
    
    print("\n" + "="*60)
    print("Test Results Summary")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    print("\n" + "="*60)
    if all_passed:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed. Check the output above.")
    print("="*60)


if __name__ == "__main__":
    main()
