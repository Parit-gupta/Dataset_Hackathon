from ai_app.asr import transcribe_audio
from ai_app.core import score_text
from ai_app.rag import generate_explanation
from ai_app.assessments.assessment_store import load_assessments


def assess_speech(assessment_id, audio_path):
    assessments = load_assessments()
    assessment = next(a for a in assessments if a["id"] == assessment_id)

    asr_out = transcribe_audio(audio_path, assessment["language"])
    spoken_text = asr_out["text"]

    scoring = score_text(assessment["text"], spoken_text)

    explanation = generate_explanation(
        assessment["text"],
        spoken_text,
        scoring["score"],
        scoring["missing_words"],
        scoring["extra_words"]
    )

    return {
        "assessment_id": assessment_id,
        "expected_text": assessment["text"],
        "spoken_text": spoken_text,
        "score": scoring["score"],
        "errors": scoring,
        "explanation": explanation
    }
