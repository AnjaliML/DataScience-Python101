# Practice that fades, not disappears

Every lesson has an on-site practice journey. You do not need to discover a
hidden exercise folder or guess whether a solution exists.

Use the same order every time:

```text
worked warm-up → Try → Hint 1 → Hint 2 → Tests or rubric → Worked reasoning
```

## How to use a journey

1. Read the **worked warm-up** and explain why each check belongs.
2. Attempt **Try — completion** with the small scaffold still visible.
3. Attempt **Try — transfer** on the new case without copying the warm-up.
4. Open **Hint 1** only when you can name where you are stuck.
5. Open **Hint 2** when you need a stronger nudge or intermediate structure.
6. Run the **tests** or score the **rubric** before reading the reasoning.
7. Compare your decisions with **worked reasoning**, not just the final syntax.

The worked reasoning is intentionally below the checks. A solution is most
useful after your own prediction has had a chance to be wrong.

## Keep a five-line reasoning log

```text
question:
prediction:
observed:
explanation:
next check:
```

For code tasks, keep the exact command and final traceback line too. For
writing or chart tasks, keep the evidence that made you revise the artifact.

## Repository exercises

The repository has one writing exercise for lesson 01, plus starter files and
automated tests for lessons 03, 04, 05, 06, and 09. The folder numbers describe
the exercise sequence, so they do not always match the lesson number:

| Course lesson | Repository exercise |
| --- | --- |
| 01 · Question contract | `exercises/01-questions/README.md` (writing only) |
| 03 · Functions | `exercises/02-functions/` |
| 04 · NumPy | `exercises/03-numpy/` |
| 05 · pandas | `exercises/04-dataframes/` |
| 06 · Cleaning | `exercises/05-cleaning/` |
| 09 · Modeling | `exercises/06-modeling/` |

The on-site journeys explain each task, give staged hints, and provide a worked
reasoning path; the repository starters give you a place to write and execute
code.

From the repository root, the usual pattern is:

```bash
uv run pytest exercises/02-functions/test_starter.py -q
```

The exact command appears on the relevant practice page. A failing test is a
specific example of a broken contract, not a score on your ability.

## Choose a practice journey

| Lesson | Completion focus | Independent transfer |
| --- | --- | --- |
| [01](01-questions.md) | complete a question contract | frame a new decision |
| [02](02-python-basics.md) | trace values and types | express a new policy |
| [03](03-functions-control.md) | implement a binary-rate contract | validate a new record |
| [04](04-numpy.md) | standardise numeric columns | diagnose a broadcast failure |
| [05](05-pandas.md) | complete a grouped summary | preserve grain through a merge |
| [06](06-cleaning.md) | measure five quality failures | defend a missingness policy |
| [07](07-visualization.md) | repair an honest chart | make a new claim-led figure |
| [08](08-statistics.md) | complete an interval estimate | bound a new claim |
| [09](09-modeling.md) | isolate target and fit a prior baseline | build a split-first pipeline |
| [10](10-evaluation.md) | evaluate one fixed threshold | choose under a new cost policy |
| [11](11-reproducibility.md) | complete a provenance record | reproduce from a clean state |
| [12](12-tools.md) | complete a CLI boundary | add one tested option |
| [13](13-capstone.md) | audit the reference capsule | build a learner-owned capstone |

Start with [lesson 01 practice](01-questions.md), or return to the
[course overview](../start/overview.md).
