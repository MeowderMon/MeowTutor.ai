import streamlit as st

def setup_page_config():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="MeowTutor.ai",
        page_icon="🐱",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

def get_session_state():
    """Initialize session state variables"""
    if 'uploaded_file' not in st.session_state:
        st.session_state['uploaded_file'] = None
    
    if 'chatbot_chain' not in st.session_state:
        st.session_state['chatbot_chain'] = None
    
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    
    if 'quiz_data' not in st.session_state:
        st.session_state['quiz_data'] = None
    
    if 'quiz_generated' not in st.session_state:
        st.session_state['quiz_generated'] = False
    
    if 'quiz_answers' not in st.session_state:
        st.session_state['quiz_answers'] = {}

def reset_session_state():
    """Reset session state for new file upload"""
    keys_to_reset = [
        'chatbot_chain', 'chat_history', 'quiz_data', 
        'quiz_generated', 'quiz_answers'
    ]
    
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]
