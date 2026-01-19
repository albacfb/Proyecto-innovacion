import streamlit as st
import time
import os

# --- 1. CONFIGURACIÓN E INYECCIÓN DE DISEÑO ---
st.set_page_config(page_title="Les Dragons de l'Apprentissage", layout="centered", page_icon="🐉")

# (Mantenemos tu CSS anterior aquí...)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)), 
                    url('https://images.unsplash.com/photo-1578662996442-48f60103fc96?q=80&w=2070&auto=format&fit=crop');
        background-size: cover; background-position: center; background-attachment: fixed;
    }
    .glass-panel {
        background: rgba(255, 255, 255, 0.12); backdrop-filter: blur(20px);
        border-radius: 35px; padding: 30px; text-align: center; margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. ASIGNACIÓN DE RUTAS DE ARCHIVOS ---
# Usamos os.path.join para evitar errores de ruta en diferentes sistemas
base_path = os.path.dirname(__file__)

fases_dragon = {
    "Oeuf": "WhatsApp_Image_2026-01-19_at_18.49.24-removebg-preview.png",
    "Bébé": "WhatsApp_Image_2026-01-19_at_18.49.24__1_-removebg-preview.png",
    "Jeune": "WhatsApp_Image_2026-01-19_at_18.49.24__2_-removebg-preview.png",
    "Maître": "WhatsApp_Image_2026-01-19_at_18.49.24__3_-removebg-preview.png"
}

# --- 3. ESTADO Y LÓGICA ---
if 'user' not in st.session_state:
    st.session_state.user = {'nombre': 'Apprenti', 'xp': 0, 'monedas': 100, 'view': 'Home', 'setup_complete': False}

def obtener_fase_actual(xp):
    if xp < 150: return "Oeuf"
    elif xp < 400: return "Bébé"
    elif xp < 800: return "Jeune"
    else: return "Maître"

# --- 4. VISTAS ---
if not st.session_state.user['setup_complete']:
    st.markdown("<div class='glass-panel'><h1>Bienvenue</h1>", unsafe_allow_html=True)
    nombre = st.text_input("Comment t'appelles-tu ?")
    if st.button("Lancer l'aventure"):
        st.session_state.user['nombre'] = nombre
        st.session_state.user['setup_complete'] = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    fase_nombre = obtener_fase_actual(st.session_state.user['xp'])
    nombre_archivo = fases_dragon[fase_nombre]
    ruta_imagen = os.path.join(base_path, nombre_archivo)

    if st.session_state.user['view'] == 'Home':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.write(f"### Niveau {fase_nombre}")
        
        # --- SOLUCIÓN AL ERROR DE CARGA ---
        if os.path.exists(ruta_imagen):
            st.image(ruta_imagen, width=300)
        else:
            st.error(f"⚠️ No se pudo encontrar el archivo: {nombre_archivo}")
            st.info("Asegúrate de que el nombre del archivo en GitHub coincida exactamente (mayúsculas y minúsculas).")
        
        st.write(f"### {st.session_state.user['nombre']}")
        st.write(f"✨ {st.session_state.user['xp']} XP")
        st.markdown("</div>", unsafe_allow_html=True)

    # Navegación
    if st.button("📝 Ganar XP (Simulación)"):
        st.session_state.user['xp'] += 60
        st.rerun()
