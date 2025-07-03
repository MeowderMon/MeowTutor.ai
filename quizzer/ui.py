import streamlit as st
from quizzer.generator import generate_mcqs_from_text
from quizzer.scorer import score_quiz
from langchain_community.document_loaders import PyMuPDFLoader

def show_mcq_interface(pdf_path):
    if "quiz_questions" not in st.session_state or not st.session_state["quiz_questions"]:
        st.markdown("### 🧠 Generate a Quiz from PDF")
        num_mcqs = st.slider("Number of MCQs", min_value=5, max_value=20, value=5, step=1, key="numq_slider")
        if st.button("Generate Quiz", key="gen_quiz_btn"):
            with st.spinner("🔄 Generating questions from PDF..."):
                loader = PyMuPDFLoader(pdf_path)
                docs = loader.load()
                full_text = "\n".join([d.page_content for d in docs])
                questions = generate_mcqs_from_text(full_text, num_questions=num_mcqs)
                if not questions:
                    st.error("❌ Failed to generate any questions. Try with a different PDF or check your generator.")
                    return
                st.success(f"✅ Generated {len(questions)} MCQs.")
                st.session_state["quiz_questions"] = questions
            st.rerun()
        return

    questions = st.session_state["quiz_questions"]
    st.markdown("### 📝 Take the Quiz")
    responses = []
    for i, q in enumerate(questions):
        st.markdown(f"**Q{i+1}. {q['question']}**")
        choice = st.radio("Select an option:", q["options"], key=f"ans_{i}")
        responses.append(choice)
        st.markdown("---")

    if st.button("Submit Quiz", key="submit_quiz_btn"):
        score, results = score_quiz(responses, questions)
        st.success(f"✅ You scored {score}/{len(questions)}")
        for idx, q in enumerate(questions):
            correct = q['answer']
            user = responses[idx]
            icon = "✅" if results[idx] else "❌"
            st.markdown(f"Q{idx+1}: {icon} Correct: **{correct}**, You: {user}")
            explanation = q.get('explanation')
            st.write(f"*Explanation:* {explanation}")
            st.markdown("---")
