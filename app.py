import streamlit as st
import time
import random

# --- 1. CONFIGURACIÓN E INYECCIÓN DE DISEÑO "TABLET FANTASY" ---
st.set_page_config(page_title="Les Dragons de l'Apprentissage", layout="centered", page_icon="🐉")

# CSS para imitar la imagen: Mapa de Francia de fondo, Glassmorphism y Sidebar
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Quicksand:wght@400;600&display=swap');

    .stApp {
        background: linear-gradient(rgba(15, 23, 42, 0.8), rgba(15, 23, 42, 0.8)), 
                    url('https://img.freepik.com/free-vector/france-map-with-landmarks-illustration_52683-47535.jpg');
        background-size: cover;
        background-position: center;
        color: #f8fafc;
        font-family: 'Quicksand', sans-serif;
    }

    /* Estilo de la Tarjeta Central (Glassmorphism de la imagen) */
    .glass-panel {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 30px;
        padding: 40px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        text-align: center;
        margin-top: 20px;
    }

    .fancy-title {
        font-family: 'Cinzel', serif;
        font-size: 2.5rem !important;
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin-bottom: 5px;
    }

    /* Sidebar de Evolución (Derecha) */
    .evo-sidebar {
        position: fixed;
        right: 30px;
        top: 25%;
        display: flex;
        flex-direction: column;
        gap: 20px;
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 50px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .evo-step { font-size: 30px; opacity: 0.3; filter: grayscale(1); transition: 0.5s; }
    .evo-active { opacity: 1; filter: grayscale(0); transform: scale(1.3); }

    /* Botones Estilo App */
    .stButton button {
        border-radius: 20px !important;
        padding: 10px 24px !important;
        background: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        font-weight: bold !important;
        transition: 0.3s !important;
    }
    .stButton button:hover { background: rgba(255, 255, 255, 0.4) !important; transform: translateY(-2px); }

    /* Barra de Progreso */
    .xp-bg { width: 100%; background: rgba(255,255,255,0.1); border-radius: 20px; height: 12px; margin: 10px 0; }
    .xp-fill { height: 100%; border-radius: 20px; background: linear-gradient(90deg, #fbbf24, #f59e0b); }

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
        'inventario': [],
        'fase': 'Oeuf',
        'view': 'Home'
    }

ASSETS = {
    "Oeuf": "https://cdn-icons-png.flaticon.com/512/3232/3232670.png",
    "Bébé": "https://cdn-icons-png.flaticon.com/512/7880/7880222.png",
    "Jeune": "https://cdn-icons-png.flaticon.com/512/1625/1625348.png",
    "Ailé": "https://cdn-icons-png.flaticon.com/512/4699/4699313.png"
}

# --- 3. LÓGICA DE EVOLUCIÓN ---
def check_evolution():
    xp = st.session_state.user['xp']
    if xp >= 700: st.session_state.user['fase'] = "Ailé"
    elif xp >= 300: st.session_state.user['fase'] = "Jeune"
    elif xp >= 100: st.session_state.user['fase'] = "Bébé"
    else: st.session_state.user['fase'] = "Oeuf"

# --- 4. NAVEGACIÓN Y VISTAS ---
if not st.session_state.user['setup_complete']:
    st.markdown("<div class='glass-panel'><h1 class='fancy-title'>Bienvenue</h1><p>Configura tu compañero</p>", unsafe_allow_html=True)
    nombre = st.text_input("Nom de l'Apprenti:")
    color = st.color_picker("Couleur de ton dragon:", "#FFD700")
    if st.button("Éclore l'oeuf 🥚"):
        st.session_state.user['nombre'] = nombre
        st.session_state.user['dragon_color'] = color
        st.session_state.user['setup_complete'] = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    check_evolution()
    fase = st.session_state.user['fase']
    
    # Sidebar Visual (Como en la imagen)
    st.markdown(f"""
        <div class="evo-sidebar">
            <div class="evo-step {'evo-active' if fase == 'Ailé' else ''}">🐉</div>
            <div class="evo-step {'evo-active' if fase == 'Jeune' else ''}">🦖</div>
            <div class="evo-step {'evo-active' if fase == 'Bébé' else ''}">👶</div>
            <div class="evo-step {'evo-active' if fase == 'Oeuf' else ''}">🥚</div>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.user['view'] == 'Home':
        st.markdown(f"<div class='glass-panel'><h1 class='fancy-title'>Les Dragons de l'Apprentissage</h1>", unsafe_allow_html=True)
        st.markdown(f"<img src='{ASSETS[fase]}' width='220' style='filter: drop-shadow(0 0 15px {st.session_state.user['dragon_color']}); margin-bottom: 20px;'>", unsafe_allow_html=True)
        st.write(f"### {st.session_state.user['nombre']} - Stade {fase}")
        
        # Barra de XP
        progress = min(st.session_state.user['xp'] / 1000 * 100, 100)
        st.markdown(f'<div class="xp-bg"><div class="xp-fill" style="width:{progress}%"></div></div>', unsafe_allow_html=True)
        st.caption(f"XP: {st.session_state.user['xp']} | Pièces: {st.session_state.user['monedas']} 🪙")
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.user['view'] == 'Registro':
        st.markdown("<div class='glass-panel'><h2>Mon Journal de Français</h2>", unsafe_allow_html=True)
        mood = st.select_slider("Mon Humeur du Jour", ["😴", "😐", "🙂", "🔥"])
        appris = st.text_area("Ce que j'ai appris aujourd'hui...")
        duda = st.text_area("Ce que je n'ai pas compris (Error = Progress!)")
        
        if st.button("Enregistrer"):
            xp_ganado = 20 if appris else 10
            bonus_error = 30 if duda else 0
            st.session_state.user['xp'] += (xp_ganado + bonus_error)
            st.session_state.user['monedas'] += 10
            
            if duda:
                st.balloons()
                st.success("Bravo! Valorar tus dudas te hace evolucionar más rápido.")
            
            time.sleep(2)
            st.session_state.user['view'] = 'Home'
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.user['view'] == 'Tienda':
        st.markdown("<div class='glass-panel'><h2>La Grotte aux Trésors 💎</h2>", unsafe_allow_html=True)
        st.write(f"Tu as **{st.session_state.user['monedas']}** pièces 🪙")
        
        items = [
            {"name": "Couronne Royale", "cost": 30, "icon": "👑"},
            {"name": "Ailes de Feu", "cost": 50, "icon": "🔥"},
            {"name": "Livre de Magie", "cost": 20, "icon": "📖"}
        ]
        
        cols = st.columns(3)
        for i, item in enumerate(items):
            with cols[i]:
                st.write(f"{item['icon']}\n**{item['name']}**")
                if st.button(f"Acheter ({item['cost']} 🪙)", key=item['name']):
                    if st.session_state.user['monedas'] >= item['cost']:
                        st.session_state.user['monedas'] -= item['cost']
                        st.session_state.user['inventario'].append(item['name'])
                        st.success(f"¡{item['name']} comprado!")
                        st.rerun()
                    else:
                        st.error("¡No tienes suficientes monedas!")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- DOCK DE NAVEGACIÓN INFERIOR ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    nav_cols = st.columns(3)
    with nav_cols[0]:
        if st.button("🏠 Home", use_container_width=True): st.session_state.user['view'] = 'Home'; st.rerun()
    with nav_cols[1]:
        if st.button("➕ Journal", use_container_width=True): st.session_state.user['view'] = 'Registro'; st.rerun()
    with nav_cols[2]:
        if st.button("💎 Grotte", use_container_width=True): st.session_state.user['view'] = 'Tienda'; st.rerun()
