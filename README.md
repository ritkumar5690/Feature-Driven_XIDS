# 🛡️ XIDS - Explainable Intrusion Detection System

A production-ready, explainable machine learning system for network intrusion detection using the CIC-IDS2017 dataset. Features XGBoost classification with SHAP-based interpretability, FastAPI backend, and modern Streamlit frontend.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)
![License](https://img.shields.io/badge/License-Academic-yellow.svg)

## 🌟 Features

- **🎯 Multi-Class Detection**: Detects 7 types of network attacks (DoS, DDoS, PortScan, Bot, Brute Force, Web Attack)
- **🔍 Explainable AI**: SHAP-based explanations for every prediction
- **⚡ Real-time Inference**: Fast predictions with < 50ms latency
- **📊 Modern UI**: Interactive Streamlit dashboard with visualizations
- **🔌 RESTful API**: Well-documented FastAPI backend
- **🐳 Docker Support**: Easy deployment with Docker Compose
- **📈 High Accuracy**: ~95% accuracy on CIC-IDS2017 dataset

## 🏗️ Architecture

```
xids_project/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── main.py         # FastAPI application
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   └── schemas/        # Pydantic models
│   └── model/
│       ├── train.py        # Model training script
│       ├── preprocessing.py # Data preprocessing
│       └── saved_model.pkl  # Trained model (generated)
│
├── frontend/               # Streamlit Frontend
│   ├── app.py             # Main application
│   └── components/        # UI components
│
└── docker-compose.yml     # Docker orchestration
```

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager
- (Optional) Docker and Docker Compose
- CIC-IDS2017 Dataset

### Option 1: Local Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd xids_project
```

2. **Install Backend Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

3. **Install Frontend Dependencies**
```bash
cd ../frontend
pip install -r requirements.txt
```

4. **Configure Environment**
```bash
cd ..
cp .env.example .env
# Edit .env with your configuration
```

### Option 2: Docker Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd xids_project
```

2. **Build and run with Docker Compose**
```bash
docker-compose up --build
```

## 📊 Dataset Setup

### Download CIC-IDS2017

1. Visit: [CIC-IDS2017 Dataset](https://www.unb.ca/cic/datasets/ids-2017.html)
2. Download the CSV files (flow-based format)
3. Combine all CSV files or use individual files

### Dataset Structure

The dataset should contain network flow features including:
- Flow Duration
- Total Fwd/Bwd Packets
- Packet Lengths (Max, Min, Mean, Std)
- Flow Bytes/s, Packets/s
- Inter-Arrival Time (IAT) statistics
- Label column (target variable)

Expected classes:
- BENIGN
- DoS
- DDoS
- PortScan
- Bot
- Brute Force
- Web Attack

## 🚀 Usage

### 1. Train the Model

Update the dataset path in `backend/model/train.py`:

```python
DATA_PATH = "/path/to/CIC-IDS2017.csv"
```

Run training:

```bash
cd backend/model
python train.py
```

This will:
- Load and preprocess the dataset
- Train XGBoost and Random Forest models
- Evaluate and select the best model
- Save `saved_model.pkl` and `preprocessor.pkl`

### 2. Start the Backend API

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### 3. Start the Frontend

```bash
cd frontend
streamlit run app.py
```

The frontend will be available at: http://localhost:8501

### 4. Using Docker

```bash
docker-compose up
```

Access:
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🔌 API Endpoints

### Prediction

**POST** `/predict`

Request:
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

Response:
```json
{
  "prediction": "DDoS",
  "confidence": 0.97,
  "probabilities": {
    "BENIGN": 0.01,
    "DoS": 0.01,
    "DDoS": 0.97,
    "PortScan": 0.01
  }
}
```

### Explanation

**POST** `/explain?top_n=10`

Request: Same as prediction

Response:
```json
{
  "prediction": "DDoS",
  "top_features": [
    {
      "feature": "Flow Duration",
      "impact": 0.45
    },
    {
      "feature": "Total Fwd Packets",
      "impact": 0.32
    }
  ],
  "base_value": 0.14
}
```

### Health Check

**GET** `/health`

Response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_type": "XGBClassifier",
  "feature_count": 78
}
```

## 📸 Screenshots & Usage Guide

### Single Prediction
1. Select "Manual Entry" or "Upload CSV" in sidebar
2. Enter network flow features
3. Click "Analyze Traffic"
4. View prediction results with confidence gauge
5. Switch to "Explanation" tab for SHAP analysis

### Batch Analysis
1. Navigate to "Batch Analysis" page
2. Upload CSV with multiple flows
3. Click "Analyze All Flows"
4. Download results as CSV

### Explanation View
1. After making a prediction
2. Go to "Explanation" tab
3. Click "Generate Explanation"
4. View SHAP waterfall chart, feature table, and impact summary

## 🛠️ Technical Details

### Model

- **Algorithm**: XGBoost Classifier
- **Baseline**: Random Forest Classifier
- **Features**: 78+ network flow features
- **Classes**: 7 (1 benign + 6 attack types)
- **Preprocessing**: StandardScaler, LabelEncoder
- **Train/Test Split**: 80/20

### Metrics

- Accuracy
- Precision (weighted)
- Recall (weighted)
- F1-Score (weighted)
- Confusion Matrix

### Explainability

- **Method**: SHAP (SHapley Additive exPlanations)
- **Explainer**: TreeExplainer (optimized for tree-based models)
- **Outputs**: 
  - Feature importance rankings
  - SHAP values per feature
  - Waterfall visualizations
  - Force plots

### Tech Stack

**Backend:**
- FastAPI (API framework)
- XGBoost (ML model)
- Scikit-learn (preprocessing)
- SHAP (explainability)
- Pydantic (validation)
- Uvicorn (ASGI server)

**Frontend:**
- Streamlit (UI framework)
- Plotly (visualizations)
- Pandas (data handling)
- Requests (API calls)

## 🧪 Testing

### Test Backend API

```bash
# Health check
curl http://localhost:8000/health

# Prediction (example)
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "Destination Port": 80,
      "Flow Duration": 120000,
      "Total Fwd Packets": 10,
      "Total Backward Packets": 8,
      "Flow Bytes/s": 1500.5,
      "Flow Packets/s": 150.0
    }
  }'
```

### Run Frontend Locally

```bash
cd frontend
streamlit run app.py
```

## 📝 Configuration

### Environment Variables

Edit `.env` file:

```env
API_URL=http://localhost:8000
MODEL_PATH=backend/model/saved_model.pkl
PREPROCESSOR_PATH=backend/model/preprocessor.pkl
LOG_LEVEL=INFO
DATASET_PATH=/path/to/CIC-IDS2017.csv
```

### Model Parameters

Edit `backend/model/train.py` to customize:

```python
params = {
    'max_depth': 10,
    'learning_rate': 0.1,
    'n_estimators': 200,
    'subsample': 0.8,
    'colsample_bytree': 0.8
}
```

## 🐛 Troubleshooting

### Model Not Loading

**Problem**: "Model file not found" error

**Solution**: 
1. Ensure you've trained the model first
2. Check `MODEL_PATH` in `.env`
3. Verify `saved_model.pkl` exists in `backend/model/`

### API Connection Failed

**Problem**: Frontend can't connect to backend

**Solution**:
1. Ensure backend is running on port 8000
2. Check `API_URL` in frontend `.env`
3. If using Docker, services should be on same network

### SHAP Explanation Slow

**Problem**: Explanation takes too long

**Solution**:
1. Reduce `top_n` parameter
2. Use smaller dataset for training
3. Consider using SHAP's approximate methods

### Memory Issues

**Problem**: Out of memory during training

**Solution**:
1. Reduce dataset size
2. Use sampling
3. Adjust XGBoost parameters (reduce tree depth)

## 📚 References

### Dataset
- [CIC-IDS2017](https://www.unb.ca/cic/datasets/ids-2017.html)
- Sharafaldin, I., Lashkari, A.H., & Ghorbani, A.A. (2018). Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization.

### Technologies
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)
- [SHAP Documentation](https://shap.readthedocs.io/)

## 🤝 Contributing

This project is designed for academic and research purposes. Contributions are welcome:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is intended for academic and research use. Please cite the CIC-IDS2017 dataset if used in publications.

## 👨‍💻 Authors

XIDS - Explainable Intrusion Detection System  
Version 1.0.0

## 🎓 Academic Use

This system is suitable for:
- Cybersecurity research
- Machine learning coursework
- Intrusion detection studies
- Explainable AI demonstrations
- Network security analysis

## ⚠️ Disclaimer

This system is intended for research and educational purposes. For production deployment in critical infrastructure, additional security hardening, testing, and validation are required.

## 📞 Support

For issues, questions, or contributions:
- Create an issue on GitHub
- Check documentation at `/docs` endpoint
- Review API documentation at `/redoc`

---

**Built with ❤️ for Cybersecurity Research**

*Powered by XGBoost, SHAP, FastAPI, and Streamlit*
#   F e a t u r e - D r i v e n _ X I D S  
 