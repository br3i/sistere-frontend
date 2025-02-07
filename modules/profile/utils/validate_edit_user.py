from modules.profile.utils.edit_user import edit_user
from helpers.validator_fields import (
    validate_email,
    validate_length,
    validate_name,
    validate_password,
    validate_username,
)


def validate_edit_user(
    id,
    first_name_new,
    last_name_new,
    username_new,
    email_new,
    password_new,
    repeat_password_new,
):
    first_name_new = first_name_new.strip()
    last_name_new = last_name_new.strip()
    username_new = username_new.strip()
    email_new = email_new.strip()
    password_new = password_new.strip()
    repeat_password_new = repeat_password_new.strip()
    if not validate_name(first_name_new):
        return "", None, "El primer nombre no es válido"
    if not validate_name(last_name_new):
        return "", None, "El apellido no es válido"
    if not validate_username(username_new):
        return "", None, "El nombre de usuario no es válido"
    if not validate_email(email_new):
        return "", None, "El correo electrónico no es válido"
    if password_new != "edit_profile":
        if not validate_length(password_new, 1) or not validate_length(
            repeat_password_new, 1
        ):
            return (
                "",
                None,
                "Los campos de contraseña/repetir contraseña no pueden estar vacíos",
            )
        if password_new != repeat_password_new:
            return "", None, "Las contraseñas no coinciden"
        if not validate_password(password_new):
            return "", None, "La contraseña no cumple con los criterios"

    return edit_user(
        id, first_name_new, last_name_new, username_new, email_new, password_new
    )
