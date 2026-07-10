# Your first 15 minutes with Python

This bridge is for someone who has never run a program. By the end, you will
have used Python in two ways, saved a script, caused one harmless error, and
read the useful part of its traceback.

You cannot damage the course data in this activity. Work in a new file called
`scratch.py` in the repository root, and delete it later if you wish.

## Minute 0–3: meet the prompt

A **terminal** is a text interface for starting programs. A line ending in `$`,
`%`, or `>` is usually the terminal prompt; do not type that prompt itself.

From the course folder, start Python:

=== "With uv"

    ```bash
    uv run python
    ```

=== "Active virtual environment"

    ```bash
    python
    ```

Python displays a prompt like `>>>`. This interactive mode is the **REPL**:
Read, Evaluate, Print, Loop. Type one expression and press Enter:

```pycon
>>> 2 + 3
5
>>> hours = 12
>>> hours * 4
48
```

The REPL is good for one tiny experiment. Its history is not a dependable
analysis. Exit with `exit()` (or ++ctrl+d++ on macOS/Linux).

## Minute 3–7: save a script

Create `scratch.py` in your editor and type this code:

```python title="scratch.py"
customer = "C1042"
monthly_hours = 12
annual_hours = monthly_hours * 12

print(customer)
print(annual_hours)
```

Before running it, predict the two printed lines. Save the file, then run:

=== "With uv"

    ```bash
    uv run python scratch.py
    ```

=== "Active virtual environment"

    ```bash
    python scratch.py
    ```

Expected output:

```text
C1042
144
```

Python executes a script from top to bottom. Names created on earlier lines are
available to later lines. `print(...)` makes a value visible; it does not
change the value.

## Minute 7–11: cause a useful error

Change the final line to use a name that does not exist:

```python
print(annual_hour)
```

Predict what will happen, save, and rerun. You should see a traceback ending
approximately like this:

```text
Traceback (most recent call last):
  File ".../scratch.py", line 6, in <module>
    print(annual_hour)
          ^^^^^^^^^^^
NameError: name 'annual_hour' is not defined
```

Read a traceback from the bottom upward:

1. `NameError` is the kind of failed contract.
2. The message names the missing name.
3. The nearest `scratch.py` line points to code you own.
4. The caret points near the expression Python could not evaluate.

The traceback is evidence, not a judgement. Here the smallest explanation is a
missing `s`: the script created `annual_hours` but asked for `annual_hour`.
Restore the final line and confirm the script runs again.

## Minute 11–15: change, predict, check

Change `monthly_hours` to `7.5`. Before running, write down:

- the expected value of `annual_hours`;
- whether that value is a whole number or a decimal;
- the two output lines.

Run the file and compare observed with expected. If they differ, keep both
notes: the disagreement is where learning happens.

## REPL or script?

| Use the REPL when… | Use a script when… |
| --- | --- |
| you need one tiny calculation | the order of steps matters |
| you are checking one value or type | you want to rerun or share the work |
| losing the experiment is harmless | a test or another file will use it |

The course uses scripts for canonical practice because saved steps can be
reviewed, tested, and reproduced.

## Ready check

You are ready for lesson 01 when you can:

- [ ] tell the terminal prompt from the Python `>>>` prompt;
- [ ] run `scratch.py` from the repository root;
- [ ] predict and confirm two printed values;
- [ ] identify the error type, message, and your line in a traceback;
- [ ] explain why fixing a traceback is a small evidence-driven experiment.

Next: [learn the course practice loop](how-to-learn.md), then
[ask an answerable question](../lessons/01-questions.md).
