import streamlit as st
import requests

BACKEND_URL = st.secrets.get("BACKEND_URL", "Not found")


@st.cache_data(show_spinner=False, ttl=300)
def get_collections():
    try:
        # Realizamos la solicitud al backend para obtener las colecciones
        response = requests.get(f"{BACKEND_URL}/list_collections")

        # Comprobamos si la solicitud fue exitosa (status code 200)
        if response.status_code == 200:
            collections_data = response.json()
            collections = collections_data.get("collections", [])
            print("[mensaje get_collections] collections:", collections)
            print("[mensaje get_collections] type collections:", type(collections))
            return collections
        else:
            print(
                f"[mensaje get_collections] Error al obtener colecciones: {response.status_code}"
            )
            return []
    except Exception as e:
        print(f"Error al obtener colecciones: {e}")
        return []
