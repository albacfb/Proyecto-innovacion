import streamlit as st
import time
import random
from datetime import date
import json
import gspread
from google.oauth2.service_account import Credentials

# --- 1. CONFIGURACIÓN Y CONEXIÓN A EXCEL ---
st.set_page_config(page_title="Les Dragons de l’Apprentissage", layout="wide", page_icon="🐉")

def save_to_sheets(datos_fila):
    try:
        # Usa los Secrets de Streamlit para conectar de forma segura
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds_dict = json.loads(st.secrets["google_sheets_creds"])
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)
        
        # Abre el Excel (Asegúrate de que se llame exactamente así en tu Drive)
        sheet = client.open("JournalApprentices").sheet1
        sheet.append_row(datos_fila)
        return True
    except Exception as e:
        st.error(f"Error al conectar con el Reino de Papel (Excel): {e}")
        return False

# --- 2. ESTADO DEL JUEGO ---
if 'user' not in st.session_state:
    st.session_state.user = {
        'nombre': '', 'xp': 0, 'monedas': 10, 'inventario': [],
        'reino_actual': 'Centro del Reino', 'setup_done': False
    }

def ganar_recompensa(xp_ganado, monedas_ganadas):
    st.session_state.user['xp'] += xp_ganado
    st.session_state.user['monedas'] += monedas_ganadas
    st.toast(f"¡+{xp_ganado} XP!", icon="✨")

def obtener_imagen_dragon(xp):
    if xp < 50: return "https://cdn-icons-png.flaticon.com/512/808/808506.png"
    elif xp < 150: return "https://cdn-icons-png.flaticon.com/512/3554/3554371.png"
    else: return "https://cdn-icons-png.flaticon.com/512/3069/3069418.png"

# --- 3. INTERFAZ ---
if not st.session_state.user['setup_done']:
    st.title("🏹 Bienvenue au Royaume")
    nombre = st.text_input("¿Cómo te llamas, aprendiz?")
    if st.button("Empezar"):
        if nombre:
            st.session_state.user['nombre'] = nombre
            st.session_state.user['setup_done'] = True
            st.rerun()
else:
    # Sidebar con Stats siempre visibles
    with st.sidebar:
        st.header(f"Héroe: {st.session_state.user['nombre']}")
        st.image(obtener_imagen_dragon(st.session_state.user['xp']), width=150)
        st.metric("XP", st.session_state.user['xp'])
        st.metric("Or", st.session_state.user['monedas'])

    tab_mapa, tab_journal = st.tabs(["🗺️ Carte", "📜 Journal Royal"])

    with tab_mapa:
        st.title("Mapa Transversal")
        c1, c2, c3 = st.columns(3)
        if c1.button("🇫🇷 Francés"): st.session_state.user['reino_actual'] = "Francés"
        if c2.button("🔢 Mates"): st.session_state.user['reino_actual'] = "Mates"
        if c3.button("🧪 Ciencias"): st.session_state.user['reino_actual'] = "Ciencias"
        st.info(f"📍 Estás en: {st.session_state.user['reino_actual']}")

    with tab_journal:
        st.title("📜 Ficha de Metacognición")
        with st.container():
            sent = st.select_slider("Sentimiento", ["😞", "😐", "🙂", "🤩"])
            logro = st.text_area("1. Logros hoy:")
            reto = st.text_area("2. Mayor dificultad:")
            estrat = st.text_area("3. Estrategia usada:")
            feedback = st.text_area("4. Mensaje al Maestro:")
            
            if st.button("Sellar y enviar a la Nube 🖋️"):
                if logro and reto:
                    # Preparamos la fila para el Excel
                    fila = [
                        st.session_state.user['nombre'], 
                        str(date.today()), 
                        sent, logro, reto, estrat, feedback, 
                        st.session_state.user['xp']
                    ]
                    
                    if save_to_sheets(fila):
                        ganar_recompensa(50, 20)
                        st.balloons()
                        st.success("¡Datos guardados en el Excel del Maestro!")
                else:
                    st.error("Completa los campos para que el Maestro pueda evaluarte.")
