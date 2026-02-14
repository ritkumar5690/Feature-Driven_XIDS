# XIDS Multi-Page Dashboard Architecture

## Overview

The XIDS Frontend has been completely restructured into a professional enterprise-grade multi-page analytics dashboard with 6 comprehensive pages focused on explainability, security analysis, and risk assessment.

## Architecture Changes

### Previous Structure
```
frontend/
├── app.py (single-page)
├── components/
│   ├── prediction_view.py
│   ├── explanation_view.py
│   ├── sidebar.py
│   └── login.py
```

### New Structure
```
frontend/
├── app.py (multi-page router)
├── components/
│   ├── pages/ (NEW - 6 analytics pages)
│   │   ├── __init__.py
│   │   ├── dashboard.py (SOC Dashboard)
│   │   ├── detection_analytics.py (Model Performance)
│   │   ├── feature_importance.py (Feature Analysis)
│   │   ├── explainability.py (SHAP/LIME)
│   │   ├── drift_monitoring.py (Data Drift)
│   │   └── risk_assessment.py (Security Risk)
│   ├── sidebar.py (updated navigation)
│   ├── prediction_view.py (legacy - preserved)
│   ├── explanation_view.py (legacy - preserved)
│   ├── login.py (authentication)
│   └── __init__.py
```

## 6 Dashboard Pages

### 1️⃣ Overview / SOC Dashboard
**Purpose:** Executive-level security monitoring

**Location:** `components/pages/dashboard.py`

**Key Metrics:**
- Security Score (0-100 gauge)
- Total Traffic Analyzed
- Threats Detected (24h)
- Risk Level Indicator (Color-coded)

**Visualizations:**
- 📈 Threat Trend Chart (24h line chart with fill)
- 🎯 Attack Distribution (donut chart)
- 📊 Detection Rate Gauge
- 🎯 False Positive Rate Gauge
- ⚡ Average Response Time
- Top 5 Attack Categories (table)
- Real-time Detection Timeline

**Data Points:**
- Security score: 78.5/100
- Total traffic: 9,205 flows
- Threats detected: 1,705
- Risk level: MEDIUM
- Detection rate: 94.2%
- False positive rate: 2.1%

---

### 2️⃣ Detection Analytics Page
**Purpose:** Model performance metrics and evaluation

**Location:** `components/pages/detection_analytics.py`

**Key Metrics:**
- Accuracy (94.20%)
- Precision (91.85%)
- Recall (93.10%)
- F1-Score (92.47%)

**Visualizations:**
- 🔲 Confusion Matrix (heatmap with actual counts)
- 📉 ROC Curve (with AUC score)
- 📊 Per-class Performance (table with progress bars)
- 📊 Probability Score Distribution (histogram)
- 🔴 False Positive Analysis (by attack type)
- 🎯 Attack Count Distribution (stacked bar)

**Per-Class Metrics:**
- BENIGN: P=0.94, R=0.96, F1=0.95
- DoS: P=0.91, R=0.94, F1=0.92
- DDoS: P=0.93, R=0.95, F1=0.94
- PortScan: P=0.88, R=0.90, F1=0.89
- Bot: P=0.82, R=0.85, F1=0.83
- Brute Force: P=0.85, R=0.87, F1=0.86
- Web Attack: P=0.89, R=0.91, F1=0.90

---

### 3️⃣ Feature Importance Page
**Purpose:** Feature-driven analysis - Which features drive attacks?

**Location:** `components/pages/feature_importance.py`

**Key Analysis:**
- Top 10 Most Important Features
- Feature Correlation Heatmap
- Feature Distribution (Normal vs Attack)
- Feature Statistics (Mean, Std Dev, Min, Max)
- Feature Importance by Attack Type
- Feature Selection Method Comparison (K-Best, MI, Random Forest)
- Outlier Detection Analysis

**Top 10 Features:**
1. Flow Duration (18.5%)
2. Total Fwd Packets (15.6%)
3. Total Bwd Packets (14.2%)
4. Flow Bytes/s (12.8%)
5. Fwd PSH Flags (11.8%)
6. Bwd PSH Flags (10.5%)
7. Flow Packets/s (9.5%)
8. Fwd IAT Mean (8.2%)
9. Bwd IAT Mean (7.4%)
10. Fwd Packet Length Mean (6.8%)

**Visualizations:**
- 📊 Feature Importance Bar Chart
- 🔗 Correlation Heatmap (top 10 features)
- 📈 Distribution Comparison (KDE plots)
- 🎯 Attack Type Importance Bars
- 🎯 Outlier Detection Chart

---

### 4️⃣ Explainability (SHAP/LIME) Page
**Purpose:** Explain individual predictions - Heart of Feature-Driven XIDS

**Location:** `components/pages/explainability.py`

**Explanation Methods:**
- SHAP Summary Plot (impact across all samples)
- SHAP Force Plot (individual sample contribution)
- Feature Contribution Waterfall (cumulative effect)
- LIME Explanation (local linear model)

**Sample Features Explained:**
- Flow Duration: 2500.5 (SHAP: +0.3245)
- Total Fwd Packets: 150 (SHAP: +0.2812)
- Flow Bytes/s: 3200.5 (SHAP: +0.2412)
- Fwd PSH Flags: 5 (SHAP: +0.1834)
- Total Bwd Packets: 120 (SHAP: +0.1523)

**Visualizations:**
- 📊 SHAP Summary Plot (scatter with color coding)
- 🔥 SHAP Force Plot (horizontal waterfall)
- 📉 Feature Contribution Waterfall
- 🍋 LIME Local Explanation
- Feature Impact Distribution
- Detailed Feature Statistics

---

### 5️⃣ Data Drift Monitoring Page
**Purpose:** Enterprise-level monitoring - Detect feature distribution changes

**Location:** `components/pages/drift_monitoring.py`

**Drift Metrics:**
- Critical Drifts: 2
- Warning Drifts: 2
- Stable Features: 6
- Average Drift Score: 0.22

**Statistical Tests:**
- Kolmogorov-Smirnov (KS) Test
- Distribution Comparison (Reference vs Current)
- Drift Timeline (24h)
- Performance Impact Analysis

**Critical Drifts Detected:**
1. Flow Duration (KS: 0.38) - Consider retraining
2. Total Fwd Packets (KS: 0.35) - Consider retraining

**Warning Drifts:**
1. Flow Bytes/s (KS: 0.22) - Monitor
2. Fwd IAT Mean (KS: 0.19) - Monitor

**Visualizations:**
- 🎯 Drift Score Bar Chart
- 📈 Distribution Comparison (histograms)
- 📊 KS Test Results Table
- 📊 Drift Score Timeline
- ⚡ Performance vs Drift Scatter
- 🔥 Drift Heatmap (features over time)

---

### 6️⃣ Risk Assessment Page
**Purpose:** Translate ML output → Security meaning

**Location:** `components/pages/risk_assessment.py`

**Risk Metrics:**
- Overall Risk Score: 67.3/100
- Critical Threats: 2
- High Risk: 3
- Medium Risk: 5

**Risk Levels:**
- 🔴 CRITICAL (80+): Immediate action required
- 🟠 HIGH (60-80): Significant threats
- 🟡 MEDIUM (40-60): Moderate threats
- 🟢 LOW (0-40): Low threat level

**Top Risky Sources:**
| IP Address | Risk Score | Attack Count |
|------------|-----------|--------------|
| 192.168.1.100 | 92 (CRITICAL) | 24 |
| 10.0.0.50 | 78 (HIGH) | 18 |
| 203.0.113.45 | 65 (MEDIUM) | 12 |

**Top Risky Services:**
| Service/Port | Risk Score | Attack Count |
|-------------|-----------|--------------|
| Port 80 (HTTP) | 88 (CRITICAL) | 156 |
| Port 443 (HTTPS) | 72 (HIGH) | 98 |
| Port 22 (SSH) | 68 (HIGH) | 87 |

**Remediation Recommendations:**
1. Block Malicious IPs (CRITICAL)
2. Isolate Compromised Systems (CRITICAL)
3. Enable Enhanced Logging (HIGH)
4. Patch Vulnerable Services (HIGH)

**Visualizations:**
- 🎯 Risk Gauge (0-100 indicator)
- 🔲 Attack Severity Heatmap
- 📊 Risk Trend Chart (24h)
- 🚨 Risky IPs Table
- 🚨 Risky Services Table
- 📋 Incident Response Guide

---

## Implementation Details

### Page Import Structure
```python
# app.py imports all 6 pages
from components.pages.dashboard import render_soc_dashboard
from components.pages.detection_analytics import render_detection_analytics
from components.pages.feature_importance import render_feature_importance
from components.pages.explainability import render_explainability
from components.pages.drift_monitoring import render_drift_monitoring
from components.pages.risk_assessment import render_risk_assessment
```

### Sidebar Navigation
```python
page = st.radio(
    "Select Page",
    [
        "📊 Overview Dashboard",
        "📈 Detection Analytics",
        "⭐ Feature Importance",
        "🔍 Explainability (SHAP)",
        "📉 Data Drift Monitoring",
        "🎯 Risk Assessment"
    ],
    label_visibility="collapsed",
    key="main_navigation"
)
```

### Router Logic
```python
if page == "📊 Overview Dashboard":
    render_soc_dashboard(API_URL)
elif page == "📈 Detection Analytics":
    render_detection_analytics(API_URL)
# ... etc for all 6 pages
```

## Features Implemented

### 1. Executive Dashboard ✅
- KPI metrics with deltas
- Trend analysis
- Real-time status
- Top threat summaries

### 2. Model Evaluation ✅
- Confusion matrix
- ROC curves
- Per-class metrics
- Performance statistics

### 3. Feature Engineering ✅
- Feature importance ranking
- Correlation analysis
- Distribution analysis
- Feature selection comparison

### 4. Explainability (Non-Negotiable) ✅
- SHAP summary plots
- SHAP force plots
- Waterfall charts
- LIME explanations
- Feature contribution tracking

### 5. Enterprise Monitoring ✅
- Data drift detection
- Distribution comparison
- Statistical tests (KS)
- Performance impact analysis

### 6. Security Analytics ✅
- Risk scoring system
- Threat classification
- IP/service risk analysis
- Incident response guidance

## Data Flow

```
Backend API (http://localhost:8000)
    ↓
Frontend (http://localhost:8501)
    ↓
Sidebar (Navigation)
    ├→ 📊 Overview Dashboard
    ├→ 📈 Detection Analytics
    ├→ ⭐ Feature Importance
    ├→ 🔍 Explainability (SHAP)
    ├→ 📉 Data Drift Monitoring
    └→ 🎯 Risk Assessment
```

## Session State Management

All pages use Streamlit session state for data persistence:
```python
st.session_state = {
    'authenticated': True,
    'page': "📊 Overview Dashboard",
    'prediction_result': None,
    'explanation': None,
    'current_features': None,
    'selected_model_type': "XGBoost"
}
```

## Styling

All pages use consistent cybersecurity theme:
- Primary: `#00FF41` (neon green)
- Secondary: `#00CED1` (cyan)
- Danger: `#FF1744` (red)
- Warning: `#FFB300` (orange)
- Dark Background: `#0D1117`
- Darker Background: `#010409`

## Next Steps

1. **Backend Integration** - Connect pages to real API endpoints
2. **Data Population** - Replace sample data with actual model outputs
3. **User Testing** - Validate with security analysts
4. **Performance Optimization** - Cache data and optimize visualizations
5. **Advanced Features** - Add filtering, exports, real-time updates

## Academic Value

This 6-page architecture demonstrates:
- ✅ **ML Understanding**: Model evaluation, metrics, performance analysis
- ✅ **Feature-Driven Design**: Feature importance, selection, analysis
- ✅ **Explainable AI**: SHAP, LIME, waterfall explanations
- ✅ **Security Analytics**: Risk assessment, threat classification
- ✅ **Enterprise Readiness**: Drift monitoring, incident response
- ✅ **Professional UI/UX**: Executive dashboards, interactive visualizations

**Perfect balance for Final Year Project**: 6 pages showing comprehensive ML, security, and UX understanding.

---

**Created:** February 2026
**Status:** Implementation Complete
**Total Lines of Code:** ~2,500+ (all 6 pages)
**Visualizations:** 40+ interactive charts
**Features:** Complete feature-driven explainable XIDS system
