# Contributing

Small, teachable improvements are welcome. Keep each contribution focused enough that a reviewer can verify the lesson, code, and rendered page together.

## Start with an issue

Open an issue before a large curriculum change, new dependency, dataset addition, or navigation redesign. Include:

- the learner problem;
- the page or lesson affected;
- a small example of the proposed outcome;
- any accessibility, privacy, or maintenance implications.

Typos, broken links, and narrowly scoped corrections can go directly to a pull request.

Do not include private, licensed, or sensitive datasets in an issue or contribution. Use small synthetic examples when possible.

## Create a branch

Update your local default branch, then create a descriptive branch:

```bash
git switch main
git pull --ff-only
git switch -c docs/clarify-groupby-grain
```

Use a new branch for each independent change. Avoid mixing formatting, dependency updates, and curriculum revisions unless they must ship together.

## Write for learners

Course additions should:

- state the question or decision before code;
- ask learners to predict a value, type, shape, or behavior;
- explain the mechanism in plain language;
- include checks that could fail;
- distinguish structural validity from substantive meaning;
- use data-science examples without assuming prior programming knowledge;
- avoid unnecessary packages and unexplained shortcuts;
- include useful alternative text for informative images.

Code snippets should run in the documented environment. If a snippet is intentionally incomplete or expected to fail, say so immediately before it.

Prefer one clear method over several clever versions. Define technical terms when first used and keep units, row grain, and time cutoffs visible.

## Check the change

Review the files you changed:

```bash
git status --short
git diff --check
git diff
```

Run the project's automated checks and strict documentation build:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run mkdocs build --strict
```

If `uv` is not being used, run the equivalent commands in the activated environment:

```bash
ruff check .
ruff format --check .
python -m pytest
mkdocs build --strict
```

Preview the site when layout, navigation, code blocks, tables, images, or links change:

```bash
uv run mkdocs serve
```

Check the narrow and wide layouts, keyboard navigation, link targets, and visible focus states. Read instructional prose once without running code; it should still describe a coherent mechanism.

## Commit intentionally

Stage named files and inspect the staged patch:

```bash
git add docs/path/to/page.md
git diff --staged
git commit -m "Clarify groupby grain example"
```

Commit messages should describe the result. Do not commit virtual environments, generated site output, credentials, caches, or local notebook checkpoints.

## Open a pull request

Push the branch:

```bash
git push -u origin HEAD
```

In the pull request, include:

- what learner problem is solved;
- which pages or behavior changed;
- how the code and site were checked;
- screenshots for meaningful visual changes;
- any remaining tradeoff or follow-up.

Keep review discussion attached to evidence. When feedback changes the approach, update the branch and note what was rechecked.

## Review standard

A contribution is ready when another person can:

1. understand the intended learning outcome;
2. run the example from a clean environment;
3. predict and verify the important behavior;
4. identify the assumptions and failure boundary;
5. render and navigate the changed pages without warnings.

Maintainers may ask to split an oversized change or simplify a dependency. That keeps review and future maintenance proportional to the learning benefit.
