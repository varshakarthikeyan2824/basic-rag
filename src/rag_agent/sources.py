def format_source_passages(rows):
    """Format retrieved database rows into source passages."""
    sources = []

    for row in rows:
        source, chunk_id, content = row[:3]

        if not content or not content.strip():
            continue

        sources.append(
            {
                "source": source,
                "chunk_id": chunk_id,
                "passage": content,
            }
        )

    return sources
