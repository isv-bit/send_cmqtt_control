import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# =========================
# CONFIGURACIÓN DE PÁGINA
# =========================
st.set_page_config(
    page_title="MQTT Control Dashboard",
    page_icon="📡",
    layout="wide"
)

# =========================
# ESTILO GENERAL (MÁS COLORIDO)
# =========================
st.markdown("""
    <style>

    /* FONDO GENERAL */
    .main {
        background: linear-gradient(120deg, #00c6ff, #0072ff, #6a11cb);
    }

    /* TÍTULO */
    h1 {
        color: white;
        text-align: center;
        font-size: 44px;
        font-weight: 900;
    }

    .sub {
        text-align: center;
        color: white;
        font-size: 16px;
        margin-bottom: 25px;
    }

    /* TARJETAS */
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.25);
        margin-bottom: 20px;
    }

    /* BOTONES */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 55px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }

    .stButton>button:hover {
        transform: scale(1.03);
    }

    /* ON BUTTON (verde) */
    div[data-testid="stButton"] button:has(span:contains("ON")) {
        background-color: #2ecc71 !important;
        color: white !important;
    }

    /* OFF BUTTON (rojo) */
    div[data-testid="stButton"] button:has(span:contains("OFF")) {
        background-color: #e74c3c !important;
        color: white !important;
    }

    /* =========================
       SLIDER SIN BARRAS BLANCAS
    ========================== */
    [data-baseweb="slider"] {
        background: transparent !important;
    }

    .stSlider > div {
        background: transparent !important;
    }

    /* track del slider */
    .stSlider [data-testid="stTickBar"] {
        background: linear-gradient(90deg, #00c6ff, #0072ff) !important;
    }

    /* línea activa */
    .stSlider div[role="progressbar"] {
        background: linear-gradient(90deg, #00c6ff, #0072ff) !important;
    }

    </style>
""", unsafe_allow_html=True)

# =========================
# TÍTULO
# =========================
st.title("📡 MQTT Control Dashboard")
st.markdown('<p class="sub">Sistema IoT con control en tiempo real vía MQTT</p>', unsafe_allow_html=True)

st.write("🧠 Versión de Python:", platform.python_version())

values = 0.0
act1 = "OFF"

# =========================
# MQTT CALLBACKS
# =========================
def on_publish(client,userdata,result):
    print("el dato ha sido publicado")

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write("📩 Mensaje recibido:", message_received)

broker = "157.230.214.127"
port = 1883

client1 = paho.Client("GIT-HUB")
client1.on_message = on_message

# =========================
# CONTROLES PRINCIPALES
# =========================
st.markdown("## ⚙️ Control del sistema")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🟢 Encender sistema")

    if st.button("ON"):
        act1 = "ON"
        client1 = paho.Client("GIT-HUB")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        client1.publish("cmqtt_s", message)
        st.success("Sistema ENCENDIDO")

    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🔴 Apagar sistema")

    if st.button("OFF"):
        act1 = "OFF"
        client1 = paho.Client("GIT-HUB")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        client1.publish("cmqtt_s", message)
        st.error("Sistema APAGADO")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# CONTROL ANALÓGICO
# =========================
st.markdown("## 🎚️ Control analógico")

st.markdown('<div class="card">', unsafe_allow_html=True)

values = st.slider('📊 Selecciona el rango de valores', 0.0, 100.0)
st.write("Valor seleccionado:", f"**{values}**")

if st.button("📤 Enviar valor analógico"):
    client1 = paho.Client("GIT-HUB")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Analog": float(values)})
    client1.publish("cmqtt_a", message)
    st.success("Valor enviado correctamente")

st.markdown('</div>', unsafe_allow_html=True)
