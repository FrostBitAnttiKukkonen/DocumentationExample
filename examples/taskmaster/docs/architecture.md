# Architecture

Why TaskMaster is built the way it is.

## Two layers

`taskmaster.core` contains all storage and business logic and has **no
dependency on the command line**. `taskmaster.cli` is a thin argparse
wrapper around `TaskStore`. This separation exists so the logic can be
tested (see `tests/test_core.py`) and reused from other interfaces without
parsing command-line arguments.

## Storage choice

Tasks live in a single SQLite file instead of a JSON file because SQLite
gives us atomic writes and a stable schema for free — there is no file to
corrupt if two processes write at once. The database path is configurable
via `TASKS_DB` so tests can use a temporary file (`tmp_path` fixture)
instead of touching the user's real database.

## Why docstrings drive the API docs

The docstrings in `src/` are the single source of truth for the
[API reference](api.md): mkdocstrings renders them into this site at build
time. That means the reference can never drift away from the code — if a
function changes, the generated docs change with it on the next
`zensical build`.
