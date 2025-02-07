import streamlit as st
import jwt
import hashlib
from datetime import datetime

SECRET_KEY = st.secrets.get("SECRET_KEY")
SESSION_KEY = st.secrets.get("SESSION_KEY")
ALGORITHM = st.secrets.get("ALGORITHM")


# Función para verificar la firma del token
def verify_token_signature(payload: dict):
    try:
        # print(f"[verify_token_signature] Payload recibido: {payload}")

        # Obtener la firma del payload
        received_signature = payload.get("signature")
        # print(f"[verify_token_signature] Firma recibida: {received_signature}")

        if not received_signature:
            return False  # No hay firma en el payload

        # Regenerar la firma a partir de los datos en el payload
        expire_timestamp = payload["exp"]  # Tomamos el timestamp del payload
        session_data = f"{payload['sub']}:{expire_timestamp}:{SESSION_KEY}"
        # print(f"[verify_token_signature] Datos para generar firma: {session_data}")

        generated_signature = hashlib.sha256(session_data.encode()).hexdigest()
        # print(f"[verify_token_signature] Firma generada: {generated_signature}")

        # Verificar que las firmas coinciden
        if received_signature != generated_signature:
            return False  # La firma no coincide

        return True  # Firma válida

    except Exception as e:
        # print(f"[verify_token_signature] Error: {e}")
        return False  # Si hubo algún error en la verificación


# Función para validar el token y retornar el username si es válido
def is_token_valid(token: str):
    # print(f"[is_token_valid] Token recibido: {token}")

    try:
        # Decodificar el token sin verificar la firma (por ahora solo decodificamos)
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False}  # type: ignore
        )
        # print(f"[is_token_valid] Payload decodificado: {payload}")

        # Verificar la firma del token
        if not verify_token_signature(payload):
            return None  # Firma inválida

        # Verificación de la expiración
        exp_timestamp = payload.get("exp")
        # print(f"[is_token_valid] Timestamp de expiración: {exp_timestamp}")

        if exp_timestamp is None:
            # print("[is_token_valid] No se encontró el campo 'exp' en el token")
            return None  # Token sin campo de expiración

        # Comprobar si el token ha expirado
        current_time = datetime.now().timestamp()
        if current_time > exp_timestamp:
            # print("[is_token_valid] Token expirado")
            return None  # Token expirado

        # print("[is_token_valid] Token válido")
        username = payload.get("sub")  # Obtener el nombre de usuario del payload
        return (username, True)  # Retornar el nombre de usuario y True

    except jwt.ExpiredSignatureError as e:
        print(f"[is_token_valid] Token expirado {e}")
        return None  # Token expirado
    except jwt.InvalidTokenError as e:
        print(f"[is_token_valid] Token inválido {e}")
        return None  # Token inválido
