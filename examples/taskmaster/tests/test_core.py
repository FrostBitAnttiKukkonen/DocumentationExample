from datetime import date

import pytest

from taskmaster.core import TaskStore, parse_due_date


def test_parse_due_date_iso():
    assert parse_due_date("2026-01-31") == date(2026, 1, 31)


def test_parse_due_date_weekday_includes_today():
    # 2026-01-30 is a Friday
    assert parse_due_date("fri", today=date(2026, 1, 30)) == date(2026, 1, 30)


def test_parse_due_date_weekday_next_week():
    assert parse_due_date("mon", today=date(2026, 1, 30)) == date(2026, 2, 2)


def test_parse_due_date_invalid():
    with pytest.raises(ValueError):
        parse_due_date("someday")


def test_store_roundtrip(tmp_path):
    store = TaskStore(tmp_path / "test.db")
    task = store.add("Buy milk", date(2026, 2, 1))
    assert task.id is not None
    assert store.list() == [task]
    done = store.complete(task.id)
    assert done is not None and done.done is True
    assert store.list() == []
    assert store.list(include_done=True)[0].done is True
    assert store.complete(999) is None
