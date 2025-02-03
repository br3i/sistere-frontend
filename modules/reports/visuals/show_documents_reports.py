import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt
from modules.reports.utils.get_docs_reports import (
    get_top_documents,
    get_time_data,
    get_processing_metrics,
    get_resource_data,
)
from helpers.colors_reports import (
    colors_allowed,
    get_opposite_bright_color,
)


def fetch_data(n_docs):
    return {
        "top_documents": get_top_documents(n_docs),
        "time_data": get_time_data(n_docs),
        "processing_metrics": get_processing_metrics(n_docs),
        "resource_data": get_resource_data(n_docs),
    }


def display_top_documents(top_documents):
    if top_documents:
        st.subheader("Top 5 Documentos por Número de Solicitudes")
        df_top_docs = pd.DataFrame(top_documents).rename(
            columns={"name": "Nombre", "requests_count": "N° Solicitudes"}
        )
    if top_documents:
        df_top_docs = pd.DataFrame(top_documents)
        n_clrs_top_docs = random.sample(colors_allowed, 1)

        df_top_docs = df_top_docs.rename(
            columns={
                "name": "Nombre",
                "requests_count": "N° Solicitudes",
                "collection_name": "Colección",
                "path": "Enlace",
            }
        )

        st.dataframe(
            df_top_docs[["Nombre", "N° Solicitudes", "Colección", "Enlace"]],
            column_config={
                "Enlace": st.column_config.LinkColumn(
                    width="small",
                    display_text="💻",
                    required=True,
                    disabled=True,
                    max_chars=100,
                ),
            },
            hide_index=True,
            use_container_width=True,
        )

        st.subheader("Frecuencia de Solicitudes por Documento")
        st.bar_chart(
            df_top_docs.set_index("Nombre")["N° Solicitudes"], color=n_clrs_top_docs[0]
        )
    else:
        st.warning("No hay datos disponibles en este momento.")


def display_time_data(time_data):
    if time_data:
        df_time_data = pd.DataFrame(time_data)
        n_clrs_df_time_data = random.sample(colors_allowed, 2)
        comp_color_2 = get_opposite_bright_color(
            n_clrs_df_time_data[0]
        )  # Obtener color complementario pastel
        comp_color_3 = get_opposite_bright_color(
            n_clrs_df_time_data[1]
        )  # Obtener color complementario pastel
        df_time_data = df_time_data.rename(columns={"name": "Nombre"})
        df_time_data.set_index("Nombre", inplace=True)

        # Renombrar las columnas para mostrar etiquetas personalizadas
        df_time_data.rename(
            columns={
                "save_time": "Tiempo de Guardado (s)",
                "process_time": "Tiempo de Procesamiento (s)",
            },
            inplace=True,
        )

        # Gráfico de líneas con Streamlit (st.line_chart)
        st.subheader("Tiempos de Guardado y Procesamiento por Documento")
        st.line_chart(
            df_time_data[["Tiempo de Guardado (s)", "Tiempo de Procesamiento (s)"]],
            color=[comp_color_2, comp_color_3],
        )

        # Gráfico de área con Streamlit (st.area_chart)
        st.subheader("Área de Tiempo de Guardado y Procesamiento")
        st.area_chart(
            df_time_data[["Tiempo de Guardado (s)", "Tiempo de Procesamiento (s)"]],
            color=[comp_color_2, comp_color_3],
        )
    else:
        st.warning("No hay datos disponibles en este momento.")


def display_processing_metrics(processing_metrics):
    if processing_metrics:
        df_processing = pd.DataFrame(processing_metrics)
        n_clrs_df_processing = random.sample(colors_allowed, 2)
        comp_color_4 = get_opposite_bright_color(
            n_clrs_df_processing[0]
        )  # Obtener color complementario pastel
        comp_color_5 = get_opposite_bright_color(
            n_clrs_df_processing[1]
        )  # Obtener color complementario pastel
        df_processing = df_processing.rename(columns={"name": "Nombre"})
        df_processing.set_index("Nombre", inplace=True)

        # Renombrar las columnas para mostrar etiquetas personalizadas
        df_processing.rename(
            columns={
                "cpu_save": "Uso de CPU en Guardado (%)",
                "cpu_process": "Uso de CPU en Procesamiento (%)",
            },
            inplace=True,
        )

        # Gráfico de líneas con Streamlit (st.line_chart)
        st.subheader("Uso de CPU en Guardado y Procesamiento")
        st.line_chart(
            df_processing[
                ["Uso de CPU en Guardado (%)", "Uso de CPU en Procesamiento (%)"]
            ],
            color=[comp_color_4, comp_color_5],
        )
    else:
        st.warning("No hay datos disponibles en este momento.")


def display_resource_usage(resource_data):
    if resource_data:
        df_resources = pd.DataFrame(resource_data)
        n_clrs_df_resources = random.sample(colors_allowed, 2)
        comp_color_6 = get_opposite_bright_color(
            n_clrs_df_resources[0]
        )  # Obtener color complementario pastel
        comp_color_7 = get_opposite_bright_color(
            n_clrs_df_resources[1]
        )  # Obtener color complementario pastel
        df_resources = df_resources.rename(columns={"name": "Nombre"})

        # Crear las columnas de diferencia (cpu_diff, memory_diff) con nombres personalizados
        df_resources["Cambio en CPU"] = (
            df_resources["cpu_final"] - df_resources["cpu_initial"]
        )
        df_resources["Cambio en Memoria"] = (
            df_resources["memory_final"] - df_resources["memory_initial"]
        )

        # Renombrar las columnas para el gráfico
        df_resources.rename(
            columns={
                "Cambio en CPU": "Uso de CPU",
                "Cambio en Memoria": "Uso de Memoria",
            },
            inplace=True,
        )
        df_resources.set_index("Nombre", inplace=True)

        # Gráfico de barras con Streamlit (st.bar_chart)
        st.subheader("Uso de CPU y Memoria")
        st.bar_chart(
            df_resources[["Uso de CPU", "Uso de Memoria"]],
            color=[comp_color_6, comp_color_7],
        )

        # Asegurando que los valores negativos de `memory_diff` sean corregidos
        df_resources["Uso de Memoria"] = df_resources["Uso de Memoria"].apply(
            lambda x: max(x, 0)
        )  # Reemplazar valores negativos por 0

        # Escalado basado en el valor máximo de `Uso de Memoria`
        max_memory_diff = df_resources["Uso de Memoria"].max()

        # Asegurándonos de que no haya tamaños de puntos igual a 0
        min_size = 5  # Tamaño mínimo para los puntos
        max_size = 60  # Tamaño máximo para los puntos
        df_resources["scaled_size"] = (
            (df_resources["Uso de Memoria"] / max_memory_diff) * max_size
        ).apply(
            lambda x: max(min_size, min(x, max_size))
        )  # Limitar tamaño entre min_size y max_size

        # Gráfico de dispersión con Streamlit (st.scatter_chart)
        st.subheader("Evolución de Recursos por Documento")
        st.scatter_chart(
            df_resources[["Uso de CPU", "Uso de Memoria"]],
            color=[comp_color_6, comp_color_7],
        )

        # Gráfico de Matplotlib con Streamlit (st.pyplot)
        fig, ax = plt.subplots()
        ax.plot(df_resources.index, df_resources["Uso de CPU"], label="Uso de CPU")
        ax.plot(
            df_resources.index,
            df_resources["Uso de Memoria"],
            label="Uso de Memoria",
            linestyle="--",
        )
        ax.set_xlabel("Documento")
        ax.set_ylabel("Porcentaje")
        ax.set_title("Uso de CPU y Memoria")
        ax.legend()
        plt.xticks(rotation=90)
        st.pyplot(fig)
    else:
        st.warning("No hay datos disponibles en este momento.")


def show_documents_reports():
    n_docs = st.number_input(
        "Número de registros",
        help="Ingrese la cantidad de registros que desea obtener",
        min_value=1,
        value=15,
        step=1,
    )
    data = fetch_data(n_docs)

    if any(v is None for v in data.values()):
        st.warning("No se pudo cargar la información correctamente.")
        return

    display_top_documents(data["top_documents"])
    display_time_data(data["time_data"])
    display_processing_metrics(data["processing_metrics"])
    display_resource_usage(data["resource_data"])
