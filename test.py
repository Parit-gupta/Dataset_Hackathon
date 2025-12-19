from ai_app.assessments.assess import assess_speech
from ai_app.rag.chatbot import rag_chatbot

# -----------------------------
# CONFIG
# -----------------------------
TEST_ID = "test3"          # English basic test
QUESTION_ID = "t3_q1"      # expected_text = "apple"
AUDIO_PATH = "apple.mp3"   # 👈 your audio file
USER_QUESTION = "Why did I lose marks and how can I improve?"

def main():
    print("\n=== AUDIO-BASED SPEECH ASSESSMENT ===\n")

    # 1️⃣ Run full assessment (ASR → scoring → explanation)
    assessment_result = assess_speech(
        test_id=TEST_ID,
        question_id=QUESTION_ID,
        audio_path=AUDIO_PATH
    )

    # 2️⃣ RAG chatbot response
    print("\n=== RAG CHATBOT RESPONSE ===\n")
    chatbot_response = rag_chatbot(
        user_question=USER_QUESTION,
        assessment_result=assessment_result
    )

    print(chatbot_response)

if __name__ == "__main__":
    main()
