from ai_app.asr import transcribe_audio
from ai_app.core import score_text

audio_path = "ai_app\\asr\\sample2.mp3"
expected_text = "ढांटा से टेस्टिंग में आपका स्वागत है"

asr_output = transcribe_audio(audio_path)
print("ASR OUTPUT:", asr_output)

score_output = score_text(expected_text, asr_output["text"])
print("SCORING OUTPUT:", score_output)
