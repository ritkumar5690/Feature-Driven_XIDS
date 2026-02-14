"""
XIDS Feature Importance Page
Feature-driven analysis and SHAP-based insights
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


def render_feature_importance(api_url: str):
    """
    Render Feature Importance page with feature-driven analysis
    
    Args:
        api_url: Base URL of the backend API
    """
    st.markdown("# ⭐ Feature Importance")
    st.markdown("**Feature-driven analysis: Which features drive attacks?**")
    
    # Generate sample feature importance data
    feature_data = generate_feature_importance_data()
    
    # Top features section
    st.markdown("## 🎯 Top 10 Most Important Features")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        top10_fig = create_top_features_chart(feature_data['top_features'])
        st.plotly_chart(top10_fig, width='stretch')
    
    with col2:
        st.markdown("### Feature Insights")
        st.info("""
        **Most Important Features:**
        1. **Flow Duration** - Strong attack indicator
        2. **Total Fwd Packets** - Traffic volume pattern
        3. **Total Backward Packets** - Response pattern
        4. **Flow Bytes/s** - Data rate intensity
        5. **Fwd PSH Flags** - Protocol control pattern
        
        **Interpretation:**
        Features ranked by information gain
        relative to target class.
        """)
    
    st.divider()
    
    # Feature correlation analysis
    st.markdown("## 🔗 Feature Correlation Heatmap")
    
    corr_fig = create_correlation_heatmap(feature_data['correlation_matrix'], feature_data['top_10_features'])
    st.plotly_chart(corr_fig, width='stretch')
    
    st.divider()
    
    # Feature distribution analysis
    st.markdown("## 📊 Feature Distribution Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Normal vs Attack Distribution")
        dist_fig = create_distribution_comparison(feature_data['distribution_data'])
        st.plotly_chart(dist_fig, width='stretch')
    
    with col2:
        st.markdown("### Feature Statistics")
        st.dataframe(
            feature_data['feature_stats'],
            width='stretch',
            hide_index=True,
            column_config={
                "Feature": st.column_config.TextColumn(width="medium"),
                "Mean": st.column_config.NumberColumn(width="small", format="%.2f"),
                "Std Dev": st.column_config.NumberColumn(width="small", format="%.2f"),
                "Min": st.column_config.NumberColumn(width="small", format="%.2f"),
                "Max": st.column_config.NumberColumn(width="small", format="%.2f"),
            }
        )
    
    st.divider()
    
    # Feature importance by attack type
    st.markdown("## 🎯 Feature Importance by Attack Type")
    
    attack_type = st.selectbox(
        "Select Attack Type",
        ['All Attacks', 'DoS', 'DDoS', 'PortScan', 'Bot', 'Brute Force', 'Web Attack'],
        key="feature_importance_attack"
    )
    
    attack_importance = create_attack_type_importance(
        feature_data['attack_type_importance'],
        attack_type
    )
    st.plotly_chart(attack_importance, width='stretch')
    
    st.divider()
    
    # Feature selection method comparison
    st.markdown("## 🔬 Feature Selection Methods Comparison")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🏆 K-Best Features",
            value=20,
            delta="ANOVA F-score"
        )
    
    with col2:
        st.metric(
            label="📊 Mutual Information",
            value=18,
            delta="Information gain"
        )
    
    with col3:
        st.metric(
            label="🌳 Random Forest",
            value=22,
            delta="MDI importance"
        )
    
    # Feature selection results table
    st.markdown("### Selected Features by Method")
    
    selection_methods = pd.DataFrame({
        'Feature': ['Flow Duration', 'Total Fwd Packets', 'Total Bwd Packets', 'Flow Bytes/s', 'Fwd PSH Flags'],
        'K-Best Rank': [1, 2, 3, 4, 5],
        'MI Rank': [1, 3, 2, 5, 4],
        'RF Rank': [2, 1, 3, 4, 6],
        'Consensus Rank': [1, 2, 3, 4, 5]
    })
    
    st.dataframe(
        selection_methods,
        width='stretch',
        hide_index=True
    )
    
    st.divider()
    
    # Outlier detection
    st.markdown("## 🎯 Outlier Detection in Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        outlier_fig = create_outlier_chart(feature_data['outlier_data'])
        st.plotly_chart(outlier_fig, width='stretch')
    
    with col2:
        st.markdown("### Outlier Statistics")
        st.info("""
        **Features with Outliers:**
        - Flow Duration: 2.3% outliers
        - Total Fwd Packets: 1.8% outliers
        - Flow Bytes/s: 3.1% outliers
        - Fwd IAT Mean: 1.2% outliers
        
        **Handling Strategy:**
        Outliers retained for attack detection
        as they may indicate suspicious patterns.
        """)


def generate_feature_importance_data() -> dict:
    """Generate sample feature importance data"""
    
    top_features = [
        {'Feature': 'Flow Duration', 'Importance': 0.185, 'Rank': 1},
        {'Feature': 'Total Fwd Packets', 'Importance': 0.156, 'Rank': 2},
        {'Feature': 'Total Bwd Packets', 'Importance': 0.142, 'Rank': 3},
        {'Feature': 'Flow Bytes/s', 'Importance': 0.128, 'Rank': 4},
        {'Feature': 'Fwd PSH Flags', 'Importance': 0.118, 'Rank': 5},
        {'Feature': 'Bwd PSH Flags', 'Importance': 0.105, 'Rank': 6},
        {'Feature': 'Flow Packets/s', 'Importance': 0.095, 'Rank': 7},
        {'Feature': 'Fwd IAT Mean', 'Importance': 0.082, 'Rank': 8},
        {'Feature': 'Bwd IAT Mean', 'Importance': 0.074, 'Rank': 9},
        {'Feature': 'Fwd Packet Length Mean', 'Importance': 0.068, 'Rank': 10},
    ]
    
    top_10_features = [f['Feature'] for f in top_features]
    
    # Correlation matrix (top 10 features)
    np.random.seed(42)
    n_features = len(top_10_features)
    corr_matrix = np.eye(n_features)
    for i in range(n_features):
        for j in range(i+1, n_features):
            corr_value = np.random.uniform(0.1, 0.9) if np.random.rand() > 0.5 else np.random.uniform(-0.9, -0.1)
            corr_matrix[i, j] = corr_value
            corr_matrix[j, i] = corr_value
    
    # Feature statistics
    feature_stats = pd.DataFrame({
        'Feature': top_10_features,
        'Mean': np.random.uniform(100, 10000, n_features),
        'Std Dev': np.random.uniform(50, 5000, n_features),
        'Min': np.zeros(n_features),
        'Max': np.random.uniform(50000, 100000, n_features),
    })
    
    # Distribution data (Normal vs Attack)
    distribution_data = {
        'Normal': np.random.normal(500, 200, 1000),
        'Attack': np.random.normal(2000, 800, 300)
    }
    
    # Attack type importance
    attack_importance_data = {
        'DoS': {feature: np.random.rand() for feature in top_10_features},
        'DDoS': {feature: np.random.rand() for feature in top_10_features},
        'PortScan': {feature: np.random.rand() for feature in top_10_features},
        'Bot': {feature: np.random.rand() for feature in top_10_features},
        'Brute Force': {feature: np.random.rand() for feature in top_10_features},
        'Web Attack': {feature: np.random.rand() for feature in top_10_features},
    }
    
    # Outlier data
    outlier_data = {
        'Feature': top_10_features[:5],
        'Outliers (%)': [2.3, 1.8, 3.1, 1.2, 2.5]
    }
    
    return {
        'top_features': top_features,
        'top_10_features': top_10_features,
        'correlation_matrix': corr_matrix,
        'feature_stats': feature_stats,
        'distribution_data': distribution_data,
        'attack_type_importance': attack_importance_data,
        'outlier_data': outlier_data
    }


def create_top_features_chart(top_features: list) -> go.Figure:
    """Create top features horizontal bar chart"""
    
    df = pd.DataFrame(top_features)
    
    fig = go.Figure(data=[go.Bar(
        y=df['Feature'],
        x=df['Importance'],
        orientation='h',
        marker=dict(
            color=df['Importance'],
            colorscale='Viridis',
            showscale=False
        ),
        text=df['Importance'].apply(lambda x: f'{x:.1%}'),
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Importance: %{x:.1%}<extra></extra>'
    )])
    
    fig.update_layout(
        title=None,
        xaxis_title='Importance Score',
        yaxis_title=None,
        paper_bgcolor='#0D1117',
        plot_bgcolor='#16202E',
        font={'color': '#E8E8E8'},
        height=450,
        margin=dict(l=200),
        showlegend=False
    )
    
    fig.update_yaxes(autorange="reversed")
    
    return fig


def create_correlation_heatmap(corr_matrix: np.ndarray, features: list) -> go.Figure:
    """Create correlation matrix heatmap"""
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix,
        x=features,
        y=features,
        colorscale='RdBu',
        zmid=0,
        zmin=-1,
        zmax=1,
        text=np.round(corr_matrix, 2),
        texttemplate='%{text:.2f}',
        textfont={"size": 8},
        colorbar=dict(title="Correlation"),
        hovertemplate='%{x} vs %{y}<br>Correlation: %{z:.3f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=None,
        paper_bgcolor='#0D1117',
        font={'color': '#E8E8E8'},
        height=600,
        xaxis={'side': 'bottom'},
    )
    
    return fig


def create_distribution_comparison(dist_data: dict) -> go.Figure:
    """Create distribution comparison chart"""
    
    fig = go.Figure()
    
    # Normal distribution
    fig.add_trace(go.Histogram(
        x=dist_data['Normal'],
        name='Normal Traffic',
        opacity=0.7,
        marker=dict(color='#00FF41'),
        nbinsx=40
    ))
    
    # Attack distribution
    fig.add_trace(go.Histogram(
        x=dist_data['Attack'],
        name='Attack Traffic',
        opacity=0.7,
        marker=dict(color='#FF1744'),
        nbinsx=40
    ))
    
    fig.update_layout(
        title=None,
        xaxis_title='Feature Value',
        yaxis_title='Frequency',
        barmode='overlay',
        paper_bgcolor='#0D1117',
        plot_bgcolor='#16202E',
        font={'color': '#E8E8E8'},
        height=400,
        hovermode='x unified'
    )
    
    return fig


def create_attack_type_importance(importance_data: dict, attack_type: str) -> go.Figure:
    """Create feature importance for specific attack type"""
    
    if attack_type == 'All Attacks':
        # Average across all attack types
        avg_importance = {}
        for attack in importance_data:
            for feature, score in importance_data[attack].items():
                if feature not in avg_importance:
                    avg_importance[feature] = []
                avg_importance[feature].append(score)
        
        features = list(avg_importance.keys())
        importance_scores = [np.mean(avg_importance[f]) for f in features]
    else:
        features = list(importance_data[attack_type].keys())
        importance_scores = list(importance_data[attack_type].values())
    
    # Sort by importance
    sorted_indices = np.argsort(importance_scores)[::-1][:10]
    features = [features[i] for i in sorted_indices]
    importance_scores = [importance_scores[i] for i in sorted_indices]
    
    fig = go.Figure(data=[go.Bar(
        x=importance_scores,
        y=features,
        orientation='h',
        marker=dict(
            color=importance_scores,
            colorscale='Plasma',
            showscale=True
        ),
        text=[f'{score:.2%}' for score in importance_scores],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Importance: %{x:.2%}<extra></extra>'
    )])
    
    fig.update_layout(
        title=f"Attack Type: {attack_type}",
        xaxis_title='Importance Score',
        yaxis_title=None,
        paper_bgcolor='#0D1117',
        plot_bgcolor='#16202E',
        font={'color': '#E8E8E8'},
        height=400,
        margin=dict(l=200),
    )
    
    fig.update_yaxes(autorange="reversed")
    
    return fig


def create_outlier_chart(outlier_data: dict) -> go.Figure:
    """Create outlier detection chart"""
    
    fig = go.Figure(data=[go.Bar(
        x=outlier_data['Feature'],
        y=outlier_data['Outliers (%)'],
        marker=dict(
            color=outlier_data['Outliers (%)'],
            colorscale='Reds',
            showscale=False
        ),
        text=[f"{pct:.1f}%" for pct in outlier_data['Outliers (%)']],
        textposition='outside',
        hovertemplate='%{x}<br>Outliers: %{y:.1f}%<extra></extra>'
    )])
    
    fig.update_layout(
        title=None,
        xaxis_title='Feature',
        yaxis_title='Outlier Percentage',
        paper_bgcolor='#0D1117',
        plot_bgcolor='#16202E',
        font={'color': '#E8E8E8'},
        height=400,
        showlegend=False
    )
    
    return fig