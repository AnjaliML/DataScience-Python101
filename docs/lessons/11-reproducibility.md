# 11 — Reproducibility: make the path visible

A result is reproducible when another person can start from declared inputs,
run declared code in a declared environment, and rebuild the same artifacts.
“The notebook worked yesterday” is not an execution contract.

## Frame

The renewal analysis depends on more than a fitted model:

~~~text
question + raw data + cleaning rules + split + preprocessing + model
         + evaluation + environment + command + provenance
~~~

If any part lives only in memory, a plausible-looking figure may be impossible
to explain or rebuild later.

## Predict

Predict which survive a fresh clone: a local absolute path, an undeclared
package, an uncommitted notebook cell, a seed stored in source, a documented
raw CSV, and an ignored figure rebuilt by one command. The last two can be
reproducible even though only one is tracked.

## Build

Use a layout that separates sources from products:

~~~text
project/
├── README.md
├── pyproject.toml
├── uv.lock
├── data/
│   ├── README.md
│   └── customer_renewals.csv
├── src/ds_python101/       # reusable analysis modules
├── tests/
├── notebooks/
├── build/                 # generated, not hand-edited
└── .github/workflows/
~~~

Raw inputs remain unchanged. Cleaning writes a new file under `build/` or a
clearly named processed-data directory. Figures and metrics are downstream
products, never the only record of the values behind them.

Anchor repository-owned paths to source, not the caller’s current directory:

~~~python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW_DATA = ROOT / "data" / "customer_renewals.csv"
~~~

Inputs that genuinely vary should still be command-line arguments. Constants
such as the teaching seed can have one named source of truth:

~~~python
RANDOM_SEED = 101
TEST_SIZE = 0.25
~~~

A seed controls pseudo-random choices; it does not remove sampling uncertainty.
Record it so a split can be replayed, then use cross-validation or sensitivity
checks to learn whether the result depends heavily on that split.

### Declare the environment

`pyproject.toml` names direct dependencies and supported Python versions.
`uv.lock` records the resolved environment that passed the checks.

~~~bash
uv sync --locked --all-extras
uv run pytest
uv run mkdocs build --strict
~~~

The lock file is not a promise to freeze software forever. It is a replayable
record. Update dependencies deliberately, then rerun tests and review changed
outputs.

### Record provenance

A checksum detects byte-level change in an input:

~~~python
import hashlib

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
~~~

Pair the checksum with meaning:

~~~python
provenance = {
    "source": str(RAW_DATA.relative_to(ROOT)),
    "source_sha256": sha256(RAW_DATA),
    "row_unit": "one customer renewal opportunity",
    "target": "renewed",
    "random_seed": RANDOM_SEED,
    "test_size": TEST_SIZE,
}
~~~

A checksum cannot tell you whether the source is representative, lawful, or
correctly defined. The data README must describe origin, schema, permissions,
known exclusions, and whether the records are synthetic.

### Keep notebooks exploratory

Use notebooks to inspect a table, try a plot, or discuss intermediate output.
Before sharing one, restart the kernel and run every cell from top to bottom.
Move cleaning, feature preparation, modeling, plotting, and metrics into
importable functions when another artifact depends on them.

The notebook may import and call source-of-truth functions. It should not
contain a second, slightly different implementation.

### Use Git as reasoning history

Commit coherent changes and inspect them before sharing:

~~~bash
git status --short
git diff
git add src/ds_python101/modeling.py tests/test_modeling.py
git commit -m "Add leakage-safe renewal baseline"
~~~

Do not commit secrets, private records, local absolute paths, virtual
environments, caches, or large accidental notebook outputs.

## Check

Tests should protect contracts rather than preferred conclusions:

~~~python
def test_training_is_repeatable(clean_customers):
    first = fit_renewal_model(clean_customers, random_seed=101)
    second = fit_renewal_model(clean_customers, random_seed=101)
    assert first.metrics == second.metrics

def test_raw_input_is_not_modified(tmp_path, raw_copy):
    before = sha256(raw_copy)
    build_report(raw_copy, output=tmp_path)
    assert sha256(raw_copy) == before
~~~

Continuous integration repeats the clean-machine check on pushes and pull
requests: install the locked environment, lint, test, build documentation, and
only then deploy. CI proves that the declared workflow ran; it does not prove
that the data or interpretation are fair and valid.

## Explain

Reproducibility removes hidden degrees of freedom. A reviewer can see the exact
input, code version, environment, seed, transformations, test policy, and
outputs. That visibility makes disagreement useful: assumptions can be changed
and the consequences rebuilt.

## Practice

1. Move one notebook calculation into a tested function.
2. Run the analysis from another directory and recreate the locked environment.
3. Change one input byte and confirm its checksum changes.
4. Ask a classmate to rebuild the result without verbal instructions.

## Guided practice journey

[Work through Try → Hint 1 → Hint 2 → rubric → worked reasoning](../practice/11-reproducibility.md).
You will complete a provenance record before testing it from a clean state.

## Keep going

The next lesson gives this reproducible project one narrow command-line front
door with explicit paths, useful failures, deterministic outputs, and a
checksum manifest.
