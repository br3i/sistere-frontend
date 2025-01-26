import chromadb
from chromadb.api.shared_system_client import SharedSystemClient


# Crear cliente para conectarse a Chroma
def chroma_client():
    SharedSystemClient.clear_system_cache()
    chroma_client = chromadb.HttpClient(host="localhost", port=8000)
    # Limpiar la caché del sistema
    return chroma_client
