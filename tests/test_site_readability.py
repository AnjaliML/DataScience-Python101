from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CSS_PATH = ROOT / "docs" / "stylesheets" / "extra.css"
README_PATH = ROOT / "README.md"
MKDOCS_PATH = ROOT / "mkdocs.yml"
FONT_PATH = ROOT / "docs" / "assets" / "fonts"
OVERRIDES_PATH = ROOT / "docs" / "overrides" / "partials"
ACCESSIBILITY_JS_PATH = ROOT / "docs" / "javascripts" / "accessibility.js"


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


@pytest.mark.parametrize(
    ("scheme", "foreground", "background", "minimum"),
    [
        ("ds-light", "--ds-copy", "--md-code-bg-color--lighter", 4.5),
        ("ds-dark", "--ds-copy", "--md-code-bg-color--lighter", 4.5),
        ("ds-light", "--ds-gridline", "--md-default-bg-color", 3.0),
        ("ds-dark", "--ds-gridline", "--md-default-bg-color", 3.0),
    ],
)
def test_audited_controls_have_visible_contrast(
    scheme: str,
    foreground: str,
    background: str,
    minimum: float,
) -> None:
    css = CSS_PATH.read_text(encoding="utf-8")
    variables = _variables(_block(css, ":root"))
    variables.update(_variables(_block(css, f'[data-md-color-scheme="{scheme}"]')))

    ratio = _contrast(_resolve(foreground, variables), _resolve(background, variables))
    assert ratio >= minimum, f"{scheme} {foreground} on {background}: {ratio:.2f}:1"


@pytest.mark.parametrize("scheme", ["ds-light", "ds-dark"])
def test_syntax_palette_meets_wcag_aa(scheme: str) -> None:
    css = CSS_PATH.read_text(encoding="utf-8")
    variables = _variables(_block(css, ":root"))
    variables.update(_variables(_block(css, f'[data-md-color-scheme="{scheme}"]')))
    tokens = {
        "--md-code-hl-number-color",
        "--md-code-hl-special-color",
        "--md-code-hl-function-color",
        "--md-code-hl-constant-color",
        "--md-code-hl-keyword-color",
        "--md-code-hl-string-color",
        "--md-code-hl-name-color",
        "--md-code-hl-operator-color",
        "--md-code-hl-punctuation-color",
        "--md-code-hl-comment-color",
        "--md-code-hl-generic-color",
        "--md-code-hl-variable-color",
    }
    background = _resolve("--md-code-bg-color", variables)

    for token in tokens:
        ratio = _contrast(_resolve(token, variables), background)
        assert ratio >= 4.5, f"{scheme} {token}: {ratio:.2f}:1"


def test_fonts_are_self_hosted_with_licences() -> None:
    css = CSS_PATH.read_text(encoding="utf-8")
    config = MKDOCS_PATH.read_text(encoding="utf-8")
    expected_fonts = {
        "ibm-plex-sans-latin-wght-normal.woff2",
        "ibm-plex-sans-latin-wght-italic.woff2",
        "ibm-plex-mono-latin-400-normal.woff2",
        "ibm-plex-mono-latin-600-normal.woff2",
        "source-serif-4-latin-wght-normal.woff2",
    }
    expected_licences = {
        "OFL-IBM-Plex-Sans.txt",
        "OFL-IBM-Plex-Mono.txt",
        "OFL-Source-Serif-4.txt",
    }

    assert "font: false" in config
    assert "https://" not in css
    for filename in expected_fonts | expected_licences:
        path = FONT_PATH / filename
        assert path.is_file() and path.stat().st_size > 1_000
    for filename in expected_fonts:
        assert filename in css


def test_application_shell_uses_named_button_controls() -> None:
    header = (OVERRIDES_PATH / "header.html").read_text(encoding="utf-8")
    search = (OVERRIDES_PATH / "search.html").read_text(encoding="utf-8")
    navigation = (OVERRIDES_PATH / "nav.html").read_text(encoding="utf-8")
    javascript = ACCESSIBILITY_JS_PATH.read_text(encoding="utf-8")

    assert '<button type="button"' in header
    assert 'aria-controls="site-navigation"' in header
    assert 'aria-expanded="false"' in header
    assert 'data-ds-toggle="drawer"' in header
    assert 'role="dialog"' in search and 'aria-labelledby="__search-title"' in search
    assert 'id="site-navigation"' in navigation
    assert "Escape" in javascript and "restoreFocus" in javascript
    assert 'setAttribute("aria-expanded"' in javascript


def test_tables_gain_a_named_keyboard_scroll_region() -> None:
    javascript = ACCESSIBILITY_JS_PATH.read_text(encoding="utf-8")
    css = CSS_PATH.read_text(encoding="utf-8")

    assert "region.tabIndex = overflow ? 0 : -1" in javascript
    assert 'region.setAttribute("role", "region")' in javascript
    assert 'region.setAttribute("aria-labelledby", caption.id)' in javascript
    assert "ResizeObserver" in javascript
    assert ".ds-table-region" in css
    assert "position: sticky" in css


def test_readme_inspiration_note_is_the_final_section() -> None:
    readme = README_PATH.read_text(encoding="utf-8")

    assert readme.count("comphy-lab/comphy-python101") == 1
    assert readme.index("## Inspiration") > readme.index("## License")
    assert readme.rstrip().endswith("physics-specific material removed.")
