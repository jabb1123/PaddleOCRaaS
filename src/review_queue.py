import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any


DB_PATH = Path("review_queue.db")


def init_db():
    """Initialize the SQLite database schema."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tasks table: core extracted task data
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_page TEXT NOT NULL,
            source_hash TEXT,
            raw_text TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            confidence REAL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    
    # Task metadata: entities and themes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS task_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL UNIQUE,
            entities TEXT,
            themes TEXT,
            FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
        )
    """)
    
    # Review queue: tasks awaiting human review
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS review_queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL UNIQUE,
            reason TEXT,
            priority INTEGER DEFAULT 0,
            enqueued_at TEXT NOT NULL,
            reviewed_at TEXT,
            FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
        )
    """)
    
    # Revisions: track all changes to tasks
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS task_revisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL,
            action TEXT,
            old_value TEXT,
            new_value TEXT,
            reason TEXT,
            changed_by TEXT,
            changed_at TEXT NOT NULL,
            FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
        )
    """)
    
    # OCR results: raw text blocks extracted from documents
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ocr_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_name TEXT NOT NULL,
            page_number INTEGER NOT NULL,
            block_index INTEGER,
            text TEXT NOT NULL,
            confidence REAL,
            created_at TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()


def add_task_to_queue(
    source_page: str,
    raw_text: str,
    entities: List[Dict[str, str]],
    themes: List[Dict[str, str]],
    reason: str = "pending_review",
    confidence: Optional[float] = None,
    source_hash: Optional[str] = None,
) -> int:
    """Add a task to the review queue."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    now = datetime.utcnow().isoformat()
    
    # Insert task
    cursor.execute(
        """
        INSERT INTO tasks (source_page, source_hash, raw_text, confidence, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (source_page, source_hash, raw_text, confidence, now, now),
    )
    task_id = cursor.lastrowid
    
    # Insert metadata
    cursor.execute(
        """
        INSERT INTO task_metadata (task_id, entities, themes)
        VALUES (?, ?, ?)
        """,
        (task_id, json.dumps(entities), json.dumps(themes)),
    )
    
    # Insert into review queue
    cursor.execute(
        """
        INSERT INTO review_queue (task_id, reason, enqueued_at)
        VALUES (?, ?, ?)
        """,
        (task_id, reason, now),
    )
    
    # Log initial revision
    cursor.execute(
        """
        INSERT INTO task_revisions (task_id, action, new_value, changed_at)
        VALUES (?, ?, ?, ?)
        """,
        (task_id, "created", raw_text, now),
    )
    
    conn.commit()
    conn.close()
    
    return task_id


def get_review_queue(limit: int = 50) -> List[Dict[str, Any]]:
    """Fetch pending tasks from the review queue."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute(
        """
        SELECT t.id, t.source_page, t.raw_text, t.confidence, t.status,
               tm.entities, tm.themes,
               rq.reason, rq.enqueued_at
        FROM tasks t
        JOIN task_metadata tm ON t.id = tm.task_id
        JOIN review_queue rq ON t.id = rq.task_id
        WHERE rq.reviewed_at IS NULL
        ORDER BY rq.priority DESC, rq.enqueued_at ASC
        LIMIT ?
        """,
        (limit,),
    )
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def approve_task(task_id: int, approved_by: str = "user") -> bool:
    """Approve a task from the review queue."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    
    try:
        # Update task status
        cursor.execute(
            "UPDATE tasks SET status = ?, updated_at = ? WHERE id = ?",
            ("approved", now, task_id),
        )
        
        # Mark review as completed
        cursor.execute(
            "UPDATE review_queue SET reviewed_at = ? WHERE task_id = ?",
            (now, task_id),
        )
        
        # Log revision
        cursor.execute(
            """
            INSERT INTO task_revisions (task_id, action, new_value, changed_by, changed_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (task_id, "approved", "approved", approved_by, now),
        )
        
        conn.commit()
        return True
    finally:
        conn.close()


def reject_task(task_id: int, reason: str = "", rejected_by: str = "user") -> bool:
    """Reject a task from the review queue."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    
    try:
        # Update task status
        cursor.execute(
            "UPDATE tasks SET status = ?, updated_at = ? WHERE id = ?",
            ("rejected", now, task_id),
        )
        
        # Mark review as completed
        cursor.execute(
            "UPDATE review_queue SET reviewed_at = ? WHERE task_id = ?",
            (now, task_id),
        )
        
        # Log revision
        cursor.execute(
            """
            INSERT INTO task_revisions (task_id, action, new_value, reason, changed_by, changed_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (task_id, "rejected", "rejected", reason, rejected_by, now),
        )
        
        conn.commit()
        return True
    finally:
        conn.close()


def edit_task(task_id: int, new_text: str, reason: str = "", edited_by: str = "user") -> bool:
    """Edit a task and mark it as approved."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    
    try:
        # Fetch old value
        cursor.execute("SELECT raw_text FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        if not row:
            return False
        old_text = row[0]
        
        # Update task
        cursor.execute(
            "UPDATE tasks SET raw_text = ?, status = ?, updated_at = ? WHERE id = ?",
            (new_text, "approved", now, task_id),
        )
        
        # Mark review as completed
        cursor.execute(
            "UPDATE review_queue SET reviewed_at = ? WHERE task_id = ?",
            (now, task_id),
        )
        
        # Log revision
        cursor.execute(
            """
            INSERT INTO task_revisions (task_id, action, old_value, new_value, reason, changed_by, changed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (task_id, "edited", old_text, new_text, reason, edited_by, now),
        )
        
        conn.commit()
        return True
    finally:
        conn.close()


def get_task_history(task_id: int) -> List[Dict[str, Any]]:
    """Fetch the revision history for a task."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute(
        """
        SELECT id, action, old_value, new_value, reason, changed_by, changed_at
        FROM task_revisions
        WHERE task_id = ?
        ORDER BY changed_at ASC
        """,
        (task_id,),
    )
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_approved_tasks(limit: int = 100) -> List[Dict[str, Any]]:
    """Fetch approved tasks."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute(
        """
        SELECT t.id, t.source_page, t.raw_text, t.confidence, t.status,
               tm.entities, tm.themes, t.updated_at
        FROM tasks t
        JOIN task_metadata tm ON t.id = tm.task_id
        WHERE t.status = 'approved'
        ORDER BY t.updated_at DESC
        LIMIT ?
        """,
        (limit,),
    )
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def store_ocr_results(
    document_name: str,
    page_number: int,
    ocr_blocks: List[Dict[str, Any]],
) -> None:
    """Store OCR results for a document page."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    
    try:
        for block_index, block in enumerate(ocr_blocks):
            cursor.execute(
                """
                INSERT INTO ocr_results (document_name, page_number, block_index, text, confidence, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    document_name,
                    page_number,
                    block_index,
                    block.get("text", ""),
                    block.get("confidence", 0.0),
                    now,
                ),
            )
        conn.commit()
    finally:
        conn.close()


def get_ocr_results(document_name: str, page_number: Optional[int] = None) -> List[Dict[str, Any]]:
    """Fetch OCR results for a document (optionally filtered by page)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if page_number is not None:
        cursor.execute(
            """
            SELECT id, document_name, page_number, block_index, text, confidence, created_at
            FROM ocr_results
            WHERE document_name = ? AND page_number = ?
            ORDER BY page_number ASC, block_index ASC
            """,
            (document_name, page_number),
        )
    else:
        cursor.execute(
            """
            SELECT id, document_name, page_number, block_index, text, confidence, created_at
            FROM ocr_results
            WHERE document_name = ?
            ORDER BY page_number ASC, block_index ASC
            """,
            (document_name,),
        )
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_documents() -> List[str]:
    """Fetch all unique document names in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT DISTINCT document_name FROM ocr_results ORDER BY document_name DESC")
    rows = cursor.fetchall()
    conn.close()
    
    return [row[0] for row in rows]
