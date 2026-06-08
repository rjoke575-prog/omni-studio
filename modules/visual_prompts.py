import streamlit as st
from core.llm_client import call_groq

def render():
    st.header("🎨 Visual & Image Prompt Generator")
    st.write("Generate scene-by-scene AI image prompts for your video.")

    script_input = st.text_area(
        "📋 Paste your script here:",
        value=st.session_state.get("current_script", ""),
        height=200,
        placeholder="Paste your script from Tab 2..."
    )

    col1, col2 = st.columns(2)
    with col1:
        visual_style = st.selectbox("🎨 Visual Style:", [
            "Cinematic & Dark",
            "Realistic & Documentary",
            "Illustrated & Artistic",
            "Vintage & Retro",
            "Futuristic & Sci-Fi"
        ])
    with col2:
        image_tool = st.selectbox("🖼️ Target Image Tool:", [
            "Midjourney",
            "DALL-E",
            "Stable Diffusion",
            "Adobe Firefly",
            "Leonardo AI"
        ])

    if st.button("🎨 Generate Visual Prompts"):
        if script_input.strip() == "":
            st.warning("Please paste your script first!")
        else:
            with st.spinner("Generating visual prompts..."):
                prompt = f"""
                Analyze this script and generate detailed AI image prompts for each scene:
                
                SCRIPT:
                {script_input}
                
                Visual Style: {visual_style}
                Target Tool: {image_tool}
                
                For each major scene provide:
                1. SCENE NAME — brief title
                2. IMAGE PROMPT — detailed, optimized prompt for {image_tool}
                3. NEGATIVE PROMPT — what to exclude
                4. MOOD & LIGHTING — atmosphere description
                5. CAMERA ANGLE — suggested shot type
                
                Make prompts highly detailed and production-ready.
                """

                system = "You are a professional AI art director and visual prompt engineer who creates stunning imagery for YouTube productions."

                result = call_groq(prompt, system)

                st.success("✅ Visual Prompts Ready!")
                st.markdown(result)
                st.session_state.current_visuals = result

                st.download_button(
                    label="📥 Download Visual Prompts",
                    data=result,
                    file_name="omni_studio_visuals.txt",
                    mime="text/plain"
                )
