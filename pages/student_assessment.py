"""
Student Assessment Page - Taking Assessments
"""

import streamlit as st
from audio_recorder_streamlit import audio_recorder
from utils import load_assessments, navigate_to
from config import (
    ASSESSMENT_TYPE_QA,
    ASSESSMENT_TYPE_IMAGE,
    ASSESSMENT_TYPE_FILLBLANK,
    AUDIO_SAMPLE_RATE,
    AUDIO_PAUSE_THRESHOLD
)


def render_assessment_page():
    """Main assessment page for students"""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 🎤 TAKE ASSESSMENT")
    st.markdown("---")
    
    assessments_data = load_assessments()
    assessments = assessments_data.get("assessments", [])
    
    if not st.session_state.selected_assessment:
        display_assessment_list(assessments)
    else:
        render_selected_assessment(st.session_state.selected_assessment)
    
    st.markdown('</div>', unsafe_allow_html=True)


def display_assessment_list(assessments):
    """Display list of available assessments"""
    st.markdown("### 📋 Available Assessments")
    
    if not assessments:
        st.info("📭 No assessments available yet. Please check back later!")
        return
    
    type_icons = {
        ASSESSMENT_TYPE_QA: "💬",
        ASSESSMENT_TYPE_IMAGE: "🖼️",
        ASSESSMENT_TYPE_FILLBLANK: "✍️"
    }
    
    for assessment in assessments:
        st.markdown('<div class="assessment-card">', unsafe_allow_html=True)
        col1, col2 = st.columns([4, 1])
        
        with col1:
            icon = type_icons.get(assessment['type'], "📝")
            st.markdown(f"**{icon} {assessment['topic']}**")
            st.write(f"Difficulty: {assessment['difficulty']}")
            if assessment['type'] == ASSESSMENT_TYPE_QA:
                st.write(f"Questions: {len(assessment['questions'])}")
            elif assessment['type'] == ASSESSMENT_TYPE_FILLBLANK:
                st.write(f"Sentences: {len(assessment['sentences'])}")
        
        with col2:
            if st.button("Start", key=f"start_{assessment['id']}"):
                st.session_state.selected_assessment = assessment
                st.session_state.current_question_index = 0
                st.session_state.question_responses = []
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)


def render_selected_assessment(assessment):
    """Render the selected assessment based on type"""
    assessment_type = assessment['type']
    
    if assessment_type == ASSESSMENT_TYPE_QA:
        render_qa_assessment(assessment)
    elif assessment_type == ASSESSMENT_TYPE_IMAGE:
        render_image_assessment(assessment)
    elif assessment_type == ASSESSMENT_TYPE_FILLBLANK:
        render_fillblank_assessment(assessment)
    
    # Back button
    st.markdown("---")
    if st.button("← Choose Different Assessment"):
        st.session_state.selected_assessment = None
        st.session_state.current_question_index = 0
        st.session_state.question_responses = []
        st.rerun()


def render_qa_assessment(assessment):
    """Render Q&A assessment flow"""
    st.markdown(f"### 💬 {assessment['topic']}")
    st.info(f"Difficulty: **{assessment['difficulty']}**")
    
    questions = assessment['questions']
    current_q = st.session_state.current_question_index
    
    # Progress indicator
    st.markdown(
        f'<div class="progress-indicator">Question {current_q + 1} of {len(questions)}</div>', 
        unsafe_allow_html=True
    )
    st.progress((current_q) / len(questions))
    
    if current_q < len(questions):
        # Display current question
        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="question-text">❓ {questions[current_q]}</div>', 
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🎙️ Record Your Answer")
        
        # Audio recording tabs
        render_audio_input(current_q, questions[current_q], "qa")
    
    else:
        # All questions answered
        st.success("✅ All questions answered!")
        st.balloons()
        
        if st.button("Submit Assessment 🚀", type="primary"):
            with st.spinner("🔍 Analyzing your responses..."):
                st.session_state.assessment_results = {
                    "score": 85,
                    "accuracy": 90,
                    "fluency": 80,
                    "pronunciation": 85,
                    "feedback": "Great job! Your responses were clear and well-articulated.",
                    "assessment_topic": assessment['topic'],
                    "responses": st.session_state.question_responses
                }
                navigate_to("results")


def render_image_assessment(assessment):
    """Render image description assessment flow"""
    st.markdown(f"### 🖼️ {assessment['topic']}")
    st.info(f"Difficulty: **{assessment['difficulty']}**")
    
    st.markdown("---")
    st.markdown("### 📷 Describe This Image")
    
    # Display image
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image(assessment['image_url'], use_column_width=True)
    st.markdown(f"**Prompt:** {assessment['prompt']}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🎙️ Record Your Description")
    
    # Audio recording tabs
    tab1, tab2 = st.tabs(["🔴 Record Audio", "📁 Upload Audio"])
    
    with tab1:
        st.markdown('<div class="recording-option">', unsafe_allow_html=True)
        audio_bytes = audio_recorder(
            pause_threshold=AUDIO_PAUSE_THRESHOLD,
            sample_rate=AUDIO_SAMPLE_RATE,
            text="Click to record",
            recording_color="#e74c3c",
            neutral_color="#6aa84f",
            icon_name="microphone",
            icon_size="3x"
        )
        
        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")
            
            if st.button("Submit Description 🚀", type="primary"):
                with st.spinner("🔍 Analyzing your description..."):
                    st.session_state.assessment_results = {
                        "score": 88,
                        "accuracy": 92,
                        "fluency": 85,
                        "pronunciation": 87,
                        "feedback": "Excellent description! You covered all key elements of the image.",
                        "assessment_topic": assessment['topic']
                    }
                    navigate_to("results")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="recording-option">', unsafe_allow_html=True)
        audio_file = st.file_uploader(
            "Upload audio file",
            type=['wav', 'mp3', 'm4a'],
            key="image_upload"
        )
        
        if audio_file:
            st.audio(audio_file, format='audio/wav')
            
            if st.button("Submit Description 🚀", type="primary", key="submit_image_upload"):
                with st.spinner("🔍 Analyzing your description..."):
                    st.session_state.assessment_results = {
                        "score": 88,
                        "accuracy": 92,
                        "fluency": 85,
                        "pronunciation": 87,
                        "feedback": "Excellent description! You covered all key elements of the image.",
                        "assessment_topic": assessment['topic']
                    }
                    navigate_to("results")
        
        st.markdown('</div>', unsafe_allow_html=True)


def render_fillblank_assessment(assessment):
    """Render fill-in-blank assessment flow"""
    st.markdown(f"### ✍️ {assessment['topic']}")
    st.info(f"Difficulty: **{assessment['difficulty']}**")
    
    sentences = assessment['sentences']
    current_s = st.session_state.current_question_index
    
    # Progress indicator
    st.markdown(
        f'<div class="progress-indicator">Sentence {current_s + 1} of {len(sentences)}</div>', 
        unsafe_allow_html=True
    )
    st.progress((current_s) / len(sentences))
    
    if current_s < len(sentences):
        sentence = sentences[current_s]
        display_text = sentence['text'].replace("_____", '<span class="blank-space">_____</span>')
        
        st.markdown('<div class="sentence-card">', unsafe_allow_html=True)
        st.markdown(display_text, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🎙️ Speak the Missing Word")
        
        # Audio recording tabs
        render_audio_input(current_s, sentence, "fillblank")
    
    else:
        # All sentences completed
        st.success("✅ All sentences completed!")
        st.balloons()
        
        if st.button("Submit Assessment 🚀", type="primary"):
            with st.spinner("🔍 Analyzing your responses..."):
                st.session_state.assessment_results = {
                    "score": 87,
                    "accuracy": 91,
                    "fluency": 84,
                    "pronunciation": 86,
                    "feedback": "Good work! Most of your answers were correct and clearly spoken.",
                    "assessment_topic": assessment['topic'],
                    "responses": st.session_state.question_responses
                }
                navigate_to("results")


def render_audio_input(index, question_data, assessment_type):
    """Render audio input options (record or upload)"""
    tab1, tab2 = st.tabs(["🔴 Record Audio", "📁 Upload Audio"])
    
    with tab1:
        st.markdown('<div class="recording-option">', unsafe_allow_html=True)
        audio_bytes = audio_recorder(
            pause_threshold=AUDIO_PAUSE_THRESHOLD,
            sample_rate=AUDIO_SAMPLE_RATE,
            text="Click to record",
            recording_color="#e74c3c",
            neutral_color="#6aa84f",
            icon_name="microphone",
            icon_size="3x",
            key=f"recorder_{assessment_type}_{index}"
        )
        
        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")
            
            if st.button("Submit Answer ✅", type="primary", key=f"submit_record_{index}"):
                if assessment_type == "qa":
                    st.session_state.question_responses.append({
                        "question": question_data,
                        "audio": audio_bytes,
                        "type": "recorded"
                    })
                elif assessment_type == "fillblank":
                    st.session_state.question_responses.append({
                        "sentence": question_data['text'],
                        "expected": question_data['blank'],
                        "audio": audio_bytes,
                        "type": "recorded"
                    })
                st.session_state.current_question_index += 1
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="recording-option">', unsafe_allow_html=True)
        audio_file = st.file_uploader(
            "Upload audio file",
            type=['wav', 'mp3', 'm4a'],
            key=f"upload_{assessment_type}_{index}"
        )
        
        if audio_file:
            st.audio(audio_file, format='audio/wav')
            
            if st.button("Submit Answer ✅", type="primary", key=f"submit_upload_{index}"):
                if assessment_type == "qa":
                    st.session_state.question_responses.append({
                        "question": question_data,
                        "audio": audio_file,
                        "type": "uploaded"
                    })
                elif assessment_type == "fillblank":
                    st.session_state.question_responses.append({
                        "sentence": question_data['text'],
                        "expected": question_data['blank'],
                        "audio": audio_file,
                        "type": "uploaded"
                    })
                st.session_state.current_question_index += 1
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)