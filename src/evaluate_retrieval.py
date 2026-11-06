import json
from pathlib import Path

from embeddings import generate_embeddings
from retrieval import search_chunks

BASE_DIR = Path(__file__).resolve().parent.parent
GOLDEN_FILE = BASE_DIR / "data" / "golden" / "golden_questions.json"

TENANT = "company_A"
K_VALUES = [1, 3, 5]


def main():
    with open(GOLDEN_FILE, encoding="utf-8") as file:
        questions = json.load(file)

    results = {k: 0 for k in K_VALUES}

    for item in questions:
        question = item["question"]
        expected_source = item["expected_source"]
        expected_chunk_id = item["expected_chunk_id"]
        user_role = item["user_role"]
        embedding = generate_embeddings([question])[0]

        retrieved = search_chunks(
            embedding,
            tenant=TENANT,
            user_role=user_role,
            limit=max(K_VALUES),
        )

        print(f"\nQuestion: {question}")
        if not any(
            row[0] == expected_source and str(row[1]) == str(expected_chunk_id)
            for row in retrieved
        ):
            print("Expected:", expected_source, expected_chunk_id)
            print("Retrieved top 5:")
            for row in retrieved:
                print(f"  {row[0]} | {row[1]} | distance: {row[4]:.4f}")

        for k in K_VALUES:
            top_k = retrieved[:k]

            found = any(
                row[0] == expected_source and str(row[1]) == str(expected_chunk_id)
                for row in top_k
            )

            if found:
                results[k] += 1

            print(f"Recall@{k} hit: {found}")

    print("\n========== Recall@K Results ==========")

    total = len(questions)

    for k in K_VALUES:
        recall = results[k] / total
        print(f"Recall@{k}: {recall:.2%} ({results[k]}/{total})")


if __name__ == "__main__":
    main()
