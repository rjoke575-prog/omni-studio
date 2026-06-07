import streamlit as st
from core.session_state import init_session
from modules import idea_concept, script_generator, voiceover_engine, visual_prompts, bgm_selector
from ai_managers import debate_panel

st.set_page_config(page_title="Omni Studio", page_icon="🎬", layout="wide")
init_session()

st.title("🎬 Omni Studio")
st.caption("All-in-One AI Storytelling Studio")
st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💡 Idea & Concept",
    "📝 Script Generator",
    "🎙️ Voiceover Engine",
    "🎨 Visual Prompts",
    "🎵 BGM & Assets"
])

with tab1:
    idea_concept.render()
with tab2:
    script_generator.render()
with tab3:
    voiceover_engine.render()
with tab4:
    visual_prompts.render()
with tab5:
    bgm_selector.render()

st.divider()
debate_panel.render()
