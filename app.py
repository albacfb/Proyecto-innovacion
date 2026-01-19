import streamlit as st
import time
import random
import os
from PIL import Image

# --- 1. CONFIGURACIÓN E IMAGEN DE FONDO ---
st.set_page_config(page_title="Les Dragons de l'Apprentissage", layout="centered", page_icon="🐉")

# URL de la imagen del Reino con Castillo
fondo_reino = "http://googleusercontent.com/image_collection/image_retrieval/3792873239093654663_0"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Quicksand:wght@400;600&display=swap');

    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), 
                    url('{fondo_reino}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .glass-panel {{
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 30px; padding: 25px;
        text-align: center; margin-bottom: 20px;
        color: white;
    }}

    /* ANIMACIÓN FLOTANTE PARA EL DRAGÓN */
    .dragon-anim {{
        animation: float 3.5s ease-in-out infinite;
        filter: drop-shadow(0 0 15px gold);
    }}

    @keyframes float {{
        0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
        50% {{ transform: translateY(-20px) rotate(1deg); }}
    }}

    .xp-bg {{ width: 100%; background: rgba(255,255,255,0.1); border-radius: 15px; height: 14px; margin: 15px 0; }}
    .xp-fill {{ height: 100%; border-radius: 15px; background: linear-gradient(90deg, #fcd34d, #f59e0b); transition: 0.5s; }}
    .fancy-title {{ font-family: 'Cinzel', serif; color: #fcd34d !important; text-shadow: 2px 2px 10px black; }}
    
    .stButton button {{ border-radius: 12px; font-weight: bold; }}
    </style>
""", unsafe_allow_html=True)

# --- 2. GESTIÓN DE ESTADO ---
if 'user' not in st.session_state:
    st.session_state.user = {
        'nombre': 'Apprenti', 'xp': 0, 'monedas': 100, 'view': 'Home', 
        'setup_complete': False, 'inventario': []
    }

# Lógica del Juego de Parejas
if 'cards' not in st.session_state:
    words = [("Manger", "Mangé"), ("Finir", "Fini"), ("Être", "Été"), ("Avoir", "Eu")]
    deck = []
    for i, (inf, part) in enumerate(words):
        deck.append({'id': i, 'val': inf})
        deck.append({'id': i, 'val': part})
    random.shuffle(deck)
    st.session_state.cards = deck
    st.session_state.flipped = []
    st.session_state.matched = []

fases_dragon = {
    "Oeuf": "huevo.png", "Bébé": "bebe.png", "Expert": "experto.png", "Maître": "adulto.png"
}

def reward(xp, coins):
    st.session_state.user['xp'] += xp
    st.session_state.user['monedas'] += coins

def obtener_fase(xp):
    if xp < 150: return "Oeuf"
    elif xp < 400: return "Bébé"
    elif xp < 800: return "Expert"
    else: return "Maître"

# --- 3. MINIJUEGOS ---

def minijuego_cartas():
    st.markdown("### 🧠 Memory: Passé Composé")
    cols = st.columns(4)
    for idx, card in enumerate(st.session_state.cards):
        with cols[idx % 4]:
            if idx in st.session_state.matched:
                st.button(card['val'], key=f"m_{idx}", disabled=True)
            elif idx in st.session_state.flipped:
                st.button(card['val'], key=f"f_{idx}")
            else:
                if st.button("❓", key=f"q_{idx}"):
                    if len(st.session_state.flipped) < 2:
                        st.session_state.flipped.append(idx)
                        st.rerun()
    
    if len(st.session_state.flipped) == 2:
        i1, i2 = st.session_state.flipped
        if st.session_state.cards[i1]['id'] == st.session_state.cards[i2]['id']:
            st.session_state.matched.extend([i1, i2])
            st.session_state.flipped = []
            reward(50, 25)
            st.success("¡Pareja encontrada! +50 XP")
            st.rerun()
        elif st.button("No coinciden. Reintentar"):
            st.session_state.flipped = []
            st.rerun()

def minijuego_caballero():
    st.markdown("### ⚔️ Batalla del Caballero")
    st.write("¿Cuál es el participio correcto de **'Prendre'** para derrotar al caballero?")
    ans = st.radio("Elige tu ataque:", ["Prendu", "Pris", "Prendé"])
    if st.button("¡Atacar!"):
        if ans == "Pris":
            reward(40, 20)
            st.success("¡Victoria! Caballero derrotado. +40 XP")
        else:
            st.error("¡Oh no! El ataque falló.")

# --- 4. VISTAS ---

if not st.session_state.user['setup_complete']:
    st.markdown("<div class='glass-panel'><h1 class='fancy-title'>Bienvenue</h1>", unsafe_allow_html=True)
    nombre = st.text_input("Ton nom, Apprenti:")
    if st.button("Commencer ⚔️"):
        st.session_state.user['nombre'] = nombre
        st.session_state.user['setup_complete'] = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    fase = obtener_fase(st.session_state.user['xp'])
    
    if st.session_state.user['view'] == 'Home':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown(f"<h1 class='fancy-title'>Niveau {fase}</h1>", unsafe_allow_html=True)
        
        # Imagen dinámica y animada
        try:
            st.image(fases_dragon[fase], width=300)
            # Nota: para aplicar la clase 'dragon-anim' de CSS, el st.image es limitado. 
            # Si los archivos están bien, podemos usar HTML:
            # st.markdown(f'<img src="{fases_dragon[fase]}" class="dragon-anim" width="300">', unsafe_allow_html=True)
        except:
            st.warning(f"Sube '{fases_dragon[fase]}' para ver tu dragón.")
            
        st.write(f"### {st.session_state.user['nombre']}")
        progreso = min(st.session_state.user['xp'] / 800 * 100, 100)
        st.markdown(f'<div class="xp-bg"><div class="xp-fill" style="width:{progreso}%"></div></div>', unsafe_allow_html=True)
        st.write(f"✨ {st.session_state.user['xp']} XP | 🪙 {st.session_state.user['monedas']} Pièces")
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.user['view'] == 'Jeux':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        game = st.selectbox("Challenge:", ["Cartas Memory", "Batalla Caballero"])
        if game == "Cartas Memory": minijuego_cartas()
        else: minijuego_caballero()
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.user['view'] == 'Boutique':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("<h2 class='fancy-title'>Boutique de Magie</h2>", unsafe_allow_html=True)
        st.write(f"Tesoro: {st.session_state.user['monedas']} 🪙")
        c1, c2 = st.columns(2)
        if c1.button("Épée de Feu (50 🪙)"):
            if st.session_state.user['monedas'] >= 50:
                st.session_state.user['monedas'] -= 50
                st.session_state.user['inventario'].append("Épée")
                st.success("¡Comprada!")
        st.markdown("</div>", unsafe_allow_html=True)

    # NAVEGACIÓN
    cols = st.columns(3)
    if cols[0].button("🏠 Foyer"): st.session_state.user['view'] = 'Home'; st.rerun()
    if cols[1].button("🎮 Entraînement"): st.session_state.user['view'] = 'Jeux'; st.rerun()
    if cols[2].button("💎 Boutique"): st.session_state.user['view'] = 'Boutique'; st.rerun()
