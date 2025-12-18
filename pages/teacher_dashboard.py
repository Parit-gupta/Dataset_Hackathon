"""
Teacher Dashboard Page - Assessment Management
"""

import streamlit as st
from datetime import datetime
from utils import load_assessments, save_assessments, navigate_to
from config import (
    ASSESSMENT_TYPE_QA, 
    ASSESSMENT_TYPE_IMAGE, 
    ASSESSMENT_TYPE_FILLBLANK,
    DEFAULT_QUESTIONS_COUNT,
    DEFAULT_SENTENCES_COUNT,
    DIFFICULTY_LEVELS
)


def render_teacher_dashboard():
    """Main teacher dashboard page"""
    if st.session_state.user_role != "teacher":
        st.error("⛔ Access Denied: This page is only for teachers")
        if st.button("Go Back"):
            navigate_to("home")
        return
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 👨‍🏫 ASSESSMENT MANAGEMENT")
    st.markdown("---")
    
    # Dashboard Stats
    assessments_data = load_assessments()
    assessments = assessments_data.get("assessments", [])
    teacher_assessments = [a for a in assessments if a.get('created_by') == st.session_state.user_email]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        st.metric("Total Assessments", len(teacher_assessments))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        qa_count = len([a for a in teacher_assessments if a['type'] == ASSESSMENT_TYPE_QA])
        st.metric("Q&A", qa_count)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        image_count = len([a for a in teacher_assessments if a['type'] == ASSESSMENT_TYPE_IMAGE])
        st.metric("Image", image_count)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        fillblank_count = len([a for a in teacher_assessments if a['type'] == ASSESSMENT_TYPE_FILLBLANK])
        st.metric("Fill-in-Blank", fillblank_count)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Create New Assessment Button
    if not st.session_state.new_assessment_type:
        if st.button("➕ Create New Assessment", type="primary"):
            st.session_state.new_assessment_type = "select"
            st.rerun()
    
    # CREATE NEW ASSESSMENT FLOW
    if st.session_state.new_assessment_type:
        render_create_assessment_flow(assessments, assessments_data)
    
    # DISPLAY EXISTING ASSESSMENTS
    if not st.session_state.new_assessment_type and teacher_assessments:
        st.markdown("---")
        st.markdown("### 📋 Your Assessments")
        display_teacher_assessments(teacher_assessments, assessments_data)
    
    elif not st.session_state.new_assessment_type and not teacher_assessments:
        st.info("📭 You haven't created any assessments yet. Click 'Create New Assessment' to get started!")
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_create_assessment_flow(assessments, assessments_data):
    """Render the assessment creation flow"""
    st.markdown("### ✨ Create New Assessment")
    
    if st.session_state.new_assessment_type == "select":
        st.markdown("**Select Assessment Type:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💬 Q&A Assessment", use_container_width=True):
                st.session_state.new_assessment_type = ASSESSMENT_TYPE_QA
                st.rerun()
        
        with col2:
            if st.button("🖼️ Image Description", use_container_width=True):
                st.session_state.new_assessment_type = ASSESSMENT_TYPE_IMAGE
                st.rerun()
        
        with col3:
            if st.button("✍️ Fill in the Blanks", use_container_width=True):
                st.session_state.new_assessment_type = ASSESSMENT_TYPE_FILLBLANK
                st.rerun()
        
        if st.button("Cancel"):
            st.session_state.new_assessment_type = None
            st.rerun()
    
    elif st.session_state.new_assessment_type == ASSESSMENT_TYPE_QA:
        create_qa_assessment(assessments, assessments_data)
    
    elif st.session_state.new_assessment_type == ASSESSMENT_TYPE_IMAGE:
        create_image_assessment(assessments, assessments_data)
    
    elif st.session_state.new_assessment_type == ASSESSMENT_TYPE_FILLBLANK:
        create_fillblank_assessment(assessments, assessments_data)


def create_qa_assessment(assessments, assessments_data):
    """Create Q&A assessment form"""
    with st.form("create_qa_assessment"):
        st.markdown("#### 💬 Q&A Assessment")
        
        topic = st.text_input("Assessment Topic", placeholder="e.g., General Knowledge Q&A")
        difficulty = st.selectbox("Difficulty Level", DIFFICULTY_LEVELS)
        
        st.markdown(f"**Questions (Enter {DEFAULT_QUESTIONS_COUNT} questions):**")
        questions = []
        for i in range(DEFAULT_QUESTIONS_COUNT):
            q = st.text_input(f"Question {i+1}", key=f"qa_q{i}", placeholder=f"Enter question {i+1}")
            questions.append(q)
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Create Assessment", type="primary", use_container_width=True)
        with col2:
            cancel = st.form_submit_button("Cancel", use_container_width=True)
        
        if submit:
            if topic and all(questions):
                new_assessment = {
                    "id": str(len(assessments) + 1),
                    "type": ASSESSMENT_TYPE_QA,
                    "topic": topic,
                    "difficulty": difficulty,
                    "questions": questions,
                    "created_by": st.session_state.user_email,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                assessments_data["assessments"].append(new_assessment)
                if save_assessments(assessments_data):
                    st.success("✅ Q&A Assessment created successfully!")
                    st.session_state.new_assessment_type = None
                    st.rerun()
            else:
                st.error("❌ Please fill in all fields")
        
        if cancel:
            st.session_state.new_assessment_type = None
            st.rerun()


def create_image_assessment(assessments, assessments_data):
    """Create image description assessment form"""
    with st.form("create_image_assessment"):
        st.markdown("#### 🖼️ Image Description Assessment")
        
        topic = st.text_input("Assessment Topic", placeholder="e.g., Image Description Challenge")
        difficulty = st.selectbox("Difficulty Level", DIFFICULTY_LEVELS)
        image_url = st.text_input("Image URL", placeholder="https://example.com/image.jpg")
        prompt = st.text_area("Prompt/Instructions", placeholder="Describe what you see in this image...")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Create Assessment", type="primary", use_container_width=True)
        with col2:
            cancel = st.form_submit_button("Cancel", use_container_width=True)
        
        if submit:
            if topic and image_url and prompt:
                new_assessment = {
                    "id": str(len(assessments) + 1),
                    "type": ASSESSMENT_TYPE_IMAGE,
                    "topic": topic,
                    "difficulty": difficulty,
                    "image_url": image_url,
                    "prompt": prompt,
                    "created_by": st.session_state.user_email,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                assessments_data["assessments"].append(new_assessment)
                if save_assessments(assessments_data):
                    st.success("✅ Image Assessment created successfully!")
                    st.session_state.new_assessment_type = None
                    st.rerun()
            else:
                st.error("❌ Please fill in all fields")
        
        if cancel:
            st.session_state.new_assessment_type = None
            st.rerun()


def create_fillblank_assessment(assessments, assessments_data):
    """Create fill-in-blank assessment form"""
    with st.form("create_fillblank_assessment"):
        st.markdown("#### ✍️ Fill in the Blanks Assessment")
        
        topic = st.text_input("Assessment Topic", placeholder="e.g., Vocabulary Fill-in-the-Blank")
        difficulty = st.selectbox("Difficulty Level", DIFFICULTY_LEVELS)
        
        st.markdown(f"**Sentences (Enter {DEFAULT_SENTENCES_COUNT} sentences with blanks):**")
        st.info("Use _____ (5 underscores) to mark the blank in each sentence")
        
        sentences = []
        for i in range(DEFAULT_SENTENCES_COUNT):
            col1, col2 = st.columns([3, 1])
            with col1:
                text = st.text_input(f"Sentence {i+1}", key=f"fb_s{i}", placeholder="The cat is _____ on the mat.")
            with col2:
                blank = st.text_input(f"Answer {i+1}", key=f"fb_a{i}", placeholder="sleeping")
            if text and blank:
                sentences.append({"text": text, "blank": blank})
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Create Assessment", type="primary", use_container_width=True)
        with col2:
            cancel = st.form_submit_button("Cancel", use_container_width=True)
        
        if submit:
            if topic and len(sentences) == DEFAULT_SENTENCES_COUNT:
                new_assessment = {
                    "id": str(len(assessments) + 1),
                    "type": ASSESSMENT_TYPE_FILLBLANK,
                    "topic": topic,
                    "difficulty": difficulty,
                    "sentences": sentences,
                    "created_by": st.session_state.user_email,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                assessments_data["assessments"].append(new_assessment)
                if save_assessments(assessments_data):
                    st.success("✅ Fill-in-Blank Assessment created successfully!")
                    st.session_state.new_assessment_type = None
                    st.rerun()
            else:
                st.error(f"❌ Please fill in all {DEFAULT_SENTENCES_COUNT} sentences with answers")
        
        if cancel:
            st.session_state.new_assessment_type = None
            st.rerun()


def display_teacher_assessments(teacher_assessments, assessments_data):
    """Display list of teacher's assessments"""
    for assessment in teacher_assessments:
        st.markdown('<div class="teacher-card">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            type_icons = {
                ASSESSMENT_TYPE_QA: "💬",
                ASSESSMENT_TYPE_IMAGE: "🖼️",
                ASSESSMENT_TYPE_FILLBLANK: "✍️"
            }
            icon = type_icons.get(assessment['type'], "📝")
            st.markdown(f"**{icon} {assessment['topic']}**")
            st.write(f"Type: {assessment['type'].upper()} | Difficulty: {assessment['difficulty']}")
            st.write(f"Created: {assessment.get('created_at', 'N/A')}")
        
        with col2:
            if st.button("✏️ Edit", key=f"edit_{assessment['id']}"):
                st.session_state.editing_assessment = assessment
                st.rerun()
        
        with col3:
            if st.button("🗑️ Delete", key=f"delete_{assessment['id']}"):
                assessments_data["assessments"] = [
                    a for a in assessments_data["assessments"] 
                    if a['id'] != assessment['id']
                ]
                if save_assessments(assessments_data):
                    st.success("Assessment deleted!")
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)