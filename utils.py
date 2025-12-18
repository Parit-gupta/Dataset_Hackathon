"""
Utility Functions for GenAI Big Data Platform
Helper functions for file operations, session state, and navigation
"""

import streamlit as st
import json
import os
import uuid
from datetime import datetime
from config import (
    ASSESSMENTS_FILE,
    ASSESSMENTS_DIR,
    PAGE_HOME,
    THEME_LIGHT,
    THEME_DARK
)


# ============================================================================
# SESSION STATE MANAGEMENT
# ============================================================================

def initialize_session_state():
    """Initialize all session state variables"""
    
    # Authentication
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'auth_stage' not in st.session_state:
        st.session_state.auth_stage = None
    
    # Navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = PAGE_HOME
    
    # Theme
    if 'theme' not in st.session_state:
        st.session_state.theme = THEME_LIGHT
    
    # Assessment state
    if 'selected_assessment' not in st.session_state:
        st.session_state.selected_assessment = None
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'question_responses' not in st.session_state:
        st.session_state.question_responses = []
    if 'assessment_results' not in st.session_state:
        st.session_state.assessment_results = None
    
    # Teacher state
    if 'viewing_assessment' not in st.session_state:
        st.session_state.viewing_assessment = None


def reset_assessment_state():
    """Reset assessment-related session state"""
    st.session_state.selected_assessment = None
    st.session_state.current_question_index = 0
    st.session_state.question_responses = []
    st.session_state.assessment_results = None


# ============================================================================
# NAVIGATION
# ============================================================================

def navigate_to(page):
    """Navigate to a different page"""
    st.session_state.current_page = page
    st.rerun()


# ============================================================================
# FILE OPERATIONS
# ============================================================================

def ensure_directories():
    """Ensure all required directories exist"""
    os.makedirs(ASSESSMENTS_DIR, exist_ok=True)


def load_assessments():
    """
    Load assessments from JSON file
    
    Returns:
        dict: Dictionary containing assessments list
    """
    ensure_directories()
    
    if not os.path.exists(ASSESSMENTS_FILE):
        # Create empty assessments file
        default_data = {"assessments": []}
        save_assessments(default_data)
        return default_data
    
    try:
        with open(ASSESSMENTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading assessments: {e}")
        return {"assessments": []}


def save_assessments(data):
    """
    Save assessments to JSON file
    
    Args:
        data (dict): Dictionary containing assessments
    """
    ensure_directories()
    
    try:
        with open(ASSESSMENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving assessments: {e}")
        return False


def generate_assessment_id():
    """
    Generate a unique assessment ID
    
    Returns:
        str: Unique assessment ID
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return f"assess_{timestamp}_{unique_id}"


def get_assessment_by_id(assessment_id):
    """
    Get assessment by ID
    
    Args:
        assessment_id (str): Assessment ID
        
    Returns:
        dict: Assessment object or None
    """
    data = load_assessments()
    assessments = data.get("assessments", [])
    
    for assessment in assessments:
        if assessment.get('id') == assessment_id:
            return assessment
    
    return None


def delete_assessment(assessment_id):
    """
    Delete an assessment by ID
    
    Args:
        assessment_id (str): Assessment ID
        
    Returns:
        bool: True if deleted successfully
    """
    data = load_assessments()
    assessments = data.get("assessments", [])
    
    # Filter out the assessment
    data["assessments"] = [a for a in assessments if a.get('id') != assessment_id]
    
    return save_assessments(data)


def update_assessment(assessment_id, updated_data):
    """
    Update an assessment
    
    Args:
        assessment_id (str): Assessment ID
        updated_data (dict): Updated assessment data
        
    Returns:
        bool: True if updated successfully
    """
    data = load_assessments()
    assessments = data.get("assessments", [])
    
    for i, assessment in enumerate(assessments):
        if assessment.get('id') == assessment_id:
            assessments[i] = updated_data
            data["assessments"] = assessments
            return save_assessments(data)
    
    return False


# ============================================================================
# ASSESSMENT HELPERS
# ============================================================================

def get_assessments_by_teacher(teacher_username):
    """
    Get all assessments created by a teacher
    
    Args:
        teacher_username (str): Teacher's username
        
    Returns:
        list: List of assessments
    """
    data = load_assessments()
    assessments = data.get("assessments", [])
    
    return [a for a in assessments if a.get('created_by') == teacher_username]


def get_assessments_by_type(assessment_type):
    """
    Get all assessments of a specific type
    
    Args:
        assessment_type (str): Assessment type
        
    Returns:
        list: List of assessments
    """
    data = load_assessments()
    assessments = data.get("assessments", [])
    
    return [a for a in assessments if a.get('type') == assessment_type]


def count_assessments_by_teacher(teacher_username):
    """
    Count assessments created by a teacher
    
    Args:
        teacher_username (str): Teacher's username
        
    Returns:
        int: Number of assessments
    """
    return len(get_assessments_by_teacher(teacher_username))


# ============================================================================
# AUDIO HELPERS
# ============================================================================

def validate_audio_file(file):
    """
    Validate uploaded audio file
    
    Args:
        file: Streamlit UploadedFile object
        
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if file is None:
        return False, "No file uploaded"
    
    # Check file size (max 10MB)
    max_size = 10 * 1024 * 1024  # 10MB
    if file.size > max_size:
        return False, "File too large. Maximum size is 10MB"
    
    # Check file type
    allowed_types = ['audio/wav', 'audio/mpeg', 'audio/mp3', 'audio/x-m4a']
    if file.type not in allowed_types:
        return False, "Invalid file type. Please upload WAV, MP3, or M4A"
    
    return True, "File is valid"


# ============================================================================
# DATE/TIME HELPERS
# ============================================================================

def format_datetime(iso_string):
    """
    Format ISO datetime string to readable format
    
    Args:
        iso_string (str): ISO format datetime string
        
    Returns:
        str: Formatted datetime string
    """
    try:
        dt = datetime.fromisoformat(iso_string)
        return dt.strftime("%B %d, %Y at %I:%M %p")
    except:
        return iso_string


def get_current_timestamp():
    """
    Get current timestamp in ISO format
    
    Returns:
        str: Current timestamp
    """
    return datetime.now().isoformat()


# ============================================================================
# VALIDATION HELPERS
# ============================================================================

def validate_text_input(text, min_length=1, max_length=500):
    """
    Validate text input
    
    Args:
        text (str): Text to validate
        min_length (int): Minimum length
        max_length (int): Maximum length
        
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if not text or not text.strip():
        return False, "Text cannot be empty"
    
    text = text.strip()
    
    if len(text) < min_length:
        return False, f"Text must be at least {min_length} characters"
    
    if len(text) > max_length:
        return False, f"Text must be less than {max_length} characters"
    
    return True, "Valid"


def validate_word(word):
    """
    Validate a single word
    
    Args:
        word (str): Word to validate
        
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if not word or not word.strip():
        return False, "Word cannot be empty"
    
    word = word.strip()
    
    # Check if it's a single word (no spaces)
    if ' ' in word:
        return False, "Please enter a single word without spaces"
    
    # Check length
    if len(word) < 2:
        return False, "Word must be at least 2 characters"
    
    if len(word) > 50:
        return False, "Word must be less than 50 characters"
    
    # Check if alphabetic (with optional hyphens and apostrophes)
    if not all(c.isalpha() or c in ['-', "'"] for c in word):
        return False, "Word can only contain letters, hyphens, and apostrophes"
    
    return True, "Valid"


# ============================================================================
# STATISTICS HELPERS
# ============================================================================

def calculate_average_score(responses):
    """
    Calculate average score from responses
    
    Args:
        responses (list): List of response dictionaries
        
    Returns:
        float: Average score
    """
    if not responses:
        return 0.0
    
    total = sum(r.get('score', 0) for r in responses)
    return round(total / len(responses), 2)


def get_grade_from_score(score):
    """
    Get letter grade from numerical score
    
    Args:
        score (float): Numerical score (0-100)
        
    Returns:
        str: Letter grade
    """
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def get_performance_emoji(score):
    """
    Get emoji based on performance score
    
    Args:
        score (float): Score (0-100)
        
    Returns:
        str: Emoji
    """
    if score >= 90:
        return "🌟"
    elif score >= 80:
        return "👍"
    elif score >= 70:
        return "✅"
    elif score >= 60:
        return "📚"
    else:
        return "💪"


# ============================================================================
# STRING HELPERS
# ============================================================================

def truncate_text(text, max_length=50):
    """
    Truncate text to maximum length
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length
        
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def sanitize_filename(filename):
    """
    Sanitize filename to remove invalid characters
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Sanitized filename
    """
    # Remove invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    
    return filename