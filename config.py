"""
Configuration File for GenAI Big Data Platform
Contains all constants and settings
"""

# ============================================================================
# APPLICATION SETTINGS
# ============================================================================
APP_TITLE = "GenAI Big Data Platform"
APP_ICON = "📊"
APP_LAYOUT = "wide"

# ============================================================================
# PAGE CONSTANTS
# ============================================================================
PAGE_HOME = "home"
PAGE_ASSESSMENT = "assessment"
PAGE_TEACHER_DASHBOARD = "teacher_dashboard"
PAGE_RESULTS = "results"
PAGE_LEARN = "learn"
PAGE_STUDENT_RESULTS = "student_results"
PAGE_ANALYTICS = "analytics"

# ============================================================================
# ASSESSMENT TYPES
# ============================================================================
ASSESSMENT_TYPE_WORD_PRONUNCIATION = "word_pronunciation"
ASSESSMENT_TYPE_IMAGE = "image_description"
ASSESSMENT_TYPE_FILLBLANK = "fill_blank"

# ============================================================================
# AUDIO SETTINGS
# ============================================================================
AUDIO_SAMPLE_RATE = 16000
AUDIO_PAUSE_THRESHOLD = 2.0
AUDIO_MAX_DURATION = 60  # seconds

# ============================================================================
# FILE PATHS
# ============================================================================
ASSESSMENTS_DIR = "assessments"
ASSESSMENTS_FILE = "assessments/assessments.json"
USERS_FILE = "users.json"
AUDIO_SUBMISSIONS_DIR = "audio_submissions"

# ============================================================================
# THEME SETTINGS
# ============================================================================
THEME_LIGHT = "light"
THEME_DARK = "dark"
DEFAULT_THEME = THEME_LIGHT

# ============================================================================
# SCORING SETTINGS
# ============================================================================
MIN_PASS_SCORE = 60
EXCELLENT_SCORE = 90
GOOD_SCORE = 75

# ============================================================================
# PRONUNCIATION SCORING THRESHOLDS
# ============================================================================
PRONUNCIATION_EXACT_MATCH = 100
PRONUNCIATION_CLOSE_MATCH = 85
PRONUNCIATION_PARTIAL_MATCH = 60
PRONUNCIATION_NO_MATCH = 30

# ============================================================================
# UI CONSTANTS
# ============================================================================
MAX_WORDS_PER_ASSESSMENT = 20
MAX_SENTENCES_PER_ASSESSMENT = 15
MIN_ASSESSMENT_ITEMS = 1