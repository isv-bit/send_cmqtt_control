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
# ESTILO MÁS COLORIDO
# =========================
st.markdown("""
    <style>

    .main {
        background: linear-gradient(135deg, #e0f7ff, #fef9ff);
    }

    h1 {
        color: #1f4aff;
        text-align: center;
        font-size: 42px;
        font-weight: 800;
    }

    .sub {
        text-align: center;
        color: #444;
        margin-bottom: 25px;
        font-size: 16px;
    }

    .card {
        background-color: white;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.08);
        margin-bottom: 20px;
        border-left: 6px solid #1f4aff;
    }

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
        box-shadow: 0px 6px 15px rgba(0,0,0,0.15);
    }

    /* Colores específicos de botones */
    div[data-testid="stButton"] > button[kind="primary"] {
        background-color: #2ecc71;
        color: white;
    }

    div[data-testid="stButton"] > button[kind="secondary"] {
        background-color: #e74c3c;
        color: white;
    }

    </style>
""", unsafe_allow_html=True)

# =========================
# TÍTULO
# =========================
st.title("📡 MQTT Control Dashboard")
st.markdown('<p class="sub">Sistema de control IoT con comunicación en tiempo real</p>', unsafe_allow_html=True)

st.write("🧠 Versión de Python:", platform.python_version())

values = 0.0
act1 = "OFF"

# =========================
# CALLBACKS MQTT
# =========================
def on_publish(client, userdata, result):
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
# CONTROLES
# =========================
st.markdown("## ⚙️ Control principal")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🟢 Encender sistema")

    if st.button('ON'):
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

    if st.button('OFF'):
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

if st.button('📤 Enviar valor analógico'):
    client1 = paho.Client("GIT-HUB")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Analog": float(values)})
    client1.publish("cmqtt_a", message)
    st.success("Valor enviado correctamente")

st.markdown('</div>', unsafe_allow_html=True)
