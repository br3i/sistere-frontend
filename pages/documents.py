import streamlit as st
import requests
from helpers.access_token_verification import is_token_valid
from modules.menu.create_menu import create_menu
from modules.documents.visuals.show_upload_docs import show_upload_docs
from modules.documents.visuals.show_df_documents import show_df_documents
from modules.documents.visuals.show_df_delete import show_df_delete
from modules.log_in.login import create_login
from modules.log_in.local_storage.local_storage import getLocalS
from modules.settings.utils.load_theme_extra_config import load_theme_extra_config

BACKEND_URL = st.secrets.get("BACKEND_URL", "Not found")

theme_extra_config = load_theme_extra_config()

# Crear el placeholder para mostrar mensajes de carga
placeholder = st.empty()

if "username_logged" not in st.session_state:
    localS = getLocalS()
    access_token = localS.getItem("access_token")

    if access_token is None:
        placeholder = create_login(localS)
    else:
        token_validation = is_token_valid(access_token)
        print(f"[token_validation] {token_validation}")
        if token_validation is not None:
            username, valid_token = token_validation
            print(f"[valid_token] valid_token: {valid_token}")
            if valid_token:
                create_menu(username)
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
            try:
                response_validate = requests.get(
                    f"{BACKEND_URL}/validate_token", json={"token": access_token}
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
                    localS.eraseItem("access_token")
                    placeholder = create_login(localS)
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
