from ai_app.rag.retriever import retrieve_context


def rag_chatbot(user_question, assessment_result):
    """
    Generate a focused, question-aware explanation
    using system analysis + retrieved therapy knowledge.
    """

    response = []

    # ---------------------------
    # SAFE ACCESS
    # ---------------------------
    word_score = assessment_result.get("word_score", 0)
    phoneme_score = assessment_result.get("phoneme_score")

    # Compute score safely if missing (defensive design)
    score = assessment_result.get(
        "score",
        round(
            0.6 * word_score +
            0.4 * (phoneme_score if phoneme_score is not None else 0),
            2
        )
    )

    user_q = user_question.lower()

    # ============================
    # 1️⃣ DIRECT ANSWER (QUESTION-AWARE)
    # ============================
    response.append("💡 Direct Answer:")

    if "why" in user_q:
        response.append(
            f"You lost marks because your spoken pronunciation did not fully "
            f"match the expected word and sound patterns. "
            f"Your overall score was {score}%."
        )

        response.append(
            f"Word accuracy: {word_score}%."
        )

        if phoneme_score is not None:
            response.append(
                f"Phoneme-level accuracy: {phoneme_score}%."
            )

    elif "improve" in user_q or "how" in user_q:
        response.append(
            "To improve your pronunciation, speak slowly, exaggerate mouth "
            "movements initially, and repeat the word while focusing on "
            "individual sounds."
        )

    else:
        response.append(
            "Your pronunciation attempt has been evaluated in detail below."
        )

    # ============================
    # 2️⃣ SYSTEM EXPLANATION (XAI)
    # ============================
    response.append("\n🧠 System Explanation:")
    response.append(assessment_result.get("explanation", "No explanation available."))

    # ============================
    # 3️⃣ RETRIEVED KNOWLEDGE (RAG)
    # ============================
    response.append("\n📚 Therapy Guidance:")

    retrieved = retrieve_context({
        **assessment_result,
        "score": score  # Ensure retriever always receives score
    })

    if retrieved:
        for item in retrieved:
            response.append(f"- {item}")
    else:
        response.append("- No specific therapy guidance required.")

    return "\n".join(response)
