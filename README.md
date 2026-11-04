# RAG Agent – Day 6 FDE Training Project

## Project Overview

This project explores the fundamentals of Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG).

It covers token counting, document chunking, embeddings, vector storage, information retrieval, and comparison of local and hosted LLMs using synthetic company policy documents.

## Technologies Used

- Python 3.12
- UV – Python package and project management
- tiktoken – Token counting
- Ollama – Local embedding and LLM models
- Nomic Embed Text – Text embeddings
- ChromaDB – Vector database
- Groq – Hosted LLM API
- Pandas and HTTPX – Data processing and API requests
- Pytest – Testing

## Project Structure

```text
rag-agent/
├── data/
│   ├── policies/
│   └── chroma_db/
├── docs/
│   ├── ai_building_blocks.md
│   ├── model_comparison.md
│   └── what_llm_cannot_do.md
├── results/
│   ├── token_results.csv
│   ├── chunks_fixed.csv
│   ├── chunks_paragraph.csv
│   ├── chunks_sentence.csv
│   ├── embeddings_fixed.json
│   ├── embeddings_paragraph.json
│   ├── embeddings_sentence.json
│   ├── retrieval_results.csv
│   └── retrieval_comparison.csv
├── src/
│   ├── token_lab.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── ask_questions.py
│   ├── compare_chunking.py
│   └── groq_test.py
├── tests/
├── pyproject.toml
└── README.md
```

## Tasks Completed

### 1. Token Lab
- Counted tokens for six different text samples.
- Compared prose, Python code, JSON, English, Tamil, and Hindi.
- Saved token counts in `results/token_results.csv`.

### 2. Document Chunking
- Created 20 synthetic company policy documents.
- Implemented fixed-size, paragraph-based, and sentence-based chunking.
- Saved the generated chunks as CSV files.

### 3. Embeddings
- Generated embeddings using the local Nomic Embed Text model through Ollama.
- Generated 768-dimensional vectors for all three chunking methods.

### 4. Vector Storage
- Stored document chunks and embeddings in ChromaDB.
- Created separate collections for fixed-size, paragraph, and sentence chunks.

### 5. Retrieval
- Tested 10 questions against the policy documents.
- Retrieved the top 3 matching chunks for each question.
- Saved retrieval results in `results/retrieval_results.csv`.

### 6. Chunking Comparison
- Compared retrieval results across all three chunking methods.
- Evaluated relevance and completeness of retrieved information.
- Saved the comparison in `results/retrieval_comparison.csv`.

### 7. Local vs Hosted LLM Comparison
- Tested a small local model using Ollama.
- Compared its response with a hosted Groq model.
- Observed differences in accuracy, instruction following, and hallucination.

### 8. Documentation
- Documented the limitations of LLMs.
- Explained important AI building blocks.
- Recorded the local and hosted model comparison.

## Setup Instructions

### 1. Install dependencies

```bash
uv sync
```

### 2. Start Ollama

Make sure the Ollama server is running in a separate terminal:

```bash
ollama serve
```

### 3. Download the embedding model

```bash
ollama pull nomic-embed-text
```

### 4. Run the project scripts

Run the scripts from the project root in the following order:

```bash
uv run python src/token_lab.py
uv run python src/chunking.py
uv run python src/embeddings.py
uv run python src/vector_store.py
uv run python src/ask_questions.py
uv run python src/compare_chunking.py
```

### 5. Run tests

```bash
uv run pytest
```

## Key Learnings

- How tokenization works across different types of text.
- How chunking strategies affect document retrieval.
- How embeddings represent text as numerical vectors.
- How vector databases store and retrieve similar information.
- How RAG retrieves relevant context from documents.
- Why LLM outputs need validation and human review.
- Differences between small local models and hosted models.

## Conclusion

This project provided practical experience with LLM fundamentals, embeddings, vector databases, and retrieval techniques. It also demonstrated the importance of evaluating model responses rather than blindly trusting generated answers.
