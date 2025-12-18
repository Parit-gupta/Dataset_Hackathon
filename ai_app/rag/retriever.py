from ai_app.rag.knowledge_base import PRONUNCIATION_KB


def retrieve_context(score, missing, extra):
    context = []

    if score < 60:
        context.append("low_score")

    if missing:
        context.append("missing_words")

    if extra:
        context.append("extra_words")

    context.append("improvement")

    return [
        item["content"]
        for item in PRONUNCIATION_KB
        if item["topic"] in context
    ]
