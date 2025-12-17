import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer
from openai import OpenAI

client = OpenAI(api_key="YOUR_OPENAI_KEY")

embedder = SentenceTransformer("all-MiniLM-L6-v2")

index = None
documents = []

def build_vector_store(df):
    global index, documents

    documents = df.astype(str).apply(" | ".join, axis=1).tolist()
    embeddings = embedder.encode(documents)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

def ask_question(question, top_k=5):
    q_emb = embedder.encode([question])
    _, idx = index.search(q_emb, top_k)

    context = "\n".join([documents[i] for i in idx[0]])

    prompt = f"""
    Use the following dataset to answer the question.

    Data:
    {context}

    Question:
    {question}

    Answer clearly in simple terms.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content
