"""
Configuration and Constants for GenAI Big Data Platform
"""

# ============================================================================
# PAGE NAMES
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
ASSESSMENT_TYPE_QA = "qa"
ASSESSMENT_TYPE_IMAGE = "image"
ASSESSMENT_TYPE_FILLBLANK = "fillblank"

ASSESSMENT_TYPES = {
    ASSESSMENT_TYPE_QA: {"icon": "💬", "name": "Q&A Assessment"},
    ASSESSMENT_TYPE_IMAGE: {"icon": "🖼️", "name": "Image Description"},
    ASSESSMENT_TYPE_FILLBLANK: {"icon": "✍️", "name": "Fill in the Blanks"}
}

# ============================================================================
# DIFFICULTY LEVELS
# ============================================================================
DIFFICULTY_BEGINNER = "Beginner"
DIFFICULTY_INTERMEDIATE = "Intermediate"
DIFFICULTY_ADVANCED = "Advanced"

DIFFICULTY_LEVELS = [DIFFICULTY_BEGINNER, DIFFICULTY_INTERMEDIATE, DIFFICULTY_ADVANCED]

# ============================================================================
# USER ROLES
# ============================================================================
ROLE_STUDENT = "student"
ROLE_TEACHER = "teacher"

# ============================================================================
# FILE PATHS
# ============================================================================
ASSESSMENTS_DIR = "assessments"
ASSESSMENTS_FILE = "assessments/assessments.json"

# ============================================================================
# AUDIO SETTINGS
# ============================================================================
AUDIO_SAMPLE_RATE = 16000
AUDIO_PAUSE_THRESHOLD = 2.0
AUDIO_FORMATS = ['wav', 'mp3', 'm4a']

# ============================================================================
# THEME SETTINGS
# ============================================================================
THEME_LIGHT = "light"
THEME_DARK = "dark"

# ============================================================================
# DEFAULT VALUES
# ============================================================================
DEFAULT_THEME = THEME_LIGHT
DEFAULT_QUESTIONS_COUNT = 5
DEFAULT_SENTENCES_COUNT = 5

# ============================================================================
# APP SETTINGS
# ============================================================================
APP_TITLE = "GenAI Big Data Platform"
APP_ICON = "📊"
APP_LAYOUT = "wide"