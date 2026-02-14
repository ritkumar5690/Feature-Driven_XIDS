"""
XIDS SOC Dashboard Page
Executive-level monitoring and security overview
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests


def render_soc_dashboard(api_url: str):
    """
    Render the SOC Dashboard with executive-level metrics
    
    Args:
        api_url: Base URL of the backend API
    """
    st.markdown("# 📊 SOC Dashboard")
    st.markdown("**Executive-level security monitoring and threat overview**")
    
    # Generate sample data (in production, fetch from backend)
    metrics_data = generate_sample_metrics()
    
    # Top-level KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🛡️ Security Score",
            value=f"{metrics_data['security_score']:.1f}/100",
            delta=f"+{metrics_data['score_change']:.1f}%",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            label="📊 Traffic Analyzed",
            value=f"{metrics_data['total_traffic']:,}",
            delta=f"+{metrics_data['traffic_change']:,}",
        )
    
    with col3:
        st.metric(
            label="⚠️ Threats Detected",
            value=f"{metrics_data['threats_detected']:,}",
            delta=f"+{metrics_data['threat_change']:.1f}%",
            delta_color="off"
        )
    
    with col4:
        risk_color = "🔴" if metrics_data['risk_level'] == "CRITICAL" else "🟡" if metrics_data['risk_level'] == "HIGH" else "🟢"
        st.metric(
            label="🎯 Risk Level",
            value=f"{risk_color} {metrics_data['risk_level']}",
            delta=None
        )
    
    st.divider()
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Threat Trend (24h)")
        threat_chart = create_threat_trend_chart(metrics_data['threat_timeline'])
        st.plotly_chart(threat_chart, width='stretch')
    
    with col2:
        st.markdown("### 🎯 Attack Distribution")
        attack_chart = create_attack_distribution_chart(metrics_data['attack_distribution'])
        st.plotly_chart(attack_chart, width='stretch')
    
    st.divider()
    
    # Top attack categories
    st.markdown("### 🔴 Top Attack Categories")
    
    col1, col2 = st.columns(2)
    
    with col1:
        attack_table = create_attack_table(metrics_data['top_attacks'])
        st.dataframe(
            attack_table,
            width='stretch',
            hide_index=True,
            column_config={
                "Attack Type": st.column_config.TextColumn(width="medium"),
                "Count": st.column_config.NumberColumn(width="small"),
                "% of Total": st.column_config.ProgressColumn(min_value=0, max_value=100, width="small"),
            }
        )
    
    with col2:
        st.markdown("### ⏰ Detection Timeline")
        st.info("""
        **Latest Detections (Last 30 min)**
        
        • 14:32:15 - DDoS Attack (192.168.1.100) - HIGH
        • 14:28:42 - Port Scan (10.0.0.50) - MEDIUM
        • 14:21:08 - Brute Force (172.16.0.5) - MEDIUM
        • 14:15:33 - DoS Attack (203.0.113.45) - HIGH
        • 14:08:19 - Web Attack (198.51.100.1) - LOW
        """)
    
    st.divider()
    
    # Real-time stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📊 Detection Rate")
        detection_rate = metrics_data['detection_rate']
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=detection_rate,
            title={'text': "Attack Detection Rate"},
            delta={'reference': detection_rate - 2},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#00FF41"},
                'steps': [
                    {'range': [0, 50], 'color': "#1A1F2E"},
                    {'range': [50, 100], 'color': "#16202E"}
                ],
                'threshold': {
                    'line': {'color': "#FF1744", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig.update_layout(
            height=300,
            paper_bgcolor="#0D1117",
            font={'color': "#E8E8E8"}
        )
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.markdown("### 🎯 False Positive Rate")
        fpr = metrics_data['false_positive_rate']
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=fpr,
            title={'text': "False Positive Rate"},
            delta={'reference': fpr + 0.5, 'suffix': "%"},
            gauge={
                'axis': {'range': [0, 10]},
                'bar': {'color': "#00CED1"},
                'steps': [
                    {'range': [0, 5], 'color': "#1A1F2E"},
                    {'range': [5, 10], 'color': "#16202E"}
                ],
                'threshold': {
                    'line': {'color': "#FF1744", 'width': 4},
                    'thickness': 0.75,
                    'value': 8
                }
            }
        ))
        fig.update_layout(
            height=300,
            paper_bgcolor="#0D1117",
            font={'color': "#E8E8E8"}
        )
        st.plotly_chart(fig, width='stretch')
    
    with col3:
        st.markdown("### ⚡ Avg. Response Time")
        response_time = metrics_data['avg_response_time']
        fig = go.Figure(go.Indicator(
            mode="number+delta",
            value=response_time,
            title={'text': "Response Time (ms)"},
            delta={'reference': response_time + 10},
            number={'suffix': " ms"},
            domain={'x': [0, 1], 'y': [0, 1]}
        ))
        fig.update_layout(
            height=300,
            paper_bgcolor="#0D1117",
            font={'color': "#E8E8E8"}
        )
        st.plotly_chart(fig, width='stretch')


def generate_sample_metrics() -> dict:
    """Generate sample metrics data"""
    
    # Time-based data for threat timeline
    hours = 24
    threat_timeline = []
    for i in range(hours):
        hour = datetime.now() - timedelta(hours=hours-i)
        count = int(30 + 20 * np.sin(i/4) + np.random.randint(-5, 15))
        threat_timeline.append({
            'time': hour.strftime("%H:%M"),
            'threats': max(0, count)
        })
    
    # Attack distribution
    attack_distribution = {
        'BENIGN': 7500,
        'DoS': 450,
        'DDoS': 650,
        'PortScan': 280,
        'Bot': 120,
        'Brute Force': 95,
        'Web Attack': 110
    }
    
    # Top attacks
    top_attacks = [
        {'Attack Type': 'DDoS', 'Count': 650, 'Percentage': 45.2},
        {'Attack Type': 'DoS', 'Count': 450, 'Percentage': 31.3},
        {'Attack Type': 'PortScan', 'Count': 280, 'Percentage': 19.4},
        {'Attack Type': 'Bot', 'Count': 120, 'Percentage': 8.3},
        {'Attack Type': 'Web Attack', 'Count': 110, 'Percentage': 7.6},
        {'Attack Type': 'Brute Force', 'Count': 95, 'Percentage': 6.6},
    ]
    
    return {
        'security_score': 78.5,
        'score_change': 3.2,
        'total_traffic': 9205,
        'traffic_change': 345,
        'threats_detected': 1705,
        'threat_change': 12.5,
        'risk_level': 'MEDIUM',
        'threat_timeline': threat_timeline,
        'attack_distribution': attack_distribution,
        'top_attacks': top_attacks,
        'detection_rate': 94.2,
        'false_positive_rate': 2.1,
        'avg_response_time': 48.5
    }


def create_threat_trend_chart(threat_timeline: list) -> go.Figure:
    """Create threat trend line chart"""
    df = pd.DataFrame(threat_timeline)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['time'],
        y=df['threats'],
        fill='tozeroy',
        name='Threats Detected',
        line=dict(color='#FF1744', width=3),
        fillcolor='rgba(255, 23, 68, 0.2)',
        hovertemplate='<b>%{x}</b><br>Threats: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title=None,
        xaxis_title='Time',
        yaxis_title='Number of Threats',
        hovermode='x unified',
        paper_bgcolor='#0D1117',
        plot_bgcolor='#16202E',
        font={'color': '#E8E8E8'},
        height=400,
        showlegend=False
    )
    
    return fig


def create_attack_distribution_chart(attack_dist: dict) -> go.Figure:
    """Create attack distribution pie chart"""
    
    fig = go.Figure(data=[go.Pie(
        labels=list(attack_dist.keys()),
        values=list(attack_dist.values()),
        hole=0.4,
        marker=dict(
            colors=['#00FF41', '#FF1744', '#FFB300', '#00CED1', '#9C27B0', '#4CAF50', '#F44336'],
            line=dict(color='#0D1117', width=2)
        ),
        textposition='inside',
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title=None,
        paper_bgcolor='#0D1117',
        font={'color': '#E8E8E8'},
        height=400,
        showlegend=True
    )
    
    return fig


def create_attack_table(top_attacks: list) -> pd.DataFrame:
    """Create attack summary table"""
    df = pd.DataFrame(top_attacks)
    df.columns = ['Attack Type', 'Count', '% of Total']
    return df