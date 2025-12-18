from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

DB_DIR = "vectordb"


def load_vector_db():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )

    vectordb = Chroma(
        persist_directory=DB_DIR,
        embedding_function=embeddings
    )
    return vectordb


def build_prompt(context, question):
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are analyzing Amazon customer reviews.

Use ONLY the information provided in the reviews below.
If the answer is not present, say:
"I don't know based on the provided reviews."

Reviews:
{context}

Question:
{question}

Answer clearly and concisely.
"""
    )

    return prompt.format(context=context, question=question)


def main():
    vectordb = load_vector_db()

    llm = OllamaLLM(
        model="gpt-oss:120b-cloud",
        temperature=0
    )

    print("\n📌 Amazon Review RAG System Ready")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("Ask a question: ")
        if query.lower() == "exit":
            break

        # 1️⃣ Retrieve relevant reviews
        docs = vectordb.similarity_search(query, k=5)

        print("\n🔎 Retrieved Context:\n")
        for i, doc in enumerate(docs, 1):
            print(f"--- Retrieved Doc {i} ---")
            print(doc.page_content)
            print()

        # 2️⃣ Build prompt
        context_text = "\n\n".join(doc.page_content for doc in docs)
        final_prompt = build_prompt(context_text, query)

        # 3️⃣ Generate answer (LOCAL LLM)
        answer = llm.invoke(final_prompt)

        print("\n🧠 Answer:\n", answer)
        print("-" * 60)


if __name__ == "__main__":
    main()