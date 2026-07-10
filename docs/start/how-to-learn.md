# How to learn here

The easiest way to become dependent on code is to run it before you have an
expectation. The fastest way to learn from code is to make a prediction precise
enough that the program can disagree with you.

## Predict before execution

Before pressing Run, write at least one of:

- the output type;
- the array or table shape;
- the number of matching rows;
- the direction of a group difference;
- the metric range;
- the exception you expect from an invalid input.

“It should work” is not a prediction. “The mask has one Boolean per row and
selects fewer rows than the source table” is.

## Trace a small example by hand

When code is unfamiliar, reduce it to three or four values. Write each name and
its value after every line. For a table operation, write the row count, column
names, and key uniqueness before and after.

```python
scores = [4, 8, 5]
passing = []

for score in scores:
    if score >= 6:
        passing.append(score)
```

Predict the final value of `passing` before running it. Then change the boundary
from `>=` to `>` and choose an input that exposes the difference.

## Read errors as evidence

An exception has three useful layers:

1. **Type** — what kind of contract failed.
2. **Message** — what Python knows about the failure.
3. **Traceback** — the calls that led to the failing line.

Start at the final line of the traceback. Move upward until you reach code you
own. The traceback locates the symptom; your smallest failing input helps find
the cause.

## Shrink before fixing

When a full pipeline fails:

1. preserve the failing command and input;
2. identify the first incorrect intermediate result;
3. call the smallest responsible function;
4. remove unrelated loading, plotting, and modelling;
5. turn the failure into a test;
6. fix the underlying rule;
7. rerun the full path.

This is controlled experimentation applied to code.

## Keep the raw data unchanged

Treat source data as an observation, not a draft. Load it, validate it, and
write cleaned or derived outputs somewhere else. Record every choice that
changes rows or values.

A cleaning rule such as “fill missing satisfaction with the median” is not a
neutral technical step. It is a policy that changes the evidence. Name it,
test it, and consider alternatives.

## Use notebooks as an exploration bench

A notebook is useful for:

- meeting a dataset;
- trying one transformation;
- seeing a distribution;
- discussing a chart interactively.

Move durable work into a module when:

- cell order changes the result;
- another analysis needs the same logic;
- a clean process cannot reproduce the output;
- a test or command-line job must run it;
- the notebook has become too large to review.

The endpoint is not “no notebooks”. It is one source of truth.

## Use AI without outsourcing judgement

AI can accelerate mechanical work, but you still own the analytical claim.
For generated code:

1. state what the code assumes about rows, columns, types, and missingness;
2. predict one result before execution;
3. construct an input that could falsify it;
4. compare it with a simple baseline or independent calculation;
5. explain every accepted change in your own words.

Never accept a metric because the surrounding code looks polished. Check which
rows trained the model, which rows were evaluated, and whether any feature
contains future or target information.

## Ask better help questions

A useful question includes:

- the intended result;
- the smallest input that fails;
- the exact command;
- the complete error;
- what you predicted;
- what you have already ruled out.

“pandas is broken” gives nobody a mechanism to inspect.

## Keep a reasoning log

For every exercise, retain five short notes:

```text
question:
prediction:
observed:
explanation:
next check:
```

Those notes scale into issue reports, code reviews, analysis plans, model cards,
and methods sections.

## Use worked solutions well

Every lesson ends with a published
[practice journey](../practice/index.md): worked warm-up → Try → Hint 1 → Hint
2 → tests or rubric → worked reasoning. You never need to discover an unlisted
solution folder to know what comes next.

Attempt the completion and transfer problems before opening worked reasoning.
Then compare in this order:

1. input and output contract;
2. invalid-input policy;
3. tests and boundary cases;
4. implementation body;
5. explanation and limitations.

A different implementation is not automatically wrong. Prefer the version
whose behaviour is easier to state, test, and review.

Next: [ask an answerable question](../lessons/01-questions.md), then use its
[guided practice journey](../practice/01-questions.md).
