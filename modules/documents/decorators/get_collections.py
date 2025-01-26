import streamlit as st
from helpers.chroma_client import chroma_client


@st.cache_data(show_spinner=False, ttl=60)
def get_collections():
    try:
        client = chroma_client()
        collections = client.list_collections()
        print("[mensaje get_collections] collections:", collections)
        print("[mensaje get_collections] type collections:", type(collections))

        if collections is None:
            return []
        return collections
    except Exception as e:
        print(f"Error al obtener colecciones: {e}")
        return []
