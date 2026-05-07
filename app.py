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
# ESTILO PERSONALIZADO
# =========================
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    h1 {
        color: #00c6ff;
        text-align: center;
        font-size: 42px;
        font-weight: bold;
    }
    .sub {
        text-align: center;
        color: #aaa;
        margin-bottom: 30px;
    }
    .card {
        background-color: #1c1f26;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 50px;
        font-size: 18px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# INFORMACIÓN INICIAL
# =========================
st.title("📡 MQTT Control Dashboard")
st.markdown('<p class="sub">Interfaz de control para envío de mensajes MQTT en tiempo real</p>', unsafe_allow_html=True)

st.write("🧠 Versión de Python:", platform.python_version())

values = 0.0
act1 = "OFF"

# =========================
# CALLBACKS MQTT
# =========================
def on_publish(client, userdata, result):
    print("el dato ha sido publicado")
    pass

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
    st.markdown("### 🔌 Encendido del sistema")

    if st.button('🟢 ON'):
        act1 = "ON"
        client1 = paho.Client("GIT-HUB")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        client1.publish("cmqtt_s", message)
        st.success("Sistema encendido")

    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🔌 Apagado del sistema")

    if st.button('🔴 OFF'):
        act1 = "OFF"
        client1 = paho.Client("GIT-HUB")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        client1.publish("cmqtt_s", message)
        st.warning("Sistema apagado")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# CONTROL ANALÓGICO
# =========================
st.markdown("## 🎚️ Control analógico")

st.markdown('<div class="card">', unsafe_allow_html=True)
values = st.slider('📊 Selecciona el rango de valores', 0.0, 100.0)
st.write('Valor seleccionado:', f"**{values}**")

if st.button('📤 Enviar valor analógico'):
    client1 = paho.Client("GIT-HUB")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Analog": float(values)})
    client1.publish("cmqtt_a", message)
    st.success("Valor enviado correctamente")

st.markdown('</div>', unsafe_allow_html=True)
