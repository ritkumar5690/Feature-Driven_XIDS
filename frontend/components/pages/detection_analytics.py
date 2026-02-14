"""
XIDS Detection Analytics Page
Model performance metrics and evaluation
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


def render_detection_analytics(api_url: str):
    """
    Render Detection Analytics page with model performance metrics
    
    Args:
        api_url: Base URL of the backend API
    """
    st.markdown("# 📈 Detection Analytics")
    st.markdown("**Model performance metrics and attack classification analysis**")
    
    # Generate sample model evaluation data
    eval_data = generate_evaluation_metrics()
    
    # Performance Metrics Section
    st.markdown("## Model Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="✅ Accuracy",
            value=f"{eval_data['accuracy']:.2%}",
            delta=f"+{eval_data['accuracy_change']:.2f}%"
        )
    
    with col2:
        st.metric(
            label="🎯 Precision",
            value=f"{eval_data['precision']:.2%}",
            delta=f"+{eval_data['precision_change']:.2f}%"
        )
    
    with col3:
        st.metric(
            label="🔍 Recall",
            value=f"{eval_data['recall']:.2%}",
            delta=f"+{eval_data['recall_change']:.2f}%"
        )
    
    with col4:
        st.metric(
            label="📊 F1-Score",
            value=f"{eval_data['f1_score']:.2%}",
            delta=f"+{eval_data['f1_change']:.2f}%"
        )
    
    st.divider()
    
    # Confusion Matrix and ROC Curve
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔲 Confusion Matrix")
        cm_fig = create_confusion_matrix(eval_data['confusion_matrix'], eval_data['classes'])
        st.plotly_chart(cm_fig, width='stretch')
    
    with col2:
        st.markdown("### 📉 ROC Curve")
        roc_fig = create_roc_curve(eval_data['roc_data'])
        st.plotly_chart(roc_fig, width='stretch')
    
    st.divider()
    
    # Per-class metrics
    st.markdown("## Per-Class Performance")
    
    class_metrics_df = create_class_metrics_table(eval_data['class_metrics'])
    
    st.dataframe(
        class_metrics_df,
        width='stretch',
        hide_index=True,
        column_config={
            "Class": st.column_config.TextColumn(width="medium"),
            "Precision": st.column_config.ProgressColumn(min_value=0, max_value=1, width="small"),
            "Recall": st.column_config.ProgressColumn(min_value=0, max_value=1, width="small"),
            "F1-Score": st.column_config.ProgressColumn(min_value=0, max_value=1, width="small"),
            "Support": st.column_config.NumberColumn(width="small"),
        }
    )
    
    st.divider()
    
    # Attack Detection Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Probability Score Distribution")
        prob_fig = create_probability_distribution(eval_data['probability_distribution'])
        st.plotly_chart(prob_fig, width='stretch')
    
    with col2:
        st.markdown("### 🔴 False Positive Analysis")
        fp_fig = create_false_positive_chart(eval_data['false_positive_by_class'])
        st.plotly_chart(fp_fig, width='stretch')
    
    st.divider()
    
    # Attack Type Distribution
    st.markdown("### 🎯 Attack Count per Type")
    
    attack_counts = create_attack_count_chart(eval_data['attack_counts'])
    st.plotly_chart(attack_counts, width='stretch')
    
    st.divider()
    
    # Detailed Statistics
    st.markdown("## Detailed Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total Samples",
            value=f"{eval_data['total_samples']:,}",
            delta="Training Set"
        )
    
    with col2:
        st.metric(
            label="True Positives",
            value=f"{eval_data['true_positives']:,}",
            delta=f"{(eval_data['true_positives']/eval_data['total_samples']):.1%} of total"
        )
    
    with col3:
        st.metric(
            label="False Positives",
            value=f"{eval_data['false_positives']:,}",
            delta=f"{(eval_data['false_positives']/eval_data['total_samples']):.1%} of total"
        )


def generate_evaluation_metrics() -> dict:
    """Generate sample evaluation metrics"""
    
    classes = ['BENIGN', 'DoS', 'DDoS', 'PortScan', 'Bot', 'Brute Force', 'Web Attack']
    
    # Confusion matrix (normalized for visualization)
    cm = np.array([
        [950, 5, 8, 12, 15, 8, 2],
        [8, 380, 5, 3, 2, 1, 1],
        [5, 8, 610, 12, 8, 5, 2],
        [10, 2, 8, 255, 3, 2, 2],
        [12, 3, 5, 2, 95, 2, 1],
        [8, 1, 4, 2, 1, 78, 1],
        [3, 2, 3, 1, 2, 1, 103]
    ])
    
    # Class metrics
    class_metrics = [
        {'Class': 'BENIGN', 'Precision': 0.94, 'Recall': 0.96, 'F1-Score': 0.95, 'Support': 1000},
        {'Class': 'DoS', 'Precision': 0.91, 'Recall': 0.94, 'F1-Score': 0.92, 'Support': 400},
        {'Class': 'DDoS', 'Precision': 0.93, 'Recall': 0.95, 'F1-Score': 0.94, 'Support': 650},
        {'Class': 'PortScan', 'Precision': 0.88, 'Recall': 0.90, 'F1-Score': 0.89, 'Support': 280},
        {'Class': 'Bot', 'Precision': 0.82, 'Recall': 0.85, 'F1-Score': 0.83, 'Support': 120},
        {'Class': 'Brute Force', 'Precision': 0.85, 'Recall': 0.87, 'F1-Score': 0.86, 'Support': 95},
        {'Class': 'Web Attack', 'Precision': 0.89, 'Recall': 0.91, 'F1-Score': 0.90, 'Support': 110},
    ]
    
    # Attack counts
    attack_counts = {
        'BENIGN': 2500,
        'DoS': 1200,
        'DDoS': 1800,
        'PortScan': 650,
        'Bot': 300,
        'Brute Force': 225,
        'Web Attack': 325
    }
    
    # ROC curve data
    fpr = np.array([0, 0.02, 0.05, 0.10, 0.15, 0.20, 0.30, 0.50, 1.0])
    tpr = np.array([0, 0.85, 0.90, 0.93, 0.94, 0.95, 0.96, 0.97, 1.0])
    
    # False positive by class
    fp_by_class = {
        'BENIGN': 8,
        'DoS': 3,
        'DDoS': 5,
        'PortScan': 4,
        'Bot': 2,
        'Brute Force': 1,
        'Web Attack': 2
    }
    
    # Probability distribution
    prob_dist = {
        'High (0.8-1.0)': 7200,
        'Medium (0.5-0.8)': 1500,
        'Low (0.2-0.5)': 280,
        'Very Low (0-0.2)': 20
    }
    
    return {
        'accuracy': 0.9420,
        'accuracy_change': 2.15,
        'precision': 0.9185,
        'precision_change': 1.82,
        'recall': 0.9310,
        'recall_change': 2.43,
        'f1_score': 0.9247,
        'f1_change': 2.08,
        'confusion_matrix': cm,
        'classes': classes,
        'class_metrics': class_metrics,
        'attack_counts': attack_counts,
        'roc_data': {'fpr': fpr, 'tpr': tpr},
        'false_positive_by_class': fp_by_class,
        'probability_distribution': prob_dist,
        'total_samples': 9000,
        'true_positives': 8478,
        'false_positives': 155
    }


def create_confusion_matrix(cm: np.ndarray, classes: list) -> go.Figure:
    """Create confusion matrix heatmap"""
    
    # Normalize confusion matrix for percentage display
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    
    fig = go.Figure(data=go.Heatmap(
        z=cm_normalized,
        x=classes,
        y=classes,
        colorscale='Blues',
        text=cm,  # Show actual counts
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Normalized<br>Count"),
        hovertemplate='Predicted: %{x}<br>Actual: %{y}<br>Count: %{text}<br>Percentage: %{z:.1%}<extra></extra>'
    ))
    
    fig.update_layout(
        title=None,
        xaxis_title='Predicted Label',
        yaxis_title='True Label',
        paper_bgcolor='#0D1117',
        font={'color': '#E8E8E8'},
        height=500,
        xaxis={'side': 'bottom'}
    )
    
    return fig


def create_roc_curve(roc_data: dict) -> go.Figure:
    """Create ROC curve"""
    
    fpr = roc_data['fpr']
    tpr = roc_data['tpr']
    
    # Calculate AUC using trapezoidal rule
    auc = np.trapezoid(tpr, fpr) if hasattr(np, 'trapezoid') else np.trapz(tpr, fpr)
    
    fig = go.Figure()
    
    # ROC curve
    fig.add_trace(go.Scatter(
        x=fpr,
        y=tpr,
        name=f'ROC Curve (AUC = {auc:.3f})',
        line=dict(color='#00FF41', width=3),
        hovertemplate='FPR: %{x:.2%}<br>TPR: %{y:.2%}<extra></extra>'
    ))
    
    # Random classifier line
    fig.add_trace(go.Scatter(
        x=[0, 1],
        y=[0, 1],
        name='Random Classifier',
        line=dict(color='#FF1744', width=2, dash='dash'),
        hovertemplate='FPR: %{x:.2%}<br>TPR: %{y:.2%}<extra></extra>'
    ))
    
    fig.update_layout(
        title=None,
        xaxis_title='False Positive Rate',
        yaxis_title='True Positive Rate',
        hovermode='closest',
        paper_bgcolor='#0D1117',
        plot_bgcolor='#16202E',
        font={'color': '#E8E8E8'},
        height=400,
    )
    
    return fig


def create_class_metrics_table(class_metrics: list) -> pd.DataFrame:
    """Create class metrics table"""
    df = pd.DataFrame(class_metrics)
    return df


def create_probability_distribution(prob_dist: dict) -> go.Figure:
    """Create probability distribution histogram"""
    
    fig = go.Figure(data=[go.Bar(
        x=list(prob_dist.keys()),
        y=list(prob_dist.values()),
        marker=dict(color='#00CED1'),
        text=list(prob_dist.values()),
        textposition='outside',
        hovertemplate='%{x}<br>Count: %{y}<extra></extra>'
    )])
    
    fig.update_layout(
        title=None,
        xaxis_title='Confidence Score Range',
        yaxis_title='Number of Predictions',
        paper_bgcolor='#0D1117',
        plot_bgcolor='#16202E',
        font={'color': '#E8E8E8'},
        height=400,
        showlegend=False
    )
    
    return fig


def create_false_positive_chart(fp_by_class: dict) -> go.Figure:
    """Create false positive analysis chart"""
    
    fig = go.Figure(data=[go.Bar(
        x=list(fp_by_class.keys()),
        y=list(fp_by_class.values()),
        marker=dict(color='#FF1744'),
        text=list(fp_by_class.values()),
        textposition='outside',
        hovertemplate='%{x}<br>False Positives: %{y}<extra></extra>'
    )])
    
    fig.update_layout(
        title=None,
        xaxis_title='Attack Type',
        yaxis_title='False Positive Count',
        paper_bgcolor='#0D1117',
        plot_bgcolor='#16202E',
        font={'color': '#E8E8E8'},
        height=400,
        showlegend=False
    )
    
    return fig


def create_attack_count_chart(attack_counts: dict) -> go.Figure:
    """Create attack count bar chart"""
    
    fig = px.bar(
        x=list(attack_counts.keys()),
        y=list(attack_counts.values()),
        labels={'x': 'Attack Type', 'y': 'Count'},
        color=list(attack_counts.values()),
        color_continuous_scale=['#00FF41', '#FFB300', '#FF1744']
    )
    
    fig.update_layout(
        title=None,
        paper_bgcolor='#0D1117',
        plot_bgcolor='#16202E',
        font={'color': '#E8E8E8'},
        height=400,
        showlegend=False
    )
    
    return fig