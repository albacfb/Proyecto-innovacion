import streamlit as st
import time
import random
import os
from datetime import date

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
    
    .progress-container {{ width: 100%; background-color: rgba(255, 255, 255, 0.1); border-radius: 20px; margin: 20px 0; border: 1px solid rgba(254, 211, 77, 0.3); overflow: hidden; }}
    .progress-bar {{ height: 20px; background: linear-gradient(90deg, #fcd34d, #f59e0b); box-shadow: 0 0 15px #fcd34d; transition: width 0.5s ease-in-out; }}
    
    .item-tag {{ background: rgba(252, 211, 77, 0.2); border: 1px solid #fcd34d; padding: 2px 8px; border-radius: 10px; font-size: 0.8rem; margin: 2px; display: inline-block; }}
    </style>
""", unsafe_allow_html=True)

# --- 2. ESTADO DEL JUEGO ---
if 'user' not in st.session_state:
    st.session_state.user = {
        'nombre': 'Apprenti', 'xp': 0, 'monedas': 100, 'view': 'Home', 
        'setup_complete': False, 'inventario': [],
        'last_login': None 
    }

fases_dragon = {"Oeuf": "huevo.png", "Bébé": "bebe.png", "Expert": "experto.png", "Maître": "adulto.png"}

def reward(xp, coins):
    if "⚔️ Épée de Feu" in st.session_state.user['inventario']:
        xp = int(xp * 1.2) # Bonus de XP
    if "🛡️ Armure en Or" in st.session_state.user['inventario']:
        coins = int(coins * 1.5) # Bonus de Monedas
    st.session_state.user['xp'] += xp
    st.session_state.user['monedas'] += coins
    return xp, coins

def obtener_fase(xp):
    if xp < 150: return "Oeuf"
    elif xp < 400: return "Bébé"
    elif xp < 800: return "Expert"
    else: return "Maître"

# --- 3. LÓGICA DE MINIJUEGOS ---

def minijuego_sopa():
    st.markdown("### 🔍 Mots Mêlés")
    st.code("A V O I R X P\nL L F A I R E\nL E T R E Z Q\nE R G T B C M")
    palabras = ["AVOIR", "ÊTRE", "ALLER", "FAIRE"]
    intento = st.text_input("Écris un mot que tu as trouvé :").upper()
    if st.button("Vérifier"):
        if intento in palabras:
            xp, coins = reward(30, 15)
            st.success(f"Bien joué ! +{xp} XP / +{coins} 🪙")
        else: st.error("Mot non trouvé.")

def minijuego_duelo():
    st.markdown("### ⚔️ Le Duel du Chevalier")
    opciones = ["Nous avons fini", "Nous somos fini", "Nous avons finu"]
    eleccion = st.radio("Comment dit-on 'Nosotros hemos terminado' ?", opciones)
    if st.button("Attaquer"):
        if eleccion == "Nous avons fini":
            xp, coins = reward(50, 20)
            st.balloons(); st.success(f"Victoire ! +{xp} XP")
        else:
            if "🛡️ Bouclier Magique" in st.session_state.user['inventario']:
                st.warning("Échec ! Mais le Bouclier t'a protégé.") # Protección
            else:
                st.error("Défaite ! -10 🪙"); st.session_state.user['monedas'] = max(0, st.session_state.user['monedas'] - 10)

def minijuego_traduccion():
    st.markdown("### ⚡ Traduction Rapide")
    frases = {"Bonjour": "Hola", "Merci": "Gracias", "S'il vous plaît": "Por favor", "L'école": "La escuela"}
    frase_fr = random.choice(list(frases.keys()))
    st.write(f"Traduisez : **{frase_fr}**")
    intento = st.text_input("Ta réponse :")
    if st.button("Valider"):
        if intento.lower() == frases[frase_fr].lower():
            xp, coins = reward(20, 10)
            st.success(f"Correct ! +{xp} XP")
        else: st.error("Incorrect.")

def minijuego_ortografia():
    st.markdown("### ✍️ Orthographe Magique")
    st.write("Lequel est correctement écrit ?")
    opciones = ["Beaucoup", "Beaucup", "Beacuop"]
    eleccion = st.radio("Choisis :", opciones)
    if st.button("Vérifier"):
        if eleccion == "Beaucoup":
            xp, coins = reward(25, 10)
            st.success(f"Bravo ! +{xp} XP")
        else: st.error("Oups !")

# --- 4. VISTAS ---

if not st.session_state.user['setup_complete']:
    st.markdown("<div class='glass-panel'><h1 class='fancy-title'>Bienvenue</h1>", unsafe_allow_html=True)
    st.session_state.user['nombre'] = st.text_input("Ton nom, Apprenti :")
    if st.button("Lancer l'aventure ⚔️"):
        st.session_state.user['setup_complete'] = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    today = str(date.today())
    if st.session_state.user['last_login'] != today:
        st.session_state.user['last_login'] = today
        st.balloons()
        xp, coins = reward(20, 50) # Cofre Diario
        st.toast(f"🎁 Coffre quotidien ouvert ! +{coins} 🪙 / +{xp} XP", icon="💰")

    fase = obtener_fase(st.session_state.user['xp'])
    
    if st.session_state.user['view'] == 'Home':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown(f"<h1 class='fancy-title'>Niveau {fase}</h1>", unsafe_allow_html=True)
        proximo = 150 if fase == "Oeuf" else 400 if fase == "Bébé" else 800 if fase == "Expert" else 1000
        porcentaje = min((st.session_state.user['xp'] / proximo) * 100, 100)
        st.markdown(f'<div class="progress-container"><div class="progress-bar" style="width: {porcentaje}%;"></div></div>', unsafe_allow_html=True)
        
        if os.path.exists(fases_dragon[fase]): st.image(fases_dragon[fase], width=300)
        else: st.warning(f"Téléchargez {fases_dragon[fase]}")
        
        st.write(f"### {st.session_state.user['nombre']}")
        st.write(f"✨ {st.session_state.user['xp']} XP | 🪙 {st.session_state.user['monedas']} Pièces")
        if st.session_state.user['inventario']:
            inv_html = "".join([f"<span class='item-tag'>{item}</span>" for item in st.session_state.user['inventario']])
            st.markdown(f"🎒 {inv_html}", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.user['view'] == 'Journal':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("<h2 class='fancy-title'>Mon Journal</h2>", unsafe_allow_html=True)
        st.select_slider("Comment te sens-tu aujourd'hui ?", ["😞", "😐", "🙂", "🤩"])
        
        success = st.text_area("Aujourd'hui, j'ai réussi à... (Obligatoire)")
        fail = st.text_area("Je n'ai pas réussi à... (Obligatoire)")
        change = st.text_area("Qu'est-ce que tu changerais dans le cours d'aujourd'hui ?")
        extra = st.text_area("Y a-t-il autre chose que tu aimerais dire au dragon ?")
        
        if st.button("Enregistrer 📝"):
            if success.strip() and fail.strip(): # Validación
                bonus = 20 if "🪖 Casque de Fer" in st.session_state.user['inventario'] else 0
                xp, coins = reward(40 + bonus, 10)
                st.success(f"Enregistré ! +{xp} XP")
                time.sleep(1); st.session_state.user['view'] = 'Home'; st.rerun()
            else: st.error("Veuillez remplir les champs obligatoires.")
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.user['view'] == 'Jeux':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        juego = st.selectbox("Choisis un jeu :", ["Sopa de Letras", "Duelo del Caballero", "Traducción Rápida", "Ortografía"])
        if juego == "Sopa de Letras": minijuego_sopa()
        elif juego == "Duelo del Caballero": minijuego_duelo()
        elif juego == "Traducción Rápida": minijuego_traduccion()
        elif juego == "Ortografía": minijuego_ortografia()
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.user['view'] == 'Boutique':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("<h2 class='fancy-title'>Armurerie</h2>", unsafe_allow_html=True)
        
        # Funciones de cada objeto
        items = {
            "⚔️ Épée de Feu": {"p": 50, "d": "+20% XP bonus"},
            "🛡️ Bouclier Magique": {"p": 40, "d": "Protège tes pièces"},
            "🪖 Casque de Fer": {"p": 30, "d": "Bonus XP au Journal"},
            "🛡️ Armure en Or": {"p": 100, "d": "+50% Pièces bonus"}
        }
        
        for item, info in items.items():
            col1, col2 = st.columns([2, 1])
            col1.write(f"**{item}**\n\n*{info['d']}*")
            if item in st.session_state.user['inventario']: col2.button("Possédé", disabled=True, key=item)
            elif col2.button(f"Acheter ({info['p']} 🪙)", key=item):
                if st.session_state.user['monedas'] >= info['p']:
                    st.session_state.user['monedas'] -= info['p']
                    st.session_state.user['inventario'].append(item)
                    st.rerun()
                else: st.error("Pas assez de pièces !")
        st.markdown("</div>", unsafe_allow_html=True)

    cols = st.columns(4)
    if cols[0].button("🏠 Foyer"): st.session_state.user['view'] = 'Home'; st.rerun()
    if cols[1].button("📝 Journal"): st.session_state.user['view'] = 'Journal'; st.rerun()
    if cols[2].button("🎮 Jeux"): st.session_state.user['view'] = 'Jeux'; st.rerun()
    if cols[3].button("💎 Boutique"): st.session_state.user['view'] = 'Boutique'; st.rerun()
