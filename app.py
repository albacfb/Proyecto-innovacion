import streamlit as st
import time
import random
import pandas as pd

# --- 1. CONFIGURACIÓN E INYECCIÓN DE DISEÑO ---
st.set_page_config(page_title="Les Dragons de l'Apprentissage", layout="centered", page_icon="🐉")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Quicksand:wght@400;600&display=swap');

    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                    url('https://images.unsplash.com/photo-1599423300746-b62533397364?q=80&w=2070&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #f8fafc;
        font-family: 'Quicksand', sans-serif;
    }

    .glass-panel {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 35px;
        padding: 30px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
        text-align: center;
        margin-bottom: 20px;
    }

    .fancy-title {
        font-family: 'Cinzel', serif;
        font-size: 2rem !important;
        color: #fcd34d !important;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.8);
    }

    /* Estilo de botones de juegos */
    .game-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 10px;
        cursor: pointer;
        transition: 0.3s;
    }
    
    .letter-grid {
        display: grid;
        grid-template-columns: repeat(8, 1fr);
        gap: 5px;
        max-width: 400px;
        margin: auto;
    }
    
    .letter-cell {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 5px;
        padding: 10px;
        font-weight: bold;
        color: white;
    }

    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 2. GESTIÓN DE ESTADO ---
if 'user' not in st.session_state:
    st.session_state.user = {
        'setup_complete': False,
        'nombre': 'Apprenti',
        'dragon_color': '#FFD700',
        'xp': 10,
        'monedas': 0,
        'fase': 'Oeuf',
        'view': 'Home'
    }

if 'game_state' not in st.session_state:
    st.session_state.game_state = {
        'pair_selected': None,
        'soup_found': []
    }

# --- 3. LÓGICA DE JUEGOS ---

def render_match_pairs():
    st.subheader("🤝 Associer les Paires (Passé Composé)")
    pares = {"Manger": "Mangé", "Prendre": "Pris", "Vendre": "Vendu", "Être": "Été"}
    
    col1, col2 = st.columns(2)
    infinitivos = list(pares.keys())
    participios = list(pares.values())
    random.shuffle(infinitivos)
    random.shuffle(participios)
    
    with col1:
        inf = st.selectbox("Infinitif", ["Selecciona..."] + infinitivos)
    with col2:
        part = st.selectbox("Participe Passé", ["Selecciona..."] + participios)
        
    if st.button("Vérifier la paire"):
        if inf != "Selecciona..." and part != "Selecciona...":
            if pares.get(inf) == part:
                st.success(f"¡Correcto! {inf} -> {part}")
                st.session_state.user['xp'] += 10
                st.session_state.user['monedas'] += 5
                st.balloons()
            else:
                st.error("No es correcto, ¡sigue intentándolo!")

def render_word_search():
    st.subheader("🔍 Mots Mêlés (Sopa de Letras)")
    # Cuadrícula simplificada 8x8 con palabras ocultas: "EU", "FAIT", "MIS"
    grid = [
        ['F','A','I','T','X','Q','L','P'],
        ['A','Z','E','U','R','T','Y','O'],
        ['I','S','D','F','G','H','J','K'],
        ['T','M','I','S','L','Z','X','C'],
        ['B','N','M','Q','W','E','R','T'],
        ['A','S','D','F','G','H','J','K'],
        ['L','O','P','I','U','Y','T','R'],
        ['Q','W','E','R','T','Y','U','I']
    ]
    
    st.markdown("<div class='letter-grid'>", unsafe_allow_html=True)
    for row in grid:
        cols = st.columns(8)
        for i, char in enumerate(row):
            cols[i].markdown(f"<div class='letter-cell'>{char}</div>", unsafe_allow_html=True)
    
    palabra = st.text_input("¿Qué participio encontraste?").upper()
    if st.button("Valider le mot"):
        if palabra in ["FAIT", "EU", "MIS"]:
            st.success(f"¡Increíble! Encontraste {palabra}")
            st.session_state.user['xp'] += 15
            st.session_state.user['monedas'] += 10
        else:
            st.warning("Esa palabra no está o no es un participio válido.")

# --- 4. VISTAS PRINCIPALES ---

if not st.session_state.user['setup_complete']:
    st.markdown("<div class='glass-panel'><h1 class='fancy-title'>Bienvenue</h1>", unsafe_allow_html=True)
    st.session_state.user['nombre'] = st.text_input("Nom:")
    if st.button("Commencer"):
        st.session_state.user['setup_complete'] = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # Sidebar de evolución (simplificada para el ejemplo)
    st.sidebar.title(f"🐉 {st.session_state.user['fase']}")
    st.sidebar.metric("XP", st.session_state.user['xp'])
    st.sidebar.metric("Pièces", st.session_state.user['monedas'])

    if st.session_state.user['view'] == 'Home':
        st.markdown("<div class='glass-panel'><h1 class='fancy-title'>Les Dragons de l'Apprentissage</h1>", unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/1625/1625348.png", width=150)
        st.write(f"Bonjour, **{st.session_state.user['nombre']}**!")
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.user['view'] == 'Jeux':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("<h1 class='fancy-title'>Salle d'Entraînement</h1>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Unir Parejas", "Sopa de Letras"])
        with tab1:
            render_match_pairs()
        with tab2:
            render_word_search()
        st.markdown("</div>", unsafe_allow_html=True)

    # --- NAVEGACIÓN ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("🏠 Home"): st.session_state.user['view'] = 'Home'; st.rerun()
    if c2.button("🎮 Minijeux"): st.session_state.user['view'] = 'Jeux'; st.rerun()
    if c3.button("📝 Journal"): st.session_state.user['view'] = 'Registro'; st.rerun()
