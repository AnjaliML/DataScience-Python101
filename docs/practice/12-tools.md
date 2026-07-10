# Practice 12 — Give the analysis one narrow front door

This on-site lab pairs with [lesson 12](../lessons/12-tools.md).

## Worked warm-up

A command-line interface has a boundary and a core. The boundary parses text,
reads files, writes artifacts, logs progress, and returns an exit status. The
core accepts ordinary Python values and returns ordinary Python values. Keeping
analysis logic out of `main()` makes it easier to test and reuse.

## Try

### Completion — finish a safe command

Use the pure `summarise_customers`, `write_text_atomic`, and `sha256` helpers
from lesson 12, then replace the four `___` placeholders in this coordinator:

```python
def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=___)
    parser.add_argument("--output-dir", type=Path, required=___)
    args = parser.parse_args(argv)

    try:
        customers = pd.read_csv(args.input)
        summary = summarise_customers(customers)  # validates its contract
        args.output_dir.mkdir(parents=True, exist_ok=True)
        summary_path = args.output_dir / "summary.json"
        write_text_atomic(
            summary_path,
            json.dumps(summary, indent=2, sort_keys=True) + "\n",
        )
        manifest = f"{sha256(summary_path)}  {summary_path.name}\n"
        write_text_atomic(args.output_dir / "manifest.sha256", manifest)
    except (FileNotFoundError, OSError, ValueError, pd.errors.ParserError) as error:
        LOGGER.error("%s", error)
        return ___

    LOGGER.info("wrote %s", args.output_dir)
    return ___
```

Both paths are required. Expected file or invalid-data failures return code `2`;
success returns `0`. Run the same command twice and compare output bytes.

### Transfer — add one option without tangling layers

Add `--minimum-tenure` as a non-negative integer. Put the filtering rule in a
pure function, test the function at `0`, the boundary value, and a negative
input, then connect it to argument parsing. Run the command from a different
working directory with explicit paths.

## Hint 1

??? tip "Reveal Hint 1"
    Give `argparse` the conversion and help text, but keep domain validation in
    a function whose contract can be called without a shell.

## Hint 2

??? tip "Reveal Hint 2"
    Catch expected boundary failures narrowly. Do not catch `Exception`, which
    would turn programming defects into vague user errors and hide tracebacks.

## Tests or rubric

Test success, missing input, invalid schema, invalid option, nested output
creation, deterministic rerun, unchanged raw input, atomic replacement, and a
manifest that names every public artifact. Assert both return codes and output
content; a zero exit status alone proves very little.

## Worked reasoning

??? success "Reveal worked reasoning"
    A pure tenure filter can be tested with a tiny frame before any file is
    opened. The CLI then coordinates path parsing, loading, that function, and
    writing. Stable key ordering and absence of current timestamps make JSON
    byte-repeatable. Expected user or data errors return a documented non-zero
    code; unexpected defects retain their traceback so they can be fixed.

    The four completion values are `True`, `True`, `2`, and `0`. Required
    arguments make the boundary explicit; narrow expected exceptions produce a
    useful process status without hiding unrelated programming defects.

Next: [lesson 13](../lessons/13-capstone.md) or
[practice 13](13-capstone.md).
