import streamlit as st
from auth import add_user, login_user
import database  # init DB
import json
from audio_recorder_streamlit import audio_recorder

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = None

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
        .title { font-size: 34px; font-weight: 800; color: #ffffff; }
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
        .stButton > button {
            border-radius: 25px;
            font-weight: 600;
        }
        .assessment-card {
            background: #374151;
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            border-left: 4px solid #3b82f6;
            color: #e0e0e0;
        }
        .result-success {
            background: #1e4620;
            padding: 1rem;
            border-radius: 10px;
            border-left: 4px solid #22c55e;
            color: #a7f3d0;
        }
        .result-warning {
            background: #78350f;
            padding: 1rem;
            border-radius: 10px;
            border-left: 4px solid #f59e0b;
            color: #fde68a;
        }
        .recording-option {
            background: #374151;
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            color: #e0e0e0;
        }
        </style>
        """
    else:
        return """
        <style>
        .stApp { background: linear-gradient(to right, #f8fafc, #eef2ff); }
        .title { font-size: 34px; font-weight: 800; color: #1e293b; }
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
        .stButton > button {
            border-radius: 25px;
            font-weight: 600;
        }
        .assessment-card {
            background: #f0f9ff;
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            border-left: 4px solid #3b82f6;
        }
        .result-success {
            background: #f0fdf4;
            padding: 1rem;
            border-radius: 10px;
            border-left: 4px solid #22c55e;
        }
        .result-warning {
            background: #fef3c7;
            padding: 1rem;
            border-radius: 10px;
            border-left: 4px solid #f59e0b;
        }
        .recording-option {
            background: #f9fafb;
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            border: 2px solid #e5e7eb;
        }
        </style>
        """

st.markdown(get_theme_css(), unsafe_allow_html=True)

# ---------------- HELPER FUNCTIONS ----------------
def load_assessments():
    """Load assessments from JSON file"""
    try:
        with open('assessments/assessments.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "assessments": [
                {
                    "id": "1",
                    "topic": "English Pronunciation",
                    "language": "English",
                    "difficulty": "Beginner",
                    "words": ["hello", "world", "python", "assessment", "speech"]
                },
                {
                    "id": "2",
                    "topic": "Spanish Basics",
                    "language": "Spanish",
                    "difficulty": "Intermediate",
                    "words": ["hola", "mundo", "gracias", "amigo", "familia"]
                }
            ]
        }

def navigate_to(page):
    """Navigate to a page, check login first"""
    if page in ["assessment", "learn", "results"] and not st.session_state.logged_in:
        st.session_state.auth_stage = "login"
        st.warning("🔒 Please login first to access this feature")
    else:
        st.session_state.current_page = page
        st.rerun()

def toggle_theme():
    """Toggle between light and dark theme"""
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
    st.rerun()

# ---------------- HEADER ----------------
col_left, col_right = st.columns([8, 2])

with col_left:
    if st.session_state.current_page != "home":
        if st.button("← Back to Home", key="back_home"):
            st.session_state.current_page = "home"
            st.session_state.selected_assessment = None
            st.session_state.uploaded_audio = None
            st.session_state.recorded_audio = None
            st.session_state.assessment_results = None
            st.rerun()
    st.markdown('<div class="title">🚀 GenAI Big Data Platform</div>', unsafe_allow_html=True)

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
            st.write(f"*Email:* {st.session_state.user_email}")
            
            # Theme Toggle
            theme_icon = "🌙" if st.session_state.theme == "light" else "☀"
            theme_text = "Dark Mode" if st.session_state.theme == "light" else "Light Mode"
            
            if st.button(f"{theme_icon} {theme_text}"):
                toggle_theme()
            
            st.divider()
            
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.user_email = None
                st.session_state.auth_stage = None
                st.session_state.current_page = "home"
                st.rerun()

st.divider()

# ---------------- AUTH SECTION ----------------
if st.session_state.auth_stage and not st.session_state.logged_in:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    if st.session_state.auth_stage == "signup":
        st.subheader("📝 Create Account")
        username = st.text_input("Username", key="su_user")
        email = st.text_input("Email", key="su_email")
        password = st.text_input("Password", type="password", key="su_pass")

        if st.button("Create Account"):
            if add_user(username, email, password):
                st.session_state.auth_stage = "signup_success"
                st.rerun()
            else:
                st.error("Invalid details or user already exists")

        st.markdown("---")
        if st.button("Already have an account? Login"):
            st.session_state.auth_stage = "login"
            st.rerun()

    elif st.session_state.auth_stage == "signup_success":
        st.success("🎉 Account created successfully!")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Go to Login"):
            st.session_state.auth_stage = "login"
            st.rerun()

    elif st.session_state.auth_stage == "login":
        st.subheader("🔐 Login")
        email = st.text_input("Email", key="li_email")
        password = st.text_input("Password", type="password", key="li_pass")

        if st.button("Login"):
            if login_user(email, password):
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.session_state.auth_stage = None
                st.success("Login successful 🎉")
                st.rerun()
            else:
                st.error("Invalid email or password")

        st.markdown("---")
        if st.button("New here? Create an account"):
            st.session_state.auth_stage = "signup"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PAGE ROUTING ----------------
if st.session_state.current_page == "home" and not st.session_state.auth_stage:
    # HOME PAGE WITH 3 OPTIONS
    st.markdown("### Choose Your Path")
    st.markdown("<br>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        if st.button("🎤", key="assessment_btn", use_container_width=True):
            navigate_to("assessment")
        st.markdown('<div class="icon-card">', unsafe_allow_html=True)
        st.markdown('<div class="icon-text">🎤</div>', unsafe_allow_html=True)
        st.markdown('<div class="icon-title">ASSESSMENT</div>', unsafe_allow_html=True)
        st.markdown('<div class="icon-desc">Take speech assessments</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c2:
        if st.button("📚", key="learn_btn", use_container_width=True):
            navigate_to("learn")
        st.markdown('<div class="icon-card">', unsafe_allow_html=True)
        st.markdown('<div class="icon-text">📚</div>', unsafe_allow_html=True)
        st.markdown('<div class="icon-title">LEARN</div>', unsafe_allow_html=True)
        st.markdown('<div class="icon-desc">Explore courses and tutorials</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c3:
        if st.button("📊", key="results_btn", use_container_width=True):
            navigate_to("results")
        st.markdown('<div class="icon-card">', unsafe_allow_html=True)
        st.markdown('<div class="icon-text">📊</div>', unsafe_allow_html=True)
        st.markdown('<div class="icon-title">RESULTS</div>', unsafe_allow_html=True)
        st.markdown('<div class="icon-desc">View your assessment results</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # INFO SECTION
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">
            <h3>💡 About</h3>
            <ul>
                <li>AI-powered speech assessment</li>
                <li>Multiple language support</li>
                <li>Instant feedback & results</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <h3>⚙ How It Works</h3>
            <ol>
                <li>Create account / Login</li>
                <li>Select an assessment</li>
                <li>Record your speech</li>
                <li>Get instant results</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

# ---------------- ASSESSMENT PAGE ----------------
elif st.session_state.current_page == "assessment":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 🎤 SPEECH ASSESSMENT")
    st.markdown("---")
    
    assessments_data = load_assessments()
    assessments = assessments_data.get("assessments", [])
    
    if not st.session_state.selected_assessment:
        # STEP 1: SELECT ASSESSMENT
        st.markdown("### 📋 Select an Assessment")
        
        for assessment in assessments:
            with st.container():
                st.markdown('<div class="assessment-card">', unsafe_allow_html=True)
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"{assessment['topic']}")
                    st.write(f"Language: {assessment['language']} | Difficulty: {assessment['difficulty']}")
                    st.write(f"Words to pronounce: {len(assessment['words'])} words")
                
                with col2:
                    if st.button("Select", key=f"select_{assessment['id']}"):
                        st.session_state.selected_assessment = assessment
                        st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # STEP 2: RECORD OR UPLOAD AUDIO
        assessment = st.session_state.selected_assessment
        
        st.markdown(f"### 🎯 Assessment: {assessment['topic']}")
        st.info(f"Language: *{assessment['language']}* | Difficulty: *{assessment['difficulty']}*")
        
        st.markdown("---")
        st.markdown("### 📝 Words to Pronounce:")
        
        cols = st.columns(3)
        for idx, word in enumerate(assessment['words']):
            with cols[idx % 3]:
                st.markdown(f"{idx + 1}.** {word}")
        
        st.markdown("---")
        st.markdown("### 🎙 Choose Recording Method")
        
        # Two options: Record or Upload
        tab1, tab2 = st.tabs(["🔴 Record Audio", "📁 Upload Audio"])
        
        with tab1:
            st.markdown('<div class="recording-option">', unsafe_allow_html=True)
            st.markdown("#### Record your voice directly")
            st.info("Click the microphone button below to start recording. Click again to stop.")
            
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
                st.session_state.recorded_audio = audio_bytes
                
                if st.button("Submit Recorded Audio 🚀", type="primary"):
                    with st.spinner("🔍 Analyzing your speech..."):
                        # TODO: Add your speech processing logic here
                        st.session_state.assessment_results = {
                            "score": 85,
                            "accuracy": 90,
                            "fluency": 80,
                            "pronunciation": 85,
                            "feedback": "Great job! Your pronunciation is clear and accurate.",
                            "assessment_topic": assessment['topic']
                        }
                        
                        st.success("✅ Assessment submitted successfully!")
                        st.balloons()
                        
                        if st.button("View Results"):
                            navigate_to("results")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="recording-option">', unsafe_allow_html=True)
            st.markdown("#### Upload a pre-recorded audio file")
            
            audio_file = st.file_uploader(
                "Upload audio file (WAV, MP3, M4A)",
                type=['wav', 'mp3', 'm4a'],
                key="audio_upload"
            )
            
            if audio_file:
                st.audio(audio_file, format='audio/wav')
                
                if st.button("Submit Uploaded Audio 🚀", type="primary"):
                    with st.spinner("🔍 Analyzing your speech..."):
                        # TODO: Add your speech processing logic here
                        st.session_state.uploaded_audio = audio_file
                        
                        st.session_state.assessment_results = {
                            "score": 85,
                            "accuracy": 90,
                            "fluency": 80,
                            "pronunciation": 85,
                            "feedback": "Great job! Your pronunciation is clear and accurate.",
                            "assessment_topic": assessment['topic']
                        }
                        
                        st.success("✅ Assessment submitted successfully!")
                        st.balloons()
                        
                        if st.button("View Results"):
                            navigate_to("results")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        if st.button("← Choose Different Assessment"):
            st.session_state.selected_assessment = None
            st.session_state.recorded_audio = None
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- LEARN PAGE ----------------
elif st.session_state.current_page == "learn":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 📚 LEARN PAGE")
    st.markdown("---")
    st.write("This is the LEARN page. Add your learning content here!")
    st.info("You can add courses, tutorials, videos, or learning materials here.")
    
    # Sample learning content structure
    st.markdown("### 🎓 Available Courses")
    
    courses = [
        {"title": "English Pronunciation Basics", "duration": "2 hours", "level": "Beginner"},
        {"title": "Advanced Speaking Techniques", "duration": "3 hours", "level": "Advanced"},
        {"title": "Accent Training", "duration": "4 hours", "level": "Intermediate"}
    ]
    
    for course in courses:
        with st.expander(f"📖 {course['title']}"):
            st.write(f"*Duration:* {course['duration']}")
            st.write(f"*Level:* {course['level']}")
            st.button(f"Start Course: {course['title']}", key=f"course_{course['title']}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RESULTS PAGE ----------------
elif st.session_state.current_page == "results":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 📊 ASSESSMENT RESULTS")
    st.markdown("---")
    
    if st.session_state.assessment_results:
        results = st.session_state.assessment_results
        
        st.markdown(f"### 🎯 {results['assessment_topic']}")
        st.markdown("---")
        
        # Overall Score
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Overall Score", f"{results['score']}%", delta="Good")
        with col2:
            st.metric("Accuracy", f"{results['accuracy']}%")
        with col3:
            st.metric("Fluency", f"{results['fluency']}%")
        
        st.markdown("---")
        
        # Detailed Metrics
        st.markdown("### 📈 Detailed Analysis")
        
        st.progress(results['pronunciation'] / 100)
        st.write(f"*Pronunciation:* {results['pronunciation']}%")
        
        st.markdown("---")
        
        # Feedback
        st.markdown("### 💬 Feedback")
        if results['score'] >= 60:
            st.markdown(f'<div class="result-success">{results["feedback"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="result-warning">{results["feedback"]}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.button("Take Another Assessment"):
            st.session_state.selected_assessment = None
            st.session_state.uploaded_audio = None
            st.session_state.recorded_audio = None
            st.session_state.assessment_results = None
            navigate_to("assessment")
    
    else:
        st.info("📭 No assessment results yet. Take an assessment first!")
        if st.button("Take Assessment Now"):
            navigate_to("assessment")
    
    st.markdown('</div>', unsafe_allow_html=True)
