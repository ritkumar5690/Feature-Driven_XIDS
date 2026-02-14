# XIDS - Technical Documentation

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Component Details](#component-details)
3. [API Reference](#api-reference)
4. [Model Training Pipeline](#model-training-pipeline)
5. [Deployment Guide](#deployment-guide)
6. [Performance Optimization](#performance-optimization)
7. [Troubleshooting](#troubleshooting)

---

## System Architecture

### Overview
XIDS is a microservices-based architecture with three main components:

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                    (Streamlit Frontend)                      │
│                      Port: 8501                              │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                       API Layer                              │
│                    (FastAPI Backend)                         │
│                      Port: 8000                              │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Prediction  │  │ Explanation  │  │    Model     │      │
│  │   Service    │  │   Service    │  │   Loader     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     ML Components                            │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   XGBoost    │  │     SHAP     │  │    Scaler    │      │
│  │    Model     │  │  Explainer   │  │   Encoder    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Backend:**
- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI
- **Pydantic**: Data validation using Python type annotations
- **XGBoost**: Gradient boosting library for ML
- **Scikit-learn**: Machine learning utilities
- **SHAP**: Explainability framework
- **Joblib**: Model serialization

**Frontend:**
- **Streamlit**: Rapid web app development framework
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation
- **Requests**: HTTP library for API calls

**Infrastructure:**
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration

---

## Component Details

### 1. Backend Services

#### 1.1 Model Loader Service
**Purpose**: Singleton service for loading and caching ML models

**Key Features:**
- Lazy loading on first access
- Singleton pattern for memory efficiency
- Automatic model validation
- Preprocessor management

**Code Location**: `backend/app/services/model_loader.py`

**Methods:**
```python
load_model(model_path: str) -> Any
load_preprocessor(preprocessor_path: str) -> Dict
get_model() -> Any
get_label_encoder() -> LabelEncoder
get_scaler() -> StandardScaler
get_feature_columns() -> List[str]
```

#### 1.2 Prediction Service
**Purpose**: Handles prediction logic and feature preprocessing

**Key Features:**
- Feature alignment and validation
- Missing feature handling
- Batch prediction support
- Confidence scoring
- Threat level assessment

**Code Location**: `backend/app/services/prediction_service.py`

**Methods:**
```python
prepare_features(features: Dict) -> np.ndarray
predict(features: Dict) -> Tuple[str, float, Dict]
batch_predict(features_list: List[Dict]) -> List[Tuple]
get_prediction_details(features: Dict) -> Dict
```

#### 1.3 Explanation Service
**Purpose**: Generates SHAP-based explanations

**Key Features:**
- TreeExplainer for tree-based models
- Local feature importance
- Visualization data preparation
- Top-N feature selection

**Code Location**: `backend/app/services/explanation_service.py`

**Methods:**
```python
explain_prediction(features: Dict, top_n: int) -> Dict
explain_with_visualization_data(features: Dict, top_n: int) -> Dict
get_feature_contribution_summary(features: Dict) -> str
```

### 2. API Endpoints

#### 2.1 Prediction Endpoints

**POST /predict**
- **Purpose**: Single flow prediction
- **Input**: Flow features as JSON
- **Output**: Prediction, confidence, probabilities
- **Timeout**: 10s

**POST /predict/details**
- **Purpose**: Detailed prediction with threat assessment
- **Input**: Flow features as JSON
- **Output**: Extended prediction info including threat level
- **Timeout**: 10s

#### 2.2 Explanation Endpoints

**POST /explain**
- **Purpose**: Generate SHAP explanation
- **Input**: Flow features + top_n parameter
- **Output**: Feature importance rankings
- **Timeout**: 30s

**POST /explain/visualization**
- **Purpose**: Get visualization-ready explanation data
- **Input**: Flow features + top_n parameter
- **Output**: Formatted data for charts
- **Timeout**: 30s

**POST /explain/summary**
- **Purpose**: Human-readable explanation
- **Input**: Flow features
- **Output**: Text summary
- **Timeout**: 30s

#### 2.3 Health Endpoints

**GET /health**
- **Purpose**: Health check and status
- **Output**: Service status, model info
- **Timeout**: 5s

**GET /**
- **Purpose**: API information
- **Output**: Basic API metadata

### 3. Frontend Components

#### 3.1 Sidebar Component
**Purpose**: Navigation and configuration

**Features:**
- Page navigation
- Input method selection
- Model status display
- Dataset information
- Attack type reference

**Code Location**: `frontend/components/sidebar.py`

#### 3.2 Prediction View
**Purpose**: Main prediction interface

**Features:**
- Manual feature input form
- CSV file upload
- Real-time prediction
- Confidence gauge
- Probability distribution chart

**Code Location**: `frontend/components/prediction_view.py`

#### 3.3 Explanation View
**Purpose**: SHAP explanation visualization

**Features:**
- SHAP waterfall chart
- Feature impact table
- Impact distribution pie chart
- Downloadable results

**Code Location**: `frontend/components/explanation_view.py`

---

## API Reference

### Request/Response Schemas

#### FlowFeatures Schema
```json
{
  "features": {
    "Destination Port": 80,
    "Flow Duration": 120000,
    "Total Fwd Packets": 10,
    "Total Backward Packets": 8,
    "Flow Bytes/s": 1500.5,
    "Flow Packets/s": 150.0,
    ...
  }
}
```

#### PredictionResponse Schema
```json
{
  "prediction": "DDoS",
  "confidence": 0.97,
  "probabilities": {
    "BENIGN": 0.01,
    "DoS": 0.01,
    "DDoS": 0.97,
    "PortScan": 0.01,
    ...
  }
}
```

#### ExplanationResponse Schema
```json
{
  "prediction": "DDoS",
  "top_features": [
    {
      "feature": "Flow Duration",
      "impact": 0.45
    },
    ...
  ],
  "base_value": 0.14
}
```

### Error Responses

**400 Bad Request**
```json
{
  "error": "Validation error",
  "detail": "Missing required features: ..."
}
```

**500 Internal Server Error**
```json
{
  "error": "Prediction failed",
  "detail": "Model not loaded"
}
```

---

## Model Training Pipeline

### 1. Data Preprocessing

**Steps:**
1. Load CSV data
2. Remove duplicates
3. Handle missing values (NaN, Inf)
4. Encode categorical features
5. Separate features and target
6. Train/test split (80/20)
7. Feature scaling (StandardScaler)

**Code Location**: `backend/model/preprocessing.py`

### 2. Model Training

**XGBoost Parameters:**
```python
{
    'objective': 'multi:softmax',
    'num_class': 7,
    'max_depth': 10,
    'learning_rate': 0.1,
    'n_estimators': 200,
    'subsample': 0.8,
    'colsample_bytree': 0.8
}
```

**Random Forest Parameters:**
```python
{
    'n_estimators': 100,
    'max_depth': 20,
    'min_samples_split': 5,
    'min_samples_leaf': 2
}
```

### 3. Model Evaluation

**Metrics:**
- Accuracy
- Precision (weighted)
- Recall (weighted)
- F1-Score (weighted)
- Confusion Matrix
- Per-class metrics

### 4. Model Selection

Selection criteria:
1. F1-Score (primary)
2. Accuracy (secondary)
3. Confusion matrix analysis

Best model is saved as `saved_model.pkl`

---

## Deployment Guide

### Local Deployment

#### Prerequisites
- Python 3.10+
- pip
- 8GB RAM minimum
- 2GB free disk space

#### Steps
1. Install dependencies:
```bash
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

2. Train model:
```bash
cd backend/model
python train.py
```

3. Start backend:
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

4. Start frontend:
```bash
cd frontend
streamlit run app.py
```

### Docker Deployment

#### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- 8GB RAM minimum

#### Steps
1. Build containers:
```bash
docker-compose build
```

2. Start services:
```bash
docker-compose up
```

3. Access:
- Frontend: http://localhost:8501
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Production Deployment

#### Additional Requirements
- Reverse proxy (Nginx)
- SSL certificates
- Load balancer (if scaling)
- Monitoring (Prometheus, Grafana)
- Logging (ELK stack)

#### Security Considerations
1. Enable HTTPS
2. Configure CORS properly
3. Add rate limiting
4. Implement authentication
5. Use environment variables for secrets
6. Regular security updates

---

## Performance Optimization

### Backend Optimization

1. **Model Loading**
   - Use singleton pattern
   - Lazy loading
   - Model caching

2. **Prediction**
   - Batch predictions when possible
   - Async processing for multiple requests
   - Feature preprocessing caching

3. **API**
   - Enable compression
   - Use HTTP/2
   - Implement caching headers

### Frontend Optimization

1. **Streamlit**
   - Use `@st.cache_data` for expensive operations
   - Minimize recomputation
   - Lazy loading of components

2. **Visualization**
   - Limit chart complexity
   - Use appropriate chart types
   - Optimize Plotly rendering

### Database Optimization (if added)

1. Index frequently queried fields
2. Use connection pooling
3. Implement query caching
4. Regular vacuuming/optimization

---

## Troubleshooting

### Common Issues

#### 1. Model Not Loading
**Symptom**: "Model file not found" error

**Solutions:**
- Verify model file exists at correct path
- Check file permissions
- Ensure training completed successfully
- Verify path in environment variables

#### 2. High Memory Usage
**Symptom**: Out of memory errors

**Solutions:**
- Reduce batch size
- Use model pruning
- Implement pagination for results
- Increase container memory limits

#### 3. Slow Predictions
**Symptom**: High latency (>1s)

**Solutions:**
- Check model complexity
- Profile code for bottlenecks
- Use GPU acceleration if available
- Optimize feature preprocessing

#### 4. SHAP Timeout
**Symptom**: Explanation generation times out

**Solutions:**
- Reduce top_n parameter
- Use approximate SHAP values
- Increase timeout limits
- Consider caching explanations

### Debug Mode

Enable debug logging:

**Backend:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Frontend:**
```python
import streamlit as st
st.set_option('client.showErrorDetails', True)
```

### Monitoring

**Key Metrics:**
- Request latency (p50, p95, p99)
- Error rate
- CPU/Memory usage
- Model accuracy drift
- API response codes

**Tools:**
- Prometheus for metrics
- Grafana for visualization
- ELK for log aggregation
- Sentry for error tracking

---

## Best Practices

### Code Quality
1. Follow PEP 8 style guide
2. Use type hints
3. Write docstrings
4. Add unit tests
5. Use linting tools (pylint, flake8)

### Security
1. Validate all inputs
2. Sanitize user data
3. Use HTTPS in production
4. Implement rate limiting
5. Regular dependency updates

### Performance
1. Profile before optimizing
2. Cache expensive operations
3. Use async where appropriate
4. Minimize data transfers
5. Optimize database queries

### Maintenance
1. Regular backups
2. Monitor system health
3. Update dependencies
4. Review logs regularly
5. Plan for scaling

---

## Future Enhancements

### Planned Features
1. **Real-time Monitoring**
   - Live traffic analysis
   - Alert system
   - Dashboard widgets

2. **Advanced ML**
   - Ensemble models
   - Online learning
   - Anomaly detection

3. **User Management**
   - Authentication
   - Role-based access
   - Usage analytics

4. **Integration**
   - SIEM integration
   - API webhooks
   - Export capabilities

5. **Performance**
   - GPU acceleration
   - Model quantization
   - Edge deployment

---

## Support & Resources

### Documentation
- FastAPI Docs: https://fastapi.tiangolo.com/
- Streamlit Docs: https://docs.streamlit.io/
- XGBoost Docs: https://xgboost.readthedocs.io/
- SHAP Docs: https://shap.readthedocs.io/

### Community
- GitHub Issues
- Stack Overflow
- Research Papers

### Contact
For bugs, feature requests, or questions:
- Open a GitHub issue
- Contact development team
- Refer to API documentation

---

**Last Updated**: 2024
**Version**: 1.0.0
**Status**: Production Ready
