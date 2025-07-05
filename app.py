import os, base64, streamlit as st
from dotenv import load_dotenv

from utils.helpers      import setup_page_config, get_session_state
from utils.pdf_utils    import extract_text_from_pdf
from utils.doc_loader   import load_and_chunk_text
from chatbot.chatbot    import create_chatbot_chain
from quizzer.generator  import generate_quiz
from quizzer.ui         import display_quiz_interface

load_dotenv()


from streamlit_pdf_viewer import pdf_viewer

def display_pdf(uploaded):
    if uploaded:
        pdf_viewer(uploaded.getvalue(), width=700, height=900)


# ── Main Streamlit App ──────────────────────────────────────────────
def main():
    setup_page_config()
    get_session_state()
    # ── Injecting custom CSS ──────────────────────────────────────────
    # ── CYBERPUNK UI OVERHAUL ───────────────────────────────────────────────
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)


    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">

    <style>
    /* Global styles */
     html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        font-size: 16px;
        color: #f5f5f5;
        background-color: #2e2e2e !important;  /* Soft, modern gray */
        color: #f5f5f5 !important;
        background: linear-gradient(145deg, #2e2e2e, #3a3a3a, #1e1e1e);
        background-attachment: fixed;
        background-size: cover;
        background-repeat: no-repeat;
        overflow-x: hidden;
    }
    
    /* Gradient Text Headings */
    h1, h2, h3, h4 {
        background: linear-gradient(to right, #ff9900, #ffcc00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.5);
    }

    /* Widget styling */
    /* Fix input field background */
    .stTextInput > div > div > input {
        background-color: #1e1e1e !important; /* Or any gray you prefer */
        color: #f5f5f5 !important;
        border-radius: 10px;
        box-shadow: none !important;
        border: 1px solid #444 !important;
    }
    .stSelectbox>div>div>div>input,
    


    .stButton>button {
        background: linear-gradient(90deg, #00d2ff, #3a47d5);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 10px;
        padding: 0.6em 1.2em;
        box-shadow: 0 4px 12px rgba(0,212,255,0.3);
        transition: 0.3s ease-in-out;
    }

    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 18px rgba(0,212,255,0.4);
    }

    /* Radio button styling */
    .stRadio>div>label {
        background-color: #1e1e1e;
        border: 1px solid #3a47d5;
        border-radius: 12px;
        padding: 0.4em 0.8em;
        transition: all 0.2s ease-in-out;
    }

    .stRadio>div>label:hover {
        background-color: #2e2e2e;
        transform: scale(1.03);
        box-shadow: 0 0 10px rgba(0,212,255,0.2);
    }

    .stRadio>div>label[data-selected="true"] {
        background: linear-gradient(90deg, #00d2ff, #3a47d5);
        color: white !important;
        font-weight: 600;
    }

    /* Expander styling */
    .stExpander {
        border: 1px solid #3a47d5 !important;
        border-radius: 12px;
        background-color: #1a1a1a !important;
        box-shadow: 0 0 15px rgba(0,212,255,0.1);
    }
    .stExpanderHeader {
        color: #00d2ff !important;
        font-weight: bold;
    }

    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 10px;
    }
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(#00d2ff, #3a47d5);
        border-radius: 6px;
    }

    /* Floating paw print animation */
    @keyframes floatPaws {
        0%   { transform: translateY(0px) rotate(0deg); opacity: 0.08; }
        50%  { transform: translateY(-20px) rotate(10deg); opacity: 0.15; }
        100% { transform: translateY(0px) rotate(-5deg); opacity: 0.08; }
    }

    .paw-print {
        position: absolute;
        font-size: 60px;
        opacity: 0.08;
        animation: floatPaws 6s ease-in-out infinite;
        user-select: none;
        pointer-events: none;
        z-index: 0;
    }

    .paw1 { top: 60%; left: 10%; animation-delay: 0s; }
    .paw2 { top: 72%; left: 35%; animation-delay: 1s; }
    .paw3 { top: 78%; left: 70%; animation-delay: 2s; }
    .paw4 { top: 86%; left: 20%; animation-delay: 3s; }
    .paw5 { top: 91%; left: 60%; animation-delay: 4s; }
    </style>

    <!-- Paw prints using emoji 🐾 -->
    <div class="paw-print paw1">🐾</div>
    <div class="paw-print paw2">🐾</div>
    <div class="paw-print paw3">🐾</div>
    <div class="paw-print paw4">🐾</div>
    <div class="paw-print paw5">🐾</div>
    """, unsafe_allow_html=True)

    # Inject animated paw prints in random positions across the screen
    css = """
    <style>
    body {
        overflow-x: hidden;
        background: linear-gradient(135deg, #2e2e2e, #1e1e1e);
    }

    /* Floating paw animation */
    @keyframes floatPaws {
        0%   { transform: translateY(0px) rotate(0deg); opacity: 0.5; }
        50%  { transform: translateY(-10px) rotate(5deg); opacity: 0.6; }
        100% { transform: translateY(0px) rotate(-5deg); opacity: 0.5; }
    }

    .paw-print {
        position: fixed;
        font-size: 55px;
        opacity: 0.55;
        animation: floatPaws 7s ease-in-out infinite;
        user-select: none;
        pointer-events: none;
        z-index: 0;
    }
    """

    # Generate positions and corresponding class CSS
    positions = [
        (10, 5), (12, 40), (15, 75), (18, 20), (20, 60),
        (25, 10), (28, 30), (30, 55), (33, 80), (36, 15),
        (40, 50), (42, 70), (45, 25), (48, 90), (50, 35),
        (53, 5), (56, 60), (60, 40), (63, 75), (66, 20),
        (70, 10), (73, 50), (75, 80), (78, 30), (81, 65),
        (84, 15), (86, 90), (88, 45), (90, 70), (92, 25)
    ]

    paw_classes = "\n".join([
        f".paw{i} {{ top: {top}%; left: {left}%; animation-delay: {i % 5}s; }}"
        for i, (top, left) in enumerate(positions)
    ])

    paw_divs = "\n".join([
        f'<div class="paw-print paw{i}">🐾</div>'
        for i in range(len(positions))
    ])

    # Finally inject everything
    st.markdown(css + paw_classes + "</style>" + paw_divs, unsafe_allow_html=True)

    # Replace `st.title("🐱 MeowTutor.ai")` with:
    st.markdown("""
        <div style='text-align: center; padding-top: 10px; padding-bottom: 5px;'>
            <span style='font-size: 48px;'>🐱</span>
            <span style='
                font-size: 48px;
                font-weight: 700;
                background: linear-gradient(to right, #ff7e5f, #feb47b);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                display: inline-block;
            '>MeowTutor.ai</span>
        </div>
    """, unsafe_allow_html=True)

    #st.title("🐱 MeowTutor.ai")
    st.caption("AI-powered reading & testing with your own PDFs")

    uploaded = st.file_uploader("Upload a PDF", type="pdf")
    if not uploaded:
        st.stop()


    #mode = st.radio("Select Mode", ["📖 Reading", "🧠 Testing"], horizontal=True)
    mode = st.radio("⚡ Choose Your Cyber Mode", ["🧬 Neural Read", "🎯 Quiz Attack"], horizontal=True)

    # =======================================================
    # 📖  READING MODE
    # =======================================================
    if mode.startswith("🧬"):
        col1, col2 = st.columns([3, 2])

        with col1:
            st.subheader("PDF")
            display_pdf(uploaded)

        with col2:
            st.subheader("AI Tutor")

            # Initialize chatbot once
            if "chatbot_chain" not in st.session_state or st.session_state.chatbot_chain is None:
                try:
                    #st.info("Initializing chatbot…")
                    text = extract_text_from_pdf(uploaded)
                    docs = load_and_chunk_text(text)
                    chain = create_chatbot_chain(docs)

                    if chain is not None:
                        st.session_state.chatbot_chain = chain
                        st.session_state.chat_history = []
                        #st.success("✅ Chatbot initialized successfully.")
                    else:
                        st.session_state.chatbot_chain = None
                        st.error("❌ Failed to create chatbot chain.")

                except Exception as e:
                    st.session_state.chatbot_chain = None
                    st.error(f"❌ Error during chatbot setup: {e}")

            # Show chat history
            if "chat_history" in st.session_state:
                for i, (q, a) in enumerate(st.session_state.chat_history, 1):
                    with st.expander(f"Q{i}: {q[:50]}"):
                        st.markdown(f"**You:** {q}")
                        st.markdown(f"**AI:**  {a}")

            # Ask a new question
            with st.form("chat"):
                user_q = st.text_input("Ask a question")
                sent   = st.form_submit_button("Ask AI Tutor")

            if sent and user_q.strip():
                if st.session_state.chatbot_chain:
                    try:
                        out = st.session_state.chatbot_chain({"question": user_q})
                        answer = out["answer"]
                        st.session_state.chat_history.append((user_q, answer))
                        st.markdown(f"**AI Tutor:** {answer}")
                    except Exception as e:
                        st.error(f"❌ Error while chatting: {e}")
                else:
                    st.error("❌ Chatbot is not initialized.")

    # =======================================================
    # 🧠  TESTING MODE
    # =======================================================
    else:
        st.header("Testing Mode")
        n_qs = st.slider("Questions", 5, 20, 10)
        diff = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])

        if st.button("Generate Quiz"):
            with st.spinner("Generating…"):
                try:
                    quiz = generate_quiz(extract_text_from_pdf(uploaded), n_qs, diff)
                    if quiz.get("questions"):
                        st.session_state.quiz_data = quiz
                        st.session_state.quiz_generated = True
                    else:
                        st.session_state.quiz_generated = False
                        st.error("❌ No questions generated.")
                except Exception as e:
                    st.session_state.quiz_generated = False
                    st.error(f"❌ Error generating quiz: {e}")

        if st.session_state.get("quiz_generated"):
            display_quiz_interface(st.session_state.quiz_data)


# ── App Entry Point ───────────────────────────────────────────────
if __name__ == "__main__":
    main()
