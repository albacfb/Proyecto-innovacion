import streamlit as st
import time
import random
import os
from datetime import date
import gspread
import json
from PIL import Image

# --- 1. CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="Le Royaume des Savoirs", layout="wide", page_icon="🗺️")

MAPA_IMAGEN_PATH = "mapa_reinos.png" 
fondo_general_url = "https://images.unsplash.com/photo-1599408162172-19bc30f65839?q=80&w=2070&auto=format&fit=crop"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Quicksand:wght@400;600&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{fondo_general_url}');
        background-size: cover; background-position: center; background-attachment: fixed;
        color: white;
    }}

    .map-container {{
        position: relative;
        width: 100%;
        max-width: 900px;
        margin: 20px auto;
        border: 10px solid #8b4513;
        border-radius: 15px;
        box-shadow: 0 0 50px rgba(0,0,0,0.8);
        overflow: hidden;
    }}
    
    .map-dragon-icon {{
        position: absolute;
        width: 60px;
        height: 60px;
        background-image: url("https://cdn-icons-png.flaticon.com/512/3069/3069418.png");
        background-size: cover;
        transform: translate(-50%, -50%);
        transition: left 1s ease-in-out, top 1s ease-in-out;
        filter: drop-shadow(0 0 10px #fcd34d);
        z-index: 100;
    }}

    .parchment {{
        background: #fdf5e6;
        background-image: url("https://www.transparenttextures.com/patterns/old-paper.png");
        padding: 30px; border-radius: 10px; border: 4px solid #8b4513;
        color: #3e2723; font-family: 'Quicksand', sans-serif;
    }}
    
    .fancy-title {{ font-family: 'Cinzel', serif; color: #fcd34d !important; text-shadow: 2px 2px 10px #000; text-align: center; }}
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

# --- 2. ESTADO DEL JUEGO (REFORZADO CONTRA KEYERROR) ---
if 'user' not in st.session_state:
    st.session_state.user = {
        'nombre': 'Apprenti', 'xp': 0, 'monedas': 100, 'view': 'Home', 
        'reino_actual': None, 'inventario': [], 'last_login': None,
        'setup_complete': False,
        'dragon_pos_x': '50%', 
        'dragon_pos_y': '50%'
    }

# ESTA PARTE ARREGLA TU ERROR: Si faltan las coordenadas las crea sobre la marcha
def check_user_integrity():
    keys_needed = {
        'dragon_pos_x': '50%',
        'dragon_pos_y': '50%',
        'reino_actual': None,
        'setup_complete': False,
        'xp': 0,
        'monedas': 100
    }
    for key, default in keys_needed.items():
        if key not in st.session_state.user:
            st.session_state.user[key] = default

check_user_integrity()

def reward(xp, coins):
    st.session_state.user['xp'] += xp
    st.session_state.user['monedas'] += coins
    return xp, coins

# --- 3. FUNCIONES DE REINOS ---
def valle_mates():
    st.markdown("<div class='parchment'><h3>🔢 Valle Matemático</h3><p>Calcula rápido:</p>", unsafe_allow_html=True)
    n1, n2 = random.randint(2, 12), random.randint(2, 10)
    ans = st.number_input(f"¿Cuánto es {n1} x {n2}?", step=1, key="math_input")
    if st.button("Lanzar Hechizo"):
        if ans == n1 * n2:
            xp, co = reward(30, 15)
            st.success(f"¡Hechizo certero! +{xp} XP")
        else: st.error("Magia fallida...")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 4. MAPA INTERACTIVO ---
def mostrar_mapa_interactivo():
    st.markdown("<h2 class='fancy-title'>Carte des Royaumes</h2>", unsafe_allow_html=True)
    
    posiciones = {
        "Mates": {'x': '28%', 'y': '25%'},
        "Frances": {'x': '75%', 'y': '22%'},
        "Ciencias": {'x': '28%', 'y': '70%'},
        "Musica": {'x': '72%', 'y': '65%'}
    }

    # Intentar mostrar el mapa (usamos una URL directa si el archivo local falla para que no de error)
    # Reemplaza 'TU_USUARIO' y 'TU_REPO' por tus datos reales de GitHub
    url_github_mapa = "https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/mapa_reinos.png"

    st.markdown(f"""
    <div class="map-container">
        <img src="{url_github_mapa}" style="width:100%;" onerror="this.src='https://images.unsplash.com/photo-1580136608260-42d1c4aa7fbb?q=80&w=1000&auto=format&fit=crop'">
        <div class="map-dragon-icon" style="left: {st.session_state.user['dragon_pos_x']}; top: {st.session_state.user['dragon_pos_y']};"></div>
    </div>
    """, unsafe_allow_html=True)

    st.write("Selecciona tu destino:")
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("🔢 Valle Mates"):
        st.session_state.user['reino_actual'] = "Mates"
        st.session_state.user['dragon_pos_x'], st.session_state.user['dragon_pos_y'] = posiciones["Mates"]['x'], posiciones["Mates"]['y']
        st.rerun()
    if c2.button("🇫🇷 Royaume Français"):
        st.session_state.user['reino_actual'] = "Frances"
        st.session_state.user['dragon_pos_x'], st.session_state.user['dragon_pos_y'] = posiciones["Frances"]['x'], posiciones["Frances"]['y']
        st.rerun()
    if c3.button("🧪 Labo Alchimie"):
        st.session_state.user['reino_actual'] = "Ciencias"
        st.session_state.user['dragon_pos_x'], st.session_state.user['dragon_pos_y'] = posiciones["Ciencias"]['x'], posiciones["Ciencias"]['y']
        st.rerun()
    if c4.button("🎶 Temple Musique"):
        st.session_state.user['reino_actual'] = "Musica"
        st.session_state.user['dragon_pos_x'], st.session_state.user['dragon_pos_y'] = posiciones["Musica"]['x'], posiciones["Musica"]['y']
        st.rerun()

    if st.session_state.user['reino_actual'] == "Mates": valle_mates()

# --- 5. LOGICA PRINCIPAL ---
if not st.session_state.user['setup_complete']:
    st.markdown("<div class='parchment'><h1>Bienvenue</h1>", unsafe_allow_html=True)
    st.session_state.user['nombre'] = st.text_input("Comment t'appelles-tu ?")
    if st.button("Commencer ⚔️"):
        st.session_state.user['setup_complete'] = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
else:
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Foyer", "🗺️ Carte", "📜 Journal", "💎 Boutique"])
    
    with tab1:
        st.markdown(f"<h1 class='fancy-title'>Bonjour, {st.session_state.user['nombre']}</h1>", unsafe_allow_html=True)
        st.write(f"✨ XP: {st.session_state.user['xp']} | 🪙 Or: {st.session_state.user['monedas']}")
        st.image("https://cdn-icons-png.flaticon.com/512/3069/3069418.png", width=150)

    with tab2:
        mostrar_mapa_interactivo()

    with tab3:
        st.markdown('<div class="parchment"><h2>📜 Journal de Bord</h2>', unsafe_allow_html=True)
        sent = st.select_slider("Moral", ["😞", "😐", "🙂", "🤩"])
        succ = st.text_area("Succès du jour")
        if st.button("Sceller 🖋️"):
            if succ:
                reward(40, 10)
                save_to_sheets([st.session_state.user['nombre'], str(date.today()), sent, succ])
                st.success("C'est fait !")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab4:
        st.markdown("<div class='parchment'><h2>💎 Boutique Royale</h2>", unsafe_allow_html=True)
        st.write("Bientôt de nuevos objetos...")
        st.markdown("</div>", unsafe_allow_html=True)
