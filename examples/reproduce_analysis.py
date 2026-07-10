"""Build the complete course analysis using repository-relative paths."""

from pathlib import Path

from ds_python101.capsule import build_capsule

ROOT = Path(__file__).resolve().parents[1]


if __name__ == "__main__":
    result = build_capsule(
        ROOT / "data" / "customer_renewals.csv",
        ROOT / "artifacts",
    )
    print(f"built {result['rows']} rows in {result['output_dir']}")
