import streamlit as st
import time
import random

# --- 1. CONFIGURACIÓN E INYECCIÓN DE DISEÑO ---
st.set_page_config(page_title="Les Dragons de l'Apprentissage", layout="centered", page_icon="🐉")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Quicksand:wght@400;600&display=swap');

    /* FONDO: DRAGÓN Y CASTILLO IMPRESIONANTE */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)), 
                    url('https://images.unsplash.com/photo-1578662996442-48f60103fc96?q=80&w=2070&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #f8fafc;
        font-family: 'Quicksand', sans-serif;
    }

    .glass-panel {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 35px;
        padding: 30px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8);
        text-align: center;
        margin-bottom: 20px;
    }

    .fancy-title {
        font-family: 'Cinzel', serif;
        font-size: 2.2rem !important;
        color: #fcd34d !important;
        text-shadow: 2px 2px 15px rgba(0,0,0,1);
    }

    /* Sidebar de Evolución */
    .evo-sidebar {
        position: fixed;
        right: 20px;
        top: 20%;
        display: flex;
        flex-direction: column;
        gap: 20px;
        background: rgba(0, 0, 0, 0.4);
        padding: 20px 10px;
        border-radius: 40px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .evo-step { font-size: 30px; opacity: 0.2; transition: 0.5s; }
    .evo-active { opacity: 1; transform: scale(1.3); filter: drop-shadow(0 0 10px gold); }

    .stButton button {
        border-radius: 15px !important;
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        font-weight: bold !important;
    }
    
    .xp-bg { width: 100%; background: rgba(255,255,255,0.1); border-radius: 10px; height: 12px; margin: 10px 0; }
    .xp-fill { height: 100%; border-radius: 10px; background: linear-gradient(90deg, #fcd34d, #fbbf24); }

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
        'monedas': 50, # Empezamos con algo de oro
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

# --- 4. VISTAS PRINCIPALES ---

if not st.session_state.user['setup_complete']:
    st.markdown("<div class='glass-panel'><h1 class='fancy-title'>Bienvenue</h1>", unsafe_allow_html=True)
    nombre = st.text_input("Comment t'appelles-tu ?")
    color = st.color_picker("Couleur de ton dragon", "#FFD700")
    if st.button("Commencer l'aventure"):
        st.session_state.user['nombre'] = nombre
        st.session_state.user['dragon_color'] = color
        st.session_state.user['setup_complete'] = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    check_evolution()
    fase = st.session_state.user['fase']
    
    # Sidebar Visual
    st.markdown(f"""
        <div class="evo-sidebar">
            <div class="evo-step {'evo-active' if fase == 'Ailé' else ''}">🐉</div>
            <div class="evo-step {'evo-active' if fase == 'Jeune' else ''}">🦖</div>
            <div class="evo-step {'evo-active' if fase == 'Bébé' else ''}">👶</div>
            <div class="evo-step {'evo-active' if fase == 'Oeuf' else ''}">🥚</div>
        </div>
    """, unsafe_allow_html=True)

    # VISTA HOME
    if st.session_state.user['view'] == 'Home':
        st.markdown(f"<div class='glass-panel'><h1 class='fancy-title'>Bonjour, {st.session_state.user['nombre']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<img src='{ASSETS[fase]}' width='180' style='filter: drop-shadow(0 0 15px {st.session_state.user['dragon_color']});'>", unsafe_allow_html=True)
        
        progress = min(st.session_state.user['xp'] / 1000 * 100, 100)
        st.markdown(f'<div class="xp-bg"><div class="xp-fill" style="width:{progress}%"></div></div>', unsafe_allow_html=True)
        st.write(f"✨ {st.session_state.user['xp']} XP | 🪙 {st.session_state.user['monedas']} Pièces")
        
        if st.session_state.user['inventario']:
            st.write("🎒 **Ton Inventaire:** " + ", ".join(st.session_state.user['inventario']))
        st.markdown("</div>", unsafe_allow_html=True)

    # VISTA JOURNAL (CORREGIDA)
    elif st.session_state.user['view'] == 'Registro':
        st.markdown("<div class='glass-panel'><h2 class='fancy-title'>Mon Journal de Français</h2>", unsafe_allow_html=True)
        mood = st.select_slider("Mon Humeur", ["😴", "😐", "🙂", "🔥"])
        appris = st.text_area("Qu'est-ce que j'ai appris ?")
        duda = st.text_area("Ce que je n'ai pas compris (Valore ton erreur!)")
        
        if st.button("Enregistrer y Gagner XP"):
            puntos = 20 if appris else 10
            puntos += 40 if duda else 0 # Más puntos por identificar errores
            st.session_state.user['xp'] += puntos
            st.session_state.user['monedas'] += 20
            st.success(f"Bravo! +{puntos} XP y +20 🪙")
            time.sleep(1.5)
            st.session_state.user['view'] = 'Home'
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # VISTA TIENDA (BOUTIQUE)
    elif st.session_state.user['view'] == 'Boutique':
        st.markdown("<div class='glass-panel'><h2 class='fancy-title'>La Grotte aux Trésors</h2>", unsafe_allow_html=True)
        st.write(f"Tu as **{st.session_state.user['monedas']}** 🪙")
        
        tienda_items = [
            {"name": "Couronne Dorée", "cost": 50, "icon": "👑"},
            {"name": "Ailes de Feu", "cost": 100, "icon": "🔥"},
            {"name": "Épée Magique", "cost": 75, "icon": "🗡️"}
        ]
        
        cols = st.columns(3)
        for i, item in enumerate(tienda_items):
            with cols[i]:
                st.write(f"{item['icon']}\n**{item['name']}**")
                if st.button(f"{item['cost']} 🪙", key=item['name']):
                    if st.session_state.user['monedas'] >= item['cost']:
                        st.session_state.user['monedas'] -= item['cost']
                        st.session_state.user['inventario'].append(item['name'])
                        st.toast(f"Acheté: {item['name']}!")
                        st.rerun()
                    else:
                        st.error("Pas assez d'or!")
        st.markdown("</div>", unsafe_allow_html=True)

    # VISTA JUEGOS
    elif st.session_state.user['view'] == 'Jeux':
        st.markdown("<div class='glass-panel'><h2 class='fancy-title'>Minijeux</h2><p>Gagne des pièces et de l'XP!</p>", unsafe_allow_html=True)
        # Aquí iría el código de la sopa de letras y parejas que vimos antes
        st.write("🎮 ¡Entrena tu francés para conseguir más monedas!")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- NAVEGACIÓN DOCK ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    n1, n2, n3, n4 = st.columns(4)
    if n1.button("🏠 Home"): st.session_state.user['view'] = 'Home'; st.rerun()
    if n2.button("📝 Journal"): st.session_state.user['view'] = 'Registro'; st.rerun()
    if n3.button("🎮 Jeux"): st.session_state.user['view'] = 'Jeux'; st.rerun()
    if n4.button("💎 Boutique"): st.session_state.user['view'] = 'Boutique'; st.rerun()
