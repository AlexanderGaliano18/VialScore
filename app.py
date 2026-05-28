import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import base64

# 1. CONFIGURACIÓN E IDENTIDAD VISUAL DE VIALSCORE
st.set_page_config(
    page_title="VialScore - Panel de Control Integral",
    page_icon="🚘",
    layout="wide"
)

# Estilos CSS personalizados para el Dark Mode y el formato de los elementos
st.markdown("""
    <style>
    .main { background-color: #0B1528; color: #FFFFFF; }
    .stMetric { background-color: #1E293B; padding: 18px; border-radius: 12px; border: 1px solid #00F5D4; box-shadow: 0px 4px 10px rgba(0, 245, 212, 0.1); }
    .card-beneficio { background-color: #1A2333; padding: 15px; border-radius: 10px; border-left: 5px solid #00F5D4; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Inicializar Base de Datos en Estado de Sesión (Session State) para simular persistencia
if 'df_conductores' not in st.session_state:
    raw_data = {
        "ID": [101, 102, 103, 104, 105],
        "Conductor": ["Luis Mendoza", "Carlos Jayo", "Jorge Quispe", "Andrés Soto", "Miguel Benites"],
        "Ruta": ["Javier Prado", "Corredor Azul", "Javier Prado", "Corredor Azul", "Javier Prado"],
        "Viajes Completados": [124, 98, 110, 45, 12],
        "Frenadas Bruscas": [2, 5, 1, 12, 28],
        "Excesos Velocidad": [0, 3, 0, 8, 19],
        "Calificación Pasajeros": [4.8, 4.2, 4.9, 3.9, 3.2],
        "Score Dinámico": [185, 142, 195, 85, 38],
        # Coordenadas iniciales sobre el mapa de Lima Metropolitana
        "latitude": [-12.0858, -12.0464, -12.0921, -12.0712, -12.0815],
        "longitude": [-77.0358, -77.0345, -76.9740, -77.0360, -77.0120]
    }
    st.session_state.df_conductores = pd.DataFrame(raw_data)

df = st.session_state.df_conductores

# ALGORITMO CONDUCTUAL PARA CLASIFICACIÓN DE NIVELES (Pilar 2)
def calcular_nivel(score):
    if score >= 150: return "ALTO"
    elif score >= 80: return "MEDIO"
    else: return "BAJO"

df["Nivel"] = df["Score Dinámico"].apply(calcular_nivel)

# ==========================================
# BARRA LATERAL - LOGO ULTRA CIRCULAR OPTIMIZADO
# ==========================================
try:
    # Leemos tu imagen local jpeg y la transformamos de forma segura sin romper contenedores
    with open("img/vialscore.jpeg", "rb") as image_file:
        encoded_img = base64.b64encode(image_file.read()).decode()
    
    # Inyección HTML/CSS para forzar círculo perfecto sin bordes blancos cuadrados
    st.sidebar.markdown(
        f"""
        <div style="display: flex; justify-content: center; margin-top: 10px; margin-bottom: 15px;">
            <img src="data:image/jpeg;base64,{encoded_img}" 
                 style="width: 300px; height: 300px; border-radius: 50%; object-fit: cover; border: 3px solid #00F5D4; box-shadow: 0px 4px 15px rgba(0, 245, 212, 0.4);">
        </div>
        """, 
        unsafe_allow_html=True
    )
except Exception:
    st.sidebar.warning("Verifica la ruta: img/vialscore.jpeg")

st.sidebar.title("Navegación VialScore")
menu = st.sidebar.radio("Ir a la Sección:", ["🎛️ Dashboard de Operaciones", "📡 Simulador IoT / Telemetría", "💵 Viabilidad y Presupuesto"])

# ------------------------------------------------------------------
# VISTA 1: DASHBOARD DE OPERACIONES
# ------------------------------------------------------------------
if menu == "🎛️ Dashboard de Operaciones":
    st.title("🚘 VialScore: Sistema de Gestión Conductual de Transporte")
    st.caption("AAP Innovation Challenge 2026 | Desarrollado por Equipo NextStep")
    st.markdown("---")
    
    # KPIs Globales con deltas del piloto
    st.markdown("### 📊 Indicadores Clave del Piloto (Flota Actual)")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Reducción de Siniestros (Proyectado)", value="-30%", delta="Meta Base: -25%")
    with col2:
        st.metric(label="Score Promedio de Flota", value=f"{int(df['Score Dinámico'].mean())} pts", delta="+49 vs Línea Base")
    with col3:
        st.metric(label="Satisfacción Promedio Pasajero", value=f"{df['Calificación Pasajeros'].mean():.2f} / 5.0", delta="+15% este mes")
    with col4:
        st.metric(label="Conductores en Nivel Alto", value=f"{len(df[df['Nivel']=='ALTO'])} / {len(df)}", delta="Crecimiento sostenido")
        
    st.markdown("---")
    
    # SECCIÓN DEL MAPA INTEGRADOR EN VIVO
    st.markdown("### 🗺️ Monitoreo de Unidades en Vivo (GPS Tracking Piloto)")
    st.markdown("Mapa interactivo que simula el rastreo por satélite de los buses asignados a las rutas piloto.")
    st.map(df, latitude="latitude", longitude="longitude", size=40)
    st.caption("💡 *Nota para el jurado: El movimiento de los puntos en el mapa se calcula dinámicamente al procesar datos telemétricos de telemetría por viaje.*")
    st.markdown("---")
    
    # Filtros de las rutas piloto en Lima
    rutas = st.multiselect("Filtrar por Corredor Vial Piloto:", options=df["Ruta"].unique(), default=df["Ruta"].unique())
    df_filtrado = df[df["Ruta"].isin(rutas)]
    
    # Tablas y gráficos de distribución
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("### 📋 Registro en Tiempo Real de Conductores Formales")
        # El background_gradient que requiere matplotlib funciona perfecto aquí
        st.dataframe(df_filtrado.style.background_gradient(cmap="summer", subset=["Score Dinámico", "Calificación Pasajeros"]), use_container_width=True)
    with c2:
        st.markdown("### 🎯 Distribución de la Flota por Niveles")
        fig_pie = px.pie(df_filtrado, names='Nivel', values='Score Dinámico', color='Nivel',
                         color_discrete_map={'ALTO': '#00F5D4', 'MEDIO': '#F59E0B', 'BAJO': '#EF4444'}, hole=0.3)
        st.plotly_chart(fig_pie, use_container_width=True)

# ------------------------------------------------------------------
# VISTA 2: SIMULADOR IOT / TELEMETRÍA
# ------------------------------------------------------------------
elif menu == "📡 Simulador IoT / Telemetría":
    st.title("📡 Módulo de Procesamiento de Telemetría (Cámaras + GPS)")
    st.markdown("Simula la entrada de datos en tiempo real de los sensores inteligentes instalados a bordo de los buses viales.")
    st.markdown("---")
    
    col_sim1, col_sim2 = st.columns(2)
    
    with col_sim1:
        st.markdown("### 📥 Registrar Eventos de Viaje (Simulación del Dispositivo)")
        conductor_select = st.selectbox("Seleccionar Unidad / Conductor:", df["Conductor"])
        
        frenadas_nuevas = st.number_input("Frenadas Bruscas Detectadas por Sensor:", min_value=0, max_value=10, value=0)
        velocidad_nueva = st.number_input("Infracciones por Exceso de Velocidad (GPS):", min_value=0, max_value=5, value=0)
        rating_pasajero = st.slider("Calificación de Pasajeros vía QR (1 Tap):", 1.0, 5.0, 5.0, step=0.1)
        
        btn_procesar = st.button("🚀 Procesar Datos de Telemetría y Actualizar Score")
        
        if btn_procesar:
            idx = df[df["Conductor"] == conductor_select].index[0]
            
            # Penalizaciones lógicas por mala conducta conductual
            penalizacion = (frenadas_nuevas * 10) + (velocidad_nueva * 15)
            score_viaje = max(0, min(200, 150 - penalizacion + int(rating_pasajero * 10)))
            
            # Actualización del DataFrame dinámico en la sesión actual
            st.session_state.df_conductores.at[idx, "Viajes Completados"] += 1
            st.session_state.df_conductores.at[idx, "Frenadas Bruscas"] += frenadas_nuevas
            st.session_state.df_conductores.at[idx, "Excesos Velocidad"] += velocidad_nueva
            st.session_state.df_conductores.at[idx, "Calificación Pasajeros"] = round((st.session_state.df_conductores.at[idx, "Calificación Pasajeros"] + rating_pasajero)/2, 2)
            
            # Simular desplazamiento físico del bus sobre el mapa de Lima
            st.session_state.df_conductores.at[idx, "latitude"] += np.random.uniform(-0.002, 0.002)
            st.session_state.df_conductores.at[idx, "longitude"] += np.random.uniform(-0.002, 0.002)
            
            # Actualizar el score histórico integrado del chofer
            nuevo_score_hist = int((st.session_state.df_conductores.at[idx, "Score Dinámico"] + score_viaje) / 2)
            st.session_state.df_conductores.at[idx, "Score Dinámico"] = min(200, max(0, nuevo_score_hist))
            
            st.success(f"¡Viaje de {conductor_select} procesado con éxito! Se calculó el impacto vial y la unidad avanzó en el mapa.")
            st.rerun()
            
    with col_sim2:
        st.markdown("### 🎁 Billetera Digital de Incentivos (Pilar 3)")
        idx_c = df[df["Conductor"] == conductor_select].index[0]
        chofer_info = df.iloc[idx_c]
        
        st.markdown(f"**Conductor:** {chofer_info['Conductor']} | **Puntaje Actual:** `{chofer_info['Score Dinámico']} / 200 pts`")
        
        if chofer_info["Nivel"] == "ALTO":
            st.markdown("<div class='card-beneficio'>🏆 <b>NIVEL ALTO DESBLOQUEADO</b><br>• 20% Descuento Directo en renovación de SOAT.<br>• Acceso Prioritario a Microcréditos.<br>• Bono de Combustible Premium.</div>", unsafe_allow_html=True)
        elif chofer_info["Nivel"] == "MEDIO":
            st.markdown("<div class='card-beneficio' style='border-left-color: #F59E0B;'>⚠️ <b>NIVEL MEDIO (Estable)</b><br>• Acceso a Subsidios parciales de Mantenimiento Vehicular.<br>• Próximo desbloqueo de bonos a los 150 puntos.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='card-beneficio' style='border-left-color: #EF4444;'>🚨 <b>NIVEL BAJO (Plan de Mitigación)</b><br>• Restringido de incentivos viales.<br>• Alerta enviada a la empresa operadora para capacitación obligatoria en Ecodriving.</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# VISTA 3: VIABILIDAD FINANCIERA Y PRESUPUESTO
# ------------------------------------------------------------------
elif menu == "💵 Viabilidad y Presupuesto":
    st.title("📊 Análisis Financiero y Viabilidad del Proyecto")
    st.markdown("Proyección presupuestaria para el Piloto Inicial de 6 meses en Lima Metropolitana.")
    st.markdown("---")
    
    c_fin1, c_fin2 = st.columns(2)
    with c_fin1:
        st.markdown("### 📈 Costos del Piloto (50 Vehículos / 6 Meses)")
        presupuesto = {
            "Concepto de Inversión": ["Hardware (Cámaras + GPS IoT)", "Desarrollo del MVP Móvil", "Infraestructura Cloud / Servidores", "Operaciones, Equipo y Monitoreo"],
            "Monto (USD)": [25000, 15000, 5000, 10000]
        }
        df_p = pd.DataFrame(presupuesto)
        st.table(df_p)
        st.metric(label="Total Inversión Requerida", value="US$ 55,000")
        
    with c_fin2:
        st.markdown("### 💸 Canales de Financiamiento e Ingresos")
        fig_fin = px.bar(
            x=["Suscripción Empresas", "Subsidio Esperado MTC", "Brecha Financiera"],
            y=[12000, 20000, 23000],
            labels={'x': 'Fuente de Financiamiento', 'y': 'Monto en USD'},
            title="Estructura de Financiamiento del Piloto",
            color_discrete_sequence=['#00F5D4']
        )
        st.plotly_chart(fig_fin, use_container_width=True)
        st.info("💡 **Ahorro Social Estimado:** El despliegue a gran escala de VialScore proyecta un ahorro de S/ 2,000 millones a 5 años en reducción de costos por siniestros y congestión vial en el Perú.")
