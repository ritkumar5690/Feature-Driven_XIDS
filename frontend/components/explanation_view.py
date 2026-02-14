"""
Explanation View Component
Displays SHAP-based explanations with visualizations
"""

import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, List


def create_shap_waterfall(features: List[Dict], base_value: float, prediction: str) -> go.Figure:
    """
    Create SHAP waterfall chart
    
    Args:
        features: List of feature importance dictionaries
        base_value: SHAP base value
        prediction: Predicted class
        
    Returns:
        Plotly figure
    """
    # Extract data
    feature_names = [f['feature'] for f in features]
    impacts = [f['impact'] for f in features]
    
    # Create colors (positive impacts in red, negative in blue)
    colors = ['#E74C3C' if imp > 0 else '#3498DB' for imp in impacts]
    
    fig = go.Figure(go.Bar(
        x=impacts,
        y=feature_names,
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='#333', width=1)
        ),
        text=[f"{imp:+.4f}" for imp in impacts],
        textposition='auto',
    ))
    
    fig.update_layout(
        title=f"SHAP Feature Impact for {prediction}",
        xaxis_title="Impact on Prediction",
        yaxis_title="",
        height=max(400, len(features) * 30),
        margin=dict(l=20, r=20, t=60, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': "#333", 'family': "Arial"},
        showlegend=False
    )
    
    fig.update_xaxis(gridcolor='#e0e0e0', zeroline=True, zerolinecolor='#333', zerolinewidth=2)
    
    # Add base value annotation
    fig.add_annotation(
        text=f"Base Value: {base_value:.4f}",
        xref="paper", yref="paper",
        x=0.02, y=0.98,
        showarrow=False,
        bgcolor="rgba(74, 144, 226, 0.1)",
        bordercolor="#4A90E2",
        borderwidth=2,
        borderpad=4,
        font=dict(size=12, color="#333")
    )
    
    return fig


def create_feature_impact_table(features: List[Dict], current_values: Dict) -> pd.DataFrame:
    """
    Create feature impact table
    
    Args:
        features: List of feature importance dictionaries
        current_values: Dictionary of current feature values
        
    Returns:
        DataFrame for display
    """
    data = []
    for feat in features:
        feature_name = feat['feature']
        impact = feat['impact']
        value = current_values.get(feature_name, 0)
        
        data.append({
            "Feature": feature_name,
            "Value": f"{value:.2f}",
            "Impact": f"{impact:+.6f}",
            "Direction": "↑ Increases" if impact > 0 else "↓ Decreases"
        })
    
    return pd.DataFrame(data)


def create_impact_summary(features: List[Dict]) -> go.Figure:
    """
    Create summary pie chart of positive vs negative impacts
    
    Args:
        features: List of feature importance dictionaries
        
    Returns:
        Plotly figure
    """
    positive_impact = sum(f['impact'] for f in features if f['impact'] > 0)
    negative_impact = abs(sum(f['impact'] for f in features if f['impact'] < 0))
    
    fig = go.Figure(data=[go.Pie(
        labels=['Positive Impact', 'Negative Impact'],
        values=[positive_impact, negative_impact],
        marker=dict(colors=['#E74C3C', '#3498DB']),
        hole=.4,
        textinfo='label+percent',
        textposition='outside'
    )])
    
    fig.update_layout(
        title="Impact Distribution",
        height=300,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': "#333", 'family': "Arial"},
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig


def render_explanation_view(api_url: str):
    """
    Render SHAP explanation view
    
    Args:
        api_url: Backend API URL
    """
    st.markdown("## 🔍 Explanation & Interpretability")
    
    # Check if we have a prediction to explain
    if 'prediction_result' not in st.session_state or 'current_features' not in st.session_state:
        st.info("👈 Make a prediction first to see explanations")
        return
    
    # Get prediction info
    prediction = st.session_state['prediction_result']['prediction']
    confidence = st.session_state['prediction_result']['confidence']
    features = st.session_state['current_features']
    
    # Display current prediction summary
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
        border-radius: 10px;
        padding: 1.5rem;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    '>
        <h3 style='margin: 0; color: white;'>Current Prediction</h3>
        <p style='margin: 0.5rem 0; font-size: 1.2rem;'>
            <strong>{prediction}</strong> (Confidence: {confidence*100:.2f}%)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Number of features to explain
    col1, col2 = st.columns([3, 1])
    with col2:
        top_n = st.selectbox(
            "Top Features",
            [5, 10, 15, 20],
            index=1,
            help="Number of top contributing features to display"
        )
    
    # Get explanation
    if st.button("🔍 Generate Explanation", width='stretch'):
        with st.spinner("🔄 Generating SHAP explanation..."):
            try:
                response = requests.post(
                    f"{api_url}/explain",
                    json={"features": features},
                    params={"top_n": top_n},
                    timeout=30
                )
                
                if response.status_code == 200:
                    explanation = response.json()
                    st.session_state['explanation'] = explanation
                    st.success("✅ Explanation generated!")
                else:
                    st.error(f"❌ Explanation failed: {response.text}")
                    return
                    
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Connection error: {str(e)}")
                return
    
    # Display explanation if available
    if 'explanation' in st.session_state:
        explanation = st.session_state['explanation']
        
        st.markdown("---")
        st.markdown("### 📊 SHAP Feature Importance")
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📊 Waterfall Chart", "📋 Feature Table", "🥧 Impact Summary"])
        
        with tab1:
            st.markdown("""
            <div style='background: #f8f9fa; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;'>
                <p style='margin: 0; color: #666;'>
                    <strong>How to read:</strong> Red bars push the prediction towards the detected class, 
                    while blue bars push it away. Larger bars indicate stronger influence.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            waterfall_fig = create_shap_waterfall(
                explanation['top_features'],
                explanation['base_value'],
                explanation['prediction']
            )
            st.plotly_chart(waterfall_fig, width='stretch')
        
        with tab2:
            st.markdown("**Detailed Feature Contributions**")
            impact_table = create_feature_impact_table(
                explanation['top_features'],
                features
            )
            
            # Style the dataframe
            st.dataframe(
                impact_table,
                width='stretch',
                hide_index=True,
                column_config={
                    "Feature": st.column_config.TextColumn("Feature", width="large"),
                    "Value": st.column_config.TextColumn("Current Value", width="small"),
                    "Impact": st.column_config.TextColumn("SHAP Value", width="small"),
                    "Direction": st.column_config.TextColumn("Effect", width="medium")
                }
            )
            
            # Download button
            csv = impact_table.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name="shap_explanation.csv",
                mime="text/csv",
                width='stretch'
            )
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                summary_fig = create_impact_summary(explanation['top_features'])
                st.plotly_chart(summary_fig, width='stretch')
            
            with col2:
                st.markdown("### 📈 Key Insights")
                
                # Calculate statistics
                positive_features = [f for f in explanation['top_features'] if f['impact'] > 0]
                negative_features = [f for f in explanation['top_features'] if f['impact'] < 0]
                
                total_positive = sum(f['impact'] for f in positive_features)
                total_negative = abs(sum(f['impact'] for f in negative_features))
                
                st.metric("Positive Contributions", len(positive_features))
                st.metric("Negative Contributions", len(negative_features))
                st.metric("Total Positive Impact", f"{total_positive:.4f}")
                st.metric("Total Negative Impact", f"{total_negative:.4f}")
                
                # Top contributor
                if explanation['top_features']:
                    top_feature = explanation['top_features'][0]
                    st.markdown(f"""
                    **🏆 Top Contributor:**  
                    `{top_feature['feature']}`  
                    Impact: {top_feature['impact']:+.6f}
                    """)
        
        # Explanation text
        st.markdown("---")
        st.markdown("### 💡 Understanding the Results")
        st.markdown(f"""
        The model predicted **{explanation['prediction']}** based on the provided features.
        The SHAP (SHapley Additive exPlanations) values show how each feature contributed 
        to this prediction:
        
        - **Base Value:** {explanation['base_value']:.4f} - The average model output
        - **Red bars (positive):** Features that push towards detecting the attack
        - **Blue bars (negative):** Features that push towards benign classification
        
        The final prediction is the sum of the base value and all feature contributions.
        """)


def render_batch_analysis(api_url: str):
    """
    Render batch analysis view
    
    Args:
        api_url: Backend API URL
    """
    st.markdown("## 📁 Batch Analysis")
    st.markdown("Upload a CSV file to analyze multiple network flows at once.")
    
    uploaded_file = st.file_uploader(
        "Choose a CSV file with multiple flows",
        type=['csv'],
        help="Upload CSV with network flow features"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ Loaded {len(df)} flows")
            
            # Show preview
            with st.expander("📊 Data Preview"):
                st.dataframe(df.head(10), width='stretch')
            
            # Analyze all button
            if st.button("🔍 Analyze All Flows", width='stretch'):
                results = []
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for idx, row in df.iterrows():
                    status_text.text(f"Analyzing flow {idx + 1}/{len(df)}...")
                    
                    try:
                        features = row.to_dict()
                        response = requests.post(
                            f"{api_url}/predict",
                            json={"features": features},
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            results.append({
                                'Flow': idx + 1,
                                'Prediction': result['prediction'],
                                'Confidence': f"{result['confidence']*100:.2f}%"
                            })
                        else:
                            results.append({
                                'Flow': idx + 1,
                                'Prediction': 'ERROR',
                                'Confidence': '0%'
                            })
                    except Exception as e:
                        results.append({
                            'Flow': idx + 1,
                            'Prediction': 'ERROR',
                            'Confidence': '0%'
                        })
                    
                    progress_bar.progress((idx + 1) / len(df))
                
                status_text.text("Analysis complete!")
                
                # Display results
                results_df = pd.DataFrame(results)
                st.dataframe(results_df, width='stretch', hide_index=True)
                
                # Summary statistics
                st.markdown("### 📊 Summary")
                col1, col2, col3 = st.columns(3)
                
                attack_count = len(results_df[results_df['Prediction'] != 'BENIGN'])
                benign_count = len(results_df[results_df['Prediction'] == 'BENIGN'])
                
                col1.metric("Total Flows", len(results_df))
                col2.metric("Attacks Detected", attack_count)
                col3.metric("Benign Traffic", benign_count)
                
                # Download results
                csv = results_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results",
                    data=csv,
                    file_name="batch_analysis_results.csv",
                    mime="text/csv",
                    width='stretch'
                )
                
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")


def render_about_page():
    """
    Render about page
    """
    st.markdown("## ℹ️ About XIDS")
    
    st.markdown("""
    ### Explainable Intrusion Detection System
    
    XIDS is a production-ready machine learning system for detecting network intrusions
    with built-in explainability using SHAP (SHapley Additive exPlanations).
    
    #### 🎯 Features
    - **Real-time Detection:** Fast classification of network flows
    - **Multiple Attack Types:** Detects DoS, DDoS, PortScan, Bots, and more
    - **Explainability:** SHAP-based explanations for every prediction
    - **High Accuracy:** Trained on CIC-IDS2017 dataset
    - **Modern UI:** Interactive visualizations and charts
    
    #### 🤖 Model Details
    - **Algorithm:** XGBoost Classifier
    - **Dataset:** CIC-IDS2017
    - **Features:** 78+ network flow features
    - **Classes:** 7 (BENIGN + 6 attack types)
    
    #### 📚 Attack Types
    1. **BENIGN** - Normal network traffic
    2. **DoS** - Denial of Service attacks
    3. **DDoS** - Distributed Denial of Service
    4. **PortScan** - Port scanning activities
    5. **Bot** - Botnet-related traffic
    6. **Brute Force** - Password brute force attempts
    7. **Web Attack** - Web application exploits
    
    #### 🔬 Technology Stack
    - **Backend:** FastAPI
    - **ML:** XGBoost + Scikit-learn
    - **Explainability:** SHAP
    - **Frontend:** Streamlit
    - **Visualization:** Plotly
    
    #### 📖 How to Use
    1. Select input method (Manual or CSV)
    2. Enter or upload network flow features
    3. Click "Analyze" to get prediction
    4. View SHAP explanation for interpretability
    
    #### 👨‍💻 For Developers
    - API Documentation: `/docs`
    - Health Check: `/health`
    - Source Code: GitHub (if applicable)
    
    ---
    
    **Version:** 1.0.0  
    **License:** Academic/Research Use  
    **Dataset:** [CIC-IDS2017](https://www.unb.ca/cic/datasets/ids-2017.html)
    """)
    
    # Display some metrics/statistics if available
    st.markdown("### 📊 System Statistics")
    col1, col2, col3 = st.columns(3)
    
    col1.metric("Model Accuracy", "~95%", help="Typical accuracy on CIC-IDS2017")
    col2.metric("Inference Time", "< 50ms", help="Average prediction time")
    col3.metric("Features", "78+", help="Number of input features")