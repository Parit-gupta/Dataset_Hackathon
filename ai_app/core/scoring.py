import difflib
import re


def _normalize_text(text: str) -> str:
    """Normalize text for fair comparison."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def score_text(expected: str, actual: str) -> dict:
    """
    Compare expected vs actual text and compute score + errors.
    """

    expected_norm = _normalize_text(expected)
    actual_norm = _normalize_text(actual)

    matcher = difflib.SequenceMatcher(None, expected_norm, actual_norm)
    score = round(matcher.ratio() * 100, 2)

    expected_words = expected_norm.split()
    actual_words = actual_norm.split()

    missing_words = [w for w in expected_words if w not in actual_words]
    extra_words = [w for w in actual_words if w not in expected_words]

    return {
        "score": score,
        "missing_words": missing_words,
        "extra_words": extra_words
    }
