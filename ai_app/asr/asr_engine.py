import whisper
import os
import tempfile
from pydub import AudioSegment
from datetime import datetime

# ================================
# LOAD MODEL (ONCE)
# ================================
MODEL_SIZE = "small"
model = whisper.load_model(MODEL_SIZE)

# ================================
# TRANSCRIPT STORAGE
# ================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRANSCRIPT_DIR = os.path.join(BASE_DIR, "transcripts")
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)


# ================================
# AUDIO PREPROCESSING
# ================================
def _convert_to_wav(audio_path: str) -> str:
    """Convert audio to mono 16kHz WAV (Whisper standard)."""
    audio = AudioSegment.from_file(audio_path)
    audio = audio.set_channels(1).set_frame_rate(16000)

    tmp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    audio.export(tmp_wav.name, format="wav")
    return tmp_wav.name


# ================================
# SAVE TRANSCRIPT
# ================================
def _save_transcript(text: str, language: str, audio_path: str) -> str:
    base = os.path.splitext(os.path.basename(audio_path))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{base}_{language}_{timestamp}.txt"

    path = os.path.join(TRANSCRIPT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

    return path


# ================================
# MAIN ASR FUNCTION
# ================================
def transcribe_audio(audio_path: str, language: str | None = None) -> dict:
    """
    Transcribe audio using Whisper.
    Language is auto-detected if not provided.
    """

    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    wav_path = _convert_to_wav(audio_path)

    try:
        options = {
            "task": "transcribe",
            "fp16": False,
            "verbose": False
        }

        if language:
            options["language"] = language

        result = model.transcribe(wav_path, **options)

        text = result["text"].strip()
        detected_language = result["language"]

        transcript_path = _save_transcript(
            text=text,
            language=detected_language,
            audio_path=audio_path
        )

        return {
            "text": text,
            "language": detected_language,
            "transcript_path": transcript_path
        }

    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)


# ================================
# CLI TEST (OPTIONAL)
# ================================
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python asr_engine.py <audio_file> [language_code]")
        sys.exit(1)

    audio_file = sys.argv[1]
    lang = sys.argv[2] if len(sys.argv) > 2 else None

    output = transcribe_audio(audio_file, lang)

    print("\n--- ASR OUTPUT ---")
    print("Language:", output["language"])
    print("Text:", output["text"])
    print("Transcript saved at:", output["transcript_path"])
