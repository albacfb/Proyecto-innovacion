import streamlit as st
import time
import random
import os
from datetime import date
import gspread # Necesitarás instalar esta librería: pip install gspread

# --- 1. CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="Les Dragons de l'Apprentissage", layout="centered", page_icon="🐉")

# Nuevo fondo épico
fondo_reino = "https://images.unsplash.com/photo-1547826039-bfc3ade20521?q=80&w=1932&auto=format&fit=crop" # Un paisaje de fantasía brillante y épico

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Quicksand:wght@400;600&display=swap');
    .stApp {{
        background: url('{fondo_reino}');
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

# --- CONFIGURACIÓN DE GOOGLE SHEETS ---
# INSTRUCCIONES:
# 1. Ve a Google Cloud Console (console.cloud.google.com).
# 2. Crea un nuevo proyecto.
# 3. Habilita la "Google Drive API" y la "Google Sheets API".
# 4. Crea una cuenta de servicio:
#    - Ve a "APIs y servicios" > "Credenciales".
#    - Haz clic en "Crear credenciales" > "Clave de cuenta de servicio".
#    - Elige "JSON" como tipo de clave y descárgala.
# 5. Guarda el contenido de ese archivo JSON en Streamlit Secrets
#    (en .streamlit/secrets.toml) bajo la clave `google_sheets_creds`.
#    Ejemplo:
#    google_sheets_creds = """
#    {
#      "type": "service_account",
#      "project_id": "tu-proyecto-id",
#      "private_key_id": "...",
#      "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
#      "client_email": "tu-cuenta-de-servicio@tu-proyecto-id.iam.gserviceaccount.com",
#      "client_id": "...",
#      "auth_uri": "...",
#      "token_uri": "...",
#      "auth_provider_x509_cert_url": "...",
#      "client_x509_cert_url": "..."
#    }
#    """
# 6. Crea una hoja de cálculo en Google Sheets. La primera hoja debe llamarse "JournalEntries".
# 7. Comparte esa hoja de cálculo con el "client_email" de tu cuenta de servicio (ver paso 5).

@st.cache_resource(ttl=3600)
def get_spreadsheet_client():
    creds = st.secrets["google_sheets_creds"]
    gc = gspread.service_account_from_dict(creds)
    # Abre tu hoja de cálculo por nombre
    spreadsheet = gc.open("JournalApprentices") # Reemplaza "JournalApprentices" con el nombre de tu hoja
    return spreadsheet

def save_journal_entry(nombre, fecha, sentimiento, success, fail, change, extra, xp, monedas):
    try:
        spreadsheet = get_spreadsheet_client()
        worksheet = spreadsheet.worksheet("JournalEntries") # Asegúrate de que tu primera hoja se llama "JournalEntries"
        
        # Añadir cabeceras si la hoja está vacía
        if not worksheet.row_values(1):
            worksheet.append_row(["Nombre", "Fecha", "Sentimiento", "J'ai réussi à", "Je n'ai pas réussi à", "Changements suggérés", "Extra", "XP Ganhada", "Monedas Ganadas"])

        worksheet.append_row([nombre, fecha, sentimiento, success, fail, change, extra, xp, monedas])
        st.success("Entrada del Journal guardada en Google Sheets.")
    except Exception as e:
        st.error(f"Error al guardar en Google Sheets: {e}")
        st.info("Asegúrate de haber configurado las credenciales y compartido la hoja de cálculo correctamente.")

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
    opciones = ["Nous avons fini", "Nous sommes fini", "Nous avons finu"] # Corregido "somos" por "sommes"
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
        xp_cofre, coins_cofre = reward(20, 50) # Cofre Diario
        st.toast(f"🎁 Coffre quotidien ouvert ! +{coins_cofre} 🪙 / +{xp_cofre} XP", icon="💰")

    fase = obtener_fase(st.session_state.user['xp'])
    
    if st.session_state.user['view'] == 'Home':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown(f"<h1 class='fancy-title'>Niveau {fase}</h1>", unsafe_allow_html=True)
        proximo = 150 if fase == "Oeuf" else 400 if fase == "Bébé" else 800 if fase == "Expert" else 1000
        porcentaje = min((st.session_state.user['xp'] / proximo) * 100, 100)
        st.markdown(f'<div class="progress-container"><div class="progress-bar" style="width: {porcentaje}%;"></div></div>', unsafe_allow_html=True)
        
        # No necesitas os.path.exists para una URL externa de imagen
        # if os.path.exists(fases_dragon[fase]):
        st.image(fases_dragon[fase], width=300)
        # else: st.warning(f"Téléchargez {fases_dragon[fase]}")
        
        st.write(f"### {st.session_state.user['nombre']}")
        st.write(f"✨ {st.session_state.user['xp']} XP | 🪙 {st.session_state.user['monedas']} Pièces")
        if st.session_state.user['inventario']:
            inv_html = "".join([f"<span class='item-tag'>{item}</span>" for item in st.session_state.user['inventario']])
            st.markdown(f"🎒 {inv_html}", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.user['view'] == 'Journal':
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("<h2 class='fancy-title'>Mon Journal</h2>", unsafe_allow_html=True)
        
        sentimiento = st.select_slider("Comment te sens-tu aujourd'hui ?", ["😞", "😐", "🙂", "🤩"])
        success = st.text_area("Aujourd'hui, j'ai réussi à... (Obligatoire)")
        fail = st.text_area("Je n'ai pas réussi à... (Obligatoire)")
        change = st.text_area("Qu'est-ce que tu changerais dans le cours d'aujourd'hui ?")
        extra = st.text_area("Y a-t-il autre chose que tu aimerais dire au dragon ?")
        
        if st.button("Enregistrer 📝"):
            if success.strip() and fail.strip(): # Validación
                bonus_xp_journal = 20 if "🪖 Casque de Fer" in st.session_state.user['inventario'] else 0
                xp_ganada, coins_ganadas = reward(40 + bonus_xp_journal, 10)
                
                # Guarda la entrada del journal en Google Sheets
                save_journal_entry(
                    st.session_state.user['nombre'],
                    today,
                    sentimiento,
                    success,
                    fail,
                    change,
                    extra,
                    xp_ganada, # Guardamos la XP final con bonus
                    coins_ganadas # Guardamos las monedas finales con bonus
                )
                st.success(f"Journal enregistré ! +{xp_ganada} XP / +{coins_ganadas} 🪙")
                time.sleep(1); st.session_state.user['view'] = 'Home'; st.rerun()
            else: st.error("Veuillez remplir les champs obligatoires 'J'ai réussi à...' et 'Je n'ai pas réussi à...'.")
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
        
        items = {
            "⚔️ Épée de Feu": {"p": 50, "d": "Augmente tous les gains d'XP de 20% !"},
            "🛡️ Bouclier Magique": {"p": 40, "d": "Protège tes pièces si tu échoues à un jeu."},
            "🪖 Casque de Fer": {"p": 30, "d": "Bonus de +20 XP quand tu enregistres ton Journal."},
            "🛡️ Armure en Or": {"p": 100, "d": "Augmente tous les gains de pièces de 50% !"}
        }
        
        for item, info in items.items():
            col1, col2 = st.columns([2, 1])
            col1.write(f"**{item}** ({info['p']} 🪙)\n\n*{info['d']}*")
            if item in st.session_state.user['inventario']: col2.button("Possédé", disabled=True, key=item)
            elif col2.button(f"Acheter", key=item): # Botón simplificado, el precio ya está en la descripción
                if st.session_state.user['monedas'] >= info['p']:
                    st.session_state.user['monedas'] -= info['p']
                    st.session_state.user['inventario'].append(item)
                    st.success(f"Vous avez acheté {item} !")
                    st.rerun()
                else: st.error("Pas assez de pièces !")
        st.markdown("</div>", unsafe_allow_html=True)

    cols = st.columns(4)
    if cols[0].button("🏠 Foyer"): st.session_state.user['view'] = 'Home'; st.rerun()
    if cols[1].button("📝 Journal"): st.session_state.user['view'] = 'Journal'; st.rerun()
    if cols[2].button("🎮 Jeux"): st.session_state.user['view'] = 'Jeux'; st.rerun()
    if cols[3].button("💎 Boutique"): st.session_state.user['view'] = 'Boutique'; st.rerun()
