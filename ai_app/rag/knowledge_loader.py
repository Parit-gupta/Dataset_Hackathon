import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge")

def load_knowledge():
    texts = []
    for fname in ["common_errors.txt", "phoneme_rules.txt", "therapy_tips.txt"]:
        path = os.path.join(KNOWLEDGE_DIR, fname)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                texts.append(f.read().strip())
    return texts
