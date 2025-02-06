import streamlit as st
import requests
import json

BACKEND_URL = st.secrets.get("BACKEND_URL", "Not found")


@st.cache_data(show_spinner=False, ttl=60)
def get_collections():
    response = requests.get(f"{BACKEND_URL}/list_collections")
    if response.status_code == 200:
        if (
            "No collections found" in response.text
        ):  # Verifica si el mensaje es "No collections found"
            return []
        return response.json()
    return []
