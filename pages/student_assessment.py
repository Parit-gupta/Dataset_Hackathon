"""
Student Assessment Page
- Uses assessments.json (tests[])
- Whisper ASR
- Stores full responses
- Shows System Explanation after test
"""

import json
import os
from datetime import datetime
import streamlit as st
from audio_recorder_streamlit import audio_recorder

from utils import navigate_to
from config import AUDIO_SAMPLE_RATE, AUDIO_PAUSE_THRESHOLD

from ai_app.utils.results_store import save_result
from ai_app.rag.explanation import generate_explanation


# ================= ASR =================
try:
    import sys
    sys.path.append("ai_app/asr")
    from ai_app.asr.asr_engine import transcribe_audio
    ASR_AVAILABLE = True
except Exception:
    ASR_AVAILABLE = False
    st.warning("⚠️ Whisper ASR not available")

# ================= PATHS =================
ASSESSMENT_JSON = "ai_app/assessments/assessments.json"
AUDIO_DIR = "audio_submissions"
os.makedirs(AUDIO_DIR, exist_ok=True)


# ======================================================
# LOAD TESTS
# ======================================================
def load_tests():
    with open(ASSESSMENT_JSON, "r", encoding="utf-8") as f:
        return json.load(f)["tests"]


# ======================================================
# MAIN PAGE
# ======================================================
def render_assessment_page():
    st.markdown("## 🎤 Take Pronunciation Assessment")
    st.divider()

    st.session_state.setdefault("selected_test", None)
    st.session_state.setdefault("current_q", 0)
    st.session_state.setdefault("responses", [])

    if not st.session_state.selected_test:
        render_test_list()
    else:
        render_test_runner()


# ======================================================
# TEST LIST
# ======================================================
def render_test_list():
    tests = load_tests()

    for t in tests:
        st.markdown("### 📘 " + t["title"])
        st.caption(f"Language: {t['language']} | Questions: {len(t['questions'])}")

        if st.button("Start Test", key=t["test_id"]):
            st.session_state.selected_test = t
            st.session_state.current_q = 0
            st.session_state.responses = []
            st.rerun()

        st.divider()


# ======================================================
# TEST RUNNER
# ======================================================
def render_test_runner():
    test = st.session_state.selected_test
    questions = test["questions"]
    idx = st.session_state.current_q

    st.markdown(f"### 🧪 {test['title']}")
    st.progress(idx / len(questions))

    if idx < len(questions):
        render_word_question(questions[idx], idx, test)
    else:
        render_test_complete(test)


# ======================================================
# WORD QUESTION
# ======================================================
def render_word_question(question, idx, test):
    expected_word = question["expected_text"]

    st.markdown("### Pronounce this word:")
    st.markdown(f"## 🗣️ **{expected_word}**")

    audio = audio_recorder(
        pause_threshold=AUDIO_PAUSE_THRESHOLD,
        sample_rate=AUDIO_SAMPLE_RATE,
        key=f"rec_{idx}"
    )

    if audio and st.button("Submit Pronunciation"):
        audio_path = save_audio(audio, idx)
        result = process_asr(audio_path, expected_word, test["language"])

        if not result["success"]:
            st.error(result["error"])
            return

        # ---------- SYSTEM EXPLANATION ----------
        explanation = generate_explanation(
            expected_text=expected_word,
            spoken_text=result["text"],
            word_score=result["score"],
            missing_words=[] if expected_word in result["text"] else [expected_word],
            extra_words=[],
            phoneme_score=None
        )

        # ---------- SAVE RESPONSE (NO MASKING) ----------
        st.session_state.responses.append({
            "question_id": question["question_id"],
            "word": expected_word,
            "expected_text": expected_word,
            "spoken_text": result["text"],
            "transcription": result["text"],
            "score": result["score"],
            "accuracy": result["accuracy"],
            "explanation": explanation
        })

        st.session_state.current_q += 1
        st.rerun()


# ======================================================
# ASR + SCORING
# ======================================================
def process_asr(audio_path, expected, language):
    try:
        res = transcribe_audio(audio_path, language)
        spoken = res["text"].lower().strip()
        expected = expected.lower().strip()

        if spoken == expected:
            return success(spoken, 100)
        elif expected in spoken:
            return success(spoken, 80)
        else:
            return success(spoken, 40)

    except Exception as e:
        return {"success": False, "error": str(e)}


def success(text, score):
    return {
        "success": True,
        "text": text,
        "score": score,
        "accuracy": score
    }


# ======================================================
# AUDIO SAVE
# ======================================================
def save_audio(audio_bytes, idx):
    user = st.session_state.get("username", "student")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(AUDIO_DIR, f"{user}_q{idx}_{ts}.wav")

    with open(path, "wb") as f:
        f.write(audio_bytes)

    return path


# ======================================================
# TEST COMPLETE + EXPLANATION DISPLAY
# ======================================================
def render_test_complete(test):
    st.success("✅ Test Completed")

    scores = [r["score"] for r in st.session_state.responses]
    avg_score = round(sum(scores) / len(scores), 2)

    st.metric("Final Score", f"{avg_score}%")

    # ================= SYSTEM EXPLANATION =================
    st.markdown("## 🧠 System Explanation")

    for r in st.session_state.responses:
        st.markdown(f"### 🗣️ Word: **{r['word']}**")
        st.markdown(f"Student said: **{r['spoken_text']}**")
        st.markdown(f"Score: **{r['score']}%**")
        st.info(r["explanation"])
        st.divider()

    # ================= SAVE RESULT =================
    save_result({
        "student": st.session_state.username,
        "assessment_id": test["test_id"],
        "assessment_topic": test["title"],
        "assessment_type": "word_pronunciation",
        "language": test["language"],
        "score": avg_score,
        "accuracy": avg_score,
        "responses": st.session_state.responses,
        "submitted_at": datetime.now().isoformat()
    })

    if st.button("Back to Tests"):
        st.session_state.selected_test = None
        st.session_state.current_q = 0
        st.session_state.responses = []
        st.rerun()
