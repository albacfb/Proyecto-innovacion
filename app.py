import streamlit as st
import time
from datetime import datetime

# --- 1. CONFIGURACIÓN E INYECCIÓN CSS (ESTILO APP MÓVIL TOTAL) ---
st.set_page_config(page_title="Mon Dragon Français", layout="centered", page_icon="🐉")

# Definimos colores según el elemento elegido (se aplicarán dinámicamente)
TEMAS = {
    "Fuego": {"bg": "#FFF5F5", "accent": "#FF6B6B", "gradient": "linear-gradient(135deg, #FF9A9E 0%, #FECFEF 100%)", "icon": "🔥"},
    "Agua":  {"bg": "#F0F8FF", "accent": "#4FACFE", "gradient": "linear-gradient(135deg, #43E97B 0%, #38F9D7 100%)", "icon": "💧"},
    "Naturaleza": {"bg": "#F1F8E9", "accent": "#66BB6A", "gradient": "linear-gradient(135deg, #a8e6cf 0%, #dcedc1 100%)", "icon": "🌿"}
}

st.markdown("""
    <style>
    /* RESET GENERAL */
    .stApp {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* BARRA DE PROGRESO (XP) */
    .xp-container {
        width: 100%;
        background-color: #E0E0E0;
        border-radius: 10px;
        margin: 10px 0;
        height: 10px;
        overflow: hidden;
    }
    .xp-bar {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    /* EL CÍRCULO DEL DRAGÓN (TIPO MUSA) */
    .dragon-circle {
        width: 240px;
        height: 240px;
        border-radius: 50%;
        margin: 20px auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        border: 8px solid white;
        background: white;
        position: relative;
        transition: all 0.5s ease;
    }
    
    /* TARJETAS INTERACTIVAS */
    .stat-card {
        background: white;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        text-align: center;
        border: 1px solid #f0f0f0;
    }
    
    /* MENÚ DOCK INFERIOR */
    .dock {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: white;
        padding: 15px 0;
        box-shadow: 0 -5px 20px rgba(0,0,0,0.05);
        display: flex;
        justify-content: space-around;
        z-index: 999;
        border-top: 1px solid #eee;
    }
    
    /* OCULTAR ELEMENTOS NATIVOS */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display:none;}
    </style>
""", unsafe_allow_html=True)

# --- 2. GESTIÓN DE ESTADO (MEMORIA ROBUSTA) ---
# Aquí guardamos todo: tipo de dragón, nivel, XP, y estadísticas de Input/Output
if 'user' not in st.session_state:
    st.session_state.user = {}

valores_por_defecto = {
    'setup_complete': False,
    'nombre': 'Apprenti',
    'elemento': 'Fuego', # Por defecto, se cambia en el onboarding
    'nivel': 1,
    'xp': 0,
    'xp_next': 50,
    'stats': {'input': 0, 'output': 0}, # Input = Sabiduría, Output = Fuerza
    'fase_actual': 'Éveil',
    'historial': [],
    'view': 'Home'
}

for key, val in valores_por_defecto.items():
    if key not in st.session_state.user:
        st.session_state.user[key] = val

# --- 3. BIBLIOTECA DE IMÁGENES DINÁMICAS ---
# Las imágenes cambian según ELEMENTO (Fuego/Agua) y FASE (Dormido/Volando)
ASSETS = {
    "Fuego": {
        "Éveil": "https://cdn-icons-png.flaticon.com/512/7880/7880228.png", # Huevo Rojo
        "Expansion": "https://cdn-icons-png.flaticon.com/512/1625/1625348.png", # Dragón Rojo Volando
        "Repli": "https://cdn-icons-png.flaticon.com/512/7880/7880228.png", # Huevo/Descanso
        "Renouveau": "https://cdn-icons-png.flaticon.com/512/4699/4699313.png" # Dragón Rojo Poderoso
    },
    "Agua": {
        "Éveil": "https://cdn-icons-png.flaticon.com/512/7880/7880222.png", # Huevo Azul
        "Expansion": "https://cdn-icons-png.flaticon.com/512/3093/3093608.png", # Dragón Azul Nadando
        "Repli": "https://cdn-icons-png.flaticon.com/512/7880/7880222.png", 
        "Renouveau": "https://cdn-icons-png.flaticon.com/512/4699/4699298.png"
    },
    "Naturaleza": {
        "Éveil": "https://cdn-icons-png.flaticon.com/512/7880/7880233.png", # Huevo Verde
        "Expansion": "https://cdn-icons-png.flaticon.com/512/3715/3715097.png", # Dragón Verde Volando
        "Repli": "https://cdn-icons-png.flaticon.com/512/7880/7880233.png", 
        "Renouveau": "https://cdn-icons-png.flaticon.com/512/4699/4699276.png"
    }
}

# --- 4. ONBOARDING (PRIMERA VEZ) ---
if not st.session_state.user['setup_complete']:
    st.title("🥚 Elige tu Compañero")
    st.write("Tu dragón evolucionará según cómo aprendas francés.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image(ASSETS["Fuego"]["Éveil"], width=80)
        if st.button("Fuego (Pasión)"):
            st.session_state.user['elemento'] = "Fuego"
            st.session_state.user['setup_complete'] = True
            st.rerun()
            
    with col2:
        st.image(ASSETS["Agua"]["Éveil"], width=80)
        if st.button("Agua (Calma)"):
            st.session_state.user['elemento'] = "Agua"
            st.session_state.user['setup_complete'] = True
            st.rerun()
            
    with col3:
        st.image(ASSETS["Naturaleza"]["Éveil"], width=80)
        if st.button("Tierra (Fuerza)"):
            st.session_state.user['elemento'] = "Naturaleza"
            st.session_state.user['setup_complete'] = True
            st.rerun()

# --- 5. APP PRINCIPAL ---
else:
    # Recuperamos tema visual del usuario
    tema = TEMAS[st.session_state.user['elemento']]
    
    # Inyectamos el color de fondo personalizado
    st.markdown(f"""
        <style>
        .stApp {{ background-color: {tema['bg']}; }}
        .xp-bar {{ background: {tema['gradient']}; width: {(st.session_state.user['xp'] / st.session_state.user['xp_next']) * 100}%; }}
        .dragon-circle {{ background: {tema['gradient']}; }}
        h1, h2, h3 {{ color: {tema['accent']}; }}
        </style>
    """, unsafe_allow_html=True)

    # --- VISTA: HOME (EL CICLO) ---
    if st.session_state.user['view'] == 'Home':
        
        # 1. BARRA DE NIVEL Y XP
        st.markdown(f"**Niveau {st.session_state.user['nivel']}** <span style='float:right; color:gray; font-size:0.8em;'>{st.session_state.user['xp']} / {st.session_state.user['xp_next']} XP</span>", unsafe_allow_html=True)
        st.markdown('<div class="xp-container"><div class="xp-bar"></div></div>', unsafe_allow_html=True)
        
        # 2. EL CÍRCULO DEL DRAGÓN
        fase = st.session_state.user['fase_actual']
        img_url = ASSETS[st.session_state.user['elemento']][fase]
        
        st.markdown(f"""
            <div class="dragon-circle">
                <img src="{img_url}" width="140" style="filter: drop-shadow(0 5px 5px rgba(0,0,0,0.2)); transition: transform 0.3s;">
                <p style="color: white; margin-top: 10px; font-weight: bold; text-shadow: 0 1px 3px rgba(0,0,0,0.3);">{fase}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # 3. FEEDBACK EVOLUTIVO (INPUT vs OUTPUT)
        input_cnt = st.session_state.user['stats']['input']
        output_cnt = st.session_state.user['stats']['output']
        
        mensaje_evolucion = "Tu dragón es joven y equilibrado."
        if input_cnt > output_cnt + 2:
            mensaje_evolucion = "👁️ Tu dragón tiene una **mirada profunda**. (Gran Comprensión)"
        elif output_cnt > input_cnt + 2:
            mensaje_evolucion = "🔥 Tu dragón tiene **alas fuertes**. (Gran Expresión)"
            
        st.info(f"💡 {mensaje_evolucion}")
        
        # Botón de Registro Rápido
        st.write("")
        if st.button("➕ Registrar Progreso Hoy", type="primary", use_container_width=True):
            st.session_state.user['view'] = 'Registro'
            st.rerun()

    # --- VISTA: REGISTRO (CHECK-IN) ---
    elif st.session_state.user['view'] == 'Registro':
        st.title("Check-in 📝")
        st.markdown("¿Qué has entrenado hoy?")
        
        with st.form("training_form"):
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("### 📥 Input")
                st.caption("(Escuchar, Leer)")
                inputs = st.multiselect("He...", ["Música Francés", "Serie/Video", "Lectura", "Escucha Activa"], key="in")
            
            with col_b:
                st.markdown("### 📤 Output")
                st.caption("(Hablar, Escribir)")
                outputs = st.multiselect("He...", ["Hablar en clase", "Grabar audio", "Escribir texto", "Pronunciación"], key="out")
            
            st.markdown("---")
            animo = st.select_slider("Energía de hoy:", options=["😴 Baja", "😐 Normal", "⚡ Alta"])
            
            submit = st.form_submit_button("Guardar y Evolucionar", use_container_width=True)
            
            if submit:
                # 1. CÁLCULO DE XP
                xp_ganada = (len(inputs) * 10) + (len(outputs) * 15) + 5
                st.session_state.user['xp'] += xp_ganada
                
                # 2. ACTUALIZAR STATS (Para la forma del dragón)
                st.session_state.user['stats']['input'] += len(inputs)
                st.session_state.user['stats']['output'] += len(outputs)
                
                # 3. DETERMINAR FASE DEL CICLO
                nueva_fase = "Éveil"
                if animo == "😴 Baja":
                    nueva_fase = "Repli" # Descanso
                elif len(outputs) > 0 and animo == "⚡ Alta":
                    nueva_fase = "Expansion" # Acción
                elif len(inputs) > 0:
                    nueva_fase = "Renouveau" # Integración
                
                st.session_state.user['fase_actual'] = nueva_fase
                
                # 4. SUBIDA DE NIVEL
                if st.session_state.user['xp'] >= st.session_state.user['xp_next']:
                    st.session_state.user['nivel'] += 1
                    st.session_state.user['xp'] = 0
                    st.session_state.user['xp_next'] = int(st.session_state.user['xp_next'] * 1.2) # Cada vez cuesta más
                    st.balloons()
                    st.success(f"¡NIVEL {st.session_state.user['nivel']} ALCANZADO!")
                    time.sleep(2)
                
                st.success(f"+{xp_ganada} XP | Fase: {nueva_fase}")
                time.sleep(1)
                st.session_state.user['view'] = 'Home'
                st.rerun()
                
        if st.button("Cancelar"):
            st.session_state.user['view'] = 'Home'
            st.rerun()

    # --- VISTA: PERFIL/GALERÍA ---
    elif st.session_state.user['view'] == 'Perfil':
        st.title("ADN de Dragón 🧬")
        
        # Estadísticas visuales
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Sabiduría (Input)", st.session_state.user['stats']['input'])
        with c2:
            st.metric("Fuerza (Output)", st.session_state.user['stats']['output'])
            
        st.markdown("### Tu Evolución Actual")
        # Mostramos las 4 fases de SU dragón (personalizado)
        cols = st.columns(4)
        phases_list = ["Éveil", "Expansion", "Repli", "Renouveau"]
        
        for i, p in enumerate(phases_list):
            opacity = "1.0" if p == st.session_state.user['fase_actual'] else "0.4"
            border = f"2px solid {tema['accent']}" if p == st.session_state.user['fase_actual'] else "none"
            
            with cols[i]:
                st.image(ASSETS[st.session_state.user['elemento']][p], use_container_width=True)
                st.markdown(f"<p style='text-align:center; font-size:0.8em; opacity:{opacity}; font-weight:bold;'>{p}</p>", unsafe_allow_html=True)

    # --- MENÚ DOCK INFERIOR ---
    st.write("<br><br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🏠 Dragón"):
            st.session_state.user['view'] = 'Home'
            st.rerun()
    with c2:
        if st.button("➕ Entrenar"):
            st.session_state.user['view'] = 'Registro'
            st.rerun()
    with c3:
        if st.button("🧬 ADN"):
            st.session_state.user['view'] = 'Perfil'
            st.rerun()