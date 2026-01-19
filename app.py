import streamlit as st
import time
import random

# --- 1. CONFIGURACIÓN E INYECCIÓN DE DISEÑO "DRAGON & CASTLE" ---
st.set_page_config(page_title="Les Dragons de l'Apprentissage", layout="centered", page_icon="🐉")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Quicksand:wght@400;600&display=swap');

    /* FONDO DE CASTILLO ÉPICO Y DRAGÓN */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
                    url('https://images.unsplash.com/photo-1599423300746-b62533397364?q=80&w=2070&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* CONTENEDOR SPRITE ANIMADO */
    .dragon-container {
        position: relative;
        width: 180px;
        margin: 0 auto;
        padding: 20px;
    }

    .dragon-sprite {
        width: 150px;
        animation: float 3s ease-in-out infinite;
        transition: all 0.5s ease;
        z-index: 2;
        position: relative;
    }

    /* EFECTO DE FUEGO */
    .fire-effect {
        position: absolute;
        top: 0; left: 15px;
        width: 150px; height: 150px;
        background: radial-gradient(circle, rgba(255,69,0,0.8) 0%, rgba(255,140,0,0) 70%);
        filter: blur(15px);
        animation: flicker 0.2s infinite;
        z-index: 1;
        display: none;
    }

    .on-fire .fire-effect { display: block; }
    .on-fire .dragon-sprite { filter: drop-shadow(0 0 25px #ff4500) brightness(1.2); }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
        100% { transform: translateY(0px); }
    }

    @keyframes flicker {
        0% { opacity: 0.8; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.1); }
        100% { opacity: 0.8; transform: scale(1); }
    }

    /* PANELES Y BARRAS */
    .glass-panel {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 30px;
        padding: 30px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.7);
        text-align: center;
    }

    .xp-bg { width: 100%; background: rgba(255,255,255,0.1); border-radius: 15px; height: 14px; margin: 15px 0; border: 1px solid rgba(255,255,255,0.1); }
    .xp-fill { height: 100%; border-radius: 15px; background: linear-gradient(90deg, #fcd34d, #f59e0b); box-shadow: 0 0 10px gold; }

    .fancy-title { font-family: 'Cinzel', serif; color: #fcd34d !important; text-shadow: 2px 2px 8px black; }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 2. GESTIÓN DE ESTADO ---
if 'user' not in st.session_state:
    st.session_state.user = {
        'setup_complete': False,
        'nombre': 'Apprenti',
        'xp': 10,
        'monedas': 100,
        'inventario': [],
        'view': 'Home',
        'on_fire': False
    }

# --- 3. LOGICA DE RECOMPENSAS ---
def reward(xp_gain, coin_gain):
    st.session_state.user['xp'] += xp_gain
    st.session_state.user['monedas'] += coin_gain

# --- 4. VISTAS ---
if not st.session_state.user['setup_complete']:
    st.markdown("<div class='glass-panel'><h1 class='fancy-title'>Bienvenue</h1>", unsafe_allow_html=True)
    nombre = st.text_input("Nom de l'Apprenti:")
    if st.button("Lancer"):
        st.session_state.user['nombre'] = nombre
        st.session_state.user['setup_complete'] = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    fire_class = "on-fire" if st.session_state.user['on_fire'] else ""

    # --- PÁGINA PRINCIPAL (HOME) ---
    if st.session_state.user['view'] == 'Home':
        st.markdown(f"<div class='glass-panel {fire_class}'>", unsafe_allow_html=True)
        st.markdown("<h1 class='fancy-title'>Les Dragons de l'Apprentissage</h1>", unsafe_allow_html=True)
        
        # Sprite del Dragón
        st.markdown(f"""
            <div class="dragon-container">
                <div class="fire-effect"></div>
                <img src="https://cdn-icons-png.flaticon.com/512/616/616430.png" class="dragon-sprite">
            </div>
        """, unsafe_allow_html=True)
        
        st.write(f"### {st.session_state.user['nombre']}")
        
        # LÍNEA DE PROCESO (Barra de XP)
        progress = min(st.session_state.user['xp'] / 1000 * 100, 100)
        st.markdown(f'<div class="xp-bg"><div class="xp-fill" style="width:{progress}%"></div></div>', unsafe_allow_html=True)
        st.write(f"✨ {st.session_state.user['xp']} XP | 🪙 {st.session_state.user['monedas']} Pièces")
        
        if st.session_state.user['inventario']:
            st.write("🎒 **Items:** " + ", ".join(st.session_state.user['inventario']))
        st.markdown("</div>", unsafe_allow_html=True)

    # --- BOUTIQUE (RESTABLECIDA) ---
    elif st.session_state.user['view'] == 'Boutique':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("<h2 class='fancy-title'>La Grotte aux Trésors</h2>", unsafe_allow_html=True)
        st.write(f"Or disponible: {st.session_state.user['monedas']} 🪙")
        
        items = [
            {"name": "Couronne", "cost": 50, "icon": "👑"},
            {"name": "Ailes", "cost": 150, "icon": "🔥"},
            {"name": "Épée", "cost": 80, "icon": "🗡️"}
        ]
        
        cols = st.columns(3)
        for i, it in enumerate(items):
            with cols[i]:
                st.write(f"{it['icon']}\n**{it['name']}**")
                if st.button(f"{it['cost']} 🪙", key=it['name']):
                    if st.session_state.user['monedas'] >= it['cost']:
                        st.session_state.user['monedas'] -= it['cost']
                        st.session_state.user['inventario'].append(it['name'])
                        st.success("Acheté!")
                        st.rerun()
                    else:
                        st.error("Trop cher!")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- JOURNAL ---
    elif st.session_state.user['view'] == 'Registro':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("<h2 class='fancy-title'>Mon Journal</h2>", unsafe_allow_html=True)
        appris = st.text_area("Ce que j'ai appris...")
        duda = st.text_area("Mes doutes (Error = Progress!)")
        if st.button("Sauvegarder"):
            reward(50 if duda else 25, 20)
            st.session_state.user['view'] = 'Home'; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # --- JUEGOS ---
    elif st.session_state.user['view'] == 'Jeux':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.write("⚔️ ¡Derrota al caballero con el participio correcto!")
        if st.button("Prendre -> Pris"):
            st.session_state.user['on_fire'] = True
            reward(30, 15)
            st.success("¡FUEGO ACTIVADO!")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- NAVEGACIÓN ---
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("🏠"): st.session_state.user['view'] = 'Home'; st.rerun()
    if c2.button("📝"): st.session_state.user['view'] = 'Registro'; st.rerun()
    if c3.button("⚔️"): st.session_state.user['view'] = 'Jeux'; st.rerun()
    if c4.button("💎"): st.session_state.user['view'] = 'Boutique'; st.rerun()
