import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

# Configuración de página
st.set_page_config(
    page_title="PCSHEK - Dashboard Empresarial",
    page_icon="🏢",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e293b, #334155);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🏢 PCSHEK - Dashboard Empresarial</h1>
    <p>💚 Reciclaje Inteligente - Control de Asistencia</p>
</div>
""", unsafe_allow_html=True)

# Datos simulados (reemplazar con API real)
def get_dashboard_data():
    return {
        'total_records': 45,
        'employees_inside': [
            {'name': 'Juan Pérez', 'time': '08:30'},
            {'name': 'María García', 'time': '08:45'},
        ],
        'employees_outside': [
            {'name': 'Carlos López', 'time': '17:30'},
        ],
        'recent_records': [
            {'name': 'Ana Rodríguez', 'event_type': 'entrada', 'timestamp': '2024-01-06 09:15:00'},
            {'name': 'Pedro Martín', 'event_type': 'salida', 'timestamp': '2024-01-06 17:00:00'},
        ]
    }

# Layout principal
col1, col2, col3 = st.columns(3)

data = get_dashboard_data()

with col1:
    st.metric("📊 Registros Hoy", data['total_records'])
    
with col2:
    st.metric("👥 Empleados Dentro", len(data['employees_inside']))
    
with col3:
    st.metric("🚪 Empleados Fuera", len(data['employees_outside']))

# Empleados dentro/fuera
col1, col2 = st.columns(2)

with col1:
    st.subheader("✅ Empleados Dentro")
    for emp in data['employees_inside']:
        st.success(f"👤 {emp['name']} - {emp['time']}")

with col2:
    st.subheader("❌ Empleados Fuera")
    for emp in data['employees_outside']:
        st.info(f"👤 {emp['name']} - {emp['time']}")

# Actividad reciente
st.subheader("📋 Actividad Reciente")
for record in data['recent_records']:
    icon = "🟢" if record['event_type'] == 'entrada' else "🔴"
    st.write(f"{icon} **{record['name']}** - {record['event_type'].upper()} - {record['timestamp']}")

# Auto-refresh
if st.button("🔄 Actualizar"):
    st.rerun()

# Auto-refresh cada 30 segundos
time.sleep(30)
st.rerun()