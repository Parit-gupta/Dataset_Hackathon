import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "assessments.json")


def load_tests():
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["tests"]


def get_test_by_id(test_id):
    tests = load_tests()
    return next(t for t in tests if t["test_id"] == test_id)


def get_question(test_id, question_id):
    test = get_test_by_id(test_id)
    return next(q for q in test["questions"] if q["question_id"] == question_id)
