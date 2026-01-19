import streamlit as st
import time
import random

# --- 1. CONFIGURACIÓN E INYECCIÓN DE DISEÑO ---
st.set_page_config(page_title="Les Dragons de l'Apprentissage", layout="centered", page_icon="🐉")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Quicksand:wght@400;600&display=swap');

    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)), 
                    url('https://images.unsplash.com/photo-1578662996442-48f60103fc96?q=80&w=2070&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #f8fafc;
        font-family: 'Quicksand', sans-serif;
    }

    .glass-panel {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 35px;
        padding: 30px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8);
        text-align: center;
        margin-bottom: 20px;
    }

    /* ANIMACIÓN PARA TUS NUEVOS SPRITES */
    .dragon-display {
        width: 280px;
        margin: 0 auto;
        animation: float 4s ease-in-out infinite;
        filter: drop-shadow(0 0 20px rgba(252, 211, 77, 0.4));
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(2deg); }
    }

    .xp-bg { width: 100%; background: rgba(255,255,255,0.1); border-radius: 15px; height: 14px; margin: 15px 0; }
    .xp-fill { height: 100%; border-radius: 15px; background: linear-gradient(90deg, #fcd34d, #f59e0b); box-shadow: 0 0 10px gold; }
    .fancy-title { font-family: 'Cinzel', serif; color: #fcd34d !important; text-shadow: 2px 2px 10px black; }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 2. ASIGNACIÓN DE TUS IMÁGENES SUBIDAS ---
# Streamlit maneja los archivos subidos mediante sus nombres de archivo si están en la misma carpeta
fases_dragon = {
    "Oeuf": "WhatsApp_Image_2026-01-19_at_18.49.24-removebg-preview.png",
    "Bébé": "WhatsApp_Image_2026-01-19_at_18.49.24__1_-removebg-preview.png",
    "Jeune": "WhatsApp_Image_2026-01-19_at_18.49.24__2_-removebg-preview.png",
    "Maître": "WhatsApp_Image_2026-01-19_at_18.49.24__3_-removebg-preview.png"
}

# --- 3. LÓGICA DE ESTADO Y EVOLUCIÓN ---
if 'user' not in st.session_state:
    st.session_state.user = {
        'nombre': 'Apprenti',
        'xp': 0,
        'monedas': 100,
        'view': 'Home',
        'setup_complete': False
    }

def obtener_fase_actual(xp):
    if xp < 150: return "Oeuf"
    elif xp < 400: return "Bébé"
    elif xp < 800: return "Jeune"
    else: return "Maître"

# --- 4. VISTAS ---
if not st.session_state.user['setup_complete']:
    st.markdown("<div class='glass-panel'><h1 class='fancy-title'>Bienvenue</h1>", unsafe_allow_html=True)
    nombre = st.text_input("Comment t'appelles-tu ?", placeholder="Ton nom...")
    if st.button("Lancer l'aventure ⚔️"):
        st.session_state.user['nombre'] = nombre
        st.session_state.user['setup_complete'] = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    fase_nombre = obtener_fase_actual(st.session_state.user['xp'])
    imagen_fase = fases_dragon[fase_nombre]

    if st.session_state.user['view'] == 'Home':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown(f"<h1 class='fancy-title'>Niveau {fase_nombre}</h1>", unsafe_allow_html=True)
        
        # MOSTRAR TU IMAGEN CORRESPONDIENTE
        st.image(imagen_fase, use_container_width=False, width=300, output_format="PNG")
        
        st.write(f"### {st.session_state.user['nombre']}")
        
        # Barra de progreso XP
        proximo_nivel = 150 if fase_nombre == "Oeuf" else 400 if fase_nombre == "Bébé" else 800
        progreso_porcentaje = min(st.session_state.user['xp'] / proximo_nivel * 100, 100)
        
        st.markdown(f'<div class="xp-bg"><div class="xp-fill" style="width:{progreso_porcentaje}%"></div></div>', unsafe_allow_html=True)
        st.write(f"✨ {st.session_state.user['xp']} XP | 🪙 {st.session_state.user['monedas']} Pièces")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- BOTONES DE NAVEGACIÓN ---
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("🏠 Home"): st.session_state.user['view'] = 'Home'; st.rerun()
    if c2.button("📝 Journal"): 
        # Simulación de ganar XP para probar la evolución
        st.session_state.user['xp'] += 60
        st.toast("¡Has estudiado! +60 XP")
        st.rerun()
    if c3.button("🎮 Jeux"): st.toast("Próximamente..."); st.rerun()
