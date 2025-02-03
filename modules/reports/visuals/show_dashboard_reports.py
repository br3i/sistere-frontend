import streamlit as st
from modules.reports.visuals.show_documents_reports import show_documents_reports
from modules.reports.visuals.show_feedback_reports import show_feedback_reports
from modules.reports.visuals.show_users_reports import show_users_reports
from modules.reports.visuals.show_notification_reports import show_notification_reports


def show_dashboard_reports():
    resports_options = [
        "Documentos",
        "Feedback",
        "Usuarios",
        "Notificaciones",
        "Rendimiento",
        "Códigos",
    ]
    # Crear pestañas para las diferentes funcionalidades
    report_selected = st.segmented_control(
        "Categoría",
        resports_options,
        selection_mode="single",
        default="Documentos",
        key="options_reports",
        help="Seleccione la categoría de la que desea ver los reportes",
        # on_change=None,
        # args=None,
        # kwargs=None,
        label_visibility="visible",
    )

    match report_selected:
        case "Documentos":
            with st.spinner("Cargando datos..."):
                show_documents_reports()
        case "Feedback":
            with st.spinner("Cargando datos..."):
                show_feedback_reports()
        case "Usuarios":
            with st.spinner("Cargando datos..."):
                show_users_reports()
        case "Notificaciones":
            with st.spinner("Cargando datos..."):
                show_notification_reports()
        case "Rendimiento":
            print("Mostrando reportes de Rendimiento")
        case "Códigos":
            print("Mostrando reportes de Códigos")
        case _:
            print("Selección no válida")
