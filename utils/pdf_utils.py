import PyPDF2
import fitz  # PyMuPDF
import streamlit as st
from io import BytesIO

def extract_text_from_pdf(uploaded_file):
        try:
            # Fallback to PyPDF2
            pdf_bytes = uploaded_file.getvalue()
            pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_bytes))
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text
            
        except Exception as e2:
            st.error(f"Both PDF readers failed: {e2}")
            return ""

def get_pdf_page_count(uploaded_file):
    """Get number of pages in PDF"""
    try:
        pdf_bytes = uploaded_file.getvalue()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page_count = len(doc)
        doc.close()
        return page_count
    except:
        return 0

def extract_text_from_page(uploaded_file, page_number):
    """Extract text from specific page"""
    try:
        pdf_bytes = uploaded_file.getvalue()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        if page_number < len(doc):
            page = doc.load_page(page_number)
            text = page.get_text()
            doc.close()
            return text
        else:
            doc.close()
            return ""
            
    except Exception as e:
        st.error(f"Error extracting text from page {page_number}: {e}")
        return ""
