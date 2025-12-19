def generate_explanation(
    expected_text: str,
    spoken_text: str,
    word_score: float,
    missing_words: list,
    extra_words: list,
    phoneme_score: float | None = None
):
    explanation = []

    # ----------------------------
    # BASIC CONTEXT
    # ----------------------------
    explanation.append(f"Expected phrase: {expected_text}.")
    explanation.append(f"You said: {spoken_text}.")

    # ----------------------------
    # WORD-LEVEL FEEDBACK (FIXED)
    # ----------------------------
    if word_score >= 80:
        explanation.append("Excellent pronunciation at the word level.")
    elif word_score >= 60:
        explanation.append("Good attempt, some word-level pronunciation issues detected.")
    else:
        explanation.append("Word-level pronunciation needs significant improvement.")

    if missing_words:
        explanation.append(
            f"Missing or unclear words: {', '.join(missing_words)}."
        )

    if extra_words:
        explanation.append(
            f"Extra or mispronounced words: {', '.join(extra_words)}."
        )

    # ----------------------------
    # PHONEME-LEVEL FEEDBACK
    # ----------------------------
    if phoneme_score is not None:
        if phoneme_score >= 80:
            explanation.append("Phoneme articulation is mostly correct.")
        elif phoneme_score >= 60:
            explanation.append("Some phoneme articulation issues were detected.")
        else:
            explanation.append("Significant phoneme-level articulation issues detected.")

        explanation.append(
            f"Phoneme accuracy score: {phoneme_score}%."
        )

    return " ".join(explanation)
