import streamlit as st
from core.llm_client import call_groq

def render():
    st.header("🎙️ Voiceover & TTS Export Engine")
    st.write("Transform your script into emotion-tagged audio ready for free TTS engines.")

    script_input = st.text_area(
        "📋 Paste your script here:",
        value=st.session_state.get("current_script", ""),
        height=200,
        placeholder="Paste your script from Tab 2..."
    )

    col1, col2 = st.columns(2)
    with col1:
        voice_tone = st.selectbox("🎭 Voice Tone:", [
            "Deep & Dramatic",
            "Calm & Authoritative",
            "Mysterious & Whispery",
            "Energetic & Exciting",
            "Sad & Reflective"
        ])
    with col2:
        engine = st.selectbox("🔧 Target TTS Engine:", [
            "Chatterbox TTS (Best Quality)",
            "Kokoro HuggingFace (Browser)",
            "TextaVoice.com (Easy)"
        ])

    st.divider()

    if st.button("🎙️ Generate TTS-Ready Script"):
        if script_input.strip() == "":
            st.warning("Please paste your script first!")
        else:
            with st.spinner("Preparing your TTS export..."):

                if "Chatterbox" in engine:
                    system = """You are a TTS direction expert for Chatterbox TTS.
                    Chatterbox uses emotion_intensity from 0.0 to 2.0:
                    0.0-0.5 = calm/neutral, 0.6-1.0 = natural, 1.1-1.5 = expressive, 1.6-2.0 = dramatic.
                    Format the script with [EMOTION: X.X] tags before each section.
                    Also add [PACE: slow/medium/fast] and [PAUSE: Xs] markers."""

                    prompt = f"""
                    Take this script and reformat it for Chatterbox TTS narration.
                    Voice tone requested: {voice_tone}
                    
                    SCRIPT:
                    {script_input}
                    
                    Add Chatterbox-style tags:
                    - [EMOTION: 0.0-2.0] before dramatic shifts
                    - [PAUSE: 1s] or [PAUSE: 2s] for dramatic effect
                    - [PACE: slow/medium/fast] for pacing changes
                    - Bold the emphasis words
                    
                    Return the fully tagged script ready to paste into Chatterbox.
                    Also provide recommended global emotion_intensity setting at the top.
                    """

                elif "Kokoro" in engine:
                    system = """You are a TTS direction expert for Kokoro TTS on HuggingFace.
                    Kokoro works best with clean, well-punctuated text.
                    Use punctuation strategically: commas for short pauses, periods for full stops,
                    ellipsis (...) for dramatic pauses, em dashes (—) for sudden breaks."""

                    prompt = f"""
                    Take this script and reformat it for Kokoro TTS narration.
                    Voice tone requested: {voice_tone}
                    
                    SCRIPT:
                    {script_input}
                    
                    Optimize for Kokoro by:
                    - Using ... for dramatic pauses
                    - Using — for sudden breaks
                    - Breaking long sentences into shorter punchy ones
                    - Capitalizing words that need EMPHASIS
                    - Adding line breaks between scenes
                    
                    Also split into chunks of max 500 words each,
                    clearly labeled CHUNK 1, CHUNK 2 etc for easy pasting.
                    """

                else:  # TextaVoice
                    system = """You are a TTS direction expert for TextaVoice.com.
                    TextaVoice has a 2000 character limit per conversion.
                    Split text at natural sentence boundaries."""

                    prompt = f"""
                    Take this script and prepare it for TextaVoice.com.
                    Voice tone requested: {voice_tone}
                    
                    SCRIPT:
                    {script_input}
                    
                    Do the following:
                    - Split into chunks of maximum 1800 characters each
                    - Split only at sentence endings (never mid-sentence)
                    - Label each chunk: CHUNK 1 (1800 chars), CHUNK 2 etc
                    - Add a character count estimate for each chunk
                    - Mark [DRAMATIC PAUSE] and [SLOW DOWN] directions
                    - At the end, provide TextaVoice settings:
                      Speed, Pitch, and Emotion recommendations
                    """

                result = call_groq(prompt, system)
                st.session_state.current_tts = result

            st.success("✅ TTS Script Ready!")

            # Show engine-specific instructions
            if "Chatterbox" in engine:
                st.info("""
                **How to use with Chatterbox TTS:**
                1. Go to → huggingface.co/spaces/ResembleAI/Chatterbox
                2. Paste your tagged script
                3. Set emotion_intensity based on recommendation above
                4. Click Generate → Download MP3
                """)
            elif "Kokoro" in engine:
                st.info("""
                **How to use with Kokoro HuggingFace:**
                1. Go to → huggingface.co/spaces/Remsky/Kokoro-TTS-Zero
                2. Paste each chunk one at a time
                3. Select voice style → Generate → Download
                4. Stitch audio files in any free editor
                """)
            else:
                st.info("""
                **How to use with TextaVoice.com:**
                1. Go to → textavoice.com
                2. Paste CHUNK 1 → set recommended settings → Generate → Download
                3. Repeat for each chunk
                4. Stitch audio files together
                """)

            st.markdown(result)

            st.download_button(
                label="📥 Download TTS Script",
                data=result,
                file_name="omni_studio_tts_export.txt",
                mime="text/plain"
            )

    st.divider()
    st.caption("🔧 More TTS engines coming soon — modular system makes adding them instant.")
