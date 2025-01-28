import streamlit as st
import requests
import time
from modules.admin.visuals.show_main_dashboard import show_main_dashboard
from modules.menu.create_menu import create_menu
from modules.log_in.login import create_login
from modules.log_in.cookie.cookie_manager import get_cookie_controller

BACKEND_URL = st.secrets.get("BACKEND_URL", "Not found")

# with st.status("Valores en st.session_state"):
#     for key in st.session_state:
#         st.markdown(f"**Key**: `{key}`  \n**Value**: `{st.session_state[key]}`")

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
                show_main_dashboard()
            else:
                placeholder = create_login(controller)
        except Exception as e:
            print(f"[admin] Error validando el token: {e}")
else:
    create_menu(st.session_state.username)
    show_main_dashboard()
