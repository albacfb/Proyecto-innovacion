import streamlit as st
import time
import os
from datetime import date
import json

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Le Royaume des Savoirs", layout="wide", page_icon="🐉")

MAPA_LOCAL = "mapa_reinos.png"

# --- 2. ESTADO DEL JUEGO ---
if 'user' not in st.session_state:
    st.session_state.user = {
        'nombre': 'Apprenti', 'xp': 0, 'monedas': 100, 
        'reino_actual': None, 'setup_complete': False,
        'dragon_pos_x': '50%', 'dragon_pos_y': '50%'
    }

# Coordenadas de los dibujos en TU mapa
posiciones = {
    "Mates": {'x': '22%', 'y': '28%'},
    "Frances": {'x': '78%', 'y': '25%'},
    "Ciencias": {'x': '25%', 'y': '72%'},
    "Musica": {'x': '68%', 'y': '75%'}
}

# --- 3. ESTILOS CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #1a1a1a; color: white; }}
    
    /* Contenedor del mapa */
    .map-wrapper {{
        position: relative;
        width: 100%;
        max-width: 800px;
        margin: auto;
        border: 5px solid #8b4513;
        border-radius: 15px;
        overflow: hidden;
    }}

    .map-img {{ width: 100%; display: block; }}

    /* El Dragón */
    .dragon-sprite {{
        position: absolute;
        width: 60px; height: 60px;
        background-image: url("https://cdn-icons-png.flaticon.com/512/3069/3069418.png");
        background-size: cover;
        transform: translate(-50%, -50%);
        transition: all 1s ease-in-out;
        z-index: 10;
        pointer-events: none; /* El dragón no bloquea los clics */
        filter: drop-shadow(0 0 10px gold);
    }}

    /* Botones invisibles sobre el mapa */
    .map-area {{
        position: absolute;
        cursor: pointer;
        background: rgba(255, 255, 255, 0); /* Invisible */
        border: None;
        z-index: 5;
    }}
    .map-area:hover {{
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid gold;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. LÓGICA DE NAVEGACIÓN ---
def viajar_a(reino):
    st.session_state.user['reino_actual'] = reino
    st.session_state.user['dragon_pos_x'] = posiciones[reino]['x']
    st.session_state.user['dragon_pos_y'] = posiciones[reino]['y']

# --- 5. INTERFAZ ---
if not st.session_state.user['setup_complete']:
    st.title("Bienvenue")
    nombre = st.text_input("Ton nombre:")
    if st.button("Commencer"):
        st.session_state.user['nombre'] = nombre
        st.session_state.user['setup_complete'] = True
        st.rerun()
else:
    tab1, tab2 = st.tabs(["🗺️ Carte du Royaume", "📜 Journal"])

    with tab1:
        st.subheader(f"Explorateur: {st.session_state.user['nombre']} | ✨ {st.session_state.user['xp']} XP")
        
        # MAPA CON BOTONES INVISIBLES
        st.markdown(f"""
        <div class="map-wrapper">
            <img src="https://raw.githubusercontent.com/{st.secrets.get('github_username', 'user')}/{st.secrets.get('github_repo', 'repo')}/main/mapa_reinos.png" class="map-img">
            <div class="dragon-sprite" style="left: {st.session_state.user['dragon_pos_x']}; top: {st.session_state.user['dragon_pos_y']};"></div>
        </div>
        """, unsafe_allow_html=True)

        # Botones de control para activar la lógica de Streamlit
        # (Streamlit no permite clics directos en HTML, así que usamos botones con estilo)
        cols = st.columns(4)
        if cols[0].button("📍 Royaume Français"): viajar_a("Frances"); st.rerun()
        if cols[1].button("📍 Valle Matemático"): viajar_a("Mates"); st.rerun()
        if cols[2].button("📍 Labo Alchimie"): viajar_a("Ciencias"); st.rerun()
        if cols[3].button("📍 Temple Musical"): viajar_a("Musica"); st.rerun()

        # Mostrar el contenido del Reino DEBAJO de la imagen
        if st.session_state.user['reino_actual'] == "Frances":
            st.markdown("""
            <div style="background: #fdf5e6; color: #3e2723; padding: 20px; border-radius: 10px; border: 3px solid #8b4513;">
                <h3>🇫🇷 Bienvenue au Royaume Français</h3>
                <p>Reto: ¿Cómo se dice 'Castillo' en francés?</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Le château"): 
                st.session_state.user['xp'] += 50
                st.success("¡Bravo! +50 XP")
                time.sleep(1); st.rerun()

    with tab2:
        st.write("Escribe tu Journal aquí...")
