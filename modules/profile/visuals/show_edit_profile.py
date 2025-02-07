import streamlit as st
from modules.profile.utils.validate_edit_user import validate_edit_user

MAX_FIRSTNAME_LENGTH = int(st.secrets.get("MAX_FIRSTNAME_LENGTH", "Not found"))
MAX_LASTNAME_LENGTH = int(st.secrets.get("MAX_LASTNAME_LENGTH", "Not found"))
MAX_USERNAME_LENGTH = int(st.secrets.get("MAX_USERNAME_LENGTH", "Not found"))
MAX_PASSWORD_LENGTH = int(st.secrets.get("MAX_PASSWORD_LENGTH", "Not found"))


def show_edit_profile(user_data):
    print("[show_edit_profile] Se ejecuta")
    with st.form("frm_edit_profile", clear_on_submit=False):
        # Título del formulario
        st.subheader("Edición de perfil")

        col1, col2 = st.columns([0.5, 0.5], gap="small", vertical_alignment="center")
        with col1:
            first_name_input = st.text_input(
                "Primer nombre",
                value=user_data["first_name"],
                max_chars=MAX_FIRSTNAME_LENGTH,
                help="Ingrese un nuevo primer nombre",
                placeholder="Ingrese un nuevo primer nombre",
                label_visibility="visible",
            )

            last_name_input = st.text_input(
                "Apellido",
                value=user_data["last_name"],
                max_chars=MAX_LASTNAME_LENGTH,
                help="Ingrese un nuevo apellido",
                placeholder="Ingrese un nuevo primer apellido",
                label_visibility="visible",
            )

        with col2:
            username_input = st.text_input(
                "Usuario",
                value=user_data["username"],
                max_chars=MAX_USERNAME_LENGTH,
                help="Ingrese un nuevo nombre de usuario",
                placeholder="Ingrese un nuevo nombre de usuario",
                label_visibility="visible",
            )

            email_input = st.text_input(
                "Email",
                value=user_data["email"],
                help="""
                Ingresa una dirección de correo electrónico válida.\n
                Ejemplos:
                - usuario@gmail.com
                - nombre.apellido@outlook.com
                - contacto@empresa.com
                """,
                placeholder="usuario@correo.com",
                label_visibility="visible",
            )

        col3, col4 = st.columns([0.5, 0.5], gap="small", vertical_alignment="center")

        with col3:
            password_input = st.text_input(
                "Contraseña",
                type="password",
                max_chars=MAX_PASSWORD_LENGTH,
                help="Ingrese una nueva contraseña",
                placeholder="Ingrese una nueva contraseña",
                label_visibility="visible",
            )

        with col4:
            repeat_password_input = st.text_input(
                "Repetir Contraseña",
                type="password",
                max_chars=MAX_PASSWORD_LENGTH,
                help="Repetir contraseña",
                placeholder="Repetir contraseña",
                label_visibility="visible",
            )

        options_roles = user_data["roles"]
        # Diccionario de traducción a español con la primera letra en mayúscula
        roles_translation = {
            "user": "Usuario",
            "admin": "Administrador",
            "viewer": "Espectador",
        }

        translated_roles = [roles_translation[role] for role in options_roles]

        st.markdown(f"**:orange[Roles]:** {', '.join(translated_roles)}")

        if st.form_submit_button(label=":material/save:", type="primary"):
            return validate_edit_user(
                user_data["id"],
                first_name_input or "edit_profile",
                last_name_input or "edit_profile",
                username_input or "edit_profile",
                email_input or "edit_profile",
                password_input or "edit_profile",
                repeat_password_input or "edit_profile",
            )
        return None, False, None
