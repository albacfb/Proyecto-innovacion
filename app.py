import streamlit as st
import time
import random

# --- 1. CONFIGURACIÓN E INYECCIÓN DE DISEÑO "EPIC DRAGON CASTLE" ---
st.set_page_config(page_title="Les Dragons de l'Apprentissage", layout="centered", page_icon="🐉")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Quicksand:wght@400;600&display=swap');

    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
                    url('https://images.unsplash.com/photo-1578662996442-48f60103fc96?q=80&w=2070&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    .glass-panel {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 30px; padding: 30px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.7);
        text-align: center; margin-bottom: 20px;
    }

    /* ESTILO CARTAS DE MEMORIA */
    .stButton button {
        border-radius: 15px !important;
        height: 80px !important;
        font-weight: bold !important;
        font-size: 18px !important;
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
        'view': 'Home'
    }

# Estado del Juego de Memoria
if 'memory_cards' not in st.session_state:
    words = [("Prendre", "Pris"), ("Vendre", "Vendu"), ("Voir", "Vu"), ("Boire", "Bu")]
    deck = []
    for i, (inf, part) in enumerate(words):
        deck.append({'id': i, 'val': inf, 'type': 'inf'})
        deck.append({'id': i, 'val': part, 'type': 'part'})
    random.shuffle(deck)
    st.session_state.memory_cards = deck
    st.session_state.flipped = []
    st.session_state.matched = []

def reward(xp, coins):
    st.session_state.user['xp'] += xp
    st.session_state.user['monedas'] += coins

# --- 3. LÓGICA DE MINIJUEGOS ---

def memory_visual():
    st.markdown("### 🧠 Memory: Passé Composé")
    st.write("¡Gira las cartas y encuentra las parejas de verbos!")
    
    cards = st.session_state.memory_cards
    cols = st.columns(4)
    
    for idx, card in enumerate(cards):
        with cols[idx % 4]:
            if idx in st.session_state.matched:
                st.button(card['val'], key=f"matched_{idx}", disabled=True)
            elif idx in st.session_state.flipped:
                st.button(card['val'], key=f"flipped_{idx}")
            else:
                if st.button("❓", key=f"back_{idx}"):
                    if len(st.session_state.flipped) < 2:
                        st.session_state.flipped.append(idx)
                        st.rerun()

    if len(st.session_state.flipped) == 2:
        idx1, idx2 = st.session_state.flipped
        if cards[idx1]['id'] == cards[idx2]['id']:
            st.session_state.matched.extend([idx1, idx2])
            st.session_state.flipped = []
            reward(50, 20)
            st.success("¡Pareja encontrada! 🎉")
            time.sleep(1)
            st.rerun()
        else:
            st.error("No coinciden...")
            if st.button("Intentar de nuevo"):
                st.session_state.flipped = []
                st.rerun()

    if len(st.session_state.matched) == len(cards):
        st.balloons()
        st.success("¡Has completado el tablero! +50 XP")
        if st.button("Reiniciar Juego"):
            st.session_state.memory_cards = None # Forzar regeneración
            del st.session_state.memory_cards
            st.rerun()

# --- 4. VISTAS ---

if not st.session_state.user['setup_complete']:
    st.markdown("<div class='glass-panel'><h1 class='fancy-title'>Bienvenue</h1>", unsafe_allow_html=True)
    nombre = st.text_input("Nom de l'Apprenti:")
    if st.button("Lancer l'aventure"):
        st.session_state.user['nombre'] = nombre
        st.session_state.user['setup_complete'] = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    if st.session_state.user['view'] == 'Home':
        st.markdown(f"<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("<h1 class='fancy-title'>Les Dragons de l'Apprentissage</h1>", unsafe_allow_html=True)
        st.write(f"### {st.session_state.user['nombre']}")
        
        progress = min(st.session_state.user['xp'] / 1000 * 100, 100)
        st.markdown(f'<div class="xp-bg"><div class="xp-fill" style="width:{progress}%"></div></div>', unsafe_allow_html=True)
        st.write(f"✨ {st.session_state.user['xp']} XP | 🪙 {st.session_state.user['monedas']} Pièces")
        
        if st.session_state.user['inventario']:
            st.write("🎒 **Items:** " + ", ".join(st.session_state.user['inventario']))
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.user['view'] == 'Jeux':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("<h1 class='fancy-title'>Salle d'Entraînement</h1>", unsafe_allow_html=True)
        memory_visual()
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.user['view'] == 'Boutique':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("<h2 class='fancy-title'>La Grotte aux Trésors</h2>", unsafe_allow_html=True)
        st.write(f"Monedas: {st.session_state.user['monedas']} 🪙")
        items = [{"n": "Couronne", "c": 50, "i": "👑"}, {"n": "Ailes", "c": 150, "i": "🔥"}, {"n": "Épée", "c": 80, "i": "🗡️"}]
        cols = st.columns(3)
        for i, it in enumerate(items):
            with cols[i]:
                st.write(f"{it['i']}\n**{it['n']}**")
                if st.button(f"{it['c']} 🪙", key=it['n']):
                    if st.session_state.user['monedas'] >= it['c']:
                        st.session_state.user['monedas'] -= it['c']
                        st.session_state.user['inventario'].append(it['n'])
                        st.success("¡Comprado!")
                        st.rerun()
                    else: st.error("No tienes suficiente oro.")
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.user['view'] == 'Registro':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("<h2 class='fancy-title'>Mon Journal</h2>", unsafe_allow_html=True)
        appris = st.text_area("Ce que j'ai appris...")
        duda = st.text_area("Mes doutes (Error = Progrès)")
        if st.button("Sauvegarder"):
            reward(50 if duda else 25, 20)
            st.session_state.user['view'] = 'Home'; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # NAVEGACIÓN
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("🏠"): st.session_state.user['view'] = 'Home'; st.rerun()
    if c2.button("📝"): st.session_state.user['view'] = 'Registro'; st.rerun()
    if c3.button("⚔️"): st.session_state.user['view'] = 'Jeux'; st.rerun()
    if c4.button("💎"): st.session_state.user['view'] = 'Boutique'; st.rerun()
