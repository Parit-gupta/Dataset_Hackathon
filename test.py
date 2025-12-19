from ai_app.assessments import assess_speech
from ai_app.rag import rag_chatbot

# 1️⃣ Choose an existing assessment ID from assessments.json
ASSESSMENT_ID = "a1"

# 2️⃣ Path to test audio file
AUDIO_PATH = "ai_app/asr/sample2.mp3"

# 3️⃣ Run assessment pipeline
print("\n--- RUNNING ASSESSMENT ---\n")

assessment_result = assess_speech(
    assessment_id=ASSESSMENT_ID,
    audio_path=AUDIO_PATH
)

print("Assessment Result:")
print(assessment_result)

# 4️⃣ Ask RAG chatbot a question
print("\n--- RAG CHATBOT RESPONSE ---\n")

question = "Why did I lose marks and how can I improve?"

rag_response = rag_chatbot(
    user_question=question,
    assessment_result=assessment_result
)

print(rag_response)
