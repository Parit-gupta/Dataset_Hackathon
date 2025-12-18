"""
Results and Other Pages (Analytics, Learn, Student Results)
"""

import streamlit as st
from utils import navigate_to


def render_student_results():
    """Render student's own results page"""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 📊 ASSESSMENT RESULTS")
    st.markdown("---")
    
    if st.session_state.assessment_results:
        results = st.session_state.assessment_results
        
        st.markdown(f"### 🎯 {results['assessment_topic']}")
        st.markdown("---")
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Overall Score", f"{results['score']}%", delta="Good")
        with col2:
            st.metric("Accuracy", f"{results['accuracy']}%")
        with col3:
            st.metric("Fluency", f"{results['fluency']}%")
        
        st.markdown("---")
        
        # Detailed Analysis
        st.markdown("### 📈 Detailed Analysis")
        st.progress(results['pronunciation'] / 100)
        st.write(f"**Pronunciation:** {results['pronunciation']}%")
        
        st.markdown("---")
        
        # Feedback
        st.markdown("### 💬 Feedback")
        if results['score'] >= 80:
            st.success(results['feedback'])
        else:
            st.warning(results['feedback'])
        
        st.markdown("---")
        
        if st.button("Take Another Assessment"):
            st.session_state.selected_assessment = None
            st.session_state.uploaded_audio = None
            st.session_state.recorded_audio = None
            st.session_state.assessment_results = None
            st.session_state.current_question_index = 0
            st.session_state.question_responses = []
            navigate_to("assessment")
    
    else:
        st.info("📭 No assessment results yet. Take an assessment first!")
        if st.button("Take Assessment Now"):
            navigate_to("assessment")
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_teacher_student_results():
    """Render teacher's view of student results"""
    if st.session_state.user_role != "teacher":
        st.error("⛔ Access Denied: This page is only for teachers")
        if st.button("Go Back"):
            navigate_to("home")
        return
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 👥 STUDENT RESULTS")
    st.markdown("---")
    st.info("📊 Student submission tracking feature coming soon!")
    st.markdown('</div>', unsafe_allow_html=True)


def render_analytics_dashboard():
    """Render analytics dashboard for teachers"""
    if st.session_state.user_role != "teacher":
        st.error("⛔ Access Denied: This page is only for teachers")
        if st.button("Go Back"):
            navigate_to("home")
        return
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 📊 ANALYTICS DASHBOARD")
    st.markdown("---")
    st.info("📈 Analytics and performance tracking coming soon!")
    st.markdown('</div>', unsafe_allow_html=True)


def render_learn_page():
    """Render learning center page"""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 📚 LEARNING CENTER")
    st.markdown("---")
    
    st.markdown("### 🎓 Available Courses")
    
    courses = [
        {"title": "Speech Fundamentals", "duration": "2 hours", "level": "Beginner", "lessons": 8},
        {"title": "Advanced Pronunciation", "duration": "3 hours", "level": "Advanced", "lessons": 12},
        {"title": "Fluency Training", "duration": "4 hours", "level": "Intermediate", "lessons": 10}
    ]
    
    for course in courses:
        with st.expander(f"📖 {course['title']} ({course['level']})"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Duration:** {course['duration']}")
                st.write(f"**Lessons:** {course['lessons']}")
            with col2:
                st.write(f"**Level:** {course['level']}")
                if st.button(f"Start Course", key=f"course_{course['title']}"):
                    st.info("📚 Course content coming soon!")
    
    st.markdown('</div>', unsafe_allow_html=True)