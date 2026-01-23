import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

# ------------------------
# CONFIGURACIÓN
# ------------------------
st.set_page_config(page_title="Dragon Learning Quest", layout="centered")

USER_FILE = "data/user.json"
JOURNAL_FILE = "data/journal.csv"

XP_LEVELS = {
    "huevo": 0,
    "bebe": 50,
    "joven": 150,
    "adulto": 300
}

ACCESSORIES = {
    "amuleto.png": {
        "price": 20,
        "effect": "bienestar",
        "description": "Aporta calma y equilibrio emocional."
    },
    "lupa.png": {
        "price": 15,
        "effect": "atencion",
        "description": "Mejora la concentración en los duelos."
    },
    "collar.png": {
        "price": 18,
        "effect": "confianza",
        "description": "Aumenta la seguridad del dragón."
    },
    "casco.png": {
        "price": 25,
        "effect": "proteccion",
        "description": "Permite repetir un duelo fallido."
    },
    "escudo.png": {
        "price": 30,
        "effect": "defensa",
        "description": "Reduce penalizaciones."
    },
    "armadura.png": {
        "price": 35,
        "effect": "resistencia",
        "description": "Da estabilidad en retos largos."
    },
    "botas.png": {
        "price": 15,
        "effect": "agilidad",
        "description": "Facilita el progreso en el mapa."
    },
    "cinturon.png": {
        "price": 12,
        "effect": "organizacion",
        "description": "Ayuda a completar tareas."
    },
    "capa.png": {
        "price": 22,
        "effect": "motivacion",
        "description": "Aumenta las ganas de seguir jugando."
    },
    "corona.png": {
        "price": 40,
        "effect": "liderazgo",
        "description": "Representa el progreso del alumno."
    },
    "alas_extra.png": {
        "price": 45,
        "effect": "exploracion",
        "description": "Permite acceder a nuevas zonas."
    },
    "pluma.png": {
        "price": 10,
        "effect": "escritura",
        "description": "Mejora el journal."
    },
    "gemas.png": {
        "price": 30,
        "effect": "recompensa",
        "description": "Incrementa monedas ganadas."
    },
    "guantes.png": {
        "price": 18,
        "effect": "precision",
        "description": "Mejora la exactitud."
    },
    "sombrero_magico.png": {
        "price": 35,
        "effect": "creatividad",
        "description": "Potencia la imaginación."
    },
    "medallon.png": {
        "price": 28,
        "effect": "recuerdo",
        "description": "Refuerza el aprendizaje."
    },
    "anillo.png": {
        "price": 20,
        "effect": "compromiso",
        "description": "Refuerza la constancia."
    },
    "cetro.png": {
        "price": 50,
        "effect": "maestria",
        "description": "Objeto especial de alto nivel."
    },
    "pergamino.png": {
        "price": 15,
        "effect": "conocimiento",
        "description": "Aporta sabiduría."
    },
    "libro.png": {
        "price": 25,
        "effect": "aprendizaje",
        "description": "Refuerza contenidos."
    }
}

}

# ------------------------
# CREAR EXCEL SI NO EXISTE
# ------------------------
if not os.path.exists(JOURNAL_FILE):
    df = pd.DataFrame(columns=[
        "fecha",
        "sentimiento",
        "logro",
        "mejora",
        "emocion"
    ])
    df.to_csv(JOURNAL_FILE, index=False)

# ------------------------
# FUNCIONES
# ------------------------
def load_user():
    if not os.path.exists(USER_FILE):
        return {
            "xp": 0,
            "coins": 0,
            "accessories": [],
            "journal": []
        }
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_user(user):
    with open(USER_FILE, "w") as f:
        json.dump(user, f, indent=4)

def get_dragon_stage(xp):
    if xp >= 300:
        return "adulto"
    elif xp >= 150:
        return "joven"
    elif xp >= 50:
        return "bebe"
    else:
        return "huevo"

# ------------------------
# APP
# ------------------------
user = load_user()
stage = get_dragon_stage(user["xp"])

st.title("🐉 Dragon Learning Quest")

st.image(f"assets/dragons/{stage}.png", width=280)
st.markdown(f"### Estado del dragón: **{stage.upper()}**")
st.progress(min(user["xp"] / 300, 1.0))
st.markdown(f"🪙 Monedas: **{user['coins']}**")

tabs = st.tabs(["📜 Journal", "⚔️ Duelos", "🗺️ Mapa", "🛍️ Boutique"])

# ------------------------
# JOURNAL
# ------------------------
with tabs[0]:
    st.subheader("📜 Diario medieval")

    feeling = st.selectbox("¿Cómo te has sentido hoy?", [
        "Feliz", "Tranquilo", "Cansado", "Motivado", "Preocupado"
    ])

    achievement = st.text_area("¿Qué has logrado hoy?")
    improvement = st.text_area("¿Qué puedes mejorar?")
    emotion = st.text_area("¿Cómo te sientes ahora?")

    if st.button("Guardar Journal"):
        user["xp"] += 10
        user["coins"] += 5
        save_user(user)

        df = pd.read_csv(JOURNAL_FILE)
        new_entry = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "sentimiento": feeling,
            "logro": achievement,
            "mejora": improvement,
            "emocion": emotion
        }
        df = pd.concat([df, pd.DataFrame([new_entry])])
        df.to_csv(JOURNAL_FILE, index=False)

        st.success("✨ Journal guardado — +10 XP y +5 monedas")

# ------------------------
# DUELO FRANCÉS
# ------------------------
with tabs[1]:
    st.subheader("⚔️ Duelo de Francés")

    answer = st.radio(
        "Hier, j'___ mangé une pomme.",
        ["ai", "as", "est", "avais"]
    )

    if st.button("Combatir"):
        if answer == "ai":
            user["xp"] += 15
            user["coins"] += 8
            save_user(user)
            st.success("🔥 Victoria — +15 XP y +8 monedas")
        else:
            st.error("💀 Has perdido el duelo")

# ------------------------
# MAPA
# ------------------------
with tabs[2]:
    st.subheader("🗺️ Mapa del conocimiento")
    st.image("assets/map.png", use_column_width=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.button("🇫🇷 Francés")
    with c2:
        st.button("🔢 Matemáticas")
    with c3:
        st.button("🔬 Ciencias")

# ------------------------
# BOUTIQUE
# ------------------------
with tabs[3]:
    st.subheader("🛍️ Boutique medieval")

    for item, data in ACCESSORIES.items():
        col1, col2, col3 = st.columns([2, 3, 1])
        with col1:
            st.image(f"assets/accessories/{item}", width=70)
        with col2:
            st.write(item.replace(".png", ""))
            st.write(f"💰 {data['price']} monedas")
        with col3:
            if st.button(f"Comprar {item}"):
                if user["coins"] >= data["price"]:
                    user["coins"] -= data["price"]
                    user["accessories"].append(item)
                    save_user(user)
                    st.success("Comprado 🐉")
                else:
                    st.error("No tienes monedas suficientes")
