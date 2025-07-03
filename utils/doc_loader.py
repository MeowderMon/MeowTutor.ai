from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import streamlit as st

def load_and_chunk_text(text, chunk_size=1000, chunk_overlap=200):
    """Load text and split into chunks for processing"""
    try:
        # Create text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Split text into chunks
        chunks = text_splitter.split_text(text)
        
        # Convert to Document objects
        documents = [Document(page_content=chunk) for chunk in chunks]
        
        return documents
        
    except Exception as e:
        st.error(f"Error chunking text: {e}")
        return []

def create_document_from_text(text, metadata=None):
    """Create a Document object from text"""
    if metadata is None:
        metadata = {}
    
    return Document(page_content=text, metadata=metadata)
