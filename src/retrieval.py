import os

import psycopg
from pgvector import Vector
from pgvector.psycopg import register_vector

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://rag_user:rag_dev_password@localhost:5433/rag_db",
)


def search_chunks(query_embedding, tenant, user_role, limit=5):
    with psycopg.connect(DATABASE_URL) as conn:
        register_vector(conn)

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    source,
                    chunk_id,
                    content,
                    strategy,
                    embedding <=> %s AS distance,
                    tenant
                FROM document_chunks
                WHERE tenant = %s
                  AND %s = ANY(allowed_roles)
                ORDER BY embedding <=> %s
                LIMIT %s
                """,
                (
                    Vector(query_embedding),
                    tenant,
                    user_role,
                    Vector(query_embedding),
                    limit,
                ),
            )

            return cur.fetchall()
