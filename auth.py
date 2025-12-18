"""
Authentication Module for GenAI Big Data Platform
Handles user login, registration, and session management
"""

import streamlit as st
from database import (
    verify_user, 
    register_user, 
    get_user_role,
    get_user_by_email,
    user_exists
)

def init_auth_state():
    """Initialize authentication-related session state"""
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

def add_user(username, email, password, role):
    """
    Add a new user to the system
    
    Args:
        username (str): User's display name
        email (str): User's email (used as login)
        password (str): User's password
        role (str): User role ('teacher' or 'student')
        
    Returns:
        bool: True if registration successful, False otherwise
    """
    # Validation
    if not username or not email or not password:
        return False
    
    if len(username) < 2:
        return False
    
    if len(password) < 6:
        return False
    
    if '@' not in email:
        return False
    
    if role not in ['teacher', 'student']:
        return False
    
    if user_exists(email):
        return False
    
    # Register user
    return register_user(username, email, password, role)

def login_user(email, password):
    """
    Authenticate user and return user data
    
    Args:
        email (str): User's email
        password (str): User's password
        
    Returns:
        dict: User data if successful, None otherwise
        Example: {'username': 'John', 'role': 'student', 'email': 'john@example.com'}
    """
    if not email or not password:
        return None
    
    if verify_user(email, password):
        user_data = get_user_by_email(email)
        return user_data
    
    return None

def logout_user():
    """Clear authentication session state"""
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.user_email = None
    st.session_state.user_role = None
    st.session_state.auth_stage = None
    st.session_state.current_page = 'home'

def is_authenticated():
    """Check if user is authenticated"""
    return st.session_state.get('logged_in', False)

def get_current_user():
    """Get current logged-in username"""
    return st.session_state.get('username', None)

def get_current_email():
    """Get current logged-in user's email"""
    return st.session_state.get('user_email', None)

def get_current_role():
    """Get current user's role"""
    return st.session_state.get('user_role', None)

def is_teacher():
    """Check if current user is a teacher"""
    return st.session_state.get('user_role') == 'teacher'

def is_student():
    """Check if current user is a student"""
    return st.session_state.get('user_role') == 'student'

def require_auth(role=None):
    """
    Check authentication and role
    
    Args:
        role (str, optional): Required role ('teacher' or 'student')
        
    Returns:
        bool: True if authenticated and has required role
    """
    if not is_authenticated():
        return False
    
    if role and get_current_role() != role:
        return False
    
    return True

def validate_email(email):
    """
    Validate email format
    
    Args:
        email (str): Email to validate
        
    Returns:
        bool: True if valid email format
    """
    if not email or '@' not in email or '.' not in email:
        return False
    return True

def validate_password(password):
    """
    Validate password strength
    
    Args:
        password (str): Password to validate
        
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    
    return True, "Password is valid"

def validate_username(username):
    """
    Validate username
    
    Args:
        username (str): Username to validate
        
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if not username:
        return False, "Username is required"
    
    if len(username) < 2:
        return False, "Username must be at least 2 characters"
    
    if len(username) > 50:
        return False, "Username must be less than 50 characters"
    
    return True, "Username is valid"