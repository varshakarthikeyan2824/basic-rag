import csv
from pathlib import Path

import tiktoken

# Load the tokenizer
encoding = tiktoken.get_encoding("cl100k_base")

# Six different text samples
samples = {
    "Prose": "Artificial intelligence helps businesses automate repetitive tasks.",
    "Python Code": """
def greet(name):
    return f"Hello, {name}!"
""",
    "JSON": """
{
    "name": "Arun",
    "role": "Software Tester",
    "experience": 2
}
""",
    "English": "I am learning artificial intelligence and machine learning.",
    "Tamil": "நான் செயற்கை நுண்ணறிவு கற்றுக்கொண்டு இருக்கிறேன்.",
    "Hindi": "मैं कृत्रिम बुद्धिमत्ता सीख रहा हूँ।",
}

# Count tokens
results = []

print("TOKEN COUNT RESULTS")
print("-" * 40)

for category, text in samples.items():
    tokens = encoding.encode(text)
    count = len(tokens)

    results.append(
        {
            "category": category,
            "token_count": count,
        }
    )

    print(f"{category}: {count} tokens")

# Save results to CSV
output_file = Path("results/token_results.csv")
output_file.parent.mkdir(parents=True, exist_ok=True)

with output_file.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["category", "token_count"],
    )
    writer.writeheader()
    writer.writerows(results)

print("-" * 40)
print(f"Results saved to: {output_file}")
