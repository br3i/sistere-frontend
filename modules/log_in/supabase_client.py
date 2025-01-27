import streamlit as st
from supabase import create_client

# Configuración de Supabase
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "Not found")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "Not found")


def get_client_supabase():
    # Crear el cliente de Supabase
    client_supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    return client_supabase
