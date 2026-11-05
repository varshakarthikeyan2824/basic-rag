import json
import os
from pathlib import Path

import psycopg
from pgvector.psycopg import register_vector

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://rag_user:rag_dev_password@localhost:5433/rag_db",
)

RESULTS_DIR = Path("results")

ACCESS_RULES = {
    "all_employees": {
        "annual_leave.txt",
        "casual_leave.txt",
        "performance.txt",
        "training.txt",
        "sick_leave.txt",
        "resignation.txt",
        "attendance.txt",
        "internet.txt",
    },
    "hr": {
        "expenses.txt",
        "grievance.txt",
        "id_card.txt",
        "travel.txt",
        "visitor.txt",
        "refund.txt",
    },
    "it": {
        "data_privacy.txt",
        "email.txt",
        "laptop.txt",
    },
    "manager_it": {
        "overtime.txt",
        "password.txt",
        "remote_work.txt",
    },
}

ROLE_MAP = {
    "all_employees": ["EMPLOYEE", "HR", "MANAGER", "IT"],
    "hr": ["HR"],
    "it": ["IT"],
    "manager_it": ["MANAGER", "IT"],
}


def get_allowed_roles(source):
    for group, files in ACCESS_RULES.items():
        if source in files:
            return ROLE_MAP[group]

    raise ValueError(f"No access rule defined for {source}")


def main():
    with psycopg.connect(DATABASE_URL) as conn:
        register_vector(conn)

        with conn.cursor() as cur:
            for path in sorted(RESULTS_DIR.glob("embeddings_*.json")):
                strategy = path.stem.replace("embeddings_", "")
                records = json.loads(path.read_text())

                for record in records:
                    source = record["source"]
                    roles = get_allowed_roles(source)

                    for tenant in ["company_A", "company_B"]:
                        cur.execute(
                            """
                            INSERT INTO document_chunks (
                                chunk_id,
                                content,
                                embedding,
                                tenant,
                                allowed_roles,
                                source,
                                strategy
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (
                                tenant, source, strategy, chunk_id
                            ) DO NOTHING
                            """,
                            (
                                record["chunk_id"],
                                record["text"],
                                record["embedding"],
                                tenant,
                                roles,
                                source,
                                strategy,
                            ),
                        )

    print("Migration completed successfully.")


if __name__ == "__main__":
    main()
