import streamlit as st
import time
from helpers.show_toast import show_toast
from modules.log_in.cache_data.load_data import load_user
from modules.profile.visuals.show_edit_profile import show_edit_profile
from modules.log_in.local_storage.local_storage import getLocalS


def show_profile(username):
    placeholder_info = st.empty()
    try:
        user_data = load_user(username)
        print(f"[show_profile] user_data: {user_data}")
        if user_data is not None:
            username_new, status_edit, message = show_edit_profile(user_data)
            print(f"[show_profile] username_new: {username_new}")
            print(f"[show_profile] status_edit: {status_edit}")
            print(f"[show_profile] message: {message}")
            if status_edit == "success":
                show_toast(
                    f"{message}: {username_new}",
                    icon=":material/check:",
                )
                localS = getLocalS()
                localS.eraseItem("access_token")
                time.sleep(0.7)
                load_user.clear()
                st.session_state.clear()
                st.rerun()
            if status_edit is None:
                placeholder_info.error(message, icon=":material/gpp_maybe:")
        else:
            print(f"[show_profile] Error al obtener datos del usuario {user_data}")
    except Exception as e:
        placeholder_info.error(e)
