import main


def test_normalize_shorthand_expands_common_patterns():
    raw = "Need follow up w/ Alice b/c project is blocked. Tmr we should review notes."

    normalized = main.normalize_shorthand(raw)

    assert "with" in normalized.lower()
    assert "because" in normalized.lower()
    assert "tomorrow" in normalized.lower()


def test_extract_tasks_picks_up_action_items():
    text = """
    TODO: follow up with Alice
    Next: review pricing notes
    Need to draft summary for client
    """

    tasks = main.extract_tasks(text)

    assert len(tasks) >= 3
    assert any("follow up with alice" in task["text"].lower() for task in tasks)
    assert all(task["status"] == "pending" for task in tasks)
