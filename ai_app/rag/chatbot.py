from ai_app.rag.retriever import retrieve_context


def rag_chatbot(user_question, assessment_result):
    response = []

    # 1️⃣ Use system-generated explanation FIRST
    response.append("System Explanation:")
    response.append(assessment_result["explanation"])

    # 2️⃣ Add retrieved knowledge
    retrieved_context = retrieve_context(
        assessment_result["score"],
        assessment_result["errors"]["missing_words"],
        assessment_result["errors"]["extra_words"]
    )

    response.append("Additional Guidance:")
    for ctx in retrieved_context:
        response.append(ctx)

    # 3️⃣ User question
    response.append(f"Your question: {user_question}")
    response.append("You can ask more questions or try again.")

    return " ".join(response)
