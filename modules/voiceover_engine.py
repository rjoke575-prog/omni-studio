import re
import streamlit as st
from core.llm_client import call_groq

def render():
    st.header("🎙️ Voiceover & TTS Export Engine")
    st.write("Transform your script into emotion-tagged audio ready for free TTS engines.")

    script_input = st.text_area(
        "📋 Paste your script here:",
        key="voiceover_script_input",
        value=st.session_state.get("current_script", ""),
        height=200,
        placeholder="Paste your script from Tab 2..."
    )

    col1, col2 = st.columns(2)
    with col1:
        voice_tone = st.selectbox(
            "🎭 Voice Tone:",
            key="voice_tone_select",
            options=[
                "Deep & Dramatic",
                "Calm & Authoritative",
                "Mysterious & Whispery",
                "Energetic & Exciting",
                "Sad & Reflective"
            ]
        )
    with col2:
        engine = st.selectbox(
            "🔧 Target TTS Engine:",
            key="engine_select",
            options=[
                "Chatterbox TTS (Best Quality)",
                "Kokoro HuggingFace (Browser)",
                "TextaVoice.com (Easy)"
            ]
        )

    st.divider()

    if st.button("🎙️ Generate TTS-Ready Script", key="tts_generate_btn"):
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

                else:
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

                # Clean version — strips all tags for direct TTS pasting
                clean_result = re.sub(r'\[EMOTION:[^\]]*\]', '', result)
                clean_result = re.sub(r'\[PACE:[^\]]*\]', '', clean_result)
                clean_result = re.sub(r'\[PAUSE:[^\]]*\]', '', clean_result)
                clean_result = re.sub(r'\[PAUSE:[^\]]*\]', '', clean_result)
                clean_result = re.sub(r'\[B-ROLL CUE:[^\]]*\]', '', clean_result)
                clean_result = re.sub(r'\[DRAMATIC PAUSE\]', '', clean_result)
                clean_result = re.sub(r'\[SLOW DOWN\]', '', clean_result)
                clean_result = re.sub(r'\*\*(.*?)\*\*', r'\1', clean_result)
                clean_result = re.sub(r'\n\s*\n', '\n\n', clean_result).strip()

            st.success("✅ TTS Script Ready!")

            # Engine-specific instructions
            if "Chatterbox" in engine:
                st.info("""
                **How to use with Chatterbox TTS:**
                1. Go to → huggingface.co/spaces/ResembleAI/Chatterbox
                2. Paste the CLEAN VERSION below into the text box
                3. Set emotion_intensity based on recommendation above
                4. Click Generate → Download MP3
                """)
            elif "Kokoro" in engine:
                st.info("""
                **How to use with Kokoro HuggingFace:**
                1. Go to → huggingface.co/spaces/Remsky/Kokoro-TTS-Zero
                2. Paste each chunk from the CLEAN VERSION below
                3. Select voice style → Generate → Download
                4. Stitch audio files in any free editor
                """)
            else:
                st.info("""
                **How to use with TextaVoice.com:**
                1. Go to → textavoice.com
                2. Paste each chunk from the CLEAN VERSION below
                3. Set recommended settings → Generate → Download
                4. Stitch audio files together
                """)

            st.markdown("### 🎬 Director's Copy — Your Reference")
            st.markdown(result)

            st.divider()

            st.markdown("### 🎙️ Clean Audio Copy — Paste Into TTS")
            st.text_area(
                "Copy this and paste directly into your TTS engine — no tags, pure narration:",
                key="clean_tts_output",
                value=clean_result,
                height=300,
            )

            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="📥 Download Director's Copy",
                    key="director_download_btn",
                    data=result,
                    file_name="omni_studio_director_copy.txt",
                    mime="text/plain"
                )
            with col2:
                st.download_button(
                    label="📥 Download Clean Audio Copy",
                    key="clean_download_btn",
                    data=clean_result,
                    file_name="omni_studio_clean_audio.txt",
                    mime="text/plain"
                )

    st.divider()
    st.caption("🔧 More TTS engines coming soon — modular system makes adding them instant.")
