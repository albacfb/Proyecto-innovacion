import streamlit as st
import time
import random
import os
import json
import base64
from datetime import date
import gspread

# --- 1. CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="Les Dragons de l'Apprentissage", layout="wide", page_icon="🐉")

# Intentar cargar mapa local para el fondo del contenedor
MAPA_LOCAL = "mapa_reinos.png"
mapa_bg = ""
if os.path.exists(MAPA_LOCAL):
    with open(MAPA_LOCAL, "rb") as f:
        mapa_bg = base64.b64encode(f.read()).decode()

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Quicksand:wght@400;600&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://cdn.pixabay.com/photo/2022/11/04/10/24/dragon-7569512_1280.jpg');
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* Contenedor del Mapa */
    .map-container {{
        position: relative;
        width: 100%;
        max-width: 800px;
        margin: auto;
        border: 8px solid #8b4513;
        border-radius: 15px;
        overflow: hidden;
        background: url('data:image/png;base64,{mapa_bg}') center/cover;
        min-height: 500px;
        box-shadow: 0 0 30px rgba(0,0,0,0.7);
    }}

    .dragon-sprite {{
        position: absolute;
        width: 60px; height: 60px;
        background-image: url("https://cdn-icons-png.flaticon.com/512/3069/3069418.png");
        background-size: cover;
        transform: translate(-50%, -50%);
        transition: all 1s ease-in-out;
        z-index: 10;
        filter: drop-shadow(0 0 10px gold);
    }}

    .parchment-box {{
        background: #fdf5e6;
        background-image: url("https://www.transparenttextures.com/patterns/old-paper.png");
        padding: 30px; border-radius: 10px; border: 8px double #8b4513;
        color: #3e2723; font-family: 'Quicksand', sans-serif;
    }}

    .glass-panel {{
        background: rgba(0, 0, 0, 0.7); backdrop-filter: blur(12px);
        border: 2px solid #fcd34d; border-radius: 20px; padding: 20px; color: white;
    }}

    .fancy-title {{ font-family: 'Cinzel', serif; color: #fcd34d !important; text-align: center; }}
    </style>
""", unsafe_allow_html=True)

# --- CONEXIÓN A GOOGLE SHEETS ---
def save_to_sheets(data):
    try:
        creds_raw = st.secrets["google_sheets_creds"]
        creds_info = json.loads(creds_raw) if isinstance(creds_raw, str) else dict(creds_raw)
        gc = gspread.service_account_from_dict(creds_info)
        sh = gc.open("JournalApprentices").worksheet("JournalEntries")
        sh.append_row(data)
        return True
    except: return False

# --- 2. ESTADO DEL JUEGO ---
if 'user' not in st.session_state:
    st.session_state.user = {
        'nombre': 'Apprenti', 'xp': 0, 'monedas': 100, 'view': 'Home', 
        'setup_complete': False, 'inventario': [], 'last_login': None,
        'reino_actual': 'Centro', 'pos_x': '50%', 'pos_y': '50%'
    }

# Asegurar claves de mapa
for k, v in {'pos_x': '50%', 'pos_y': '50%', 'reino_actual': 'Centro'}.items():
    if k not in st.session_state.user: st.session_state.user[k] = v

posiciones = {
    "Mates": {'x': '22%', 'y': '28%'},
    "Frances": {'x': '78%', 'y': '25%'},
    "Ciencias": {'x': '25%', 'y': '72%'},
    "Musica": {'x': '68%', 'y': '75%'}
}

def reward(xp, coins):
    st.session_state.user['xp'] += xp
    st.session_state.user['monedas'] += coins
    return xp, coins

# --- 3. VISTAS ---
if not st.session_state.user['setup_complete']:
    st.markdown("<div class='glass-panel'><h1 class='fancy-title'>Bienvenue</h1>", unsafe_allow_html=True)
    nombre = st.text_input("Comment t'appelles-tu ?")
    if st.button("Lancer l'aventure ⚔️"):
        st.session_state.user['nombre'] = nombre
        st.session_state.user['setup_complete'] = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # Sidebar de Stats
    with st.sidebar:
        st.markdown(f"### 🛡️ {st.session_state.user['nombre']}")
        st.metric("XP", st.session_state.user['xp'])
        st.metric("Or", st.session_state.user['monedas'])
        st.write("---")
        st.write("**Inventaire:**")
        for item in st.session_state.user['inventario']: st.write(f"- {item}")

    # Pestañas
    tab_home, tab_mapa, tab_journal = st.tabs(["🏠 Foyer", "🗺️ Carte du Royaume", "📜 Journal"])

    with tab_home:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown(f"<h1 class='fancy-title'>Foyer du Dragon</h1>", unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/3069/3069418.png", width=200)
        st.write("¡Sigue explorando los reinos para evolucionar!")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_mapa:
        st.markdown("<h2 class='fancy-title'>Exploration Transversale</h2>", unsafe_allow_html=True)
        
        # Mapa Visual con el Dragón
        st.markdown(f"""
            <div class="map-container">
                <div class="dragon-sprite" style="left: {st.session_state.user['pos_x']}; top: {st.session_state.user['pos_y']};"></div>
            </div>
        """, unsafe_allow_html=True)

        cols = st.columns(4)
        if cols[0].button("🔢 Mates"):
            st.session_state.user['reino_actual'] = "Mates"
            st.session_state.user['pos_x'], st.session_state.user['pos_y'] = posiciones["Mates"]['x'], posiciones["Mates"]['y']
            st.rerun()
        if cols[1].button("🇫🇷 Français"):
            st.session_state.user['reino_actual'] = "Frances"
            st.session_state.user['pos_x'], st.session_state.user['pos_y'] = posiciones["Frances"]['x'], posiciones["Frances"]['y']
            st.rerun()
        if cols[2].button("🧪 Sciences"):
            st.session_state.user['reino_actual'] = "Ciencias"
            st.session_state.user['pos_x'], st.session_state.user['pos_y'] = posiciones["Ciencias"]['x'], posiciones["Ciencias"]['y']
            st.rerun()
        if cols[3].button("🎶 Musique"):
            st.session_state.user['reino_actual'] = "Musica"
            st.session_state.user['pos_x'], st.session_state.user['pos_y'] = posiciones["Musica"]['x'], posiciones["Musica"]['y']
            st.rerun()

        if st.session_state.user['reino_actual'] != "Centro":
            st.info(f"📍 Vous êtes dans le royaume: {st.session_state.user['reino_actual']}")

    with tab_journal:
        st.markdown('<div class="parchment-box">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>📜 Parchemin de Métacognition</h2>", unsafe_allow_html=True)
        sent = st.select_slider("Moral", ["😞", "😐", "🙂", "🤩"])
        logros = st.text_area("1. ¿Qué objetivos has conseguido hoy?")
        retos = st.text_area("2. ¿Qué ha sido lo más difícil?")
        mejora = st.text_area("3. ¿Qué podrías mejorar mañana?")
        
        if st.button("Sceller 🖋️"):
            if logros and retos:
                reward(40, 10)
                data = [st.session_state.user['nombre'], str(date.today()), sent, logros, retos, mejora]
                if save_to_sheets(data):
                    st.success("¡Enviado al Maestro!")
                    st.balloons()
            else: st.error("Completa el diario.")
        st.markdown("</div>", unsafe_allow_html=True)
