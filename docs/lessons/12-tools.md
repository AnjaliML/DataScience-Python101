# 12 — Tools: give the analysis one front door

A reusable analysis accepts choices as arguments, keeps computation separate
from I/O, fails usefully, and writes observable outputs.

## Frame

An absolute source path such as `/Users/me/Desktop/final/customers-v3.csv` is a
caller choice disguised as code. A command-line interface makes it explicit:

~~~bash
uv run ds-python101 --input data/customer_renewals.csv \
  --output-dir build/renewal-summary
~~~

## Predict

Before writing the command, decide its required input, configurable output,
successful artifacts, expected user errors, unexpected failures, and rerun
policy. Those decisions are part of the tool’s contract.

## Build

Keep the analytical core independent of paths, printing, and process state:

~~~python
import pandas as pd

def summarise_customers(frame: pd.DataFrame) -> dict[str, object]:
    required = {"customer_id", "plan", "renewed"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"missing columns: {sorted(missing)}")
    if frame.empty:
        raise ValueError("input contains no rows")
    if frame["customer_id"].duplicated().any():
        raise ValueError("customer_id must be unique")

    renewal_map = {
        "true": 1, "false": 0, "yes": 1, "no": 0,
        "1": 1, "0": 0, "1.0": 1, "0.0": 0,
    }
    renewed = (
        frame["renewed"].astype("string").str.strip().str.lower()
        .map(renewal_map)
    )
    if renewed.isna().any():
        raise ValueError("renewed contains missing or unknown values")

    plans = (
        frame["plan"].astype("string").fillna("<missing>")
        .value_counts().sort_index()
    )
    return {
        "rows": int(len(frame)),
        "renewal_rate": float(renewed.mean()),
        "plan_counts": {str(key): int(value) for key, value in plans.items()},
    }
~~~

This function is easy to test with a three-row DataFrame. File handling belongs
at the edge. Write outputs atomically so a failed run does not leave a partial
file that looks complete:

~~~python
import hashlib
import json
from pathlib import Path

def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()

def write_text_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)
~~~

Now add a thin `argparse` boundary:

~~~python
import argparse
import logging
from collections.abc import Sequence

LOGGER = logging.getLogger(__name__)

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ds-python101",
        description="Validate and summarise customer renewal data.",
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument(
        "--output-dir", type=Path, required=True, help="output directory"
    )
    parser.add_argument("--verbose", action="store_true")
    return parser

def main(arguments: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(arguments)
    level = logging.INFO if args.verbose else logging.WARNING
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")

    try:
        customers = pd.read_csv(args.input)
        summary = summarise_customers(customers)
        summary_path = args.output_dir / "summary.json"
        write_text_atomic(
            summary_path,
            json.dumps(summary, indent=2, sort_keys=True) + "\n",
        )

        tracked = [args.input, summary_path]
        manifest_text = "".join(
            f"{sha256(path)}  {path.name}\n" for path in tracked
        )
        write_text_atomic(args.output_dir / "manifest.sha256", manifest_text)
    except (OSError, ValueError, pd.errors.ParserError) as error:
        LOGGER.error("%s", error)
        return 2

    LOGGER.info("wrote %s", args.output_dir)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
~~~

`main` coordinates reading, computation, and writing; it does not contain the
analytical rule itself. Exit code `0` means success. Code `2` marks an expected
input or file failure. Unexpected programming errors keep their traceback
instead of being hidden by `except Exception`.

## Check

Call functions directly in tests rather than spawning a process for every
claim:

~~~python
def test_summary_command(tmp_path):
    output = tmp_path / "report"
    arguments = [
        "--input",
        "data/customer_renewals.csv",
        "--output-dir", str(output),
    ]
    assert main(arguments) == 0
    summary = output / "summary.json"
    assert summary.is_file() and (output / "manifest.sha256").is_file()
    first = summary.read_bytes()
    assert main(arguments) == 0
    assert summary.read_bytes() == first
~~~

Rerunning replaces complete files atomically and produces the same JSON for the
same bytes and code. Do not skip work merely because an output exists; validate
its manifest or rebuild it.

## Explain

The shell supplies text arguments. `argparse` validates their structure and
converts paths. The boundary reads a table, the pure core returns ordinary
Python data, and the writer serializes deterministic artifacts. Logging helps a
human follow the run; exit status lets another program decide whether it
succeeded.

Use `pathlib`, never manual slash concatenation. Give outputs stable names,
sort serialized keys, avoid timestamps inside deterministic artifacts, and
record checksums for traceability.

## Practice

1. Add a `--minimum-tenure` argument and keep its filter in a function.
2. Make a missing input return code `2` with a useful message.
3. Fail on an unknown target, then rerun from elsewhere with absolute paths.

## Guided practice journey

[Work through Try → Hint 1 → Hint 2 → tests → worked reasoning](../practice/12-tools.md).
You will complete a safe command before adding one independently tested option.
