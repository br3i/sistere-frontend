import streamlit as st
import requests

BACKEND_URL = st.secrets.get("BACKEND_URL")


@st.cache_data(show_spinner=False, ttl=3600)
def get_data_from_backend(endpoint, limit=1000):
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


def get_resource_data(limit=None):
    """Función para obtener datos de recursos desde el backend, con filtrado en frontend."""
    if limit is None:
        limit = st.session_state.get("n_docs", 15)

    # Si no se han obtenido datos previamente, los solicitamos con un valor grande
    if "resource_data" not in st.session_state:
        st.session_state["resource_data"] = get_data_from_backend(
            "/documents/resources_usage", limit=1000
        )

    # Si el límite solicitado es menor que los datos obtenidos, filtramos los resultados
    resource_data = st.session_state["resource_data"]
    if len(resource_data) > limit:
        resource_data = resource_data[:limit]

    return resource_data


def get_processing_metrics(limit=None):
    """Función para obtener métricas de procesamiento desde el backend, con filtrado en frontend."""
    if limit is None:
        limit = st.session_state.get("n_docs", 15)

    # Si no se han obtenido datos previamente, los solicitamos con un valor grande
    if "processing_metrics" not in st.session_state:
        st.session_state["processing_metrics"] = get_data_from_backend(
            "/documents/processing_metrics", limit=1000
        )

    # Si el límite solicitado es menor que los datos obtenidos, filtramos los resultados
    processing_metrics = st.session_state["processing_metrics"]
    if len(processing_metrics) > limit:
        processing_metrics = processing_metrics[:limit]

    return processing_metrics


def get_time_data(limit=None):
    """Función para obtener datos de distribución de tiempo desde el backend, con filtrado en frontend."""
    if limit is None:
        limit = st.session_state.get("n_docs", 15)

    # Si no se han obtenido datos previamente, los solicitamos con un valor grande
    if "time_data" not in st.session_state:
        st.session_state["time_data"] = get_data_from_backend(
            "/documents/time_distribution", limit=1000
        )

    # Si el límite solicitado es menor que los datos obtenidos, filtramos los resultados
    time_data = st.session_state["time_data"]
    if len(time_data) > limit:
        time_data = time_data[:limit]

    return time_data


def get_top_documents(limit=None):
    """Función para obtener los documentos principales desde el backend, con filtrado en frontend."""
    if limit is None:
        limit = st.session_state.get("n_docs", 15)

    # Si no se han obtenido datos previamente, los solicitamos con un valor grande
    if "top_documents" not in st.session_state:
        st.session_state["top_documents"] = get_data_from_backend(
            "/documents/top_requests", limit=1000
        )

    # Si el límite solicitado es menor que los datos obtenidos, filtramos los resultados
    top_documents = st.session_state["top_documents"]
    if len(top_documents) > limit:
        top_documents = top_documents[:limit]

    return top_documents
