# Specification: RAG Ask Function

## Objective
Build an ask() function that answers user questions
using retrieved company policy documents.

## Requirements
1. Accept question, tenant and user role.
2. Generate question embeddings using Ollama.
3. Retrieve relevant chunks from PostgreSQL.
4. Respect tenant and role-based access.
5. Assemble context within a 3000-token budget.
6. Generate answers using Groq.
7. Include numbered citations.
8. Display original source passages.
9. Return "I don't know" when evidence is missing.

## Expected Output
- Answer
- Source document
- Chunk ID
- Original source passage

## Error Handling
- No retrieved chunks.
- Empty source passages.
- Embedding API failure.
- LLM API failure.
- Context exceeding token budget.

## Out of Scope
- Frontend development.
- New database tables.
- Document uploading.
- Changing embedding models.
