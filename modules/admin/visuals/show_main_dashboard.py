import streamlit as st
from datetime import datetime
from modules.admin.utils.active_users import active_users
from modules.admin.utils.get_requested_document import get_len_requested_document
from modules.documents.decorators.get_documents_from_db import get_len_documents_from_db

MAX_NOTIFICATIONS_HEIGHT = st.secrets.get("MAX_NOTIFICATIONS_HEIGHT", 10)


def show_main_dashboard(roles):
    print(f"[show_main_dashboard] roles: {roles}")
    st.header(
        "Dashboard de :orange[Administración] :material/admin_panel_settings:",
        divider="orange",
    )

    # Mostrar el contenido que no depende de las métricas
    st.subheader("Accesos Rápidos")

    # Diccionario de accesos rápidos con íconos
    ROLE_PERMISSIONS = {
        "admin": {
            "pages/profile.py": (":material/account_box:", "Perfil"),
            "pages/users.py": (":material/group:", "Usuarios"),
            "pages/documents.py": (":material/folder:", "Documentos"),
            "pages/reports.py": (":material/bar_chart:", "Reportes"),
        },
        "user": {
            "pages/profile.py": (":material/account_box:", "Perfil"),
            "pages/documents.py": (":material/folder:", "Documentos"),
            "pages/reports.py": (":material/bar_chart:", "Reportes"),
        },
        "viewer": {
            "pages/profile.py": (":material/account_box:", "Perfil"),
            "pages/settings.py": (":material/settings:", "Configuración"),
            "pages/help.py": (":material/help:", "Documentación"),
        },
    }

    # Definir prioridad de roles
    PRIORIDAD_ROLES = ["admin", "user", "viewer"]

    # Obtener el rol más alto del usuario
    roles_usuario = roles
    rol_activo = next((r for r in PRIORIDAD_ROLES if r in roles_usuario), "viewer")

    # Obtener accesos rápidos según el rol
    accesos_rapidos = ROLE_PERMISSIONS[rol_activo]

    # Crear columnas (máximo 4 por fila)
    cols = st.columns([0.25] * min(4, len(accesos_rapidos)), gap="small")

    # Iterar sobre accesos y colocarlos en las columnas
    for i, (page, (icon, label)) in enumerate(accesos_rapidos.items()):
        with cols[i % len(cols)]:  # Distribuir en las columnas de forma equitativa
            if st.button(
                f"{icon} {label}", key=f"btn_{label.lower()}", use_container_width=True
            ):
                st.switch_page(page)

    st.write("___")

    # Ahora, comenzar a mostrar las métricas
    st.subheader("Resumen del Sistema")

    # Usamos st.empty para crear lugares vacíos en cada columna
    # Primera fila (2 columnas)
    col4, col5, col6 = st.columns(3)

    with col4:
        placeholder_users = st.empty()  # Creamos un espacio vacío para los usuarios

    with col5:
        placeholder_docs_consulted = (
            st.empty()
        )  # Otro espacio vacío para los documentos
    with col6:
        placeholder_docs_loaded = st.empty()  # Otro espacio vacío para los documentos

    # Usamos un spinner para simular la carga
    with st.spinner("Cargando métricas de Usuarios..."):
        n_users = active_users()  # Aquí usas la función real para obtener los usuarios
        placeholder_users.metric(
            "Usuarios Registrados",
            n_users,
            help="Usuarios registrados en la Base de Datos",
            label_visibility="visible",
            border=True,
        )

    with st.spinner("Cargando métricas de Documentos Consultados..."):
        n_documents_consulted = get_len_requested_document()
        placeholder_docs_consulted.metric(
            "Documentos Consultados",
            n_documents_consulted,
            help="Documentos consultados",
            label_visibility="visible",
            border=True,
        )

    with st.spinner("Cargando métricas de Documentos Cargados..."):
        n_documents_loaded = get_len_documents_from_db()
        placeholder_docs_loaded.metric(
            "Documentos Cargados",
            n_documents_loaded,
            help="Documentos cargados en la Base de Datos",
            label_visibility="visible",
            border=True,
        )
