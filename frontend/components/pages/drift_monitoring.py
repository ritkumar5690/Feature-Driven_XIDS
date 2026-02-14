"""
XIDS Data Drift Monitoring Page
Monitor feature distribution changes and model drift
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


def render_drift_monitoring(api_url: str):
    """
    Render Data Drift Monitoring page
    
    Args:
        api_url: Base URL of the backend API
    """
    st.markdown("# 📉 Data Drift Monitoring")
    st.markdown("**Enterprise-level monitoring: Detect feature distribution changes and model drift**")
    
    # Generate sample drift data
    drift_data = generate_drift_data()
    
    # Drift Summary Metrics
    st.markdown("## 📊 Drift Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🚨 Critical Drifts",
            value=drift_data['critical_drift_count'],
            delta=f"+{drift_data['critical_change']}"
        )
    
    with col2:
        st.metric(
            label="⚠️ Warning Drifts",
            value=drift_data['warning_drift_count'],
            delta=f"+{drift_data['warning_change']}"
        )
    
    with col3:
        st.metric(
            label="✅ Stable Features",
            value=drift_data['stable_count'],
            delta=f"-{drift_data['stable_change']}"
        )
    
    with col4:
        st.metric(
            label="🔄 Avg Drift Score",
            value=f"{drift_data['avg_drift_score']:.2f}",
            delta=f"+{drift_data['drift_score_change']:.2f}"
        )
    
    st.divider()
    
    # Feature Drift Overview
    st.markdown("## 🎯 Feature Drift Scores")
    
    drift_fig = create_drift_score_chart(drift_data['feature_drifts'])
    st.plotly_chart(drift_fig, width='stretch')
    
    st.divider()
    
    # Distribution Comparison
    st.markdown("## 📈 Distribution Comparison (Reference vs Current)")
    
    selected_feature = st.selectbox(
        "Select Feature for Distribution Analysis",
        drift_data['feature_names'],
        key="drift_feature"
    )
    
    dist_fig = create_distribution_comparison(
        drift_data['distributions'][selected_feature]
    )
    st.plotly_chart(dist_fig, width='stretch')
    
    st.divider()
    
    # Statistical Drift Tests
    st.markdown("## 🔬 Statistical Drift Tests (Kolmogorov-Smirnov)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Top Drifting Features")
        st.dataframe(
            drift_data['ks_test_results'],
            width='stretch',
            hide_index=True,
            column_config={
                "Feature": st.column_config.TextColumn(width="medium"),
                "KS Statistic": st.column_config.NumberColumn(width="small", format="%.4f"),
                "P-Value": st.column_config.NumberColumn(width="small", format="%.4f"),
                "Status": st.column_config.TextColumn(width="small"),
            }
        )
    
    with col2:
        st.markdown("### Interpretation")
        st.info("""
        **Kolmogorov-Smirnov Test:**
        - Compares reference vs current distribution
        - KS Statistic: Measures maximum difference (0-1)
        - P-Value: Statistical significance
        
        **Decision Rules:**
        - KS > 0.3: Critical drift 🚨
        - KS 0.15-0.3: Warning drift ⚠️
        - KS < 0.15: Stable ✅
        """)
    
    st.divider()
    
    # Drift Timeline
    st.markdown("## 📊 Drift Score Timeline")
    
    timeline_fig = create_drift_timeline(drift_data['drift_timeline'])
    st.plotly_chart(timeline_fig, width='stretch')
    
    st.divider()
    
    # Model Performance Impact
    st.markdown("## ⚡ Model Performance Impact Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Performance vs Drift")
        perf_fig = create_performance_vs_drift(drift_data['perf_drift_correlation'])
        st.plotly_chart(perf_fig, width='stretch')
    
    with col2:
        st.markdown("### Drift Alerts")
        st.warning("""
        ⚠️ **Recent Drift Alerts:**
        
        **Critical:**
        - Flow Duration (KS: 0.38) - Consider retraining
        - Total Fwd Packets (KS: 0.35)
        
        **Warning:**
        - Flow Bytes/s (KS: 0.22) - Monitor
        - Fwd IAT Mean (KS: 0.19)
        
        **Recommendation:**
        Retrain model if average drift exceeds 0.25
        """)
    
    st.divider()
    
    # Drift Heatmap by Time
    st.markdown("## 🔥 Drift Heatmap (Features Over Time)")
    
    heatmap_fig = create_drift_heatmap(drift_data['drift_heatmap'])
    st.plotly_chart(heatmap_fig, width='stretch')


def generate_drift_data() -> dict:
    """Generate sample drift data"""
    
    feature_names = [
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
    
    # Feature drift scores
    feature_drifts = [
        {'Feature': fn, 'Drift Score': np.random.uniform(0, 0.5), 'Status': 'Stable' if np.random.rand() > 0.3 else 'Drifting'}
        for fn in feature_names
    ]
    feature_drifts.sort(key=lambda x: x['Drift Score'], reverse=True)
    
    # KS test results
    ks_results = pd.DataFrame({
        'Feature': feature_names[:7],
        'KS Statistic': [0.38, 0.35, 0.22, 0.19, 0.16, 0.14, 0.12],
        'P-Value': [0.0001, 0.0002, 0.015, 0.032, 0.058, 0.092, 0.124],
        'Status': ['Critical', 'Critical', 'Warning', 'Warning', 'Stable', 'Stable', 'Stable']
    })
    
    # Distribution data
    distributions = {}
    for feature in feature_names:
        ref_dist = np.random.normal(1000, 300, 1000)
        curr_dist = np.random.normal(1200, 350, 1000)
        distributions[feature] = {
            'reference': ref_dist,
            'current': curr_dist
        }
    
    # Drift timeline
    hours = 24
    drift_timeline = []
    for i in range(hours):
        drift_timeline.append({
            'time': f"{i:02d}:00",
            'avg_drift': 0.15 + 0.05 * np.sin(i/6) + np.random.uniform(-0.02, 0.02)
        })
    
    # Performance vs drift correlation
    perf_drift = {
        'features': feature_names[:7],
        'drift_scores': [0.38, 0.35, 0.22, 0.19, 0.16, 0.14, 0.12],
        'performance_impact': [-0.08, -0.07, -0.03, -0.02, 0.00, 0.01, 0.02]
    }
    
    # Drift heatmap
    drift_heatmap_data = np.random.uniform(0.05, 0.4, (10, 10))
    
    return {
        'critical_drift_count': 2,
        'critical_change': 1,
        'warning_drift_count': 2,
        'warning_change': 0,
        'stable_count': 6,
        'stable_change': 1,
        'avg_drift_score': 0.22,
        'drift_score_change': 0.05,
        'feature_names': feature_names,
        'feature_drifts': feature_drifts,
        'ks_test_results': ks_results,
        'distributions': distributions,
        'drift_timeline': drift_timeline,
        'perf_drift_correlation': perf_drift,
        'drift_heatmap': drift_heatmap_data
    }


def create_drift_score_chart(feature_drifts: list) -> go.Figure:
    """Create feature drift scores chart"""
    
    df = pd.DataFrame(feature_drifts).sort_values('Drift Score', ascending=True)
    
    colors = ['#FF1744' if status == 'Drifting' else '#00FF41' for status in df['Status']]
    
    fig = go.Figure(data=[go.Bar(
        x=df['Drift Score'],
        y=df['Feature'],
        orientation='h',
        marker=dict(color=colors),
        text=[f'{score:.2f}' for score in df['Drift Score']],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Drift Score: %{x:.3f}<extra></extra>'
    )])
    
    fig.update_layout(
        title=None,
        xaxis_title='Drift Score',
        yaxis_title=None,
        paper_bgcolor='#0D1117',
        plot_bgcolor='#16202E',
        font={'color': '#E8E8E8'},
        height=450,
        margin=dict(l=200),
        showlegend=False
    )
    
    return fig


def create_distribution_comparison(dist_data: dict) -> go.Figure:
    """Create reference vs current distribution comparison"""
    
    fig = go.Figure()
    
    # Reference distribution
    fig.add_trace(go.Histogram(
        x=dist_data['reference'],
        name='Reference Distribution',
        opacity=0.6,
        marker=dict(color='#00CED1'),
        nbinsx=40,
        hovertemplate='Reference<br>Range: %{x}<br>Count: %{y}<extra></extra>'
    ))
    
    # Current distribution
    fig.add_trace(go.Histogram(
        x=dist_data['current'],
        name='Current Distribution',
        opacity=0.6,
        marker=dict(color='#FF1744'),
        nbinsx=40,
        hovertemplate='Current<br>Range: %{x}<br>Count: %{y}<extra></extra>'
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


def create_drift_timeline(timeline_data: list) -> go.Figure:
    """Create drift score timeline"""
    
    df = pd.DataFrame(timeline_data)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['time'],
        y=df['avg_drift'],
        fill='tozeroy',
        name='Average Drift Score',
        line=dict(color='#FFB300', width=3),
        fillcolor='rgba(255, 179, 0, 0.2)',
        hovertemplate='<b>%{x}</b><br>Drift: %{y:.3f}<extra></extra>'
    ))
    
    # Add warning threshold
    fig.add_hline(
        y=0.25,
        line_dash="dash",
        line_color="#FF1744",
        annotation_text="Retraining Threshold",
        annotation_position="right"
    )
    
    fig.update_layout(
        title=None,
        xaxis_title='Time (Hours)',
        yaxis_title='Average Drift Score',
        paper_bgcolor='#0D1117',
        plot_bgcolor='#16202E',
        font={'color': '#E8E8E8'},
        height=400,
        showlegend=False
    )
    
    return fig


def create_performance_vs_drift(perf_data: dict) -> go.Figure:
    """Create scatter plot of performance vs drift"""
    
    fig = go.Figure(data=[go.Scatter(
        x=perf_data['drift_scores'],
        y=perf_data['performance_impact'],
        mode='markers+text',
        marker=dict(
            size=12,
            color=perf_data['drift_scores'],
            colorscale='Reds',
            showscale=True,
            colorbar=dict(title="Drift Score")
        ),
        text=perf_data['features'],
        textposition="top center",
        hovertemplate='<b>%{text}</b><br>Drift: %{x:.3f}<br>Perf Impact: %{y:.3f}<extra></extra>'
    )])
    
    fig.update_layout(
        title=None,
        xaxis_title='Drift Score',
        yaxis_title='Performance Impact on F1-Score',
        paper_bgcolor='#0D1117',
        plot_bgcolor='#16202E',
        font={'color': '#E8E8E8'},
        height=400,
        hovermode='closest'
    )
    
    return fig


def create_drift_heatmap(drift_matrix: np.ndarray) -> go.Figure:
    """Create drift heatmap over time"""
    
    feature_names = [f'Feature {i+1}' for i in range(drift_matrix.shape[0])]
    time_steps = [f'{i:02d}:00' for i in range(drift_matrix.shape[1])]
    
    fig = go.Figure(data=go.Heatmap(
        z=drift_matrix,
        x=time_steps,
        y=feature_names,
        colorscale='YlOrRd',
        colorbar=dict(title="Drift Score"),
        hovertemplate='%{y}<br>%{x}<br>Drift: %{z:.3f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=None,
        xaxis_title='Time',
        yaxis_title='Features',
        paper_bgcolor='#0D1117',
        font={'color': '#E8E8E8'},
        height=500,
    )
    
    return fig