import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Dragon Learning Quest", layout="centered")

USER_FILE = "data/user.json"
JOURNAL_FILE = "data/journal.csv"

# ------------------------
# EVOLUCIÓN
# ------------------------
XP_LEVELS = {
    "huevo": 0,
    "bebe": 50,
    "joven": 150,
    "adulto": 300
}

# ------------------------
# ACCESORIOS
# ------------------------
ACCESSORIES = {
    "amuleto.png": {"price": 20, "desc": "Calma emocional"},
    "lupa.png": {"price": 15, "desc": "Mejora atención"},
    "collar.png": {"price": 18, "desc": "Confianza"},
    "casco.png": {"price": 25, "desc": "Protección"},
    "escudo.png": {"price": 30, "desc": "Defensa"},
    "armadura.png": {"price": 35, "desc": "Resistencia"},
    "botas.png": {"price": 15, "desc": "Agilidad"},
    "cinturon.png": {"price": 12, "desc": "Organización"},
    "capa.png": {"price": 22, "desc": "Motivación"},
    "corona.png": {"price": 40, "desc": "Liderazgo"},
    "alas_extra.png": {"price": 45, "desc": "Exploración"},
    "pluma.png": {"price": 10, "desc": "Escritura"},
    "gemas.png": {"price": 30, "desc": "Recompensas"},
    "guantes.png": {"price": 18, "desc": "Precisión"},
    "sombrero_magico.png": {"price": 35, "desc": "Creatividad"},
    "medallon.png": {"price": 28, "desc": "Memoria"},
    "anillo.png": {"price": 20, "desc": "Constancia"},
    "cetro.png": {"price": 50, "desc": "Maestría"},
    "pergamino.png": {"price": 15, "desc": "Conocimiento"},
    "libro.png": {"price": 25, "desc": "Aprendizaje"}
}

# ------------------------
# ARCHIVOS
# ------------------------
if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({"xp": 0, "coins": 0, "accessories": []}, f)

if not os.path.exists(JOURNAL_FILE):
    pd.DataFrame(columns=[
        "fecha", "sentimiento", "logro", "mejora", "emocion"
    ]).to_csv(JOURNAL_FILE, index=False)

# ------------------------
# FUNCIONES
# ------------------------
def load_user():
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_user(user):
    with open(USER_FILE, "w") as f:
        json.dump(user, f, indent=4)

def dragon_stage(xp):
    if xp >= 300:
        return "adulto"
    elif xp >= 150:
        return "joven"
    elif xp >= 50:
        return "bebe"
    return "huevo"

# ------------------------
# APP
# ------------------------
user = load_user()
stage = dragon_stage(user["xp"])

st.title("🐉 Dragon Learning Quest")

st.image(f"assets/dragons/{stage}.png", width=280)
st.markdown(f"### Dragón: **{stage.upper()}**")
st.progress(min(user["xp"] / 300, 1.0))
st.markdown(f"🪙 Monedas: {user['coins']}")

tabs = st.tabs(["📜 Journal", "⚔️ Duelo", "🗺️ Mapa", "🛍️ Boutique"])

# ------------------------
# JOURNAL
# ------------------------
with tabs[0]:
    st.image("assets/journal.png", use_column_width=True)

    feeling = st.selectbox("¿Cómo te has sentido hoy?", ["Feliz", "Tranquilo", "Cansado", "Motivado", "Preocupado"])
    logro = st.text_area("¿Qué has logrado?")
    mejora = st.text_area("¿Qué puedes mejorar?")
    emocion = st.text_area("¿Cómo te sientes ahora?")

    if st.button("Guardar Journal"):
        user["xp"] += 10
        user["coins"] += 5
        save_user(user)

        df = pd.read_csv(JOURNAL_FILE)
        df.loc[len(df)] = [datetime.now(), feeling, logro, mejora, emocion]
        df.to_csv(JOURNAL_FILE, index=False)

        st.success("✨ +10 XP y +5 monedas")

# ------------------------
# DUELO
# ------------------------
with tabs[1]:
    st.image("assets/duelo.png", use_column_width=True)

    answer = st.radio("Hier, j'___ mangé une pomme.", ["ai", "as", "est", "avais"])

    if st.button("Combatir"):
        if answer == "ai":
            user["xp"] += 15
            user["coins"] += 8
            save_user(user)
            st.success("🔥 Victoria")
        else:
            st.error("💀 Derrota")

# ------------------------
# MAPA
# ------------------------
with tabs[2]:
    st.image("assets/map.png", use_column_width=True)
    st.info("Explora las distintas asignaturas")

# ------------------------
# BOUTIQUE
# ------------------------
with tabs[3]:
    for item, data in ACCESSORIES.items():
        c1, c2, c3 = st.columns([2,3,1])
        with c1:
            st.image(f"assets/accessories/{item}", width=70)
        with c2:
            st.write(item.replace(".png", ""))
            st.write(f"{data['desc']} — 💰 {data['price']}")
        with c3:
            if st.button(f"Comprar {item}"):
                if user["coins"] >= data["price"]:
                    user["coins"] -= data["price"]
                    user["accessories"].append(item)
                    save_user(user)
                    st.success("Comprado 🐉")
                else:
                    st.error("No tienes monedas")
