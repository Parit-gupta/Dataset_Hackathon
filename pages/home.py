"""
Home Page Logic for GenAI Big Data Platform
Includes landing page, teacher home, and student home
"""

import streamlit as st
from utils import load_assessments, navigate_to
from styles import toggle_theme


def render_landing_page():
    """Render landing page for non-logged in users with theme toggle"""
    
    # Theme toggle button at top right
    col1, col2, col3 = st.columns([6, 1, 1])
    with col3:
        theme_icon = "🌙" if st.session_state.theme == "light" else "☀️"
        if st.button(theme_icon, key="landing_theme_toggle"):
            toggle_theme()
    
    st.markdown("### Welcome to GenAI Big Data Platform")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>💡 About the Platform</h3>
            <ul>
                <li><strong>AI-Powered Speech Assessment</strong> - Advanced voice analysis technology</li>
                <li><strong>Multiple Assessment Types</strong> - Q&A, Image Description, Fill-in-Blank</li>
                <li><strong>For Teachers & Students</strong> - Complete learning ecosystem</li>
                <li><strong>Instant Feedback</strong> - Real-time results and analytics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <h3>⚙️ How It Works</h3>
            <ol>
                <li><strong>Create an Account</strong> - Choose Student or Teacher role</li>
                <li><strong>Login</strong> - Access your personalized dashboard</li>
                <li><strong>Teachers</strong> - Create and manage assessments</li>
                <li><strong>Students</strong> - Take assessments and view results</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="icon-card">', unsafe_allow_html=True)
        st.markdown('<div class="icon-text">👨‍🏫</div>', unsafe_allow_html=True)
        st.markdown('<div class="icon-title">FOR TEACHERS</div>', unsafe_allow_html=True)
        st.markdown('<div class="icon-desc">Create assessments, manage content, track student progress</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="icon-card">', unsafe_allow_html=True)
        st.markdown('<div class="icon-text">🎓</div>', unsafe_allow_html=True)
        st.markdown('<div class="icon-title">FOR STUDENTS</div>', unsafe_allow_html=True)
        st.markdown('<div class="icon-desc">Take assessments, get instant feedback, improve skills</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="icon-card">', unsafe_allow_html=True)
        st.markdown('<div class="icon-text">📊</div>', unsafe_allow_html=True)
        st.markdown('<div class="icon-title">ANALYTICS</div>', unsafe_allow_html=True)
        st.markdown('<div class="icon-desc">Comprehensive performance tracking and insights</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("👆 Please Login or Signup to get started!")


def render_teacher_home():
    """Render home page for teachers"""
    st.markdown("### 👨‍🏫 Teacher Dashboard")
    st.markdown("<br>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown('<div class="icon-card clickable">', unsafe_allow_html=True)
        if st.button("📝 MANAGE", key="manage_btn", use_container_width=True):
            navigate_to("teacher_dashboard")
        st.markdown('<div class="icon-text">📝</div>', unsafe_allow_html=True)
        st.markdown('<div class="icon-title">MANAGE ASSESSMENTS</div>', unsafe_allow_html=True)
        st.markdown('<div class="icon-desc">Create, edit & delete assessments</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c2:
        st.markdown('<div class="icon-card clickable">', unsafe_allow_html=True)
        if st.button("👥 RESULTS", key="student_results_btn", use_container_width=True):
            navigate_to("student_results")
        st.markdown('<div class="icon-text">👥</div>', unsafe_allow_html=True)
        st.markdown('<div class="icon-title">STUDENT RESULTS</div>', unsafe_allow_html=True)
        st.markdown('<div class="icon-desc">View all student submissions</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c3:
        st.markdown('<div class="icon-card clickable">', unsafe_allow_html=True)
        if st.button("📊 ANALYTICS", key="analytics_btn", use_container_width=True):
            navigate_to("analytics")
        st.markdown('<div class="icon-text">📊</div>', unsafe_allow_html=True)
        st.markdown('<div class="icon-title">ANALYTICS</div>', unsafe_allow_html=True)
        st.markdown('<div class="icon-desc">Performance metrics & insights</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Stats
    assessments_data = load_assessments()
    assessments = assessments_data.get("assessments", [])
    teacher_assessments = [a for a in assessments if a.get('created_by') == st.session_state.user_email]
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="card">
            <h3>📊 Quick Stats</h3>
            <ul>
                <li><strong>Total Assessments:</strong> {}</li>
                <li><strong>Q&A Assessments:</strong> {}</li>
                <li><strong>Image Assessments:</strong> {}</li>
                <li><strong>Fill-in-Blank:</strong> {}</li>
            </ul>
        </div>
        """.format(
            len(teacher_assessments),
            len([a for a in teacher_assessments if a['type'] == 'qa']),
            len([a for a in teacher_assessments if a['type'] == 'image']),
            len([a for a in teacher_assessments if a['type'] == 'fillblank'])
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>🚀 Quick Actions</h3>
            <p>Get started with these common tasks:</p>
            <ul>
                <li>Create your first assessment</li>
                <li>View student submissions</li>
                <li>Check analytics dashboard</li>
                <li>Edit existing assessments</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


def render_student_home():
    """Render home page for students"""
    st.markdown("### 🎓 Student Dashboard")
    st.markdown("<br>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown('<div class="icon-card clickable">', unsafe_allow_html=True)
        if st.button("🎤 START", key="assessment_btn", use_container_width=True):
            navigate_to("assessment")
        st.markdown('<div class="icon-text">🎤</div>', unsafe_allow_html=True)
        st.markdown('<div class="icon-title">ASSESSMENTS</div>', unsafe_allow_html=True)
        st.markdown('<div class="icon-desc">Take speech assessments</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c2:
        st.markdown('<div class="icon-card clickable">', unsafe_allow_html=True)
        if st.button("📚 LEARN", key="learn_btn", use_container_width=True):
            navigate_to("learn")
        st.markdown('<div class="icon-text">📚</div>', unsafe_allow_html=True)
        st.markdown('<div class="icon-title">LEARN</div>', unsafe_allow_html=True)
        st.markdown('<div class="icon-desc">Courses and tutorials</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c3:
        st.markdown('<div class="icon-card clickable">', unsafe_allow_html=True)
        if st.button("📊 VIEW", key="results_btn", use_container_width=True):
            navigate_to("results")
        st.markdown('<div class="icon-text">📊</div>', unsafe_allow_html=True)
        st.markdown('<div class="icon-title">MY RESULTS</div>', unsafe_allow_html=True)
        st.markdown('<div class="icon-desc">View your performance</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>💡 Available Features</h3>
            <ul>
                <li><strong>Multiple Assessment Types</strong> - Q&A, Image, Fill-in-Blank</li>
                <li><strong>Voice Recording</strong> - Record or upload audio</li>
                <li><strong>Instant Feedback</strong> - Get results immediately</li>
                <li><strong>Track Progress</strong> - Monitor your improvement</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <h3>🎯 Getting Started</h3>
            <ol>
                <li>Browse available assessments</li>
                <li>Select an assessment to take</li>
                <li>Record your responses</li>
                <li>Submit and view results</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)