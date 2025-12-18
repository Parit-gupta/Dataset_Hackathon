"""
Teacher Dashboard - Create and Manage Assessments
Updated with Word Pronunciation Assessment
"""

import streamlit as st
from datetime import datetime
from utils import (
    load_assessments, 
    save_assessments, 
    navigate_to,
    generate_assessment_id
)
from config import (
    ASSESSMENT_TYPE_WORD_PRONUNCIATION,
    ASSESSMENT_TYPE_IMAGE,
    ASSESSMENT_TYPE_FILLBLANK
)


def render_teacher_dashboard():
    """Main teacher dashboard"""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 👨‍🏫 TEACHER DASHBOARD")
    st.markdown("---")
    
    # Dashboard tabs
    tab1, tab2, tab3 = st.tabs([
        "📝 Create Assessment", 
        "📋 My Assessments",
        "📊 Statistics"
    ])
    
    with tab1:
        render_create_assessment()
    
    with tab2:
        render_assessment_list()
    
    with tab3:
        render_teacher_stats()
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_create_assessment():
    """Create new assessment interface"""
    st.markdown("### 🎯 Create New Assessment")
    
    # Assessment type selection
    assessment_type = st.selectbox(
        "Assessment Type",
        [
            ASSESSMENT_TYPE_WORD_PRONUNCIATION,
            ASSESSMENT_TYPE_IMAGE,
            ASSESSMENT_TYPE_FILLBLANK
        ],
        format_func=lambda x: {
            ASSESSMENT_TYPE_WORD_PRONUNCIATION: "🗣️ Word Pronunciation",
            ASSESSMENT_TYPE_IMAGE: "🖼️ Image Description",
            ASSESSMENT_TYPE_FILLBLANK: "✍️ Fill in the Blank"
        }[x]
    )
    
    st.markdown("---")
    
    # Render appropriate form based on type
    if assessment_type == ASSESSMENT_TYPE_WORD_PRONUNCIATION:
        render_word_pronunciation_form()
    elif assessment_type == ASSESSMENT_TYPE_IMAGE:
        render_image_assessment_form()
    elif assessment_type == ASSESSMENT_TYPE_FILLBLANK:
        render_fillblank_form()


def render_word_pronunciation_form():
    """Form for creating word pronunciation assessment"""
    st.markdown("### 🗣️ Word Pronunciation Assessment")
    st.info("💡 Students will pronounce specific words. Perfect for vocabulary and pronunciation practice!")
    
    with st.form("word_pronunciation_form"):
        # Basic details
        topic = st.text_input(
            "Topic/Title *",
            placeholder="e.g., Basic English Vocabulary, Medical Terms, etc.",
            help="Give your assessment a descriptive name"
        )
        
        difficulty = st.select_slider(
            "Difficulty Level",
            options=["Easy", "Medium", "Hard"],
            value="Medium"
        )
        
        language = st.selectbox(
            "Language",
            ["English", "Tamil", "Hindi", "Spanish", "French", "German"],
            help="Language of the words to be pronounced"
        )
        
        st.markdown("---")
        st.markdown("### 📝 Add Words")
        st.caption("Add words that students need to pronounce. You can add example sentences for context.")
        
        # Number of words
        num_words = st.number_input(
            "Number of words",
            min_value=1,
            max_value=20,
            value=5,
            help="How many words in this assessment?"
        )
        
        words_data = []
        
        for i in range(num_words):
            st.markdown(f"#### Word {i+1}")
            col1, col2 = st.columns([2, 3])
            
            with col1:
                word = st.text_input(
                    f"Word {i+1} *",
                    key=f"word_{i}",
                    placeholder="e.g., beautiful, pronunciation, etc."
                )
            
            with col2:
                example = st.text_input(
                    f"Example Sentence (optional)",
                    key=f"example_{i}",
                    placeholder="e.g., The sunset was beautiful"
                )
            
            phonetic = st.text_input(
                f"Phonetic (optional)",
                key=f"phonetic_{i}",
                placeholder="e.g., /bjuːtɪfl/ for beautiful",
                help="Add phonetic spelling to help students"
            )
            
            if word:
                words_data.append({
                    "word": word.strip(),
                    "example": example.strip() if example else "",
                    "phonetic": phonetic.strip() if phonetic else ""
                })
            
            st.markdown("---")
        
        # Submit button
        submitted = st.form_submit_button("Create Assessment 🚀", type="primary")
        
        if submitted:
            # Validation
            if not topic:
                st.error("❌ Please provide a topic/title")
            elif len(words_data) == 0:
                st.error("❌ Please add at least one word")
            else:
                # Create assessment object
                assessment = {
                    "id": generate_assessment_id(),
                    "type": ASSESSMENT_TYPE_WORD_PRONUNCIATION,
                    "topic": topic,
                    "difficulty": difficulty,
                    "language": language,
                    "words": words_data,
                    "created_by": st.session_state.username,
                    "created_at": datetime.now().isoformat(),
                    "total_words": len(words_data)
                }
                
                # Save assessment
                assessments_data = load_assessments()
                assessments_data["assessments"].append(assessment)
                save_assessments(assessments_data)
                
                st.success("✅ Word Pronunciation Assessment created successfully!")
                st.balloons()
                st.rerun()


def render_image_assessment_form():
    """Form for creating image description assessment"""
    st.markdown("### 🖼️ Image Description Assessment")
    st.info("💡 Students will describe an image in their own words")
    
    with st.form("image_assessment_form"):
        topic = st.text_input(
            "Topic/Title *",
            placeholder="e.g., Describe the Scene, Animal Identification"
        )
        
        difficulty = st.select_slider(
            "Difficulty Level",
            options=["Easy", "Medium", "Hard"],
            value="Medium"
        )
        
        image_url = st.text_input(
            "Image URL *",
            placeholder="https://example.com/image.jpg",
            help="Paste a direct link to an image"
        )
        
        prompt = st.text_area(
            "Description Prompt *",
            placeholder="e.g., Describe what you see in this image. Include colors, objects, and actions.",
            help="Instructions for students on what to describe"
        )
        
        # Preview image
        if image_url:
            st.markdown("#### Image Preview")
            try:
                st.image(image_url, caption="Assessment Image", use_column_width=True)
            except:
                st.warning("⚠️ Could not load image preview")
        
        submitted = st.form_submit_button("Create Assessment 🚀", type="primary")
        
        if submitted:
            if not topic or not image_url or not prompt:
                st.error("❌ Please fill in all required fields")
            else:
                assessment = {
                    "id": generate_assessment_id(),
                    "type": ASSESSMENT_TYPE_IMAGE,
                    "topic": topic,
                    "difficulty": difficulty,
                    "image_url": image_url,
                    "prompt": prompt,
                    "created_by": st.session_state.username,
                    "created_at": datetime.now().isoformat()
                }
                
                assessments_data = load_assessments()
                assessments_data["assessments"].append(assessment)
                save_assessments(assessments_data)
                
                st.success("✅ Image Assessment created successfully!")
                st.balloons()
                st.rerun()


def render_fillblank_form():
    """Form for creating fill-in-blank assessment"""
    st.markdown("### ✍️ Fill in the Blank Assessment")
    st.info("💡 Students will speak the missing word in each sentence")
    
    with st.form("fillblank_form"):
        topic = st.text_input(
            "Topic/Title *",
            placeholder="e.g., Grammar Practice, Vocabulary Building"
        )
        
        difficulty = st.select_slider(
            "Difficulty Level",
            options=["Easy", "Medium", "Hard"],
            value="Medium"
        )
        
        st.markdown("---")
        st.markdown("### 📝 Add Sentences")
        st.caption("Use _____ (5 underscores) to mark the blank space")
        
        num_sentences = st.number_input(
            "Number of sentences",
            min_value=1,
            max_value=15,
            value=5
        )
        
        sentences_data = []
        
        for i in range(num_sentences):
            st.markdown(f"#### Sentence {i+1}")
            
            sentence = st.text_input(
                f"Sentence {i+1} *",
                key=f"sentence_{i}",
                placeholder="e.g., The cat is _____ on the mat",
                help="Use _____ to mark where the word goes"
            )
            
            blank_word = st.text_input(
                f"Missing Word {i+1} *",
                key=f"blank_{i}",
                placeholder="e.g., sitting"
            )
            
            if sentence and blank_word and "_____" in sentence:
                sentences_data.append({
                    "text": sentence.strip(),
                    "blank": blank_word.strip().lower()
                })
            elif sentence and blank_word:
                st.warning(f"⚠️ Sentence {i+1} must contain _____ (5 underscores)")
            
            st.markdown("---")
        
        submitted = st.form_submit_button("Create Assessment 🚀", type="primary")
        
        if submitted:
            if not topic:
                st.error("❌ Please provide a topic")
            elif len(sentences_data) == 0:
                st.error("❌ Please add at least one valid sentence with _____")
            else:
                assessment = {
                    "id": generate_assessment_id(),
                    "type": ASSESSMENT_TYPE_FILLBLANK,
                    "topic": topic,
                    "difficulty": difficulty,
                    "sentences": sentences_data,
                    "created_by": st.session_state.username,
                    "created_at": datetime.now().isoformat(),
                    "total_sentences": len(sentences_data)
                }
                
                assessments_data = load_assessments()
                assessments_data["assessments"].append(assessment)
                save_assessments(assessments_data)
                
                st.success("✅ Fill-in-Blank Assessment created successfully!")
                st.balloons()
                st.rerun()


def render_assessment_list():
    """Display list of teacher's assessments"""
    st.markdown("### 📚 Your Assessments")
    
    assessments_data = load_assessments()
    assessments = assessments_data.get("assessments", [])
    
    # Filter by current teacher
    my_assessments = [
        a for a in assessments 
        if a.get('created_by') == st.session_state.username
    ]
    
    if not my_assessments:
        st.info("📭 You haven't created any assessments yet")
        return
    
    type_icons = {
        ASSESSMENT_TYPE_WORD_PRONUNCIATION: "🗣️",
        ASSESSMENT_TYPE_IMAGE: "🖼️",
        ASSESSMENT_TYPE_FILLBLANK: "✍️"
    }
    
    for assessment in my_assessments:
        st.markdown('<div class="assessment-card">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            icon = type_icons.get(assessment['type'], "📝")
            st.markdown(f"**{icon} {assessment['topic']}**")
            st.caption(f"Difficulty: {assessment['difficulty']} | Created: {assessment['created_at'][:10]}")
            
            if assessment['type'] == ASSESSMENT_TYPE_WORD_PRONUNCIATION:
                st.caption(f"Words: {assessment.get('total_words', len(assessment.get('words', [])))} | Language: {assessment.get('language', 'English')}")
            elif assessment['type'] == ASSESSMENT_TYPE_FILLBLANK:
                st.caption(f"Sentences: {assessment.get('total_sentences', len(assessment.get('sentences', [])))}")
        
        with col2:
            if st.button("📊 View", key=f"view_{assessment['id']}"):
                st.session_state.viewing_assessment = assessment
                st.rerun()
        
        with col3:
            if st.button("🗑️ Delete", key=f"delete_{assessment['id']}"):
                assessments_data["assessments"] = [
                    a for a in assessments_data["assessments"] 
                    if a['id'] != assessment['id']
                ]
                save_assessments(assessments_data)
                st.success("✅ Assessment deleted")
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)


def render_teacher_stats():
    """Display teacher statistics"""
    st.markdown("### 📊 Your Statistics")
    
    assessments_data = load_assessments()
    assessments = assessments_data.get("assessments", [])
    
    my_assessments = [
        a for a in assessments 
        if a.get('created_by') == st.session_state.username
    ]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Assessments", len(my_assessments))
    
    with col2:
        word_count = sum(1 for a in my_assessments if a['type'] == ASSESSMENT_TYPE_WORD_PRONUNCIATION)
        st.metric("Word Pronunciation", word_count)
    
    with col3:
        fillblank_count = sum(1 for a in my_assessments if a['type'] == ASSESSMENT_TYPE_FILLBLANK)
        st.metric("Fill-in-Blank", fillblank_count)
    
    # Assessment breakdown
    st.markdown("---")
    st.markdown("#### Assessment Types")
    
    type_counts = {}
    for assessment in my_assessments:
        atype = assessment['type']
        type_counts[atype] = type_counts.get(atype, 0) + 1
    
    if type_counts:
        for atype, count in type_counts.items():
            type_name = {
                ASSESSMENT_TYPE_WORD_PRONUNCIATION: "🗣️ Word Pronunciation",
                ASSESSMENT_TYPE_IMAGE: "🖼️ Image Description",
                ASSESSMENT_TYPE_FILLBLANK: "✍️ Fill-in-Blank"
            }.get(atype, atype)
            
            st.progress(count / len(my_assessments))
            st.caption(f"{type_name}: {count} assessments")
    else:
        st.info("No data to display yet")