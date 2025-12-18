def generate_explanation(expected, spoken, score, missing_words, extra_words):
    explanation = []

    explanation.append(f"Expected phrase: {expected}")
    explanation.append(f"You said: {spoken}")

    if score >= 80:
        explanation.append("Excellent pronunciation.")
    elif score >= 60:
        explanation.append("Good attempt, some pronunciation issues detected.")
    else:
        explanation.append("Pronunciation needs significant improvement.")

    if missing_words:
        explanation.append(
            f"Missing or unclear words: {', '.join(missing_words)}"
        )

    if extra_words:
        explanation.append(
            f"Extra or mispronounced words: {', '.join(extra_words)}"
        )

    return " ".join(explanation)
