"""
XIDS Risk Assessment Page
Translate ML output to security meaning and risk scoring
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


def render_risk_assessment(api_url: str):
    """
    Render Risk Assessment page with security-focused analysis
    
    Args:
        api_url: Base URL of the backend API
    """
    st.markdown("# 🎯 Risk Assessment")
    st.markdown("**Translate ML output to security meaning: Risk scoring and threat classification**")
    
    # Generate sample risk data
    risk_data = generate_risk_data()
    
    # Risk Score Summary
    st.markdown("## 🎯 Network Risk Score")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        risk_score = risk_data['overall_risk_score']
        st.metric(
            label="📊 Overall Risk Score",
            value=f"{risk_score:.1f}/100",
            delta=f"+{risk_data['score_change']:.1f}",
            delta_color="off"
        )
    
    with col2:
        st.metric(
            label="🔴 Critical Threats",
            value=risk_data['critical_count'],
            delta=f"+{risk_data['critical_change']}"
        )
    
    with col3:
        st.metric(
            label="🟠 High Risk",
            value=risk_data['high_count'],
            delta=f"+{risk_data['high_change']}"
        )
    
    with col4:
        st.metric(
            label="🟡 Medium Risk",
            value=risk_data['medium_count'],
            delta=f"+{risk_data['medium_change']}"
        )
    
    st.divider()
    
    # Risk Gauge
    st.markdown("## Risk Level Indicator")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        gauge_fig = create_risk_gauge(risk_data['overall_risk_score'])
        st.plotly_chart(gauge_fig, width='stretch')
    
    with col2:
        st.markdown("### Risk Interpretation")
        risk_level = determine_risk_level(risk_data['overall_risk_score'])
        
        if risk_level == "CRITICAL":
            color = "🔴"
            desc = "Immediate action required. Multiple high-severity threats detected."
        elif risk_level == "HIGH":
            color = "🟠"
            desc = "Significant threats present. Urgent investigation needed."
        elif risk_level == "MEDIUM":
            color = "🟡"
            desc = "Moderate threats detected. Monitor closely and respond."
        else:
            color = "🟢"
            desc = "Low threat level. Normal operations. Routine monitoring."
        
        st.info(f"{color} **{risk_level}** Risk\n\n{desc}")
    
    st.divider()
    
    # Top Risky IPs/Services
    st.markdown("## 🚨 High-Risk Sources Detection")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Riskiest Source IPs")
        st.dataframe(
            risk_data['risky_ips'],
            width='stretch',
            hide_index=True,
            column_config={
                "IP Address": st.column_config.TextColumn(width="medium"),
                "Risk Score": st.column_config.ProgressColumn(min_value=0, max_value=100, width="small"),
                "Attack Count": st.column_config.NumberColumn(width="small"),
                "Status": st.column_config.TextColumn(width="small"),
            }
        )
    
    with col2:
        st.markdown("### Riskiest Destination Services")
        st.dataframe(
            risk_data['risky_services'],
            width='stretch',
            hide_index=True,
            column_config={
                "Service/Port": st.column_config.TextColumn(width="medium"),
                "Risk Score": st.column_config.ProgressColumn(min_value=0, max_value=100, width="small"),
                "Attack Count": st.column_config.NumberColumn(width="small"),
                "Status": st.column_config.TextColumn(width="small"),
            }
        )
    
    st.divider()
    
    # Attack Severity Classification
    st.markdown("## 🎯 Attack Severity Classification")
    
    severity_fig = create_severity_heatmap(risk_data['severity_matrix'])
    st.plotly_chart(severity_fig, width='stretch')
    
    st.markdown("""
    **Severity Scoring Logic:**
    - CRITICAL: Immediate exploitation risk, active compromise indicators
    - HIGH: Significant impact potential, targeted attacks
    - MEDIUM: Moderate damage potential, opportunistic attacks
    - LOW: Limited impact, reconnaissance or noise
    """)
    
    st.divider()
    
    # Risk Trend Analysis
    st.markdown("## 📊 Risk Trend Analysis (24h)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        trend_fig = create_risk_trend_chart(risk_data['risk_timeline'])
        st.plotly_chart(trend_fig, width='stretch')
    
    with col2:
        st.markdown("### Risk Statistics")
        st.metric(
            label="📈 Peak Risk Score",
            value=f"{risk_data['peak_risk']:.1f}",
            delta="in last 24h"
        )
        
        st.metric(
            label="📊 Average Risk Score",
            value=f"{risk_data['avg_risk']:.1f}",
            delta="24h average"
        )
        
        st.metric(
            label="⏱️ Time Above Threshold",
            value=f"{risk_data['time_above_threshold']}h",
            delta="(>60 threshold)"
        )
    
    st.divider()
    
    # Risk Remediation Recommendations
    st.markdown("## 💡 Risk Remediation Recommendations")
    
    recommendations = risk_data['recommendations']
    
    for i, rec in enumerate(recommendations, 1):
        severity = rec['severity']
        if severity == 'CRITICAL':
            icon = '🔴'
        elif severity == 'HIGH':
            icon = '🟠'
        else:
            icon = '🟡'
        
        with st.expander(f"{icon} {rec['title']}", expanded=(i <= 2)):
            st.markdown(f"**Priority:** {severity}")
            st.markdown(f"**Action:** {rec['action']}")
            st.markdown(f"**Impact:** {rec['impact']}")
    
    st.divider()
    
    # Incident Response Guide
    st.markdown("## 📋 Incident Response Guide")
    
    response_col = st.selectbox(
        "Select Risk Level for Response Instructions",
        ["CRITICAL", "HIGH", "MEDIUM", "LOW"],
        key="irg_level"
    )
    
    irg_data = get_incident_response_guide(response_col)
    
    st.markdown(f"### Response for {response_col} Risk Threats")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Immediate Actions (0-15 min):**")
        for action in irg_data['immediate']:
            st.markdown(f"• {action}")
    
    with col2:
        st.markdown("**Follow-up Actions (15 min - 2h):**")
        for action in irg_data['followup']:
            st.markdown(f"• {action}")


def generate_risk_data() -> dict:
    """Generate sample risk assessment data"""
    
    # Risk timeline
    hours = 24
    risk_timeline = []
    for i in range(hours):
        risk_score = 45 + 25 * np.sin(i/6) + np.random.uniform(-5, 10)
        risk_timeline.append({'hour': i, 'risk_score': max(0, min(100, risk_score))})
    
    # Risky IPs
    risky_ips = pd.DataFrame({
        'IP Address': ['192.168.1.100', '10.0.0.50', '203.0.113.45', '172.16.0.5', '198.51.100.1'],
        'Risk Score': [92, 78, 65, 58, 45],
        'Attack Count': [24, 18, 12, 9, 6],
        'Status': ['CRITICAL', 'HIGH', 'MEDIUM', 'MEDIUM', 'LOW']
    })
    
    # Risky services
    risky_services = pd.DataFrame({
        'Service/Port': ['Port 80 (HTTP)', 'Port 443 (HTTPS)', 'Port 22 (SSH)', 'Port 3389 (RDP)', 'Port 25 (SMTP)'],
        'Risk Score': [88, 72, 68, 55, 42],
        'Attack Count': [156, 98, 87, 45, 28],
        'Status': ['CRITICAL', 'HIGH', 'HIGH', 'MEDIUM', 'LOW']
    })
    
    # Severity matrix (attack type vs impact)
    severity_matrix = np.random.uniform(0.3, 1.0, (7, 4))  # 7 attack types, 4 severity levels
    
    # Recommendations
    recommendations = [
        {
            'severity': 'CRITICAL',
            'title': 'Block Malicious IPs Immediately',
            'action': 'Implement firewall rules to block 192.168.1.100 and 10.0.0.50',
            'impact': 'Reduce attack surface by ~40%'
        },
        {
            'severity': 'CRITICAL',
            'title': 'Isolate Compromised Systems',
            'action': 'Move high-risk systems to isolated network segment',
            'impact': 'Prevent lateral movement and containment of breach'
        },
        {
            'severity': 'HIGH',
            'title': 'Enable Enhanced Logging',
            'action': 'Increase verbosity of security logs for Port 22/80/443',
            'impact': 'Better forensics and attack pattern detection'
        },
        {
            'severity': 'HIGH',
            'title': 'Patch Vulnerable Services',
            'action': 'Apply security patches for web and SSH services',
            'impact': 'Close exploitation vectors'
        }
    ]
    
    return {
        'overall_risk_score': 67.3,
        'score_change': 3.5,
        'critical_count': 2,
        'critical_change': 1,
        'high_count': 3,
        'high_change': 0,
        'medium_count': 5,
        'medium_change': -1,
        'risky_ips': risky_ips,
        'risky_services': risky_services,
        'severity_matrix': severity_matrix,
        'risk_timeline': risk_timeline,
        'peak_risk': 78.5,
        'avg_risk': 55.2,
        'time_above_threshold': 6,
        'recommendations': recommendations
    }


def determine_risk_level(risk_score: float) -> str:
    """Determine risk level from score"""
    if risk_score >= 80:
        return "CRITICAL"
    elif risk_score >= 60:
        return "HIGH"
    elif risk_score >= 40:
        return "MEDIUM"
    else:
        return "LOW"


def create_risk_gauge(risk_score: float) -> go.Figure:
    """Create risk gauge chart"""
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=risk_score,
        title={'text': "Network Risk Score"},
        delta={'reference': 50},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#FF1744"},
            'steps': [
                {'range': [0, 40], 'color': "#1A1F2E"},
                {'range': [40, 60], 'color': "#2C2C2C"},
                {'range': [60, 80], 'color': "#2A1A1A"},
                {'range': [80, 100], 'color': "#3A0000"}
            ],
            'threshold': {
                'line': {'color': "#00FF41", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig.update_layout(
        height=400,
        paper_bgcolor="#0D1117",
        font={'color': "#E8E8E8"}
    )
    
    return fig


def create_severity_heatmap(severity_matrix: np.ndarray) -> go.Figure:
    """Create attack severity heatmap"""
    
    attack_types = ['DoS', 'DDoS', 'PortScan', 'Bot', 'Brute Force', 'Web Attack', 'Data Exfil']
    severity_levels = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
    
    fig = go.Figure(data=go.Heatmap(
        z=severity_matrix,
        x=severity_levels,
        y=attack_types,
        colorscale='Reds',
        text=np.round(severity_matrix, 2),
        texttemplate='%{text:.2f}',
        textfont={"size": 10},
        colorbar=dict(title="Severity Score"),
        hovertemplate='%{y} vs %{x}<br>Score: %{z:.3f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=None,
        xaxis_title='Severity Classification',
        yaxis_title='Attack Type',
        paper_bgcolor='#0D1117',
        font={'color': '#E8E8E8'},
        height=450,
    )
    
    return fig


def create_risk_trend_chart(timeline_data: list) -> go.Figure:
    """Create risk score trend chart"""
    
    df = pd.DataFrame(timeline_data)
    
    fig = go.Figure()
    
    # Risk area chart
    fig.add_trace(go.Scatter(
        x=df['hour'],
        y=df['risk_score'],
        fill='tozeroy',
        name='Risk Score',
        line=dict(color='#FF1744', width=3),
        fillcolor='rgba(255, 23, 68, 0.2)',
        hovertemplate='Hour %{x}<br>Risk: %{y:.1f}<extra></extra>'
    ))
    
    # Add threshold line
    fig.add_hline(
        y=60,
        line_dash="dash",
        line_color="#FFB300",
        annotation_text="High Risk Threshold (60)",
        annotation_position="right"
    )
    
    fig.update_layout(
        title=None,
        xaxis_title='Hour of Day',
        yaxis_title='Risk Score',
        paper_bgcolor='#0D1117',
        plot_bgcolor='#16202E',
        font={'color': '#E8E8E8'},
        height=400,
        showlegend=False
    )
    
    return fig


def get_incident_response_guide(risk_level: str) -> dict:
    """Get incident response guide for risk level"""
    
    guides = {
        'CRITICAL': {
            'immediate': [
                'Activate incident response team',
                'Isolate affected systems from network',
                'Preserve forensic evidence (memory, logs)',
                'Contact security leadership',
                'Block identified malicious IPs',
                'Implement emergency firewall rules'
            ],
            'followup': [
                'Conduct threat hunt across network',
                'Review all authentication logs (24h)',
                'Identify lateral movement indicators',
                'Patch or disable vulnerable services',
                'Reset credentials for affected accounts',
                'Deploy additional monitoring sensors',
                'Prepare incident report and timeline'
            ]
        },
        'HIGH': {
            'immediate': [
                'Alert security team',
                'Monitor for escalation',
                'Begin initial analysis',
                'Document findings',
                'Review related alerts'
            ],
            'followup': [
                'Conduct network scans',
                'Review vulnerable services',
                'Check for compromise indicators',
                'Implement protective measures',
                'Schedule follow-up analysis'
            ]
        },
        'MEDIUM': {
            'immediate': [
                'Log incident details',
                'Monitor related activity',
                'Check attack source'
            ],
            'followup': [
                'Analyze attack patterns',
                'Review security controls',
                'Update threat intelligence',
                'Plan monitoring improvements'
            ]
        },
        'LOW': {
            'immediate': [
                'Record incident in system',
                'Continue normal monitoring'
            ],
            'followup': [
                'Review trends weekly',
                'Update baseline knowledge'
            ]
        }
    }
    
    return guides.get(risk_level, guides['LOW'])