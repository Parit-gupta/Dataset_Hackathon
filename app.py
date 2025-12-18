"""
Main Entry Point for GenAI Big Data Platform
Modular Architecture - Connects all components
"""

import streamlit as st
from config import (
    APP_TITLE, APP_ICON, APP_LAYOUT,
    PAGE_HOME, PAGE_ASSESSMENT, PAGE_TEACHER_DASHBOARD,
    PAGE_RESULTS, PAGE_LEARN, PAGE_STUDENT_RESULTS, PAGE_ANALYTICS
)
from styles import get_theme_css, toggle_theme
from utils import initialize_session_state, navigate_to, reset_assessment_state
from auth import add_user, login_user

# Import page modules
from pages.home import render_landing_page, render_teacher_home, render_student_home
from pages.teacher_dashboard import render_teacher_dashboard
from pages.student_assessment import render_assessment_page
from pages.results import (
    render_student_results,
    render_teacher_student_results,
    render_analytics_dashboard,
    render_learn_page
)

# ============================================================================
# INITIALIZE SESSION STATE
# ============================================================================
initialize_session_state()

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(APP_TITLE, APP_ICON, layout=APP_LAYOUT)

# ============================================================================
# APPLY THEME
# ============================================================================
st.markdown(get_theme_css(), unsafe_allow_html=True)

# ============================================================================
# HEADER SECTION
# ============================================================================
col_left, col_right = st.columns([8, 2])

with col_left:
    # Back to home button
    if st.session_state.current_page != PAGE_HOME:
        if st.button("← Back to Home", key="back_home"):
            st.session_state.current_page = PAGE_HOME
            reset_assessment_state()
            st.rerun()
    
    # Title with role emoji
    role_emoji = (
        "👨‍🏫" if st.session_state.user_role == "teacher" 
        else "🎓" if st.session_state.user_role == "student" 
        else "📊"
    )
    st.markdown(
        f'<div class="title">{role_emoji} {APP_TITLE}</div>', 
        unsafe_allow_html=True
    )
    
    # Welcome message for logged-in users
    if st.session_state.logged_in and st.session_state.username:
        role_text = st.session_state.user_role.capitalize() if st.session_state.user_role else "User"
        st.markdown(
            f'<div class="subtitle">Welcome, {st.session_state.username} ({role_text})</div>', 
            unsafe_allow_html=True
        )

with col_right:
    if not st.session_state.logged_in:
        # Login/Signup buttons for non-logged users
        if st.button("Login", key="top_login"):
            st.session_state.auth_stage = "login"
            st.rerun()
        if st.button("Signup", key="top_signup"):
            st.session_state.auth_stage = "signup"
            st.rerun()
    else:
        # User profile popover
        with st.popover("👤"):
            st.write(f"**Name:** {st.session_state.username}")
            st.write(f"**Email:** {st.session_state.user_email}")
            st.write(f"**Role:** {st.session_state.user_role.capitalize() if st.session_state.user_role else 'User'}")
            
            # Theme toggle
            theme_icon = "🌙" if st.session_state.theme == "light" else "☀️"
            theme_text = "Dark Mode" if st.session_state.theme == "light" else "Light Mode"
            
            if st.button(f"{theme_icon} {theme_text}"):
                toggle_theme()
            
            st.divider()
            
            # Logout button
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.user_email = None
                st.session_state.user_role = None
                st.session_state.username = None
                st.session_state.auth_stage = None
                st.session_state.current_page = PAGE_HOME
                reset_assessment_state()
                st.rerun()

st.divider()

# ============================================================================
# AUTHENTICATION SECTION
# ============================================================================
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

# ============================================================================
# PAGE ROUTING
# ============================================================================
elif st.session_state.current_page == PAGE_HOME and not st.session_state.auth_stage:
    # HOME PAGE
    if not st.session_state.logged_in:
        render_landing_page()
    elif st.session_state.user_role == "teacher":
        render_teacher_home()
    else:
        render_student_home()

elif st.session_state.current_page == PAGE_TEACHER_DASHBOARD:
    # TEACHER DASHBOARD
    render_teacher_dashboard()

elif st.session_state.current_page == PAGE_ASSESSMENT:
    # STUDENT ASSESSMENT
    render_assessment_page()

elif st.session_state.current_page == PAGE_RESULTS:
    # STUDENT RESULTS
    render_student_results()

elif st.session_state.current_page == PAGE_STUDENT_RESULTS:
    # TEACHER VIEW OF STUDENT RESULTS
    render_teacher_student_results()

elif st.session_state.current_page == PAGE_ANALYTICS:
    # ANALYTICS DASHBOARD
    render_analytics_dashboard()

elif st.session_state.current_page == PAGE_LEARN:
    # LEARNING CENTER
    render_learn_page()