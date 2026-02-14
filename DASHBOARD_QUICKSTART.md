# XIDS Dashboard Quick Start Guide

## 🚀 Access Your Dashboard

### Services Running
- **Frontend (Streamlit):** http://localhost:8501
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

### Login Credentials
```
Email: demo@xids.local
Password: demo123
```

---

## 📊 6 Dashboard Pages Overview

### Page 1: 📊 Overview Dashboard
**Executive summary of your security posture**

What you'll see:
- Security Score gauge
- Traffic analyzed (24h)
- Total threats detected
- Current risk level
- Threat trends graph
- Attack distribution pie chart
- Top attack types table

**Use case:** Daily security briefing, executive reporting

---

### Page 2: 📈 Detection Analytics
**Model performance and classification metrics**

What you'll see:
- Accuracy, Precision, Recall, F1-Score
- Confusion matrix (all attack types)
- ROC curve with AUC
- Per-class performance breakdown
- Probability distribution
- False positive analysis

**Use case:** Model validation, performance tuning

---

### Page 3: ⭐ Feature Importance
**Which features drive attack detection?**

What you'll see:
- Top 10 most important features
- Feature correlation heatmap
- Feature distributions (Normal vs Attack)
- Feature statistics
- Attack-type-specific importance
- Feature selection method comparison
- Outlier detection analysis

**Use case:** Understanding attack patterns, feature engineering

---

### Page 4: 🔍 Explainability (SHAP)
**Why did the model make this prediction? ⭐ CORE PAGE**

What you'll see:
- SHAP Summary Plot (global importance)
- SHAP Force Plot (how prediction was made)
- Feature Contribution Waterfall
- LIME Local Explanation
- Top contributing features
- Detailed feature analysis
- SHAP vs LIME comparison

**Use case:** Understanding specific predictions, model debugging

---

### Page 5: 📉 Data Drift Monitoring
**Is your model still performing well?**

What you'll see:
- Drift metrics (Critical, Warning, Stable)
- Feature drift scores
- Distribution comparison (Reference vs Current)
- Kolmogorov-Smirnov test results
- Drift timeline (24h)
- Performance impact analysis
- Drift heatmap

**Use case:** Model monitoring, retraining decisions

---

### Page 6: 🎯 Risk Assessment
**What's the security risk level?**

What you'll see:
- Overall risk score (0-100)
- Risk level indicator (Color-coded)
- Critical threats count
- Riskiest source IPs
- Riskiest destination services
- Attack severity heatmap
- Risk trend (24h)
- Incident response recommendations

**Use case:** Security alerting, incident response

---

## 🎯 Common Tasks

### Check Security Status
→ Go to **📊 Overview Dashboard**
- Look at Security Score
- Check Risk Level
- See Threat Trend

### Validate Model Performance
→ Go to **📈 Detection Analytics**
- Check F1-Score and Accuracy
- Review Confusion Matrix
- Analyze False Positives

### Understand What Matters
→ Go to **⭐ Feature Importance**
- See Top 10 Features
- Check correlation heatmap
- Compare selection methods

### Explain a Specific Prediction
→ Go to **🔍 Explainability (SHAP)**
- Choose sample to explain
- View SHAP Force Plot
- See feature contributions

### Check for Model Drift
→ Go to **📉 Data Drift Monitoring**
- Review drift scores
- Check KS test results
- Look at performance impact

### Assess Security Risk
→ Go to **🎯 Risk Assessment**
- Check overall risk score
- See risky IPs/services
- Review incident response steps

---

## 📊 Sample Data Included

All pages come with realistic sample data showing:
- **9,205** network flows analyzed
- **1,705** threats detected (24h)
- **7** attack types detected
- **94.2%** detection rate
- **92.5%** F1-Score
- **10** top features identified

This helps you understand:
- How each page looks with real data
- What metrics to expect
- How to interpret the visualizations

---

## 🔧 Customization Guide

### Change Login Credentials
File: `frontend/components/login.py`
- Update `.users.json` with your credentials

### Modify Color Scheme
File: `frontend/app.py`
- Edit CSS section (lines 38-200)
- Change hex color values

### Add New Page
1. Create `frontend/components/pages/my_page.py`
2. Implement `render_my_page()` function
3. Add to sidebar navigation
4. Import and route in `app.py`

### Connect Real Data
Update page functions to call backend API:
```python
response = requests.get(f"{api_url}/endpoint")
data = response.json()
# Use real data instead of sample data
```

---

## 📖 Key Concepts

### Security Score
Composite metric combining:
- Detection rate (how many attacks caught)
- False positive rate (how many false alarms)
- Model confidence (prediction certainty)
- Risk assessment (threat severity)
- **Range:** 0-100 (higher = safer)

### Risk Level
- 🔴 CRITICAL (80+): Immediate response needed
- 🟠 HIGH (60-80): Urgent investigation
- 🟡 MEDIUM (40-60): Close monitoring
- 🟢 LOW (0-40): Normal operations

### Attack Types Detected
1. **BENIGN** - Normal traffic
2. **DoS** - Denial of Service (single source)
3. **DDoS** - Distributed DoS (multiple sources)
4. **PortScan** - Port scanning reconnaissance
5. **Bot** - Botnet command & control
6. **Brute Force** - Credential guessing
7. **Web Attack** - Application-level attacks

### Drift Monitoring
Detects when data distribution changes:
- **KS Score > 0.3** = Critical drift (retrain)
- **KS Score 0.15-0.3** = Warning drift (monitor)
- **KS Score < 0.15** = Stable (normal)

---

## ⚙️ System Requirements

- Python 3.10+
- 8GB RAM (recommended)
- 2GB free disk space
- Chrome/Firefox/Safari browser

### Current Services
- Backend API: Port 8000 ✅
- Frontend: Port 8501 ✅
- Both running and accessible

---

## 🆘 Troubleshooting

### "API Connection Failed"
**Fix:** Make sure backend is running on port 8000
```powershell
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### "Model Not Loaded"
**Fix:** This is expected - train the model first
```powershell
cd backend/model
python train_model.py
```

### Pages not loading
**Fix:** Clear Streamlit cache
```
Ctrl+Shift+R (Hard refresh in browser)
```

### Port already in use
**Fix:** Kill existing processes
```powershell
taskkill /F /IM python.exe
```

---

## 📚 Learn More

### Understanding SHAP
- SHAP values show feature contribution to prediction
- Positive = pushes toward attack classification
- Negative = pushes toward benign classification
- Magnitude = strength of contribution

### Interpreting Confusion Matrix
- Diagonal = correct predictions
- Off-diagonal = misclassifications
- High values on diagonal = good model
- Look for patterns in errors

### Feature Importance
- Shows which features discriminate attacks from benign
- Higher rank = stronger attack indicator
- Used for feature selection
- Varies by attack type

---

## 🎓 Final Year Project Tips

### When Presenting
- Start with **Overview Dashboard** (big picture)
- Show **Detection Analytics** (model quality)
- Highlight **Feature Importance** (engineering)
- Demo **Explainability** (the "why" - most impressive!)
- Mention **Drift Monitoring** (production readiness)
- Conclude with **Risk Assessment** (security value)

### Key Talking Points
1. Feature-driven design (explain what matters)
2. SHAP explainability (why predictions made)
3. Comprehensive evaluation (metrics & analysis)
4. Enterprise monitoring (drift detection)
5. Security focus (risk assessment)

### Answer Expected Questions
- **Q: Why feature importance?** A: Identifies attack patterns
- **Q: Why SHAP?** A: Explains individual predictions
- **Q: Why drift monitoring?** A: Ensures model stays valid
- **Q: Why risk assessment?** A: Translates ML to security
- **Q: Why 6 pages?** A: Comprehensive analysis system

---

## ✅ Next Steps

1. **Log In** → demo@xids.local / demo123
2. **Explore Each Page** → Spend 2 min on each
3. **Read the Explanations** → Hover over elements
4. **Try Different Features** → Use selectboxes
5. **Connect Real Data** → Replace sample data
6. **Add Your Features** → Customize as needed

---

## 📞 Support

**For issues:**
- Check `IMPLEMENTATION_COMPLETE.md`
- Review `FRONTEND_ARCHITECTURE.md`
- Check `PROJECT_SUMMARY.md`

**All documentation included in project root.**

---

**Enjoy your professional XIDS dashboard! 🛡️**

Built for explainability, security analytics, and enterprise-grade intrusion detection.
