# Contributing to TaskMaster

Thanks for considering a contribution!

## How to report a bug or request a feature

1. Search the [issues](../../issues) first - your problem may already be reported.
2. Open a new issue using the **Bug report** or **Feature request** template.
   Fill in every required field: steps to reproduce, expected vs. actual
   behavior, and your environment (OS, Python version, commit).
3. One topic per issue. Keep bug reports minimal and reproducible.

## How to contribute code

1. Fork the repository and create a branch: `git checkout -b fix/thing`.
2. Install in editable mode and run the tests:

   ```bash
   python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -e . pytest
   pytest
   ```

3. Update the docs **in the same pull request** as the code change:
   edit `docs/*.md` and the docstrings in `src/`, then check
   `zensical serve` locally.
4. Open a pull request. Use the PR template and reference the issue it
   fixes, e.g. `Closes #12` - the issue closes automatically on merge.

## Style

- Docstrings follow the Google style (see `src/taskmaster/core.py`).
- Keep examples in docstrings and docs copy-pasteable.
- Be kind and follow the code of conduct.
