# modules/reports/visuals/show_notification_reports.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from helpers.colors_reports import colors_allowed, get_opposite_bright_color
from modules.reports.utils.get_notification_reports import fetch_notification_data


def display_notification_types(data):
    if data:
        st.subheader("Distribución por Tipo de Notificación")
        df = pd.DataFrame(data)

        # Gráfico de pastel
        fig, ax = plt.subplots()
        ax.pie(df.set_index("type")["count"], autopct="%1.1f%%", startangle=90)
        ax.set_ylabel("")
        st.pyplot(fig)

        # Gráfico de barras
        st.bar_chart(df.set_index("type"))
    else:
        st.warning("No hay datos de tipos de notificación disponibles.")


def display_frequency_by_role(data):
    if data:
        st.subheader("Frecuencia de Notificaciones por Rol")
        df = pd.DataFrame(data)

        # Gráfico de barras
        st.bar_chart(df.set_index("role"))
    else:
        st.warning("No hay datos de frecuencia por rol disponibles.")


def display_notification_summary(summary):
    if summary:
        st.subheader("Resumen General de Notificaciones")

        # Métricas principales
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Notificaciones", summary["total_notifications"])
        with col2:
            st.metric("Tipo Más Común", summary["most_common_type"])
        with col3:
            st.metric("Rol Más Activo", summary["most_active_role"])
    else:
        st.warning("No hay datos de resumen disponibles.")


def show_notification_reports():
    n_notifications = st.number_input(
        "Número de notificaciones a analizar",
        min_value=1,
        value=100,
        step=10,
        help="Selecciona la cantidad de notificaciones a incluir en el análisis",
    )

    data = fetch_notification_data(n_notifications)

    if not data or any(v is None for v in data.values()):
        st.error("Error al cargar los datos de notificaciones")
        return

    display_notification_summary(data["notification_summary"])
    display_frequency_by_role(data["frequency_by_role"])
    display_notification_types(data["notification_types"])
