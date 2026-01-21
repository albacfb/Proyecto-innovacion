import streamlit as st
import time
import os
from datetime import date
import json
import gspread

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Le Royaume des Savoirs", layout="wide", page_icon="🐉")

# --- 2. ESTADO DEL JUEGO (RESETEO SEGURO) ---
if 'user' not in st.session_state:
    st.session_state.user = {
        'nombre': 'Apprenti', 'xp': 0, 'monedas': 100, 
        'reino_actual': None, 'setup_complete': False,
        'dragon_pos_x': '50%', 'dragon_pos_y': '50%',
        'inventario': []
    }

# Asegurar que no falte ninguna clave para evitar errores
keys_check = ['dragon_pos_x', 'dragon_pos_y', 'reino_actual', 'setup_complete', 'xp', 'monedas']
for k in keys_check:
    if k not in st.session_state.user:
        st.session_state.user[k] = '50%' if 'pos' in k else (None if k == 'reino_actual' else 0)

# Coordenadas exactas para tu mapa
posiciones = {
    "Mates": {'x': '22%', 'y': '28%'},
    "Frances": {'x': '78%', 'y': '25%'},
    "Ciencias": {'x': '25%', 'y': '72%'},
    "Musica": {'x': '68%', 'y': '75%'}
}

# --- 3. ESTILOS CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Quicksand:wght@400;600&display=swap');
    
    .stApp {{ background-color: #1a1a1a; color: white; }}
    
    .map-container {{
        position: relative;
        width: 100%;
        max-width: 800px;
        margin: auto;
        border: 8px solid #8b4513;
        border-radius: 15px;
        box-shadow: 0 0 30px rgba(0,0,0,0.7);
        overflow: hidden;
    }}

    .dragon-icon {{
        position: absolute;
        width: 50px; height: 50px;
        background-image: url("https://cdn-icons-png.flaticon.com/512/3069/3069418.png");
        background-size: cover;
        transform: translate(-50%, -50%);
        transition: all 1s ease-in-out;
        z-index: 99;
        filter: drop-shadow(0 0 10px gold);
    }}

    .parchment {{
        background: #fdf5e6;
        background-image: url("https://www.transparenttextures.com/patterns/old-paper.png");
        padding: 25px; border-radius: 10px; border: 4px solid #8b4513;
        color: #3e2723; font-family: 'Quicksand', sans-serif;
        margin-top: 20px;
    }}
    
    .fancy-title {{ font-family: 'Cinzel', serif; color: #fcd34d !important; text-align: center; }}
    </style>
""", unsafe_allow_html=True)

# --- 4. LOGICA ---
def viajar_a(reino):
    st.session_state.user['reino_actual'] = reino
    st.session_state.user['dragon_pos_x'] = posiciones[reino]['x']
    st.session_state.user['dragon_pos_y'] = posiciones[reino]['y']

# --- 5. INTERFAZ ---
if not st.session_state.user['setup_complete']:
    st.markdown("<div class='parchment'><h1>Bienvenue au Royaume</h1>", unsafe_allow_html=True)
    nombre = st.text_input("Comment t'appelles-tu ?")
    if st.button("Commencer l'aventure ⚔️"):
        st.session_state.user['nombre'] = nombre
        st.session_state.user['setup_complete'] = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
else:
    tab1, tab2, tab3 = st.tabs(["🗺️ La Carte", "🏠 Foyer", "📜 Journal"])

    with tab1:
        st.markdown("<h2 class='fancy-title'>Carte des Royaumes</h2>", unsafe_allow_html=True)
        
        # MOSTRAR EL MAPA (Usamos URL de respaldo por si GitHub falla)
        # IMPORTANTE: Reemplaza TU_USUARIO y TU_REPO con tus datos si quieres usar tu PNG
        mapa_url = "https://images.unsplash.com/photo-1580136608260-42d1c4aa7fbb?q=80&w=1000"
        
        st.markdown(f"""
        <div class="map-container">
            <img src="{mapa_url}" style="width:100%; opacity:0.6;">
            <div class="dragon-icon" style="left: {st.session_state.user['dragon_pos_x']}; top: {st.session_state.user['dragon_pos_y']};"></div>
        </div>
        """, unsafe_allow_html=True)

        # Botones de navegación (Debajo del mapa para estabilidad)
        st.write("### Selecciona tu destino:")
        c1, c2, c3, c4 = st.columns(4)
        if c1.button("🇫🇷 Français"): viajar_a("Frances"); st.rerun()
        if c2.button("🔢 Mates"): viajar_a("Mates"); st.rerun()
        if c3.button("🧪 Alchimie"): viajar_a("Ciencias"); st.rerun()
        if c4.button("🎶 Musique"): viajar_a("Musica"); st.rerun()

        # Contenido del Reino
        if st.session_state.user['reino_actual'] == "Frances":
            st.markdown('<div class="parchment"><h3>🇫🇷 Royaume du Français</h3><p>¿Comment dit-on "Hola" en Français ?</p></div>', unsafe_allow_html=True)
            if st.button("Bonjour"): 
                st.session_state.user['xp'] += 20
                st.success("Correct ! +20 XP")

    with tab2:
        st.markdown(f"<h1 class='fancy-title'>Bienvenue, {st.session_state.user['nombre']}</h1>", unsafe_allow_html=True)
        st.write(f"✨ XP: {st.session_state.user['xp']} | 🪙 Or: {st.session_state.user['monedas']}")
        st.image("https://cdn-icons-png.flaticon.com/512/3069/3069418.png", width=150)

    with tab3:
        st.markdown('<div class="parchment"><h2>📜 Journal de Bord</h2>', unsafe_allow_html=True)
        succ = st.text_area("Qu'as-tu appris aujourd'hui ?")
        if st.button("Enregistrer"):
            st.success("¡Guardado en el Reino!")
        st.markdown("</div>", unsafe_allow_html=True)
