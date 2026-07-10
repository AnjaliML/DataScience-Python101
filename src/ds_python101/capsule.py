"""Build and verify the capstone's reproducible output capsule."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd

from ds_python101.analysis import (
    FEATURES,
    POSITIVE_CLASS,
    renewal_summary,
    train_and_evaluate,
)
from ds_python101.data import load_customer_data
from ds_python101.plotting import plot_confusion, plot_renewal_by_plan, save_figure

OUTPUT_NAMES = (
    "cleaned.csv",
    "summary.json",
    "renewal-by-plan.png",
    "metrics.json",
    "confusion-matrix.png",
)
ALLOWED_OUTPUT_NAMES = {*OUTPUT_NAMES, "manifest.sha256"}


def _write_json(payload: object, destination: Path) -> None:
    destination.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_manifest(output_dir: Path) -> Path:
    lines = []
    for name in sorted(OUTPUT_NAMES):
        digest = hashlib.sha256((output_dir / name).read_bytes()).hexdigest()
        lines.append(f"{digest}  {name}")
    destination = output_dir / "manifest.sha256"
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return destination


def build_capsule(
    input_path: str | Path,
    output_dir: str | Path,
    *,
    random_state: int = 42,
) -> dict[str, object]:
    """Validate data and write every documented analysis artifact."""

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    unexpected = sorted(
        path.name
        for path in destination.iterdir()
        if path.name not in ALLOWED_OUTPUT_NAMES
    )
    if unexpected:
        raise ValueError(f"output directory contains unexpected entries: {unexpected}")
    source = Path(input_path)
    customers = load_customer_data(source)
    raw = pd.read_csv(source)
    cleaned = customers.assign(
        satisfaction_score_missing=customers["satisfaction_score"].isna()
    )
    cleaned.to_csv(destination / "cleaned.csv", index=False, lineterminator="\n")

    summary = {
        "source": {
            "file": source.name,
            "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        },
        "source_rows": int(len(raw)),
        "cleaned_rows": int(len(cleaned)),
        "original_missingness": {
            str(column): int(count) for column, count in raw.isna().sum().items()
        },
        "plan_counts": {
            str(name): int(count)
            for name, count in customers["plan"].value_counts().sort_index().items()
        },
        "target_counts": {
            str(int(name)): int(count)
            for name, count in customers["renewed"].value_counts().sort_index().items()
        },
        "renewal_rate": float(customers["renewed"].mean()),
        "features": list(FEATURES),
        "target_definition": {
            "raw_column": "renewed",
            "zero": "did not renew",
            "one": "renewed",
            "evaluation_positive_class": POSITIVE_CLASS,
        },
        "split": {"seed": random_state, "test_fraction": 0.25},
        "exclusions": [],
        "repairs": [
            "trimmed and lowercased plan and signup_channel",
            "parsed numeric columns",
            "added satisfaction_score_missing indicator to cleaned.csv",
        ],
        "descriptive_summary": renewal_summary(customers),
    }
    _write_json(summary, destination / "summary.json")
    save_figure(
        plot_renewal_by_plan(customers),
        destination / "renewal-by-plan.png",
    )

    result = train_and_evaluate(customers, random_state=random_state)
    metrics = {
        "positive_class": POSITIVE_CLASS,
        "threshold": result.decision_threshold,
        "threshold_rule": result.threshold_rule,
        "baseline": result.baseline_metrics,
        "logistic_regression": result.metrics,
        "cross_validation": result.cross_validation,
        "confusion_matrix": result.confusion,
        "holdout_rows": int(len(result.y_test)),
        "subgroups": result.subgroup_metrics,
        "limitations": [
            "The dataset is synthetic and does not estimate real customer behaviour.",
            "Observed associations do not show that changing a feature causes renewal.",
            (
                "The threshold was selected for training-fold F1, "
                "not a measured action cost."
            ),
            "Small holdout subgroups make their error rates unstable.",
        ],
    }
    _write_json(metrics, destination / "metrics.json")
    save_figure(plot_confusion(result.confusion), destination / "confusion-matrix.png")
    manifest = _write_manifest(destination)

    return {
        "rows": int(len(customers)),
        "output_dir": str(destination.resolve()),
        "manifest": str(manifest.resolve()),
    }


def read_cleaned(path: str | Path) -> pd.DataFrame:
    """Read a capsule's cleaned table for examples and review."""

    return pd.read_csv(path)
