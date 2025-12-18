"""
Student Assessment Page - Word Pronunciation with Whisper ASR Integration
"""

import streamlit as st
import os
import tempfile
from datetime import datetime
from audio_recorder_streamlit import audio_recorder
from utils import load_assessments, navigate_to
from config import (
    ASSESSMENT_TYPE_WORD_PRONUNCIATION,
    ASSESSMENT_TYPE_IMAGE,
    ASSESSMENT_TYPE_FILLBLANK,
    AUDIO_SAMPLE_RATE,
    AUDIO_PAUSE_THRESHOLD,
    PRONUNCIATION_EXACT_MATCH,
    PRONUNCIATION_CLOSE_MATCH,
    PRONUNCIATION_PARTIAL_MATCH,
    PRONUNCIATION_NO_MATCH
)

# Import your Whisper ASR engine
try:
    import sys
    sys.path.append('ai_app/asr')
    from asr_engine import transcribe_audio
    ASR_AVAILABLE = True
except ImportError:
    ASR_AVAILABLE = False
    st.warning("⚠️ ASR engine not available. Install: pip install openai-whisper")

# Directory for audio submissions
AUDIO_SUBMISSIONS_DIR = "audio_submissions"
os.makedirs(AUDIO_SUBMISSIONS_DIR, exist_ok=True)


def render_assessment_page():
    """Main assessment page for students"""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 🎤 TAKE ASSESSMENT")
    st.markdown("---")
    
    assessments_data = load_assessments()
    assessments = assessments_data.get("assessments", [])
    
    if not st.session_state.selected_assessment:
        display_assessment_list(assessments)
    else:
        render_selected_assessment(st.session_state.selected_assessment)
    
    st.markdown('</div>', unsafe_allow_html=True)


def display_assessment_list(assessments):
    """Display available assessments"""
    st.markdown("### 📋 Available Assessments")
    
    if not assessments:
        st.info("📭 No assessments available yet. Check back later!")
        return
    
    type_icons = {
        ASSESSMENT_TYPE_WORD_PRONUNCIATION: "🗣️",
        ASSESSMENT_TYPE_IMAGE: "🖼️",
        ASSESSMENT_TYPE_FILLBLANK: "✍️"
    }
    
    type_names = {
        ASSESSMENT_TYPE_WORD_PRONUNCIATION: "Word Pronunciation",
        ASSESSMENT_TYPE_IMAGE: "Image Description",
        ASSESSMENT_TYPE_FILLBLANK: "Fill-in-Blank"
    }
    
    for assessment in assessments:
        st.markdown('<div class="assessment-card">', unsafe_allow_html=True)
        col1, col2 = st.columns([4, 1])
        
        with col1:
            icon = type_icons.get(assessment['type'], "📝")
            type_name = type_names.get(assessment['type'], "Assessment")
            st.markdown(f"**{icon} {assessment['topic']}**")
            st.caption(f"Type: {type_name} | Difficulty: {assessment['difficulty']}")
            
            if assessment['type'] == ASSESSMENT_TYPE_WORD_PRONUNCIATION:
                st.caption(f"Words: {len(assessment.get('words', []))} | Language: {assessment.get('language', 'English')}")
            elif assessment['type'] == ASSESSMENT_TYPE_FILLBLANK:
                st.caption(f"Sentences: {len(assessment.get('sentences', []))}")
        
        with col2:
            if st.button("Start", key=f"start_{assessment['id']}"):
                st.session_state.selected_assessment = assessment
                st.session_state.current_question_index = 0
                st.session_state.question_responses = []
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)


def render_selected_assessment(assessment):
    """Render assessment based on type"""
    assessment_type = assessment['type']
    
    if assessment_type == ASSESSMENT_TYPE_WORD_PRONUNCIATION:
        render_word_pronunciation_assessment(assessment)
    elif assessment_type == ASSESSMENT_TYPE_IMAGE:
        render_image_assessment(assessment)
    elif assessment_type == ASSESSMENT_TYPE_FILLBLANK:
        render_fillblank_assessment(assessment)
    
    # Back button
    st.markdown("---")
    if st.button("← Choose Different Assessment"):
        st.session_state.selected_assessment = None
        st.session_state.current_question_index = 0
        st.session_state.question_responses = []
        st.rerun()


def save_audio_file(audio_input, audio_type, prefix="audio"):
    """Save audio and return filepath"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    username = st.session_state.get('username', 'unknown')
    filename = f"{username}_{prefix}_{timestamp}.wav"
    filepath = os.path.join(AUDIO_SUBMISSIONS_DIR, filename)
    
    if audio_type == "bytes":
        with open(filepath, 'wb') as f:
            f.write(audio_input)
    elif audio_type == "uploaded":
        with open(filepath, 'wb') as f:
            f.write(audio_input.read())
    
    return filepath


def evaluate_pronunciation(transcribed_text, expected_word):
    """
    Evaluate pronunciation accuracy by comparing transcribed text with expected word
    
    Returns:
        dict with score, accuracy, and feedback
    """
    transcribed = transcribed_text.lower().strip()
    expected = expected_word.lower().strip()
    
    # Exact match
    if transcribed == expected:
        return {
            'score': PRONUNCIATION_EXACT_MATCH,
            'accuracy': 100,
            'match_type': 'exact',
            'feedback': f"Perfect! You pronounced '{expected}' correctly! ✅"
        }
    
    # Check if expected word is in transcribed text
    if expected in transcribed.split():
        return {
            'score': PRONUNCIATION_CLOSE_MATCH,
            'accuracy': 85,
            'match_type': 'close',
            'feedback': f"Good! Word '{expected}' was recognized. Try to pronounce only the target word."
        }
    
    # Check phonetic similarity (basic)
    similarity = calculate_similarity(transcribed, expected)
    
    if similarity > 0.7:
        return {
            'score': PRONUNCIATION_PARTIAL_MATCH,
            'accuracy': 60,
            'match_type': 'partial',
            'feedback': f"Close! You said '{transcribed}', but we expected '{expected}'. Try again!"
        }
    else:
        return {
            'score': PRONUNCIATION_NO_MATCH,
            'accuracy': 30,
            'match_type': 'none',
            'feedback': f"Not quite. You said '{transcribed}', but we expected '{expected}'. Listen carefully and try again."
        }


def calculate_similarity(str1, str2):
    """Calculate basic string similarity (Levenshtein-like)"""
    if not str1 or not str2:
        return 0
    
    # Convert to sets of characters
    set1 = set(str1.lower())
    set2 = set(str2.lower())
    
    # Calculate Jaccard similarity
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    return intersection / union if union > 0 else 0


def process_audio_with_asr(audio_path, expected_word=None, language=None):
    """
    Process audio through Whisper ASR and evaluate
    """
    if not ASR_AVAILABLE:
        return {
            'success': False,
            'error': 'ASR engine not available',
            'score': 0,
            'accuracy': 0
        }
    
    try:
        # Transcribe with Whisper
        asr_result = transcribe_audio(audio_path, language)
        
        transcribed_text = asr_result['text']
        detected_language = asr_result['language']
        
        # Evaluate pronunciation if expected word provided
        if expected_word:
            evaluation = evaluate_pronunciation(transcribed_text, expected_word)
            
            return {
                'success': True,
                'text': transcribed_text,
                'expected': expected_word,
                'language': detected_language,
                'transcript_path': asr_result['transcript_path'],
                'score': evaluation['score'],
                'accuracy': evaluation['accuracy'],
                'match_type': evaluation['match_type'],
                'feedback': evaluation['feedback']
            }
        else:
            # No expected word (for image descriptions)
            return {
                'success': True,
                'text': transcribed_text,
                'language': detected_language,
                'transcript_path': asr_result['transcript_path'],
                'score': 85,
                'accuracy': 100,
                'feedback': "Audio transcribed successfully!"
            }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'score': 0,
            'accuracy': 0
        }


def render_word_pronunciation_assessment(assessment):
    """Render word pronunciation assessment"""
    st.markdown(f"### 🗣️ {assessment['topic']}")
    st.info(f"**Difficulty:** {assessment['difficulty']} | **Language:** {assessment.get('language', 'English')}")
    
    words = assessment.get('words', [])
    current_idx = st.session_state.current_question_index
    
    # Progress
    st.markdown(
        f'<div class="progress-indicator">Word {current_idx + 1} of {len(words)}</div>',
        unsafe_allow_html=True
    )
    st.progress((current_idx) / len(words))
    
    if current_idx < len(words):
        word_data = words[current_idx]
        word = word_data['word']
        example = word_data.get('example', '')
        phonetic = word_data.get('phonetic', '')
        
        # Display word card
        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="question-text" style="font-size: 2em; font-weight: bold; color: #2196F3;">{word}</div>', unsafe_allow_html=True)
        
        if phonetic:
            st.markdown(f'<p style="color: #666; font-style: italic;">Pronunciation: {phonetic}</p>', unsafe_allow_html=True)
        
        if example:
            st.markdown(f'<p style="color: #555;">📝 Example: <i>"{example}"</i></p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🎙️ Pronounce This Word")
        st.caption("💡 Speak clearly and pronounce only this word")
        
        # Audio input
        render_audio_input_for_word(current_idx, word_data, assessment)
    
    else:
        # All words completed
        st.success("✅ All words completed!")
        st.balloons()
        
        if st.button("Submit Assessment 🚀", type="primary"):
            with st.spinner("🔍 Calculating your final score..."):
                results = calculate_final_results(
                    st.session_state.question_responses,
                    assessment
                )
                st.session_state.assessment_results = results
                navigate_to("results")


def render_audio_input_for_word(index, word_data, assessment):
    """Render audio input for word pronunciation"""
    word = word_data['word']
    language = assessment.get('language', 'english').lower()
    
    # Map language names to codes
    lang_codes = {
        'english': 'en',
        'tamil': 'ta',
        'hindi': 'hi',
        'spanish': 'es',
        'french': 'fr',
        'german': 'de'
    }
    lang_code = lang_codes.get(language, None)
    
    tab1, tab2 = st.tabs(["🔴 Record Audio", "📁 Upload Audio"])
    
    with tab1:
        st.markdown('<div class="recording-option">', unsafe_allow_html=True)
        audio_bytes = audio_recorder(
            pause_threshold=AUDIO_PAUSE_THRESHOLD,
            sample_rate=AUDIO_SAMPLE_RATE,
            text="Click to record",
            recording_color="#e74c3c",
            neutral_color="#6aa84f",
            icon_name="microphone",
            icon_size="3x",
            key=f"recorder_word_{index}"
        )
        
        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")
            
            if st.button("Submit Pronunciation ✅", type="primary", key=f"submit_record_{index}"):
                with st.spinner("🔍 Analyzing your pronunciation with Whisper AI..."):
                    process_word_response(audio_bytes, "bytes", word_data, index, lang_code)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="recording-option">', unsafe_allow_html=True)
        audio_file = st.file_uploader(
            "Upload audio file",
            type=['wav', 'mp3', 'm4a'],
            key=f"upload_word_{index}"
        )
        
        if audio_file:
            st.audio(audio_file, format='audio/wav')
            
            if st.button("Submit Pronunciation ✅", type="primary", key=f"submit_upload_{index}"):
                with st.spinner("🔍 Analyzing your pronunciation with Whisper AI..."):
                    process_word_response(audio_file, "uploaded", word_data, index, lang_code)
        
        st.markdown('</div>', unsafe_allow_html=True)


def process_word_response(audio_input, audio_type, word_data, index, language):
    """Process word pronunciation with ASR"""
    word = word_data['word']
    
    # Save audio
    audio_path = save_audio_file(audio_input, audio_type, f"word_{index}_{word}")
    
    # Process with Whisper ASR
    asr_result = process_audio_with_asr(audio_path, word, language)
    
    if asr_result['success']:
        # Save response
        response_data = {
            'word': word,
            'audio_path': audio_path,
            'transcription': asr_result['text'],
            'expected': word,
            'language': asr_result.get('language', 'unknown'),
            'transcript_path': asr_result.get('transcript_path'),
            'score': asr_result['score'],
            'accuracy': asr_result['accuracy'],
            'match_type': asr_result.get('match_type', 'unknown'),
            'feedback': asr_result['feedback']
        }
        
        st.session_state.question_responses.append(response_data)
        
        # Show immediate feedback
        if asr_result['score'] >= 90:
            st.success(asr_result['feedback'])
        elif asr_result['score'] >= 60:
            st.info(asr_result['feedback'])
        else:
            st.warning(asr_result['feedback'])
        
        st.caption(f"🎯 You said: **{asr_result['text']}** | Expected: **{word}**")
        
        # Move to next word
        st.session_state.current_question_index += 1
        st.rerun()
    else:
        st.error(f"❌ Error: {asr_result.get('error', 'Could not process audio')}")


def render_image_assessment(assessment):
    """Render image description assessment"""
    st.markdown(f"### 🖼️ {assessment['topic']}")
    st.info(f"Difficulty: **{assessment['difficulty']}**")
    
    st.markdown("---")
    st.markdown("### 📷 Describe This Image")
    
    st.image(assessment['image_url'], use_column_width=True)
    st.markdown(f"**Prompt:** {assessment['prompt']}")
    
    st.markdown("---")
    st.markdown("### 🎙️ Record Your Description")
    
    render_simple_audio_input("image", assessment)


def render_fillblank_assessment(assessment):
    """Render fill-in-blank assessment"""
    st.markdown(f"### ✍️ {assessment['topic']}")
    st.info(f"Difficulty: **{assessment['difficulty']}**")
    
    sentences = assessment['sentences']
    current_idx = st.session_state.current_question_index
    
    st.markdown(
        f'<div class="progress-indicator">Sentence {current_idx + 1} of {len(sentences)}</div>',
        unsafe_allow_html=True
    )
    st.progress((current_idx) / len(sentences))
    
    if current_idx < len(sentences):
        sentence = sentences[current_idx]
        display_text = sentence['text'].replace("_____", '<span style="color: #2196F3; font-weight: bold;">_____</span>')
        
        st.markdown('<div class="sentence-card">', unsafe_allow_html=True)
        st.markdown(f'<p style="font-size: 1.3em;">{display_text}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🎙️ Speak the Missing Word")
        st.info(f"💡 Say the word: **{sentence['blank']}**")
        
        render_audio_input_for_fillblank(current_idx, sentence)
    else:
        st.success("✅ All sentences completed!")
        st.balloons()
        
        if st.button("Submit Assessment 🚀", type="primary"):
            with st.spinner("🔍 Calculating your final score..."):
                results = calculate_final_results(
                    st.session_state.question_responses,
                    assessment
                )
                st.session_state.assessment_results = results
                navigate_to("results")


def render_audio_input_for_fillblank(index, sentence):
    """Render audio input for fill-blank"""
    blank_word = sentence['blank']
    
    tab1, tab2 = st.tabs(["🔴 Record Audio", "📁 Upload Audio"])
    
    with tab1:
        audio_bytes = audio_recorder(
            pause_threshold=AUDIO_PAUSE_THRESHOLD,
            sample_rate=AUDIO_SAMPLE_RATE,
            text="Click to record",
            recording_color="#e74c3c",
            neutral_color="#6aa84f",
            icon_name="microphone",
            icon_size="3x",
            key=f"recorder_blank_{index}"
        )
        
        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")
            
            if st.button("Submit Answer ✅", type="primary", key=f"submit_blank_record_{index}"):
                with st.spinner("🔍 Analyzing with Whisper AI..."):
                    process_fillblank_response(audio_bytes, "bytes", sentence, index)
    
    with tab2:
        audio_file = st.file_uploader(
            "Upload audio file",
            type=['wav', 'mp3', 'm4a'],
            key=f"upload_blank_{index}"
        )
        
        if audio_file:
            st.audio(audio_file, format='audio/wav')
            
            if st.button("Submit Answer ✅", type="primary", key=f"submit_blank_upload_{index}"):
                with st.spinner("🔍 Analyzing with Whisper AI..."):
                    process_fillblank_response(audio_file, "uploaded", sentence, index)


def process_fillblank_response(audio_input, audio_type, sentence, index):
    """Process fill-blank response"""
    blank_word = sentence['blank']
    
    # Save audio
    audio_path = save_audio_file(audio_input, audio_type, f"blank_{index}")
    
    # Process with ASR
    asr_result = process_audio_with_asr(audio_path, blank_word)
    
    if asr_result['success']:
        response_data = {
            'sentence': sentence['text'],
            'expected': blank_word,
            'audio_path': audio_path,
            'transcription': asr_result['text'],
            'language': asr_result.get('language'),
            'transcript_path': asr_result.get('transcript_path'),
            'score': asr_result['score'],
            'accuracy': asr_result['accuracy'],
            'feedback': asr_result['feedback']
        }
        
        st.session_state.question_responses.append(response_data)
        
        # Show feedback
        if asr_result['score'] >= 90:
            st.success(asr_result['feedback'])
        elif asr_result['score'] >= 60:
            st.info(asr_result['feedback'])
        else:
            st.warning(asr_result['feedback'])
        
        st.caption(f"🎯 You said: **{asr_result['text']}** | Expected: **{blank_word}**")
        
        st.session_state.current_question_index += 1
        st.rerun()
    else:
        st.error(f"❌ Error: {asr_result.get('error')}")


def render_simple_audio_input(prefix, assessment):
    """Simple audio input for image descriptions"""
    tab1, tab2 = st.tabs(["🔴 Record Audio", "📁 Upload Audio"])
    
    with tab1:
        audio_bytes = audio_recorder(
            pause_threshold=AUDIO_PAUSE_THRESHOLD,
            sample_rate=AUDIO_SAMPLE_RATE,
            text="Click to record",
            recording_color="#e74c3c",
            neutral_color="#6aa84f",
            icon_name="microphone",
            icon_size="3x"
        )
        
        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")
            
            if st.button("Submit 🚀", type="primary"):
                with st.spinner("🔍 Processing..."):
                    audio_path = save_audio_file(audio_bytes, "bytes", prefix)
                    asr_result = process_audio_with_asr(audio_path)
                    
                    if asr_result['success']:
                        st.session_state.assessment_results = {
                            'score': asr_result['score'],
                            'transcription': asr_result['text'],
                            'language': asr_result.get('language'),
                            'feedback': asr_result['feedback'],
                            'assessment_topic': assessment['topic']
                        }
                        navigate_to("results")
    
    with tab2:
        audio_file = st.file_uploader("Upload audio", type=['wav', 'mp3', 'm4a'])
        
        if audio_file:
            st.audio(audio_file)
            
            if st.button("Submit 🚀", type="primary", key="upload_submit"):
                with st.spinner("🔍 Processing..."):
                    audio_path = save_audio_file(audio_file, "uploaded", prefix)
                    asr_result = process_audio_with_asr(audio_path)
                    
                    if asr_result['success']:
                        st.session_state.assessment_results = {
                            'score': asr_result['score'],
                            'transcription': asr_result['text'],
                            'language': asr_result.get('language'),
                            'feedback': asr_result['feedback'],
                            'assessment_topic': assessment['topic']
                        }
                        navigate_to("results")


def calculate_final_results(responses, assessment):
    """Calculate final scores"""
    if not responses:
        return {
            'score': 0,
            'accuracy': 0,
            'feedback': 'No responses recorded',
            'assessment_topic': assessment['topic'],
            'responses': []
        }
    
    total_score = sum(r.get('score', 0) for r in responses)
    total_accuracy = sum(r.get('accuracy', 0) for r in responses)
    
    avg_score = total_score / len(responses)
    avg_accuracy = total_accuracy / len(responses)
    
    # Generate feedback
    if avg_score >= 90:
        feedback = "🌟 Outstanding! Your pronunciation is excellent!"
    elif avg_score >= 75:
        feedback = "👍 Great job! Keep practicing to improve further."
    elif avg_score >= 60:
        feedback = "✅ Good effort! Focus on clarity and accuracy."
    else:
        feedback = "💪 Keep practicing! Listen to examples and try again."
    
    return {
        'score': round(avg_score, 2),
        'accuracy': round(avg_accuracy, 2),
        'feedback': feedback,
        'assessment_topic': assessment['topic'],
        'total_questions': len(responses),
        'responses': responses,
        'language': responses[0].get('language', 'unknown') if responses else 'unknown'
    }