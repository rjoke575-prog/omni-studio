import streamlit as st
from core.llm_client import call_groq

def render():
    st.header("🎵 BGM & Asset Selector")
    st.write("Get music mood recommendations and asset suggestions for your video.")

    script_input = st.text_area(
        "📋 Paste your script or concept here:",
        value=st.session_state.get("current_script", ""),
        height=150,
        placeholder="Paste your script from Tab 2..."
    )

    col1, col2 = st.columns(2)
    with col1:
        platform = st.selectbox("🎬 Publishing Platform:", [
            "YouTube",
            "TikTok",
            "Instagram Reels",
            "Podcast"
        ])
    with col2:
        budget = st.selectbox("💰 Music Budget:", [
            "Free Only (YouTube Audio Library)",
            "Free Only (Pixabay/Freesound)",
            "Paid OK (Epidemic Sound)",
            "Paid OK (Artlist)"
        ])

    if st.button("🎵 Generate BGM & Asset Plan"):
        if script_input.strip() == "":
            st.warning("Please paste your script first!")
        else:
            with st.spinner("Building your asset plan..."):
                prompt = f"""
                Analyze this script and create a complete BGM and asset plan:
                
                SCRIPT:
                {script_input}
                
                Platform: {platform}
                Budget: {budget}
                
                Provide:
                1. OVERALL MUSIC MOOD — describe the perfect soundtrack feel
                2. SCENE-BY-SCENE BGM GUIDE — music direction for each scene
                3. SPECIFIC TRACK RECOMMENDATIONS — real searchable track names/styles from {budget}
                4. SOUND EFFECTS LIST — key sound effects needed with timing
                5. TRANSITION SOUNDS — audio bridges between scenes
                6. ROYALTY-FREE SEARCH KEYWORDS — exact terms to search on free music sites
                7. AUDIO MIXING NOTES — volume levels, fade ins/outs
                """

                system = "You are a professional YouTube audio producer and music supervisor who specializes in creating perfect soundscapes for storytelling videos."

                result = call_groq(prompt, system)

                st.success("✅ BGM & Asset Plan Ready!")
                st.markdown(result)
                st.session_state.current_bgm = result

                st.download_button(
                    label="📥 Download Asset Plan",
                    data=result,
                    file_name="omni_studio_bgm.txt",
                    mime="text/plain"
                )
