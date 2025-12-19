"""
Persistent storage for assessment results
"""

import json
import os
from datetime import datetime

RESULTS_FILE = "data/results.json"


def _ensure_file():
    os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)
    if not os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "w", encoding="utf-8") as f:
            json.dump({"submissions": []}, f)


def load_results():
    _ensure_file()
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_result(result):
    _ensure_file()
    data = load_results()

    result["submitted_at"] = datetime.now().isoformat()
    data["submissions"].append(result)

    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
