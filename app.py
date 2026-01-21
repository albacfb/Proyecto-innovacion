import streamlit as st
import time
import random
import os
from datetime import date
import gspread
import json

# --- 1. CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="Le Royaume des Savoirs", layout="centered", page_icon="🗺️")

# Fondo de castillo épico con dragón
fondo_url = "https://cdn.pixabay.com/photo/2022/11/04/10/24/dragon-7569512_1280.jpg"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Quicksand:wght@400;600&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('{fondo_url}');
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* Estilo Pergamino Medieval */
    .parchment {{
        background: #fdf5e6;
        background-image: url("https://www.transparenttextures.com/patterns/old-paper.png");
        padding: 30px; border-radius: 10px; border: 5px double #8b4513;
        color: #3e2723; font-family: 'Quicksand', sans-serif;
        box-shadow: 10px 10px 20px rgba(0,0,0,0.5);
    }}

    /* Animación flotante para el dragón */
    @keyframes floating {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-20px); }}
        100% {{ transform: translateY(0px); }}
    }}
    .dragon-float {{ animation: floating 3s ease-in-out infinite; text-align: center; }}

    .glass-panel {{
        background: rgba(0, 0, 0, 0.7); backdrop-filter: blur(10px);
        border: 2px solid #fcd34d; border-radius: 20px; padding: 20px;
        color: white; margin-bottom: 20px;
    }}

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

# --- 2. ESTADO DEL JUEGO (REFORZADO) ---
if 'user' not in st.session_state:
    st.session_state.user = {
        'nombre': 'Apprenti', 'xp': 0, 'monedas': 100, 'view': 'Home', 
        'reino_actual': 'Mapa', 'inventario': [], 'last_login': None,
        'setup_complete': False
    }

# Asegurar que las nuevas claves existan para usuarios antiguos (Evita KeyError)
if 'reino_actual' not in st.session_state.user:
    st.session_state.user['reino_actual'] = 'Mapa'

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

# --- 3. CONTENIDO DE LOS REINOS ---

def valle_mates():
    st.markdown("<div class='parchment'><h3>🔢 Valle de las Matemáticas</h3><p>Resuelve el enigma para ganar oro:</p></div>", unsafe_allow_html=True)
    n1, n2 = random.randint(1, 10), random.randint(1, 10)
    ans = st.number_input(f"¿Cuánto es {n1} x {n2}?", step=1)
    if st.button("Lanzar Hechizo"):
        if ans == n1 * n2:
            xp, co = reward(30, 15)
            st.success(f"¡Magia pura! +{xp} XP / +{co} 🪙")
        else: st.error("El hechizo se ha disuelto...")

def reino_frances():
    st.markdown("<div class='parchment'><h2>🇫🇷 Royaume du Français</h2><p>Traduction rapide :</p></div>", unsafe_allow_html=True)
    op = st.radio("¿Cómo se dice 'Escuela'?", ["L'école", "Le château", "La forêt"])
    if st.button("Vérifier"):
        if op == "L'école":
            xp, co = reward(30, 15)
            st.success("Magnifique ! +30 XP")
        else: st.error("Oups... réessaye !")

# --- 4. VISTAS PRINCIPALES ---

if not st.session_state.user['setup_complete']:
    st.markdown("<div class='glass-panel'><h1 class='fancy-title'>Bienvenue</h1>", unsafe_allow_html=True)
    st.session_state.user['nombre'] = st.text_input("Comment t'appelles-tu, voyageur ?")
    if st.button("Lancer l'aventure ⚔️"):
        st.session_state.user['setup_complete'] = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # Cofre diario
    today = str(date.today())
    if st.session_state.user['last_login'] != today:
        st.session_state.user['last_login'] = today
        reward(20, 50)
        st.toast("🎁 Bonus quotidien reçu !", icon="💰")

    # BARRA DE NAVEGACIÓN SUPERIOR
    menu = st.tabs(["🏠 Foyer", "🗺️ Carte des Royaumes", "📜 Journal", "💎 Boutique"])

    with menu[0]: # HOME
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        fase = obtener_fase(st.session_state.user['xp'])
        st.markdown(f"<h1 class='fancy-title'>Niveau : {fase}</h1>", unsafe_allow_html=True)
        
        # Dragón flotante
        st.markdown('<div class="dragon-float">', unsafe_allow_html=True)
        if os.path.exists(fases_dragon[fase]): st.image(fases_dragon[fase], width=300)
        else: st.image("https://cdn-icons-png.flaticon.com/512/3069/3069418.png", width=200) # Imagen backup
        st.markdown('</div>', unsafe_allow_html=True)

        st.write(f"### Chevalier {st.session_state.user['nombre']}")
        st.write(f"✨ {st.session_state.user['xp']} XP | 🪙 {st.session_state.user['monedas']} Pièces")
        st.markdown("</div>", unsafe_allow_html=True)

    with menu[1]: # MAPA
        st.markdown("<h2 class='fancy-title'>Explore les Terres</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔢 Valle Matemático"): st.session_state.user['reino_actual'] = "Mates"
            if st.button("🔬 Labo Alquimia (Ciencias)"): st.session_state.user['reino_actual'] = "Ciencias"
        with col2:
            if st.button("🇫🇷 Royaume Français"): st.session_state.user['reino_actual'] = "Frances"
            if st.button("🎶 Templo Musical"): st.session_state.user['reino_actual'] = "Musica"
        
        st.markdown("---")
        if st.session_state.user['reino_actual'] == "Mates": valle_mates()
        elif st.session_state.user['reino_actual'] == "Frances": reino_frances()
        else: st.info("Selecciona un lugar en el mapa para empezar.")

    with menu[2]: # JOURNAL
        st.markdown('<div class="parchment">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>📜 Parchemin Royal</h2>", unsafe_allow_html=True)
        sent = st.select_slider("Ton moral", ["😞", "😐", "🙂", "🤩"])
        succ = st.text_area("Ma victoire du jour...")
        fail = st.text_area("Mon défi...")
        if st.button("Sceller 🖋️"):
            if succ and fail:
                xp_g, co_g = reward(40, 10)
                data = [st.session_state.user['nombre'], today, sent, succ, fail, "", "", xp_g, co_g]
                if save_to_sheets(data):
                    st.success("Parchemin envoyé al profesor !")
                    time.sleep(1); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with menu[3]: # BOUTIQUE
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("<h1 class='fancy-title'>Boutique de l'Alchimiste</h1>", unsafe_allow_html=True)
        items = {"⚔️ Épée de Feu (XP)": 50, "🛡️ Bouclier (Protección)": 40, "🛡️ Armure Or (Coins)": 100}
        for it, pr in items.items():
            c1, c2 = st.columns([3, 1])
            c1.write(f"**{it}**")
            if it in st.session_state.user['inventario']: c2.button("Poseído", disabled=True, key=it)
            elif c2.button(f"{pr} 🪙", key=it):
                if st.session_state.user['monedas'] >= pr:
                    st.session_state.user['monedas'] -= pr
                    st.session_state.user['inventario'].append(it)
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
