import streamlit as st
from core.llm_client import call_groq

def render():
    st.header("🎙️ Voiceover Prompt Engine")
    st.write("Transform your script into detailed voiceover direction cues.")

    script_input = st.text_area(
        "📋 Paste your script here:",
        value=st.session_state.get("current_script", ""),
        height=200,
        placeholder="Paste your script from Tab 2, or type directly..."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        voice_tone = st.selectbox("🎭 Voice Tone:", [
            "Deep & Dramatic",
            "Calm & Authoritative",
            "Mysterious & Whispery",
            "Energetic & Exciting",
            "Sad & Reflective"
        ])
    with col2:
        pace = st.selectbox("⏱️ Pacing:", [
            "Slow & Deliberate",
            "Medium & Steady",
            "Fast & Urgent",
            "Dynamic (varies)"
        ])
    with col3:
        audience = st.selectbox("👥 Target Audience:", [
            "General YouTube",
            "True Crime Fans",
            "History Buffs",
            "Horror Enthusiasts",
            "Motivational Seekers"
        ])

    if st.button("🎙️ Generate Voiceover Directions"):
        if script_input.strip() == "":
            st.warning("Please paste your script first!")
        else:
            with st.spinner("Creating voiceover directions..."):
                prompt = f"""
                Analyze this script and create detailed voiceover direction cues:
                
                SCRIPT:
                {script_input}
                
                Voice Tone: {voice_tone}
                Pacing: {pace}
                Target Audience: {audience}
                
                For each section of the script provide:
                1. EMOTION CUE — what emotion to convey
                2. PACE DIRECTION — speed instructions
                3. EMPHASIS WORDS — which words to stress
                4. BREATH MARKERS — where to pause and breathe
                5. VOLUME GUIDE — loud/soft/whisper instructions
                6. DELIVERY NOTE — special acting direction
                
                Format it clearly section by section.
                """

                system = "You are a professional voiceover director and audio producer who has worked on major documentary and YouTube productions."

                result = call_groq(prompt, system)

                st.success("✅ Voiceover Directions Ready!")
                st.markdown(result)
                st.session_state.current_voiceover = result

                st.download_button(
                    label="📥 Download Voiceover Guide",
                    data=result,
                    file_name="omni_studio_voiceover.txt",
                    mime="text/plain"
                )
