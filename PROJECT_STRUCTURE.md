# XIDS Project Structure Documentation

## Project Overview

The **XIDS (Explainable Intrusion Detection System)** is a comprehensive machine learning system for detecting and explaining network intrusions. The project follows a modular architecture with clear separation of concerns between data processing, model training, explainability, and user interface.

## Complete Directory Structure

```
XIDS/
│
├── backend/
│   ├── data/
│   │   ├── raw/
│   │   │   ├── KDDTrain+.txt
│   │   │   └── KDDTest+.txt
│   │   └── processed/
│   │       ├── train_processed.csv
│   │       └── test_processed.csv
│   │
│   ├── preprocessing/
│   │   ├── __init__.py
│   │   ├── load_data.py
│   │   ├── clean_data.py
│   │   ├── encode_normalize.py
│   │   └── preprocess_pipeline.py
│   │
│   ├── features/
│   │   ├── __init__.py
│   │   ├── feature_selection.py
│   │   └── feature_analysis.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── train_model.py
│   │   ├── evaluate_model.py
│   │   └── saved_models/
│   │       ├── model.pkl
│   │       └── preprocessor.pkl
│   │
│   ├── explainability/
│   │   ├── __init__.py
│   │   ├── shap_explainer.py
│   │   ├── lime_explainer.py
│   │   └── rule_extraction.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   └── config.py
│   │
│   ├── app/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── schemas/
│   │   └── main.py
│   │
│   ├── Dockerfile
│   ├── requirements.txt
│   └── main.py (API entry point)
│
├── frontend/
│   ├── app.py (Streamlit entry point)
│   ├── components/
│   │   ├── sidebar.py
│   │   ├── prediction_view.py
│   │   ├── explanation_view.py
│   │   └── login.py
│   │
│   ├── static/
│   │   └── styles.css
│   │
│   ├── assets/
│   │   └── logo.png
│   │
│   ├── Dockerfile
│   └── requirements.txt
│
├── results/
│   ├── metrics/
│   ├── plots/
│   └── explanations/
│
├── notebooks/
│   ├── data_exploration.ipynb
│   └── feature_importance.ipynb
│
├── docker-compose.yml
├── requirements.txt
├── README.md
├── DOCUMENTATION.md
├── .gitignore
└── PROJECT_SUMMARY.md
```

## Backend Architecture

### 1. Data Management (`backend/data/`)

**Purpose**: Store raw and processed datasets

- **raw/**: Contains original KDD IDS datasets
  - `KDDTrain+.txt`: Training dataset (4.9M records)
  - `KDDTest+.txt`: Test dataset (311K records)
  
- **processed/**: Contains preprocessed and cleaned data
  - `train_processed.csv`: Cleaned and normalized training data
  - `test_processed.csv`: Cleaned and normalized test data

### 2. Preprocessing Module (`backend/preprocessing/`)

**Purpose**: Data loading, cleaning, encoding, and normalization

#### Files:

- **load_data.py**
  - `load_data()`: Load CSV/TXT files
  - `load_kdd_train_data()`: Load KDD training dataset
  - `load_kdd_test_data()`: Load KDD test dataset

- **clean_data.py**
  - `clean_data()`: Remove duplicates, handle missing/infinite values
  - `remove_duplicates()`: Deduplicate rows
  - `handle_missing_values()`: Strategy-based imputation or removal
  - `handle_infinite_values()`: Handle inf/-inf values

- **encode_normalize.py**
  - `FeatureEncoder`: Categorical encoding using LabelEncoder
  - `FeatureNormalizer`: Feature scaling (Standard/MinMax)
  - `encode_categorical_features()`: Encode all categorical columns
  - `normalize_numeric_features()`: Normalize numeric features

- **preprocess_pipeline.py**
  - `preprocess_pipeline()`: Complete preprocessing workflow
  - Orchestrates: Load → Clean → Encode → Split → Normalize

### 3. Feature Engineering (`backend/features/`)

**Purpose**: Feature selection and analysis

#### Files:

- **feature_selection.py**
  - `select_kbest_features()`: K-best selection using ANOVA F-score
  - `select_mutual_information_features()`: MI-based selection
  - `select_forest_features()`: Random Forest importance-based selection
  - `get_feature_importance_scores()`: Compute importance scores

- **feature_analysis.py**
  - `compute_feature_statistics()`: Descriptive statistics
  - `analyze_feature_distribution()`: Distribution analysis
  - `detect_outliers()`: Z-score based outlier detection
  - `analyze_class_distribution()`: Class balance analysis

### 4. Model Management (`backend/models/`)

**Purpose**: Train, evaluate, and persist models

#### Files:

- **train_model.py**
  - `XIDSTrainer`: Main trainer class
  - `train_xgboost()`: XGBoost model training
  - `train_random_forest()`: Random Forest training
  - `evaluate_model()`: Model evaluation
  - `select_best_model()`: Compare and select best model
  - `save_model()`: Persist model artifacts
  - `train_pipeline()`: Complete training workflow

- **evaluate_model.py**
  - `evaluate_model()`: Compute accuracy, precision, recall, F1
  - `get_confusion_matrix()`: Confusion matrix generation
  - `get_classification_report()`: Detailed classification metrics
  - `evaluate_multiclass()`: Per-class evaluation
  - `compare_models()`: Compare multiple models

- **saved_models/**
  - `model.pkl`: Trained XGBoost/Random Forest model
  - `preprocessor.pkl`: Fitted encoders and scalers

### 5. Explainability Module (`backend/explainability/`)

**Purpose**: Explain model predictions using multiple techniques

#### Files:

- **shap_explainer.py**
  - `SHAPExplainer`: SHAP-based explanations
  - `explain_instance()`: Explain single prediction
  - `explain_batch()`: Batch explanations
  - `explain_prediction()`: Convenience function

- **lime_explainer.py**
  - `LIMEExplainer`: LIME-based local explanations
  - `explain_prediction()`: Local linear approximation
  - `explain_local()`: Wrapper function

- **rule_extraction.py**
  - `RuleExtractor`: Extract rules from tree models
  - `extract_decision_path()`: Decision tree path extraction
  - `extract_feature_rules()`: Feature importance-based rules
  - `extract_rules()`: Main extraction function

### 6. Utilities (`backend/utils/`)

**Purpose**: Configuration and utilities

#### Files:

- **config.py**
  - Path definitions (PROJECT_ROOT, DATA_ROOT, MODELS_ROOT, etc.)
  - DATA_CONFIG: Dataset configuration
  - MODEL_CONFIG: Model hyperparameters (XGBoost, Random Forest, Decision Tree)
  - FEATURE_CONFIG: Feature selection settings
  - EXPLAINABILITY_CONFIG: Explainability settings
  - API_CONFIG: API settings
  - `create_directories()`: Initialize directory structure

### 7. API Layer (`backend/app/`)

**Purpose**: FastAPI application for model serving

- **main.py**: API entry point
  - Health check endpoint
  - Prediction endpoints
  - Model loading and management

- **routes/**: API route handlers
  - predict.py: Prediction endpoints
  - explain.py: Explanation endpoints

- **services/**: Business logic
  - prediction_service.py: Prediction logic
  - explanation_service.py: Explanation logic
  - model_loader.py: Model loading and caching

- **schemas/**: Request/response schemas
  - request_schema.py: Prediction request format
  - response_schema.py: Prediction response format

## Frontend Architecture

### 1. Main Application (`frontend/app.py`)

- Streamlit entry point
- User authentication (login/registration)
- Session state management
- Cybersecurity dark theme

### 2. Components (`frontend/components/`)

- **sidebar.py**: Navigation and user info
- **prediction_view.py**: Input form and prediction display
- **explanation_view.py**: SHAP/LIME visualizations
- **login.py**: Authentication forms

### 3. Styling (`frontend/static/`)

- **styles.css**: Global CSS styles
- Dark cybersecurity theme with neon accents

### 4. Assets (`frontend/assets/`)

- **logo.png**: Project logo
- Branding assets

## Results Management (`results/`)

### Subdirectories:

- **metrics/**: Model performance metrics and reports
- **plots/**: Visualization outputs
- **explanations/**: SHAP/LIME explanation outputs

## Notebooks (`notebooks/`)

### Analysis Notebooks:

1. **data_exploration.ipynb**
   - Dataset overview
   - Statistical analysis
   - Class distribution
   - Feature characteristics
   - Data quality assessment

2. **feature_importance.ipynb**
   - Feature importance from tree models
   - Feature selection methods
   - Correlation analysis
   - Feature visualization
   - Selection recommendations

## Configuration Management

### Key Configuration Files:

1. **backend/utils/config.py**
   - Centralized configuration
   - Path management
   - Model hyperparameters
   - Feature selection settings
   - API settings

2. **docker-compose.yml**
   - Service orchestration
   - Backend (FastAPI) service
   - Frontend (Streamlit) service
   - Volume mappings

3. **requirements.txt** (Root & Backend & Frontend)
   - Project dependencies
   - Package versions

## Data Pipeline

### Complete Processing Workflow:

```
Raw Data (KDDTrain+.txt, KDDTest+.txt)
    ↓
[load_data.py] → Load CSV/TXT
    ↓
[clean_data.py] → Remove duplicates, handle missing values
    ↓
[encode_normalize.py] → Encode categorical, normalize numeric
    ↓
[preprocess_pipeline.py] → Orchestrate and split (80/20)
    ↓
Processed Data (train_processed.csv, test_processed.csv)
    ↓
[feature_selection.py] → Select K-best features
    ↓
[train_model.py] → Train XGBoost & Random Forest
    ↓
[evaluate_model.py] → Evaluate performance
    ↓
Saved Models (model.pkl, preprocessor.pkl)
```

## Model Serving Pipeline

```
API Request
    ↓
[FastAPI Endpoint] (app/routes/predict.py)
    ↓
[model_loader.py] → Load model & preprocessor
    ↓
[prediction_service.py] → Make prediction
    ↓
[explainability/] → Generate explanations
    ├─ shap_explainer.py
    ├─ lime_explainer.py
    └─ rule_extraction.py
    ↓
JSON Response (prediction + explanation)
```

## Technology Stack

### Backend:
- **Framework**: FastAPI 0.129.0
- **Server**: Uvicorn 0.40.0
- **ML**: XGBoost, scikit-learn, pandas, numpy
- **Explainability**: SHAP, LIME
- **Data**: joblib

### Frontend:
- **Framework**: Streamlit 1.54.0
- **Visualization**: Plotly, matplotlib, seaborn
- **Styling**: Custom CSS with cybersecurity theme

### Infrastructure:
- **Containerization**: Docker
- **Orchestration**: Docker Compose

## Authentication & Security

- **Frontend**: Email/password authentication
- **User Database**: JSON-based storage (.users.json)
- **Password Hashing**: SHA-256
- **Session Management**: Streamlit session state

## Styling & Theme

### Color Palette:
- **Primary Dark**: #0D1117 (Very Dark Blue)
- **Secondary Dark**: #1A1F2E (Dark Blue-Gray)
- **Accent Green**: #00FF41 (Neon Green)
- **Accent Cyan**: #00CED1 (Cyan)
- **Text Primary**: #E0E0E0 (Light Gray)

### Features:
- Dark cybersecurity theme
- Glow effects on headings
- Gradient backgrounds
- Neon text shadows

## Getting Started

### 1. Setup Environment
```bash
cd XIDS/
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Train Model
```bash
cd backend/models/
python train_model.py
```

### 3. Start Backend
```bash
cd backend/
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 4. Start Frontend
```bash
cd frontend/
streamlit run app.py
```

### 5. Access Application
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Key Features

1. **Data Preprocessing**: Complete pipeline for data cleaning and normalization
2. **Feature Engineering**: Multiple feature selection methods
3. **Model Training**: XGBoost and Random Forest implementations
4. **Model Evaluation**: Comprehensive metrics and comparison
5. **Explainability**: SHAP, LIME, and rule extraction
6. **REST API**: FastAPI for model serving
7. **Web Interface**: Streamlit frontend with authentication
8. **Interactive Notebooks**: Jupyter notebooks for analysis

## Development Workflow

1. **Data Exploration**: Use notebooks in `notebooks/` folder
2. **Feature Analysis**: Run feature importance notebook
3. **Model Training**: Execute `backend/models/train_model.py`
4. **API Testing**: Use FastAPI docs at `/docs`
5. **Frontend Integration**: Test predictions in Streamlit app
6. **Results**: Check outputs in `results/` folder

## Future Enhancements

- Real-time model monitoring
- Advanced hyperparameter optimization
- Ensemble methods integration
- Production deployment on cloud
- API rate limiting and authentication
- Database integration for results persistence
- Advanced visualization dashboard
- Model versioning and tracking
