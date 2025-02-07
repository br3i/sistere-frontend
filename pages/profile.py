import streamlit as st
import requests
from helpers.access_token_verification import is_token_valid
from modules.profile.visuals.show_profile import show_profile
from modules.menu.create_menu import create_menu
from modules.log_in.login import create_login
from modules.log_in.local_storage.local_storage import getLocalS

BACKEND_URL = st.secrets.get("BACKEND_URL", "Not found")

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
                show_profile(username)
        else:
            try:
                response_validate = requests.get(
                    f"{BACKEND_URL}/validate_token", json={"token": access_token}
                )

                if response_validate.status_code == 200:
                    create_menu(response_validate.json().get("username"))
                    show_profile(response_validate.json().get("username"))
                else:
                    localS.eraseItem("access_token")
                    placeholder = create_login(localS)
            except Exception as e:
                print(f"[admin] Error validando el token: {e}")
else:
    create_menu(st.session_state.username)
    show_profile(st.session_state.username)
