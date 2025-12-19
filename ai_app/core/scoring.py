import difflib
import re

# --------------------------------------------------
# TEXT NORMALIZATION
# --------------------------------------------------
def _normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


# --------------------------------------------------
# PHONEME NORMALIZATION
# --------------------------------------------------
def _normalize_phonemes(phonemes: str) -> list:
    return phonemes.lower().strip().split()


# --------------------------------------------------
# PHONEME APPROXIMATION (Fallback)
# --------------------------------------------------
def approximate_phonemes(text: str) -> list:
    """
    Approximate phonemes (language-agnostic fallback)
    Works reasonably for English / Hindi / Tamil
    """
    text = _normalize_text(text)

    replacements = {
        "th": "θ",
        "sh": "ʃ",
        "ch": "tʃ",
        "ph": "f",
        "bh": "bʱ",
        "dh": "d̪ʱ",
        "kh": "kʰ",
        "gh": "gʱ"
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    return list(text)


# --------------------------------------------------
# MAIN SCORING FUNCTION
# --------------------------------------------------
def score_text(
    expected_text: str,
    actual_text: str,
    expected_phonemes: str | None = None
) -> dict:

    # -------- WORD LEVEL --------
    expected_norm = _normalize_text(expected_text)
    actual_norm = _normalize_text(actual_text)

    word_matcher = difflib.SequenceMatcher(None, expected_norm, actual_norm)
    word_score = round(word_matcher.ratio() * 100, 2)

    expected_words = expected_norm.split()
    actual_words = actual_norm.split()

    missing_words = [w for w in expected_words if w not in actual_words]
    extra_words = [w for w in actual_words if w not in expected_words]

    # -------- PHONEME LEVEL --------
    phoneme_score = None
    phoneme_analysis = None

    if expected_phonemes:
        expected_ph = _normalize_phonemes(expected_phonemes)
        spoken_ph = approximate_phonemes(actual_text)

        ph_matcher = difflib.SequenceMatcher(None, expected_ph, spoken_ph)
        phoneme_score = round(ph_matcher.ratio() * 100, 2)

        missing_phonemes = [p for p in expected_ph if p not in spoken_ph]
        extra_phonemes = [p for p in spoken_ph if p not in expected_ph]

        phoneme_analysis = {
            "expected_phonemes": expected_ph,
            "spoken_phonemes": spoken_ph,
            "missing_phonemes": missing_phonemes,
            "extra_phonemes": extra_phonemes
        }

    return {
        "word_score": word_score,
        "phoneme_score": phoneme_score,
        "missing_words": missing_words,
        "extra_words": extra_words,
        "phoneme_analysis": phoneme_analysis
    }
