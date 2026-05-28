import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import base64

# 1. CONFIGURACIÓN E IDENTIDAD VISUAL DE VIALSCORE
st.set_page_config(
    page_title="VialScore - Plataforma Inteligente",
    page_icon="🚘",
    layout="wide"
)

# Estilos CSS avanzados para el Look & Feel de VialScore
st.markdown("""
    <style>
    .main { background-color: #0B1528; color: #FFFFFF; }
    .stMetric { background-color: #1E293B; padding: 18px; border-radius: 12px; border: 1px solid #00F5D4; box-shadow: 0px 4px 10px rgba(0, 245, 212, 0.1); }
    .card-beneficio { background-color: #1A2333; padding: 15px; border-radius: 10px; border-left: 5px solid #00F5D4; margin-bottom: 12px; }
    .card-reto { background-color: #1A2333; padding: 15px; border-radius: 10px; border-left: 5px solid #F59E0B; margin-bottom: 12px; }
    
    /* Contenedor del Score Gigante */
    .score-container { text-align: center; padding: 25px; background-color: #1E293B; border-radius: 20px; border: 2px solid #00F5D4; margin-bottom: 15px; }
    .score-numero { font-size: 64px; font-weight: bold; color: #FFFFFF; margin: 0; }
    .score-nivel { font-size: 20px; font-weight: bold; color: #00F5D4; margin: 0; letter-spacing: 2px; }
    
    /* Nota de simulación */
    .login-note { background-color: #1A2333; padding: 12px; border-radius: 8px; border: 1px solid #1E293B; font-size: 13px; color: #9CA3AF; margin-bottom: 15px; }
    
    /* Quitar bordes por defecto de las pestañas */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #1E293B; border-radius: 8px; padding: 10px 20px; color: #FFFFFF; }
    .stTabs [aria-selected="true"] { background-color: #00F5D4 !important; color: #0B1528 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Inicializar base de datos en Session State para persistencia de datos
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

# Control de estado de autenticación (Login persistente de Streamlit)
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
    st.session_state.rol = "Invitado"

df = st.session_state.df_conductores

# Algoritmo de clasificación conductual
def calcular_nivel(score):
    if score >= 150: return "ALTO"
    elif score >= 80: return "MEDIO"
    else: return "BAJO"

df["Nivel"] = df["Score Dinámico"].apply(calcular_nivel)

# ==========================================
# BARRA LATERAL - LOGO CIRCULAR GIGANTE
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
    st.sidebar.warning("Verifica tu imagen en: img/vialscore.jpeg")

# ==========================================
# SISTEMA DE LOGIN Y CONTROL DE FLUJO
# ==========================================
if not st.session_state.autenticado:
    st.sidebar.title("🔐 Control de Acceso")
    st.sidebar.markdown("""
    <div class="login-note">
        💡 <b>Credenciales de Simulación:</b><br>
        • Conductor Móvil: Escribe <b>123</b><br>
        • Administrador Web: Escribe <b>admin</b>
    </div>
    """, unsafe_allow_html=True)
    
    usuario_input = st.sidebar.text_input("Ingresa tu Código de Usuario:", type="password")
    btn_login = st.sidebar.button("Ingresar al Sistema")
    
    if btn_login:
        if usuario_input == "123":
            st.session_state.autenticado = True
            st.session_state.rol = "Conductor"
            st.rerun()
        elif usuario_input.lower() == "admin":
            st.session_state.autenticado = True
            st.session_state.rol = "Administrador"
            st.rerun()
        else:
            st.sidebar.error("❌ Código inválido")
else:
    # Si ya está logueado, muestra el botón de Cerrar Sesión fijo en la barra lateral
    st.sidebar.title("👤 Usuario Activo")
    st.sidebar.info(f"Conectado como: **{st.session_state.rol}**")
    if st.sidebar.button("🚪 Cerrar Sesión"):
        st.session_state.autenticado = False
        st.session_state.rol = "Invitado"
        st.rerun()

# ------------------------------------------------------------------
# VISTA: INVITADO (PANTALLA DE BIENVENIDA)
# ------------------------------------------------------------------
if st.session_state.rol == "Invitado":
    st.title("🚘 Bienvenidos al Ecosistema VialScore")
    st.subheader("AAP Innovation Challenge 2026 | Equipo NextStep")
    st.markdown("---")
    st.markdown("""
    Esta solución transforma el comportamiento de los conductores de transporte público mediante analítica, IoT y gamificación estructurada.
    
    ### 🛠️ Para iniciar la simulación del software interactivo:
    1. Diríjase al panel de **Control de Acceso** en la barra lateral izquierda.
    2. Escriba **`123`** para abrir la interfaz del **Conductor** (Luis Mendoza) y ver sus retos o activos acumulados.
    3. Escriba **`admin`** para desplegar el **Panel de Administración Macro** que gestiona la seguridad vial de toda la flota de Lima Metropolitana.
    """)
    st.image("https://images.unsplash.com/photo-1557223562-6c77ef16210f?q=80&w=600&auto=format&fit=crop", width=700)

# ------------------------------------------------------------------
# VISTA: CONDUCTOR (APP MÓVIL TOTALMENTE REORGANIZADA CON TABS Y DASHBOARDS)
# ------------------------------------------------------------------
elif st.session_state.rol == "Conductor":
    st.title("📱 VialScore - Mi Perfil de Conductor")
    st.caption("Hola Luis, consulta tu rendimiento en ruta e incentivos acumulados.")
    st.markdown("---")
    
    # Jalar datos estables del chofer Luis Mendoza
    info_chofer = df[df["ID"] == 101].iloc[0]
    
    # BARRA DE NAVEGACIÓN SUPERIOR (Pestañas móviles)
    tab_resumen, tab_billetera, tab_historial = st.tabs(["📊 Mi Resumen", "🎁 Mi Billetera Viales", "📈 Historial y Calificaciones"])
    
    with tab_resumen:
        col_res1, col_res2 = st.columns([1, 2])
        with col_res1:
            st.markdown(f"""
                <div class="score-container">
                    <p style="margin: 0; color: #9CA3AF; font-size: 13px; font-weight: bold; letter-spacing: 1px;">MI SCORE CONDUCTUAL</p>
                    <h1 class="score-numero">{info_chofer['Score Dinámico']}</h1>
                    <p class="score-nivel">{info_chofer['Nivel']}</p>
                    <p style="margin: 10px 0 0 0; color: #9CA3AF; font-size: 13px;">Línea: {info_chofer['Ruta']}</p>
                </div>
            """, unsafe_allow_html=True)
            st.metric(label="⭐ Calificación de Pasajeros", value=f"{info_chofer['Calificación Pasajeros']} / 5.0")
            
        with col_res2:
            st.markdown("### 🎯 Retos Activos y Gamificación Semanal")
            st.markdown("<div class='card-reto'>🏅 <b>Reto Velocidad Constante:</b> Culmina tus siguientes 5 rutas sin alertas GPS y recibe +20 puntos de score.</div>", unsafe_allow_html=True)
            st.markdown("<div class='card-reto' style='border-left-color: #00F5D4;'>👑 <b>Ránking de Flota:</b> ¡Felicidades! Ocupas el Puesto #2 en el Corredor Javier Prado.</div>", unsafe_allow_html=True)
            
            # Gráfico de Dashboard Personal del Conductor
            st.markdown("### 📊 Evolución Semanal de Score")
            df_evolucion = pd.DataFrame({
                "Día": ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Hoy"],
                "Score": [160, 165, 155, 170, 172, 180, int(info_chofer['Score Dinámico'])]
            })
            fig_evol = px.line(df_evolucion, x="Día", y="Score", markers=True, color_discrete_sequence=["#00F5D4"])
            fig_evol.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#FFFFFF", height=200, margin=dict(t=10,b=10,l=10,r=10))
            st.plotly_chart(fig_evol, use_container_width=True)

    with tab_billetera:
        st.markdown("### 🎁 Activos Económicos Acumulados por Buen Manejo")
        st.markdown("<div class='card-beneficio'>🏆 <b>DESCUENTO DE SOAT INTEGRADO (Nivel Alto):</b> Validado con Aseguradoras para un 20% de descuento directo en tu renovación trimestral.</div>", unsafe_allow_html=True)
        st.markdown("<div class='card-beneficio'>💳 <b>MICROCRÉDITO ASIGNADO:</b> Tienes una línea de crédito blando aprobada para reposición de neumáticos en talleres oficiales.</div>", unsafe_allow_html=True)
        st.markdown("<div class='card-beneficio'>⛽ <b>CÓDIGO DE COMBUSTIBLE GRIS:</b> Usa el código <code>VS-LUIS-2026</code> en estaciones asociadas para S/ 30 de descuento en GNV/Gasolina.</div>", unsafe_allow_html=True)

    with tab_historial:
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            st.markdown("### 🚌 Historial de Telemetría (Últimos Viajes)")
            st.markdown("""
            <div style="background-color: #111A2E; padding: 12px; border-radius: 8px; margin-bottom: 8px;"><b>Viaje #124:</b> Ruta Javier Prado • 0 Incidentes • <span style="color:#00F5D4;">195 pts</span></div>
            <div style="background-color: #111A2E; padding: 12px; border-radius: 8px; margin-bottom: 8px;"><b>Viaje #123:</b> Ruta Javier Prado • 1 Frenada Brusca • <span style="color:#00F5D4;">150 pts</span></div>
            <div style="background-color: #111A2E; padding: 12px; border-radius: 8px; margin-bottom: 8px;"><b>Viaje #122:</b> Ruta Javier Prado • 1 Exceso de Velocidad • <span style="color:#F59E0B;">120 pts</span></div>
            """, unsafe_allow_html=True)
        with col_h2:
            st.markdown("### 📲 Calificación del Pasajero Virtual (Simulador QR)")
            st.caption("Prueba cómo los usuarios escanean el QR de tu asiento y su nota impacta en vivo en tu perfil.")
            rating_slider = st.slider("Asignar estrellitas al viaje actual:", 1.0, 5.0, 5.0, step=0.5)
            if st.button("Enviar Calificación Pasajero"):
                idx_luis = df[df["ID"] == 101].index[0]
                st.session_state.df_conductores.at[idx_luis, "Calificación Pasajeros"] = round((st.session_state.df_conductores.at[idx_luis, "Calificación Pasajeros"] + rating_slider) / 2, 2)
                st.success("¡Nota procesada al instante!")
                st.rerun()

# ------------------------------------------------------------------
# ROL: ADMINISTRADOR (PANEL INTEGRAL MACRO CON BARRA SUPERIOR)
# ------------------------------------------------------------------
elif st.session_state.rol == "Administrador":
    st.title("💼 Panel de Control Corporativo - Administrador MTC / Empresas")
    st.caption("Gestión centralizada de analítica conductual y geolocalización satelital")
    st.markdown("---")
    
    # BARRA DE NAVEGACIÓN SUPERIOR PARA ADMINISTRADOR
    tab_dash, tab_iot, tab_costos = st.tabs(["🎛️ Dashboard Operativo", "📡 Central IoT / Telemetría", "💵 Viabilidad Financiera"])
    
    with tab_dash:
        # Módulo de métricas de alto nivel
        st.markdown("### 📊 KPIs de Seguridad Vial de la Flota")
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1: st.metric(label="Reducción Proyectada de Siniestros", value="-30%", delta="Meta: -25%")
        with col_m2: st.metric(label="Score Promedio General Flota", value=f"{int(df['Score Dinámico'].mean())} pts", delta="+49 vs Base")
        with col_m3: st.metric(label="Satisfacción Pasajero Promedio", value=f"{df['Calificación Pasajeros'].mean():.2f} / 5.0")
        with col_m4: st.metric(label="Buses Operando Activos", value=f"{len(df[df['Nivel']=='ALTO'])} / {len(df)}", delta="Bajo control")
        
        st.markdown("---")
        st.markdown("### 🗺️ Rastreo por Satélite en Tiempo Real (GPS Tracking)")
        st.map(df, latitude="latitude", longitude="longitude", size=40)
        st.markdown("---")
        
        # Filtros de las rutas piloto en Lima Metropolitana
        rutas_sel = st.multiselect("Filtrar por Corredor Vial Activo:", options=df["Ruta"].unique(), default=df["Ruta"].unique())
        df_filtrado_admin = df[df["Ruta"].isin(rutas_sel)]
        
        c_adm1, c_adm2 = st.columns([2, 1])
        with c_adm1:
            st.markdown("### 📋 Tabla de Control y Auditoría de Conductores")
            st.dataframe(df_filtrado_admin.style.background_gradient(cmap="summer", subset=["Score Dinámico", "Calificación Pasajeros"]), use_container_width=True)
        with c_adm2:
            st.markdown("### 🎯 Segmentación de Flota por Niveles")
            fig_pie_admin = px.pie(df_filtrado_admin, names='Nivel', values='Score Dinámico', color='Nivel',
                                   color_discrete_map={'ALTO': '#00F5D4', 'MEDIO': '#F59E0B', 'BAJO': '#EF4444'}, hole=0.3)
            fig_pie_admin.update_layout(height=280, margin=dict(t=10,b=10,l=10,r=10))
            st.plotly_chart(fig_pie_admin, use_container_width=True)

    with tab_iot:
        st.markdown("### 📡 Consola de Simulación Telemétrica de Dispositivos en Buses")
        st.markdown("Pruebe el procesamiento de alertas del algoritmo conductual inyectando incidencias en ruta.")
        st.markdown("---")
        
        col_iot1, col_iot2 = st.columns(2)
        with col_iot1:
            st.markdown("#### 📥 Registrar Incidencia del Bus")
            chofer_sel_iot = st.selectbox("Seleccionar Conductor Asignado:", df["Conductor"])
            frenadas_input = st.number_input("Eventos de Frenado Brusco (Sensor G):", min_value=0, max_value=10, value=0)
            velocidad_input = st.number_input("Infracciones por Exceso de Velocidad (GPS):", min_value=0, max_value=5, value=0)
            pasajero_input = st.slider("Calificación promedio del viaje finalizado:", 1.0, 5.0, 5.0, step=0.1)
            
            if st.button("🚀 Inyectar Datos Telemétricos"):
                idx_iot = df[df["Conductor"] == chofer_sel_iot].index[0]
                penalidad = (frenadas_input * 10) + (velocidad_input * 15)
                score_viaje_nuevo = max(0, min(200, 150 - penalidad + int(pasajero_input * 10)))
                
                # Modificar base en Session State
                st.session_state.df_conductores.at[idx_iot, "Viajes Completados"] += 1
                st.session_state.df_conductores.at[idx_iot, "Frenadas Bruscas"] += frenadas_input
                st.session_state.df_conductores.at[idx_iot, "Excesos Velocidad"] += velocidad_input
                st.session_state.df_conductores.at[idx_iot, "Calificación Pasajeros"] = round((st.session_state.df_conductores.at[idx_iot, "Calificación Pasajeros"] + pasajero_input)/2, 2)
                st.session_state.df_conductores.at[idx_iot, "latitude"] += np.random.uniform(-0.002, 0.002)
                st.session_state.df_conductores.at[idx_iot, "longitude"] += np.random.uniform(-0.002, 0.002)
                
                score_total_act = int((st.session_state.df_conductores.at[idx_iot, "Score Dinámico"] + score_viaje_nuevo) / 2)
                st.session_state.df_conductores.at[idx_iot, "Score Dinámico"] = min(200, max(0, score_total_act))
                
                st.success(f"¡Datos de {chofer_sel_iot} procesados! Re-calculando activos conductuales...")
                st.rerun()
                
        with col_iot2:
            st.markdown("#### 🔍 Estado de Auditoría de Incentivos")
            idx_aud = df[df["Conductor"] == chofer_sel_iot].index[0]
            info_aud = df.iloc[idx_aud]
            st.write(f"**Chofer:** {info_aud['Conductor']} | **Puntaje Histórico:** `{info_aud['Score Dinámico']} / 200 pts`")
            
            if info_aud["Nivel"] == "ALTO":
                st.markdown("<div class='card-beneficio'>🏆 Nivel ALTO verificado. Beneficios y subsidios habilitados en la base del MTC.</div>", unsafe_allow_html=True)
            elif info_aud["Nivel"] == "MEDIO":
                st.markdown("<div class='card-beneficio' style='border-left-color: #F59E0B;'>⚠️ Nivel MEDIO. Rendimiento estable, restringido de bonos mayores de combustibles.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='card-beneficio' style='border-left-color: #EF4444;'>🚨 Nivel BAJO. Alerta de riesgo vial emitida a la central corporativa.</div>", unsafe_allow_html=True)

    with tab_costos:
        st.markdown("### 📊 Viabilidad Económica y Finanzas del Proyecto Piloto")
        st.markdown("---")
        c_c1, c_c2 = st.columns(2)
        with c_c1:
            st.markdown("#### 📈 Matriz de Inversión Inicial (50 Unidades / 6 Meses)")
            presupuesto_data = {
                "Concepto Operativo": ["Hardware IoT (Cámaras + Rastreador)", "Desarrollo MVP Móvil React Native", "Infraestructura Cloud Servidores", "Equipo de Monitoreo Técnico"],
                "Monto Requerido (USD)": [25000, 15000, 5000, 10000]
            }
            st.table(pd.DataFrame(presupuesto_data))
            st.metric(label="Inversión Consolidada del Piloto", value="US$ 55,000")
        with c_c2:
            st.markdown("#### 💸 Estructura de Captación de Ingresos")
            fig_bar_adm = px.bar(x=["Suscripción de Líneas", "Subsidios de Entidades", "Brecha Financiera"], y=[12000, 20000, 23000], title="Financiamiento del Modelo SaaS", color_discrete_sequence=['#00F5D4'])
            fig_bar_adm.update_layout(height=260)
            st.plotly_chart(fig_bar_adm, use_container_width=True)
