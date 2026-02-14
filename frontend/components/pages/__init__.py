"""
XIDS Pages Package
Multi-page dashboard components
"""

from .dashboard import render_soc_dashboard
from .detection_analytics import render_detection_analytics
from .feature_importance import render_feature_importance
from .explainability import render_explainability
from .drift_monitoring import render_drift_monitoring
from .risk_assessment import render_risk_assessment

__all__ = [
    'render_soc_dashboard',
    'render_detection_analytics',
    'render_feature_importance',
    'render_explainability',
    'render_drift_monitoring',
    'render_risk_assessment'
]
