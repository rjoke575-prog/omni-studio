import streamlit as st
from core.llm_client import call_groq

def render():
    st.header("💡 Idea & Concept")
    st.write("Enter your topic and let the AI generate story angles for your YouTube channel.")

    topic = st.text_input("🎯 Enter your video topic:", placeholder="e.g. The mystery of the Bermuda Triangle")
    genre = st.selectbox("🎭 Select your genre:", [
        "Mystery & Conspiracy",
        "True Crime",
        "History & Mythology",
        "Science & Space",
        "Horror & Paranormal",
        "Motivational",
        "Biography"
    ])

    if st.button("🚀 Generate Concept"):
        if topic.strip() == "":
            st.warning("Please enter a topic first!")
        else:
            with st.spinner("Generating your concept..."):
                prompt = f"""
                I want to create a YouTube storytelling video about: {topic}
                Genre: {genre}
                
                Please provide:
                1. Three unique story angles I can take
                2. The best hook sentence to open the video
                3. The core emotional theme (fear, curiosity, inspiration, etc.)
                4. Suggested video title (YouTube SEO optimized)
                """
                
                system = "You are an expert YouTube storytelling strategist who specializes in viral narrative content."
                
                result = call_groq(prompt, system)
                
                st.success("✅ Concept Generated!")
                st.markdown(result)
                st.session_state.current_idea = result
