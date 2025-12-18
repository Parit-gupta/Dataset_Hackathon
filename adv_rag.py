import os
import numpy as np
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
from groq import Groq

# =========================
# CONFIG
# =========================
DATASET_PATH = os.path.join("dataset", "train.csv")
MAX_CHUNKS = 10000
TOP_K = 5

VECTOR_DIR = "vectorstore"
INDEX_PATH = os.path.join(VECTOR_DIR, "faiss.index")
CHUNKS_PATH = os.path.join(VECTOR_DIR, "chunks.npy")

os.makedirs(VECTOR_DIR, exist_ok=True)

# =========================
# GROQ API (TEMP – REMOVE BEFORE COMMIT)
# =========================
client = Groq(
    api_key="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"
)

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(
    DATASET_PATH,
    header=None,
    names=["label", "title", "review"],
    engine="python"
)

texts = (df["title"] + ". " + df["review"]).astype(str).tolist()

# =========================
# TEXT CHUNKING
# =========================
def chunk_text(texts, chunk_size=800, overlap=100):
    chunks = []
    for text in texts:
        words = text.split()
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
    return chunks

# =========================
# EMBEDDINGS + FAISS
# =========================
embedder = SentenceTransformer("all-MiniLM-L6-v2")

if os.path.exists(INDEX_PATH) and os.path.exists(CHUNKS_PATH):
    index = faiss.read_index(INDEX_PATH)
    chunks = np.load(CHUNKS_PATH, allow_pickle=True).tolist()
else:
    chunks = chunk_text(texts)[:MAX_CHUNKS]

    embeddings = embedder.encode(
        chunks,
        batch_size=128,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)
    np.save(CHUNKS_PATH, np.array(chunks, dtype=object))

# =========================
# RETRIEVAL
# =========================
def retrieve_chunks(query, top_k=TOP_K):
    query_vec = embedder.encode([query], normalize_embeddings=True)
    _, indices = index.search(query_vec, top_k)
    return [chunks[i] for i in indices[0]]

# =========================
# RAG ANSWER
# =========================
def generate_answer(query, context_chunks):
    context = "\n\n".join(context_chunks)

    prompt = f"""
You are a helpful assistant.

Use the context below when relevant.
If the context is insufficient, use general knowledge.

Context:
{context}

Question:
{query}

Answer clearly and naturally.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content

# =========================
# SIMPLE XAI (NO EXTRA LLM)
# =========================
def extract_key_drivers(context_chunks):
    text = " ".join(context_chunks).lower()

    drivers = []
    if "condition" in text:
        drivers.append("book condition")
    if "shipping" in text or "delivery" in text:
        drivers.append("shipping experience")
    if "price" in text or "value" in text:
        drivers.append("price/value")
    if "author" in text or "writer" in text:
        drivers.append("author quality")

    if not drivers:
        drivers.append("semantic similarity to the question")

    return drivers[:3]

def xai_explanation(drivers):
    return "Answer based mainly on: " + ", ".join(drivers)

# =========================
# CONFIDENCE
# =========================
def confidence_score(context_chunks):
    return round(min(len(context_chunks) * 0.15, 1.0), 2)

# =========================
# INTERACTIVE LOOP
# =========================
if __name__ == "__main__":
    print("RAG system ready. Type 'exit' to quit.\n")

    while True:
        query = input("Question: ").strip()

        if query.lower() in ["exit", "quit"]:
            break

        context_chunks = retrieve_chunks(query)
        answer = generate_answer(query, context_chunks)
        drivers = extract_key_drivers(context_chunks)
        explanation = xai_explanation(drivers)
        confidence = confidence_score(context_chunks)

        print("\nAnswer:\n", answer)
        print("\nWhy:", explanation)
        print("Confidence:", confidence)
        print("\n" + "-" * 60 + "\n")
