import streamlit as st
import time
import random
from datetime import date
import json

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Les Dragons de l’Apprentissage", layout="wide", page_icon="🐉")

# --- 2. ESTADO DEL JUEGO ---
if 'user' not in st.session_state:
    st.session_state.user = {
        'nombre': '',
        'xp': 0,
        'monedas': 10,
        'inventario': [],
        'reino_actual': 'Centro del Reino',
        'setup_done': False,
        'last_journal': None
    }

# --- 3. FUNCIONES DE APOYO ---
def ganar_recompensa(xp_ganado, monedas_ganadas):
    st.session_state.user['xp'] += xp_ganado
    st.session_state.user['monedas'] += monedas_ganadas
    st.toast(f"¡+{xp_ganado} XP y +{monedas_ganadas} 🪙!", icon="✨")

def obtener_imagen_dragon(xp):
    # Evolución visual basada en el progreso académico
    if xp < 50:
        return "https://cdn-icons-png.flaticon.com/512/808/808506.png" # Huevo
    elif xp < 150:
        return "https://cdn-icons-png.flaticon.com/512/3554/3554371.png" # Bebé
    else:
        return "https://cdn-icons-png.flaticon.com/512/3069/3069418.png" # Adulto

# --- 4. ESTILOS VISUALES ---
st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a; color: white; }
    .parchment {
        background: #fdf5e6;
        background-image: url("https://www.transparenttextures.com/patterns/old-paper.png");
        padding: 30px; border-radius: 10px; border: 4px solid #8b4513;
        color: #3e2723; font-family: 'serif';
        margin-bottom: 20px;
    }
    .stat-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 10px; border-radius: 10px; border: 1px solid gold;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- 5. LÓGICA DE INICIO ---
if not st.session_state.user['setup_done']:
    st.title("🏹 Bienvenue au Royaume des Dragons")
    st.subheader("Tu aventura de innovación docente comienza aquí.")
    nombre = st.text_input("¿Cómo te llamas, joven aprendiz?")
    if st.button("Lancer l'aventure ⚔️"):
        if nombre:
            st.session_state.user['nombre'] = nombre
            st.session_state.user['setup_done'] = True
            st.rerun()
else:
    # --- SIDEBAR (Panel de Control del Alumno) ---
    with st.sidebar:
        st.header(f"Chevalier: {st.session_state.user['nombre']}")
        st.image(obtener_imagen_dragon(st.session_state.user['xp']), width=150)
        
        col1, col2 = st.columns(2)
        with col1: st.metric("XP", st.session_state.user['xp'])
        with col2: st.metric("🪙 Or", st.session_state.user['monedas'])
        
        st.write("---")
        st.subheader("🎒 Inventaire de l'Apprenti")
        if st.session_state.user['inventario']:
            for item in st.session_state.user['inventario']: st.write(f"🛡️ {item}")
        else: st.write("*Tu inventario está vacío*")

    # --- PESTAÑAS PRINCIPALES ---
    tab_foyer, tab_mapa, tab_juegos, tab_journal = st.tabs(["🏠 Foyer", "🗺️ Carte des Savoirs", "🎮 Entraînement", "📜 Journal Royal"])

    with tab_foyer:
        st.title("Estado de tu Dragón")
        c_img, c_info = st.columns([1, 2])
        with c_img:
            st.image(obtener_imagen_dragon(st.session_state.user['xp']), width=300)
        with c_info:
            xp = st.session_state.user['xp']
            if xp < 50:
                st.subheader("Fase: Huevo")
                st.write("Registra tus aprendizajes en el Journal para que el huevo eclosione.")
                st.progress(xp / 50)
            elif xp < 150:
                st.subheader("Fase: Dragón Joven")
                st.write("¡Has eclosionado! Sigue superando retos en los reinos.")
                st.progress((xp - 50) / 100)
            else:
                st.subheader("Fase: Dragón Maestro")
                st.balloons()
                st.success("¡Has alcanzado la maestría máxima!")

    with tab_mapa:
        st.title("Mapa de las Asignaturas (Transversalidad)")
        st.write("Viaja a los distintos reinos para desbloquear conocimientos.")
        
        # Simulación de Mapa con columnas
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            if st.button("🇫🇷 Royaume Français"): st.session_state.user['reino_actual'] = "Royaume Français"
        with col_m2:
            if st.button("🔢 Valle Matemático"): st.session_state.user['reino_actual'] = "Valle Matemático"
        with col_m3:
            if st.button("🧪 Labo Alchimie (Ciencias)"): st.session_state.user['reino_actual'] = "Laboratorio de Alquimia"
            
        st.info(f"📍 Estás en: **{st.session_state.user['reino_actual']}**")

    with tab_juegos:
        st.title("Minijuegos de Entrenamiento")
        juego = st.selectbox("Selecciona tu prueba:", ["Cálculo de Fuego", "Traductor de Pergaminos"])
        
        if juego == "Cálculo de Fuego":
            n1, n2 = random.randint(5, 15), random.randint(2, 9)
            res = st.number_input(f"¿Cuánto es {n1} x {n2}?", step=1)
            if st.button("Lanzar Ataque Mágico"):
                if res == n1 * n2:
                    st.success("¡Impacto directo!")
                    ganar_recompensa(15, 5)
                else: st.error("El hechizo falló...")

    with tab_journal:
        st.markdown("<div class='parchment'>", unsafe_allow_html=True)
        st.title("📜 Journal de l'Apprenti")
        st.write("Esta es la parte más importante: tu reflexión sobre lo aprendido hoy.")
        
        # Campos detallados para el Proyecto de Innovación
        f_hoy = st.date_input("Fecha del registro", date.today())
        sentimiento = st.select_slider("¿Cómo te has sentido hoy aprendiendo?", options=["😞", "😐", "🙂", "🤩"])
        
        st.write("---")
        logro = st.text_area("1. ¿Qué éxito has conseguido hoy? (Objetivos alcanzados)")
        dificultad = st.text_area("2. ¿Qué ha sido lo más difícil y por qué?")
        estrategia = st.text_area("3. ¿Qué has hecho para superar esa dificultad?")
        mejora = st.text_area("4. ¿Qué te gustaría aprender o mejorar mañana?")
        feedback = st.text_area("5. Mensaje para el Maestro (Propuestas para la clase)")
        
        if st.button("Sellar Diario 🖋️"):
            if logro and dificultad:
                ganar_recompensa(40, 10)
                st.balloons()
                st.success("Tus reflexiones han sido enviadas a la Torre del Maestro.")
                st.session_state.user['last_journal'] = str(f_hoy)
            else:
                st.error("Debes completar al menos los dos primeros apartados para ganar XP.")
        st.markdown("</div>", unsafe_allow_html=True)
