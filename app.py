import streamlit as st
import time
import random
import os

# --- 1. CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="Les Dragons de l'Apprentissage", layout="centered", page_icon="🐉")

fondo_reino = "https://images.unsplash.com/photo-1514373941175-0a1410629892?q=80&w=2070&auto=format&fit=crop"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Quicksand:wght@400;600&display=swap');
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('{fondo_reino}');
        background-size: cover; background-position: center; background-attachment: fixed;
    }}
    .glass-panel {{
        background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 30px; padding: 25px;
        text-align: center; margin-bottom: 20px; color: white;
    }}
    .fancy-title {{ font-family: 'Cinzel', serif; color: #fcd34d !important; text-shadow: 2px 2px 10px black; }}
    .stButton button {{ border-radius: 12px; font-weight: bold; width: 100%; transition: 0.3s; }}
    .stButton button:hover {{ transform: scale(1.05); background-color: #fcd34d; color: black; }}
    </style>
""", unsafe_allow_html=True)

# --- 2. ESTADO DEL JUEGO ---
if 'user' not in st.session_state:
    st.session_state.user = {
        'nombre': 'Apprenti', 'xp': 0, 'monedas': 100, 'view': 'Home', 
        'setup_complete': False, 'inventario': []
    }

fases_dragon = {"Oeuf": "huevo.png", "Bébé": "bebe.png", "Expert": "experto.png", "Maître": "adulto.png"}

def reward(xp, coins):
    st.session_state.user['xp'] += xp
    st.session_state.user['monedas'] += coins

def obtener_fase(xp):
    if xp < 150: return "Oeuf"
    elif xp < 400: return "Bébé"
    elif xp < 800: return "Expert"
    else: return "Maître"

# --- 3. MINIJUEGOS ---

def minijuego_sopa():
    st.markdown("### 🔍 Mots Mêlés (Sopa de Letras)")
    st.write("Encuentra los verbos en infinitivo ocultos:")
    palabras = ["AVOIR", "ÊTRE", "ALLER", "FAIRE"]
    # Rejilla visual simple
    st.code("A V O I R X P\nL L F A I R E\nL E T R E Z Q\nE R G T B C M")
    intento = st.text_input("Escribe una palabra que hayas encontrado:").upper()
    if st.button("Vérifier 🔍"):
        if intento in palabras:
            reward(30, 15)
            st.success(f"¡Bien! Has encontrado {intento}. +30 XP")
        else:
            st.error("Esa palabra no está o ya la encontraste.")

def minijuego_duelo():
    st.markdown("### ⚔️ Le Duel du Chevalier")
    st.write("El caballero te bloquea el paso. ¡Elige la forma correcta del verbo!")
    pregunta = "¿Cómo se dice 'Nosotros hemos terminado'?"
    opciones = ["Nous avons fini", "Nous sommes fini", "Nous avons finu"]
    eleccion = st.radio(pregunta, opciones)
    if st.button("¡Lanzar Hechizo! ✨"):
        if eleccion == "Nous avons fini":
            reward(50, 20)
            st.balloons()
            st.success("¡Victoria! El caballero se retira. +50 XP / +20 🪙")
        else:
            st.error("¡Oh no! Has fallado el ataque.")

# --- 4. VISTAS ---

if not st.session_state.user['setup_complete']:
    st.markdown("<div class='glass-panel'><h1 class='fancy-title'>Bienvenue</h1>", unsafe_allow_html=True)
    st.session_state.user['nombre'] = st.text_input("Ton nom, Apprenti:")
    if st.button("Commencer ⚔️"):
        st.session_state.user['setup_complete'] = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    fase = obtener_fase(st.session_state.user['xp'])
    
    if st.session_state.user['view'] == 'Home':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown(f"<h1 class='fancy-title'>Niveau {fase}</h1>", unsafe_allow_html=True)
        if os.path.exists(fases_dragon[fase]):
            st.image(fases_dragon[fase], width=300)
        else:
            st.warning(f"Sube {fases_dragon[fase]} para ver el dragón.")
        st.write(f"### {st.session_state.user['nombre']}")
        st.write(f"✨ {st.session_state.user['xp']} XP | 🪙 {st.session_state.user['monedas']} Pièces")
        st.write(f"🎒 Inventaire: {', '.join(st.session_state.user['inventario']) if st.session_state.user['inventario'] else 'Vide'}")
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.user['view'] == 'Journal':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("<h2 class='fancy-title'>Mon Journal</h2>", unsafe_allow_html=True)
        st.select_slider("Sentiment:", ["😞", "😐", "🙂", "🤩"])
        st.text_area("Aujourd'hui, j'ai réussi à...")
        st.text_area("Je n'ai pas réussi à...")
        if st.button("Enregistrer 📝"):
            reward(40, 10)
            st.success("Réflexion enregistrée ! +40 XP")
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.user['view'] == 'Jeux':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        tipo_juego = st.selectbox("Choisis un défi:", ["Sopa de Letras", "Duelo del Caballero", "Cartas Memory"])
        if tipo_juego == "Sopa de Letras": minijuego_sopa()
        elif tipo_juego == "Duelo del Caballero": minijuego_duelo()
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.user['view'] == 'Boutique':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("<h2 class='fancy-title'>Armurerie Royale</h2>", unsafe_allow_html=True)
        st.write(f"Ton Or: {st.session_state.user['monedas']} 🪙")
        
        items = {
            "⚔️ Épée de Feu": 50,
            "🛡️ Bouclier Magique": 40,
            "🪖 Casque de Fer": 30,
            "🛡️ Armure en Or": 100
        }
        
        for item, precio in items.items():
            col1, col2 = st.columns([2, 1])
            col1.write(f"**{item}**")
            if col2.button(f"Acheter ({precio} 🪙)", key=item):
                if st.session_state.user['monedas'] >= precio:
                    st.session_state.user['monedas'] -= precio
                    st.session_state.user['inventario'].append(item)
                    st.success(f"¡Has comprado {item}!")
                    st.rerun()
                else:
                    st.error("No tienes suficiente oro.")
        st.markdown("</div>", unsafe_allow_html=True)

    # NAVEGACIÓN
    cols = st.columns(4)
    if cols[0].button("🏠 Foyer"): st.session_state.user['view'] = 'Home'; st.rerun()
    if cols[1].button("📝 Journal"): st.session_state.user['view'] = 'Journal'; st.rerun()
    if cols[2].button("🎮 Jeux"): st.session_state.user['view'] = 'Jeux'; st.rerun()
    if cols[3].button("💎 Boutique"): st.session_state.user['view'] = 'Boutique'; st.rerun()
