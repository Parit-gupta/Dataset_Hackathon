import streamlit as st
import os
from ai_app.asr import transcribe_audio  # Whisper ASR function

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Voice Flashcards",
    layout="centered"
)

# =====================================================
# CSS (Boom Card Style)
# =====================================================
st.markdown(
    """
    <style>
    .boom-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 30px;
        border-radius: 18px;
        color: white;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        box-shadow: 0 12px 30px rgba(0,0,0,0.3);
        margin-bottom: 25px;
        transition: transform 0.25s ease;
    }
    .boom-card:hover {
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# FLASHCARDS DATA
# =====================================================
flashcards = [
    {"prompt": "🐶 Dog", "answer": "dog"},
    {"prompt": "🍎 Apple", "answer": "apple"},
    {"prompt": "🚗 Car", "answer": "car"},
    {"prompt": "🐱 Cat", "answer": "cat"},
]

# =====================================================
# SESSION STATE
# =====================================================
if "index" not in st.session_state:
    st.session_state.index = 0

# =====================================================
# FINISHED STATE
# =====================================================
if st.session_state.index >= len(flashcards):
    st.success("🎉 All flashcards completed!")
    st.balloons()
    st.stop()

# =====================================================
# CURRENT CARD
# =====================================================
card = flashcards[st.session_state.index]

st.markdown(
    f"""
    <div class="boom-card">
        Say the word:<br><br>
        <h1>{card['prompt']}</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================
# LIVE MICROPHONE INPUT
# =====================================================
st.markdown("### 🎙️ Speak the answer")
audio_data = st.audio_input("Click to record")

# =====================================================
# PROCESS AUDIO
# =====================================================
if audio_data is not None:
    temp_audio = "temp_audio.wav"

    # Save mic audio
    with open(temp_audio, "wb") as f:
        f.write(audio_data.getvalue())

    with st.spinner("🧠 Listening..."):
        try:
            result = transcribe_audio(temp_audio)

            # Safe text extraction
            if isinstance(result, dict):
                text = result.get("text", "").lower()
            else:
                text = str(result).lower()

            st.info(f"📝 You said: **{text}**")

            if card["answer"] in text:
                st.success("✅ Correct! Moving to next card...")
                st.session_state.index += 1
                os.remove(temp_audio)
                st.rerun()
            else:
                st.error("❌ Not correct. Try again!")

        except Exception as e:
            st.error(f"Error processing audio: {e}")

# =====================================================
# RESET BUTTON
# =====================================================
st.markdown("---")
if st.button("🔄 Restart Flashcards"):
    st.session_state.index = 0
    st.rerun()