# Data Science Python 101

[![Course website](https://img.shields.io/badge/course-GitHub%20Pages-2457d6)](https://anjaliml.github.io/DataScience-Python101/)
[![Course checks](https://github.com/AnjaliML/DataScience-Python101/actions/workflows/ci.yml/badge.svg)](https://github.com/AnjaliML/DataScience-Python101/actions/workflows/ci.yml)
[![Pages](https://github.com/AnjaliML/DataScience-Python101/actions/workflows/pages.yml/badge.svg)](https://github.com/AnjaliML/DataScience-Python101/actions/workflows/pages.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-0f766e)](LICENSE)

Learn enough Python to make a trustworthy data-science claim—not merely to
make a notebook run.

> This guide was inspired by
> [CoMPhy Python 101](https://github.com/comphy-lab/comphy-python101) by Vatsal
> Sanjay and CoMPhy Lab contributors. It is an original data-science-focused
> rewrite with the CFD, Basilisk, and physics-specific material removed.

## The course spine

```text
question → data → transformation → validation → insight
```

Every lesson repeats five habits:

1. **Frame** the decision and its failure modes.
2. **Predict** the type, shape, distribution, or result before running code.
3. **Build** the smallest transformation that answers the question.
4. **Check** assumptions with tests, baselines, and adversarial cases.
5. **Explain** what the evidence supports—and what it does not.

## Two routes

| Route | Time | Best for |
| --- | ---: | --- |
| Quick route | 8–10 hours | Learners who already write a little Python |
| Full route | 28–32 hours | Beginners who want a complete foundation |

Both routes use the same lessons and exercises, so examples and fixes cannot
drift between separate versions.

## What you will build

- small Python functions with explicit inputs, outputs, and failure modes;
- NumPy transformations whose shapes and axes you can explain;
- pandas workflows that validate schemas before analysis;
- claim-led visualisations and uncertainty summaries;
- a leakage-safe baseline classification model;
- tests for data, transformations, and model behaviour;
- a command-line analysis that produces a reproducible report.

The included `customer_renewals.csv` dataset is synthetic. It represents no
real people or company and can be used offline.

## Run locally

```bash
git clone https://github.com/AnjaliML/DataScience-Python101.git
cd DataScience-Python101

# Recommended: install the locked environment.
uv sync --locked --all-extras

# Check the code and build the site.
uv run pytest
uv run mkdocs build --strict

# Preview the guide at http://127.0.0.1:8000
uv run mkdocs serve
```

Without `uv`, create a Python 3.11+ virtual environment and run
`python -m pip install -e ".[dev,docs]"`.

## Repository map

```text
docs/                 Course website and lessons
data/                 Small synthetic teaching data
src/ds_python101/     Tested reference workflow
exercises/            Starter tasks and learner instructions
solutions/            Worked solutions
examples/             Complete runnable examples
tests/                Unit and end-to-end checks
```

## License

The guide, examples, and code are available under the [MIT License](LICENSE).
