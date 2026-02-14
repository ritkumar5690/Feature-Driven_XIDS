"""
XIDS - Explainable Intrusion Detection System
Main Streamlit Application - Multi-Page Dashboard
"""

import streamlit as st
import os
from dotenv import load_dotenv
import logging

# Import components
from components.sidebar import render_sidebar
from components.pages.dashboard import render_soc_dashboard
from components.pages.detection_analytics import render_detection_analytics
from components.pages.feature_importance import render_feature_importance
from components.pages.explainability import render_explainability
from components.pages.drift_monitoring import render_drift_monitoring
from components.pages.risk_assessment import render_risk_assessment
from components.login import render_login_page, check_authentication

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="XIDS - Explainable IDS",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for cybersecurity theme styling
st.markdown("""
<style>
    /* Main theme colors - Cybersecurity Theme */
    :root {
        --primary-color: #00FF41;
        --secondary-color: #00CED1;
        --danger-color: #FF1744;
        --warning-color: #FFB300;
        --dark-bg: #0D1117;
        --darker-bg: #010409;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main page background */
    .main {
        background-color: #0D1117;
        color: #E8E8E8;
    }
    
    /* Custom header styling */
    .main-header {
        background: linear-gradient(135deg, #00FF41 0%, #00CED1 100%);
        padding: 2rem;
        border-radius: 10px;
        color: #010409;
        margin-bottom: 2rem;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.5);
        text-shadow: 0 0 10px rgba(0, 255, 65, 0.3);
    }
    
    /* Card styling */
    .info-card {
        background: #1A1F2E;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(0, 206, 209, 0.3);
        margin: 1rem 0;
        border-left: 4px solid #00FF41;
        color: #E8E8E8;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #00FF41 0%, #00CED1 100%);
        color: #010409;
        border: 2px solid #00FF41;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.8);
        text-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #00FF41;
        text-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1A1F2E;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #16202E;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
        color: #A0A0A0;
        border: 1px solid #00CED1;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00FF41 0%, #00CED1 100%);
        color: #010409;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.5);
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        background: #1A1F2E;
        color: #E8E8E8;
    }
    
    /* Alert styling */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid;
        background-color: #1A1F2E;
        color: #E8E8E8;
    }
    
    /* Form styling */
    .stForm {
        background: #1A1F2E;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #00CED1;
        color: #E8E8E8;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #16202E 0%, #0D1117 100%);
        border-right: 2px solid #00FF41;
    }
    
    /* Input field styling */
    .stNumberInput>div>div>input,
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select {
        border-radius: 8px;
        border: 2px solid #00CED1;
        padding: 0.5rem;
        background-color: #1A1F2E;
        color: #00FF41;
    }
    
    .stNumberInput>div>div>input:focus,
    .stTextInput>div>div>input:focus {
        border-color: #00FF41;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.5);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #16202E;
        border-radius: 8px;
        font-weight: 600;
        border: 1px solid #00CED1;
        color: #00FF41;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #00FF41 0%, #00CED1 100%);
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
    }
    
    /* Text styling */
    body, p, span {
        color: #E8E8E8;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #00FF41;
        text-shadow: 0 0 10px rgba(0, 255, 65, 0.3);
    }
</style>
""", unsafe_allow_html=True)

def main():
    """
    Main application function - Multi-page dashboard and analysis tools
    """
    # Get API URL from environment or use default
    API_URL = os.getenv("API_URL", "http://localhost:8000")
    
    # Initialize session state for all pages
    if 'prediction_result' not in st.session_state:
        st.session_state['prediction_result'] = None
    if 'current_features' not in st.session_state:
        st.session_state['current_features'] = None
    if 'explanation' not in st.session_state:
        st.session_state['explanation'] = None
    if 'page' not in st.session_state:
        st.session_state['page'] = "📊 Overview Dashboard"
    if 'selected_model_type' not in st.session_state:
        st.session_state['selected_model_type'] = "XGBoost"
    if 'selected_tool' not in st.session_state:
        st.session_state['selected_tool'] = None
    if 'input_method' not in st.session_state:
        st.session_state['input_method'] = 'Manual Entry'
    
    # Render sidebar and get selected page
    page = render_sidebar(API_URL)
    
    # Check if a tool is selected instead of dashboard page
    selected_tool = st.session_state.get('selected_tool')
    
    if selected_tool == "🎯 Manual Prediction":
        # Show manual prediction and CSV upload
        st.markdown("## 🎯 Traffic Analysis Tools")
        
        # Tabs for input methods
        tab1, tab2 = st.tabs(["✏️ Manual Entry", "📁 CSV Upload"])
        
        with tab1:
            st.session_state['input_method'] = 'Manual Entry'
            from components.prediction_view import render_manual_input
            render_manual_input(API_URL)
        
        with tab2:
            st.session_state['input_method'] = 'CSV Upload'
            from components.prediction_view import render_csv_upload
            render_csv_upload(API_URL)
        
        # Show results if available
        if 'prediction_result' in st.session_state and st.session_state['prediction_result']:
            st.markdown("---")
            st.markdown("## 📊 Prediction Results")
            from components.prediction_view import display_prediction_result
            result = st.session_state['prediction_result']
            display_prediction_result(
                result['prediction'],
                result['confidence'],
                result.get('probabilities')
            )
    
    elif selected_tool == "📁 Batch Analysis":
        # Show batch analysis
        st.markdown("## 📁 Batch Analysis")
        from components.prediction_view import render_csv_upload
        render_csv_upload(API_URL)
    
    else:
        # Default to dashboard pages
        # Default to dashboard if page is None
        if page is None:
            page = "📊 Overview Dashboard"
        
        # Store current page in session state
        st.session_state['page'] = page
        
        # Route to appropriate page component
        if page == "📊 Overview Dashboard":
            render_soc_dashboard(API_URL)
        
        elif page == "📈 Detection Analytics":
            render_detection_analytics(API_URL)
        
        elif page == "⭐ Feature Importance":
            render_feature_importance(API_URL)
        
        elif page == "🔍 Explainability (SHAP)":
            render_explainability(API_URL)
        
        elif page == "📉 Data Drift Monitoring":
            render_drift_monitoring(API_URL)
        
        elif page == "🎯 Risk Assessment":
            render_risk_assessment(API_URL)


if __name__ == "__main__":
    try:
        # Initialize authentication state
        if 'authenticated' not in st.session_state:
            st.session_state['authenticated'] = False
        
        # Check if user is authenticated
        if not check_authentication():
            render_login_page()
        else:
            main()
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        st.error(f"❌ An error occurred: {str(e)}")
        st.info("Please check the logs for more details.")
