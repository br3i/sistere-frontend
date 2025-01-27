import fitz
from PIL import Image
import io


def extract_page_image_from_memory(pdf_bytes, page_number):
    try:
        pdf_document = fitz.open(stream=pdf_bytes)
        page = pdf_document.load_page(page_number - 1)
        pix = page.get_pixmap(dpi=300)  # type: ignore
        image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        return image
    except Exception as e:
        print(f"Error al extraer la página: {e}")
        return None
