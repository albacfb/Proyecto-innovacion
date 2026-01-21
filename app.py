import streamlit as st
import time
import random
import os
from datetime import date
import gspread
import json

# --- 1. CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="Le Royaume des Savoirs", layout="centered", page_icon="🗺️")

# Fondo del Mapa General (Estilo pergamino épico)
fondo_mapa = "https://images.unsplash.com/photo-1533035353720-f1c6a75cd8ab?q=80&w=1974&auto=format&fit=crop"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Quicksand:wght@400;600&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url('{fondo_mapa}');
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    .parchment {{
        background: #fdf5e6;
        background-image: url("https://www.transparenttextures.com/patterns/old-paper.png");
        padding: 30px; border-radius: 10px; border: 5px double #8b4513;
        color: #3e2723; font-family: 'Quicksand', sans-serif;
    }}

    .realm-card {{
        background: rgba(0,0,0,0.7); border: 2px solid #fcd34d;
        border-radius: 20px; padding: 15px; margin: 10px; text-align: center;
        transition: 0.3s; cursor: pointer; color: white;
    }}
    .realm-card:hover {{ transform: scale(1.05); background: rgba(0,0,0,0.8); }}
    
    .fancy-title {{ font-family: 'Cinzel', serif; color: #fcd34d !important; text-shadow: 2px 2px 10px #000; }}
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
        'reino_actual': 'Mapa', 'inventario': [], 'last_login': None 
    }

def reward(xp, coins):
    st.session_state.user['xp'] += xp
    st.session_state.user['monedas'] += coins
    return xp, coins

# --- 3. VISTAS ---

# --- REINO: MATEMÁTICAS ---
def reino_mates():
    st.markdown("<div class='parchment'><h2>🔢 Valle de las Matemáticas</h2><p>Resuelve el enigma del Guardián:</p></div>", unsafe_allow_html=True)
    num1, num2 = random.randint(10, 50), random.randint(10, 50)
    res = st.number_input(f"¿Cuánto es {num1} + {num2}?", step=1)
    if st.button("Lanzar Hechizo Matemático"):
        if res == num1 + num2:
            xp, co = reward(20, 10)
            st.success(f"¡Correcto! +{xp} XP")
        else: st.error("El hechizo ha fallado...")

# --- REINO: FRANCÉS ---
def reino_frances():
    st.markdown("<div class='parchment'><h2>🥖 Reino de Francia</h2><p>Traduction rapide :</p></div>", unsafe_allow_html=True)
    palabra = st.radio("¿Cómo se dice 'Dragón' en francés?", ["Le Chat", "Le Dragon", "Le Chien"])
    if st.button("Vérifier"):
        if palabra == "Le Dragon":
            xp, co = reward(20, 10)
            st.success("Trés bien !")
        else: st.error("Faux !")

# --- NAVEGACIÓN PRINCIPAL ---
if not st.session_state.user['setup_complete'] if 'setup_complete' in st.session_state.user else False:
    # Lógica de Inicio (ya la tienes)
    pass
else:
    # --- MENÚ DE NAVEGACIÓN ---
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Foyer", "🗺️ Mapa de Reinos", "📝 Journal", "💎 Boutique"])

    with tab1: # HOME
        st.markdown(f"<h1 class='fancy-title'>Bonjour, {st.session_state.user['nombre']}</h1>", unsafe_allow_html=True)
        st.write(f"✨ XP: {st.session_state.user['xp']} | 🪙 Monedas: {st.session_state.user['monedas']}")
        # Aquí iría el dragón flotante que ya programamos

    with tab2: # EL MAPA
        st.markdown("<h2 class='fancy-title'>Elige tu Destino</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔢 Valle Matemático"): st.session_state.user['reino_actual'] = "Mates"
            if st.button("🧪 Laboratorio de Alquimia (Ciencias)"): st.session_state.user['reino_actual'] = "Ciencias"
        
        with col2:
            if st.button("🥖 Reino Francés"): st.session_state.user['reino_actual'] = "Frances"
            if st.button("🎶 Templo de la Música"): st.session_state.user['reino_actual'] = "Musica"

        st.markdown("---")
        # Mostrar el contenido según el reino elegido
        if st.session_state.user['reino_actual'] == "Mates": reino_mates()
        elif st.session_state.user['reino_actual'] == "Frances": reino_frances()
        else: st.info("Selecciona un reino en el mapa para empezar un reto.")

    with tab3: # JOURNAL (Pergamino medieval)
        st.markdown('<div class="parchment">', unsafe_allow_html=True)
        st.markdown("<h2>📜 Crónica del día</h2>", unsafe_allow_html=True)
        # Aquí el código del journal que ya tenemos...
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab4: # BOUTIQUE
        st.markdown("<div class='glass-panel'><h2>💎 Bazar del Reino</h2></div>", unsafe_allow_html=True)
        # Aquí el código de la boutique...
