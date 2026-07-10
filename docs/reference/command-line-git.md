# Command line and Git

The command line runs programs in a current directory. Git records intentional snapshots of files. Use both slowly enough that you can explain what each command will read or change.

## Orient yourself first

```bash
pwd                 # print the current directory
ls                  # list its visible contents
ls -la              # include hidden entries such as .git
cd path/to/project  # move into a directory
cd ..               # move to the parent directory
```

Before a project command, confirm that `pwd` shows the repository root and `ls` shows files such as `pyproject.toml`, `mkdocs.yml`, or `README.md`.

Paths containing spaces need quotes, for example `cd "path/with spaces/project"`.

Use the Up arrow to recall a command and `Ctrl-C` to stop a running command. Do not paste a command you cannot describe.

## Create an isolated environment

A virtual environment keeps one project's packages separate from the rest of your computer.

With standard Python:

```bash
python3 -m venv .venv
source .venv/bin/activate       # macOS or Linux
python -m pip install --upgrade pip
python -m pip install -e ".[dev,docs]"
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`. Leave an activated environment with `deactivate`.

If the project uses `uv`, it can create the environment and install the locked dependencies:

```bash
uv sync --locked --all-extras
```

You can activate `.venv` or let `uv run` select the environment for each command.

## Run Python and project tools

Start an interactive session, run the course example, or inspect its command-line interface:

```bash
python
uv run python examples/reproduce_analysis.py
uv run python -m ds_python101 --help
uv run ds-python101 --help
uv run ds-python101 --input data/customer_renewals.csv --output-dir artifacts --seed 42
uv --help
```

Run tests and the documentation site from the repository root:

```bash
python -m pytest
mkdocs serve
mkdocs build --strict
```

Or, in a `uv` project:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run mkdocs serve
uv run mkdocs build --strict
```

`mkdocs serve` stays running while it previews the site. Stop it with `Ctrl-C`. A successful command normally exits with status `0`; read the first relevant error, not only the final summary.

## Inspect Git before changing it

```bash
git status --short --branch
git diff
git diff --stat
git log --oneline --decorate -10
git remote -v
```

`git diff` shows unstaged edits. `git diff --staged` shows what the next commit would include. Untracked files appear in `git status` but not in a normal diff.

## Make a focused commit

Create a branch for one coherent change:

```bash
git switch -c lesson/clearer-numpy-checks
```

Inspect, stage named files, and inspect again:

```bash
git status --short
git diff
git add docs/lessons/04-numpy.md
git diff --staged
```

Commit with a message that describes the result:

```bash
git commit -m "Clarify NumPy shape checks"
```

Avoid `git add .` until you have verified every changed and untracked file belongs in the same commit.

## Synchronize safely

Before pulling, finish or deliberately save your local work. Then update without inventing a merge commit:

```bash
git pull --ff-only
```

If Git reports that a fast-forward is impossible, stop and inspect the branch history. Do not guess at a rebase or force push on shared work.

Publish the current branch:

```bash
git push -u origin HEAD
```

Later pushes can usually use `git push`. Never force-push unless you understand who else uses the branch and have agreed to rewrite its history.

## Undo with evidence

To unstage a file while keeping its working copy:

```bash
git restore --staged path/to/file
```

`git restore path/to/file` discards unstaged edits in that file. Before using it, inspect `git diff -- path/to/file` and copy irreplaceable work elsewhere. The discarded content may not be recoverable.

To reverse a published commit, prefer a new commit that records the reversal:

```bash
git revert COMMIT_ID
```

Avoid destructive shortcuts such as `git reset --hard` and `git clean -fd`. They can erase unrelated or untracked work. When status is confusing, stop, capture `git status` and relevant diffs, and ask for review.

## A reliable rhythm

1. Orient with `pwd`, `ls`, and `git status`.
2. Predict which files a command can change.
3. Make one focused edit or run one check.
4. Review `git diff`.
5. Run tests and build the site.
6. Stage named files and review `git diff --staged`.
7. Commit, pull safely, and push the branch.
