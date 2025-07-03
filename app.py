import os, base64, streamlit as st
from dotenv import load_dotenv
from utils.helpers      import setup_page_config, get_session_state
from utils.pdf_utils    import extract_text_from_pdf
from utils.doc_loader   import load_and_chunk_text
from chatbot.chatbot    import create_chatbot_chain
from quizzer.generator  import generate_quiz
from quizzer.ui         import display_quiz_interface

load_dotenv()


# ── small helper to embed PDF ───────────────────────────────────
def display_pdf(uploaded) -> bool:
    if not uploaded:
        return False
    try:
        b64 = base64.b64encode(uploaded.getvalue()).decode()
        st.markdown(
            f"""
            <div style="width:100%;height:800px;border:2px solid #e0e0e0;
                        border-radius:8px;overflow:hidden">
              <embed src="data:application/pdf;base64,{b64}" type="application/pdf"
                     width="100%" height="100%">
            </div>
            """,
            unsafe_allow_html=True,
        )
        return True
    except Exception as e:
        st.error(e)
        return False


# ────────────────────────────────────────────────────────────────
def main():
    setup_page_config()
    get_session_state()

    st.title("🐱 MeowTutor.ai")
    st.caption("AI-powered reading & testing with your own PDFs")

    uploaded = st.file_uploader("Upload a PDF", type="pdf")
    if not uploaded:
        st.stop()

    mode = st.radio("Select Mode", ["📖 Reading", "🧠 Testing"], horizontal=True)

    # =======================================================
    # 📖  READING
    # =======================================================
    if mode.startswith("📖"):
        col1, col2 = st.columns([3, 2])

        with col1:
            st.subheader("PDF")
            display_pdf(uploaded)

        with col2:
            st.subheader("AI Tutor")

            # init chain once
            if "chatbot_chain" not in st.session_state:
                text = extract_text_from_pdf(uploaded)
                docs = load_and_chunk_text(text)
                st.session_state.chatbot_chain = create_chatbot_chain(docs)
                st.session_state.chat_history  = []

            # show history
            for i, (q, a) in enumerate(st.session_state.chat_history, 1):
                with st.expander(f"Q{i}: {q[:50]}"):
                    st.markdown(f"**You:** {q}")
                    st.markdown(f"**AI:**  {a}")

            # form (no manual session-state hacks)
            with st.form("chat"):
                user_q = st.text_input("Ask a question")
                sent   = st.form_submit_button("Ask AI Tutor")

            if sent and user_q.strip():
                out   = st.session_state.chatbot_chain({"question": user_q})
                answer = out["answer"]
                st.session_state.chat_history.append((user_q, answer))
                st.markdown(f"**AI Tutor:** {answer}")

    # =======================================================
    # 🧠  TESTING
    # =======================================================
    else:
        st.header("Testing Mode")
        n_qs = st.slider("Questions", 5, 20, 10)
        diff = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])

        if st.button("Generate Quiz"):
            with st.spinner("Generating…"):
                quiz = generate_quiz(extract_text_from_pdf(uploaded), n_qs, diff)
                if quiz.get("questions"):
                    st.session_state.quiz_data = quiz
                    st.session_state.quiz_generated = True
                else:
                    st.session_state.quiz_generated = False

        if st.session_state.get("quiz_generated"):
            display_quiz_interface(st.session_state.quiz_data)


if __name__ == "__main__":
    main()
