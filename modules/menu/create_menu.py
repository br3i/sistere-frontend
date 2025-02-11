import streamlit as st
import time
from modules.log_in.cache_data.load_data import load_user
from modules.settings.utils.load_theme_extra_config import load_theme_extra_config
from modules.log_in.local_storage.local_storage import getLocalS

theme_extra_config = load_theme_extra_config()

NOMBRE_ASISTENTE = st.secrets.get("NOMBRE_ASISTENTE", "Not found")


def create_menu(username):
    print(f"[create_menu] Usuario: {username}")
    with st.sidebar:
        user_data = load_user(username)
        if user_data:
            full_name = f"{user_data['first_name']} {user_data['last_name']}"
            roles = user_data.get("roles", [])

            st.write(
                f"Hola **:{theme_extra_config['menu_name_color']}-background[{full_name.title()}]**"
            )

            # Definir accesos por rol
            role_permissions = {
                "admin": {
                    "pages/dashboard.py": "Inicio",
                    "pages/profile.py": "Perfil",
                    "pages/assistant.py": NOMBRE_ASISTENTE,
                    "pages/documents.py": "Archivos",
                    "pages/reports.py": "Reportes",
                    "pages/users.py": "Usuarios",
                },
                "user": {
                    "pages/dashboard.py": "Inicio",
                    "pages/profile.py": "Perfil",
                    "pages/assistant.py": NOMBRE_ASISTENTE,
                    "pages/documents.py": "Archivos",
                    "pages/reports.py": "Reportes",
                },
                "viewer": {
                    "pages/dashboard.py": "Inicio",
                    "pages/profile.py": "Perfil",
                    "pages/assistant.py": NOMBRE_ASISTENTE,
                },
            }

            # Orden de prioridad de roles
            role_priority = ["admin", "user", "viewer"]

            # Buscar el rol más importante que tenga el usuario
            selected_role = next(
                (role for role in role_priority if role in roles), "viewer"
            )

            # Obtener páginas según el rol más alto disponible
            user_pages = role_permissions.get(selected_role, {})

            # Crear menú con permisos asignados
            for page, label in user_pages.items():
                st.page_link(page, label=label, icon=f":material/{get_icon(label)}:")

            # Botón de salir
            if st.button("Salir"):
                print("btn salir")
                localS = getLocalS()
                localS.eraseItem("access_token")
                st.session_state.clear()
                time.sleep(0.5)
                st.rerun()

        else:
            st.error("Usuario no encontrado. Por favor, revise sus credenciales.")


def get_icon(label):
    """Asigna un icono basado en el nombre de la página"""
    icons = {
        "Inicio": "home",
        "Perfil": "account_box",
        "Sistere": "robot_2",
        "Archivos": "folder_open",
        "Reportes": "bar_chart",
        "Usuarios": "group",
    }
    return icons.get(label, "pageview")
