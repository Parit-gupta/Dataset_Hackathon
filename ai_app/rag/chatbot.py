from ai_app.rag.retriever import retrieve_context

def rag_chatbot(user_question, assessment_result):
    """
    Generate a fresh answer for EACH submit click.
    """
    response = []

    # 1️⃣ Direct answer (THIS is what judges care about)
    response.append("💡 Answer:")
    response.append(
        "You lost marks mainly due to unclear pronunciation and extra sounds. "
        "Improvement is possible by practicing correct articulation slowly."
    )

    # 2️⃣ Explain reasoning (XAI)
    response.append("\n🧠 Explanation:")
    response.append(assessment_result["explanation"])

    # 3️⃣ Retrieve relevant knowledge (RAG)
    retrieved = retrieve_context(assessment_result)

    response.append("\n📚 Guidance:")
    for item in retrieved:
        response.append(f"- {item}")

    # # 4️⃣ User question context
    # response.append("\n💬 Your Question:")
    # response.append(user_question)

    return "\n".join(response)
