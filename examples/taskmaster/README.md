# TaskMaster

A tiny command-line task manager in Python. Add, list, and complete tasks
from your terminal.

## Prerequisites

- Python 3.10 or newer
- pip

## Install

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e .
```

## Quickstart

Run these in under a minute:

```bash
task add "Buy potatoes" --due fri
task add "Finish assignment" --due 2026-12-13
task list
task done 1
task list --all
```

## Usage

| Command | Description |
|---|---|
| `task add "<title>" [--due DATE]` | Add a task. `--due` accepts `YYYY-MM-DD` or a weekday like `fri`. |
| `task list [--all]` | List open tasks (`--all` includes completed ones). |
| `task done <id>` | Mark the task with the given id as done. |

Full docs: run `zensical serve` in this directory and open
<http://localhost:8000>

## Configuration

| Environment variable | Default | Purpose |
|---|---|---|
| `TASKS_DB` | `~/.tasks.db` | Location of the SQLite database file. |

## Troubleshooting

- **`task: command not found`** - re-run `pip install -e .`, or add the
  scripts directory (e.g. `~/.local/bin`) to your `PATH`.
- **`ValueError: unrecognized date ...`** - `--due` must be `YYYY-MM-DD`
  or a weekday name such as `fri`.
- **The docs site does not update** - stop `zensical serve` and run
  `zensical build --strict` to see build errors (warnings become errors).

## Documentation

The docs live in [`docs/`](docs/) and are generated with
[Zensical](https://zensical.org/) (the successor to MkDocs, from the same team)
+ [mkdocstrings](https://mkdocstrings.github.io/), configured in
[`zensical.toml`](zensical.toml):

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-docs.txt
zensical serve      # live-reload preview at http://localhost:8000
zensical build      # static site into ./site (git-ignored)
```

The API reference is generated automatically from the docstrings in `src/`.
On every push to `main`, `.github/workflows/docs.yml` builds the site with
`zensical build --strict` and deploys it to **GitHub Pages** (repo
Settings → Pages → Source: GitHub Actions). On pull requests it runs the
tests and the strict docs build - a broken docs build blocks the merge.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Please open issues using the
**Bug report** or **Feature request** templates in this repository.

## License

[MIT](../LICENSE)
