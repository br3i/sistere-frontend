import streamlit as st
import requests
from helpers.access_token_verification import is_token_valid
from modules.menu.create_menu import create_menu
from modules.log_in.login import create_login
from modules.log_in.local_storage.local_storage import getLocalS
from modules.reports.visuals.show_dashboard_reports import show_dashboard_reports

BACKEND_URL = st.secrets.get("BACKEND_URL", "Not found")

# Crear el placeholder para mostrar mensajes de carga
placeholder = st.empty()

if "username_logged" not in st.session_state:
    localS = getLocalS()
    access_token = localS.getItem("access_token")

    if access_token is None:
        placeholder = create_login(localS)
    else:
        token_validation = is_token_valid(access_token)
        if token_validation is not None:
            username, valid_token = token_validation
            print(f"[valid_token] valid_token: {valid_token}")
            if valid_token:
                create_menu(username)
                show_dashboard_reports()
        else:
            try:
                response_validate = requests.get(
                    f"{BACKEND_URL}/validate_token", json={"token": access_token}
                )
                if response_validate.status_code == 200:
                    st.write("Reutilizar la función principal de reports 1")
                else:
                    localS.eraseItem("access_token")
                    placeholder = create_login(localS)
            except Exception as e:
                print(f"[admin] Error validando el token: {e}")
else:
    create_menu(st.session_state.username)
    # Crear pestañas para las diferentes funcionalidades
    st.write("Reutilizar la función principal de reports 2")
