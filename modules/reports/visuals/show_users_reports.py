# modules/reports/visuals/show_user_reports.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from helpers.colors_reports import colors_allowed, get_opposite_bright_color
from modules.reports.utils.get_users_reports import (
    get_role_distribution,
    get_code_usage_by_role,
    get_active_users_metrics,
)


def fetch_user_data(n_users: int):
    return {
        "role_distribution": get_role_distribution(n_users),
        "code_usage": get_code_usage_by_role(n_users),
        "active_users": get_active_users_metrics(n_users),
    }


def display_role_distribution(data):
    if data:
        st.subheader("Distribución de Roles")
        df = pd.DataFrame(data)

        # Gráfico de pastel
        fig, ax = plt.subplots()
        ax.pie(df.set_index("role")["count"], autopct="%1.1f%%", startangle=90)
        ax.set_ylabel("")
        st.pyplot(fig)

        # Gráfico de barras
        st.bar_chart(df.set_index("role"))
    else:
        st.warning("No hay datos de roles disponibles.")


def display_code_usage(data):
    if data:
        st.subheader("Uso de Códigos por Rol")
        df = pd.DataFrame(data)

        # Calcular códigos por usuario
        df["codes_per_user"] = df["code_count"] / df["user_count"]

        col1, col2 = st.columns(2)
        with col1:
            st.write("### Estadísticas por Rol")
            st.dataframe(df.set_index("role"))
        with col2:
            st.write("### Códigos por Usuario")
            st.bar_chart(df.set_index("role")["codes_per_user"])
    else:
        st.warning("No hay datos de uso de códigos.")


def display_active_users(data):
    if data:
        st.subheader("Usuarios Activos por Rol")
        df = pd.DataFrame(data)

        # Gráfico de barras
        st.bar_chart(df.set_index("role"))
    else:
        st.warning("No hay datos de usuarios activos.")


def show_users_reports():
    n_users = st.number_input(
        "Número de usuarios a analizar",
        min_value=1,
        value=100,
        step=10,
        help="Selecciona la cantidad de usuarios a incluir en el análisis",
    )

    data = fetch_user_data(n_users)

    if not data or any(v is None for v in data.values()):
        st.error("Error al cargar los datos de usuarios")
        return

    display_code_usage(data["code_usage"])
    display_active_users(data["active_users"])
    display_role_distribution(data["role_distribution"])
