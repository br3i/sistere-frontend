import urllib.parse


def extract_relative_path(file_path: str) -> str:
    """
    Extrae la ruta relativa del archivo desde una URL completa.
    """
    parsed_url = urllib.parse.urlparse(file_path)
    # Obtiene la parte final del path
    return parsed_url.path.lstrip("/storage/v1/object/public/documents")
