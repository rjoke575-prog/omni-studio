import streamlit as st

def init_session():
    if "current_idea" not in st.session_state:
        st.session_state.current_idea = ""
    if "current_script" not in st.session_state:
        st.session_state.current_script = ""
