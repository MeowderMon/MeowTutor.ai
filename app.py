import streamlit as st
import base64
import os

from quizzer.generator import generate_mcqs_from_text
from quizzer.scorer import score_quiz
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# ——— Setup Gemini LLM for Chatbot ——————————————
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
chat_llm = GoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=gemini_api_key)

# ——— PDF Embed Helper ————————————————————————
def show_pdf(path, height=800):
    """Embed a PDF in Streamlit via base64 Data URI."""
    with open(path, "rb") as f:
        pdf_bytes = f.read()
    b64 = base64.b64encode(pdf_bytes).decode("utf-8")
    iframe = f"""
        <iframe
            src="data:application/pdf;base64,{b64}"
            width="100%"
            height="{height}px"
            style="border: none;"
            type="application/pdf"
        ></iframe>
    """
    st.markdown(iframe, unsafe_allow_html=True)

# ——— Build a simple conversational QA chain —————————
def get_qa_chain(pdf_path):
    loader = PyMuPDFLoader(pdf_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return ConversationalRetrievalChain.from_llm(chat_llm, vectorstore.as_retriever())

# ——— Quiz UI —————————————————————————————————————
def show_mcq_interface(pdf_path):
    # 1) generate quiz
    if "quiz_questions" not in st.session_state or not st.session_state["quiz_questions"]:
        st.markdown("### 🧠 Generate a Quiz from PDF")
        num_mcqs = st.slider("Number of MCQs", 5, 20, 5, key="numq_slider")
        if st.button("Generate Quiz", key="gen_quiz_btn"):
            with st.spinner("🔄 Generating questions..."):
                loader = PyMuPDFLoader(pdf_path)
                docs = loader.load()
                full_text = "\n".join(d.page_content for d in docs)
                qs = generate_mcqs_from_text(full_text, num_questions=num_mcqs)
                if not qs:
                    st.error("❌ No questions generated. Check your API or PDF content.")
                    return
                st.session_state["quiz_questions"] = qs
            st.experimental_rerun()
        return

    # 2) display & answer
    st.markdown("### 📝 Take the Quiz")
    responses = []
    for i, q in enumerate(st.session_state["quiz_questions"]):
        st.markdown(f"**Q{i+1}. {q['question']}**")
        choice = st.radio("", q["options"], key=f"ans_{i}")
        responses.append(choice)
        st.markdown("---")

    # 3) score & show explanations
    if st.button("Submit Quiz", key="submit_quiz_btn"):
        score, results = score_quiz(responses, st.session_state["quiz_questions"])
        st.success(f"✅ You scored {score}/{len(responses)}")
        for idx, q in enumerate(st.session_state["quiz_questions"]):
            icon = "✅" if results[idx] else "❌"
            st.markdown(f"Q{idx+1}: {icon} Correct: **{q['answer']}**, You: {responses[idx]}")
            if q.get("explanation"):
                st.write(f"*Explanation:* {q['explanation']}")
            st.markdown("---")

# ——— Main App —————————————————————————————————————
def main():
    st.set_page_config(page_title="MeowTutor", layout="wide")
    st.title("🐱 MeowTutor")

    # Upload PDF
    uploaded = st.file_uploader("Upload a PDF", type=["pdf"])
    if not uploaded:
        return

    # Save to temp file
    pdf_path = os.path.join("temp.pdf")
    with open(pdf_path, "wb") as f:
        f.write(uploaded.read())

    # Choose mode
    mode = st.sidebar.selectbox("Mode", ["Reading Mode", "Testing Mode"])

    if mode == "Reading Mode":
        st.header("📖 Reading Mode")
        show_pdf(pdf_path)
        st.sidebar.markdown("### Chatbot")
        qa_chain = get_qa_chain(pdf_path)
        # Chat UI
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        query = st.sidebar.text_input("Ask something about the document…")
        if query:
            result = qa_chain({"question": query, "chat_history": st.session_state.chat_history})
            st.sidebar.markdown(f"**Answer:** {result['answer']}")
            st.session_state.chat_history = result["chat_history"]

    else:
        st.header("🧪 Testing Mode")
        show_mcq_interface(pdf_path)

if __name__ == "__main__":
    main()
