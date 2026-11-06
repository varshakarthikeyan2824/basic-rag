# Implementation Plan: Show Source Passage

## 1. Objective
Display the original source passage used by the RAG
system to generate an answer.

## 2. Implementation Steps

1. Review the existing retrieval.py and ask function.
2. Identify the source metadata available in PostgreSQL.
3. Update retrieval results to include source passage,
   document name, and chunk ID.
4. Add source passage information to the answer response.
5. Handle missing or empty source passages.
6. Write unit tests for all scenarios.
7. Run tests and review the changes.

## 3. Expected Output

Question: What is the annual leave policy?

Answer: Employees receive annual leave according
to the company policy.

Source:
- Document: annual_leave.txt
- Chunk ID: 12
- Passage: Original retrieved policy text.

## 4. Validation
- Verify source passage accuracy.
- Verify document name and chunk ID.
- Verify missing-source handling.
- Run all existing and new tests.

## 5. Risks
- Missing metadata in retrieved chunks.
- Incorrect source references.
- Empty or irrelevant retrieved passages.
