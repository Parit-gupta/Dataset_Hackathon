"""
Teacher Dashboard - Create and Manage Assessments
Includes:
- Word Pronunciation
- Image Description
- Fill in the Blank
- Student Performance Analytics
"""

import streamlit as st
from datetime import datetime

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

# ================= RESULTS STORAGE =================
from ai_app.utils.results_store import load_results
# ===================================================


# ===================================================
# MAIN DASHBOARD
# ===================================================

def render_teacher_dashboard():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 👨‍🏫 TEACHER DASHBOARD")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs([
        "📝 Create Assessment",
        "📋 My Assessments",
        "📊 Statistics"
    ])

    with tab1:
        render_create_assessment()

    with tab2:
        render_assessment_list()

    with tab3:
        render_teacher_stats()

    st.markdown('</div>', unsafe_allow_html=True)


# ===================================================
# CREATE ASSESSMENT
# ===================================================

def render_create_assessment():
    st.markdown("### 🎯 Create New Assessment")

    assessment_type = st.selectbox(
        "Assessment Type",
        [
            ASSESSMENT_TYPE_WORD_PRONUNCIATION,
            ASSESSMENT_TYPE_IMAGE,
            ASSESSMENT_TYPE_FILLBLANK
        ],
        format_func=lambda x: {
            ASSESSMENT_TYPE_WORD_PRONUNCIATION: "🗣️ Word Pronunciation",
            ASSESSMENT_TYPE_IMAGE: "🖼️ Image Description",
            ASSESSMENT_TYPE_FILLBLANK: "✍️ Fill in the Blank"
        }[x]
    )

    st.markdown("---")

    if assessment_type == ASSESSMENT_TYPE_WORD_PRONUNCIATION:
        render_word_pronunciation_form()
    elif assessment_type == ASSESSMENT_TYPE_IMAGE:
        render_image_assessment_form()
    elif assessment_type == ASSESSMENT_TYPE_FILLBLANK:
        render_fillblank_form()


# ===================================================
# WORD PRONUNCIATION FORM
# ===================================================

def render_word_pronunciation_form():
    st.markdown("### 🗣️ Word Pronunciation Assessment")

    with st.form("word_pronunciation_form"):
        topic = st.text_input("Topic / Title *")
        difficulty = st.select_slider("Difficulty", ["Easy", "Medium", "Hard"], value="Medium")
        language = st.selectbox("Language", ["English", "Tamil", "Hindi", "Spanish", "French", "German"])

        num_words = st.number_input("Number of words", 1, 20, 5)

        words = []
        for i in range(num_words):
            st.markdown(f"#### Word {i+1}")
            word = st.text_input(f"Word {i+1}", key=f"wp_word_{i}")
            example = st.text_input(f"Example {i+1}", key=f"wp_ex_{i}")
            phonetic = st.text_input(f"Phonetic {i+1}", key=f"wp_ph_{i}")

            if word:
                words.append({
                    "word": word.strip(),
                    "example": example.strip(),
                    "phonetic": phonetic.strip()
                })

        submitted = st.form_submit_button("Create Assessment 🚀")

        if submitted:
            if not topic or not words:
                st.error("Please enter topic and at least one word")
                return

            assessment = {
                "id": generate_assessment_id(),
                "type": ASSESSMENT_TYPE_WORD_PRONUNCIATION,
                "topic": topic,
                "difficulty": difficulty,
                "language": language,
                "words": words,
                "total_words": len(words),
                "created_by": st.session_state.username,
                "created_at": datetime.now().isoformat()
            }

            data = load_assessments()
            data["assessments"].append(assessment)
            save_assessments(data)

            st.success("✅ Assessment Created")
            st.rerun()


# ===================================================
# IMAGE ASSESSMENT FORM
# ===================================================

def render_image_assessment_form():
    st.markdown("### 🖼️ Image Description Assessment")

    with st.form("image_form"):
        topic = st.text_input("Topic / Title *")
        difficulty = st.select_slider("Difficulty", ["Easy", "Medium", "Hard"], value="Medium")
        image_url = st.text_input("Image URL *")
        prompt = st.text_area("Prompt *")

        if image_url:
            st.image(image_url, use_column_width=True)

        submitted = st.form_submit_button("Create Assessment 🚀")

        if submitted:
            if not topic or not image_url or not prompt:
                st.error("Fill all fields")
                return

            assessment = {
                "id": generate_assessment_id(),
                "type": ASSESSMENT_TYPE_IMAGE,
                "topic": topic,
                "difficulty": difficulty,
                "image_url": image_url,
                "prompt": prompt,
                "created_by": st.session_state.username,
                "created_at": datetime.now().isoformat()
            }

            data = load_assessments()
            data["assessments"].append(assessment)
            save_assessments(data)

            st.success("✅ Assessment Created")
            st.rerun()


# ===================================================
# FILL IN THE BLANK FORM
# ===================================================

def render_fillblank_form():
    st.markdown("### ✍️ Fill in the Blank Assessment")

    with st.form("fillblank_form"):
        topic = st.text_input("Topic / Title *")
        difficulty = st.select_slider("Difficulty", ["Easy", "Medium", "Hard"], value="Medium")
        num = st.number_input("Number of Sentences", 1, 15, 5)

        sentences = []
        for i in range(num):
            sentence = st.text_input(f"Sentence {i+1}", key=f"fb_s_{i}")
            blank = st.text_input(f"Missing Word {i+1}", key=f"fb_b_{i}")

            if sentence and blank and "_____" in sentence:
                sentences.append({
                    "text": sentence.strip(),
                    "blank": blank.strip().lower()
                })

        submitted = st.form_submit_button("Create Assessment 🚀")

        if submitted:
            if not topic or not sentences:
                st.error("Add valid sentences with _____")
                return

            assessment = {
                "id": generate_assessment_id(),
                "type": ASSESSMENT_TYPE_FILLBLANK,
                "topic": topic,
                "difficulty": difficulty,
                "sentences": sentences,
                "total_sentences": len(sentences),
                "created_by": st.session_state.username,
                "created_at": datetime.now().isoformat()
            }

            data = load_assessments()
            data["assessments"].append(assessment)
            save_assessments(data)

            st.success("✅ Assessment Created")
            st.rerun()


# ===================================================
# MY ASSESSMENTS
# ===================================================

def render_assessment_list():
    st.markdown("### 📚 Your Assessments")

    data = load_assessments()
    assessments = [
        a for a in data.get("assessments", [])
        if a.get("created_by") == st.session_state.username
    ]

    if not assessments:
        st.info("No assessments created yet")
        return

    for a in assessments:
        st.markdown(
            f"**📘 {a['topic']}** | {a['difficulty']} | {a['type']}"
        )


# ===================================================
# 📊 ANALYTICS & STUDENT PERFORMANCE
# ===================================================

def render_teacher_stats():
    st.markdown("### 📊 Student Performance Analytics")

    assessments = load_assessments().get("assessments", [])
    results = load_results().get("submissions", [])

    my_assessments = [
        a for a in assessments
        if a.get("created_by") == st.session_state.username
    ]

    if not my_assessments:
        st.info("No assessments created yet")
        return

    assessment_map = {a["id"]: a["topic"] for a in my_assessments}
    my_results = [r for r in results if r["assessment_id"] in assessment_map]

    col1, col2, col3 = st.columns(3)
    col1.metric("Assessments", len(my_assessments))
    col2.metric("Attempts", len(my_results))

    avg = round(
        sum(r["score"] for r in my_results) / len(my_results), 2
    ) if my_results else 0

    col3.metric("Avg Score", f"{avg}%")

    if not my_results:
        st.info("No student attempts yet")
        return

    st.markdown("### 📊 Average Score Per Assessment")

    score_map = {}
    for r in my_results:
        score_map.setdefault(r["assessment_id"], []).append(r["score"])

    chart_data = {
        assessment_map[k]: round(sum(v) / len(v), 2)
        for k, v in score_map.items()
    }

    st.bar_chart(chart_data)

    st.markdown("### 📋 Student Answers")

    for aid, title in assessment_map.items():
        attempts = [r for r in my_results if r["assessment_id"] == aid]
        if not attempts:
            continue

        with st.expander(f"{title} ({len(attempts)} attempts)"):
            for r in attempts:
                st.markdown(
                    f"**👤 {r['student']} | Score: {r['score']}% | Accuracy: {r['accuracy']}%**"
                )
                for resp in r.get("responses", []):
                    if "word" in resp:
                        st.markdown(
                            f"- 🗣️ {resp['word']} → {resp.get('transcription')} ({resp.get('score')}%)"
                        )
                    elif "sentence" in resp:
                        st.markdown(
                            f"- ✍️ {resp['sentence']} → {resp.get('transcription')} ({resp.get('score')}%)"
                        )
                st.markdown("---")
