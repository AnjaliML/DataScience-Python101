"""Command-line entry point for the reproducible course analysis."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ds_python101.capsule import build_capsule
from ds_python101.data import DataValidationError


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line contract."""

    parser = argparse.ArgumentParser(
        prog="ds-python101",
        description="Build the Data Science Python 101 analysis capsule.",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/customer_renewals.csv"),
        help="input customer CSV (default: %(default)s)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts"),
        help="directory for generated outputs (default: %(default)s)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="random seed for the train/test split (default: %(default)s)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Build the analysis and return a process-friendly exit status."""

    arguments = build_parser().parse_args(argv)
    try:
        result = build_capsule(
            arguments.input,
            arguments.output_dir,
            random_state=arguments.seed,
        )
    except (DataValidationError, FileNotFoundError, OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    print(json.dumps(result, sort_keys=True))
    return 0
