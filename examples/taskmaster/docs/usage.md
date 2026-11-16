# Usage

## Add a task

```bash
task add "Buy milk"
task add "Read the Zensical docs" --due fri
task add "Submit assignment" --due 2026-02-14
```

`--due` accepts an ISO date (`YYYY-MM-DD`) or a weekday name
(`mon` .. `sun`). A weekday means the next occurrence of that weekday,
today included.

## List tasks

```bash
task list          # open tasks only
task list --all    # include completed tasks
```

Example output:

```
[ ] 2: Read the Zensical docs (due 2026-02-06)
[x] 1: Buy milk
```

## Complete a task

```bash
task done 2
```

Exits with code 1 and prints an error if no task has that id.

## Run the tests

```bash
pip install -e . pytest
pytest
```
