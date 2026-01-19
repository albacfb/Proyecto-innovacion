import streamlit as st
import time
import random
import os

# --- 1. CONFIGURACIÓN E IMAGEN DE FONDO ---
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
    .stButton button {{ border-radius: 12px; font-weight: bold; width: 100%; }}
    </style>
""", unsafe_allow_html=True)

# --- 2. GESTIÓN DE ESTADO ---
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

# --- 3. SECCIÓN DE JUEGOS ---

def duelo_caballero():
    st.markdown("### ⚔️ Le Duel du Chevalier")
    st.write("El Caballero Oscuro te bloquea el paso. ¡Usa la gramática para vencer!")
    pregunta = "¿Cuál es el auxiliar correcto para el verbo **'Aller'**?"
    opciones = ["Avoir", "Être", "Aller"]
    eleccion = st.radio(pregunta, opciones)
    if st.button("¡Atacar!"):
        if eleccion == "Être":
            st.success("¡Touché! Has vencido al caballero. +40 XP / +20 🪙")
            reward(40, 20)
        else:
            st.error("El caballero ha bloqueado tu ataque. ¡Repasa la lista de verbos 'Être'!")

def sopa_letras():
    st.markdown("### 🔍 Soupe de Mots")
    st.write("Encuentra el verbo oculto entre las letras: **P R E N D R E**")
    grid = """
    A B P R E N D R E X
    L O R Q W E R T Y U
    L P E Z X C V B N M
    E M N J K L H G F D
    R Q W E R T Y U I O
    """
    st.code(grid, language=None)
    respuesta = st.text_input("¿Qué verbo has encontrado?")
    if st.button("Verificar"):
        if respuesta.upper() == "PRENDRE" or respuesta.upper() == "ALLER":
            st.success("¡Excelente vista! +30 XP / +15 🪙")
            reward(30, 15)
        else:
            st.warning("Sigue buscando...")

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
        if os.path.exists(fases_dragon[fase]):
            st.image(fases_dragon[fase], width=300)
        else:
            st.info(f"Fase: {fase}")
        st.write(f"### {st.session_state.user['nombre']}")
        st.write(f"✨ {st.session_state.user['xp']} XP | 🪙 {st.session_state.user['monedas']} Pièces")
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.user['view'] == 'Journal':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("<h2 class='fancy-title'>Mon Journal</h2>", unsafe_allow_html=True)
        st.select_slider("Sentimiento", ["😞", "😐", "🙂", "🤩"])
        st.text_area("Aujourd'hui, j'ai réussi à...")
        st.text_area("Je n'ai pas réussi à...")
        if st.button("Sauvegarder 📝"):
            reward(50, 10)
            st.success("¡Progreso guardado!")
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.user['view'] == 'Jeux':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("<h2 class='fancy-title'>Zone de Jeux</h2>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["⚔️ Duel du Chevalier", "🔍 Soupe de Mots"])
        with tab1: duelo_caballero()
        with tab2: sopa_letras()
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.user['view'] == 'Boutique':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("<h2 class='fancy-title'>Boutique Magique</h2>", unsafe_allow_html=True)
        st.write(f"Tesoro: {st.session_state.user['monedas']} 🪙")
        
        productos = [
            ("🛡️ Bouclier d'Argent", 40),
            ("🧪 Potion de Grammaire", 25),
            ("📜 Parchemin Ancien", 60),
            ("✨ Baguette Magique", 100),
            ("👑 Couronne Royale", 250)
        ]
        
        for prod, precio in productos:
            col1, col2 = st.columns([2, 1])
            col1.write(f"{prod}")
            if col2.button(f"{precio} 🪙", key=prod):
                if st.session_state.user['monedas'] >= precio:
                    st.session_state.user['monedas'] -= precio
                    st.session_state.user['inventario'].append(prod)
                    st.success(f"¡Has comprado {prod}!")
                else:
                    st.error("¡No tienes suficientes monedas!")
        st.markdown("</div>", unsafe_allow_html=True)

    # NAVEGACIÓN
    st.markdown("<hr>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("🏠 Home"): st.session_state.user['view'] = 'Home'; st.rerun()
    if c2.button("📝 Journal"): st.session_state.user['view'] = 'Journal'; st.rerun()
    if c3.button("🎮 Jeux"): st.session_state.user['view'] = 'Jeux'; st.rerun()
    if c4.button("💎 Boutique"): st.session_state.user['view'] = 'Boutique'; st.rerun()
