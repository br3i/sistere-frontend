import random
import streamlit as st
import requests

BACKEND_URL = st.secrets.get("BACKEND_URL")


@st.cache_data(show_spinner=False, ttl=3600)
def get_data_from_backend(endpoint, limit=100):
    """Función para obtener todos los datos del backend, con opción a limitar la cantidad de registros."""
    try:
        url = f"{BACKEND_URL}{endpoint}?limit={limit}"
        print(f"\n\n[fetch_data] Realizando solicitud a: {url}")
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {response.headers}")
        response.raise_for_status()
        print(f"Response JSON: {response.json()}")  # Para ver el contenido
        return response.json()

    except requests.exceptions.RequestException as e:
        st.error(f"Error al obtener datos: {e}")
        print(f"Error: {e}")
        return None


def get_role_distribution(limit=None):
    """Función para obtener la distribución de roles desde el backend."""
    if limit is None:
        limit = st.session_state.get("n_users", 15)

    if "role_distribution" not in st.session_state:
        st.session_state["role_distribution"] = get_data_from_backend(
            "/roles/distribution", limit=100
        )

    role_distribution = st.session_state["role_distribution"]
    if len(role_distribution) > limit:
        role_distribution = role_distribution[:limit]

    return role_distribution


def get_active_users(limit=None):
    """Función para obtener métricas de usuarios activos por rol desde el backend."""
    if limit is None:
        limit = st.session_state.get("n_users", 15)  # Valor por defecto

    # Verificamos si ya tenemos los datos en la sesión
    if "active_users_metrics" not in st.session_state:
        # Llamamos al endpoint que nos devolverá los usuarios activos
        st.session_state["active_users_metrics"] = get_data_from_backend(
            "/roles/active_users", limit=limit
        )

    # Recuperamos los datos de la sesión
    active_users_metrics = st.session_state["active_users_metrics"]

    # Si tenemos más resultados de los que necesitamos, los limitamos
    if len(active_users_metrics) > limit:
        active_users_metrics = active_users_metrics[:limit]

    return active_users_metrics
