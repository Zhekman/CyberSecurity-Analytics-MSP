import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 1. Підключення та завантаження даних
conn = sqlite3.connect('CyberSecurity.db')

# Запити для звіту
df_mfa = pd.read_sql_query("SELECT Service, ROUND(CAST(SUM(MFA_Enabled) AS FLOAT)/COUNT(*)*100, 2) as Adoption FROM mfa_status GROUP BY Service", conn)
df_events = pd.read_sql_query("SELECT EventType, IsBlocked, EventTimestamp FROM security_events", conn)
df_dept_risk = pd.read_sql_query("""
    SELECT e.Department, COUNT(se.EventID) as Total_Incidents
    FROM security_events se
    JOIN devices d ON se.DeviceID = d.DeviceID
    JOIN employees e ON d.EmployeeID = e.EmployeeID
    GROUP BY e.Department
""", conn)

# 2. Розрахунок ключових показників (KPI)
total_events = len(df_events)
blocked_rate = round(df_events['IsBlocked'].mean() * 100, 1)
avg_mfa = round(df_mfa['Adoption'].mean(), 1)

# 3. Створення графіків
# Графік 1: Рівень впровадження MFA
fig_mfa = px.bar(df_mfa, x='Service', y='Adoption', title='MFA Adoption Rate (%)',
                 color='Adoption', color_continuous_scale='RdYlGn')

# Графік 2: Розподіл інцидентів за відділами
fig_dept = px.pie(df_dept_risk, values='Total_Incidents', names='Department', 
                  title='Incidents Distribution by Department', hole=0.4)

# Графік 3: Тренд інцидентів за часом
df_events['Date'] = pd.to_datetime(df_events['EventTimestamp']).dt.date
df_trend = df_events.groupby('Date').size().reset_index(name='Count')
fig_trend = px.line(df_trend, x='Date', y='Count', title='Daily Security Events Trend')

# 4. Генерація HTML звіту
html_content = f"""
<html>
<head>
    <title>Cyber Security Executive Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f4f7f6; }}
        .header {{ background-color: #2c3e50; color: white; padding: 20px; text-align: center; border-radius: 10px; }}
        .kpi-container {{ display: flex; justify-content: space-around; margin: 20px 0; }}
        .kpi-card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center; width: 30%; }}
        .kpi-value {{ font-size: 32px; font-weight: bold; color: #2980b9; }}
        .chart {{ background: white; padding: 20px; margin-bottom: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
        .recommendations {{ background: #ebf5fb; padding: 20px; border-left: 5px solid #2980b9; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Cyber Security Compliance & Risk Report</h1>
        <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    </div>

    <div class="kpi-container">
        <div class="kpi-card">
            <p>Total Events Analyzed</p>
            <div class="kpi-value">{total_events:,}</div>
        </div>
        <div class="kpi-card">
            <p>Threat Prevention Rate</p>
            <div class="kpi-value">{blocked_rate}%</div>
        </div>
        <div class="kpi-card">
            <p>Global MFA Adoption</p>
            <div class="kpi-value">{avg_mfa}%</div>
        </div>
    </div>

    <div class="chart">{fig_trend.to_html(full_html=False, include_plotlyjs='cdn')}</div>
    
    <div style="display: flex; gap: 20px;">
        <div class="chart" style="width: 50%;">{fig_mfa.to_html(full_html=False, include_plotlyjs='cdn')}</div>
        <div class="chart" style="width: 50%;">{fig_dept.to_html(full_html=False, include_plotlyjs='cdn')}</div>
    </div>

    <div class="recommendations">
        <h2>🚀 Priority Action Plan</h2>
        <ul>
            <li><b>Critical:</b> Improve MFA for Services with less than 80% adoption.</li>
            <li><b>Department Focus:</b> Review security training for the <b>{df_dept_risk.loc[df_dept_risk['Total_Incidents'].idxmax(), 'Department']}</b> department (highest incident rate).</li>
            <li><b>Infrastructure:</b> Scheduled patching needed for devices with >30 days update lag.</li>
        </ul>
    </div>
</body>
</html>
"""

with open('CyberSecurity_Report.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Звіт успішно створено! Відкрийте файл 'CyberSecurity_Report.html' у вашому браузері.")
conn.close()
