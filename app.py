import streamlit as st
import time
import random
import os
from datetime import date
import gspread
import json

# --- 1. CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="Le Royaume des Savoirs", layout="wide", page_icon="🐉")

# Intentar cargar la imagen local, si no, usar una de respaldo
MAPA_LOCAL = "mapa_reinos.png"
if os.path.exists(MAPA_LOCAL):
    # Usamos una técnica de Streamlit para mostrar imágenes locales en HTML
    import base64
    with open(MAPA_LOCAL, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
    mapa_url = f"data:image/png;base64,{encoded}"
else:
    # Imagen de respaldo (Mapa antiguo) para que nunca se vea desconfigurado
    mapa_url = "https://images.unsplash.com/photo-1580136608260-42d1c4aa7fbb?q=80&w=1000"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Quicksand:wght@400;600&display=swap');
    
    .stApp {{
        background-color: #1a1a1a;
        color: white;
    }}

    /* Contenedor del Mapa */
    .map-container {{
        position: relative;
        width: 100%;
        max-width: 800px;
        margin: 20px auto;
        border: 8px solid #8b4513;
        border-radius: 15px;
        box-shadow: 0 0 30px rgba(0,0,0,0.7);
        overflow: hidden;
        background-color: #2a2a2a;
    }}
    
    .map-img-bg {{
        width: 100%;
        display: block;
    }}

    .map-dragon-icon {{
        position: absolute;
        width: 50px;
        height: 50px;
        background-image: url("https://cdn-icons-png.flaticon.com/512/3069/3069418.png");
        background-size: cover;
        transform: translate(-50%, -50%);
        transition: all 1s ease-in-out;
        z-index: 10;
        filter: drop-shadow(0 0 10px gold);
    }}

    .parchment {{
        background: #fdf5e6;
        background-image: url("https://www.transparenttextures.com/patterns/old-paper.png");
        padding: 25px; border-radius: 10px; border: 4px solid #8b4513;
        color: #3e2723; font-family: 'Quicksand', sans-serif;
        margin-bottom: 20px;
    }}
    
    .fancy-title {{ font-family: 'Cinzel', serif; color: #fcd34d !important; text-align: center; }}
    </style>
""", unsafe_allow_html=True)

# --- 2. ESTADO DEL JUEGO ---
if 'user' not in st.session_state:
    st.session_state.user = {
        'nombre': 'Apprenti', 'xp': 0, 'monedas': 100, 'view': 'Home', 
        'reino_actual': None, 'inventario': [], 'setup_complete': False,
        'dragon_pos_x': '50%', 'dragon_pos_y': '50%'
    }

# Asegurar integridad
for k, v in {'dragon_pos_x': '50%', 'dragon_pos_y': '50%', 'reino_actual': None}.items():
    if k not in st.session_state.user: st.session_state.user[k] = v

def reward(xp, coins):
    st.session_state.user['xp'] += xp
    st.session_state.user['monedas'] += coins

# --- 3. COMPONENTES ---
def mostrar_mapa():
    st.markdown("<h2 class='fancy-title'>Carte des Royaumes</h2>", unsafe_allow_html=True)
    
    posiciones = {
        "Mates": {'x': '22%', 'y': '28%'},
        "Frances": {'x': '78%', 'y': '25%'},
        "Ciencias": {'x': '25%', 'y': '72%'},
        "Musica": {'x': '68%', 'y': '75%'}
    }

    # Renderizado del mapa
    st.markdown(f"""
    <div class="map-container">
        <img src="{mapa_url}" class="map-img-bg">
        <div class="map-dragon-icon" style="left: {st.session_state.user['dragon_pos_x']}; top: {st.session_state.user['dragon_pos_y']};"></div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    if c1.button("🔢 Mates"):
        st.session_state.user['reino_actual'] = "Mates"
        st.session_state.user['dragon_pos_x'], st.session_state.user['dragon_pos_y'] = posiciones["Mates"]['x'], posiciones["Mates"]['y']
        st.rerun()
    if c2.button("🇫🇷 Français"):
        st.session_state.user['reino_actual'] = "Frances"
        st.session_state.user['dragon_pos_x'], st.session_state.user['dragon_pos_y'] = posiciones["Frances"]['x'], posiciones["Frances"]['y']
        st.rerun()
    if c3.button("🧪 Sciences"):
        st.session_state.user['reino_actual'] = "Ciencias"
        st.session_state.user['dragon_pos_x'], st.session_state.user['dragon_pos_y'] = posiciones["Ciencias"]['x'], posiciones["Ciencias"]['y']
        st.rerun()
    if c4.button("🎶 Musique"):
        st.session_state.user['reino_actual'] = "Musica"
        st.session_state.user['dragon_pos_x'], st.session_state.user['dragon_pos_y'] = posiciones["Musica"]['x'], posiciones["Musica"]['y']
        st.rerun()

# --- 4. NAVEGACIÓN ---
if not st.session_state.user['setup_complete']:
    st.markdown("<div class='parchment'><h1>Bienvenue</h1>", unsafe_allow_html=True)
    st.session_state.user['nombre'] = st.text_input("Ton nom :")
    if st.button("Commencer ⚔️"):
        st.session_state.user['setup_complete'] = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
else:
    tab1, tab2, tab3 = st.tabs(["🏠 Foyer", "🗺️ Carte", "📜 Journal"])
    
    with tab1:
        st.markdown(f"<h1 class='fancy-title'>Bonjour, {st.session_state.user['nombre']}</h1>", unsafe_allow_html=True)
        st.write(f"✨ XP: {st.session_state.user['xp']} | 🪙 Or: {st.session_state.user['monedas']}")
        st.image("https://cdn-icons-png.flaticon.com/512/3069/3069418.png", width=150)

    with tab2:
        mostrar_mapa()
        if st.session_state.user['reino_actual'] == "Mates":
            st.info("Reto Matemático Activo")
        elif st.session_state.user['reino_actual'] == "Frances":
            st.info("Reto de Francés Activo")

    with tab3:
        st.markdown('<div class="parchment"><h2>📜 Journal</h2>', unsafe_allow_html=True)
        succ = st.text_area("¿Qué has aprendido hoy?")
        if st.button("Enregistrer"):
            reward(40, 10)
            st.success("¡Guardado!")
        st.markdown("</div>", unsafe_allow_html=True)
