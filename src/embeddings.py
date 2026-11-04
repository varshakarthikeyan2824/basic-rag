import csv
import json
from pathlib import Path

import httpx

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "results"

MODEL = "nomic-embed-text"
API_URL = "http://localhost:11434/api/embed"
BATCH_SIZE = 32


def generate_embeddings(texts):
    all_embeddings = []

    with httpx.Client(timeout=120.0) as client:
        for start in range(0, len(texts), BATCH_SIZE):
            batch = texts[start : start + BATCH_SIZE]

            response = client.post(
                API_URL,
                json={
                    "model": MODEL,
                    "input": batch,
                },
            )

            response.raise_for_status()
            data = response.json()

            all_embeddings.extend(data["embeddings"])

    return all_embeddings


def process_file(filename):
    input_file = RESULTS_DIR / filename

    with input_file.open(encoding="utf-8", newline="") as file:
        chunks = list(csv.DictReader(file))

    texts = [chunk["text"] for chunk in chunks]
    embeddings = generate_embeddings(texts)

    if len(chunks) != len(embeddings):
        raise ValueError("Number of chunks and embeddings do not match")

    output_data = []

    for chunk, embedding in zip(chunks, embeddings):
        output_data.append(
            {
                "source": chunk["source"],
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"],
                "embedding": embedding,
            }
        )

    output_file = RESULTS_DIR / filename.replace("chunks_", "embeddings_").replace(
        ".csv", ".json"
    )

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(output_data, file, indent=2)

    print(
        f"{filename}: {len(chunks)} chunks embedded. "
        f"Vector dimensions: {len(embeddings[0])}"
    )


def main():
    files = [
        "chunks_fixed.csv",
        "chunks_paragraph.csv",
        "chunks_sentence.csv",
    ]

    for filename in files:
        process_file(filename)


if __name__ == "__main__":
    main()
