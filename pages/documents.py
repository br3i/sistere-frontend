import streamlit as st
import requests
import time
from modules.menu.create_menu import create_menu
from modules.documents.visuals.show_upload_docs import show_upload_docs
from modules.documents.visuals.show_df_documents import show_df_documents
from modules.documents.visuals.show_df_delete import show_df_delete
from modules.log_in.login import create_login
from modules.settings.utils.load_theme_extra_config import load_theme_extra_config
from modules.log_in.cookie.cookie_manager import get_cookie_controller

BACKEND_URL = st.secrets.get("BACKEND_URL", "Not found")

theme_extra_config = load_theme_extra_config()

# Crear el placeholder para mostrar mensajes de carga
placeholder = st.empty()

if "username_logged" not in st.session_state:
    controller = get_cookie_controller()

    token = controller.get("access_token")

    time.sleep(0.2)
    if token is None:
        placeholder = create_login(controller)
    else:
        try:
            response_validate = requests.get(
                f"{BACKEND_URL}/validate_token", json={"token": token}
            )

            if response_validate.status_code == 200:
                create_menu(response_validate.json().get("username"))
                st.title(
                    f'Página :{theme_extra_config["primary_docs_color"]}[Gestión de Archivos]'
                )

                # Crear pestañas para las diferentes funcionalidades
                tabs = st.tabs(
                    ["Subir Archivo", "Editar Archivos", "Eliminar Archivos"]
                )

                with tabs[0]:
                    st.header(
                        f':{theme_extra_config["secondary_docs_color"]}[Subir un PDF]'
                    )
                    with st.spinner("Cargando..."):
                        show_upload_docs()
                with tabs[1]:
                    st.header(
                        f':{theme_extra_config["secondary_docs_color"]}[Archivos Disponibles]'
                    )
                    with st.spinner("Cargando Archivos..."):
                        show_df_documents()
                with tabs[2]:
                    st.header(":red[Archivos Disponibles]")
                    with st.spinner("Cargando Archivos..."):
                        show_df_delete()

            else:
                placeholder = create_login(controller)
        except Exception as e:
            print(f"[admin] Error validando el token: {e}")
else:
    create_menu(st.session_state.username)
    st.title(f'Página :{theme_extra_config["primary_docs_color"]}[Gestión de Archivos]')

    # Crear pestañas para las diferentes funcionalidades
    tabs = st.tabs(["Subir Archivo", "Editar Archivos", "Eliminar Archivos"])

    with tabs[0]:
        st.header(f':{theme_extra_config["secondary_docs_color"]}[Subir un PDF]')
        with st.spinner("Cargando..."):
            show_upload_docs()
    with tabs[1]:
        st.header(
            f':{theme_extra_config["secondary_docs_color"]}[Archivos Disponibles]'
        )
        with st.spinner("Cargando Archivos..."):
            show_df_documents()
    with tabs[2]:
        st.header(":red[Archivos Disponibles]")
        with st.spinner("Cargando Archivos..."):
            show_df_delete()
