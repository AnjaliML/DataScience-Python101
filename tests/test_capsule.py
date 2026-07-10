import hashlib
import json
from pathlib import Path

import pytest

from ds_python101.capsule import OUTPUT_NAMES, build_capsule

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "customer_renewals.csv"


def test_capsule_writes_documented_outputs(tmp_path: Path) -> None:
    result = build_capsule(DATA_PATH, tmp_path, random_state=42)

    assert result["rows"] == 240
    expected = {*OUTPUT_NAMES, "manifest.sha256"}
    assert {path.name for path in tmp_path.iterdir()} == expected

    summary = json.loads((tmp_path / "summary.json").read_text())
    metrics = json.loads((tmp_path / "metrics.json").read_text())
    assert summary["source_rows"] == 240
    assert summary["cleaned_rows"] == 240
    assert summary["original_missingness"]["satisfaction_score"] == 18
    assert len(summary["source"]["sha256"]) == 64
    assert set(metrics) == {
        "positive_class",
        "threshold",
        "threshold_rule",
        "baseline",
        "logistic_regression",
        "cross_validation",
        "confusion_matrix",
        "holdout_rows",
        "subgroups",
        "limitations",
    }
    assert metrics["holdout_rows"] == 60
    assert metrics["positive_class"] == "not_renewed"
    assert set(metrics["cross_validation"]) == {
        "accuracy",
        "precision",
        "recall",
        "f1",
        "roc_auc",
    }
    assert {row["plan"] for row in metrics["subgroups"]} == {
        "basic",
        "plus",
        "pro",
    }
    assert len(metrics["limitations"]) == 4


def test_manifest_matches_every_output(tmp_path: Path) -> None:
    build_capsule(DATA_PATH, tmp_path)

    entries = {}
    for line in (tmp_path / "manifest.sha256").read_text().splitlines():
        digest, name = line.split("  ", maxsplit=1)
        entries[name] = digest

    assert set(entries) == set(OUTPUT_NAMES)
    assert list(entries) == sorted(OUTPUT_NAMES)
    for name, expected_digest in entries.items():
        actual_digest = hashlib.sha256((tmp_path / name).read_bytes()).hexdigest()
        assert actual_digest == expected_digest


def test_capsule_refuses_to_overwrite_unrelated_output(tmp_path: Path) -> None:
    (tmp_path / "notes.txt").write_text("keep me")

    with pytest.raises(ValueError, match="unexpected entries"):
        build_capsule(DATA_PATH, tmp_path)

    assert (tmp_path / "notes.txt").read_text() == "keep me"
