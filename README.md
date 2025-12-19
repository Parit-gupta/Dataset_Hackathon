📌 Overview

This project is a multilingual speech-language assessment platform designed for pronunciation practice and automated assessment.
It combines Automatic Speech Recognition (ASR), rule-based scoring, and Explainable AI (RAG) to deliver transparent, clinician-aligned feedback rather than black-box scores.

The system supports mentor-authored assessments, automated transcription, phoneme-level evaluation, and AI-generated explainable summaries, closely mirroring real speech-therapy workflows.

🎯 Problem Statement

⦁	Build a Multilingual Speech-Language Assessment Platform with:
⦁	Assessment authoring tools
⦁	Automated ASR scoring
⦁	Explainable documentation (SOAP-style summaries)
⦁	Indian language readiness

✅ Our Solution

⦁	Mentor-authored, topic-based pronunciation assessments
⦁	Automated speech-to-text using Whisper ASR
⦁	Rule-based, auditable pronunciation scoring
⦁	Explainable AI (RAG) for learner-friendly summaries
⦁	English assessment with Hindi ASR proof-of-concept
⦁	Modular and scalable architecture

⭐ Key Features

Explainable Pronunciation Assessment
Phoneme-level error detection with clear explanations

Transparent Rule-Based Scoring
Deterministic and auditable (no black-box ML decisions)

Responsible Generative AI (RAG)
Used only for summaries & SOAP-style feedback

Mentor-Authored Assessments
JSON-based assessment authoring, no coding required

Multilingual-Ready Design
Easily extendable to Indian languages

🧠 System Architecture (High Level)
UI (Streamlit Pages)
        ↓
Audio Submission
        ↓
ASR (Whisper)
        ↓
Rule-Based Scoring
        ↓
RAG-Based Explanation
        ↓
Results & Summaries

🗂️ Repository Structure
ai_app/
│
├── asr/                     # ASR logic (Whisper)
├── assessments/             # Assessment handling & storage
├── core/                    # Rule-based scoring logic
├── rag/                     # RAG pipeline & explainable summaries
├── utils/                   # Helper utilities
│
assessments/                 # Global assessment definitions
audio_submissions/           # User-submitted audio
pages/                       # Streamlit UI pages
app.py                       # Main application entry point

🔁 Workflow (End-to-End)

1.	Mentor defines assessments in assessments.json
2.	User selects an assessment via UI
3.	User records or uploads speech
4.	Whisper ASR transcribes audio
5.	Rule-based engine evaluates pronunciation
6.	RAG module generates explainable summary
7.	Results are displayed to the user

🤖 Explainable AI (RAG)

Used only for explanation and documentation
Retrieves pronunciation rules and therapy guidance
Produces grounded, non-hallucinated summaries
Not used for ASR or scoring decisions

🛠️ Tech Stack

UI: Streamlit
ASR: OpenAI Whisper
Scoring: Rule-based phoneme analysis
Explainable AI: RAG + LLM
Data: JSON, local storage
Language Support: English (full), Hindi (PoC)

👥 Team Contributions

Satyanarayana Karthikeya Kuna
⦁	Designed and implemented the RAG pipeline
⦁	Built explainable summary generation and retrieval logic
⦁	Structured pronunciation knowledge base

Chaitanya Singh
⦁	Co-developed RAG and Explainable AI components
⦁	Worked on explanation logic and LLM integration
⦁	Helped align summaries with clinical documentation style

Parit Gupta
⦁	Implemented Automatic Speech Recognition (ASR) using Whisper
⦁	Handled audio preprocessing and transcription pipeline
⦁	Enabled multilingual ASR proof-of-concept
⦁	Handled GitHub commits
⦁	Helped in RAG pipeline

Keshav Sharma
⦁	Developed the web UI using Streamlit
⦁	Integrated ASR, scoring, and RAG modules
⦁	Built student assessment and teacher dashboard flows

🚀 How to Run

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py

(Ensure FFmpeg is installed and available in PATH.)

🔮 Future Scope

⦁	Full multi-language pronunciation assessment
⦁	Accent-aware ASR fine-tuning
⦁	Sentence & image-based assessments
⦁	Therapist & parent dashboards
⦁	Teletherapy and home-practice integration

📌 Final Note

This prototype emphasizes explainability, transparency, and clinical relevance, with a modular design that can evolve into a full-scale multilingual speech-therapy platform.
