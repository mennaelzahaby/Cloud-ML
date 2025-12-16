import streamlit as st
import requests

st.set_page_config(page_title="ML Dashboard", layout="centered")

REGISTRY_URL = "http://model-registry:8000"

st.title("📊 ML Model Registry Dashboard")

# Active model
st.header("🔥 Active Model")
active = requests.get(f"{REGISTRY_URL}/active").json()

if active:
    st.success(f"Model: {active['name']} | Version: {active['version']}")
    st.metric("Accuracy", active["accuracy"])
else:
    st.warning("No active model")

# All models
st.header("📦 All Models")
models = requests.get(f"{REGISTRY_URL}/models").json()

for m in models:
    st.write(
        f"🧠 {m['name']} | {m['version']} | Acc: {m['accuracy']} | Active: {m['active']}"
    )
