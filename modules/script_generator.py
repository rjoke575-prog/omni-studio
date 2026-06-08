import streamlit as st
from core.llm_client import call_groq

def render():
    st.header("📝 Script Generator")
    st.write("Generate a full YouTube script based on your concept.")

    idea_input = st.text_area(
        "📋 Paste your concept or idea here:",
        value=st.session_state.get("current_idea", ""),
        height=150,
        placeholder="Paste your idea from Tab 1, or type a new one..."
    )

    col1, col2 = st.columns(2)
    with col1:
        duration = st.selectbox("⏱️ Video Length:", [
            "3-5 minutes",
            "7-10 minutes",
            "12-15 minutes",
            "20+ minutes"
        ])
    with col2:
        style = st.selectbox("🎭 Narration Style:", [
            "Dramatic & Suspenseful",
            "Calm & Documentary",
            "Energetic & Fast-paced",
            "Dark & Mysterious"
        ])

    if st.button("📝 Generate Full Script"):
        if idea_input.strip() == "":
            st.warning("Please enter a concept first!")
        else:
            with st.spinner("Writing your script..."):
                prompt = f"""
                Based on this concept: {idea_input}
                
                Write a complete YouTube storytelling script for a {duration} video.
                Narration style: {style}
                
                Structure the script with:
                1. HOOK (first 30 seconds - must grab attention immediately)
                2. INTRO (set the scene, tease what's coming)
                3. ACT 1 (build the story)
                4. ACT 2 (deepen the mystery/conflict)
                5. ACT 3 (climax and revelation)
                6. OUTRO (call to action, subscribe prompt)
                
                Include [PAUSE] markers for dramatic effect.
                Include [B-ROLL CUE: description] for visual suggestions.
                """

                system = "You are a professional YouTube scriptwriter specializing in viral storytelling content. Write engaging, dramatic scripts that keep viewers watching."

                result = call_groq(prompt, system)

                st.success("✅ Script Ready!")
                st.markdown(result)
                st.session_state.current_script = result
                
                st.download_button(
                    label="📥 Download Script",
                    data=result,
                    file_name="omni_studio_script.txt",
                    mime="text/plain"
                )
