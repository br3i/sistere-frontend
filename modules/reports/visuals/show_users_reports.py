# modules/reports/visuals/show_user_reports.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from helpers.colors_reports import colors_allowed, get_opposite_bright_color
from modules.reports.utils.get_users_reports import (
    get_role_distribution,
    get_active_users,
)


def fetch_user_data(n_users: int):
    return {
        "role_distribution": get_role_distribution(n_users),
        "active_users": get_active_users(n_users),
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


import pandas as pd
import streamlit as st


def display_active_users(data):
    if data:
        st.subheader("Usuarios Activos")

        # Convertir los datos a un DataFrame
        df = pd.DataFrame(data)

        # Asegurarnos de que 'created_at' sea del tipo datetime
        df["created_at"] = pd.to_datetime(df["created_at"])

        # Si quieres agrupar por fecha, podemos contar cuántos usuarios se crearon en cada fecha
        df_count_by_date = (
            df.groupby(df["created_at"].dt.date).size().reset_index(name="count")
        )

        # Mostrar la tabla de usuarios activos
        st.dataframe(df, hide_index=True, use_container_width=True)

        # Gráfico de barras por fecha de creación
        st.bar_chart(df_count_by_date.set_index("created_at"))
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

    display_active_users(data["active_users"])
    display_role_distribution(data["role_distribution"])
