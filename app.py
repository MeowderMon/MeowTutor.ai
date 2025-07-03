import streamlit as st
import fitz  # PyMuPDF
import base64
import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain

from quizzer.generator import generate_mcqs_from_text
from quizzer.ui import show_mcq_interface
from quizzer.scorer import score_quiz

# Load API key
dotenv_path = os.path.join(os.getcwd(), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

# Set up Streamlit
st.set_page_config(page_title="MeowTutor", layout="wide")
st.title("\U0001F4D8 MeowTutor – Smart Reading & Testing Tutor")

# Helper to embed PDF using Streamlit native PDF rendering workaround
def show_pdf(path):
    with open(path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    pdf_display = f"""
    <iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700px" type="application/pdf"></iframe>
    <p><a href="data:application/pdf;base64,{base64_pdf}" download="document.pdf">📥 Download PDF</a></p>
    """
    st.markdown(pdf_display, unsafe_allow_html=True)

# Build Gemini-based QA Chain
def get_qa_chain(pdf_path, api_key):
    loader = PyMuPDFLoader(pdf_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    vectorstore = FAISS.from_documents(chunks, embeddings)

    llm = GoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)
    return ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever())

# Session state setup
if "pdf_path" not in st.session_state:
    st.session_state["pdf_path"] = None
if "mode" not in st.session_state:
    st.session_state["mode"] = None

# Upload PDF
st.subheader("\U0001F4C4 Upload your PDF")
uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])
if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())
    st.session_state["pdf_path"] = "temp.pdf"
    st.success("✅ PDF uploaded successfully! Now choose a mode.")

# If PDF is uploaded
if st.session_state["pdf_path"]:
    st.subheader("\U0001F500 Select Mode")
    mode = st.selectbox("Choose Mode", ["Reading Mode", "Testing Mode"])
    st.session_state["mode"] = mode

    if mode == "Reading Mode":
        st.header("\U0001F4D6 Reading Mode")
        col1, col2 = st.columns([4, 1])

        with col1:
            show_pdf(st.session_state["pdf_path"])

        with col2:
            st.subheader("\U0001F4AC Chatbot")
            query = st.text_input("Ask something about the document…")
            if query:
                with st.spinner("🔄 Thinking…"):
                    qa_chain = get_qa_chain(st.session_state["pdf_path"], GOOGLE_API_KEY)
                    result = qa_chain({"question": query, "chat_history": []})
                    st.markdown(f"**Answer:** {result['answer']}")

    elif mode == "Testing Mode":
        st.header("\U0001F9E0 Testing Mode")
        show_mcq_interface(st.session_state["pdf_path"])

else:
    st.info("Please upload a PDF file to proceed.")