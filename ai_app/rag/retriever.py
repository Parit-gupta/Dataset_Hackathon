from ai_app.rag.knowledge_loader import load_knowledge


def retrieve_context(assessment_result):
    """
    Retrieve targeted therapy & pronunciation knowledge
    based on detected errors.
    """

    # ===============================
    # SAFE SCORE HANDLING
    # ===============================
    word_score = assessment_result.get("word_score", 0)
    phoneme_score = assessment_result.get("phoneme_score")

    score = assessment_result.get(
        "score",
        round(
            0.6 * word_score +
            0.4 * (phoneme_score if phoneme_score is not None else 0),
            2
        )
    )

    # ===============================
    # SAFE ERROR EXTRACTION
    # ===============================
    errors = assessment_result.get("errors", {})

    text_errors = errors.get("text", {})
    phoneme_errors = errors.get("phonemes", {})

    missing_words = text_errors.get("missing_words", [])
    extra_words = text_errors.get("extra_words", [])

    missing_phonemes = phoneme_errors.get("missing_phonemes", [])
    extra_phonemes = phoneme_errors.get("extra_phonemes", [])

    knowledge = load_knowledge()
    selected = []

    # -------------------------------
    # WORD-LEVEL FEEDBACK
    # -------------------------------
    if missing_words:
        selected.append(
            f"Missing or unclear words: {', '.join(missing_words)}."
        )

    if extra_words:
        selected.append(
            f"Extra or mispronounced words: {', '.join(extra_words)}."
        )

    # -------------------------------
    # PHONEME-LEVEL FEEDBACK
    # -------------------------------
    if missing_phonemes:
        selected.append(
            f"Missing phoneme sounds: {', '.join(missing_phonemes)}."
        )

    if extra_phonemes:
        selected.append(
            f"Extra or distorted phoneme sounds: {', '.join(extra_phonemes)}."
        )

    # -------------------------------
    # SEVERITY-BASED GUIDANCE
    # -------------------------------
    if score < 60:
        selected.append(
            "Pronunciation accuracy is low. Focus on slow, isolated word practice."
        )
    elif score < 80:
        selected.append(
            "Moderate pronunciation issues detected. Controlled repetition is advised."
        )
    else:
        selected.append(
            "Pronunciation is mostly correct. Minor articulation refinement needed."
        )

    # -------------------------------
    # THERAPY KNOWLEDGE (LIMITED & RELEVANT)
    # -------------------------------
    therapy_count = 0
    MAX_THERAPY_POINTS = 1  # 👈 control output size

    for chunk in knowledge:
        chunk_l = chunk.lower()

        # Pick only highly relevant guidance
        if (
            ("phoneme" in chunk_l and missing_phonemes) or
            ("practice" in chunk_l) or
            ("skip" in chunk_l)
        ):
            selected.append(chunk)
            therapy_count += 1

        if therapy_count >= MAX_THERAPY_POINTS:
            break

    return selected[:4]
