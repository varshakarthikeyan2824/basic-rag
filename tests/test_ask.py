from rag_agent.ask import ask


def test_ask_returns_answer_with_source_passage(monkeypatch):
    rows = [
        (
            "sick_leave.txt",
            "chunk_1",
            "Employees receive 10 days of sick leave annually.",
            "fixed",
            0.15,
            "company_A",
        )
    ]

    monkeypatch.setattr(
        "rag_agent.ask.generate_embeddings",
        lambda texts: [[0.1] * 768],
    )
    monkeypatch.setattr(
        "rag_agent.ask.search_chunks",
        lambda *args, **kwargs: rows,
    )
    monkeypatch.setattr(
        "rag_agent.ask.generate_answer",
        lambda prompt: "Employees receive 10 days of sick leave annually. [1]",
    )

    result = ask(
        "How many sick leave days are provided?",
        tenant="company_A",
        user_role="HR",
    )

    assert "10 days" in result["answer"]
    assert len(result["sources"]) == 1
    assert result["sources"][0]["source"] == "sick_leave.txt"
    assert result["sources"][0]["chunk_id"] == "chunk_1"


def test_ask_returns_dont_know_when_no_chunks_are_found(monkeypatch):
    monkeypatch.setattr(
        "rag_agent.ask.generate_embeddings",
        lambda texts: [[0.1] * 768],
    )
    monkeypatch.setattr(
        "rag_agent.ask.search_chunks",
        lambda *args, **kwargs: [],
    )

    result = ask(
        "What is the travel allowance?",
        tenant="company_A",
        user_role="HR",
    )

    assert result["answer"] == "I don't know based on available documents."
    assert result["sources"] == []


def test_ask_does_not_include_empty_source_passages(monkeypatch):
    rows = [
        (
            "sick_leave.txt",
            "chunk_1",
            "",
            "fixed",
            0.15,
            "company_A",
        )
    ]

    monkeypatch.setattr(
        "rag_agent.ask.generate_embeddings",
        lambda texts: [[0.1] * 768],
    )
    monkeypatch.setattr(
        "rag_agent.ask.search_chunks",
        lambda *args, **kwargs: rows,
    )

    result = ask(
        "How many sick leave days are provided?",
        tenant="company_A",
        user_role="HR",
    )

    assert result["sources"] == []
    assert result["answer"] == "I don't know based on available documents."
