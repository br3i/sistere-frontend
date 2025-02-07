import streamlit as st
import requests

BACKEND_URL = st.secrets.get("BACKEND_URL", "Not found")
TIME_ZONE = st.secrets.get("TIME_ZONE", "Not found")


def edit_user(id, first_name_new, last_name_new, username_new, email_new, password_new):
    print(
        f"[register_user] valores que llegan id: {id}, first_name_new : {first_name_new}, last_name_new : {last_name_new}, username_new : {username_new}, email_new : {email_new}, password_new : {password_new}"
    )
    try:
        headers = {"Content-Type": "application/json"}

        payload = {
            "email": email_new,
            "username": username_new,
            "first_name": first_name_new,
            "last_name": last_name_new,
            "password": password_new,
        }

        # Remover el campo "password" si es igual a "edit_profile"
        if payload["password"] == "edit_profile":
            del payload["password"]

        # Si deseas evitar enviar cualquier campo con "edit_profile"
        payload = {k: v for k, v in payload.items() if v != "edit_profile"}

        print(f"[edit_user] Payload final edit_user: {payload}")

        response = requests.put(
            f"{BACKEND_URL}/edit_profile/{id}", json=payload, headers=headers
        )
        response_data = response.json()
        print("\n\nresponse_data: ", response_data)
        if response.status_code == 200:
            return response_data["username"], "success", "Usuario editado"
        return "", None, response_data["detail"]
    except Exception as e:
        return "", None, e
