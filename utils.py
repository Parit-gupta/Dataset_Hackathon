"""
Utility Functions for GenAI Big Data Platform
"""

import streamlit as st
import json
import os
from config import (
    ASSESSMENTS_DIR, 
    ASSESSMENTS_FILE,
    PAGE_ASSESSMENT,
    PAGE_LEARN,
    PAGE_RESULTS,
    PAGE_TEACHER_DASHBOARD,
    PAGE_STUDENT_RESULTS,
    PAGE_ANALYTICS
)

# ============================================================================
# FILE SYSTEM UTILITIES
# ============================================================================

def ensure_assessments_directory():
    """Create assessments directory if it doesn't exist"""
    if not os.path.exists(ASSESSMENTS_DIR):
        os.makedirs(ASSESSMENTS_DIR)


def load_assessments():
    """Load assessments from JSON file"""
    ensure_assessments_directory()
    try:
        with open(ASSESSMENTS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        default_data = {"assessments": []}
        save_assessments(default_data)
        return default_data
    except json.JSONDecodeError:
        # If file is corrupted, return default
        default_data = {"assessments": []}
        save_assessments(default_data)
        return default_data


def save_assessments(data):
    """Save assessments to JSON file"""
    ensure_assessments_directory()
    try:
        with open(ASSESSMENTS_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving assessments: {e}")
        return False


# ============================================================================
# NAVIGATION UTILITIES
# ============================================================================

def navigate_to(page):
    """Navigate to a page with authentication check"""
    protected_pages = [
        PAGE_ASSESSMENT, 
        PAGE_LEARN, 
        PAGE_RESULTS, 
        PAGE_TEACHER_DASHBOARD, 
        PAGE_STUDENT_RESULTS, 
        PAGE_ANALYTICS
    ]
    
    if page in protected_pages and not st.session_state.logged_in:
        st.session_state.auth_stage = "login"
        st.warning("🔒 Please login first to access this feature")
    else:
        st.session_state.current_page = page
        st.rerun()


# ============================================================================
# SESSION STATE UTILITIES
# ============================================================================

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


def initialize_session_state():
    """Initialize all session state variables"""
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


# ============================================================================
# ASSESSMENT UTILITIES
# ============================================================================

def get_teacher_assessments(email):
    """Get all assessments created by a specific teacher"""
    assessments_data = load_assessments()
    assessments = assessments_data.get("assessments", [])
    return [a for a in assessments if a.get('created_by') == email]


def get_assessment_by_id(assessment_id):
    """Get a specific assessment by ID"""
    assessments_data = load_assessments()
    assessments = assessments_data.get("assessments", [])
    for assessment in assessments:
        if assessment.get('id') == assessment_id:
            return assessment
    return None


def delete_assessment_by_id(assessment_id):
    """Delete an assessment by ID"""
    assessments_data = load_assessments()
    assessments_data["assessments"] = [
        a for a in assessments_data["assessments"] 
        if a.get('id') != assessment_id
    ]
    return save_assessments(assessments_data)


# ============================================================================
# AUDIO UTILITIES
# ============================================================================

def validate_audio_file(file):
    """Validate uploaded audio file"""
    if file is None:
        return False, "No file uploaded"
    
    allowed_types = ['audio/wav', 'audio/mpeg', 'audio/mp3', 'audio/x-m4a']
    if file.type not in allowed_types:
        return False, "Invalid file type. Please upload WAV, MP3, or M4A"
    
    # Check file size (max 10MB)
    if file.size > 10 * 1024 * 1024:
        return False, "File too large. Maximum size is 10MB"
    
    return True, "Valid file"


# ============================================================================
# THEME UTILITIES
# ============================================================================

def toggle_theme():
    """Toggle between light and dark theme"""
    from config import THEME_LIGHT, THEME_DARK
    st.session_state.theme = THEME_DARK if st.session_state.theme == THEME_LIGHT else THEME_LIGHT
    st.rerun()


# ============================================================================
# USER UTILITIES
# ============================================================================

def logout_user():
    """Logout current user and reset session"""
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.session_state.user_role = None
    st.session_state.username = None
    st.session_state.auth_stage = None
    st.session_state.current_page = "home"
    reset_assessment_state()
    st.rerun()


# ============================================================================
# FORMATTING UTILITIES
# ============================================================================

def format_timestamp(timestamp_str):
    """Format timestamp string for display"""
    try:
        from datetime import datetime
        dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%b %d, %Y at %I:%M %p")
    except:
        return timestamp_str


def get_assessment_icon(assessment_type):
    """Get icon for assessment type"""
    icons = {
        "qa": "💬",
        "image": "🖼️",
        "fillblank": "✍️"
    }
    return icons.get(assessment_type, "📝")


def get_difficulty_color(difficulty):
    """Get color for difficulty level"""
    colors = {
        "Beginner": "#10b981",
        "Intermediate": "#f59e0b",
        "Advanced": "#ef4444"
    }
    return colors.get(difficulty, "#6b7280")