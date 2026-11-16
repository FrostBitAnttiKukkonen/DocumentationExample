# Install

## Prerequisites

- Python 3.10 or newer (`python --version`)
- pip

## Steps

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e .
```

Verify the installation:

```bash
task --help
```

You should see the list of subcommands (`add`, `list`, `done`).

## Where tasks are stored

Tasks are stored in a SQLite database. The default location is
`~/.tasks.db`; override it with the `TASKS_DB` environment variable:

```bash
export TASKS_DB="$PWD/my-tasks.db"
```

## Troubleshooting

- **`task: command not found`** — activate the virtual environment first
  (`source .venv/bin/activate`), then add the pip scripts directory
  (e.g. `~/.local/bin`) to your `PATH` if needed.
- **Docs preview or build fails** — run `zensical build --strict` in this
  directory: strict mode turns warnings (broken links, bad config) into errors.
