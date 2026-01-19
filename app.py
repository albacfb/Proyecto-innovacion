import streamlit as st
import time
import os
from PIL import Image

# --- 1. CONFIGURACIÓN E INYECCIÓN DE DISEÑO ---
st.set_page_config(page_title="Les Dragons de l'Apprentissage", layout="centered", page_icon="🐉")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Quicksand:wght@400;600&display=swap');
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)), 
                    url('https://images.unsplash.com/photo-1578662996442-48f60103fc96?q=80&w=2070&auto=format&fit=crop');
        background-size: cover; background-position: center; background-attachment: fixed;
        color: #f8fafc; font-family: 'Quicksand', sans-serif;
    }
    .glass-panel {
        background: rgba(255, 255, 255, 0.12); backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 35px;
        padding: 30px; text-align: center; margin-bottom: 20px;
    }
    .xp-bg { width: 100%; background: rgba(255,255,255,0.1); border-radius: 15px; height: 14px; margin: 15px 0; }
    .xp-fill { height: 100%; border-radius: 15px; background: linear-gradient(90deg, #fcd34d, #f59e0b); }
    .fancy-title { font-family: 'Cinzel', serif; color: #fcd34d !important; text-shadow: 2px 2px 10px black; }
    </style>
""", unsafe_allow_html=True)

# --- 2. GESTIÓN DE ESTADO ---
if 'user' not in st.session_state:
    st.session_state.user = {
        'nombre': 'Apprenti',
        'xp': 0,
        'monedas': 100,
        'view': 'Home',
        'setup_complete': False
    }

fases_dragon = {
    "Oeuf": "huevo.png",
    "Bébé": "bebe.png",
    "Expert": "experto.png",
    "Maître": "adulto.png"
}

def obtener_fase_actual(xp):
    if xp < 150: return "Oeuf"
    elif xp < 400: return "Bébé"
    elif xp < 800: return "Expert"
    else: return "Maître"

# --- 3. VISTAS ---
if not st.session_state.user['setup_complete']:
    st.markdown("<div class='glass-panel'><h1 class='fancy-title'>Bienvenue</h1>", unsafe_allow_html=True)
    nombre = st.text_input("Comment t'appelles-tu ?")
    
    # AYUDA PARA SUBIR ARCHIVOS SI NO CARGAN DESDE GITHUB
    st.info("Si tus imágenes no cargan automáticamente, súbelas aquí una vez para que la app las reconozca:")
    uploaded_files = st.file_uploader("Sube tus 4 archivos .png", accept_multiple_files=True)
    
    if st.button("Lancer l'aventure ⚔️"):
        st.session_state.user['nombre'] = nombre
        st.session_state.user['setup_complete'] = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    fase_nombre = obtener_fase_actual(st.session_state.user['xp'])
    nombre_archivo = fases_dragon[fase_nombre]
    
    if st.session_state.user['view'] == 'Home':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown(f"<h1 class='fancy-title'>Niveau {fase_nombre}</h1>", unsafe_allow_html=True)
        
        # INTENTO DE CARGA DE IMAGEN
        try:
            # Intenta cargar desde la carpeta local
            image = Image.open(nombre_archivo)
            st.image(image, width=350)
        except FileNotFoundError:
            st.error(f"⚠️ No encuentro el archivo '{nombre_archivo}' en GitHub.")
            st.warning("Asegúrate de haber subido los archivos a la carpeta principal de tu proyecto con los nombres correctos.")
        
        st.write(f"### {st.session_state.user['nombre']}")
        
        # Barra de progreso
        proximo_xp = 150 if fase_nombre == "Oeuf" else 400 if fase_nombre == "Bébé" else 800 if fase_nombre == "Expert" else 1200
        progreso = min(st.session_state.user['xp'] / proximo_xp * 100, 100)
        
        st.markdown(f'<div class="xp-bg"><div class="xp-fill" style="width:{progreso}%"></div></div>', unsafe_allow_html=True)
        st.write(f"✨ {st.session_state.user['xp']} XP | 🪙 {st.session_state.user['monedas']} Pièces")
        st.markdown("</div>", unsafe_allow_html=True)

    # NAVEGACIÓN
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("🏠 Home"): 
        st.session_state.user['view'] = 'Home'
        st.rerun()
    if c2.button("📝 Gagner XP"): 
        st.session_state.user['xp'] += 150
        st.rerun()
