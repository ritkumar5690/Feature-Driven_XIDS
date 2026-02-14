"""
Prediction View Component
Handles single and batch predictions with modern UI
"""

import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import plotly.express as px
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


def create_confidence_gauge(confidence: float, prediction: str) -> go.Figure:
    """
    Create a confidence gauge chart
    
    Args:
        confidence: Confidence score (0-1)
        prediction: Predicted class
        
    Returns:
        Plotly figure
    """
    # Determine color based on prediction and confidence
    if prediction == "BENIGN":
        color = "#28a745"  # Green
    elif confidence >= 0.9:
        color = "#dc3545"  # Red
    elif confidence >= 0.7:
        color = "#fd7e14"  # Orange
    else:
        color = "#ffc107"  # Yellow
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=confidence * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Confidence", 'font': {'size': 24, 'color': '#333'}},
        delta={'reference': 80, 'increasing': {'color': color}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#666"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#ccc",
            'steps': [
                {'range': [0, 50], 'color': '#e8f5e9'},
                {'range': [50, 70], 'color': '#fff3cd'},
                {'range': [70, 90], 'color': '#ffe5d0'},
                {'range': [90, 100], 'color': '#f8d7da'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': "#333", 'family': "Arial"}
    )
    
    return fig


def create_probability_chart(probabilities: Dict[str, float]) -> go.Figure:
    """
    Create probability distribution bar chart
    
    Args:
        probabilities: Dictionary of class probabilities
        
    Returns:
        Plotly figure
    """
    # Sort by probability
    sorted_probs = dict(sorted(probabilities.items(), key=lambda x: x[1], reverse=True))
    
    # Create colors
    colors = ['#4A90E2' if i == 0 else '#95B3D7' for i in range(len(sorted_probs))]
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(sorted_probs.values()),
            y=list(sorted_probs.keys()),
            orientation='h',
            marker=dict(
                color=colors,
                line=dict(color='#333', width=1)
            ),
            text=[f"{v*100:.2f}%" for v in sorted_probs.values()],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Class Probability Distribution",
        xaxis_title="Probability",
        yaxis_title="",
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': "#333", 'family': "Arial"}
    )
    
    fig.update_xaxis(tickformat='.0%', gridcolor='#e0e0e0')
    
    return fig


def display_prediction_result(prediction: str, confidence: float, probabilities: Optional[Dict] = None):
    """
    Display prediction result with modern styling
    
    Args:
        prediction: Predicted class
        confidence: Confidence score
        probabilities: Class probabilities (optional)
    """
    # Determine threat level and styling
    if prediction == "BENIGN":
        threat_color = "#28a745"
        threat_emoji = "✅"
        threat_text = "SAFE"
    elif confidence >= 0.9:
        threat_color = "#dc3545"
        threat_emoji = "🚨"
        threat_text = "CRITICAL THREAT"
    elif confidence >= 0.7:
        threat_color = "#fd7e14"
        threat_emoji = "⚠️"
        threat_text = "HIGH THREAT"
    else:
        threat_color = "#ffc107"
        threat_emoji = "⚡"
        threat_text = "MEDIUM THREAT"
    
    # Main prediction card
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, {threat_color}22 0%, {threat_color}11 100%);
        border-left: 5px solid {threat_color};
        border-radius: 10px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    '>
        <div style='text-align: center;'>
            <h1 style='color: {threat_color}; margin: 0; font-size: 3rem;'>{threat_emoji}</h1>
            <h2 style='color: #333; margin: 0.5rem 0;'>{threat_text}</h2>
            <h3 style='color: {threat_color}; margin: 0.5rem 0; font-size: 2rem;'>{prediction}</h3>
            <p style='color: #666; font-size: 1.1rem; margin: 0.5rem 0;'>
                Confidence: <strong>{confidence*100:.2f}%</strong>
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(
            create_confidence_gauge(confidence, prediction),
            width='stretch',
            key="confidence_gauge"
        )
    
    with col2:
        if probabilities:
            st.plotly_chart(
                create_probability_chart(probabilities),
                width='stretch',
                key="prob_chart"
            )


def render_manual_input(api_url: str):
    """
    Render manual input form for single prediction
    
    Args:
        api_url: Backend API URL
    """
    st.markdown("### 🎯 Manual Feature Input")
    st.markdown("Enter network flow features for prediction:")
    
    # Create input form with common features
    with st.form("feature_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Basic Flow Features**")
            dest_port = st.number_input("Destination Port", min_value=0, max_value=65535, value=80)
            flow_duration = st.number_input("Flow Duration (μs)", min_value=0, value=120000)
            total_fwd = st.number_input("Total Fwd Packets", min_value=0, value=10)
            total_bwd = st.number_input("Total Backward Packets", min_value=0, value=8)
            flow_bytes_s = st.number_input("Flow Bytes/s", min_value=0.0, value=1500.5)
            flow_packets_s = st.number_input("Flow Packets/s", min_value=0.0, value=150.0)
        
        with col2:
            st.markdown("**Packet Length Features**")
            fwd_pkt_len_mean = st.number_input("Fwd Packet Length Mean", min_value=0.0, value=512.0)
            bwd_pkt_len_mean = st.number_input("Bwd Packet Length Mean", min_value=0.0, value=256.0)
            fwd_iat_mean = st.number_input("Fwd IAT Mean", min_value=0.0, value=100.0)
            bwd_iat_mean = st.number_input("Bwd IAT Mean", min_value=0.0, value=150.0)
            flow_iat_mean = st.number_input("Flow IAT Mean", min_value=0.0, value=100.5)
            flow_iat_std = st.number_input("Flow IAT Std", min_value=0.0, value=50.2)
        
        # Submit button
        submitted = st.form_submit_button("🔍 Analyze Traffic", width='stretch')
        
        if submitted:
            # Prepare features
            features = {
                "Destination Port": float(dest_port),
                "Flow Duration": float(flow_duration),
                "Total Fwd Packets": float(total_fwd),
                "Total Backward Packets": float(total_bwd),
                "Flow Bytes/s": float(flow_bytes_s),
                "Flow Packets/s": float(flow_packets_s),
                "Fwd Packet Length Mean": float(fwd_pkt_len_mean),
                "Bwd Packet Length Mean": float(bwd_pkt_len_mean),
                "Fwd IAT Mean": float(fwd_iat_mean),
                "Bwd IAT Mean": float(bwd_iat_mean),
                "Flow IAT Mean": float(flow_iat_mean),
                "Flow IAT Std": float(flow_iat_std)
            }
            
            # Make prediction
            with st.spinner("🔄 Analyzing..."):
                try:
                    response = requests.post(
                        f"{api_url}/predict",
                        json={"features": features},
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state['prediction_result'] = result
                        st.session_state['current_features'] = features
                        st.success("✅ Analysis complete!")
                    else:
                        st.error(f"❌ Prediction failed: {response.text}")
                        
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Connection error: {str(e)}")


def render_csv_upload(api_url: str):
    """
    Render CSV upload interface with detailed status display
    
    Args:
        api_url: Backend API URL
    """
    st.markdown("### 📁 Upload Flow Data (CSV)")
    st.markdown("Upload a CSV file containing network flow features for batch analysis:")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="Upload CSV with network flow features. Each row will be analyzed separately."
    )
    
    if uploaded_file is not None:
        try:
            # Read CSV with progress indication
            df = pd.read_csv(uploaded_file)
            
            # Display detailed status
            st.markdown("**📤 Upload Status:**")
            status_col1, status_col2, status_col3, status_col4 = st.columns(4)
            
            with status_col1:
                st.metric("📊 Total Rows", len(df))
            
            with status_col2:
                st.metric("📋 Total Columns", len(df.columns))
            
            with status_col3:
                st.metric("💾 File Size", f"{uploaded_file.size / 1024:.1f} KB")
            
            with status_col4:
                st.metric("✅ Status", "Loaded")
            
            # Show file details
            with st.expander("📊 Data Preview & Details", expanded=True):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("**First 10 Rows:**")
                    st.dataframe(df.head(10), width='stretch')
                
                with col2:
                    st.markdown("**Column Information:**")
                    column_info = pd.DataFrame({
                        'Column': df.columns,
                        'Type': [str(dtype) for dtype in df.dtypes],
                        'Non-Null': df.notna().sum().values
                    })
                    st.dataframe(column_info, width='stretch', hide_index=True)
            
            # Statistics
            with st.expander("📈 Data Statistics"):
                st.dataframe(df.describe(), width='stretch')
            
            # Analyze button
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
            
            with col_btn1:
                if st.button("🔍 Analyze First Row", width='stretch'):
                    # Get first row features
                    features = df.iloc[0].to_dict()
                    
                    # Make prediction
                    with st.spinner("🔄 Analyzing first row..."):
                        try:
                            response = requests.post(
                                f"{api_url}/predict",
                                json={"features": features},
                                timeout=10
                            )
                            
                            if response.status_code == 200:
                                result = response.json()
                                st.session_state['prediction_result'] = result
                                st.session_state['current_features'] = features
                                st.success("✅ Analysis complete!")
                            else:
                                st.error(f"❌ Prediction failed: {response.text}")
                                
                        except requests.exceptions.RequestException as e:
                            st.error(f"❌ Connection error: {str(e)}")
            
            with col_btn2:
                if st.button("⚡ Batch Analyze", width='stretch'):
                    # Analyze all rows
                    with st.spinner(f"🔄 Analyzing {len(df)} rows..."):
                        results = []
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        try:
                            for idx, row in df.iterrows():
                                features = row.to_dict()
                                
                                response = requests.post(
                                    f"{api_url}/predict",
                                    json={"features": features},
                                    timeout=10
                                )
                                
                                if response.status_code == 200:
                                    result = response.json()
                                    results.append({
                                        'row': idx + 1,
                                        'prediction': result.get('prediction'),
                                        'confidence': result.get('confidence')
                                    })
                                
                                # Update progress
                                progress = (idx + 1) / len(df)
                                progress_bar.progress(progress)
                                status_text.text(f"Processing row {idx + 1}/{len(df)}")
                            
                            if results:
                                st.session_state['batch_results'] = results
                                st.success(f"✅ Batch analysis complete! Analyzed {len(results)} rows")
                            else:
                                st.error("❌ No results returned from analysis")
                                
                        except requests.exceptions.RequestException as e:
                            st.error(f"❌ Connection error: {str(e)}")
            
            # Show batch results if available
            if 'batch_results' in st.session_state:
                st.markdown("---")
                st.markdown("### 📊 Batch Analysis Results")
                
                results_df = pd.DataFrame(st.session_state['batch_results'])
                st.dataframe(results_df, width='stretch', hide_index=True)
                
                # Summary statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    benign_count = (results_df['prediction'] == 'BENIGN').sum()
                    st.metric("🟢 Benign Flows", benign_count)
                with col2:
                    threat_count = (results_df['prediction'] != 'BENIGN').sum()
                    st.metric("🔴 Threats Detected", threat_count)
                with col3:
                    avg_confidence = results_df['confidence'].mean()
                    st.metric("📊 Avg Confidence", f"{avg_confidence*100:.2f}%")
        
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            st.info("💡 Tip: Ensure the CSV file is properly formatted with valid data")


def render_prediction_view(api_url: str):
    """
    Main prediction view renderer
    
    Args:
        api_url: Backend API URL
    """
    st.markdown("## 🎯 Single Prediction")
    
    # Get input method from session state
    input_method = st.session_state.get('input_method', 'Manual Entry')
    
    # Render appropriate input method
    if input_method == "Manual Entry":
        render_manual_input(api_url)
    else:
        render_csv_upload(api_url)
    
    # Display results if available
    if 'prediction_result' in st.session_state:
        st.markdown("---")
        st.markdown("## 📊 Results")
        
        result = st.session_state['prediction_result']
        display_prediction_result(
            result['prediction'],
            result['confidence'],
            result.get('probabilities')
        )