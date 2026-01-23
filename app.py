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

# Función para cargar imagen local de forma segura
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

mapa_base64 = get_base64_image("mapa_reinos.png")

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Quicksand:wght@400;600&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://cdn.pixabay.com/photo/2022/11/04/10/24/dragon-7569512_1280.jpg');
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    .map-container {{
        position: relative;
        width: 100%;
        max-width: 800px;
        margin: auto;
        border: 8px solid #8b4513;
        border-radius: 15px;
        min-height: 500px;
        background-color: #2a2a2a;
        {"background-image: url('data:image/png;base64," + mapa_base64 + "');" if mapa_base64 else ""}
        background-size: cover;
        background-position: center;
        box-shadow: 0 0 30px rgba(0,0,0,0.7);
    }}

    .dragon-sprite {{
        position: absolute;
        width: 70px; height: 70px;
        background-size: contain;
        background-repeat: no-repeat;
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
    except Exception as e:
        st.error(f"Erreur de connexion Excel: {e}")
        return False

# --- 2. ESTADO DEL JUEGO ---
if 'user' not in st.session_state:
    st.session_state.user = {
        'nombre': 'Apprenti', 'xp': 0, 'monedas': 100, 'view': 'Home', 
        'setup_complete': False, 'inventario': [], 
        'reino_actual': 'Centro', 'pos_x': '50%', 'pos_y': '50%'
    }

# Asegurar que las coordenadas existan para evitar errores
if 'pos_x' not in st.session_state.user:
    st.session_state.user['pos_x'] = '50%'
    st.session_state.user['pos_y'] = '50%'

# URLs de imágenes ESTABLES (Wikimedia)
IMG_HUEVO = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Dragon_Egg.svg/512px-Dragon_Egg.svg.png"
IMG_BEBE = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Dragon-icon.svg/512px-Dragon-icon.svg.png"

def obtener_imagen_dragon(xp):
    if xp < 100:
        return IMG_HUEVO
    return IMG_BEBE

# --- 3. VISTAS ---
if not st.session_state.user['setup_complete']:
    st.markdown("<div class='glass-panel'><h1 class='fancy-title'>Bienvenue</h1>", unsafe_allow_html=True)
    nombre = st.text_input("Comment t'appelles-tu, voyageur ?")
    if st.button("Lancer l'aventure ⚔️"):
        if nombre:
            st.session_state.user['nombre'] = nombre
            st.session_state.user['setup_complete'] = True
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # Sidebar de Stats
    with st.sidebar:
        st.markdown(f"### 🛡️ {st.session_state.user['nombre']}")
        st.image(obtener_imagen_dragon(st.session_state.user['xp']), width=100)
        st.metric("XP", st.session_state.user['xp'])
        st.metric("Or", st.session_state.user['monedas'])

    tab_home, tab_mapa, tab_journal = st.tabs(["🏠 Foyer", "🗺️ Carte du Royaume", "📜 Journal"])

    with tab_home:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown(f"<h1 class='fancy-title'>Foyer du Dragon</h1>", unsafe_allow_html=True)
        st.image(obtener_imagen_dragon(st.session_state.user['xp']), width=250)
        if st.session_state.user['xp'] < 100:
            st.write("### Ton œuf a besoin de savoirs para éclore !")
            st.progress(st.session_state.user['xp'] / 100)
        else:
            st.write("### Félicitations ! Ton dragon a éclos !")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_mapa:
        st.markdown("<h2 class='fancy-title'>Exploration</h2>", unsafe_allow_html=True)
        
        # Mapa Visual
        img_dragon_mapa = obtener_imagen_dragon(st.session_state.user['xp'])
        st.markdown(f"""
            <div class="map-container">
                <div class="dragon-sprite" style="left: {st.session_state.user['pos_x']}; top: {st.session_state.user['pos_y']}; background-image: url('{img_dragon_mapa}');"></div>
            </div>
        """, unsafe_allow_html=True)

        if not mapa_base64:
            st.warning("⚠️ Sube 'mapa_reinos.png' a GitHub para ver el mapa de fondo.")

        # Botones de navegación
        posiciones = {
            "Mates": {'x': '22%', 'y': '28%'},
            "Frances": {'x': '78%', 'y': '25%'},
            "Ciencias": {'x': '25%', 'y': '72%'},
            "Musica": {'x': '68%', 'y': '75%'}
        }

        cols = st.columns(4)
        if cols[0].button("🔢 Mates"):
            st.session_state.user['reino_actual'] = "Mates"
            st.session_state.user['pos_x'], st.session_state.user['pos_y'] = posiciones["Mates"]['x'], posiciones["Mates"]['y']
            st.rerun()
        if cols[1].button("🇫🇷 Français"):
            st.session_state.user['reino_actual'] = "Frances"
            st.session_state.user['pos_x'], st.session_state.user['pos_y'] = posiciones["Frances"]['x'], posiciones["Frances"]['y']
            st.rerun()
        # ... (puedes añadir los otros botones igual)

    with tab_journal:
        st.markdown('<div class="parchment-box">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>📜 Parchemin de Métacognition</h2>", unsafe_allow_html=True)
        sent = st.select_slider("Moral", ["😞", "😐", "🙂", "🤩"])
        logros = st.text_area("1. ¿Qué objetivos has conseguido hoy?")
        retos = st.text_area("2. ¿Qué ha sido lo más difícil?")
        
        if st.button("Sceller 🖋️"):
            if logros and retos:
                st.session_state.user['xp'] += 40
                data = [st.session_state.user['nombre'], str(date.today()), sent, logros, retos]
                if save_to_sheets(data):
                    st.success("¡Enviado al Maestro!")
                    st.balloons()
            else: st.error("Completa el diario.")
        st.markdown("</div>", unsafe_allow_html=True)
