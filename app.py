import streamlit as st
import time
import random

# --- 1. CONFIGURACIÓN Y ESTÉTICA "DRAGON & CASTLE" ---
st.set_page_config(page_title="Les Dragons de l'Apprentissage", layout="centered", page_icon="🐉")

# CSS: Incluye el fondo, el sprite flotante y el nuevo efecto de fuego
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Quicksand:wght@400;600&display=swap');

    /* FONDO DE CASTILLO ÉPICO Y DRAGÓN */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), 
                    url('https://images.unsplash.com/photo-1599423300746-b62533397364?q=80&w=2070&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* CONTENEDOR SPRITE ANIMADO */
    .dragon-container {
        position: relative;
        width: 200px;
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

    /* EFECTO DE FUEGO (Solo activo en racha) */
    .fire-effect {
        position: absolute;
        top: 0; left: 25px;
        width: 150px; height: 150px;
        background: radial-gradient(circle, rgba(255,69,0,0.8) 0%, rgba(255,140,0,0) 70%);
        filter: blur(10px);
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

    .glass-panel {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 30px;
        padding: 30px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.6);
        text-align: center;
    }

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
        'fase': 'Oeuf',
        'view': 'Home',
        'on_fire': False  # Estado para el efecto de fuego
    }

# --- 3. LÓGICA DE MINIJUEGO ---
def minijuego_ataque():
    st.markdown("### ⚔️ L'Attaque du Verbe")
    
    verbos = [
        {"inf": "Prendre", "opciones": ["Prendu", "Pris", "Prendé"], "correcta": "Pris"},
        {"inf": "Faire", "opciones": ["Fait", "Fas", "Faisé"], "correcta": "Fait"},
        {"inf": "Voir", "opciones": ["Voyé", "Vu", "Voiré"], "correcta": "Vu"}
    ]
    
    reto = random.choice(verbos)
    st.write(f"Quel es le participe passé de: **{reto['inf']}**?")
    
    cols = st.columns(3)
    for i, opcion in enumerate(reto['opciones']):
        if cols[i].button(opcion, key=f"btn_{opcion}"):
            if opcion == reto['correcta']:
                st.session_state.user['on_fire'] = True
                st.session_state.user['xp'] += 30
                st.session_state.user['monedas'] += 15
                st.success("¡CORRECTO! ¡Tu dragón está en llamas! 🔥")
                time.sleep(1)
            else:
                st.session_state.user['on_fire'] = False
                st.error("Incorrecto... el fuego se apagó.")

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
    # Determinar si aplicar la clase CSS de fuego
    fire_class = "on-fire" if st.session_state.user['on_fire'] else ""

    if st.session_state.user['view'] == 'Home':
        st.markdown(f"<div class='glass-panel {fire_class}'>", unsafe_allow_html=True)
        st.markdown("<h1 class='fancy-title'>Les Dragons de l'Apprentissage</h1>", unsafe_allow_html=True)
        
        # DRAGÓN CON POSIBLE EFECTO DE FUEGO
        st.markdown(f"""
            <div class="dragon-container">
                <div class="fire-effect"></div>
                <img src="https://cdn-icons-png.flaticon.com/512/616/616430.png" class="dragon-sprite">
            </div>
        """, unsafe_allow_html=True)
        
        st.write(f"### {st.session_state.user['nombre']}")
        st.write(f"🪙 {st.session_state.user['monedas']} | ✨ {st.session_state.user['xp']} XP")
        if st.session_state.user['on_fire']:
            st.warning("¡MODO FUEGO ACTIVO! Ganas más XP")
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.user['view'] == 'Registro':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("<h2 class='fancy-title'>Mon Journal</h2>", unsafe_allow_html=True)
        appris = st.text_area("Hoy aprendí...")
        duda = st.text_area("No entendí...")
        if st.button("Sauvegarder"):
            st.session_state.user['xp'] += 40
            st.session_state.user['view'] = 'Home'; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.user['view'] == 'Jeux':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        minijuego_ataque()
        if st.button("Retour"): st.session_state.user['view'] = 'Home'; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # NAVEGACIÓN
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("🏠"): st.session_state.user['view'] = 'Home'; st.rerun()
    if c2.button("📝"): st.session_state.user['view'] = 'Registro'; st.rerun()
    if c3.button("⚔️"): st.session_state.user['view'] = 'Jeux'; st.rerun()
