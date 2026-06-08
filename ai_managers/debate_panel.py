import streamlit as st
from core.llm_client import call_groq

def render():
    st.header("🎬 AI Manager Debate Panel")
    st.write("Three AI personas will analyze and debate your script.")

    script_input = st.text_area(
        "📋 Paste your script or concept for review:",
        value=st.session_state.get("current_script", ""),
        height=150,
        placeholder="Paste your script here for the managers to debate..."
    )

    if st.button("🎬 Start Manager Debate"):
        if script_input.strip() == "":
            st.warning("Please paste a script first!")
        else:
            col1, col2, col3 = st.columns(3)

            with col1:
                with st.spinner("The Director is reviewing..."):
                    director_result = call_groq(
                        f"Review this script:\n{script_input}",
                        "You are The Director. You evaluate the big picture, story arc, pacing, and overall vision. You make final creative approvals. Be critical but constructive. Format your response with clear points."
                    )
                st.markdown("### 🎬 The Director")
                st.info(director_result)

            with col2:
                with st.spinner("The Creative Realist is reviewing..."):
                    creative_result = call_groq(
                        f"Review this script:\n{script_input}",
                        "You are The Creative Realist. You focus on viewer engagement, hooks, emotional impact, and narrative quality. You represent the audience's perspective. Be specific about what works and what doesn't."
                    )
                st.markdown("### 🎭 The Creative Realist")
                st.success(creative_result)

            with col3:
                with st.spinner("The Technical Critic is reviewing..."):
                    technical_result = call_groq(
                        f"Review this script:\n{script_input}",
                        "You are The Technical Critic. You evaluate visual consistency, audio sync cues, production feasibility, and point out specific technical problems. Be precise and list exactly what needs fixing."
                    )
                st.markdown("### 🔧 The Technical Critic")
                st.warning(technical_result)

            st.divider()
            st.markdown("### 📊 Insights & Adjustments Overview")
            with st.spinner("Compiling final insights..."):
                summary_result = call_groq(
                    f"""
                    Three managers reviewed this script: {script_input}
                    
                    Director said: {director_result}
                    Creative Realist said: {creative_result}
                    Technical Critic said: {technical_result}
                    
                    Compile a final actionable overview with:
                    1. REMOVE — what to cut
                    2. FIX — what needs improvement
                    3. KEEP — what is working well
                    4. PRIORITY ACTION — the single most important change
                    """,
                    "You are a senior production supervisor who synthesizes feedback from multiple creative directors into clear, actionable instructions."
                )
            st.markdown(summary_result)

            st.download_button(
                label="📥 Download Debate Report",
                data=f"DIRECTOR:\n{director_result}\n\nCREATIVE REALIST:\n{creative_result}\n\nTECHNICAL CRITIC:\n{technical_result}\n\nOVERVIEW:\n{summary_result}",
                file_name="omni_studio_debate.txt",
                mime="text/plain"
            )
