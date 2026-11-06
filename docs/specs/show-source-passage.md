# Feature Specification: Show Source Passage

## 1. Problem
Users need to verify the source information
used by the RAG system to generate answers.

## 2. Goal
Display the original source passage along
with the generated answer.

## 3. Functional Requirements
- Retrieve relevant source chunks.
- Generate answers using retrieved context.
- Show the original source passage.
- Show source document name and chunk ID.
- Return "I don't know" when evidence is missing.

## 4. Acceptance Criteria
- Relevant passages must be displayed.
- Multiple relevant passages must be supported.
- Missing evidence must not produce unsupported answers.
- Source information must be traceable.

## 5. Out of Scope
- Frontend development.
- Document uploading.
- Database schema changes.
- Changing embedding models.

## 6. Success Criteria
Users can verify answers using the
original retrieved source passages.
