from ai_app.asr import transcribe_audio
from ai_app.core.scoring import score_text
from ai_app.rag import generate_explanation
from ai_app.assessments.assessment_store import get_question


def assess_speech(test_id, question_id, audio_path):
    # 1️⃣ Load question
    question = get_question(test_id, question_id)

    expected_text = question["expected_text"]
    expected_phonemes = question.get("expected_phonemes")

    # 2️⃣ ASR
    asr_out = transcribe_audio(audio_path)
    spoken_text = asr_out["text"]

    # 3️⃣ Scoring (WORD + PHONEME)
    score_result = score_text(
        expected_text=expected_text,
        actual_text=spoken_text,
        expected_phonemes=expected_phonemes
    )

    word_score = score_result["word_score"]
    phoneme_score = score_result["phoneme_score"]

    # 4️⃣ FINAL COMBINED SCORE (🔥 FIX FOR RAG)
    final_score = round(
        0.6 * word_score + 0.4 * phoneme_score, 2
    )

    # 5️⃣ Explanation (XAI + RAG)
    explanation = generate_explanation(
        expected_text=expected_text,
        spoken_text=spoken_text,
        word_score=word_score,
        missing_words=score_result["missing_words"],
        extra_words=score_result["extra_words"],
        phoneme_score=phoneme_score
    )


    # 6️⃣ FINAL STRUCTURED OUTPUT (STANDARDIZED)
    return {
        "test_id": test_id,
        "question_id": question_id,

        "expected_text": expected_text,
        "expected_phonemes": expected_phonemes,
        "spoken_text": spoken_text,

        "score": final_score,                 # ✅ REQUIRED BY RAG
        "word_score": word_score,
        "phoneme_score": phoneme_score,

        "errors": {
            "text": {
                "missing_words": score_result["missing_words"],
                "extra_words": score_result["extra_words"]
            },
            "phonemes": score_result["phoneme_analysis"]
        },

        "explanation": explanation
    }
