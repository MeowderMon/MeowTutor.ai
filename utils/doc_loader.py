# utils/doc_loader.py

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List

def load_and_split_pdf(pdf_path: str) -> List[str]:
    """
    Loads a PDF from a file path and splits its content into chunks for LLM processing.
    """
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(docs)
    return [chunk.page_content for chunk in chunks]