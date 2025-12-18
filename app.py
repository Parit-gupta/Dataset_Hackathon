import streamlit as st
from auth import add_user, login_user
import database
import json
from audio_recorder_streamlit import audio_recorder
from datetime import datetime
import os

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = None

if "user_role" not in st.session_state:
    st.session_state.user_role = None

if "username" not in st.session_state:
    st.session_state.username = None

if "auth_stage" not in st.session_state:
    st.session_state.auth_stage = None

if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

if "selected_assessment" not in st.session_state:
    st.session_state.selected_assessment = None

if "uploaded_audio" not in st.session_state:
    st.session_state.uploaded_audio = None

if "assessment_results" not in st.session_state:
    st.session_state.assessment_results = None

if "theme" not in st.session_state:
    st.session_state.theme = "light"

if "recorded_audio" not in st.session_state:
    st.session_state.recorded_audio = None

if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0

if "question_responses" not in st.session_state:
    st.session_state.question_responses = []

if "editing_assessment" not in st.session_state:
    st.session_state.editing_assessment = None

if "new_assessment_type" not in st.session_state:
    st.session_state.new_assessment_type = None

# ---------------- PAGE CONFIG ----------------
st.set_page_config("GenAI Big Data Platform", "📊", layout="wide")

# ---------------- THEME CSS ----------------
def get_theme_css():
    if st.session_state.theme == "dark":
        return """
        <style>
        .stApp { 
            background: linear-gradient(to right, #1a1a2e, #16213e); 
            color: #e0e0e0;
        }
        .title { font-size: 34px; font-weight: 800; color: #ffffff; margin-bottom: 0; }
        .subtitle { font-size: 16px; color: #a0aec0; margin-top: 5px; }
        .card {
            background: #2d3748;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0px 10px 25px rgba(0,0,0,0.5);
            color: #e0e0e0;
        }
        .icon-card {
            background: #2d3748;
            padding: 3rem 2rem;
            border-radius: 20px;
            box-shadow: 0px 10px 25px rgba(0,0,0,0.5);
            text-align: center;
            cursor: pointer;
            transition: transform 0.3s, box-shadow 0.3s;
            height: 250px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            color: #e0e0e0;
        }
        .icon-card:hover {
            transform: translateY(-10px);
            box-shadow: 0px 15px 35px rgba(0,0,0,0.7);
            background: #374151;
        }
        .icon-text { font-size: 60px; margin-bottom: 1rem; }
        .icon-title { font-size: 28px; font-weight: 700; margin-bottom: 0.5rem; color: #ffffff; }
        .icon-desc { font-size: 16px; color: #a0aec0; }
        .assessment-card {
            background: #374151;
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            border-left: 4px solid #3b82f6;
            color: #e0e0e0;
        }
        .teacher-card {
            background: #374151;
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            border-left: 4px solid #8b5cf6;
            color: #e0e0e0;
        }
        .stats-card {
            background: #374151;
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            color: #e0e0e0;
        }
        .question-card {
            background: #374151;
            padding: 2rem;
            border-radius: 15px;
            margin: 1rem 0;
            border: 2px solid #3b82f6;
            color: #e0e0e0;
        }
        .question-text {
            font-size: 24px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 1rem;
        }
        .sentence-card {
            background: #374151;
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            border-left: 4px solid #10b981;
            color: #e0e0e0;
            font-size: 20px;
        }
        .blank-space {
            display: inline-block;
            min-width: 100px;
            border-bottom: 2px dashed #3b82f6;
            padding: 0 10px;
            color: #3b82f6;
        }
        .progress-indicator {
            background: #374151;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 1rem;
            color: #e0e0e0;
        }
        .recording-option {
            background: #374151;
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            color: #e0e0e0;
        }
        .image-container {
            background: #374151;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin: 1rem 0;
        }
        </style>
        """
    else:
        return """
        <style>
        .stApp { background: linear-gradient(to right, #f8fafc, #eef2ff); }
        .title { font-size: 34px; font-weight: 800; color: #1e293b; margin-bottom: 0; }
        .subtitle { font-size: 16px; color: #64748b; margin-top: 5px; }
        .card {
            background: white;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0px 10px 25px rgba(0,0,0,0.1);
        }
        .icon-card {
            background: white;
            padding: 3rem 2rem;
            border-radius: 20px;
            box-shadow: 0px 10px 25px rgba(0,0,0,0.1);
            text-align: center;
            cursor: pointer;
            transition: transform 0.3s, box-shadow 0.3s;
            height: 250px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .icon-card:hover {
            transform: translateY(-10px);
            box-shadow: 0px 15px 35px rgba(0,0,0,0.2);
        }
        .icon-text { font-size: 60px; margin-bottom: 1rem; }
        .icon-title { font-size: 28px; font-weight: 700; margin-bottom: 0.5rem; }
        .icon-desc { font-size: 16px; color: #666; }
        .assessment-card {
            background: #f0f9ff;
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            border-left: 4px solid #3b82f6;
        }
        .teacher-card {
            background: #f5f3ff;
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            border-left: 4px solid #8b5cf6;
        }
        .stats-card {
            background: white;
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0px 5px 15px rgba(0,0,0,0.1);
        }
        .question-card {
            background: #f0f9ff;
            padding: 2rem;
            border-radius: 15px;
            margin: 1rem 0;
            border: 2px solid #3b82f6;
        }
        .question-text {
            font-size: 24px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 1rem;
        }
        .sentence-card {
            background: #f0fdf4;
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            border-left: 4px solid #10b981;
            font-size: 20px;
        }
        .blank-space {
            display: inline-block;
            min-width: 100px;
            border-bottom: 2px dashed #3b82f6;
            padding: 0 10px;
            color: #3b82f6;
        }
        .progress-indicator {
            background: #f0f9ff;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 1rem;
        }
        .recording-option {
            background: #f9fafb;
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            border: 2px solid #e5e7eb;
        }
        .image-container {
            background: #f9fafb;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin: 1rem 0;
            border: 2px solid #e5e7eb;
        }
        </style>
        """

st.markdown(get_theme_css(), unsafe_allow_html=True)

# ---------------- HELPER FUNCTIONS ----------------
def ensure_assessments_directory():
    """Create assessments directory if it doesn't exist"""
    if not os.path.exists('assessments'):
        os.makedirs('assessments')

def load_assessments():
    """Load assessments from JSON file"""
    ensure_assessments_directory()
    try:
        with open('assessments/assessments.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        default_data = {"assessments": []}
        save_assessments(default_data)
        return default_data

def save_assessments(data):
    """Save assessments to JSON file"""
    ensure_assessments_directory()
    try:
        with open('assessments/assessments.json', 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving assessments: {e}")
        return False

def navigate_to(page):
    """Navigate to a page"""
    if page in ["assessment", "learn", "results", "teacher_dashboard", "student_results", "analytics"] and not st.session_state.logged_in:
        st.session_state.auth_stage = "login"
        st.warning("🔒 Please login first to access this feature")
    else:
        st.session_state.current_page = page
        st.rerun()

def toggle_theme():
    """Toggle between light and dark theme"""
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
    st.rerun()

def reset_assessment_state():
    """Reset all assessment-related state"""
    st.session_state.selected_assessment = None
    st.session_state.uploaded_audio = None
    st.session_state.recorded_audio = None
    st.session_state.assessment_results = None
    st.session_state.current_question_index = 0
    st.session_state.question_responses = []
    st.session_state.editing_assessment = None
    st.session_state.new_assessment_type = None

# ---------------- HEADER ----------------
col_left, col_right = st.columns([8, 2])

with col_left:
    if st.session_state.current_page != "home":
        if st.button("← Back to Home", key="back_home"):
            st.session_state.current_page = "home"
            reset_assessment_state()
            st.rerun()
    
    role_emoji = "👨‍🏫" if st.session_state.user_role == "teacher" else "🎓" if st.session_state.user_role == "student" else "📊"
    st.markdown(f'<div class="title">{role_emoji} GenAI Big Data Platform</div>', unsafe_allow_html=True)
    
    if st.session_state.logged_in and st.session_state.username:
        role_text = st.session_state.user_role.capitalize() if st.session_state.user_role else "User"
        st.markdown(f'<div class="subtitle">Welcome, {st.session_state.username} ({role_text})</div>', unsafe_allow_html=True)

with col_right:
    if not st.session_state.logged_in:
        if st.button("Login", key="top_login"):
            st.session_state.auth_stage = "login"
            st.rerun()
        if st.button("Signup", key="top_signup"):
            st.session_state.auth_stage = "signup"
            st.rerun()
    else:
        with st.popover("👤"):
            st.write(f"**Name:** {st.session_state.username}")
            st.write(f"**Email:** {st.session_state.user_email}")
            st.write(f"**Role:** {st.session_state.user_role.capitalize() if st.session_state.user_role else 'User'}")
            
            theme_icon = "🌙" if st.session_state.theme == "light" else "☀️"
            theme_text = "Dark Mode" if st.session_state.theme == "light" else "Light Mode"
            
            if st.button(f"{theme_icon} {theme_text}"):
                toggle_theme()
            
            st.divider()
            
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.user_email = None
                st.session_state.user_role = None
                st.session_state.username = None
                st.session_state.auth_stage = None
                st.session_state.current_page = "home"
                reset_assessment_state()
                st.rerun()

st.divider()

# ---------------- AUTH SECTION ----------------
if st.session_state.auth_stage and not st.session_state.logged_in:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    if st.session_state.auth_stage == "signup":
        st.subheader("📝 Create Account")
        username = st.text_input("Username", key="su_user", placeholder="Enter your name")
        email = st.text_input("Email", key="su_email", placeholder="your.email@example.com")
        password = st.text_input("Password", type="password", key="su_pass", placeholder="Min. 6 characters")
        
        role = st.radio("I am a:", ["Student", "Teacher"], horizontal=True, key="su_role")

        if st.button("Create Account", type="primary"):
            selected_role = "student" if role == "Student" else "teacher"
            if add_user(username, email, password, selected_role):
                st.session_state.auth_stage = "signup_success"
                st.rerun()
            else:
                st.error("❌ Invalid details or user already exists")

        st.markdown("---")
        if st.button("Already have an account? Login"):
            st.session_state.auth_stage = "login"
            st.rerun()

    elif st.session_state.auth_stage == "signup_success":
        st.success("🎉 Account created successfully!")
        st.info("Your account has been created. You can now login with your credentials.")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Go to Login", type="primary"):
            st.session_state.auth_stage = "login"
            st.rerun()

    elif st.session_state.auth_stage == "login":
        st.subheader("🔐 Login")
        email = st.text_input("Email", key="li_email", placeholder="your.email@example.com")
        password = st.text_input("Password", type="password", key="li_pass", placeholder="Enter your password")

        if st.button("Login", type="primary"):
            user_data = login_user(email, password)
            if user_data:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.session_state.user_role = user_data.get('role', 'student')
                st.session_state.username = user_data.get('username', 'User')
                st.session_state.auth_stage = None
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid email or password")

        st.markdown("---")
        if st.button("New here? Create an account"):
            st.session_state.auth_stage = "signup"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ===============================================================================
# HOME PAGE
# ===============================================================================
elif st.session_state.current_page == "home" and not st.session_state.auth_stage:
    
    if not st.session_state.logged_in:
        # LANDING PAGE FOR NON-LOGGED IN USERS
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
    
    elif st.session_state.user_role == "teacher":
        # TEACHER HOME PAGE
        st.markdown("### 👨‍🏫 Teacher Dashboard")
        st.markdown("<br>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        
        with c1:
            if st.button("📝", key="manage_assessments_btn", use_container_width=True):
                navigate_to("teacher_dashboard")
            st.markdown('<div class="icon-card">', unsafe_allow_html=True)
            st.markdown('<div class="icon-text">📝</div>', unsafe_allow_html=True)
            st.markdown('<div class="icon-title">MANAGE ASSESSMENTS</div>', unsafe_allow_html=True)
            st.markdown('<div class="icon-desc">Create, edit & delete assessments</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with c2:
            if st.button("👥", key="student_results_btn", use_container_width=True):
                navigate_to("student_results")
            st.markdown('<div class="icon-card">', unsafe_allow_html=True)
            st.markdown('<div class="icon-text">👥</div>', unsafe_allow_html=True)
            st.markdown('<div class="icon-title">STUDENT RESULTS</div>', unsafe_allow_html=True)
            st.markdown('<div class="icon-desc">View all student submissions</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with c3:
            if st.button("📊", key="analytics_btn", use_container_width=True):
                navigate_to("analytics")
            st.markdown('<div class="icon-card">', unsafe_allow_html=True)
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
    
    else:
        # STUDENT HOME PAGE
        st.markdown("### 🎓 Student Dashboard")
        st.markdown("<br>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        
        with c1:
            if st.button("🎤", key="assessment_btn", use_container_width=True):
                navigate_to("assessment")
            st.markdown('<div class="icon-card">', unsafe_allow_html=True)
            st.markdown('<div class="icon-text">🎤</div>', unsafe_allow_html=True)
            st.markdown('<div class="icon-title">ASSESSMENTS</div>', unsafe_allow_html=True)
            st.markdown('<div class="icon-desc">Take speech assessments</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with c2:
            if st.button("📚", key="learn_btn", use_container_width=True):
                navigate_to("learn")
            st.markdown('<div class="icon-card">', unsafe_allow_html=True)
            st.markdown('<div class="icon-text">📚</div>', unsafe_allow_html=True)
            st.markdown('<div class="icon-title">LEARN</div>', unsafe_allow_html=True)
            st.markdown('<div class="icon-desc">Courses and tutorials</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with c3:
            if st.button("📊", key="results_btn", use_container_width=True):
                navigate_to("results")
            st.markdown('<div class="icon-card">', unsafe_allow_html=True)
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

# ===============================================================================
# TEACHER DASHBOARD PAGE
# ===============================================================================
elif st.session_state.current_page == "teacher_dashboard":
    if st.session_state.user_role != "teacher":
        st.error("⛔ Access Denied: This page is only for teachers")
        if st.button("Go Back"):
            navigate_to("home")
    else:
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
            qa_count = len([a for a in teacher_assessments if a['type'] == 'qa'])
            st.metric("Q&A", qa_count)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            image_count = len([a for a in teacher_assessments if a['type'] == 'image'])
            st.metric("Image", image_count)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            fillblank_count = len([a for a in teacher_assessments if a['type'] == 'fillblank'])
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
            st.markdown("### ✨ Create New Assessment")
            
            if st.session_state.new_assessment_type == "select":
                st.markdown("**Select Assessment Type:**")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("💬 Q&A Assessment", use_container_width=True):
                        st.session_state.new_assessment_type = "qa"
                        st.rerun()
                
                with col2:
                    if st.button("🖼️ Image Description", use_container_width=True):
                        st.session_state.new_assessment_type = "image"
                        st.rerun()
                
                with col3:
                    if st.button("✍️ Fill in the Blanks", use_container_width=True):
                        st.session_state.new_assessment_type = "fillblank"
                        st.rerun()
                
                if st.button("Cancel"):
                    st.session_state.new_assessment_type = None
                    st.rerun()
            
            elif st.session_state.new_assessment_type == "qa":
                with st.form("create_qa_assessment"):
                    st.markdown("#### 💬 Q&A Assessment")
                    
                    topic = st.text_input("Assessment Topic", placeholder="e.g., General Knowledge Q&A")
                    difficulty = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced"])
                    
                    st.markdown("**Questions (Enter 5 questions):**")
                    questions = []
                    for i in range(5):
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
                                "type": "qa",
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
            
            elif st.session_state.new_assessment_type == "image":
                with st.form("create_image_assessment"):
                    st.markdown("#### 🖼️ Image Description Assessment")
                    
                    topic = st.text_input("Assessment Topic", placeholder="e.g., Image Description Challenge")
                    difficulty = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced"])
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
                                "type": "image",
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
            
            elif st.session_state.new_assessment_type == "fillblank":
                with st.form("create_fillblank_assessment"):
                    st.markdown("#### ✍️ Fill in the Blanks Assessment")
                    
                    topic = st.text_input("Assessment Topic", placeholder="e.g., Vocabulary Fill-in-the-Blank")
                    difficulty = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced"])
                    
                    st.markdown("**Sentences (Enter 5 sentences with blanks):**")
                    st.info("Use _____ (5 underscores) to mark the blank in each sentence")
                    
                    sentences = []
                    for i in range(5):
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
                        if topic and len(sentences) == 5:
                            new_assessment = {
                                "id": str(len(assessments) + 1),
                                "type": "fillblank",
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
                            st.error("❌ Please fill in all 5 sentences with answers")
                    
                    if cancel:
                        st.session_state.new_assessment_type = None
                        st.rerun()
        
        # DISPLAY EXISTING ASSESSMENTS
        if not st.session_state.new_assessment_type and teacher_assessments:
            st.markdown("---")
            st.markdown("### 📋 Your Assessments")
            
            for assessment in teacher_assessments:
                st.markdown('<div class="teacher-card">', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    type_icon = {"qa": "💬", "image": "🖼️", "fillblank": "✍️"}.get(assessment['type'], "📝")
                    st.markdown(f"**{type_icon} {assessment['topic']}**")
                    st.write(f"Type: {assessment['type'].upper()} | Difficulty: {assessment['difficulty']}")
                    st.write(f"Created: {assessment.get('created_at', 'N/A')}")
                
                with col2:
                    if st.button("✏️ Edit", key=f"edit_{assessment['id']}"):
                        st.session_state.editing_assessment = assessment
                        st.rerun()
                
                with col3:
                    if st.button("🗑️ Delete", key=f"delete_{assessment['id']}"):
                        assessments_data["assessments"] = [a for a in assessments if a['id'] != assessment['id']]
                        if save_assessments(assessments_data):
                            st.success("Assessment deleted!")
                            st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        elif not st.session_state.new_assessment_type and not teacher_assessments:
            st.info("📭 You haven't created any assessments yet. Click 'Create New Assessment' to get started!")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ===============================================================================
# STUDENT ASSESSMENT PAGE
# ===============================================================================
elif st.session_state.current_page == "assessment":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 🎤 TAKE ASSESSMENT")
    st.markdown("---")
    
    assessments_data = load_assessments()
    assessments = assessments_data.get("assessments", [])
    
    if not st.session_state.selected_assessment:
        st.markdown("### 📋 Available Assessments")
        
        if not assessments:
            st.info("📭 No assessments available yet. Please check back later!")
        else:
            type_icons = {"qa": "💬", "image": "🖼️", "fillblank": "✍️"}
            
            for assessment in assessments:
                st.markdown('<div class="assessment-card">', unsafe_allow_html=True)
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    icon = type_icons.get(assessment['type'], "📝")
                    st.markdown(f"**{icon} {assessment['topic']}**")
                    st.write(f"Difficulty: {assessment['difficulty']}")
                    if assessment['type'] == 'qa':
                        st.write(f"Questions: {len(assessment['questions'])}")
                    elif assessment['type'] == 'fillblank':
                        st.write(f"Sentences: {len(assessment['sentences'])}")
                
                with col2:
                    if st.button("Start", key=f"start_{assessment['id']}"):
                        st.session_state.selected_assessment = assessment
                        st.session_state.current_question_index = 0
                        st.session_state.question_responses = []
                        st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        assessment = st.session_state.selected_assessment
        assessment_type = assessment['type']
        
        # Q&A ASSESSMENT
        if assessment_type == "qa":
            st.markdown(f"### 💬 {assessment['topic']}")
            st.info(f"Difficulty: **{assessment['difficulty']}**")
            
            questions = assessment['questions']
            current_q = st.session_state.current_question_index
            
            st.markdown(f'<div class="progress-indicator">Question {current_q + 1} of {len(questions)}</div>', unsafe_allow_html=True)
            st.progress((current_q) / len(questions))
            
            if current_q < len(questions):
                st.markdown('<div class="question-card">', unsafe_allow_html=True)
                st.markdown(f'<div class="question-text">❓ {questions[current_q]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown("### 🎙️ Record Your Answer")
                
                tab1, tab2 = st.tabs(["🔴 Record Audio", "📁 Upload Audio"])
                
                with tab1:
                    st.markdown('<div class="recording-option">', unsafe_allow_html=True)
                    audio_bytes = audio_recorder(
                        pause_threshold=2.0,
                        sample_rate=16000,
                        text="Click to record",
                        recording_color="#e74c3c",
                        neutral_color="#6aa84f",
                        icon_name="microphone",
                        icon_size="3x",
                        key=f"recorder_q{current_q}"
                    )
                    
                    if audio_bytes:
                        st.audio(audio_bytes, format="audio/wav")
                        
                        if st.button("Submit Answer ✅", type="primary", key=f"submit_record_q{current_q}"):
                            st.session_state.question_responses.append({
                                "question": questions[current_q],
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
                        key=f"upload_q{current_q}"
                    )
                    
                    if audio_file:
                        st.audio(audio_file, format='audio/wav')
                        
                        if st.button("Submit Answer ✅", type="primary", key=f"submit_upload_q{current_q}"):
                            st.session_state.question_responses.append({
                                "question": questions[current_q],
                                "audio": audio_file,
                                "type": "uploaded"
                            })
                            st.session_state.current_question_index += 1
                            st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)
            
            else:
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
        
        # IMAGE DESCRIPTION ASSESSMENT
        elif assessment_type == "image":
            st.markdown(f"### 🖼️ {assessment['topic']}")
            st.info(f"Difficulty: **{assessment['difficulty']}**")
            
            st.markdown("---")
            st.markdown("### 📷 Describe This Image")
            
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.image(assessment['image_url'], use_column_width=True)
            st.markdown(f"**Prompt:** {assessment['prompt']}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### 🎙️ Record Your Description")
            
            tab1, tab2 = st.tabs(["🔴 Record Audio", "📁 Upload Audio"])
            
            with tab1:
                st.markdown('<div class="recording-option">', unsafe_allow_html=True)
                audio_bytes = audio_recorder(
                    pause_threshold=2.0,
                    sample_rate=16000,
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
        
        # FILL IN THE BLANK ASSESSMENT
        elif assessment_type == "fillblank":
            st.markdown(f"### ✍️ {assessment['topic']}")
            st.info(f"Difficulty: **{assessment['difficulty']}**")
            
            sentences = assessment['sentences']
            current_s = st.session_state.current_question_index
            
            st.markdown(f'<div class="progress-indicator">Sentence {current_s + 1} of {len(sentences)}</div>', unsafe_allow_html=True)
            st.progress((current_s) / len(sentences))
            
            if current_s < len(sentences):
                sentence = sentences[current_s]
                display_text = sentence['text'].replace("_____", '<span class="blank-space">_____</span>')
                
                st.markdown('<div class="sentence-card">', unsafe_allow_html=True)
                st.markdown(display_text, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown("### 🎙️ Speak the Missing Word")
                
                tab1, tab2 = st.tabs(["🔴 Record Audio", "📁 Upload Audio"])
                
                with tab1:
                    st.markdown('<div class="recording-option">', unsafe_allow_html=True)
                    audio_bytes = audio_recorder(
                        pause_threshold=2.0,
                        sample_rate=16000,
                        text="Click to record",
                        recording_color="#e74c3c",
                        neutral_color="#6aa84f",
                        icon_name="microphone",
                        icon_size="3x",
                        key=f"recorder_s{current_s}"
                    )
                    
                    if audio_bytes:
                        st.audio(audio_bytes, format="audio/wav")
                        
                        if st.button("Submit Answer ✅", type="primary", key=f"submit_record_s{current_s}"):
                            st.session_state.question_responses.append({
                                "sentence": sentence['text'],
                                "expected": sentence['blank'],
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
                        key=f"upload_s{current_s}"
                    )
                    
                    if audio_file:
                        st.audio(audio_file, format='audio/wav')
                        
                        if st.button("Submit Answer ✅", type="primary", key=f"submit_upload_s{current_s}"):
                            st.session_state.question_responses.append({
                                "sentence": sentence['text'],
                                "expected": sentence['blank'],
                                "audio": audio_file,
                                "type": "uploaded"
                            })
                            st.session_state.current_question_index += 1
                            st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)
            
            else:
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
        
        st.markdown("---")
        if st.button("← Choose Different Assessment"):
            st.session_state.selected_assessment = None
            st.session_state.current_question_index = 0
            st.session_state.question_responses = []
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ===============================================================================
# RESULTS PAGE
# ===============================================================================
elif st.session_state.current_page == "results":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 📊 ASSESSMENT RESULTS")
    st.markdown("---")
    
    if st.session_state.assessment_results:
        results = st.session_state.assessment_results
        
        st.markdown(f"### 🎯 {results['assessment_topic']}")
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Overall Score", f"{results['score']}%", delta="Good")
        with col2:
            st.metric("Accuracy", f"{results['accuracy']}%")
        with col3:
            st.metric("Fluency", f"{results['fluency']}%")
        
        st.markdown("---")
        
        st.markdown("### 📈 Detailed Analysis")
        
        st.progress(results['pronunciation'] / 100)
        st.write(f"**Pronunciation:** {results['pronunciation']}%")
        
        st.markdown("---")
        
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

# ===============================================================================
# LEARN PAGE
# ===============================================================================
elif st.session_state.current_page == "learn":
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
                    st.info("Course content coming soon!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ===============================================================================
# STUDENT RESULTS PAGE (for teachers)
# ===============================================================================
elif st.session_state.current_page == "student_results":
    if st.session_state.user_role != "teacher":
        st.error("⛔ Access Denied: This page is only for teachers")
        if st.button("Go Back"):
            navigate_to("home")
    else:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("## 👥 STUDENT RESULTS")
        st.markdown("---")
        st.info("Student submission tracking feature coming soon!")
        st.markdown('</div>', unsafe_allow_html=True)

# ===============================================================================
# ANALYTICS PAGE (for teachers)
# ===============================================================================
elif st.session_state.current_page == "analytics":
    if st.session_state.user_role != "teacher":
        st.error("⛔ Access Denied: This page is only for teachers")
        if st.button("Go Back"):
            navigate_to("home")
    else:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("## 📊 ANALYTICS DASHBOARD")
        st.markdown("---")
        st.info("Analytics and performance tracking coming soon!")
        st.markdown('</div>', unsafe_allow_html=True)