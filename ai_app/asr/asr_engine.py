import whisper
import os
import tempfile
from pydub import AudioSegment
from datetime import datetime

# Load Whisper model once
MODEL_SIZE = "small"
model = whisper.load_model(MODEL_SIZE)

# Directory to save transcripts
TRANSCRIPT_DIR = "ai_app\\asr\\transcripts"
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)


def _convert_to_wav(audio_path: str) -> str:
    """Convert any audio format to mono 16kHz WAV."""
    audio = AudioSegment.from_file(audio_path)
    audio = audio.set_channels(1).set_frame_rate(16000)

    tmp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    audio.export(tmp_wav.name, format="wav")
    return tmp_wav.name


def _save_transcript(text: str, language: str, audio_path: str) -> str:
    base = os.path.splitext(os.path.basename(audio_path))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{base}_{language}_{timestamp}.txt"

    path = os.path.join(TRANSCRIPT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

    return path


def transcribe_audio(audio_path: str, language: str = None) -> dict:
    """
    Transcribe audio using Whisper.
    Auto-detect language if language=None.
    """

    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    wav_path = _convert_to_wav(audio_path)

    options = {
        "task": "transcribe",
        "fp16": False,
        "verbose": False
    }

    if language:
        options["language"] = language

    result = model.transcribe(wav_path, **options)
    os.remove(wav_path)

    text = result["text"].strip().lower()
    lang = result["language"]

    transcript_path = _save_transcript(text, lang, audio_path)

    return {
        "text": text,
        "language": lang,
        "transcript_path": transcript_path
    }


# -------- CLI TEST --------
if __name__ == "__main__":
    import sys

    audio_file = sys.argv[1] if len(sys.argv) > 1 else None
    lang = sys.argv[2] if len(sys.argv) > 2 else None

    if not audio_file:
        print("Usage: python asr_engine.py <audio_file> [language_code]")
        sys.exit(1)

    output = transcribe_audio(audio_file, lang)

    print("\n--- ASR OUTPUT ---")
    print("Language:", output["language"])
    print("Text:", output["text"])
    print("Saved at:", output["transcript_path"])
