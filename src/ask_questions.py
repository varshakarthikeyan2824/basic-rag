import csv
from pathlib import Path

import chromadb
import httpx

BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "data" / "chroma_db"
RESULTS_DIR = BASE_DIR / "results"

MODEL = "nomic-embed-text"
API_URL = "http://localhost:11434/api/embed"
TOP_K = 3

questions = [
    "How many days of annual leave can employees take?",
    "What should an employee do when they are sick?",
    "What are the rules for casual leave?",
    "What happens if an employee arrives late?",
    "Can employees work remotely?",
    "How is overtime handled?",
    "What is the process for business travel?",
    "How should employees submit expense claims?",
    "What should employees do if their laptop is damaged?",
    "How should employees protect confidential data?",
]

client = chromadb.PersistentClient(path=str(DB_DIR))


def create_embedding(question):
    response = httpx.post(
        API_URL,
        json={"model": MODEL, "input": question},
        timeout=120.0,
    )
    response.raise_for_status()
    return response.json()["embeddings"][0]


def search_collection(collection_name, question):
    collection = client.get_collection(name=collection_name)
    question_embedding = create_embedding(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=TOP_K,
        include=["documents", "metadatas", "distances"],
    )

    return results


def main():
    collections = [
        "fixed_chunks",
        "paragraph_chunks",
        "sentence_chunks",
    ]

    output_file = RESULTS_DIR / "retrieval_results.csv"

    with output_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "question",
                "chunking_method",
                "rank",
                "source",
                "distance",
                "retrieved_text",
            ],
        )
        writer.writeheader()

        for question in questions:
            print(f"\nQuestion: {question}")

            for collection_name in collections:
                results = search_collection(collection_name, question)

                print(f"\n{collection_name}:")

                for rank, (document, metadata, distance) in enumerate(
                    zip(
                        results["documents"][0],
                        results["metadatas"][0],
                        results["distances"][0],
                    ),
                    start=1,
                ):
                    print(f"{rank}. {metadata['source']} (distance: {distance:.4f})")
                    print(document)

                    writer.writerow(
                        {
                            "question": question,
                            "chunking_method": collection_name,
                            "rank": rank,
                            "source": metadata["source"],
                            "distance": distance,
                            "retrieved_text": document,
                        }
                    )

    print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    main()
