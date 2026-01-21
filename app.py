import streamlit as st
import time
import random
import os
from datetime import date
import gspread
import json

# --- 1. CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="Les Dragons de l'Apprentissage", layout="centered", page_icon="🐉")

# Fondo de castillo con dragón
fondo_url = "https://images.unsplash.com/photo-1599408162172-19bc30f65839?q=80&w=2070&auto=format&fit=crop"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Quicksand:wght@400;600&display=swap');
    
    .stApp {{
        background: url('{fondo_url}');
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* Animación flotante para el dragón */
    @keyframes floating {{
        0% {{ transform: translate(0, 0px); }}
        50% {{ transform: translate(0, -15px); }}
        100% {{ transform: translate(0, 0px); }}
    }}
    .floating-dragon {{
        animation: floating 3s ease-in-out infinite;
        filter: drop-shadow(0 10px 15px rgba(0,0,0,0.5));
    }}

    /* Estilo Pergamino Medieval para el Journal */
    .parchment {{
        background-color: #f2e3c9;
        background-image: url("https://www.transparenttextures.com/patterns/paper-fibers.png");
        padding: 40px;
        border-radius: 5px;
        border: 2px solid #8b4513;
        box-shadow: 10px 10px 20px rgba(0,0,0,0.5);
        color: #4a2c0f;
        font-family: 'Quicksand', sans-serif;
    }}

    .glass-panel {{
        background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 30px; padding: 25px;
        text-align: center; margin-bottom: 20px; color: white;
    }}
    .fancy-title {{ font-family: 'Cinzel', serif; color: #fcd34d !important; text-shadow: 3px 3px 10px black; }}
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
    # --- COFRE DIARIO REAL ---
    today = str(date.today())
    if st.session_state.user.get('last_login') != today:
        st.session_state.user['last_login'] = today
        reward(20, 50)
        st.balloons()
        st.toast("🎁 Bonus quotidien reçu !", icon="💰")

    fase = obtener_fase(st.session_state.user['xp'])
    
    if st.session_state.user['view'] == 'Home':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown(f"<h1 class='fancy-title'>Niveau {fase}</h1>", unsafe_allow_html=True)
        
        # Dragón flotante
        if os.path.exists(fases_dragon[fase]):
            st.markdown(f'<div class="floating-dragon">', unsafe_allow_html=True)
            st.image(fases_dragon[fase], width=350)
            st.markdown('</div>', unsafe_allow_html=True)
        
        proximo = 150 if fase == "Oeuf" else 400 if fase == "Bébé" else 800 if fase == "Expert" else 1200
        porcentaje = min((st.session_state.user['xp'] / proximo) * 100, 100)
        st.markdown(f'<div class="progress-container"><div class="progress-bar" style="width:{porcentaje}%"></div></div>', unsafe_allow_html=True)
        
        st.write(f"### {st.session_state.user['nombre']}")
        st.write(f"✨ {st.session_state.user['xp']} XP | 🪙 {st.session_state.user['monedas']} Pièces")
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.user['view'] == 'Journal':
        st.markdown('<div class="parchment">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>📜 Mon Journal Royal</h2>", unsafe_allow_html=True)
        sent = st.select_slider("Comment te sens-tu ?", ["😞", "😐", "🙂", "🤩"])
        succ = st.text_area("Aujourd'hui, j'ai réussi à...")
        fail = st.text_area("Je n'ai pas réussi à...")
        chan = st.text_area("Changements pour la classe ?")
        
        if st.button("Sceller le parchemin 🖋️"):
            if succ and fail:
                xp_g, co_g = reward(40, 10)
                data = [st.session_state.user['nombre'], today, sent, succ, fail, chan, "", xp_g, co_g]
                if save_to_sheets(data):
                    st.success("Enregistré dans le royaume !")
                    time.sleep(1); st.session_state.user['view'] = 'Home'; st.rerun()
            else: st.error("Remplis les champs !")
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.user['view'] == 'Jeux':
        st.markdown("<div class='glass-panel'><h3>🎮 Salle d'entraînement</h3><p>Prochainement disponible...</p></div>", unsafe_allow_html=True)

    elif st.session_state.user['view'] == 'Boutique':
         st.markdown("<div class='glass-panel'><h1 class='fancy-title'>Boutique de l'Alchimiste</h1></div>", unsafe_allow_html=True)
         items = {"⚔️ Épée de Feu": 50, "🛡️ Bouclier Magique": 40, "🪖 Casque de Fer": 30, "🛡️ Armure en Or": 100}
         for item, precio in items.items():
            col1, col2 = st.columns([2, 1])
            col1.write(f"**{item}**")
            if item in st.session_state.user['inventario']: col2.button("Possédé", disabled=True, key=item)
            elif col2.button(f"Acheter {precio} 🪙", key=item):
                if st.session_state.user['monedas'] >= precio:
                    st.session_state.user['monedas'] -= precio
                    st.session_state.user['inventario'].append(item)
                    st.rerun()

    # Navegación fija abajo
    st.markdown("---")
    cols = st.columns(4)
    if cols[0].button("🏠 Foyer"): st.session_state.user['view'] = 'Home'; st.rerun()
    if cols[1].button("📝 Journal"): st.session_state.user['view'] = 'Journal'; st.rerun()
    if cols[2].button("🎮 Jeux"): st.session_state.user['view'] = 'Jeux'; st.rerun()
    if cols[3].button("💎 Boutique"): st.session_state.user['view'] = 'Boutique'; st.rerun()
