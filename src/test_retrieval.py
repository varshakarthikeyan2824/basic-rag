import json

from retrieval import search_chunks

with open("results/embeddings_fixed.json") as file:
    records = json.load(file)

query_embedding = records[0]["embedding"]

allowed_sources = {
    "EMPLOYEE": {
        "annual_leave.txt",
        "attendance.txt",
        "casual_leave.txt",
        "internet.txt",
        "performance.txt",
        "resignation.txt",
        "sick_leave.txt",
        "training.txt",
    },
    "HR": {
        "annual_leave.txt",
        "attendance.txt",
        "casual_leave.txt",
        "internet.txt",
        "performance.txt",
        "resignation.txt",
        "sick_leave.txt",
        "training.txt",
        "expenses.txt",
        "grievance.txt",
        "id_card.txt",
        "refund.txt",
        "travel.txt",
        "visitor.txt",
    },
    "MANAGER": {
        "annual_leave.txt",
        "attendance.txt",
        "casual_leave.txt",
        "internet.txt",
        "performance.txt",
        "resignation.txt",
        "sick_leave.txt",
        "training.txt",
        "overtime.txt",
        "password.txt",
        "remote_work.txt",
    },
    "IT": {
        "annual_leave.txt",
        "attendance.txt",
        "casual_leave.txt",
        "internet.txt",
        "performance.txt",
        "resignation.txt",
        "sick_leave.txt",
        "training.txt",
        "data_privacy.txt",
        "email.txt",
        "laptop.txt",
        "overtime.txt",
        "password.txt",
        "remote_work.txt",
    },
}

for role, expected_sources in allowed_sources.items():
    results = search_chunks(query_embedding, "company_A", role, limit=500)

    actual_sources = {row[0] for row in results}

    assert actual_sources == expected_sources
    assert all(row[5] == "company_A" for row in results)

    print(f"{role}: Access check passed ({len(results)} chunks)")

company_b = search_chunks(query_embedding, "company_B", "EMPLOYEE", limit=500)

assert all(row[5] == "company_B" for row in company_b)

print("Tenant isolation check passed!")
print("All security checks passed!")
