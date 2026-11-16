"""Command-line interface for TaskMaster."""

from __future__ import annotations

import argparse
import sys

from taskmaster.core import TaskStore, parse_due_date


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the ``task`` command."""
    parser = argparse.ArgumentParser(
        prog="task",
        description="A tiny command-line task manager.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="add a task")
    add.add_argument("title", help="what to do")
    add.add_argument("--due", help="due date: YYYY-MM-DD or a weekday like 'fri'")

    list_p = sub.add_parser("list", help="list open tasks")
    list_p.add_argument("--all", action="store_true", help="include completed tasks")

    done = sub.add_parser("done", help="mark a task as done")
    done.add_argument("id", type=int, help="task id shown by 'task list'")

    return parser


def main(argv: list[str] | None = None) -> int:
    """Entry point for the ``task`` command. Returns a process exit code."""
    args = build_parser().parse_args(argv)
    store = TaskStore()

    if args.command == "add":
        due = parse_due_date(args.due) if args.due else None
        task = store.add(args.title, due)
        due_text = f" (due {task.due})" if task.due else ""
        print(f"[{task.id}] {task.title}{due_text}")
        return 0

    if args.command == "list":
        tasks = store.list(include_done=args.all)
        if not tasks:
            print("no tasks")
            return 0
        for t in tasks:
            mark = "x" if t.done else " "
            due_text = f" (due {t.due})" if t.due else ""
            print(f"[{mark}] {t.id}: {t.title}{due_text}")
        return 0

    if args.command == "done":
        task = store.complete(args.id)
        if task is None:
            print(f"no task with id {args.id}", file=sys.stderr)
            return 1
        print(f"done: {task.title}")
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
