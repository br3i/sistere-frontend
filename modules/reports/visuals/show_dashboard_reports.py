import streamlit as st
from modules.reports.visuals.show_documents_reports import show_documents_reports
from modules.reports.visuals.show_users_reports import show_users_reports


def show_dashboard_reports():
    resports_options = [
        "Documentos",
        "Usuarios",
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
        case "Usuarios":
            with st.spinner("Cargando datos..."):
                show_users_reports()
        case _:
            print("Selección no válida")
