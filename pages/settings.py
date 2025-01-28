import streamlit as st
import requests
import time
from modules.menu.create_menu import create_menu
from modules.settings.utils.load_theme_config import load_theme_config
from modules.settings.utils.load_theme_extra_config import load_theme_extra_config
from modules.settings.visuals.change_theme_config import change_theme_config
from modules.log_in.login import create_login
from modules.log_in.cookie.cookie_manager import get_cookie_controller

BACKEND_URL = st.secrets.get("BACKEND_URL", "Not found")

theme_config = load_theme_config()
theme_extra_config = load_theme_extra_config()
print(f"[theme_extra_config]: {theme_extra_config}")

# Crear el placeholder para mostrar mensajes de carga
placeholder = st.empty()

if "switch_theme" not in st.session_state:
    if theme_config["backgroundColor"] == "#FFFFFF":
        st.session_state.switch_theme = "dark"
    else:
        st.session_state.switch_theme = "light"

if "saved_changed_theme" not in st.session_state:
    st.session_state.saved_changed_theme = False


def saved_changed_theme():
    st.session_state.saved_changed_theme = True
    st.session_state.saved_changed_theme


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

            if response_validate.status_code == 200 and theme_extra_config is not None:
                create_menu(response_validate.json().get("username"))
                st.title(
                    f'Configuración :{theme_extra_config["primary_config_color"]}[Global]'
                )
                with st.spinner("Cargando..."):
                    change_theme_config(theme_config, theme_extra_config)
            else:
                placeholder = create_login(controller)
        except Exception as e:
            print(f"[admin] Error validando el token: {e}")
else:
    create_menu(st.session_state.username)
    if theme_extra_config is not None:
        st.title(f'Configuración :{theme_extra_config["primary_config_color"]}[Global]')
        with st.spinner("Cargando..."):
            change_theme_config(theme_config, theme_extra_config)
