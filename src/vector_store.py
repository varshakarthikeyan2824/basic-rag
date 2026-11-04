import json
from pathlib import Path

import chromadb

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "results"
DB_DIR = BASE_DIR / "data" / "chroma_db"

DB_DIR.mkdir(parents=True, exist_ok=True)

client = chromadb.PersistentClient(path=str(DB_DIR))


def store_embeddings(filename, collection_name):
    input_file = RESULTS_DIR / filename

    with input_file.open(encoding="utf-8") as file:
        records = json.load(file)

    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
    )

    ids = [f"{record['source']}_{record['chunk_id']}" for record in records]

    documents = [record["text"] for record in records]
    embeddings = [record["embedding"] for record in records]

    metadatas = [
        {
            "source": record["source"],
            "chunk_id": str(record["chunk_id"]),
        }
        for record in records
    ]

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"{collection_name}: {collection.count()} records stored")


def main():
    methods = {
        "embeddings_fixed.json": "fixed_chunks",
        "embeddings_paragraph.json": "paragraph_chunks",
        "embeddings_sentence.json": "sentence_chunks",
    }

    for filename, collection_name in methods.items():
        store_embeddings(filename, collection_name)


if __name__ == "__main__":
    main()
