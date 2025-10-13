# BDD Test Suite

This directory contains BDD artifacts (Gherkin feature files and pytest-bdd step definitions) for end-to-end and integration behaviors.

Structure
- `bdd/features/` - feature (.feature) files written in Gherkin
- `bdd/steps/` - pytest-bdd step definition modules
- `bdd/helpers/` - small test helpers and mocks used by step defs

Running BDD tests (local, using project venv)

Use the project's Python virtual environment and the requirements files. The project provides a CI helper script that can create/update the venv and install dependencies.
```cmd
Windows (Git Bash / cmd.exe) example:
```bash
python -m venv .venv
# Git Bash:
source .venv/bin/activate
# cmd.exe:
# .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

```cmd
Playwright note (E2E): after installing `playwright` you must fetch browser binaries:
```
Windows (Git Bash / cmd.exe):
```bash
# Git Bash or WSL: .venv/bin/python -m playwright install
# cmd.exe: .venv\Scripts\python -m playwright install
- Keep BDD tests focused on behavior and integration scenarios; unit tests remain in the `tests/` directory.

Run the BDD suite (separate from unit tests):
```bash
# with venv active
pytest bdd -q
