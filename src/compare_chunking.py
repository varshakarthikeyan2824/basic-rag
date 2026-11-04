import csv
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "results" / "retrieval_results.csv"
OUTPUT_FILE = BASE_DIR / "results" / "retrieval_comparison.csv"

METHODS = {
    "fixed_chunks": "Fixed-size",
    "paragraph_chunks": "Paragraph",
    "sentence_chunks": "Sentence",
}


def find_column(fieldnames, possible_names):
    """Find a CSV column using possible column names."""
    for name in possible_names:
        for field in fieldnames:
            if field.lower().strip() == name:
                return field
    raise ValueError(
        f"Could not find any of these columns: {possible_names}. "
        f"Available columns: {fieldnames}"
    )


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    with INPUT_FILE.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("The input CSV has no column headers.")

        question_col = find_column(reader.fieldnames, ["question"])
        method_col = find_column(
            reader.fieldnames, ["collection", "chunking_method", "method"]
        )
        rank_col = find_column(reader.fieldnames, ["rank"])
        source_col = find_column(reader.fieldnames, ["source", "filename"])
        distance_col = find_column(reader.fieldnames, ["distance"])
        text_col = find_column(
            reader.fieldnames, ["text", "document", "retrieved_text"]
        )

        # Keep only the top-ranked result for each question and method.
        best_results = {}

        for row in reader:
            method_key = row[method_col].strip()
            method_name = METHODS.get(method_key, method_key)

            key = (row[question_col], method_name)
            rank = int(row[rank_col])

            if key not in best_results or rank < best_results[key]["rank"]:
                best_results[key] = {
                    "rank": rank,
                    "source": row[source_col],
                    "distance": float(row[distance_col]),
                    "text": row[text_col],
                }

    # Group results by question.
    grouped = defaultdict(dict)

    for (question, method), result in best_results.items():
        grouped[question][method] = result

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(
            [
                "question",
                "chunking_method",
                "source",
                "top_distance",
                "retrieved_text",
                "relevant",
                "complete",
                "notes",
            ]
        )

        for question, methods in grouped.items():
            for method in ["Fixed-size", "Paragraph", "Sentence"]:
                result = methods.get(method)

                if result is None:
                    continue

                writer.writerow(
                    [
                        question,
                        method,
                        result["source"],
                        round(result["distance"], 4),
                        result["text"],
                        "",  # Fill manually: Yes or No
                        "",  # Fill manually: Yes or No
                        "",  # Add observations
                    ]
                )

    print(f"Comparison saved to: {OUTPUT_FILE}")
    print(f"Questions compared: {len(grouped)}")
    print(f"Comparison rows: {len(best_results)}")


if __name__ == "__main__":
    main()
