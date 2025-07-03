# ───────────────────────────────────────────────────────────────
#  app.py  –  MeowTutor.ai  (07-2025)
# ───────────────────────────────────────────────────────────────
import os, base64, streamlit as st
from dotenv import load_dotenv

# local helper modules (same as before)
from utils.helpers      import setup_page_config, get_session_state
from utils.pdf_utils    import extract_text_from_pdf
from utils.doc_loader   import load_and_chunk_text
from chatbot.chatbot    import create_chatbot_chain
from quizzer.generator  import generate_quiz
from quizzer.ui         import display_quiz_interface

load_dotenv()                         # read GOOGLE_API_KEY, etc.


# ───────────────────────────────────────────────────────────────
# PDF viewer that works on Streamlit Cloud (simple <embed>)
# ───────────────────────────────────────────────────────────────
def display_pdf(uploaded_file) -> bool:
    if not uploaded_file:
        return False
    try:
        b64 = base64.b64encode(uploaded_file.getvalue()).decode()
        st.markdown(
            f"""
            <style>
              .pdfbox{{width:100%;height:800px;border:2px solid #e0e0e0;
                      border-radius:8px;overflow:hidden}}
              .pdfbox embed{{width:100%;height:100%;border:none}}
            </style>
            <div class="pdfbox">
              <embed src="data:application/pdf;base64,{b64}"
                     type="application/pdf">
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.download_button("📥  Download PDF",
                           data=uploaded_file.getvalue(),
                           file_name=uploaded_file.name,
                           mime="application/pdf")
        return True
    except Exception as e:
        st.error(f"PDF display failed: {e}")
        return False


# ───────────────────────────────────────────────────────────────
def main() -> None:
    # page / session init
    setup_page_config()
    get_session_state()

    st.title("🐱  MeowTutor.ai")
    st.caption("AI-powered reading & testing with your own PDFs")

    # ── upload area ────────────────────────────────────────────
    uploaded = st.file_uploader(
        "Upload a PDF", type="pdf",
        on_change=lambda: st.session_state.update(
            chatbot_chain=None,
            chat_history=[],
            quiz_data=None,
            quiz_generated=False,
            quiz_answers={},
        ),
    )
    if not uploaded:
        st.stop()

    # ── mode picker ────────────────────────────────────────────
    mode = st.radio("Select Mode:",
                    ("📖 Reading Mode", "🧠 Testing Mode"),
                    horizontal=True)

    # ==========================================================
    # 📖  READING MODE
    # ==========================================================
    if mode.startswith("📖"):
        st.header("Reading Mode")
        col_pdf, col_chat = st.columns([3, 2])

        # ---------- left: PDF viewer --------------------------
        with col_pdf:
            st.subheader("PDF")
            if not display_pdf(uploaded):
                st.stop()

        # ---------- right: Chatbot ---------------------------
        with col_chat:
            st.subheader("AI Tutor")

            # ➊ initialise chain once per PDF
            if "chatbot_chain" not in st.session_state or st.session_state.chatbot_chain is None:
                with st.spinner("Initialising AI Tutor…"):
                    raw_text = extract_text_from_pdf(uploaded)
                    if not raw_text.strip():
                        st.error("PDF contains no selectable text.")
                        st.stop()

                    docs  = load_and_chunk_text(raw_text)
                    try:
                        st.session_state.chatbot_chain = create_chatbot_chain(docs)
                        st.session_state.chat_history  = []
                    except Exception as e:
                        st.error(f"Failed to start AI Tutor: {e}")
                        st.stop()

            # ➋ show previous Q&A
            for i, (q, a) in enumerate(st.session_state.chat_history, 1):
                with st.expander(f"Q{i}: {q[:60]}"):
                    st.markdown(f"**You:** {q}")
                    st.markdown(f"**AI:**  {a}")

            # ➌ one-click ask-answer form
            with st.form("chat_form", clear_on_submit=True):
                user_q   = st.text_input("Ask a question about the document")
                submitted = st.form_submit_button("Ask AI Tutor")

            if submitted and user_q.strip():
                chain = st.session_state.chatbot_chain
                try:
                    # get the key the chain expects ("input" or "question")
                    key   = chain.input_keys[0] if chain.input_keys else "question"
                    out   = chain.invoke({key: user_q})
                    answer = out["answer"]
                except Exception as e:
                    st.error(f"❌ AI error: {e}")
                else:
                    st.session_state.chat_history.append((user_q, answer))
                    st.markdown(f"**AI Tutor:** {answer}")

    # ==========================================================
    # 🧠  TESTING MODE
    # ==========================================================
    else:
        st.header("Testing Mode")

        n_qs       = st.slider("Number of questions", 5, 20, 10)
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])

        if st.button("Generate Quiz"):
            with st.spinner("Generating…"):
                quiz = generate_quiz(
                    extract_text_from_pdf(uploaded),
                    num_q=n_qs,
                    difficulty=difficulty,
                )
                if quiz.get("questions"):
                    st.session_state.quiz_data      = quiz
                    st.session_state.quiz_generated = True
                else:
                    st.error("Quiz generation failed.")
                    st.session_state.quiz_generated = False

        if st.session_state.get("quiz_generated"):
            display_quiz_interface(st.session_state.quiz_data)


# ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
