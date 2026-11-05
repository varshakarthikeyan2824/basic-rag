CREATE TABLE IF NOT EXISTS document_chunks (
    id BIGSERIAL PRIMARY KEY,
    chunk_id TEXT NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(768) NOT NULL,
    tenant TEXT NOT NULL,
    allowed_roles TEXT[] NOT NULL,
    source TEXT NOT NULL,
    strategy TEXT NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (tenant, source, strategy, chunk_id)
);
