import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# =========================
# CONFIGURACIÓN
# =========================
st.set_page_config(
    page_title="MQTT Control",
    page_icon="📡",
    layout="wide"
)

# =========================
# ESTILO MÁS COLORIDO Y LIMPIO
# =========================
st.markdown("""
    <style>

    /* FONDO GENERAL MUY COLORIDO */
    .main {
        background: linear-gradient(135deg, #ff416c, #ff4b2b, #1fddff, #4b6cb7);
        background-size: 400% 400%;
        animation: gradientMove 10s ease infinite;
    }

    @keyframes gradientMove {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* TITULO */
    h1 {
        color: white;
        text-align: center;
        font-size: 46px;
        font-weight: 900;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.4);
    }

    /* SUBTITULO */
    .sub {
        text-align: center;
        color: white;
        font-size: 16px;
        margin-bottom: 20px;
    }

    /* QUITAR TODO TIPO DE "CAJAS" */
    div.block-container {
        padding-top: 1rem;
    }

    /* BOTONES MÁS MODERNOS Y COLORIDOS */
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 0px !important;   /* 🔥 sin bordes redondeados */
        border: none;
        transition: 0.2s;
        color: white;
    }

    .stButton>button:hover {
        transform: scale(1.02);
        filter: brightness(1.1);
    }

    /* BOTÓN ON */
    button[kind="primary"] {
        background: linear-gradient(90deg, #00c853, #64dd17);
    }

    /* BOTÓN OFF */
    button[kind="secondary"] {
        background: linear-gradient(90deg, #ff1744, #d50000);
    }

    /* SLIDER MÁS LIMPIO Y COLORIDO */
    [data-baseweb="slider"] {
        padding: 10px 0;
    }

    .stSlider > div {
        background: transparent !important;
    }

    /* línea del slider */
    .stSlider [data-testid="stTickBar"] {
        background: linear-gradient(90deg, #00c6ff, #ff00cc) !important;
    }

    /* círculo del slider */
    div[role="slider"] {
        background: #ffffff !important;
        border: 3px solid #ff00cc !important;
    }

    /* texto */
    p, label {
        color: white !important;
        font-weight: 500;
    }

    </style>
""", unsafe_allow_html=True)

# =========================
# TITULO
# =========================
st.title("📡 MQTT Control Dashboard")
st.markdown('<p class="sub">Control IoT en tiempo real con estilo vibrante</p>', unsafe_allow_html=True)

st.write("🧠 Versión de Python:", platform.python_version())

values = 0.0
act1 = "OFF"

# =========================
# MQTT CALLBACKS
# =========================
def on_publish(client, userdata, result):
    print("Publicado")

def on_message(client, userdata, message):
    global message_received
    time.sleep(1)
    message_received = str(message.payload.decode("utf-8"))
    st.write("📩", message_received)

broker = "157.230.214.127"
port = 1883

client1 = paho.Client("GIT-HUB")
client1.on_message = on_message

# =========================
# CONTROL PRINCIPAL
# =========================
st.markdown("## ⚙️ Control")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🟢 ENCENDER")

    if st.button("ON"):
        act1 = "ON"
        client1 = paho.Client("GIT-HUB")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        client1.publish("cmqtt_s", message)
        st.success("ENCENDIDO")

with col2:
    st.markdown("### 🔴 APAGAR")

    if st.button("OFF"):
        act1 = "OFF"
        client1 = paho.Client("GIT-HUB")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        client1.publish("cmqtt_s", message)
        st.error("APAGADO")

# =========================
# CONTROL ANALÓGICO
# =========================
st.markdown("## 🎚️ Control analógico")

values = st.slider('Selecciona valor', 0.0, 100.0)
st.write("Valor:", values)

if st.button("📤 ENVIAR"):
    client1 = paho.Client("GIT-HUB")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Analog": float(values)})
    client1.publish("cmqtt_a", message)
    st.success("Enviado")
