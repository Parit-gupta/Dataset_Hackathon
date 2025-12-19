"""
Teacher Dashboard
- Create & Manage Assessments
- JSON / Manual Assessments
- Student Performance Analytics
- XAI System Explanation
- RAG Therapy Guidance
"""

import streamlit as st
from datetime import datetime
import json
import os

from utils import (
    load_assessments,
    save_assessments,
    navigate_to,
    generate_assessment_id
)

from config import (
    ASSESSMENT_TYPE_WORD_PRONUNCIATION,
    ASSESSMENT_TYPE_IMAGE,
    ASSESSMENT_TYPE_FILLBLANK
)

# ================= RESULTS =================
from ai_app.utils.results_store import load_results

# ================= RAG =====================
from ai_app.rag.chatbot import rag_chatbot

# ================= XAI =====================
from ai_app.rag.explanation import generate_explanation

# ================= PATH ====================
JSON_ASSESS_PATH = "data/assessment.json"


# ======================================================
# MAIN DASHBOARD
# ======================================================
def render_teacher_dashboard():
    st.markdown("## 👨‍🏫 Teacher Dashboard")

    tab1, tab2, tab3 = st.tabs([
        "📝 Create Assessment",
        "📋 My Assessments",
        "📊 Analytics"
    ])

    with tab1:
        render_create_assessment()

    with tab2:
        render_assessment_list()

    with tab3:
        render_teacher_analytics()


# ======================================================
# CREATE ASSESSMENT
# ======================================================
def render_create_assessment():
    st.markdown("### 🎯 Create Assessment")

    source = st.radio(
        "Assessment Source",
        ["Create Manually", "Use assessment.json"],
        horizontal=True
    )

    if source == "Use assessment.json":
        load_from_json()
        return

    assessment_type = st.selectbox(
        "Assessment Type",
        [
            ASSESSMENT_TYPE_WORD_PRONUNCIATION,
            ASSESSMENT_TYPE_IMAGE,
            ASSESSMENT_TYPE_FILLBLANK
        ]
    )

    if assessment_type == ASSESSMENT_TYPE_WORD_PRONUNCIATION:
        render_word_pronunciation_form()
    elif assessment_type == ASSESSMENT_TYPE_IMAGE:
        render_image_assessment_form()
    elif assessment_type == ASSESSMENT_TYPE_FILLBLANK:
        render_fillblank_form()


# ======================================================
# JSON ASSESSMENT IMPORT
# ======================================================
def load_from_json():
    if not os.path.exists(JSON_ASSESS_PATH):
        st.error("assessment.json not found")
        return

    with open(JSON_ASSESS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    tests = data.get("tests", [])

    for t in tests:
        st.markdown(f"### 📘 {t['title']} ({t['language']})")

        if st.button("Import", key=t["test_id"]):
            assessment = {
                "id": t["test_id"],
                "topic": t["title"],
                "type": ASSESSMENT_TYPE_WORD_PRONUNCIATION,
                "language": t["language"],
                "questions": t["questions"],
                "created_by": st.session_state.username,
                "created_at": datetime.now().isoformat(),
                "source": "json"
            }

            data = load_assessments()
            data["assessments"].append(assessment)
            save_assessments(data)

            st.success("Assessment imported successfully")
            st.rerun()


# ======================================================
# WORD PRONUNCIATION FORM
# ======================================================
def render_word_pronunciation_form():
    with st.form("word_form"):
        topic = st.text_input("Topic")
        difficulty = st.select_slider("Difficulty", ["Easy", "Medium", "Hard"])
        language = st.selectbox("Language", ["English", "Hindi", "Tamil"])

        num = st.number_input("Number of Words", 1, 20, 5)
        words = []

        for i in range(num):
            w = st.text_input(f"Word {i+1}")
            ex = st.text_input(f"Example {i+1}")
            ph = st.text_input(f"Phonetic {i+1}")

            if w:
                words.append({
                    "word": w,
                    "example": ex,
                    "phonetic": ph
                })

        if st.form_submit_button("Create"):
            assessment = {
                "id": generate_assessment_id(),
                "topic": topic,
                "difficulty": difficulty,
                "language": language,
                "type": ASSESSMENT_TYPE_WORD_PRONUNCIATION,
                "words": words,
                "created_by": st.session_state.username,
                "created_at": datetime.now().isoformat()
            }

            data = load_assessments()
            data["assessments"].append(assessment)
            save_assessments(data)

            st.success("Assessment created")
            st.rerun()


# ======================================================
# IMAGE FORM
# ======================================================
def render_image_assessment_form():
    with st.form("image_form"):
        topic = st.text_input("Topic")
        difficulty = st.select_slider("Difficulty", ["Easy", "Medium", "Hard"])
        image_url = st.text_input("Image URL")
        prompt = st.text_area("Prompt")

        if st.form_submit_button("Create"):
            assessment = {
                "id": generate_assessment_id(),
                "topic": topic,
                "difficulty": difficulty,
                "type": ASSESSMENT_TYPE_IMAGE,
                "image_url": image_url,
                "prompt": prompt,
                "created_by": st.session_state.username,
                "created_at": datetime.now().isoformat()
            }

            data = load_assessments()
            data["assessments"].append(assessment)
            save_assessments(data)

            st.success("Assessment created")
            st.rerun()


# ======================================================
# FILL BLANK FORM
# ======================================================
def render_fillblank_form():
    with st.form("fillblank_form"):
        topic = st.text_input("Topic")
        difficulty = st.select_slider("Difficulty", ["Easy", "Medium", "Hard"])
        num = st.number_input("Sentences", 1, 10, 3)

        sentences = []
        for i in range(num):
            s = st.text_input(f"Sentence {i+1}")
            b = st.text_input(f"Blank {i+1}")
            if "_____" in s:
                sentences.append({"text": s, "blank": b})

        if st.form_submit_button("Create"):
            assessment = {
                "id": generate_assessment_id(),
                "topic": topic,
                "difficulty": difficulty,
                "type": ASSESSMENT_TYPE_FILLBLANK,
                "sentences": sentences,
                "created_by": st.session_state.username,
                "created_at": datetime.now().isoformat()
            }

            data = load_assessments()
            data["assessments"].append(assessment)
            save_assessments(data)

            st.success("Assessment created")
            st.rerun()


# ======================================================
# MY ASSESSMENTS
# ======================================================
def render_assessment_list():
    data = load_assessments().get("assessments", [])
    mine = [a for a in data if a["created_by"] == st.session_state.username]

    for a in mine:
        st.markdown(f"### 📘 {a['topic']}")
        st.caption(a["type"])

        if st.button("Delete", key=f"del_{a['id']}"):
            d = load_assessments()
            d["assessments"] = [x for x in d["assessments"] if x["id"] != a["id"]]
            save_assessments(d)
            st.success("Deleted")
            st.rerun()


# ======================================================
# ANALYTICS + XAI + RAG
# ======================================================
def render_teacher_analytics():
    st.markdown("### 📊 Student Performance")

    results = load_results().get("submissions", [])
    if not results:
        st.info("No student attempts yet")
        return

    # -------- BAR CHART --------
    scores = {}
    for r in results:
        scores.setdefault(r["assessment_topic"], []).append(r["score"])

    avg_scores = {k: sum(v) / len(v) for k, v in scores.items()}
    st.bar_chart(avg_scores)

    # -------- STUDENT DETAILS --------
    for r in results:
        with st.expander(f"👤 {r['student']} — {r['assessment_topic']} ({r['score']}%)"):

            for resp in r.get("responses", []):
                st.markdown(f"### 🗣️ Word: **{resp.get('word','')}**")
                st.write(f"**Student said:** {resp.get('transcription')}")
                st.write(f"**Score:** {resp.get('score')}%")

                # 🧠 SYSTEM EXPLANATION
                explanation = generate_explanation(
                    expected_text=resp.get("word", ""),
                    spoken_text=resp.get("transcription", ""),
                    word_score=resp.get("score", 0),
                    missing_words=resp.get("missing_words", []),
                    extra_words=resp.get("extra_words", []),
                    phoneme_score=resp.get("phoneme_score")
                )

                st.markdown("### 🧠 System Explanation")
                st.info(explanation)
                st.markdown("---")

            # 🤖 RAG THERAPY GUIDANCE
            rag = rag_chatbot("therapy guidance", r)
            st.markdown("### 🤖 Therapy Guidance")
            st.write(rag)
