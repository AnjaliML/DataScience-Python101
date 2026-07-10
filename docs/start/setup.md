# Set up once

The goal is a project that runs the same way tomorrow and on another computer.
Do the setup carefully once; then use the same commands throughout the course.

## What you need

- Git;
- a terminal;
- Python 3.11 or newer;
- a text editor or IDE;
- about 500 MB of free space for the environment.

The recommended environment manager is `uv`, but a standard Python virtual
environment also works.

## Get the course

```bash
git clone https://github.com/AnjaliML/DataScience-Python101.git
cd DataScience-Python101
```

Confirm where you are before installing anything:

```bash
pwd
git status
git remote -v
```

`git status` should report the expected branch and a clean working tree.
`git remote -v` should show the course repository URL.

## Recommended setup with uv

Install `uv` using its official instructions, then run:

```bash
uv sync --locked --all-extras
```

The command reads `pyproject.toml` and `uv.lock`, creates `.venv`, and installs
the exact locked environment. Run tools through that environment:

```bash
uv run python --version
uv run pytest
uv run mkdocs build --strict
```

The last two commands should pass before you change any exercise code. That
gives you a known-good starting point.

## Standard virtual-environment setup

If you do not use `uv`:

=== "macOS or Linux"

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    python -m pip install -e ".[dev,docs]"
    ```

=== "Windows PowerShell"

    ```powershell
    py -m venv .venv
    .venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    python -m pip install -e ".[dev,docs]"
    ```

When the environment is active, your prompt usually begins with `(.venv)`.
Confirm the interpreter location:

```bash
python -c "import sys; print(sys.executable)"
```

It should point inside this repository's `.venv` directory.

## Choose where to write code

Any editor that saves ordinary text files is enough. Useful options include
VS Code, PyCharm, Zed, and a terminal editor.

You may use a notebook for exploration. The course's canonical exercises are
Python files because they expose execution order, work with tests, and run in
continuous integration. If a notebook contains logic you want to keep, move
that logic into a function under `src/` or an exercise file.

## Run a first inspection

```bash
uv run python -c "import pandas as pd; customers = pd.read_csv('data/customer_renewals.csv'); print(customers.shape); print(customers.head(3))"
```

Before running it, predict:

- the Python type bound to `customers`;
- how many values the tuple in `customers.shape` contains;
- whether `head(3)` changes the original table.

Then compare the output with your prediction.

## Preview the website

```bash
uv run mkdocs serve
```

Open `http://127.0.0.1:8000`. Stop the server with ++ctrl+c++.

## Common setup failures

### `python` or `uv` is not found

The program is either not installed or its location is not on your shell's
`PATH`. Close and reopen the terminal after installation, then check:

```bash
python3 --version
uv --version
```

### Imports work in one place but not another

Your editor and terminal are probably using different Python interpreters.
Select the interpreter inside `.venv`, then restart the editor's Python tools.

### A test fails before you edit anything

Do not start repairing course code. Record:

```text
command:
Python version:
first failing test:
final traceback line:
```

Then compare your environment with `.python-version` and the lock file.

### A file path fails

Print the current directory with `pwd`. Course commands assume you run them
from the repository root unless a lesson says otherwise.

## Your setup contract

You are ready when all of these are true:

- [ ] `uv run python --version` reports 3.11 or newer;
- [ ] `uv run pytest` passes before exercise edits;
- [ ] `uv run mkdocs build --strict` succeeds;
- [ ] Python can read `data/customer_renewals.csv`;
- [ ] `git status` makes sense to you.

With an activated standard virtual environment, omit the `uv run` prefix.

Next: [learn how to use prediction and checks](how-to-learn.md).
