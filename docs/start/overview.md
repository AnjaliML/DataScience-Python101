# Course overview

Data science is not a sequence of library calls. It is a chain of decisions:
what you want to know, what one row represents, which transformations are
valid, how you will try to disprove the result, and what action the evidence
can support.

The recurring course spine is:

```text
question → data → transformation → validation → insight
```

Python makes the chain executable. It does not make the chain correct for you.

## Who this is for

The full route assumes:

- no prior programming;
- comfort reading a simple table or chart;
- willingness to write down a prediction before pressing Run.

The quick route also works as a reset for people who can make notebooks run
but have not yet built a tested function, leakage-safe model, or reproducible
analysis.

## What you will be able to do

By the end, you should be able to:

1. turn a vague request into a specific analytical question and success rule;
2. trace values, types, branches, and returned results through Python code;
3. write small functions with explicit inputs, outputs, and error policies;
4. use NumPy arrays without losing track of shape, axis, or data type;
5. select, join, group, and reshape pandas data without losing row identity;
6. validate keys, categories, ranges, duplicates, and missing values;
7. design a visual around a question rather than a chart type;
8. report variation, effect size, and uncertainty alongside averages;
9. compare a model with a simple baseline using data it did not train on;
10. detect leakage and inspect errors, thresholds, and subgroup performance;
11. move reusable logic out of a notebook into tested modules;
12. produce a deterministic report from one documented command.

## The lesson rhythm

Every lesson uses five moves.

<div class="lesson-contract">
  <p><strong>Frame.</strong> What decision are we making? What could make it wrong?</p>
  <p><strong>Predict.</strong> State a type, shape, count, distribution, or failure before execution.</p>
  <p><strong>Build.</strong> Express the smallest transformation that can answer the question.</p>
  <p><strong>Check.</strong> Challenge assumptions with tests, baselines, and awkward inputs.</p>
  <p><strong>Explain.</strong> Say what the evidence supports and where it stops.</p>
</div>

Do not treat those headings as decoration. If you cannot predict a result or
name a failure mode, the code is doing more thinking than you are.

Each lesson then links to a public practice page with the same scaffold:
**worked warm-up → completion → transfer → Hint 1 → Hint 2 → tests or rubric →
worked reasoning**. Start at the [practice index](../practice/index.md) if you
want to see the whole sequence.

## Quick route

Allow **14–18 focused hours including the practice checkpoints**. This route is
only a shortcut through material you can already demonstrate; it is not a
shortcut around the capstone's functions, testing, reproducibility, or
command-line requirements.

Use it if you can already create and run a small Python script, read a simple
traceback, and explain a list, function, and Boolean condition. If not, take the
[setup page](setup.md) as far as the Python version check, complete the
[15-minute first-script bridge](first-script.md), and use the full route.

Work through these ten lessons in order:

1. [Ask an answerable question](../lessons/01-questions.md)
2. [Functions and control flow](../lessons/03-functions-control.md)
3. [pandas DataFrames](../lessons/05-pandas.md)
4. [Clean and validate data](../lessons/06-cleaning.md)
5. [Explore and visualise](../lessons/07-visualization.md)
6. [Start with a baseline](../lessons/09-modeling.md)
7. [Evaluate honestly](../lessons/10-evaluation.md)
8. [Reproducible projects](../lessons/11-reproducibility.md)
9. [Turn analysis into a tool](../lessons/12-tools.md)
10. [Capstone](../lessons/13-capstone.md)

The route skips lessons 02, 04, and 08 only because their ideas are checked at
the point of use. Before skipping each one, confirm that you can:

- trace names, values, types, and Boolean expressions (lesson 02);
- state the shape and axis of an array operation (lesson 04);
- distinguish an estimate, an uncertainty interval, and a causal claim
  (lesson 08).

If any check is unclear, take that lesson and its practice page before
continuing. This keeps “quick” honest: the endpoint and review standard are the
same as the full route.

## Full route

Allow 28–32 hours including exercises.

If this is your first time programming, follow [Set up once](setup.md) until the
Python version command works, take
[Your first 15 minutes with Python](first-script.md), return for the setup ready
checks, then take lessons 01–13 and their linked practice journeys in order.

| Stage | Lessons | Habit you are building |
| --- | --- | --- |
| Frame | 01–03 | make the question, state, and logic explicit |
| Shape | 04–06 | preserve axes, keys, schemas, and provenance |
| Understand | 07–08 | describe patterns with context and uncertainty |
| Model | 09–10 | compare against baselines without leaking answers |
| Deliver | 11–13 | make the whole analysis testable and reproducible |

A useful cadence is 20–30 minutes of reading, 45–75 minutes of practice, and
10 minutes explaining the result in plain language.

## The running dataset

The course includes `data/customer_renewals.csv`, a deterministic synthetic
table. Each row represents one fictional subscription customer observed at a
renewal decision. It includes:

- a unique `customer_id`;
- categorical plan and signup-channel labels;
- tenure, product usage, support, and satisfaction measures;
- `renewed`, the binary outcome used in later lessons.

It is deliberately small enough to inspect on a laptop. It represents no real
people, organisation, or commercial process. Any apparent pattern is a product
of the documented generator, not a claim about real customers.

## What is deliberately not here

There is no early catalogue of every method, class feature, chart option, or
model. You meet a language feature when an analytical problem gives it a job.

There is no claim that prediction proves causation. A model can estimate an
association in data collected under particular conditions. It cannot, by
itself, tell you what would happen after an intervention.

There is also no notebook-only endpoint. Notebooks are excellent exploration
benches. Durable logic belongs in functions and modules that can be tested and
run from a clean process.

## Assessment

The [capstone studio](../lessons/13-capstone.md) separates two kinds of work:

1. **Reference audit:** reproduce the supplied renewal capsule, trace one claim
   back to source rows and assumptions, and challenge one declared choice.
2. **Learner-owned capstone:** ask a question the reference does not answer,
   make at least two material analytical choices, implement small tested steps,
   and expose one documented rebuild command.

Running the finished reference command does not count as the learner capstone.
The learner-owned project may be descriptive, inferential, or predictive; it
needs only the methods its question requires. Every project still needs a
declared row unit, validated data, visible evidence, an honest comparison,
tests, limitations, a locked environment, and a reproducible output contract.

The standard is not clever code or the highest score. The standard is whether
another learner can inspect, challenge, and reproduce **your reasoning and
choices**.
