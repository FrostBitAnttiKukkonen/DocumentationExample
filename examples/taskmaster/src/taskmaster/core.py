"""Core task storage and logic for TaskMaster."""

from __future__ import annotations

import os
import sqlite3
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

DEFAULT_DB_PATH = Path.home() / ".tasks.db"

WEEKDAYS = {"mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6}


@dataclass
class Task:
    """A single task.

    Attributes:
        id: Database id, assigned when the task is inserted.
        title: Short description of the task.
        due: Optional due date.
        done: Whether the task has been completed.
    """

    id: int | None
    title: str
    due: date | None = None
    done: bool = False


def parse_due_date(text: str, today: date | None = None) -> date:
    """Parse a due date from user text like ``"fri"`` or ``"2026-01-31"``.

    Args:
        text: An ISO date (``YYYY-MM-DD``) or a weekday name
            (``"mon"`` .. ``"sun"``, case-insensitive).
        today: Reference date used for weekday parsing; defaults to
            ``date.today()``.

    Returns:
        The parsed date. A weekday means the next occurrence of that
        weekday, today included.

    Raises:
        ValueError: If the text is neither an ISO date nor a weekday name.
    """
    today = today or date.today()
    text = text.strip().lower()
    try:
        return date.fromisoformat(text)
    except ValueError:
        pass
    if text in WEEKDAYS:
        days_ahead = (WEEKDAYS[text] - today.weekday()) % 7
        return today + timedelta(days=days_ahead)
    raise ValueError(
        f"unrecognized date {text!r}: use YYYY-MM-DD or a weekday like 'fri'"
    )


class TaskStore:
    """SQLite-backed storage for tasks.

    The database file location comes from the ``TASKS_DB`` environment
    variable and defaults to ``~/.tasks.db``.
    """

    def __init__(self, db_path: str | Path | None = None) -> None:
        """Open (creating if needed) the database at ``db_path``."""
        self.db_path = Path(db_path or os.environ.get("TASKS_DB", DEFAULT_DB_PATH))
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS tasks ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "title TEXT NOT NULL, due TEXT, done INTEGER NOT NULL DEFAULT 0)"
            )

    def add(self, title: str, due: date | None = None) -> Task:
        """Add a task and return it with its new id."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                "INSERT INTO tasks (title, due, done) VALUES (?, ?, 0)",
                (title, due.isoformat() if due else None),
            )
            return Task(cur.lastrowid, title, due, False)

    def list(self, include_done: bool = False) -> list[Task]:
        """Return tasks, newest first, optionally including completed ones."""
        query = "SELECT id, title, due, done FROM tasks"
        if not include_done:
            query += " WHERE done = 0"
        query += " ORDER BY id DESC"
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(query).fetchall()
        return [
            Task(i, t, date.fromisoformat(d) if d else None, bool(done))
            for i, t, d, done in rows
        ]

    def complete(self, task_id: int) -> Task | None:
        """Mark a task as done.

        Returns the updated task, or ``None`` if no task has that id.
        """
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
            if cur.rowcount == 0:
                return None
            i, t, d, done = conn.execute(
                "SELECT id, title, due, done FROM tasks WHERE id = ?", (task_id,)
            ).fetchone()
        return Task(i, t, date.fromisoformat(d) if d else None, bool(done))
