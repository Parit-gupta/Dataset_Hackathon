import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge")


def load_knowledge():
    """
    Load therapy & pronunciation knowledge as clean text chunks.
    Each paragraph / bullet becomes one retrievable unit.
    """

    texts = []

    files = [
        "common_errors.txt",
        "phoneme_rules.txt",
        "therapy_tips.txt"
    ]

    for fname in files:
        path = os.path.join(KNOWLEDGE_DIR, fname)

        if not os.path.exists(path):
            print(f"[RAG] Warning: Knowledge file missing -> {fname}")
            continue

        with open(path, encoding="utf-8") as f:
            content = f.read().strip()

            # Split into meaningful chunks (paragraph-based)
            chunks = [
                chunk.strip()
                for chunk in content.split("\n\n")
                if chunk.strip()
            ]

            texts.extend(chunks)

    return texts
