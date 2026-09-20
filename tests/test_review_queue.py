import pytest
import sqlite3
from pathlib import Path
import src.review_queue as review_queue


@pytest.fixture
def clean_db():
    """Ensure clean database for each test."""
    db_path = Path("review_queue.db")
    if db_path.exists():
        db_path.unlink()

    review_queue.init_db()

    yield

    if db_path.exists():
        db_path.unlink()


def test_init_db_creates_schema(clean_db):
    """Database initialization creates all required tables."""
    conn = sqlite3.connect(review_queue.DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cursor.fetchall()}

    assert "tasks" in tables
    assert "task_metadata" in tables
    assert "review_queue" in tables
    assert "task_revisions" in tables

    conn.close()


def test_add_task_to_queue(clean_db):
    """Add a task to the review queue."""
    entities = [{"value": "Alice", "type": "entity"}]
    themes = [{"value": "firmware", "type": "theme"}]

    task_id = review_queue.add_task_to_queue(
        source_page="page_1.pdf",
        raw_text="TODO: Follow up with Alice about firmware",
        entities=entities,
        themes=themes,
        reason="low_confidence",
        confidence=0.75,
    )

    assert task_id > 0

    # Verify it's in the queue
    queue = review_queue.get_review_queue()
    assert len(queue) == 1
    assert queue[0]["id"] == task_id
    assert queue[0]["raw_text"] == "TODO: Follow up with Alice about firmware"


def test_get_review_queue_empty(clean_db):
    """Empty review queue returns empty list."""
    queue = review_queue.get_review_queue()
    assert queue == []


def test_approve_task(clean_db):
    """Approve a task from the review queue."""
    task_id = review_queue.add_task_to_queue(
        source_page="page_1.pdf",
        raw_text="TODO: Review documentation",
        entities=[],
        themes=[{"value": "documentation", "type": "theme"}],
    )

    # Initially in queue
    queue = review_queue.get_review_queue()
    assert len(queue) == 1

    # Approve it
    success = review_queue.approve_task(task_id, approved_by="test_user")
    assert success

    # No longer in queue
    queue = review_queue.get_review_queue()
    assert len(queue) == 0

    # In approved list
    approved = review_queue.get_approved_tasks()
    assert len(approved) == 1
    assert approved[0]["status"] == "approved"


def test_reject_task(clean_db):
    """Reject a task from the review queue."""
    task_id = review_queue.add_task_to_queue(
        source_page="page_1.pdf",
        raw_text="TODO: something unclear",
        entities=[],
        themes=[],
    )

    # Reject it
    success = review_queue.reject_task(
        task_id, reason="unclear", rejected_by="test_user"
    )
    assert success

    # No longer in queue
    queue = review_queue.get_review_queue()
    assert len(queue) == 0

    # Check status
    conn = sqlite3.connect(review_queue.DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()

    assert row["status"] == "rejected"


def test_edit_task(clean_db):
    """Edit a task and mark it as approved."""
    task_id = review_queue.add_task_to_queue(
        source_page="page_1.pdf",
        raw_text="TODO: Review documenation",  # typo
        entities=[],
        themes=[],
    )

    # Edit it
    success = review_queue.edit_task(
        task_id,
        new_text="TODO: Review documentation",  # corrected
        reason="fixed typo",
        edited_by="test_user",
    )
    assert success

    # Check new value
    conn = sqlite3.connect(review_queue.DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT raw_text, status FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()

    assert row["raw_text"] == "TODO: Review documentation"
    assert row["status"] == "approved"


def test_task_revision_history(clean_db):
    """Track revision history for a task."""
    task_id = review_queue.add_task_to_queue(
        source_page="page_1.pdf",
        raw_text="TODO: original task",
        entities=[],
        themes=[],
    )

    # Edit the task
    review_queue.edit_task(
        task_id,
        new_text="TODO: edited task",
        reason="clarification",
        edited_by="test_user",
    )

    # Fetch history
    history = review_queue.get_task_history(task_id)

    assert len(history) >= 2  # At least created + edited
    assert history[0]["action"] == "created"
    assert history[1]["action"] == "edited"
    assert history[1]["old_value"] == "TODO: original task"
    assert history[1]["new_value"] == "TODO: edited task"
    assert history[1]["reason"] == "clarification"


def test_multiple_tasks_in_queue(clean_db):
    """Multiple tasks queue with priority ordering."""
    task1 = review_queue.add_task_to_queue(
        source_page="page_1.pdf",
        raw_text="Task 1",
        entities=[],
        themes=[],
    )

    task2 = review_queue.add_task_to_queue(
        source_page="page_2.pdf",
        raw_text="Task 2",
        entities=[],
        themes=[],
    )

    task3 = review_queue.add_task_to_queue(
        source_page="page_3.pdf",
        raw_text="Task 3",
        entities=[],
        themes=[],
    )

    # All in queue
    queue = review_queue.get_review_queue()
    assert len(queue) == 3

    # Approve one
    review_queue.approve_task(task2)

    # Only 2 left
    queue = review_queue.get_review_queue()
    assert len(queue) == 2

    # Reject another
    review_queue.reject_task(task3)

    # Only 1 left
    queue = review_queue.get_review_queue()
    assert len(queue) == 1
    assert queue[0]["id"] == task1


def test_approved_tasks_list(clean_db):
    """Fetch list of approved tasks."""
    review_queue.add_task_to_queue("p1", "Task 1", [], [])
    task2_id = review_queue.add_task_to_queue("p2", "Task 2", [], [])
    task3_id = review_queue.add_task_to_queue("p3", "Task 3", [], [])

    # Approve 2 of them
    review_queue.approve_task(task2_id)
    review_queue.approve_task(task3_id)

    # Fetch approved
    approved = review_queue.get_approved_tasks()
    assert len(approved) == 2
    assert all(task["status"] == "approved" for task in approved)
