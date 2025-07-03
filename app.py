import streamlit as st
import fitz  
import base64
import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains.question_answering import load_qa_chain

from quizzer.generator import generate_mcqs_from_text
from quizzer.ui import show_mcq_interface
from quizzer.scorer import score_quiz

dotenv_path = os.path.join(os.getcwd(), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="MeowTutor", layout="wide")
st.title("📘 MeowTutor – Smart Reading & Testing Tutor")

if "pdf_path" not in st.session_state:
    st.session_state["pdf_path"] = None
if "mode" not in st.session_state:
    st.session_state["mode"] = None

st.subheader("📄 Upload your PDF")
uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])
if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())
    st.session_state["pdf_path"] = "temp.pdf"
    st.success("✅ PDF uploaded successfully! Now choose a mode.")

if st.session_state["pdf_path"]:
    st.subheader("🔀 Select Mode")
    mode = st.selectbox("Choose Mode", ["Reading Mode", "Testing Mode"])
    st.session_state["mode"] = mode

    if mode == "Reading Mode":
        st.header("📖 Reading Mode")
        col1, col2 = st.columns([4, 1])

        with open(st.session_state["pdf_path"], "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode("utf-8")
        pdf_html = f"""
        <div style='height:700px; overflow-y:scroll; border:1px solid #ccc;'>
            <iframe src='data:application/pdf;base64,{base64_pdf}' width='100%' height='100%' style='border:none;'></iframe>
        </div>
        """
        with col1:
            st.markdown(pdf_html, unsafe_allow_html=True)

        with col2:
            st.subheader("💬 Chatbot")
            query = st.text_input("Ask something about the document…")
            if query:
                with st.spinner("🔄 Thinking…"):
                    loader = PyMuPDFLoader(st.session_state["pdf_path"])
                    docs = loader.load()

                    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
                    vectordb = Chroma.from_documents(docs, embeddings)

                    llm = GoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GOOGLE_API_KEY)
                    chain = load_qa_chain(llm, chain_type="stuff")

                    results = vectordb.similarity_search(query)
                    answer = chain.run(input_documents=results, question=query)
                    st.markdown(f"**Answer:** {answer}")


    elif mode == "Testing Mode":
        st.header("🧠 Testing Mode")
        show_mcq_interface(st.session_state["pdf_path"])



else:
    st.info("Please upload a PDF file to proceed.")
