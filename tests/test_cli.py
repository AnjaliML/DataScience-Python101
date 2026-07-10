import json
from pathlib import Path

from ds_python101.cli import main

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "customer_renewals.csv"


def test_cli_builds_capsule(tmp_path: Path, capsys: object) -> None:
    status = main(
        [
            "--input",
            str(DATA_PATH),
            "--output-dir",
            str(tmp_path),
            "--seed",
            "7",
        ]
    )

    assert status == 0
    captured = capsys.readouterr()  # type: ignore[attr-defined]
    payload = json.loads(captured.out)
    assert payload["rows"] == 240
    assert Path(payload["manifest"]).is_file()


def test_cli_returns_nonzero_for_missing_input(tmp_path: Path, capsys: object) -> None:
    status = main(
        [
            "--input",
            str(tmp_path / "missing.csv"),
            "--output-dir",
            str(tmp_path / "output"),
        ]
    )

    assert status == 2
    captured = capsys.readouterr()  # type: ignore[attr-defined]
    assert "data file not found" in captured.err
