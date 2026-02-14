"""
XIDS Explainability Page
SHAP and LIME-based model explanations
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


def render_explainability(api_url: str):
    """
    Render Explainability page with SHAP/LIME explanations
    
    Args:
        api_url: Base URL of the backend API
    """
    st.markdown("# 🔍 Explainability (SHAP/LIME)")
    st.markdown("**Understand model predictions: Why did the model classify this as an attack?**")
    
    # Generate sample explainability data
    explain_data = generate_explainability_data()
    
    # Selection method
    col1, col2 = st.columns(2)
    
    with col1:
        explanation_method = st.radio(
            "Explanation Method",
            ["SHAP Summary", "SHAP Force Plot", "Waterfall Chart"],
            key="explain_method"
        )
    
    with col2:
        sample_prediction = st.selectbox(
            "Sample Prediction",
            ["Attack Sample #1", "Attack Sample #2", "Attack Sample #3", "Normal Sample #1"],
            key="explain_sample"
        )
    
    st.divider()
    
    # SHAP Summary Plot
    if explanation_method == "SHAP Summary":
        st.markdown("## 📊 SHAP Summary Plot")
        st.markdown("Shows the impact of each feature on model output across all samples")
        
        summary_fig = create_shap_summary_plot(explain_data['shap_values'])
        st.plotly_chart(summary_fig, width='stretch')
        
        st.markdown("""
        **Interpretation:**
        - Color: Red = high feature value, Blue = low feature value
        - Position: Left = decreases prediction, Right = increases prediction
        - Size: Larger dots = more important
        """)
    
    # SHAP Force Plot
    elif explanation_method == "SHAP Force Plot":
        st.markdown("## 🔥 SHAP Force Plot (Individual Sample)")
        st.markdown("Shows how each feature contributes to push the model output from base value to prediction")
        
        force_fig = create_shap_force_plot(explain_data['force_plot_data'])
        st.plotly_chart(force_fig, width='stretch')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Prediction Details")
            st.info(f"""
            **Prediction: Attack (DDoS)**
            
            - Confidence: 97.2%
            - Base Value: 0.14
            - Final Value: 2.45
            - Impact: +1.31
            """)
        
        with col2:
            st.markdown("### Top Contributing Features")
            st.dataframe(
                explain_data['top_contributing_features'],
                width='stretch',
                hide_index=True,
                column_config={
                    "Feature": st.column_config.TextColumn(width="medium"),
                    "Value": st.column_config.NumberColumn(width="small", format="%.2f"),
                    "SHAP Impact": st.column_config.ProgressColumn(min_value=-0.5, max_value=0.5, width="small"),
                }
            )
    
    # Waterfall Chart
    else:  # Waterfall Chart
        st.markdown("## 📉 Feature Contribution Waterfall")
        st.markdown("Cumulative contribution of features to final prediction")
        
        waterfall_fig = create_waterfall_chart(explain_data['waterfall_data'])
        st.plotly_chart(waterfall_fig, width='stretch')
        
        st.markdown("""
        **How to Read:**
        - Start: Base value (model average prediction)
        - Bars: Each feature's additive contribution
        - End: Final prediction value
        - Red: Pushes toward attack
        - Blue: Pushes toward benign
        """)
    
    st.divider()
    
    # Feature explanation details
    st.markdown("## 🔬 Detailed Feature Analysis")
    
    selected_feature = st.selectbox(
        "Select Feature for Deep Dive",
        explain_data['feature_list'],
        key="feature_analysis"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### Feature: {selected_feature}")
        
        feature_detail = explain_data['feature_details'][selected_feature]
        
        st.metric(
            label="Current Value",
            value=f"{feature_detail['value']:.2f}",
            delta=None
        )
        
        st.metric(
            label="SHAP Value",
            value=f"{feature_detail['shap_value']:.4f}",
            delta=f"Pushes {'toward attack' if feature_detail['shap_value'] > 0 else 'toward benign'}"
        )
        
        st.markdown(f"""
        **Statistics:**
        - Mean (Normal): {feature_detail['mean_normal']:.2f}
        - Mean (Attack): {feature_detail['mean_attack']:.2f}
        - Percentile: {feature_detail['percentile']:.1f}%
        """)
    
    with col2:
        # Feature impact visualization
        impact_fig = create_feature_impact_chart(explain_data['feature_list'])
        st.plotly_chart(impact_fig, width='stretch')
    
    st.divider()
    
    # LIME Explanation (Alternative)
    st.markdown("## 🍋 LIME: Local Interpretable Model-Agnostic Explanations")
    st.markdown("Alternative interpretation: Local linear approximation around the sample")
    
    col1, col2 = st.columns(2)
    
    with col1:
        lime_fig = create_lime_explanation(explain_data['lime_data'])
        st.plotly_chart(lime_fig, width='stretch')
    
    with col2:
        st.markdown("### LIME Model Quality")
        st.metric(
            label="Model Fidelity (R²)",
            value=0.876,
            delta="+0.05"
        )
        
        st.markdown("""
        **LIME Interpretation:**
        LIME creates a local linear model around
        the sample to explain the prediction.
        
        **Advantages:**
        - Model-agnostic (works with any model)
        - Easy to understand (linear)
        - Local approximation near decision boundary
        
        **vs SHAP:**
        - SHAP: Game theory based
        - LIME: Local linear approximation
        - Both complementary approaches
        """)


def generate_explainability_data() -> dict:
    """Generate sample explainability data"""
    
    feature_list = [
        'Flow Duration',
        'Total Fwd Packets',
        'Total Bwd Packets',
        'Flow Bytes/s',
        'Fwd PSH Flags',
        'Bwd PSH Flags',
        'Flow Packets/s',
        'Fwd IAT Mean',
        'Bwd IAT Mean',
        'Fwd Packet Length Mean'
    ]
    
    # SHAP values
    shap_values = np.random.normal(0, 0.15, (1000, len(feature_list)))
    shap_feature_values = np.random.uniform(0, 10000, (1000, len(feature_list)))
    
    # Force plot data
    force_plot_data = {
        'base_value': 0.14,
        'features': feature_list[:7],
        'shap_values': [0.32, 0.28, 0.24, 0.18, 0.15, 0.12, 0.06],
        'feature_values': [2500, 150, 120, 3200, 5, 4, 250]
    }
    
    # Top contributing features
    top_contributing = pd.DataFrame({
        'Feature': ['Flow Duration', 'Total Fwd Packets', 'Flow Bytes/s', 'Fwd PSH Flags', 'Total Bwd Packets'],
        'Value': [2500.5, 150, 3200.5, 5, 120],
        'SHAP Impact': [0.32, 0.28, 0.24, 0.18, 0.15]
    })
    
    # Waterfall data
    waterfall_data = {
        'Feature': ['Base Value', 'Flow Duration', 'Total Fwd Packets', 'Flow Bytes/s', 
                   'Fwd PSH Flags', 'Total Bwd Packets', 'Prediction'],
        'Value': [0.14, 0.32, 0.28, 0.24, 0.18, 0.15, 2.45],
        'Cumulative': [0.14, 0.46, 0.74, 0.98, 1.16, 1.31, 1.45]
    }
    
    # Feature details
    feature_details = {
        'Flow Duration': {
            'value': 2500.5,
            'shap_value': 0.3245,
            'mean_normal': 1200.0,
            'mean_attack': 3500.0,
            'percentile': 78.5
        },
        'Total Fwd Packets': {
            'value': 150,
            'shap_value': 0.2812,
            'mean_normal': 50,
            'mean_attack': 180,
            'percentile': 82.3
        }
    }
    
    # LIME data
    lime_data = {
        'features': feature_list[:6],
        'weights': [0.28, 0.22, 0.18, 0.15, 0.12, 0.05]
    }
    
    return {
        'shap_values': shap_values,
        'shap_feature_values': shap_feature_values,
        'force_plot_data': force_plot_data,
        'top_contributing_features': top_contributing,
        'waterfall_data': waterfall_data,
        'feature_list': feature_list,
        'feature_details': feature_details,
        'lime_data': lime_data
    }


def create_shap_summary_plot(shap_values: np.ndarray) -> go.Figure:
    """Create SHAP summary plot"""
    
    # Create scatter plot showing SHAP values
    feature_names = [f'Feature {i+1}' for i in range(shap_values.shape[1])]
    
    fig = go.Figure()
    
    for i, feature in enumerate(feature_names[:10]):
        fig.add_trace(go.Scatter(
            x=shap_values[:, i],
            y=[feature] * len(shap_values),
            mode='markers',
            marker=dict(
                size=5,
                color=shap_values[:, i],
                colorscale='RdBu',
                showscale=(i == 9),
                colorbar=dict(title="SHAP Value")
            ),
            name=feature,
            hovertemplate=f'<b>{feature}</b><br>SHAP: %{{x:.4f}}<extra></extra>'
        ))
    
    fig.update_layout(
        title=None,
        xaxis_title='SHAP Value (Model Output Impact)',
        yaxis_title=None,
        paper_bgcolor='#0D1117',
        plot_bgcolor='#16202E',
        font={'color': '#E8E8E8'},
        height=400,
        hovermode='closest',
        showlegend=False
    )
    
    return fig


def create_shap_force_plot(force_data: dict) -> go.Figure:
    """Create SHAP force plot"""
    
    features = force_data['features']
    shap_values = force_data['shap_values']
    
    # Calculate cumulative contribution
    cumulative = [force_data['base_value']]
    for sv in shap_values:
        cumulative.append(cumulative[-1] + sv)
    
    colors = ['#00FF41' if sv > 0 else '#FF1744' for sv in shap_values]
    
    fig = go.Figure(data=[
        go.Bar(
            x=shap_values,
            y=features,
            orientation='h',
            marker=dict(color=colors),
            text=[f'{sv:.3f}' for sv in shap_values],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>SHAP: %{x:.4f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=f"Base Value: {force_data['base_value']:.3f} → Prediction: {cumulative[-1]:.3f}",
        xaxis_title='SHAP Value',
        yaxis_title='Feature',
        paper_bgcolor='#0D1117',
        plot_bgcolor='#16202E',
        font={'color': '#E8E8E8'},
        height=400,
        showlegend=False,
        margin=dict(l=200)
    )
    
    return fig


def create_waterfall_chart(waterfall_data: dict) -> go.Figure:
    """Create waterfall chart for feature contributions"""
    
    n = len(waterfall_data['Feature'])
    measure = ['relative'] * (n - 2) + ['total', 'total']
    
    fig = go.Figure(go.Waterfall(
        name="Contributions",
        orientation="h",
        y=waterfall_data['Feature'],
        x=waterfall_data['Value'],
        measure=measure,
        text=[f'{v:.3f}' for v in waterfall_data['Value']],
        textposition='outside',
        connector={"line": {"color": "#FFB300"}},
        increasing={"marker": {"color": "#00FF41"}},
        decreasing={"marker": {"color": "#FF1744"}},
        totals={"marker": {"color": "#00CED1"}},
        hovertemplate='<b>%{y}</b><br>Value: %{x:.4f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=None,
        xaxis_title='Contribution Value',
        yaxis_title='Feature',
        paper_bgcolor='#0D1117',
        plot_bgcolor='#16202E',
        font={'color': '#E8E8E8'},
        height=500,
        margin=dict(l=200)
    )
    
    return fig


def create_feature_impact_chart(feature_list: list) -> go.Figure:
    """Create feature impact bar chart"""
    
    # Generate random impact scores
    impact_scores = np.abs(np.random.normal(0.2, 0.1, len(feature_list[:7])))
    impact_scores = impact_scores / impact_scores.sum()  # Normalize
    
    fig = go.Figure(data=[go.Bar(
        x=[f'{score:.1%}' for score in impact_scores],
        y=feature_list[:7],
        orientation='h',
        marker=dict(
            color=impact_scores,
            colorscale='Viridis',
            showscale=True
        ),
        hovertemplate='<b>%{y}</b><br>Impact: %{x}<extra></extra>'
    )])
    
    fig.update_layout(
        title=None,
        xaxis_title='Relative Impact (%)',
        yaxis_title=None,
        paper_bgcolor='#0D1117',
        plot_bgcolor='#16202E',
        font={'color': '#E8E8E8'},
        height=300,
        showlegend=False,
        margin=dict(l=200)
    )
    
    fig.update_yaxes(autorange="reversed")
    
    return fig


def create_lime_explanation(lime_data: dict) -> go.Figure:
    """Create LIME explanation chart"""
    
    features = lime_data['features']
    weights = lime_data['weights']
    
    fig = go.Figure(data=[go.Bar(
        x=weights,
        y=features,
        orientation='h',
        marker=dict(
            color=weights,
            colorscale='Plasma'
        ),
        text=[f'{w:.2%}' for w in weights],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Weight: %{x:.2%}<extra></extra>'
    )])
    
    fig.update_layout(
        title=None,
        xaxis_title='Feature Weight (Local Model)',
        yaxis_title='Feature',
        paper_bgcolor='#0D1117',
        plot_bgcolor='#16202E',
        font={'color': '#E8E8E8'},
        height=300,
        showlegend=False,
        margin=dict(l=200)
    )
    
    fig.update_yaxes(autorange="reversed")
    
    return fig