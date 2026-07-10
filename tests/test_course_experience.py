from __future__ import annotations

import struct
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

LESSON_PRACTICE = {
    "01-questions": "01-questions",
    "02-python-basics": "02-python-basics",
    "03-functions-control": "03-functions-control",
    "04-numpy": "04-numpy",
    "05-pandas": "05-pandas",
    "06-cleaning": "06-cleaning",
    "07-visualization": "07-visualization",
    "08-statistics": "08-statistics",
    "09-modeling": "09-modeling",
    "10-evaluation": "10-evaluation",
    "11-reproducibility": "11-reproducibility",
    "12-tools": "12-tools",
    "13-capstone": "13-capstone",
}

PRACTICE_SEQUENCE = (
    "## Worked warm-up",
    "## Try",
    "## Hint 1",
    "## Hint 2",
    "## Tests or rubric",
    "## Worked reasoning",
)


@pytest.mark.parametrize(("lesson", "practice"), LESSON_PRACTICE.items())
def test_every_lesson_links_to_a_complete_practice_journey(
    lesson: str,
    practice: str,
) -> None:
    lesson_text = (DOCS / "lessons" / f"{lesson}.md").read_text(encoding="utf-8")
    practice_path = DOCS / "practice" / f"{practice}.md"
    practice_text = practice_path.read_text(encoding="utf-8")

    assert f"../practice/{practice}.md" in lesson_text
    positions = [practice_text.index(heading) for heading in PRACTICE_SEQUENCE]
    assert positions == sorted(positions)
    assert "??? tip" in practice_text
    assert "??? success" in practice_text


@pytest.mark.parametrize(
    ("practice", "starter", "required_terms"),
    [
        ("03-functions-control", "exercises/02-functions/starter.py", {"renewal_rate"}),
        ("04-numpy", "exercises/03-numpy/starter.py", {"standardize_columns"}),
        (
            "05-pandas",
            "exercises/04-dataframes/starter.py",
            {"summarise_plans", "customer_id"},
        ),
        ("06-cleaning", "exercises/05-cleaning/starter.py", {"quality_report"}),
        (
            "09-modeling",
            "exercises/06-modeling/starter.py",
            {"split_features_target", "fit_baseline"},
        ),
    ],
)
def test_repository_backed_practice_matches_the_starter_contract(
    practice: str,
    starter: str,
    required_terms: set[str],
) -> None:
    text = (DOCS / "practice" / f"{practice}.md").read_text(encoding="utf-8")

    assert starter in text
    for term in required_terms:
        assert term in text
    assert "supplied tests validate the **Completion** task" in text


def test_first_script_bridge_covers_the_beginner_execution_loop() -> None:
    text = (DOCS / "start" / "first-script.md").read_text(encoding="utf-8")

    for required in ("REPL", "scratch.py", "print(", "Traceback", "NameError"):
        assert required in text
    assert "15 minutes" in text


def test_quick_route_is_consistent_across_entry_points() -> None:
    entry_points = [
        ROOT / "README.md",
        DOCS / "index.md",
        DOCS / "start" / "overview.md",
    ]

    for path in entry_points:
        assert "14–18" in path.read_text(encoding="utf-8")
    assert "ten-lesson route" in (DOCS / "index.md").read_text(encoding="utf-8")
    assert "ten lessons" in (DOCS / "start" / "overview.md").read_text(encoding="utf-8")


def _png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    assert data.startswith(b"\x89PNG\r\n\x1a\n")
    return struct.unpack(">II", data[16:24])


def test_visualization_lesson_ships_real_readable_outputs() -> None:
    lesson = (DOCS / "lessons" / "07-visualization.md").read_text(encoding="utf-8")
    figures = (
        "monthly-usage-distribution.png",
        "usage-by-tenure.png",
        "renewal-rate-by-plan.png",
    )

    for filename in figures:
        path = DOCS / "assets" / "figures" / filename
        width, height = _png_dimensions(path)
        assert path.stat().st_size > 20_000
        assert width >= 900 and height >= 500
        assert f"../assets/figures/{filename}" in lesson
    assert lesson.count("![") >= 3
    assert "not show that" in lesson


def test_capstone_separates_reference_audit_from_learner_ownership() -> None:
    lesson = (DOCS / "lessons" / "13-capstone.md").read_text(encoding="utf-8")

    assert "## Track A — Reference audit" in lesson
    assert "## Track B — Learner-owned capstone" in lesson
    assert "Calling the supplied `build_capsule`" in lesson
    assert "at least **two material choices**" in lesson
