from rag_agent.sources import format_source_passages


def test_display_single_source_passage():
    rows = [
        (
            "annual_leave.txt",
            "chunk_1",
            "Employees receive annual leave.",
            "fixed",
            0.15,
            "company_A",
        )
    ]

    result = format_source_passages(rows)

    assert len(result) == 1
    assert result[0]["source"] == "annual_leave.txt"
    assert result[0]["chunk_id"] == "chunk_1"
    assert result[0]["passage"] == "Employees receive annual leave."


def test_display_multiple_source_passages():
    rows = [
        (
            "annual_leave.txt",
            "chunk_1",
            "Annual leave details.",
            "fixed",
            0.15,
            "company_A",
        ),
        (
            "sick_leave.txt",
            "chunk_2",
            "Sick leave details.",
            "fixed",
            0.20,
            "company_A",
        ),
    ]

    result = format_source_passages(rows)

    assert len(result) == 2
    assert result[1]["source"] == "sick_leave.txt"


def test_empty_results_return_empty_list():
    result = format_source_passages([])

    assert result == []


def test_empty_passage_is_not_displayed():
    rows = [("annual_leave.txt", "chunk_1", "", "fixed", 0.15, "company_A")]

    result = format_source_passages(rows)

    assert result == []
