import os
import streamlit as st

def get_groq_client():
    api_key = st.secrets["GROQ_API_KEY"]
    return api_key
