from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CSS_PATH = ROOT / "docs" / "stylesheets" / "extra.css"
README_PATH = ROOT / "README.md"


def _block(css: str, selector: str) -> str:
    start = css.index(selector)
    opening = css.index("{", start)
    depth = 0
    for position in range(opening, len(css)):
        if css[position] == "{":
            depth += 1
        elif css[position] == "}":
            depth -= 1
            if depth == 0:
                return css[opening + 1 : position]
    raise AssertionError(f"unclosed CSS block for {selector}")


def _variables(block: str) -> dict[str, str]:
    return {
        name: value.strip()
        for name, value in re.findall(r"(--[\w-]+):\s*([^;]+);", block)
    }


def _resolve(name: str, variables: dict[str, str]) -> str:
    value = variables[name]
    seen = {name}
    while value.startswith("var("):
        referenced = value.removeprefix("var(").removesuffix(")").strip()
        if referenced in seen:
            raise AssertionError(f"circular CSS variable: {referenced}")
        seen.add(referenced)
        value = variables[referenced]
    return value


def _luminance(hex_color: str) -> float:
    assert re.fullmatch(r"#[0-9a-fA-F]{6}", hex_color), hex_color
    channels = [int(hex_color[index : index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [
        channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4
        for channel in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def _contrast(first: str, second: str) -> float:
    lighter, darker = sorted(
        (_luminance(first), _luminance(second)),
        reverse=True,
    )
    return (lighter + 0.05) / (darker + 0.05)


def test_both_palettes_define_material_readability_contract() -> None:
    css = CSS_PATH.read_text(encoding="utf-8")
    required = {
        "--md-default-fg-color",
        "--md-default-fg-color--light",
        "--md-default-fg-color--lighter",
        "--md-default-fg-color--lightest",
        "--md-default-bg-color",
        "--md-code-fg-color",
        "--md-code-bg-color",
        "--md-typeset-color",
        "--md-typeset-a-color",
        "--md-typeset-table-color",
        "--md-admonition-fg-color",
        "--md-admonition-bg-color",
    }

    for scheme, color_scheme in (("ds-light", "light"), ("ds-dark", "dark")):
        block = _block(css, f'[data-md-color-scheme="{scheme}"]')
        variables = _variables(block)
        assert required <= set(variables)
        assert f"color-scheme: {color_scheme};" in block
        assert variables["--md-typeset-color"] == "var(--md-default-fg-color)"


@pytest.mark.parametrize(
    ("scheme", "foreground", "background"),
    [
        ("ds-light", "--ds-ink", "--md-default-bg-color"),
        ("ds-light", "--ds-muted", "--md-default-bg-color"),
        ("ds-light", "--md-typeset-a-color", "--md-default-bg-color"),
        ("ds-light", "--ds-teal", "--md-default-bg-color"),
        ("ds-light", "--ds-coral", "--ds-panel"),
        ("ds-dark", "--ds-ink", "--md-default-bg-color"),
        ("ds-dark", "--ds-muted", "--md-default-bg-color"),
        ("ds-dark", "--md-typeset-a-color", "--md-default-bg-color"),
        ("ds-dark", "--ds-teal", "--md-default-bg-color"),
        ("ds-dark", "--ds-coral", "--ds-panel"),
    ],
)
def test_palette_text_meets_wcag_aa(
    scheme: str,
    foreground: str,
    background: str,
) -> None:
    css = CSS_PATH.read_text(encoding="utf-8")
    variables = _variables(_block(css, ":root"))
    variables.update(_variables(_block(css, f'[data-md-color-scheme="{scheme}"]')))

    ratio = _contrast(_resolve(foreground, variables), _resolve(background, variables))
    assert ratio >= 4.5, f"{scheme} {foreground} on {background}: {ratio:.2f}:1"


def test_readme_inspiration_note_is_the_final_section() -> None:
    readme = README_PATH.read_text(encoding="utf-8")

    assert readme.count("comphy-lab/comphy-python101") == 1
    assert readme.index("## Inspiration") > readme.index("## License")
    assert readme.rstrip().endswith("physics-specific material removed.")
