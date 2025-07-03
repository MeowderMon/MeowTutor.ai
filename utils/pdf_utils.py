from PyPDF2 import PdfReader
from typing import List
import io

def extract_pdf_text(uploaded_file: io.BytesIO) -> List[str]:
    """
    Extracts text page by page from an uploaded PDF file.
    Returns a list of strings, where each string is the text content of one page.
    """
    reader = PdfReader(uploaded_file)
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        pages.append(text if text else "")
    return pages
