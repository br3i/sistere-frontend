import streamlit as st
import requests
from modules.menu.create_menu import create_menu
from modules.log_in.login import create_login
from modules.log_in.local_storage.local_storage import getLocalS

BACKEND_URL = st.secrets.get("BACKEND_URL", "Not found")

# Crear el placeholder para mostrar mensajes de carga
placeholder = st.empty()

if "username_logged" not in st.session_state:
    localS = getLocalS()
    access_token = localS.getItem("access_token")

    if access_token is None:
        placeholder = create_login(localS)
    else:
        try:
            response_validate = requests.get(
                f"{BACKEND_URL}/validate_token", json={"token": access_token}
            )

            if response_validate.status_code == 200:
                create_menu(response_validate.json().get("username"))
                # Crear pestañas para las diferentes funcionalidades
                tabs = st.tabs(["Report1", "Report2", "Report3"])

                with tabs[0]:
                    st.header(":green[Reporte1]")
                    with st.spinner("Cargando..."):
                        st.write(1)
                with tabs[1]:
                    st.header(":green[Reporte2]")
                    with st.spinner("Cargando Reportes..."):
                        st.write(2)
                with tabs[2]:
                    st.header(":red[Reporte3]")
                    with st.spinner("Cargando Reportes..."):
                        st.write(3)

            else:
                localS.eraseItem("access_token")
                placeholder = create_login(localS)
        except Exception as e:
            print(f"[admin] Error validando el token: {e}")
else:
    create_menu(st.session_state.username)
    # Crear pestañas para las diferentes funcionalidades
    tabs = st.tabs(["Report1", "Report2", "Report3"])

    with tabs[0]:
        st.header(":green[Reporte1]")
        with st.spinner("Cargando..."):
            st.write(1)
    with tabs[1]:
        st.header(":green[Reporte2]")
        with st.spinner("Cargando Reportes..."):
            st.write(2)
    with tabs[2]:
        st.header(":red[Reporte3]")
        with st.spinner("Cargando Reportes..."):
            st.write(3)
