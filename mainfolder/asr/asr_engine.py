import sys
import whisper

# Load model once
model = whisper.load_model("base")

def transcribe_audio(audio_path: str) -> dict:
    result = model.transcribe(audio_path)

    return {
        "text": result["text"].strip().lower(),
        "language": result["language"],
        "timestamps": []
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_whisper_terminal.py <audio_file>")
        sys.exit(1)

    audio_file = sys.argv[1]
    output = transcribe_audio(audio_file)

    print("\n--- TRANSCRIPTION RESULT ---")
    print("Language:", output["language"])
    print("Text:", output["text"])
