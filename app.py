import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import base64

# 1. CONFIGURACIÓN E IDENTIDAD VISUAL DE VIALSCORE
st.set_page_config(
    page_title="VialScore - Ecosistema Conductual",
    page_icon="🚘",
    layout="wide"
)

# Estilos CSS personalizados para el Dark Mode, alertas y tarjetas de gamificación
st.markdown("""
    <style>
    .main { background-color: #0B1528; color: #FFFFFF; }
    .stMetric { background-color: #1E293B; padding: 18px; border-radius: 12px; border: 1px solid #00F5D4; box-shadow: 0px 4px 10px rgba(0, 245, 212, 0.1); }
    .card-beneficio { background-color: #1A2333; padding: 15px; border-radius: 10px; border-left: 5px solid #00F5D4; margin-bottom: 12px; }
    .card-reto { background-color: #1A2333; padding: 15px; border-radius: 10px; border-left: 5px solid #F59E0B; margin-bottom: 12px; }
    .card-viaje { background-color: #111A2E; padding: 12px; border-radius: 8px; border: 1px solid #1E293B; margin-bottom: 8px; }
    
    /* Estilos para el Score Gigante del Conductor */
    .score-container { text-align: center; padding: 30px; background-color: #1E293B; border-radius: 20px; border: 2px solid #00F5D4; margin-bottom: 20px; }
    .score-numero { font-size: 72px; font-weight: bold; color: #FFFFFF; margin: 0; }
    .score-nivel { font-size: 24px; font-weight: bold; color: #00F5D4; margin: 0; letter-spacing: 2px; }
    
    /* Nota de credenciales */
    .login-note { background-color: #1A2333; padding: 10px; border-radius: 5px; border: 1px solid #1E293B; font-size: 12px; color: #9CA3AF; margin-bottom: 15px; }
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
# BARRA LATERAL - LOGO ULTRA CIRCULAR MÁS GRANDE
# ==========================================
try:
    with open("img/vialscore.jpeg", "rb") as image_file:
        encoded_img = base64.b64encode(image_file.read()).decode()
    st.sidebar.markdown(
        f"""
        <div style="display: flex; justify-content: center; margin-top: 15px; margin-bottom: 20px;">
            <img src="data:image/jpeg;base64,{encoded_img}" 
                 style="width: 180px; height: 180px; border-radius: 50%; object-fit: cover; border: 4px solid #00F5D4; box-shadow: 0px 6px 20px rgba(0, 245, 212, 0.5);">
        </div>
        """, 
        unsafe_allow_html=True
    )
except Exception:
    st.sidebar.warning("Verifica la ruta: img/vialscore.jpeg")

# ==========================================
# MÓDULO DE LOGIN EN LA BARRA LATERAL
# ==========================================
st.sidebar.title("🔐 Control de Acceso")

# Nota aclaratoria para el jurado
st.sidebar.markdown("""
<div class="login-note">
    💡 <b>Guía de simulación para el Pitch:</b><br>
    • Conductor normal: Digita <b>123</b><br>
    • Administrador: Digita <b>admin</b>
</div>
""", unsafe_allow_html=True)

usuario_input = st.sidebar.text_input("Código de Usuario / DNI:", type="password")

# Control de estado de autenticación
if usuario_input == "123":
    rol_actual = "Conductor"
    st.sidebar.success("🧑‍✈️ Conductor Autenticado")
elif usuario_input.lower() == "admin":
    rol_actual = "Administrador"
    st.sidebar.success("💼 Admin Autenticado")
elif usuario_input == "":
    rol_actual = "Invitado"
    st.sidebar.info("Por favor, introduce tus credenciales en la barra lateral.")
else:
    rol_actual = "Error"
    st.sidebar.error("❌ Código incorrecto")

st.sidebar.markdown("---")

# ------------------------------------------------------------------
# VISTA INTERFACES SEGÚN ROL
# ------------------------------------------------------------------

if rol_actual == "Invitado" or rol_actual == "Error":
    # Pantalla de bienvenida si no se ha logueado nadie
    st.title("🚘 Bienvenidos a VialScore")
    st.subheader("El primer sistema de incentivos conductuales para el transporte público en el Perú [cite: 2, 3, 4]")
    st.markdown("""
    Esta plataforma integra el comportamiento de manejo seguro con beneficios económicos reales[cite: 30, 65, 66].
    
    ### 🚀 Instrucciones para la presentación del Pitch:
    Vaya a la barra lateral izquierda y utilice uno de nuestros perfiles pre-configurados para iniciar la experiencia:
    1. **Escriba `123`** para auditar el ecosistema desde la app móvil del conductor (**Luis Mendoza**), donde podrá revisar su score acumulado, billetera de activos viales y ránkings de gamificación[cite: 26, 73, 82].
    2. **Escriba `admin`** para ingresar al panel macro de analítica de flota, mapas GPS en vivo e indicadores financieros de la operadora.
    """)
    st.image("https://images.unsplash.com/photo-1557223562-6c77ef16210f?q=80&w=600&auto=format&fit=crop", width=700)

# ------------------------------------------------------------------
# ROL: CONDUCTOR (APP MÓVIL OPTIMIZADA Y REPOTENCIADA)
# ------------------------------------------------------------------
elif rol_actual == "Conductor":
    st.title("📱 VialScore - Mi Perfil de Conductor")
    st.caption("Hola Luis, consulta tu rendimiento en ruta e incentivos acumulados.")
    st.markdown("---")
    
    # Jalar directamente los datos de Luis Mendoza (ID 101)
    info_chofer = df[df["ID"] == 101].iloc[0]
    
    col_c1, col_c2, col_c3 = st.columns([1.1, 1.3, 1.1])
    
    with col_c1:
        # Score Principal en Grande
        st.markdown(f"""
            <div class="score-container">
                <p style="margin: 0; color: #9CA3AF; font-size: 13px; font-weight: bold; letter-spacing: 1px;">MI SCORE ACTUAL</p>
                <h1 class="score-numero">{info_chofer['Score Dinámico']}</h1>
                <p class="score-nivel">{info_chofer['Nivel']}</p>
                <p style="margin: 10px 0 0 0; color: #9CA3AF; font-size: 13px;">Línea: {info_chofer['Ruta']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Métricas individuales de telemetría consolidada
        st.metric(label="⭐ Calificación de Pasajeros (QR)", value=f"{info_chofer['Calificación Pasajeros']} / 5.0")
        st.metric(label="🚌 Viajes Seguros Realizados", value=f"{info_chofer['Viajes Completados']}")
        st.metric(label="⚠️ Frenadas Bruscas Totales", value=f"{info_chofer['Frenadas Bruscas']} inst.")

    with col_c2:
        st.markdown("### 🎁 Mi Billetera de Activos Viales Desbloqueados [cite: 66, 81]")
        st.markdown("<div class='card-beneficio'>🏆 <b>DESCUENTO SOAT ACTIVADO (Nivel Alto)</b><br>Felicidades. Mantienes un 20% de descuento directo para la renovación de tu SOAT[cite: 75].</div>", unsafe_allow_html=True)
        st.markdown("<div class='card-beneficio'>💳 <b>MICROCRÉDITO DISPONIBLE</b><br>Línea pre-aprobada para financiamiento de repuestos vehiculares con tasa preferencial[cite: 75].</div>", unsafe_allow_html=True)
        st.markdown("<div class='card-beneficio'>⛽ <b>BONO GNV / COMBUSTIBLE</b><br>Código: <code>VS-LUIS-2026</code> activo para S/ 30 de descuento en estaciones aliadas.</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🎯 Retos y Gamificación de Flota [cite: 82]")
        st.markdown("<div class='card-reto'>🏅 <b>Reto de Velocidad Perfecta:</b> Completa tus próximos 5 viajes sin registrar alertas GPS para ganar +20 puntos adicionales[cite: 85, 88].</div>", unsafe_allow_html=True)
        st.markdown("<div class='card-reto' style='border-left-color: #00F5D4;'>👑 <b>Ránking de la Operadora:</b> ¡Te encuentras en el Puesto #2 de toda la ruta Javier Prado! [cite: 83, 86]</div>", unsafe_allow_html=True)

    with col_c3:
        st.markdown("### 🔄 Historial Reciente de Viajes")
        st.markdown("""
        <div class='card-viaje'><b style='color:#00F5D4;'>Viaje #124</b> • Finalizado<br>Ruta: Javier Prado • 0 Alertas<br>Score Viaje: <b>195 pts</b></div>
        <div class='card-viaje'><b style='color:#00F5D4;'>Viaje #123</b> • Finalizado<br>Ruta: Javier Prado • 1 Frenada<br>Score Viaje: <b>150 pts</b></div>
        <div class='card-viaje'><b style='color:#F59E0B;'>Viaje #122</b> • Finalizado<br>Ruta: Javier Prado • 1 Exceso Vel.<br>Score Viaje: <b>120 pts</b></div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        # NUEVO INTERACTIVO: Módulo de feedback directo del Pasajero simulado dentro del celular del Conductor
        st.markdown("### 📲 Feedback Virtual del Pasajero (Simulador QR) [cite: 112]")
        st.caption("Simula la interfaz que se le abre al pasajero al escanear el QR del asiento[cite: 115].")
        rating_slider = st.slider("Calificar servicio de Luis (1 Tap):", 1.0, 5.0, 5.0, step=0.5)
        if st.button("Enviar Calificación Anónima"):
            # Lógica para recalcular el promedio de estrellitas de Luis en tiempo real
            idx_luis = df[df["ID"] == 101].index[0]
            st.session_state.df_conductores.at[idx_luis, "Calificación Pasajeros"] = round((st.session_state.df_conductores.at[idx_luis, "Calificación Pasajeros"] + rating_slider) / 2, 2)
            st.success("¡Gracias! Calificación procesada instantáneamente.")
            st.rerun()

# ------------------------------------------------------------------
# ROL: ADMINISTRADOR (PANEL MACRO DE CONTROL OPERATIVO)
# ------------------------------------------------------------------
elif rol_actual == "Administrador":
    st.sidebar.title("Menú de Navegación Admin")
    menu = st.sidebar.radio("Secciones Disponibles:", ["🎛️ Dashboard de Operaciones", "📡 Simulador IoT / Telemetría", "💵 Viabilidad y Presupuesto"])

    if menu == "🎛️ Dashboard de Operaciones":
        st.title("💼 Panel de Operaciones - Administrador")
        st.caption("Central de monitoreo y auditoría macro de la flota de transporte urbano")
        st.markdown("---")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric(label="Reducción de Siniestros (Proyectado)", value="-30%")
        with col2: st.metric(label="Score Promedio de Flota", value=f"{int(df['Score Dinámico'].mean())} pts")
        with col3: st.metric(label="Satisfacción Promedio Pasajero", value=f"{df['Calificación Pasajeros'].mean():.2f} / 5.0")
        with col4: st.metric(label="Conductores en Nivel Alto", value=f"{len(df[df['Nivel']=='ALTO'])} / {len(df)}")
            
        st.markdown("---")
        st.markdown("### 🗺️ Monitoreo de Unidades en Vivo (GPS Tracking Piloto)")
        st.map(df, latitude="latitude", longitude="longitude", size=40)
        st.markdown("---")
        
        rutas = st.multiselect("Filtrar por Corredor Vial Piloto:", options=df["Ruta"].unique(), default=df["Ruta"].unique())
        df_filtrado = df[df["Ruta"].isin(rutas)]
        
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown("### 📋 Registro en Tiempo Real de Conductores Formales")
            st.dataframe(df_filtrado.style.background_gradient(cmap="summer", subset=["Score Dinámico", "Calificación Pasajeros"]), use_container_width=True)
        with c2:
            st.markdown("### 🎯 Distribución de la Flota por Niveles")
            fig_pie = px.pie(df_filtrado, names='Nivel', values='Score Dinámico', color='Nivel',
                             color_discrete_map={'ALTO': '#00F5D4', 'MEDIO': '#F59E0B', 'BAJO': '#EF4444'}, hole=0.3)
            st.plotly_chart(fig_pie, use_container_width=True)

    elif menu == "📡 Simulador IoT / Telemetría":
        st.title("📡 Módulo de Procesamiento de Telemetría (Cámaras + GPS)")
        st.markdown("Simula el procesamiento de incidencias en ruta enviadas por los dispositivos IoT integrados.")
        st.markdown("---")
        
        col_sim1, col_sim2 = st.columns(2)
        with col_sim1:
            st.markdown("### 📥 Registrar Eventos de Viaje")
            conductor_select = st.selectbox("Seleccionar Unidad / Conductor:", df["Conductor"])
            frenadas_nuevas = st.number_input("Frenadas Bruscas Detectadas por Sensor:", min_value=0, max_value=10, value=0)
            velocidad_nueva = st.number_input("Infracciones por Exceso de Velocidad (GPS):", min_value=0, max_value=5, value=0)
            rating_pasajero = st.slider("Calificación Promedio de este viaje:", 1.0, 5.0, 5.0, step=0.1)
            
            btn_procesar = st.button("🚀 Procesar Datos de Telemetría")
            if btn_procesar:
                idx = df[df["Conductor"] == conductor_select].index[0]
                penalizacion = (frenadas_nuevas * 10) + (velocidad_nueva * 15)
                score_viaje = max(0, min(200, 150 - penalizacion + int(rating_pasajero * 10)))
                
                st.session_state.df_conductores.at[idx, "Viajes Completados"] += 1
                st.session_state.df_conductores.at[idx, "Frenadas Bruscas"] += frenadas_nuevas
                st.session_state.df_conductores.at[idx, "Excesos Velocidad"] += velocidad_nueva
                st.session_state.df_conductores.at[idx, "Calificación Pasajeros"] = round((st.session_state.df_conductores.at[idx, "Calificación Pasajeros"] + rating_pasajero)/2, 2)
                st.session_state.df_conductores.at[idx, "latitude"] += np.random.uniform(-0.002, 0.002)
                st.session_state.df_conductores.at[idx, "longitude"] += np.random.uniform(-0.002, 0.002)
                
                nuevo_score_hist = int((st.session_state.df_conductores.at[idx, "Score Dinámico"] + score_viaje) / 2)
                st.session_state.df_conductores.at[idx, "Score Dinámico"] = min(200, max(0, nuevo_score_hist))
                
                st.success(f"¡Viaje de {conductor_select} procesado! Datos guardados en la central.")
                st.rerun()
                
        with col_sim2:
            st.markdown("### 🔍 Vista de Auditoría de Incentivos")
            idx_c = df[df["Conductor"] == conductor_select].index[0]
            chofer_info = df.iloc[idx_c]
            st.write(f"**Estado del Conductor:** {chofer_info['Conductor']} | **Puntaje:** `{chofer_info['Score Dinámico']} pts`")
            if chofer_info["Nivel"] == "ALTO":
                st.markdown("<div class='card-beneficio'>🏆 Nivel ALTO validado para descuentos estatales y SOAT corporativo.</div>", unsafe_allow_html=True)
            elif chofer_info["Nivel"] == "MEDIO":
                st.markdown("<div class='card-beneficio' style='border-left-color: #F59E0B;'>⚠️ Nivel MEDIO. Monitoreo regular sin penalizaciones graves.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='card-beneficio' style='border-left-color: #EF4444;'>🚨 Nivel BAJO. Alerta activa enviada para re-capacitación de ruta.</div>", unsafe_allow_html=True)

    elif menu == "💵 Viabilidad y Presupuesto":
        st.title("📊 Análisis Financiero y Viabilidad del Proyecto")
        st.markdown("---")
        c_fin1, c_fin2 = st.columns(2)
        with c_fin1:
            st.markdown("### 📈 Costos del Piloto (50 Vehículos / 6 Meses)")
            presupuesto = {"Concepto de Inversión": ["Hardware (Cámaras + GPS IoT)", "Desarrollo del MVP Móvil", "Infraestructura Cloud / Servidores", "Operaciones, Equipo y Monitoreo"], "Monto (USD)": [25000, 15000, 5000, 10000]}
            st.table(pd.DataFrame(presupuesto))
            st.metric(label="Total Inversión Requerida", value="US$ 55,000")
        with c_fin2:
            st.markdown("### 💸 Canales de Financiamiento e Ingresos")
            fig_fin = px.bar(x=["Suscripción Empresas", "Subsidio Esperado MTC", "Brecha Financiera"], y=[12000, 20000, 23000], title="Estructura de Financiamiento", color_discrete_sequence=['#00F5D4'])
            st.plotly_chart(fig_fin, use_container_width=True)
