import json
import os
import uuid

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "assessments.json")


def load_assessments():
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["assessments"]


def add_assessment(text, language, assessment_type, creator="therapist"):
    data = {"assessments": load_assessments()}

    new_assessment = {
        "id": str(uuid.uuid4())[:8],
        "created_by": creator,
        "type": assessment_type,   # word / sentence
        "text": text.strip(),
        "language": language
    }

    data["assessments"].append(new_assessment)

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return new_assessment
