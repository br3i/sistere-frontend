import streamlit as st
from modules.chat.utils.extract_page_image_from_memory import (
    extract_page_image_from_memory,
)
from modules.chat.utils.extrac_relative_path import extract_relative_path
from modules.log_in.supabase_client import get_client_supabase

BACKEND_URL = st.secrets.get("BACKEND_URL", "Not Found")
BACKEND_WS_URL = st.secrets.get("BACKEND_WS_URL", "Not Found")

#!!!! Que sea un selectbox y pida los elementos del backend
# def model_selector(models_ollama):


#!! Solo con request
# def show_sources(sources):
#     # Comprobar si existen fuentes
#     if sources:
#         # print(f"[\n\n\show_chat_component]: {sources}\n\n\n")
#         # Mostrar el número de fuentes encontradas en el mensaje de estado
#         with st.status(f"Obteniendo fuentes. Encontradas: {len(sources)}"):
#             for source in sources:
#                 # Decodificar el nombre del archivo para mostrarlo correctamente
#                 # readable_file_path = urllib.parse.unquote(source.get("file_path", "Desconocido"))
#                 readable_document_name = urllib.parse.unquote(
#                     source.get("document_name", "Desconocido")
#                 )
#                 # print(f"[\n\n\nUSER_UTILS]readable_file_path: {readable_document_name}\n\n\n")
#                 resolve_page = int(source.get("resolve_page", "Desconocido"))
#                 st.markdown(
#                     f"- :violet[Documento]: {readable_document_name} | :orange[Página]: {resolve_page}"
#                 )

#                 # Hacer la solicitud al backend para obtener la imagen de la página
#                 document_url = f"{BACKEND_URL}/get_page_image?file_path={urllib.parse.quote(source['file_path'])}&resolve_page={resolve_page}"
#                 document_response = requests.get(document_url)

#                 if document_response.status_code == 200:
#                     # Mostrar la imagen recibida
#                     img = document_response.content
#                     cols = st.columns([0.1, 0.8, 0.1], gap="small")
#                     with cols[1]:
#                         st.image(
#                             img,
#                             caption=f"Página {resolve_page} del documento",
#                             use_container_width=True,
#                         )
#                         st.markdown(
#                             f"[:gray-background[Documento Completo]]({BACKEND_URL}/document/{urllib.parse.quote(readable_document_name)}.pdf)"
#                         )
#                 else:
#                     st.error("No se pudo obtener la imagen de la página del documento.")
#     else:
#         # Si no hay fuentes, mostrar un mensaje de error
#         with st.status("Obteniendo fuentes. Ninguna fuente encontrada."):
#             st.write("No se encontraron fuentes relevantes.")


def show_sources_via_ws(sources):
    if sources:
        with st.status("Obteniendo imágenes..."):
            try:
                for index, source in enumerate(sources):
                    print(
                        f"Recibiendo imagen... (Iteración {index + 1}/{len(sources)})"
                    )

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

                            # Mostrar la imagen en Streamlit
                            document_name = source.get("file_path", "Desconocido")
                            st.link_button(
                                f":violet[Documento] | :orange[Página] {resolve_page}",
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
