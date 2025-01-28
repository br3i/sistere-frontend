import streamlit as st
import requests
import time
from modules.menu.create_menu import create_menu
from modules.user.visuals.show_user_logged import show_user_logged
from modules.log_in.login import create_login
from modules.settings.utils.load_theme_extra_config import load_theme_extra_config
from modules.log_in.cookie.cookie_manager import get_cookie_controller

# Configuración inicial
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
                    f'Administración de :{theme_extra_config["primary_users_color"]}[Usuarios :material/group:]'
                )

                show_user_logged()
            else:
                placeholder = create_login(controller)
        except Exception as e:
            print(f"[admin] Error validando el token: {e}")
else:
    create_menu(st.session_state.username)
    st.title(
        f'Administración de :{theme_extra_config["primary_users_color"]}[Usuarios :material/group:]'
    )

    show_user_logged()
