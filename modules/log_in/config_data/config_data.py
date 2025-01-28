import streamlit as st
import io
import yaml
import pytz
from datetime import datetime
from pathlib import Path
from datetime import datetime, timedelta
from modules.log_in.cache_data.load_data import load_users
from modules.log_in.supabase_client import get_client_supabase

TIME_ZONE = st.secrets.get("TIME_ZONE", "America/Guayaquil")

tz = pytz.timezone(TIME_ZONE)

# Datos predeterminados para el primer inicio
default_config = {
    "cookie": {
        "expiry_days": 1,
        "key": "key_sistere",
        "name": "cookie_sistere",
        "last_date": None,  # Inicialmente no hay fecha
    },
    "credentials": {"usernames": {}},
}


is_creating_config = False


def initialize_config():
    try:
        supabase = get_client_supabase()
        try:
            supabase.storage.from_("config").download("config.yaml")
        except Exception as e:
            yaml_data = yaml.dump(default_config)

            yaml_bytes = io.BytesIO(yaml_data.encode("utf-8"))

            response = supabase.storage.from_("config").upload(
                "config.yaml", yaml_bytes.getvalue()
            )
            if response:
                print(
                    f"[initialize_config] se subió y ahora se manda a actualizar: {response}"
                )
                update_users_in_yaml()
            else:
                print("Error creando el archivo config")
    except Exception as e:
        print(f"Error tratando de inicializar la configuración: {e}")


def load_config():
    try:
        supabase = get_client_supabase()
        file = supabase.storage.from_("config").download("config.yaml")
        # Convertir el archivo descargado en un objeto de archivo en memoria
        file_io = io.BytesIO(file)

        # Cargar el contenido YAML desde el archivo en memoria
        config = yaml.safe_load(file_io)
        print(f"[load_confing] config: {config}")

        return config
    except Exception as e:
        print("Error al obtener los datos de configuración, inicializando...")
        initialize_config()


def save_config(data):
    print("[save_config]")
    try:
        supabase = get_client_supabase()

        yaml_data = yaml.dump(data)

        yaml_bytes = io.BytesIO(yaml_data.encode("utf-8"))

        file = supabase.storage.from_("config").update(
            "config.yaml", yaml_bytes.getvalue()
        )
        print(f"[save_config] file: {file}")
    except Exception as e:
        print(f"[save_config] Error tratanto de guardar el archivo: {e}")


def is_session_valid(username):
    config = load_config()
    try:
        supabase = get_client_supabase()
        file = supabase.storage.from_("config").download("config.yaml")

        file_io = io.BytesIO(file)

        config = yaml.safe_load(file_io)

        user_data = config["credentials"]["usernames"].get(username)
        if not user_data or not user_data.get("logged_in"):
            return False
        last_login = datetime.fromisoformat(user_data["last_login"])
        expiry_days = config["cookie"]["expiry_days"]
        current_time = datetime.now(tz)
        return current_time - last_login <= timedelta(days=expiry_days)
    except Exception as e:
        print(f"[is_session_valir] Error inesperado: {e}")


def update_users_in_yaml():
    load_users.clear()
    users = load_users()  # Suponiendo que esta función carga una lista de usuarios
    print("[update_users_in_yaml] users: ", users)

    if users:
        config = load_config()  # Cargar el config desde Supabase
        print("[update_users_in_yaml] config: ", config)

        if config is not None:
            # Crear un mapeo entre los 'id' de los usuarios y sus 'username'
            id_mapping = {user["id"]: user["username"] for user in users}

            # Si config["credentials"]["usernames"] está vacío, podemos agregar los mapeos aquí
            if not config["credentials"]["usernames"]:
                config["credentials"]["usernames"] = id_mapping

            # Iterar sobre los usuarios y realizar la actualización según el mapeo
            for user in users:
                user_id = user["id"]
                if user_id in id_mapping:
                    # Encontrar el username actual basado en el id
                    current_username = id_mapping[user_id]

                    # Actualizar los datos existentes
                    config["credentials"]["usernames"][current_username] = {
                        "email": user["email"],
                        "first_name": user["first_name"],
                        "last_name": user["last_name"],
                        "logged_in": config["credentials"]["usernames"]
                        .get(current_username, {})
                        .get("logged_in", False),
                        "last_login": config["credentials"]["usernames"]
                        .get(current_username, {})
                        .get("last_login", None),
                        "roles": user["roles"],
                        "id": user_id,  # Asegurarnos de mantener el id
                    }

                    # Si cambió el username, renombrar la clave en el YAML
                    if current_username != user["username"]:
                        # Renombrar la clave en el diccionario
                        config["credentials"]["usernames"][user["username"]] = config[
                            "credentials"
                        ]["usernames"].pop(current_username)
                else:
                    # Si no existe el usuario, crearlo
                    config["credentials"]["usernames"][user["username"]] = {
                        "email": user["email"],
                        "first_name": user["first_name"],
                        "last_name": user["last_name"],
                        "logged_in": False,
                        "last_login": None,
                        "roles": user["roles"],
                        "id": user_id,
                    }

            # Imprimir para verificar los cambios
            print("[update_users_in_yaml] Updated config: ", config)

            save_config(config)
        else:
            print("[update_users_in_yaml] Error, el archivo config es: ", config)
    else:
        print(
            "[update_users_in_yaml] Error, no se obtuvieron usuarios de la base de datos"
        )


def sync_deleted_users():
    # Cargar usuarios actuales desde la base de datos
    load_users.clear()
    users_from_db = load_users()

    # Cargar configuración desde el archivo YAML
    config = load_config()

    if config is not None:
        # Obtener IDs de usuarios desde la base de datos
        db_user_ids = {user["id"] for user in users_from_db} if users_from_db else set()

        # Crear un mapeo entre usernames e IDs en el archivo YAML
        yaml_user_ids = {
            username: details["id"]
            for username, details in config["credentials"]["usernames"].items()
            if "id" in details
        }

        # Identificar usuarios que ya no están en la base de datos
        users_to_remove = [
            username
            for username, user_id in yaml_user_ids.items()
            if user_id not in db_user_ids
        ]

        # Eliminar usuarios obsoletos del archivo YAML
        for username in users_to_remove:
            del config["credentials"]["usernames"][username]
            print(f"Usuario eliminado del archivo de configuración: {username}")

        # Guardar los cambios en el archivo YAML
        save_config(config)
        print(
            f"{len(users_to_remove)} usuarios eliminados del archivo de configuración."
        )
    else:
        print(f"[log_out] Error, confing es : {config}")


def logout_user(username):
    config = load_config()  # Cargar la configuración actual
    if config is not None:
        print(f"\n\n[logout_user] config: {config}")
        user_data = config["credentials"]["usernames"].get(username)

        if user_data:
            # Actualizar el campo logged_in a false
            user_data["logged_in"] = False
            # Opcional: Actualizar la fecha de cierre de sesión, si deseas llevar un registro
            user_data["last_login"] = (
                None  # O usa datetime.now(tz).isoformat() si quieres registrar algo
            )
            # Guardar los cambios en el archivo de configuración
            save_config(config)
            print(f"Usuario '{username}' cerrado correctamente.")
        else:
            print(f"Usuario '{username}' no encontrado en el archivo de configuración.")
    else:
        print(f"[log_out] Error, confing es : {config}")


# Función para manejar el cierre de sesión
def handle_logout():
    username = st.session_state.get("username")
    if username:
        print(f"[handle_logout] username : {username}")
        logout_user(username)
        st.session_state.clear()
        st.rerun()
    else:
        print("[handle_logout] username, no se encontró")
