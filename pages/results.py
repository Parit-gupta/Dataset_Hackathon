"""
Results Page - Display Assessment Results
Updated for Word Pronunciation Assessment
"""

import streamlit as st
from utils import navigate_to, get_performance_emoji, get_grade_from_score
from config import PAGE_HOME


def render_student_results():
    """Display student assessment results"""
    
    if not st.session_state.assessment_results:
        st.warning("⚠️ No results to display")
        if st.button("← Back to Home"):
            navigate_to(PAGE_HOME)
        return
    
    results = st.session_state.assessment_results
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 🎉 Assessment Results")
    st.markdown("---")
    
    # Check if there's an error
    if 'error' in results:
        st.error(f"❌ {results['error']}")
        if st.button("← Back to Assessments"):
            navigate_to("assessment")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Topic
    st.markdown(f"### 📚 {results.get('assessment_topic', 'Assessment')}")
    
    # Overall metrics
    score = results.get('score', 0)
    accuracy = results.get('accuracy', 0)
    
    emoji = get_performance_emoji(score)
    grade = get_grade_from_score(score)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Overall Score", f"{score}%", delta=None)
    
    with col2:
        st.metric("Accuracy", f"{accuracy}%")
    
    with col3:
        st.metric("Grade", f"{grade} {emoji}")
    
    # Language detected (if available)
    if 'language' in results:
        st.info(f"🌍 Language Detected: **{results['language'].upper()}**")
    
    # Feedback
    st.markdown("---")
    st.markdown("### 💬 Feedback")
    feedback = results.get('feedback', 'Great job!')
    
    if score >= 90:
        st.success(feedback)
    elif score >= 70:
        st.info(feedback)
    elif score >= 60:
        st.warning(feedback)
    else:
        st.error(feedback)
    
    # Detailed responses (for word pronunciation and fill-blank)
    responses = results.get('responses', [])
    
    if responses:
        st.markdown("---")
        st.markdown("### 📋 Detailed Results")
        
        total_questions = results.get('total_questions', len(responses))
        st.caption(f"Total Items: {total_questions}")
        
        for i, response in enumerate(responses):
            render_response_detail(i + 1, response)
    
    # Single transcription (for image description)
    elif 'transcription' in results:
        st.markdown("---")
        st.markdown("### 📝 Your Response")
        st.info(results['transcription'])
    
    # Action buttons
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state.assessment_results = None
            navigate_to(PAGE_HOME)
    
    with col2:
        if st.button("🔄 Take Another Assessment", use_container_width=True):
            st.session_state.assessment_results = None
            st.session_state.selected_assessment = None
            navigate_to("assessment")
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_response_detail(index, response):
    """Render individual response details"""
    
    # Determine response type
    if 'word' in response:
        # Word pronunciation response
        render_word_response(index, response)
    elif 'sentence' in response:
        # Fill-in-blank response
        render_fillblank_response(index, response)
    elif 'question' in response:
        # Q&A response (legacy support)
        render_qa_response(index, response)


def render_word_response(index, response):
    """Render word pronunciation response"""
    word = response.get('word', '')
    transcription = response.get('transcription', '')
    expected = response.get('expected', word)
    score = response.get('score', 0)
    accuracy = response.get('accuracy', 0)
    match_type = response.get('match_type', 'unknown')
    feedback = response.get('feedback', '')
    
    # Determine color based on score
    if score >= 90:
        color = "#4CAF50"  # Green
        icon = "✅"
    elif score >= 70:
        color = "#FFC107"  # Yellow
        icon = "🟡"
    elif score >= 50:
        color = "#FF9800"  # Orange
        icon = "🟠"
    else:
        color = "#F44336"  # Red
        icon = "❌"
    
    st.markdown(f"""
    <div style="border-left: 4px solid {color}; padding: 10px; margin: 10px 0; background-color: rgba(0,0,0,0.02); border-radius: 5px;">
        <strong>{icon} Word {index}: {word}</strong><br>
        <span style="color: #666;">Your pronunciation: <strong>{transcription}</strong></span><br>
        <span style="color: #666;">Expected: <strong>{expected}</strong></span><br>
        <span style="color: {color};">Score: <strong>{score}%</strong> | Accuracy: <strong>{accuracy}%</strong></span><br>
        <em style="color: #555;">{feedback}</em>
    </div>
    """, unsafe_allow_html=True)


def render_fillblank_response(index, response):
    """Render fill-in-blank response"""
    sentence = response.get('sentence', '')
    transcription = response.get('transcription', '')
    expected = response.get('expected', '')
    score = response.get('score', 0)
    accuracy = response.get('accuracy', 0)
    feedback = response.get('feedback', '')
    
    # Determine color based on score
    if score >= 90:
        color = "#4CAF50"
        icon = "✅"
    elif score >= 70:
        color = "#FFC107"
        icon = "🟡"
    elif score >= 50:
        color = "#FF9800"
        icon = "🟠"
    else:
        color = "#F44336"
        icon = "❌"
    
    st.markdown(f"""
    <div style="border-left: 4px solid {color}; padding: 10px; margin: 10px 0; background-color: rgba(0,0,0,0.02); border-radius: 5px;">
        <strong>{icon} Sentence {index}</strong><br>
        <span style="color: #666;">{sentence}</span><br>
        <span style="color: #666;">You said: <strong>{transcription}</strong></span><br>
        <span style="color: #666;">Expected: <strong>{expected}</strong></span><br>
        <span style="color: {color};">Score: <strong>{score}%</strong> | Accuracy: <strong>{accuracy}%</strong></span><br>
        <em style="color: #555;">{feedback}</em>
    </div>
    """, unsafe_allow_html=True)


def render_qa_response(index, response):
    """Render Q&A response (legacy support)"""
    question = response.get('question', '')
    transcription = response.get('transcription', '')
    score = response.get('score', 85)
    
    st.markdown(f"""
    <div style="border-left: 4px solid #2196F3; padding: 10px; margin: 10px 0; background-color: rgba(0,0,0,0.02); border-radius: 5px;">
        <strong>❓ Question {index}</strong><br>
        <span style="color: #666;">{question}</span><br>
        <strong>Your Answer:</strong><br>
        <span style="color: #333;">{transcription}</span><br>
        <span style="color: #2196F3;">Score: <strong>{score}%</strong></span>
    </div>
    """, unsafe_allow_html=True)


def render_teacher_student_results():
    """Display student results for teachers"""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 📊 Student Results")
    st.markdown("---")
    
    st.info("👨‍🏫 Teacher view of student results coming soon!")
    st.caption("This feature will allow teachers to view all student submissions and track progress.")
    
    if st.button("← Back to Dashboard"):
        navigate_to("teacher_dashboard")
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_analytics_dashboard():
    """Display analytics dashboard"""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 📈 Analytics Dashboard")
    st.markdown("---")
    
    st.info("📊 Advanced analytics and insights coming soon!")
    st.caption("Features will include:")
    st.markdown("""
    - Student performance trends
    - Assessment difficulty analysis
    - Common pronunciation mistakes
    - Learning progress tracking
    - Comparative statistics
    """)
    
    if st.button("← Back to Home"):
        navigate_to(PAGE_HOME)
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_learn_page():
    """Display learning resources"""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 📚 Learning Center")
    st.markdown("---")
    
    st.markdown("### 🎯 Tips for Better Pronunciation")
    
    st.markdown("""
    #### 1. Speak Clearly 🗣️
    - Take your time
    - Enunciate each syllable
    - Don't rush
    
    #### 2. Practice Regularly 📅
    - Daily practice helps
    - Repeat difficult words
    - Record yourself
    
    #### 3. Listen Carefully 👂
    - Pay attention to native speakers
    - Use phonetic guides
    - Watch pronunciation videos
    
    #### 4. Use the Feedback 💡
    - Review your mistakes
    - Focus on problem areas
    - Track your progress
    
    #### 5. Environment Matters 🎤
    - Find a quiet place
    - Use a good microphone
    - Minimize background noise
    """)
    
    st.markdown("---")
    st.markdown("### 🌟 Resources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Pronunciation Guides:**
        - IPA (International Phonetic Alphabet)
        - Online dictionaries with audio
        - Language learning apps
        """)
    
    with col2:
        st.markdown("""
        **Practice Tools:**
        - Audio recording apps
        - Speech recognition software
        - Language exchange partners
        """)
    
    st.markdown("---")
    
    if st.button("← Back to Home"):
        navigate_to(PAGE_HOME)
    
    st.markdown('</div>', unsafe_allow_html=True)