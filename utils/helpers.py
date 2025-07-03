# utils/helpers.py

import streamlit as st


def clear_session_state(keys):
    """
    Clear specific keys from Streamlit session state.
    """
    for key in keys:
        if key in st.session_state:
            del st.session_state[key]


def set_background_color(color: str = "#F9F9F9"):
    """
    Sets a custom background color for the Streamlit app.
    """
    st.markdown(f"""
        <style>
        .stApp {{
            background-color: {color};
        }}
        </style>
    """, unsafe_allow_html=True)


def show_logo():
    """
    Displays app logo if present in assets directory.
    """
    st.image("assets/meowtutor_logo.png", width=160)
