import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt
from modules.reports.utils.get_docs_reports import (
    get_top_documents,
    get_time_data,
    get_time_data_save,
    get_time_data_process,
    get_processing_metrics,
    get_processing_metrics_cpu_save,
    get_processing_metrics_cpu_process,
    get_processing_metrics_memory_save,
    get_processing_metrics_memory_process,
    # get_resource_data,
)
from helpers.colors_reports import (
    colors_allowed,
    get_opposite_bright_color,
)


def fetch_data(n_docs):
    progress_placeholder = st.empty()
    total_steps = 9  # Total de pasos (las 9 métricas)

    # Cargar top_documents
    progress_placeholder.text(f"Cargando 1/{total_steps} - Documentos principales...")
    top_documents = get_top_documents(n_docs)

    # Cargar time_data
    progress_placeholder.text(f"Cargando 2/{total_steps} - Datos de tiempo...")
    time_data = get_time_data(n_docs)

    # Cargar time_data_save
    progress_placeholder.text(
        f"Cargando 3/{total_steps} - Datos de tiempo (Guardar)..."
    )
    time_data_save = get_time_data_save(n_docs)

    # Cargar time_data_process
    progress_placeholder.text(
        f"Cargando 4/{total_steps} - Datos de tiempo (Procesar)..."
    )
    time_data_process = get_time_data_process(n_docs)

    # Cargar processing_metrics
    progress_placeholder.text(
        f"Cargando 5/{total_steps} - Métricas de procesamiento..."
    )
    processing_metrics = get_processing_metrics(n_docs)

    # Cargar processing_metrics_cpu_save
    progress_placeholder.text(
        f"Cargando 6/{total_steps} - Métricas de CPU (Guardar)..."
    )
    processing_metrics_cpu_save = get_processing_metrics_cpu_save(n_docs)

    # Cargar processing_metrics_cpu_process
    progress_placeholder.text(
        f"Cargando 7/{total_steps} - Métricas de CPU (Procesar)..."
    )
    processing_metrics_cpu_process = get_processing_metrics_cpu_process(n_docs)

    # Cargar processing_metrics_memory_save
    progress_placeholder.text(
        f"Cargando 8/{total_steps} - Métricas de Memoria (Guardar)..."
    )
    processing_metrics_memory_save = get_processing_metrics_memory_save(n_docs)

    # Cargar processing_metrics_memory_process
    progress_placeholder.text(
        f"Cargando 9/{total_steps} - Métricas de Memoria (Procesar)..."
    )
    processing_metrics_memory_process = get_processing_metrics_memory_process(n_docs)

    progress_placeholder.empty()

    # # Cargar resource_data
    # progress_placeholder.text(f"Cargando 10/{total_steps} - Datos de recursos...")
    # resource_data = get_resource_data(n_docs)

    # Retornar los datos obtenidos
    return {
        "top_documents": top_documents,
        "time_data": time_data,
        "time_data_save": time_data_save,
        "time_data_process": time_data_process,
        "processing_metrics": processing_metrics,
        "processing_metrics_cpu_save": processing_metrics_cpu_save,
        "processing_metrics_cpu_process": processing_metrics_cpu_process,
        "processing_metrics_memory_save": processing_metrics_memory_save,
        "processing_metrics_memory_process": processing_metrics_memory_process,
        # "resource_data": resource_data,
    }


def display_top_documents(top_documents):
    if top_documents:
        st.subheader("Top Documentos por Número de Solicitudes")
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


def display_time_data_save(time_data_save):
    if time_data_save:
        print(f"[data_save_time] time_data_save \n\n{time_data_save}")
        df_time_data_save = pd.DataFrame(time_data_save)
        n_clrs_df_time_data_save = random.sample(colors_allowed, 2)
        comp_color_2 = get_opposite_bright_color(n_clrs_df_time_data_save[0])

        # Renombrar la columna "name" a "Nombre"
        df_time_data_save = df_time_data_save.rename(columns={"name": "Nombre"})

        # Renombrar "save_time" a "Tiempo de Guardado (s)"
        df_time_data_save.rename(
            columns={"save_time": "Tiempo de Guardado (s)"}, inplace=True
        )

        # Crear una nueva columna "N°" con el índice manual (empezando en 1)
        df_time_data_save["N°"] = df_time_data_save.index + 1

        # Eliminar el índice original (sin mostrar la columna de índice adicional)
        df_time_data_save.reset_index(drop=True, inplace=True)

        # Crear las columnas para el gráfico y la tabla
        col1, col2 = st.columns([0.75, 0.25], gap="small")

        # Gráfico de líneas con Streamlit (st.line_chart) en la primera columna
        with col1:
            st.subheader("Tiempos de Guardado en Orden")
            st.line_chart(
                df_time_data_save["Tiempo de Guardado (s)"], color=[comp_color_2]
            )

        # Mostrar la tabla en la segunda columna
        with col2:
            # Mostrar el dataframe con st.dataframe y ocultar el índice
            st.dataframe(df_time_data_save[["N°", "Nombre"]], hide_index=True)

    else:
        st.warning("No hay datos disponibles en este momento.")


def display_time_data_process(time_data_process):
    if time_data_process:
        print(f"[data_process_time] time_data_process \n\n{time_data_process}")
        df_time_data_process = pd.DataFrame(time_data_process)
        n_clrs_df_time_data_process = random.sample(colors_allowed, 2)
        comp_color_2 = get_opposite_bright_color(n_clrs_df_time_data_process[0])

        # Renombrar la columna "name" a "Nombre"
        df_time_data_process = df_time_data_process.rename(columns={"name": "Nombre"})

        # Renombrar "process_time" a "Tiempo de Procesamiento (s)"
        df_time_data_process.rename(
            columns={"process_time": "Tiempo de Procesamiento (s)"}, inplace=True
        )

        # Crear una nueva columna "N°" con el índice manual (empezando en 1)
        df_time_data_process["N°"] = df_time_data_process.index + 1

        # Eliminar el índice original (sin mostrar la columna de índice adicional)
        df_time_data_process.reset_index(drop=True, inplace=True)

        # Crear las columnas para los gráficos y la tabla
        col1, col2 = st.columns([0.75, 0.25], gap="small")

        # Gráfico de líneas con Streamlit (st.line_chart) en la primera columna
        with col1:
            st.subheader("Tiempos de Procesamiento en Orden")
            st.line_chart(
                df_time_data_process["Tiempo de Procesamiento (s)"],
                color=[comp_color_2],
            )

        # Mostrar la tabla con la información procesada
        with col2:
            # Mostrar el dataframe con st.dataframe y ocultar el índice
            st.dataframe(df_time_data_process[["N°", "Nombre"]], hide_index=True)

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


def display_processing_metrics_cpu_save(processing_metrics_save):
    if processing_metrics_save:
        df_processing_save = pd.DataFrame(processing_metrics_save)
        n_clrs_df_processing_save = random.sample(colors_allowed, 2)
        comp_color_4 = get_opposite_bright_color(n_clrs_df_processing_save[0])

        # Renombrar la columna "name" a "Nombre"
        df_processing_save = df_processing_save.rename(columns={"name": "Nombre"})

        # Renombrar "cpu_save" a "Uso de CPU en Guardado (%)"
        df_processing_save.rename(
            columns={"cpu_save": "Uso de CPU en Guardado (%)"}, inplace=True
        )

        # Crear una nueva columna "N°" con el índice manual (empezando en 1)
        df_processing_save["N°"] = df_processing_save.index + 1

        # Eliminar el índice original (sin mostrar la columna de índice adicional)
        df_processing_save.reset_index(drop=True, inplace=True)

        # Crear las columnas para el gráfico y la tabla
        col1, col2 = st.columns([0.75, 0.25], gap="small")

        # Gráfico de líneas con Streamlit (st.line_chart) en la primera columna
        with col1:
            st.subheader("Uso de CPU en Guardado en Orden")
            st.line_chart(
                df_processing_save["Uso de CPU en Guardado (%)"], color=[comp_color_4]
            )

        # Mostrar la tabla en la segunda columna
        with col2:
            # Mostrar el dataframe con st.dataframe y ocultar el índice
            st.dataframe(df_processing_save[["N°", "Nombre"]], hide_index=True)

    else:
        st.warning("No hay datos disponibles en este momento.")


def display_processing_metrics_cpu_process(
    processing_metrics_process,
):
    if processing_metrics_process:
        df_processing_process = pd.DataFrame(processing_metrics_process)
        n_clrs_df_processing_process = random.sample(colors_allowed, 2)
        comp_color_5 = get_opposite_bright_color(n_clrs_df_processing_process[0])

        # Renombrar la columna "name" a "Nombre"
        df_processing_process = df_processing_process.rename(columns={"name": "Nombre"})

        # Renombrar "cpu_process" a "Uso de CPU en Guardado (%)"
        df_processing_process.rename(
            columns={"cpu_process": "Uso de CPU en Procesamiento (%)"}, inplace=True
        )

        # Crear una nueva columna "N°" con el índice manual (empezando en 1)
        df_processing_process["N°"] = df_processing_process.index + 1

        # Eliminar el índice original (sin mostrar la columna de índice adicional)
        df_processing_process.reset_index(drop=True, inplace=True)

        # Crear las columnas para el gráfico y la tabla
        col1, col2 = st.columns([0.75, 0.25], gap="small")

        # Gráfico de líneas con Streamlit (st.line_chart) en la primera columna
        with col1:
            st.subheader("Uso de CPU en Procesamiento en Orden")
            st.line_chart(
                df_processing_process["Uso de CPU en Procesamiento (%)"],
                color=[comp_color_5],
            )

        # Mostrar la tabla en la segunda columna
        with col2:
            # Mostrar el dataframe con st.dataframe y ocultar el índice
            st.dataframe(df_processing_process[["N°", "Nombre"]], hide_index=True)

    else:
        st.warning("No hay datos disponibles en este momento.")


def display_processing_metrics_memory_save(
    processing_metrics_memory_save,
):
    if processing_metrics_memory_save:
        df_processing_memory_save = pd.DataFrame(processing_metrics_memory_save)
        n_clrs_df_processing_memory_save = random.sample(colors_allowed, 2)
        comp_color_6 = get_opposite_bright_color(n_clrs_df_processing_memory_save[0])

        # Renombrar la columna "name" a "Nombre"
        df_processing_memory_save = df_processing_memory_save.rename(
            columns={"name": "Nombre"}
        )

        # Renombrar "memory_save" a "Uso de Memoria en Guardado (MB)"
        df_processing_memory_save.rename(
            columns={"memory_save": "Uso de Memoria en Guardado (MB)"}, inplace=True
        )

        # Crear una nueva columna "N°" con el índice manual (empezando en 1)
        df_processing_memory_save["N°"] = df_processing_memory_save.index + 1

        # Eliminar el índice original (sin mostrar la columna de índice adicional)
        df_processing_memory_save.reset_index(drop=True, inplace=True)

        # Crear las columnas para el gráfico y la tabla
        col1, col2 = st.columns([0.75, 0.25], gap="small")

        # Gráfico de líneas con Streamlit (st.line_chart) en la primera columna
        with col1:
            st.subheader("Uso de Memoria en Guardado")
            st.line_chart(
                df_processing_memory_save["Uso de Memoria en Guardado (MB)"],
                color=[comp_color_6],
            )

        # Mostrar la tabla en la segunda columna
        with col2:
            # Mostrar el dataframe con st.dataframe y ocultar el índice
            st.dataframe(df_processing_memory_save[["N°", "Nombre"]], hide_index=True)

    else:
        st.warning("No hay datos disponibles en este momento.")


def display_processing_metrics_memory_process(
    processing_metrics_memory_process,
):
    if processing_metrics_memory_process:
        df_processing_memory_process = pd.DataFrame(processing_metrics_memory_process)
        n_clrs_df_processing_memory_process = random.sample(colors_allowed, 2)
        comp_color_7 = get_opposite_bright_color(n_clrs_df_processing_memory_process[0])

        # Renombrar la columna "name" a "Nombre"
        df_processing_memory_process = df_processing_memory_process.rename(
            columns={"name": "Nombre"}
        )

        # Renombrar "memory_process" a "Uso de Memoria en Procesamiento (MB)"
        df_processing_memory_process.rename(
            columns={"memory_process": "Uso de Memoria en Procesamiento (MB)"},
            inplace=True,
        )

        # Crear una nueva columna "N°" con el índice manual (empezando en 1)
        df_processing_memory_process["N°"] = df_processing_memory_process.index + 1

        # Eliminar el índice original (sin mostrar la columna de índice adicional)
        df_processing_memory_process.reset_index(drop=True, inplace=True)

        # Crear las columnas para el gráfico y la tabla
        col1, col2 = st.columns([0.75, 0.25], gap="small")

        # Gráfico de líneas con Streamlit (st.line_chart) en la primera columna
        with col1:
            st.subheader("Uso de Memoria en Procesamiento")
            st.line_chart(
                df_processing_memory_process["Uso de Memoria en Procesamiento (MB)"],
                color=[comp_color_7],
            )

        # Mostrar la tabla en la segunda columna
        with col2:
            # Mostrar el dataframe con st.dataframe y ocultar el índice
            st.dataframe(
                df_processing_memory_process[["N°", "Nombre"]], hide_index=True
            )

    else:
        st.warning("No hay datos disponibles en este momento.")


def display_resource_usage(resource_data):
    if resource_data:
        df_resources = pd.DataFrame(resource_data)
        n_clrs_df_resources = random.sample(colors_allowed, 2)
        comp_color_6 = get_opposite_bright_color(
            n_clrs_df_resources[0]
        )  # Color complementario 1
        comp_color_7 = get_opposite_bright_color(
            n_clrs_df_resources[1]
        )  # Color complementario 2

        # Renombrar columna "name" a "Nombre"
        df_resources = df_resources.rename(columns={"name": "Nombre"})

        # Crear las columnas de diferencia (cpu_diff, memory_diff) con nombres personalizados
        df_resources["Cambio en CPU"] = (
            df_resources["cpu_final"] - df_resources["cpu_initial"]
        )
        df_resources["Cambio en Memoria"] = (
            df_resources["memory_final"] - df_resources["memory_initial"]
        )

        # Renombrar las columnas para los gráficos
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

        # Asegurando que los valores negativos de "Uso de Memoria" sean corregidos
        df_resources["Uso de Memoria"] = df_resources["Uso de Memoria"].apply(
            lambda x: max(x, 0)
        )  # Reemplazar valores negativos por 0

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
    display_time_data_save(data["time_data_save"])
    display_time_data_process(data["time_data_process"])
    display_processing_metrics(data["processing_metrics"])
    display_processing_metrics_cpu_save(data["processing_metrics_cpu_save"])
    display_processing_metrics_cpu_process(data["processing_metrics_cpu_process"])
    display_processing_metrics_memory_save(data["processing_metrics_memory_save"])
    display_processing_metrics_memory_process(data["processing_metrics_memory_process"])
    # display_resource_usage(data["resource_data"])
