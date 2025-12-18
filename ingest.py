import os
import pandas as pd
from tqdm import tqdm

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "amazon_review_polarity_csv",
    "train.csv"
)
DB_DIR = "vectordb"


def load_reviews(csv_path, limit=5000):
    df = pd.read_csv(
        csv_path,
        header=None,
        nrows=limit   # 🔥 sampling happens here
    )
    df.columns = ["label", "title", "review"]

    documents = []

    for _, row in tqdm(df.iterrows(), total=len(df)):
        sentiment = "Positive" if row["label"] == 2 else "Negative"

        text = (
            f"Review Title: {row['title']}\n"
            f"Review Text: {row['review']}\n"
            f"Sentiment: {sentiment}"
        )

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "sentiment": sentiment,
                    "source": "amazon_review_polarity"
                }
            )
        )

    return documents


def build_vector_db(documents):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2",
        encode_kwargs={"batch_size": 64}  # optional speed-up
    )

    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=DB_DIR
    )

    vectordb.persist()
    print("✅ Vector database built and saved.")


if __name__ == "__main__":
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found at: {DATA_PATH}")

    docs = load_reviews(DATA_PATH, limit=5000)  # 👈 CONTROL SIZE HERE
    print(f"Loaded {len(docs)} reviews.")

    build_vector_db(docs)