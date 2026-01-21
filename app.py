import streamlit as st
import time
import random
import os
from datetime import date
import gspread
import json
from PIL import Image # Importar para cargar imágenes locales

# --- 1. CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="Le Royaume des Savoirs", layout="wide", page_icon="🗺️")

# Ruta de la imagen del mapa (asegúrate de que está en la misma carpeta que app.py)
MAPA_IMAGEN_PATH = "mapa_reinos.png" 

# URL de imagen de fondo general (si quieres un fondo detrás del mapa)
fondo_general_url = "https://images.unsplash.com/photo-1599408162172-19bc30f65839?q=80&w=2070&auto=format&fit=crop"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Quicksand:wght@400;600&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{fondo_general_url}');
        background-size: cover; background-position: center; background-attachment: fixed;
        color: white;
    }}

    /* Contenedor principal del mapa */
    .map-container {{
        position: relative;
        width: 100%;
        max-width: 900px; /* Ancho máximo para el mapa */
        margin: 20px auto;
        border: 10px solid #8b4513;
        border-radius: 15px;
        box-shadow: 0 0 50px rgba(0,0,0,0.8);
        overflow: hidden; /* Asegura que el dragón no se salga de los bordes del mapa */
    }}
    
    .map-image {{
        width: 100%;
        height: auto;
        display: block;
        opacity: 0.9;
    }}

    /* DRAGON EN EL MAPA */
    .map-dragon-icon {{
        position: absolute;
        width: 80px; /* Tamaño del icono del dragón */
        height: 80px;
        background: url("https://cdn-icons-png.flaticon.com/512/3069/3069418.png"); /* Icono de dragón */
        background-size: cover;
        transform: translate(-50%, -50%); /* Centra el dragón en sus coordenadas */
        transition: left 1s ease-in-out, top 1s ease-in-out; /* Animación de movimiento */
        filter: drop-shadow(0 0 15px #fcd34d);
        z-index: 100; /* Asegura que esté por encima de todo */
    }}

    /* Estilo Pergamino */
    .parchment {{
        background: #fdf5e6;
        background-image: url("https://www.transparenttextures.com/patterns/old-paper.png");
        padding: 30px; border-radius: 10px; border: 4px solid #8b4513;
        color: #3e2723; font-family: 'Quicksand', sans-serif;
        box-shadow: 10px 10px 20px rgba(0,0,0,0.5);
    }}
    
    .fancy-title {{ font-family: 'Cinzel', serif; color: #fcd34d !important; text-shadow: 2px 2px 10px #000; text-align: center; }}
    </style>
""", unsafe_allow_html=True)

# --- CONEXIÓN A GOOGLE SHEETS ---
def save_to_sheets(data):
    try:
        creds_raw = st.secrets["google_sheets_creds"]
        creds_info = json.loads(creds_raw) if isinstance(creds_raw, str) else dict(creds_raw)
        gc = gspread.service_account_from_dict(creds_info)
        sh = gc.open("JournalApprentices").worksheet("JournalEntries")
        sh.append_row(data)
        return True
    except: return False

# --- 2. ESTADO DEL JUEGO (REFORZADO) ---
if 'user' not in st.session_state:
    st.session_state.user = {
        'nombre': 'Apprenti', 'xp': 0, 'monedas': 100, 'view': 'Home', 
        'reino_actual': None, 'inventario': [], 'last_login': None,
        'setup_complete': False,
        'dragon_pos_x': '50%', # Posición inicial del dragón en el centro del mapa
        'dragon_pos_y': '50%'
    }

# Asegurar que las nuevas claves existan
for key in ['reino_actual', 'setup_complete', 'dragon_pos_x', 'dragon_pos_y']:
    if key not in st.session_state.user: 
        if key == 'dragon_pos_x': st.session_state.user[key] = '50%'
        elif key == 'dragon_pos_y': st.session_state.user[key] = '50%'
        else: st.session_state.user[key] = None

def reward(xp, coins):
    st.session_state.user['xp'] += xp
    st.session_state.user['monedas'] += coins
    return xp, coins

# --- 3. CONTENIDO DE LOS REINOS ---

def valle_mates():
    st.markdown("<div class='parchment'><h3>🔢 Valle Matemático</h3><p>Resuelve el enigma:</p>", unsafe_allow_html=True)
    n1, n2 = random.randint(1, 10), random.randint(1, 10)
    ans = st.number_input(f"¿Cuánto es {n1} x {n2}?", step=1)
    if st.button("Verificar"):
        if ans == n1 * n2:
            xp, co = reward(30, 15)
            st.success(f"¡Magia pura! +{xp} XP / +{co} 🪙")
        else: st.error("El hechizo se ha disuelto...")
    st.markdown("</div>", unsafe_allow_html=True)

def reino_frances():
    st.markdown("<div class='parchment'><h3>🇫🇷 Royaume Français</h3><p>Traduction rapide :</p>", unsafe_allow_html=True)
    op = st.radio("¿Cómo se dice 'Dragón'?", ["Le Chat", "Le Dragon", "Le Chien"])
    if st.button("Vérifier"):
        if op == "Le Dragon":
            xp, co = reward(30, 15)
            st.success("Magnifique ! +30 XP")
        else: st.error("Oups... réessaye !")
    st.markdown("</div>", unsafe_allow_html=True)

def laboratorio_alquimia():
    st.markdown("<div class='parchment'><h3>🧪 Laboratorio de Alquimia</h3><p>Próximamente...</p></div>", unsafe_allow_html=True)

def templo_musical():
    st.markdown("<div class='parchment'><h3>🎶 Templo Musical</h3><p>Próximamente...</p></div>", unsafe_allow_html=True)

# --- MAPA INTERACTIVO CON MOVIMIENTO DEL DRAGÓN ---
def mostrar_mapa_interactivo():
    st.markdown("<h2 class='fancy-title'>Carte des Royaumes</h2>", unsafe_allow_html=True)
    
    # Coordenadas de los reinos en la imagen del mapa (en porcentajes)
    REINO_POSICIONES = {
        "Mates": {'x': '25%', 'y': '30%'},      # Valle Matemático
        "Frances": {'x': '75%', 'y': '30%'},    # Royaume Français
        "Ciencias": {'x': '25%', 'y': '70%'},   # Laboratorio Alquimia
        "Musica": {'x': '75%', 'y': '70%'}      # Templo Musical
    }

    # Cargar la imagen del mapa
    try:
        map_image = Image.open(MAPA_IMAGEN_PATH)
        map_width, map_height = map_image.size
        # Streamlit no permite que los elementos HTML controlen los clicks directamente sobre la imagen
        # Así que mostraremos la imagen y los botones debajo que muevan al dragón
        st.image(map_image, use_column_width=True)

        # Usamos st.markdown para inyectar el HTML con el dragón posicionado
        # El dragón se moverá a las últimas coordenadas guardadas
        st.markdown(f"""
        <div class="map-container" style="background: url('{MAPA_IMAGEN_PATH}') center / cover; height: {map_height * (st.session_state.image_scale if 'image_scale' in st.session_state else 1)}px;">
            <div class="map-dragon-icon" style="left: {st.session_state.user['dragon_pos_x']}; top: {st.session_state.user['dragon_pos_y']};"></div>
            </div>
        """, unsafe_allow_html=True)

    except FileNotFoundError:
        st.error(f"Error: La imagen '{MAPA_IMAGEN_PATH}' no se encontró. Asegúrate de subirla a GitHub en la misma carpeta que 'app.py'.")
        st.image("https://via.placeholder.com/900x600?text=Mapa+no+encontrado", use_column_width=True)


    st.markdown("<br>Elige tu destino para mover a tu dragón:", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("🔢 Valle Matemático 📍"): 
            st.session_state.user['reino_actual'] = "Mates"
            st.session_state.user['dragon_pos_x'] = REINO_POSICIONES["Mates"]['x']
            st.session_state.user['dragon_pos_y'] = REINO_POSICIONES["Mates"]['y']
            st.rerun()
    with c2:
        if st.button("🇫🇷 Reino Francés 📍"): 
            st.session_state.user['reino_actual'] = "Frances"
            st.session_state.user['dragon_pos_x'] = REINO_POSICIONES["Frances"]['x']
            st.session_state.user['dragon_pos_y'] = REINO_POSICIONES["Frances"]['y']
            st.rerun()
    with c3:
        if st.button("🧪 Laboratorio Alquimia 📍"): 
            st.session_state.user['reino_actual'] = "Ciencias"
            st.session_state.user['dragon_pos_x'] = REINO_POSICIONES["Ciencias"]['x']
            st.session_state.user['dragon_pos_y'] = REINO_POSICIONES["Ciencias"]['y']
            st.rerun()
    with c4:
        if st.button("🎶 Templo Musical 📍"): 
            st.session_state.user['reino_actual'] = "Musica"
            st.session_state.user['dragon_pos_x'] = REINO_POSICIONES["Musica"]['x']
            st.session_state.user['dragon_pos_y'] = REINO_POSICIONES["Musica"]['y']
            st.rerun()

    # Muestra el contenido del reino seleccionado
    if st.session_state.user['reino_actual'] == "Mates": valle_mates()
    elif st.session_state.user['reino_actual'] == "Frances": reino_frances()
    elif st.session_state.user['reino_actual'] == "Ciencias": laboratorio_alquimia()
    elif st.session_state.user['reino_actual'] == "Musica": templo_musical()
    elif st.session_state.user['reino_actual'] is None:
        st.info("Selecciona un reino en el mapa para iniciar una aventura.")

# --- 5. VISTAS PRINCIPALES ---
if not st.session_state.user['setup_complete']:
    st.markdown("<div class='parchment'><h1 style='text-align:center;'>Bienvenue au Royaume des Savoirs</h1>", unsafe_allow_html=True)
    st.session_state.user['nombre'] = st.text_input("Comment t'appelles-tu, valeureux aventurier ?")
    if st.button("Forger mon Destin ⚔️"):
        st.session_state.user['setup_complete'] = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # Cofre diario
    today = str(date.today())
    if st.session_state.user.get('last_login') != today:
        st.session_state.user['last_login'] = today
        reward(25, 50)
        st.balloons()
        st.toast("🎁 Trésor quotidien reçu : 50 pièces d'or !", icon="💰")

    # BARRA DE NAVEGACIÓN SUPERIOR
    menu = st.tabs(["🏠 Foyer", "🗺️ Carte des Royaumes", "📜 Journal", "💎 Boutique"])

    with menu[0]: # HOME
        st.markdown(f"<h1 class='fancy-title'>Bienvenue, {st.session_state.user['nombre']}</h1>", unsafe_allow_html=True)
        st.write(f"✨ XP: {st.session_state.user['xp']} | 🪙 Monedas: {st.session_state.user['monedas']}")
        # Aquí iría tu dragón flotante de nivel, si tienes sus sprites.
        # Por ahora, un placeholder:
        st.image("https://cdn-icons-png.flaticon.com/512/3069/3069418.png", width=150)


    with menu[1]: # MAPA DE REINOS
        mostrar_mapa_interactivo()

    with menu[2]: # JOURNAL
        st.markdown('<div class="parchment">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>📜 Parchemin Royal du Jour</h2>", unsafe_allow_html=True)
        sent = st.select_slider("Comment te sens-tu aujourd'hui ?", ["😞 Très mal", "😐 Neutre", "🙂 Bien", "🤩 Excellent"])
        succ = st.text_area("Ma plus grande victoire du jour fut...")
        fail = st.text_area("Le défi que je n'ai pas encore vaincu est...")
        
        if st.button("Sceller le Parchemin et l'Envoyer 🖋️"):
            if succ and fail:
                xp_g, co_g = reward(40, 10)
                data = [st.session_state.user['nombre'], today, sent, succ, fail, "", "", xp_g, co_g]
                if save_to_sheets(data):
                    st.success("Le parchemin a été envoyé au Maître !")
                    time.sleep(2); st.rerun()
            else: st.error("Pour que le parchemin soit valide, tu dois écrire ta victoire et ton défi.")
        st.markdown("</div>", unsafe_allow_html=True)

    with menu[3]: # BOUTIQUE
        st.markdown("<div class='parchment'>", unsafe_allow_html=True)
        st.markdown("<h1 class='fancy-title'>💎 L'Armurerie des Héros</h1>", unsafe_allow_html=True)
        items = {
            "⚔️ Épée de Feu": {"precio": 50, "desc": "Augmente l'XP gagnée de 20%"},
            "🛡️ Bouclier Magique": {"precio": 40, "desc": "Protège 10% de tes pièces lors d'un échec"},
            "✨ Amulette de Sagesse": {"precio": 70, "desc": "Gagne +5 XP par entrée de Journal"},
            "🛡️ Armure en Or": {"precio": 100, "desc": "Augmente les pièces gagnées de 50%"}
        }
        for item, info in items.items():
            col1, col2 = st.columns([3, 1])
            col1.write(f"**{item}** - *{info['desc']}*")
            if item in st.session_state.user['inventario']: 
                col2.button("Possédé ✅", disabled=True, key=f"bought_{item}")
            elif col2.button(f"{info['precio']} 🪙 Acheter", key=f"buy_{item}"):
                if st.session_state.user['monedas'] >= info['precio']:
                    st.session_state.user['monedas'] -= info['precio']
                    st.session_state.user['inventario'].append(item)
                    st.success(f"{item} ajouté à ton inventaire !")
                    time.sleep(1); st.rerun()
                else:
                    st.error("Pas assez de pièces d'or, brave aventurier !")
        st.markdown("</div>", unsafe_allow_html=True)
```http://googleusercontent.com/image_generation_content/7
