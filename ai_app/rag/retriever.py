from ai_app.rag.knowledge_loader import load_knowledge

def retrieve_context(assessment_result):
    """
    Decide what knowledge is relevant for THIS submission.
    """
    score = assessment_result["score"]
    missing = assessment_result["errors"]["missing_words"]
    extra = assessment_result["errors"]["extra_words"]

    knowledge_chunks = load_knowledge()
    selected = []

    if missing:
        selected.append("Some words were unclear or missing.")

    if extra:
        selected.append("Some extra or mispronounced words were detected.")

    if score < 70:
        selected.append("Overall pronunciation accuracy needs improvement.")

    # Always add therapy tips
    selected.extend(knowledge_chunks)

    return selected
