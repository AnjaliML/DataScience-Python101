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

## Quick route

Allow 9–11 focused hours. Work through these in order:

1. [Ask an answerable question](../lessons/01-questions.md)
2. [Python values and expressions](../lessons/02-python-basics.md)
3. [NumPy arrays](../lessons/04-numpy.md)
4. [pandas DataFrames](../lessons/05-pandas.md)
5. [Clean and validate data](../lessons/06-cleaning.md)
6. [Explore and visualise](../lessons/07-visualization.md)
7. [Statistics and uncertainty](../lessons/08-statistics.md)
8. [Start with a baseline](../lessons/09-modeling.md)
9. [Evaluate honestly](../lessons/10-evaluation.md)

Then complete the [capstone](../lessons/13-capstone.md). Return to the linked
full-route lessons whenever a step feels like magic.

## Full route

Allow 28–32 hours including exercises.

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

The capstone is a compact renewal-analysis package. It requires:

- one answerable question and a declared unit of observation;
- a validated dataset and recorded data-quality decisions;
- descriptive evidence and one purposeful figure;
- a simple baseline and one leakage-safe classification pipeline;
- holdout metrics, error analysis, and stated limitations;
- tests, a locked environment, and a one-command rebuild.

The standard is not clever code or the highest score. The standard is whether
another learner can inspect, challenge, and reproduce the reasoning.
