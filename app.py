import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página de VialScore
st.set_page_config(
    page_title="VialScore - Panel de Operaciones",
    page_icon="🚘",
    layout="wide"
)

# Estilo personalizado (Dark Mode elegante alineado con VialScore)
st.markdown("""
    <style>
    .main { background-color: #0B1528; color: #FFFFFF; }
    .stMetric { background-color: #1E293B; padding: 15px; border-radius: 10px; border: 1px solid #00F5D4; }
    </style>
    """, unsafe_style_headers=True)

# Encabezado del Proyecto
st.title("🚘 VialScore: Control y Gestión Conductual")
st.subheader("AAP Innovation Challenge 2026 | Equipo NextStep")
st.markdown("---")

# 1. KPIs Principales del Piloto (Meta del Mes 6)
st.markdown("### 📊 Indicadores de Éxito del Piloto (Flota de 50 Vehículos)")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Reducción de Infracciones", value="-25%", delta="Meta Alcanzada")
with col2:
    st.metric(label="Score Promedio Flota", value="142 pts", delta="+42 pts vs Inicio")
with col3:
    st.metric(label="Satisfacción del Pasajero", value="4.2 / 5.0", delta="+0.2")
with col4:
    st.metric(label="Conductores Activos en App", value="85%", delta="Meta: >80%")

st.markdown("---")

# 2. Base de Datos Simulada de Conductores (Evidencia de Campo)
# Clasificación según el pilar de Score Dinámico: Alto (150-200), Medio (80-149), Bajo (0-79)
data_conductores = {
    "Conductor": ["Luis Mendoza", "Carlos Jayo", "Jorge Quispe", "Andrés Soto", "Miguel Benites"],
    "Ruta": ["Javier Prado", "Corredor Azul", "Javier Prado", "Corredor Azul", "Javier Prado"],
    "Viajes Seguros": [124, 98, 110, 45, 12],
    "Frenadas Bruscas": [2, 5, 1, 12, 28],
    "Score Dinámico": [185, 142, 190, 85, 42],
    "Nivel": ["ALTO", "MEDIO", "ALTO", "MEDIO", "BAJO"]
}

df = pd.DataFrame(data_conductores)

# Lógica de Filtros en la Barra Lateral
st.sidebar.header("Filtros de Búsqueda")
ruta_seleccionada = st.sidebar.multiselect(
    "Selecciona la Ruta Piloto:",
    options=df["Ruta"].unique(),
    default=df["Ruta"].unique()
)

df_filtrado = df[df["Ruta"].isin(ruta_seleccionada)]

# 3. Visualización de Datos (Gráfico de Distribución de Scores)
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("### 📋 Monitoreo de Conductores en Tiempo Real")
    # Mostrar la tabla formateada con los datos dinámicos
    st.dataframe(df_filtrado.style.background_gradient(cmap="Blues", subset=["Score Dinámico"]), use_container_width=True)

with col_right:
    st.markdown("### 🎯 Distribución por Niveles")
    fig = px.pie(
        df_filtrado, 
        names='Nivel', 
        values='Score Dinámico',
        color='Nivel',
        color_discrete_map={'ALTO': '#00F5D4', 'MEDIO': '#F59E0B', 'BAJO': '#EF4444'},
        hole=0.4
    )
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# 4. Sección de Impacto y Beneficios Tangibles (SCS-TP)
st.markdown("### 🎁 Sistema de Incentivos y Activos Económicos del Conductor")
conductor_select = st.selectbox("Selecciona un conductor para evaluar sus beneficios acumulados:", df["Conductor"])

datos_chofer = df[df["Conductor"] == conductor_select].iloc[0]

st.markdown(f"**Estado actual de {conductor_select}:**")
if datos_chofer["Nivel"] == "ALTO":
    st.success(f"🏆 **Nivel ALTO ({datos_chofer['Score Dinámico']} pts):** Habilitado para un 20% de descuento en el SOAT y acceso prioritario a microcréditos viales.")
elif datos_chofer["Nivel"] == "MEDIO":
    st.warning(f"⚠️ **Nivel MEDIO ({datos_chofer['Score Dinámico']} pts):** Cumple con las normas básicas. A un paso de desbloquear subsidios de mantenimiento vehicular.")
else:
    st.error(f"🚨 **Nivel BAJO ({datos_chofer['Score Dinámico']} pts):** Conductor en riesgo. Requiere capacitación en ecodriving y alertas prioritarias.")
