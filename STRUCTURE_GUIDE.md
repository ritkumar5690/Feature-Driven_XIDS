# XIDS - Explainable Intrusion Detection System
## Updated Project Structure

This document describes the reorganized XIDS project structure for improved maintainability, scalability, and code organization.

## 📁 Project Structure Overview

```
XIDS/
├── backend/                          # ML Backend
│   ├── data/
│   │   ├── raw/                      # Raw datasets
│   │   │   ├── KDDTrain+.txt
│   │   │   └── KDDTest+.txt
│   │   └── processed/                # Processed data
│   │       ├── train_processed.csv
│   │       └── test_processed.csv
│   │
│   ├── preprocessing/                # Data Processing Pipeline
│   │   ├── load_data.py              # Data loading
│   │   ├── clean_data.py             # Data cleaning
│   │   ├── encode_normalize.py       # Encoding & normalization
│   │   └── preprocess_pipeline.py    # Orchestration
│   │
│   ├── features/                     # Feature Engineering
│   │   ├── feature_selection.py      # Feature selection methods
│   │   └── feature_analysis.py       # Feature analysis
│   │
│   ├── models/                       # Model Training & Evaluation
│   │   ├── train_model.py            # Training pipeline
│   │   ├── evaluate_model.py         # Evaluation metrics
│   │   └── saved_models/
│   │       ├── model.pkl
│   │       └── preprocessor.pkl
│   │
│   ├── explainability/               # Model Explainability
│   │   ├── shap_explainer.py         # SHAP explanations
│   │   ├── lime_explainer.py         # LIME explanations
│   │   └── rule_extraction.py        # Rule extraction
│   │
│   ├── utils/                        # Utilities
│   │   └── config.py                 # Configuration
│   │
│   ├── app/                          # FastAPI Application
│   │   ├── main.py
│   │   ├── routes/                   # API endpoints
│   │   ├── services/                 # Business logic
│   │   └── schemas/                  # Request/response schemas
│   │
│   ├── requirements.txt
│   ├── Dockerfile
│   └── main.py                       # Backend entry point
│
├── frontend/                          # Streamlit Frontend
│   ├── app.py                        # Main application
│   ├── components/
│   │   ├── sidebar.py               # Navigation
│   │   ├── prediction_view.py       # Predictions
│   │   ├── explanation_view.py      # Explanations
│   │   └── login.py                 # Authentication
│   │
│   ├── static/
│   │   └── styles.css               # Styling
│   │
│   ├── assets/
│   │   └── logo.png                 # Branding
│   │
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .users.json                  # User database
│
├── results/                           # Output Results
│   ├── metrics/                      # Model metrics
│   ├── plots/                        # Visualizations
│   └── explanations/                 # Explanations
│
├── notebooks/                         # Analysis Notebooks
│   ├── data_exploration.ipynb       # Data analysis
│   └── feature_importance.ipynb     # Feature analysis
│
├── docker-compose.yml                # Docker orchestration
├── requirements.txt                  # Root dependencies
├── PROJECT_STRUCTURE.md              # Structure documentation
├── README.md                         # Project guide
└── .gitignore
```

## 🚀 Key Components

### Backend Modules

#### 1. **Preprocessing** (`backend/preprocessing/`)
Handles data loading, cleaning, and transformation.

```python
from preprocessing.preprocess_pipeline import preprocess_pipeline

# Complete pipeline execution
X_train, X_test, y_train, y_test = preprocess_pipeline(
    filepath='data/raw/KDDTrain+.txt',
    target_column='Label',
    test_size=0.2,
    normalization_method='standard'
)
```

**Key Functions:**
- `load_data()`: Load CSV/TXT files
- `clean_data()`: Remove duplicates, handle missing values
- `encode_categorical_features()`: Encode categorical columns
- `normalize_numeric_features()`: Scale features
- `preprocess_pipeline()`: Complete workflow

#### 2. **Features** (`backend/features/`)
Feature selection and analysis.

```python
from features.feature_selection import select_kbest_features, get_feature_importance_scores
from features.feature_analysis import analyze_feature_distribution, detect_outliers

# Feature selection
selected_indices = select_kbest_features(X, y, k=20)

# Feature analysis
importance_scores = get_feature_importance_scores(X, y)
distribution = analyze_feature_distribution(X)
outliers = detect_outliers(X, threshold=3.0)
```

**Key Functions:**
- `select_kbest_features()`: K-best feature selection
- `select_mutual_information_features()`: MI-based selection
- `select_forest_features()`: RF importance selection
- `compute_feature_statistics()`: Statistical analysis
- `analyze_class_distribution()`: Class imbalance analysis

#### 3. **Models** (`backend/models/`)
Model training, evaluation, and persistence.

```python
from models.train_model import XIDSTrainer

# Training
trainer = XIDSTrainer()
metrics = trainer.train_pipeline('data/processed/train_processed.csv')

# Evaluation
from models.evaluate_model import evaluate_model
results = evaluate_model(y_test, y_pred)
```

**Key Classes/Functions:**
- `XIDSTrainer`: Main training orchestrator
- `train_xgboost()`: XGBoost training
- `train_random_forest()`: Random Forest training
- `evaluate_model()`: Compute metrics
- `compare_models()`: Model comparison

#### 4. **Explainability** (`backend/explainability/`)
Model interpretation and explanation.

```python
from explainability.shap_explainer import SHAPExplainer
from explainability.lime_explainer import LIMEExplainer

# SHAP explanations
shap_exp = SHAPExplainer(model, X_train)
explanation = shap_exp.explain_instance(X_instance)

# LIME explanations
lime_exp = LIMEExplainer(model)
local_exp = lime_exp.explain_prediction(X_instance, num_features=10)
```

**Key Classes/Functions:**
- `SHAPExplainer`: SHAP-based explanations
- `LIMEExplainer`: LIME local explanations
- `RuleExtractor`: Decision rule extraction

#### 5. **Configuration** (`backend/utils/`)
Centralized configuration management.

```python
from utils.config import (
    MODEL_CONFIG, FEATURE_CONFIG, DATA_CONFIG,
    MODELS_ROOT, DATA_ROOT, RESULTS_ROOT
)

# Access configuration
model_params = MODEL_CONFIG['xgboost']
data_dir = DATA_ROOT / 'raw'
```

### Frontend Features

#### Authentication
- Email/password registration
- Login/logout functionality
- Session state management
- User database (JSON)

#### Dark Cybersecurity Theme
- Primary dark: #0D1117
- Accent green: #00FF41
- Accent cyan: #00CED1
- Glow effects and gradients

#### Components
- **Sidebar**: Navigation and user info
- **Prediction View**: Input form and results
- **Explanation View**: SHAP/LIME visualizations
- **Login Page**: User authentication

## 📊 Data Pipeline

### Processing Workflow

```
Raw Data (KDDTrain+.txt, KDDTest+.txt)
    ↓ load_data.py
Load & Validate
    ↓ clean_data.py
Remove Duplicates & Missing Values
    ↓ encode_normalize.py
Encode Categorical & Normalize Numeric
    ↓ split_data
Train/Test Split (80/20)
    ↓ preprocess_pipeline.py
Processed Data (train_processed.csv, test_processed.csv)
```

## 🤖 Model Training Pipeline

```
Processed Data
    ↓ feature_selection.py
Feature Engineering
    ↓ train_model.py
├─ XGBoost Training
├─ Random Forest Training
└─ Model Selection
    ↓ evaluate_model.py
Evaluation Metrics
    ↓ saved_models/
model.pkl & preprocessor.pkl
```

## 🔍 Explainability Pipeline

```
Model Prediction
    ↓
├─ shap_explainer.py
│  └─ SHAP Values & Feature Importance
├─ lime_explainer.py
│  └─ Local Linear Approximation
└─ rule_extraction.py
   └─ Decision Rules
    ↓
Explanation Output
```

## 🛠️ Installation & Setup

### 1. Environment Setup
```bash
cd XIDS
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Data Preparation
Place datasets in `backend/data/raw/`:
- `KDDTrain+.txt`
- `KDDTest+.txt`

### 3. Model Training
```bash
cd backend/models
python train_model.py
```

### 4. Start Backend
```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 5. Start Frontend
```bash
cd frontend
streamlit run app.py
```

### 6. Access Application
- **Frontend**: http://localhost:8501
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📝 Usage Examples

### Data Preprocessing
```python
from preprocessing.preprocess_pipeline import preprocess_pipeline

X_train, X_test, y_train, y_test = preprocess_pipeline(
    filepath='backend/data/raw/KDDTrain+.txt',
    target_column='Label',
    test_size=0.2,
    normalization_method='standard'
)
```

### Feature Selection
```python
from features.feature_selection import select_kbest_features

# Select top 20 features
selected_indices = select_kbest_features(X_train, y_train, k=20)
X_train_selected = X_train[:, selected_indices]
X_test_selected = X_test[:, selected_indices]
```

### Model Training
```python
from models.train_model import XIDSTrainer

trainer = XIDSTrainer()
metrics = trainer.train_pipeline('backend/data/processed/train_processed.csv')
print(f"F1-Score: {metrics['f1_score']:.4f}")
```

### Model Explanation
```python
from explainability.shap_explainer import SHAPExplainer

explainer = SHAPExplainer(model, X_train, model_type='tree')
explanation = explainer.explain_instance(X_test[0])
print(f"Base Value: {explanation['base_value']}")
print(f"SHAP Values: {explanation['shap_values']}")
```

## 📚 Jupyter Notebooks

### data_exploration.ipynb
- Dataset overview
- Statistical analysis
- Class distribution
- Feature characteristics
- Data quality assessment

### feature_importance.ipynb
- Feature importance ranking
- Feature selection methods
- Correlation analysis
- Cumulative importance
- Selection recommendations

## 🔧 Configuration

Edit `backend/utils/config.py` to customize:

```python
# Model hyperparameters
MODEL_CONFIG = {
    'xgboost': {
        'n_estimators': 100,
        'max_depth': 8,
        'learning_rate': 0.1,
    },
    'random_forest': {
        'n_estimators': 100,
        'max_depth': 15,
    }
}

# Feature selection
FEATURE_CONFIG = {
    'selection_method': 'forest',  # 'kbest', 'mutual_info', 'forest'
    'num_features': 20,
    'outlier_threshold': 3.0
}
```

## 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Backend will be at http://localhost:8000
# Frontend will be at http://localhost:8501
```

## 📊 Results Management

All outputs are saved in the `results/` directory:

```
results/
├── metrics/
│   ├── model_performance.json
│   ├── confusion_matrix.csv
│   └── classification_report.txt
├── plots/
│   ├── feature_importance.png
│   ├── confusion_matrix.png
│   └── roc_curve.png
└── explanations/
    ├── shap_explanations.json
    ├── lime_explanations.json
    └── rule_extractions.json
```

## 🔐 Security & Authentication

- **Login System**: Email/password authentication
- **User Database**: Hashed credentials in `.users.json`
- **Session Management**: Streamlit session state
- **Password Hashing**: SHA-256 encryption

## 📈 Performance Monitoring

- Model metrics saved in `results/metrics/`
- Predictions logged for analysis
- Explanation generation timestamped
- Performance trends tracked

## 🚀 Development Workflow

1. **Exploration**: Use Jupyter notebooks
2. **Development**: Edit modules in backend/
3. **Testing**: Run train_model.py
4. **Validation**: Test via API and frontend
5. **Deployment**: Use Docker Compose

## 📖 Documentation

- **PROJECT_STRUCTURE.md**: Detailed structure guide
- **README.md**: Project overview
- **DOCUMENTATION.md**: Complete documentation
- **Inline Comments**: Code-level documentation

## 🤝 Contributing

When contributing:
1. Follow the modular structure
2. Add tests for new modules
3. Update configuration in `config.py`
4. Document functions and classes
5. Update notebooks for major changes

## 📝 License

This project is part of the XIDS (Explainable Intrusion Detection System) initiative.

## 🆘 Troubleshooting

### Model File Not Found
```bash
cd backend/models
python train_model.py
```

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
python -m uvicorn app.main:app --port 8001
```

### Missing Dependencies
```bash
pip install -r requirements.txt
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

## 📞 Support

For issues or questions:
1. Check the notebooks for examples
2. Review configuration in `config.py`
3. Check API documentation at `/docs`
4. Review logs in `results/` folder

---

**Last Updated**: February 15, 2026  
**Version**: 2.0 (Reorganized Structure)
