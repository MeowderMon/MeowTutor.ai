import PyPDF2
import fitz  # PyMuPDF
import streamlit as st
from io import BytesIO
from pdf2image import convert_from_bytes
import pytesseract

def extract_text_from_pdf(uploaded_file):
    pdf_bytes = uploaded_file.getvalue()
    text = ""

    # ── Try PyPDF2 ───────────────────────────────
    try:
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_bytes))
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    except Exception as e1:
        st.warning(f"⚠️ PyPDF2 failed: {e1}")

    # ── Try PyMuPDF ──────────────────────────────
    if not text.strip():
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            for page in doc:
                page_text = page.get_text()
                if page_text:
                    text += page_text + "\n"
            doc.close()
        except Exception as e2:
            st.warning(f"⚠️ PyMuPDF failed: {e2}")

    # ── Final fallback: OCR ──────────────────────
    if not text.strip():
        try:
            images = convert_from_bytes(pdf_bytes, dpi=300)
            for img in images:
                ocr_text = pytesseract.image_to_string(img)
                if ocr_text.strip():
                    text += ocr_text + "\n"

            if text.strip():
                st.info("🧠 Used OCR to extract text from image-based PDF.")
            else:
                raise ValueError("OCR could not extract any meaningful text.")

        except Exception as e3:
            st.error(f"❌ OCR failed: {e3}")
            return ""

    # ── If still no text after all attempts ──────
    if not text.strip():
        raise ValueError("❌ No text was extracted from the PDF, so the AI Tutor cannot be initialised.")

    return text
