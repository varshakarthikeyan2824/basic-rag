from rag_agent.ask import build_context


def test_context_stays_within_token_budget():
    sources = [
        {
            "source": "policy.txt",
            "chunk_id": "chunk_1",
            "passage": "Annual leave is provided to employees. " * 100,
        },
        {
            "source": "sick_leave.txt",
            "chunk_id": "chunk_2",
            "passage": "Sick leave is provided to employees. " * 100,
        },
    ]

    context = build_context(sources, max_tokens=100)

    assert context["token_count"] <= 100
