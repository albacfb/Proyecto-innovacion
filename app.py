import streamlit as st
import time
import random
import os
from datetime import date
import gspread
import json # Importante para procesar el JSON de los secrets

# --- 1. CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="Les Dragons de l'Apprentissage", layout="centered", page_icon="🐉")

fondo_reino = "https://images.unsplash.com/photo-1547826039-bfc3ade20521?q=80&w=1932&auto=format&fit=crop"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Quicksand:wght@400;600&display=swap');
    .stApp {{
        background: url('{fondo_reino}');
        background-size: cover; background-position: center; background-attachment: fixed;
    }}
    .glass-panel {{
        background: rgba(255, 255, 255, 0.18); backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 30px; padding: 25px;
        text-align: center; margin-bottom: 20px; color: #1e293b;
    }}
    .fancy-title {{ font-family: 'Cinzel', serif; color: #fcd34d !important; text-shadow: 2px 2px 8px #000; }}
    .stButton button {{ border-radius: 12px; font-weight: bold; width: 100%; transition: 0.3s; }}
    
    .progress-container {{ width: 100%; background-color: rgba(0, 0, 0, 0.2); border-radius: 20px; margin: 20px 0; height: 20px; }}
    .progress-bar {{ height: 100%; background: linear-gradient(90deg, #fcd34d, #f59e0b); box-shadow: 0 0 10px #fcd34d; border-radius: 20px; transition: width 0.5s; }}
    </style>
""", unsafe_allow_html=True)

# --- CONEXIÓN A GOOGLE SHEETS (CORREGIDA) ---
def save_to_sheets(data):
    try:
        # 1. Obtener los datos de los secrets
        creds_raw = st.secrets["google_sheets_creds"]
        
        # 2. Corregir el error 'str' object has no attribute 'keys'
        # Si Streamlit Cloud lo lee como una cadena (string), lo convertimos a diccionario
        if isinstance(creds_raw, str):
            creds_info = json.loads(creds_raw)
        else:
            creds_info = dict(creds_raw)
            
        # 3. Conectar usando el diccionario de credenciales
        gc = gspread.service_account_from_dict(creds_info)
        
        # 4. Abrir la hoja y la pestaña
        sh = gc.open("JournalApprentices").worksheet("JournalEntries")
        sh.append_row(data)
        return True
    except Exception as e:
        st.error(f"Erreur Excel: {e}")
        return False

# --- 2. ESTADO DEL JUEGO ---
if 'user' not in st.session_state:
    st.session_state.user = {
        'nombre': 'Apprenti', 'xp': 0, 'monedas': 100, 'view': 'Home', 
        'setup_complete': False, 'inventario': [], 'last_login': None 
    }

fases_dragon = {"Oeuf": "huevo.png", "Bébé": "bebe.png", "Expert": "experto.png", "Maître": "adulto.png"}

def reward(xp, coins):
    if "⚔️ Épée de Feu" in st.session_state.user['inventario']: xp = int(xp * 1.2)
    if "🛡️ Armure en Or" in st.session_state.user['inventario']: coins = int(coins * 1.5)
    st.session_state.user['xp'] += xp
    st.session_state.user['monedas'] += coins
    return xp, coins

def obtener_fase(xp):
    if xp < 150: return "Oeuf"
    elif xp < 400: return "Bébé"
    elif xp < 800: return "Expert"
    else: return "Maître"

# --- 3. VISTAS ---
if not st.session_state.user['setup_complete']:
    st.markdown("<div class='glass-panel'><h1 class='fancy-title'>Bienvenue</h1>", unsafe_allow_html=True)
    st.session_state.user['nombre'] = st.text_input("Ton nom, Apprenti :")
    if st.button("Lancer l'aventure ⚔️"):
        st.session_state.user['setup_complete'] = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    today = str(date.today())
    if st.session_state.user['last_login'] != today:
        st.session_state.user['last_login'] = today
        reward(20, 50)
        st.toast("🎁 Coffre quotidien !", icon="💰")

    fase = obtener_fase(st.session_state.user['xp'])
    
    if st.session_state.user['view'] == 'Home':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown(f"<h1 class='fancy-title'>Niveau {fase}</h1>", unsafe_allow_html=True)
        proximo = 150 if fase == "Oeuf" else 400 if fase == "Bébé" else 800 if fase == "Expert" else 1200
        porcentaje = min((st.session_state.user['xp'] / proximo) * 100, 100)
        st.markdown(f'<div class="progress-container"><div class="progress-bar" style="width:{porcentaje}%"></div></div>', unsafe_allow_html=True)
        
        if os.path.exists(fases_dragon[fase]): st.image(fases_dragon[fase], width=300)
        else: st.warning(f"Image {fases_dragon[fase]} manquante")
        st.write(f"✨ {st.session_state.user['xp']} XP | 🪙 {st.session_state.user['monedas']} Pièces")
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.user['view'] == 'Journal':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("<h2 class='fancy-title'>Mon Journal</h2>", unsafe_allow_html=True)
        sent = st.select_slider("Sentiment", ["😞", "😐", "🙂", "🤩"])
        succ = st.text_area("Aujourd'hui, j'ai réussi à...")
        fail = st.text_area("Je n'ai pas réussi à...")
        chan = st.text_area("Changements pour la clase ?")
        impr = st.text_area("Amélioration personnelle ?")
        
        if st.button("Enregistrer 📝"):
            if succ and fail:
                xp_g, co_g = reward(40, 10)
                # GUARDAR EN EXCEL
                data = [st.session_state.user['nombre'], today, sent, succ, fail, chan, impr, xp_g, co_g]
                if save_to_sheets(data):
                    st.success("Données envoyées à l'Excel ! +40 XP")
                    time.sleep(1); st.session_state.user['view'] = 'Home'; st.rerun()
            else: st.error("Remplis les champs obligatorios !")
        st.markdown("</div>", unsafe_allow_html=True)

    # Navegación
    cols = st.columns(4)
    if cols[0].button("🏠 Home"): st.session_state.user['view'] = 'Home'; st.rerun()
    if cols[1].button("📝 Journal"): st.session_state.user['view'] = 'Journal'; st.rerun()
    if cols[2].button("🎮 Jeux"): st.session_state.user['view'] = 'Jeux'; st.rerun()
    if cols[3].button("💎 Boutique"): st.session_state.user['view'] = 'Boutique'; st.rerun()
