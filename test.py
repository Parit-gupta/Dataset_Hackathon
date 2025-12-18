from ai_app.assessments import assess_speech

result = assess_speech(
    assessment_id="a1",
    audio_path="ai_app/asr/sample2.mp3"
)

print(result)
