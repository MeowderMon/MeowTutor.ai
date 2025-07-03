import streamlit as st
from quizzer.scorer import calculate_score

def display_quiz_interface(quiz_data):
    """Display quiz interface"""
    if not quiz_data or "questions" not in quiz_data:
        st.error("Invalid quiz data")
        return
    
    questions = quiz_data["questions"]
    
    st.subheader(f"Quiz - {len(questions)} Questions")
    
    # Initialize answers in session state
    if 'quiz_answers' not in st.session_state:
        st.session_state['quiz_answers'] = {}
    
    # Display questions
    for i, question_data in enumerate(questions):
        st.markdown(f"**Question {i+1}:**")
        st.write(question_data["question"])
        
        # Display options
        options = question_data["options"]
        option_labels = list(options.keys())
        option_values = [f"{key}) {value}" for key, value in options.items()]
        
        # Radio button for answer selection
        selected_answer = st.radio(
            f"Select your answer for Question {i+1}:",
            option_labels,
            key=f"q_{i}",
            format_func=lambda x: f"{x}) {options[x]}"
        )
        
        # Store answer
        st.session_state['quiz_answers'][i] = selected_answer
        
        st.markdown("---")
    
    # Submit button
    if st.button("Submit Quiz", type="primary"):
        if len(st.session_state['quiz_answers']) == len(questions):
            display_quiz_results(quiz_data)
        else:
            st.warning("Please answer all questions before submitting!")

def display_quiz_results(quiz_data):
    """Display quiz results"""
    questions = quiz_data["questions"]
    user_answers = st.session_state['quiz_answers']
    
    # Calculate score
    score = calculate_score(quiz_data, user_answers)
    
    st.subheader("Quiz Results")
    st.metric("Score", f"{score['correct']}/{score['total']}", f"{score['percentage']:.1f}%")
    
    # Display detailed results
    st.markdown("### Detailed Results")
    
    for i, question_data in enumerate(questions):
        correct_answer = question_data["correct_answer"]
        user_answer = user_answers.get(i, "")
        is_correct = user_answer == correct_answer
        
        # Question header
        if is_correct:
            st.success(f"✅ Question {i+1} - Correct!")
        else:
            st.error(f"❌ Question {i+1} - Incorrect")
        
        # Question and answers
        st.write(f"**Question:** {question_data['question']}")
        st.write(f"**Your Answer:** {user_answer}) {question_data['options'][user_answer]}")
        
        if not is_correct:
            st.write(f"**Correct Answer:** {correct_answer}) {question_data['options'][correct_answer]}")
        
        st.write(f"**Explanation:** {question_data['explanation']}")
        st.markdown("---")
    
    # Reset quiz button
    if st.button("Take Quiz Again"):
        st.session_state['quiz_answers'] = {}
        st.rerun()
