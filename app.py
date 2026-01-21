import streamlit as st
import time
import random
import os
from datetime import date
import gspread
import json

# --- 1. CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="Le Royaume des Savoirs", layout="wide", page_icon="🗺️")

# Imagen del Mapa del Reino
mapa_url = "https://images.unsplash.com/photo-1580136608260-42d1c4aa7fbb?q=80&w=2000&auto=format&fit=crop"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Quicksand:wght@400;600&display=swap');
    
    .stApp {{
        background-color: #1a1a1a;
        color: white;
    }}

    /* Contenedor del Mapa Interactivo */
    .map-container {{
        position: relative;
        width: 100%;
        max-width: 900px;
        margin: auto;
        border: 10px solid #8b4513;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 0 50px rgba(0,0,0,0.8);
    }}
    
    .map-image {{
        width: 100%;
        display: block;
        opacity: 0.8;
    }}

    /* Estilo de los Puntos de Interés (Pins) */
    .map-pin {{
        position: absolute;
        width: 40px;
        height: 40px;
        background: rgba(252, 211, 77, 0.9);
        border: 3px solid #8b4513;
        border-radius: 50%;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        transition: 0.3s;
        box-shadow: 0 0 15px #fcd34d;
    }}
    .map-pin:hover {{
        transform: scale(1.3);
        background: #fcd34d;
        z-index: 10;
    }}

    /* Pergamino */
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

# --- 2. ESTADO DEL JUEGO ---
if 'user' not in st.session_state:
    st.session_state.user = {
        'nombre': 'Apprenti', 'xp': 0, 'monedas': 100, 'view': 'Home', 
        'reino_actual': None, 'inventario': [], 'last_login': None,
        'setup_complete': False
    }

# Asegurar claves
for key in ['reino_actual', 'setup_complete']:
    if key not in st.session_state.user: st.session_state.user[key] = None

def reward(xp, coins):
    st.session_state.user['xp'] += xp
    st.session_state.user['monedas'] += coins
    return xp, coins

# --- 3. COMPONENTE MAPA INTERACTIVO ---
def mostrar_mapa():
    st.markdown("<h2 class='fancy-title'>Carte des Royaumes</h2>", unsafe_allow_html=True)
    st.write("Haz clic en los iconos para viajar a cada reino:")

    # HTML del Mapa con botones posicionados absolutamente
    # Ajustamos las coordenadas % para que coincidan con zonas de la imagen
    mapa_html = f"""
    <div class="map-container">
        <img src="{mapa_url}" class="map-image">
        <div class="map-pin" style="top: 20%; left: 30%;" title="Valle Matemático">🔢</div>
        <div class="map-pin" style="top: 50%; left: 70%;" title="Reino Francés">🇫🇷</div>
        <div class="map-pin" style="top: 70%; left: 20%;" title="Laboratorio Alquimia">🧪</div>
        <div class="map-pin" style="top: 30%; left: 80%;" title="Templo Musical">🎶</div>
    </div>
    """
    st.markdown(mapa_html, unsafe_allow_html=True)

    # Botones reales de Streamlit para la lógica (el usuario hace clic aquí abajo por ahora)
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("🔢 Matemáticas"): st.session_state.user['reino_actual'] = "Mates"
    if c2.button("🇫🇷 Francés"): st.session_state.user['reino_actual'] = "Frances"
    if c3.button("🧪 Ciencias"): st.session_state.user['reino_actual'] = "Ciencias"
    if c4.button("🎶 Música"): st.session_state.user['reino_actual'] = "Musica"

# --- 4. VISTAS ---
if not st.session_state.user['setup_complete']:
    st.markdown("<div class='parchment'><h1 style='text-align:center;'>Bienvenue</h1>", unsafe_allow_html=True)
    st.session_state.user['nombre'] = st.text_input("Comment t'appelles-tu, voyageur ?")
    if st.button("Lancer l'aventure ⚔️"):
        st.session_state.user['setup_complete'] = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    menu = st.tabs(["🏠 Foyer", "🗺️ Mapa", "📜 Journal", "💎 Boutique"])

    with menu[0]: # HOME
        st.markdown(f"<h1 class='fancy-title'>Bonjour, {st.session_state.user['nombre']}</h1>", unsafe_allow_html=True)
        st.write(f"✨ XP: {st.session_state.user['xp']} | 🪙 Monedas: {st.session_state.user['monedas']}")
        # Mostrar Dragón aquí

    with menu[1]: # MAPA
        mostrar_mapa()
        st.markdown("---")
        if st.session_state.user['reino_actual'] == "Mates":
            st.markdown("<div class='parchment'><h3>🔢 Reto Matemático</h3>", unsafe_allow_html=True)
            res = st.number_input("¿Cuánto es 12 x 4?", step=1)
            if st.button("Verificar"):
                if res == 48: 
                    reward(30, 20)
                    st.success("¡Excelente!")
            st.markdown("</div>", unsafe_allow_html=True)
            
        elif st.session_state.user['reino_actual'] == "Frances":
            st.markdown("<div class='parchment'><h3>🇫🇷 Reto de Francés</h3>", unsafe_allow_html=True)
            res = st.text_input("¿Cómo se dice 'Hola'?")
            if st.button("Valider"):
                if res.lower() == "bonjour": 
                    reward(30, 20)
                    st.success("Bravo !")
            st.markdown("</div>", unsafe_allow_html=True)

    with menu[2]: # JOURNAL
        st.markdown('<div class="parchment">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>📜 Parchemin Royal</h2>", unsafe_allow_html=True)
        sent = st.select_slider("Ton moral", ["😞", "😐", "🙂", "🤩"])
        succ = st.text_area("Ma victoire du jour...")
        fail = st.text_area("Mon défi...")
        if st.button("Sceller 🖋️"):
            if succ and fail:
                xp_g, co_g = reward(40, 10)
                data = [st.session_state.user['nombre'], str(date.today()), sent, succ, fail, "", "", xp_g, co_g]
                if save_to_sheets(data): st.success("Guardado en el Excel real.")
        st.markdown("</div>", unsafe_allow_html=True)

    with menu[3]: # BOUTIQUE
        st.info("Próximamente más armas legendarias...")
