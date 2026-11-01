import streamlit as st
import json
import os
from streamlit_autorefresh import st_autorefresh

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STATE_FILE = BASE_DIR / "dashboard_state.json"

st.set_page_config(
    page_title="EdgeSentinel",
    page_icon="🛡️",
    layout="wide"
)

# Refresh dashboard every 1 second
st_autorefresh(interval=1000, key="edgesentinel_refresh")


def load_state():

    if not os.path.exists(STATE_FILE):
        return {
            "temperature": 0,
            "moisture": 0,
            "status": "WAITING",
            "gemini": "Waiting for sensor data...",
            "alert": "No alerts yet.",
            "temp_rate": 0,
            "moisture_rate": 0
        }

    try:
        with open(STATE_FILE, "r") as file:
            return json.load(file)

    except Exception:
        return {
            "temperature": 0,
            "moisture": 0,
            "status": "WAITING",
            "gemini": "Waiting for sensor data...",
            "alert": "No alerts yet.",
            "temp_rate": 0,
            "moisture_rate": 0
        }


data = load_state()

temperature = data.get("temperature", 0)
moisture = data.get("moisture", 0)
status = data.get("status", "WAITING")
gemini = data.get("gemini", "Waiting...")
alert = data.get("alert", "No alerts yet.")
temp_rate = data.get("temp_rate", 0)
moisture_rate = data.get("moisture_rate", 0)


# -----------------------------
# HEADER
# -----------------------------

st.title("🛡️ EdgeSentinel")

st.subheader("Real-Time Environmental Monitoring")

st.divider()


# -----------------------------
# SENSOR VALUES
# -----------------------------

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "🌡️ Temperature",
        f"{temperature:.2f} °C"
    )


with col2:

    st.metric(
        "💧 Moisture",
        f"{moisture:.1f} %"
    )


with col3:

    if status == "NORMAL":
        st.success("🟢 NORMAL")

    elif status == "WARNING":
        st.warning("🟡 WARNING")

    elif status == "CRITICAL":
        st.error("🔴 CRITICAL")

    else:
        st.info("⚪ WAITING")


# -----------------------------
# SENSOR TRENDS
# -----------------------------

st.divider()

st.subheader("Sensor Trends")

col1, col2 = st.columns(2)

with col1:

    st.write("Temperature Rate")

    if temp_rate > 0:
        st.metric(
            "Rate of Change",
            f"+{temp_rate:.3f} °C"
        )
    else:
        st.metric(
            "Rate of Change",
            f"{temp_rate:.3f} °C"
        )


with col2:

    st.write("Moisture Rate")

    st.metric(
        "Rate of Change",
        f"{moisture_rate:.3f} %"
    )


# -----------------------------
# GEMINI
# -----------------------------

st.divider()

st.subheader("🤖 Gemini Environmental Interpretation")

st.info(gemini)


# -----------------------------
# ALERT
# -----------------------------

st.divider()

st.subheader("🔊 Latest Alert")

if status == "CRITICAL":

    st.error(alert)

elif status == "WARNING":

    st.warning(alert)

elif status == "NORMAL":

    st.success(alert)

else:

    st.info(alert)


# -----------------------------
# FOOTER
# -----------------------------

st.divider()

st.caption(
    "EdgeSentinel • Detect locally • Explain remotely"
)