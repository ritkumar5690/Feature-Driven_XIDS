"""
Sidebar Component for XIDS Frontend
Contains navigation, file upload, and model information
"""

import streamlit as st
import pandas as pd
import requests
import logging
from components.login import logout, get_current_user

logger = logging.getLogger(__name__)


def render_sidebar(api_url: str):
    """
    Render the sidebar with navigation and controls
    
    Args:
        api_url: Backend API base URL
    """
    with st.sidebar:
        # User info and logout button
        current_user = get_current_user()
        if current_user:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #16202E 0%, #1A1F2E 100%); padding: 0.8rem; border-radius: 5px; border: 2px solid #00CED1; box-shadow: 0 0 10px rgba(0, 206, 209, 0.3);'>
                    <small style='color: #00CED1;'>Logged in as</small><br>
                    <b style='color: #00FF41; text-shadow: 0 0 5px rgba(0, 255, 65, 0.3);'>{current_user['username']}</b><br>
                    <small style='color: #00CED1;'>{current_user['email']}</small>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("🚪", help="Logout", key="logout_btn"):
                    logout()
                    st.rerun()
            st.markdown("---")
        
        # Logo and title
        st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h1 style='color: #00FF41; margin: 0; text-shadow: 0 0 20px rgba(0, 255, 65, 0.5);'>🛡️ XIDS</h1>
            <p style='color: #00CED1; font-size: 0.9rem; margin: 0.5rem 0; text-shadow: 0 0 10px rgba(0, 206, 209, 0.3);'>
                Explainable Intrusion Detection
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation - Multi-page dashboard
        st.markdown("### 📊 Dashboard Navigation")
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
        
        st.markdown("---")
        
        # Tools and Analysis
        st.markdown("### 🔧 Analysis Tools")
        show_tools = st.radio(
            "Tools",
            [
                "📊 Dashboard",
                "🎯 Manual Prediction",
                "📁 Batch Analysis"
            ],
            label_visibility="collapsed",
            key="tools_navigation",
            help="Select analysis tool or dashboard"
        )
        
        # Store tool selection in session state
        if show_tools != "📊 Dashboard":
            st.session_state['selected_tool'] = show_tools
        
        st.markdown("---")
        
        # Model information
        st.markdown("### 🤖 Model Status")
        try:
            response = requests.get(f"{api_url}/health", timeout=5)
            if response.status_code == 200:
                health = response.json()
                
                if health.get("model_loaded", False):
                    st.success("✅ Model Loaded")
                    st.info(f"**Type:** {health.get('model_type', 'Unknown')}")
                    st.info(f"**Features:** {health.get('feature_count', 0)}")
                else:
                    st.warning("⚠️ Model Not Loaded")
            else:
                st.error("❌ API Unreachable")
        except requests.exceptions.RequestException:
            st.error("❌ API Connection Failed")
        
        st.markdown("---")
        
        # Attack types info
        with st.expander("📋 Detected Attack Types"):
            st.markdown("""
            - **BENIGN** - Normal traffic
            - **DoS** - Denial of Service
            - **DDoS** - Distributed DoS
            - **PortScan** - Port scanning
            - **Bot** - Botnet activity
            - **Brute Force** - Password attacks
            - **Web Attack** - Web exploits
            """)
        
        # Dataset info
        with st.expander("📚 Dataset Info"):
            st.markdown("""
            **CIC-IDS2017**
            
            Industry-standard dataset for intrusion detection research.
            
            Contains realistic network traffic with labeled attacks.
            
            [Learn More](https://www.unb.ca/cic/datasets/ids-2017.html)
            """)
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #00CED1; font-size: 0.8rem;'>
            <p style='color: #00FF41;'>XIDS v1.0.0</p>
            <p>Powered by XGBoost & SHAP</p>
        </div>
        """, unsafe_allow_html=True)
    
    return page


def get_sample_features():
    """
    Get sample feature dictionary for testing
    
    Returns:
        Dictionary of sample features
    """
    return {
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
        "Flow IAT Min": 10,
        "Fwd IAT Total": 1000,
        "Fwd IAT Mean": 100.0,
        "Fwd IAT Std": 25.5,
        "Fwd IAT Max": 150,
        "Fwd IAT Min": 50,
        "Bwd IAT Total": 800,
        "Bwd IAT Mean": 100.0,
        "Bwd IAT Std": 20.3,
        "Bwd IAT Max": 120,
        "Bwd IAT Min": 60
    }
