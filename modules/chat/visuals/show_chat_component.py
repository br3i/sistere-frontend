import streamlit as st
from modules.chat.utils.extract_page_image_from_memory import (
    extract_page_image_from_memory,
)
from modules.chat.utils.extrac_relative_path import extract_relative_path
from modules.log_in.supabase_client import get_client_supabase


def model_selector():
    model_selected = st.selectbox(
        "Modelo LLM",
        [
            "gemma2:27b",
            "granite3.1-dense",
            "mixtral:8x7b",
            "deepseek-r1:32b",
            "granite3.1-moe:3b",
        ],
        help="Seleccione el modelo, están ordenados de menor a mayor capacidad",
        index=0,
    )
    st.session_state.model_selected = model_selected


def show_sources_via_ws(sources):
    if sources:
        print(f"show_sources_visa_ws: sources {sources}")
        with st.status("Obteniendo fuentes..."):
            try:
                for index, source in enumerate(sources):
                    print(
                        f"Recibiendo imagen... (Iteración {index + 1}/{len(sources)})"
                    )

                    document_name = source.get("document_name", "")
                    file_path = extract_relative_path(source.get("file_path", ""))
                    resolve_page = int(source.get("resolve_page", 1))
                    print(f"[file_path] file_path: {file_path}")

                    # Obtener la URL para descargar el archivo desde Supabase
                    try:
                        client_supabase = get_client_supabase()
                        file = client_supabase.storage.from_("documents").download(
                            file_path
                        )
                        # Reemplaza con tu URL de Supabase y la configuración de almacenamiento

                        # Descargar el archivo desde Supabase
                        if file:
                            print("Archivo descargado con éxito.")
                            extracted_image = extract_page_image_from_memory(
                                file, resolve_page
                            )
                            st.link_button(
                                f":violet[Documento] {document_name} | :orange[Página] {resolve_page}",
                                source.get("file_path", ""),
                                help="Haga clic para visualizar el archivo",
                                icon=":material/public:",
                                use_container_width=True,
                            )
                            cols = st.columns([0.1, 0.8, 0.1], gap="small")
                            with cols[1]:
                                if extracted_image is not None:
                                    st.image(
                                        extracted_image,
                                        caption=f"Página {resolve_page} del documento",
                                        use_container_width=True,
                                    )
                                else:
                                    st.error(
                                        "No se pudo extraer la imagen de la página."
                                    )

                        else:
                            print(f"Error al descargar el archivo: {file}")
                            st.error(f"No se pudo descargar el archivo: {file_path}")
                    except Exception as e:
                        print(f"Error durante la ejecución: {e}")
                        st.error(f"Error al obtener el archivo de Supabase: {e}")

            except Exception as e:
                print(f"Error durante la ejecución: {e}")
    else:
        st.info("No se encontraron fuentes relevantes.")
