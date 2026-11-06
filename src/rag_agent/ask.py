import os

import tiktoken
from groq import Groq

from embeddings import generate_embeddings
from rag_agent.sources import format_source_passages
from retrieval import search_chunks

DONT_KNOW = "I don't know based on available documents."


def generate_answer(prompt):
    """Generate an answer using the Groq API."""
    client = Groq(api_key=os.environ["GROQ_API_KEY"])

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0,
    )

    return response.choices[0].message.content


def build_context(sources, max_tokens=3000):
    """Build source context without exceeding the token budget."""
    encoding = tiktoken.get_encoding("cl100k_base")

    selected_sources = []
    context_parts = []
    token_count = 0

    for index, source in enumerate(sources, start=1):
        part = (
            f"[{index}] {source['source']} ({source['chunk_id']}): {source['passage']}"
        )

        part_tokens = len(encoding.encode(part))
        separator_tokens = 2 if context_parts else 0

        if token_count + part_tokens + separator_tokens > max_tokens:
            continue

        context_parts.append(part)
        selected_sources.append(source)
        token_count += part_tokens + separator_tokens

    return {
        "context": "\n\n".join(context_parts),
        "sources": selected_sources,
        "token_count": token_count,
    }


def ask(question, tenant, user_role, context_token_budget=3000):
    """Retrieve relevant policy passages and generate an answer."""
    query_embedding = generate_embeddings([question])[0]

    rows = search_chunks(
        query_embedding,
        tenant=tenant,
        user_role=user_role,
    )

    sources = format_source_passages(rows)

    if not sources:
        return {
            "answer": DONT_KNOW,
            "sources": [],
        }

    context_result = build_context(
        sources,
        max_tokens=context_token_budget,
    )

    context = context_result["context"]
    sources = context_result["sources"]

    if not sources:
        return {
            "answer": DONT_KNOW,
            "sources": [],
        }

    prompt = f"""
Answer the question using only the context below.

If the context does not contain enough information, say:
{DONT_KNOW}

Include citation numbers such as [1] in your answer.

Context:
{context}

Question:
{question}
"""

    answer = generate_answer(prompt)

    return {
        "answer": answer,
        "sources": sources,
    }
