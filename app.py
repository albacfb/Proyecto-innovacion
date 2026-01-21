import streamlit as st
import time
import random
import os
from datetime import date
import gspread
import json

# --- 1. CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="Les Dragons de l'Apprentissage", layout="centered", page_icon="🐉")

# URL de fondo épico (Castillo y Dragón)
# He cambiado esta URL por una de alta disponibilidad para asegurar que cargue
fondo_url = "https://cdn.pixabay.com/photo/2022/11/04/10/24/dragon-7569512_1280.jpg"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Quicksand:wght@400;600&display=swap');
    
    /* Fondo con imagen y color de respaldo */
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), url('{fondo_url}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-color: #1a1a1a; 
    }}

    /* Animación flotante suave */
    @keyframes floating {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-20px); }}
        100% {{ transform: translateY(0px); }}
    }}
    .dragon-container {{
        display: flex;
        justify-content: center;
        padding: 20px;
        animation: floating 4s ease-in-out infinite;
    }}
    .dragon-img {{
        filter: drop-shadow(0 15px 25px rgba(0,0,0,0.8));
        max-width: 350px;
    }}

    /* Estilo Pergamino Medieval Real para el Journal */
    .parchment-box {{
        background: #fdf5e6;
        background-image: url("https://www.transparenttextures.com/patterns/old-paper.png");
        padding: 40px;
        border-radius: 10px;
        border: 8px double #8b4513;
        box-shadow: inset 0 0 50px rgba(0,0,0,0.2), 10px 10px 30px rgba(0,0,0,0.5);
        color: #3e2723;
        font-family: 'Quicksand', sans-serif;
        margin-top: 20px;
    }}

    .glass-panel {{
        background: rgba(0, 0, 0, 0.6); 
        backdrop-filter: blur(12px);
        border: 2px solid #fcd34d; 
        border-radius: 30px; 
        padding: 25px;
        text-align: center; 
        margin-bottom: 20px; 
        color: white;
    }}

    .fancy-title {{ 
        font-family: 'Cinzel', serif; 
        color: #fcd34d !important; 
        text-shadow: 2px 2px 15px #000, 0 0 10px #f59e0b; 
    }}
    
    .stButton button {{
        background: linear-gradient(135deg, #8b4513, #5d2e0c) !important;
        color: #fcd34d !important;
        border: 1px solid #fcd34d !important;
        font-weight: bold;
    }}
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
    except Exception as e:
        st.error(f"Erreur de connexion Excel: {e}")
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
    st.session_state.user['nombre'] = st.text_input("Comment t'appelles-tu, voyageur ?")
    if st.button("Commencer l'aventure 🛡️"):
        st.session_state.user['setup_complete'] = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- BONUS DIARIO REAL ---
    today = str(date.today())
    if st.session_state.user.get('last_login') != today:
        st.session_state.user['last_login'] = today
        reward(25, 50)
        st.balloons()
        st.toast("🎁 Bonus quotidien de 50 pièces reçu !", icon="💰")

    fase = obtener_fase(st.session_state.user['xp'])
    
    if st.session_state.user['view'] == 'Home':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown(f"<h1 class='fancy-title'>Niveau : {fase}</h1>", unsafe_allow_html=True)
        
        # Dragón con animación flotante
        if os.path.exists(fases_dragon[fase]):
            st.markdown(f'''
                <div class="dragon-container">
                    <img src="data:image/png;base64,{fases_dragon[fase]}" class="dragon-img">
                </div>
            ''', unsafe_allow_html=True)
            # Nota: Si usas archivos locales, Streamlit necesita un manejo especial para base64. 
            # Por ahora, usamos st.image estándar dentro del contenedor animado:
            st.image(fases_dragon[fase], width=300)
        
        proximo = 150 if fase == "Oeuf" else 400 if fase == "Bébé" else 800 if fase == "Expert" else 1200
        porcentaje = min((st.session_state.user['xp'] / proximo) * 100, 100)
        st.markdown(f'''
            <div style="width: 100%; background: #444; border-radius: 10px; margin: 10px 0;">
                <div style="width: {porcentaje}%; background: #fcd34d; height: 15px; border-radius: 10px; box-shadow: 0 0 10px #fcd34d;"></div>
            </div>
        ''', unsafe_allow_html=True)
        
        st.write(f"### Chevalier {st.session_state.user['nombre']}")
        st.write(f"✨ {st.session_state.user['xp']} XP | 🪙 {st.session_state.user['monedas']} Pièces")
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.user['view'] == 'Journal':
        st.markdown('<div class="parchment-box">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #5d2e0c;'>📜 Parchemin de Réflexion</h2>", unsafe_allow_html=True)
        sent = st.select_slider("Ton moral aujourd'hui :", ["😞", "😐", "🙂", "🤩"])
        succ = st.text_area("Ta plus grande victoire du jour :")
        fail = st.text_area("Le défi que tu n'as pas encore vaincu :")
        chan = st.text_area("Un conseil pour ton maître (professeur) :")
        
        if st.button("Sceller et envoyer 🖋️"):
            if succ and fail:
                xp_g, co_g = reward(40, 10)
                data = [st.session_state.user['nombre'], today, sent, succ, fail, chan, "", xp_g, co_g]
                if save_to_sheets(data):
                    st.success("Le message a été envoyé par pigeon voyageur !")
                    time.sleep(2); st.session_state.user['view'] = 'Home'; st.rerun()
            else: st.error("Le parchemin doit être complété !")
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.user['view'] == 'Boutique':
         st.markdown("<div class='glass-panel'><h1 class='fancy-title'>🛡️ L'Armurerie Royale</h1>", unsafe_allow_html=True)
         items = {
             "⚔️ Épée de Feu": {"precio": 50, "desc": "+20% XP en tout"},
             "🛡️ Bouclier Magique": {"precio": 40, "desc": "Protège tes pièces"},
             "🪖 Casque de Fer": {"precio": 30, "desc": "Bonus XP au Journal"},
             "🛡️ Armure en Or": {"precio": 100, "desc": "+50% Pièces en tout"}
         }
         for item, info in items.items():
            col1, col2 = st.columns([3, 1])
            col1.write(f"**{item}** - {info['desc']}")
            if item in st.session_state.user['inventario']: col2.button("Possédé ✅", disabled=True, key=item)
            elif col2.button(f"{info['precio']} 🪙", key=item):
                if st.session_state.user['monedas'] >= info['precio']:
                    st.session_state.user['monedas'] -= info['precio']
                    st.session_state.user['inventario'].append(item)
                    st.rerun()
         st.markdown("</div>", unsafe_allow_html=True)

    # NAVEGACIÓN
    st.write("---")
    cols = st.columns(4)
    if cols[0].button("🏠 Foyer"): st.session_state.user['view'] = 'Home'; st.rerun()
    if cols[1].button("📝 Journal"): st.session_state.user['view'] = 'Journal'; st.rerun()
    if cols[2].button("🎮 Jeux"): st.session_state.user['view'] = 'Jeux'; st.rerun()
    if cols[3].button("💎 Boutique"): st.session_state.user['view'] = 'Boutique'; st.rerun()
