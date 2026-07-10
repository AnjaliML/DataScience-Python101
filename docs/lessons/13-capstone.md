# 13 — Capstone studio: audit a reference, then own a claim

The course includes a finished analysis capsule. Running it is valuable, but it
is **not** a learner capstone. This studio therefore has two explicitly
different tracks:

| Track | Purpose | Evidence of completion |
| --- | --- | --- |
| **A · Reference audit** | reproduce, inspect, and challenge supplied expert work | an audit note that traces and tests one claim |
| **B · Learner-owned capstone** | make and defend your own analytical choices | your own question, functions, tests, artifacts, and command |

Do Track A first. Then complete Track B for the course capstone. If your goal is
code review rather than course completion, Track A can stand alone.

## Shared frame

A capstone is a small data-science argument that another person can rebuild,
inspect, and challenge. Its goal is not the highest score or the most artifacts.
Its goal is a visible chain:

```text
question → data → transformation → validation → insight
```

Before either track, write predictions that you will not rewrite after seeing
the result:

1. required fields, row unit, and allowed values;
2. timing and likely leakage risks;
3. missingness, range, duplicate, and coverage failures;
4. an appropriate simple comparison or baseline;
5. the result most likely to be unstable;
6. one outcome that would make you report “not enough evidence.”

## Track A — Reference audit

### Reproduce the supplied capsule

This command deliberately calls the **finished reference implementation**:

```bash
uv run ds-python101 --input data/customer_renewals.csv \
  --output-dir build/reference-audit --seed 101
```

It should create:

```text
build/reference-audit/
├── cleaned.csv
├── summary.json
├── renewal-by-plan.png
├── metrics.json
├── confusion-matrix.png
└── manifest.sha256
```

Running the command proves that the packaged workflow can execute in your
environment. It does not prove that its question, data policy, model, threshold,
or conclusion is correct.

### Inspect from claim back to source

Choose one value or statement in `metrics.json` or a figure. Trace it backward:

1. Which held-out rows and positive-class convention define the metric?
2. Which frozen threshold turns probabilities into decisions?
3. Which training-fold rule selected that threshold?
4. Which preprocessing and model were fitted on training rows?
5. Which cleaned fields feed those transformations?
6. Which raw bytes and question contract give those fields meaning?

Record file names, field names, and checks rather than saying “the library
handles it.”

### Audit each public artifact

- **`cleaned.csv`** — one row per unique account, stable columns, documented
  conversions, unchanged raw input, and visible missingness policy.
- **`summary.json`** — source checksum, row counts, original missingness,
  target definition, features, split seed, exclusions, and repairs.
- **`renewal-by-plan.png`** — supporting table, zero-based rate scale, group
  counts, readable labels, and association-not-causation language.
- **`metrics.json`** — explicit positive class, baseline, threshold and training
  rule, holdout metrics, cross-validation variation, subgroup counts, and
  limitations.
- **`confusion-matrix.png`** — labelled actual and predicted axes, integer
  counts, consistent positive class, and cells summing to holdout size.
- **`manifest.sha256`** — one sorted checksum per generated public artifact and
  a reproducible result on a second identical run.

### Challenge one choice

Change exactly one safe input or declared condition—for example the seed or a
training-fold threshold constraint. Predict which outputs should change,
rebuild into a different directory, and compare. Do not hand-edit generated
artifacts.

Your Track A deliverable is a short audit note:

```text
claim traced:
source-to-claim path:
checks that passed:
choice challenged:
predicted change:
observed change:
remaining limitation:
```

## Track B — Learner-owned capstone

### Choose a question the reference does not answer

You may use the course CSV or another public/synthetic dataset whose provenance
you can document. Suitable course-data questions include:

- How does missing satisfaction coverage differ by plan, and where is the
  descriptive comparison least reliable?
- What uncertainty surrounds plan-level renewal rates without ranking
  individual accounts?
- How does a simple usage-based review rule compare with a capacity-matched
  rule based only on the training data?
- Which pre-decision table-quality failures would block a weekly analysis, and
  how should they be reported?

You may propose another bounded question. A descriptive capstone can be as
rigorous as a model when the evidence and limitations are stronger.

### Pass the ownership gate

Your project must make at least **two material choices** that are not inherited
unchanged from the reference:

- question and decision;
- target, outcome, or statistic;
- fields and timing boundary;
- missingness or exclusion policy;
- comparison or baseline;
- figure or public artifact;
- validation rule tied to the new claim.

Create your own module and command. Calling the supplied `build_capsule`
function, wrapping the existing `ds-python101` command, or merely renaming its
outputs does not pass Track B.

### Define the contract before implementation

Write these two small contracts:

```text
QUESTION CONTRACT
decision:
population and row unit:
timing:
outcome or statistic:
permitted fields:
comparison:
success and stop rules:

OUTPUT CONTRACT
one exact rebuild command:
public files and what each proves:
deterministic inputs and seeds:
failure exit behavior:
manifest policy:
```

Use a new output directory such as `build/learner-capstone/`. One command must
rebuild it from raw input. Stable JSON/CSV, at least one purposeful figure, a
plain-language conclusion, and a checksum manifest are enough; do not copy the
reference's six-file shape unless your question genuinely needs it.

### Build in vertical passes

1. Validate the row unit, required fields, and raw-input checksum.
2. Implement one small transformation in a pure function with boundary tests.
3. Produce one checked table that directly answers part of the question.
4. Render one figure from that table and inspect it at final size.
5. Add the simple comparison, uncertainty estimate, or model required by the
   question—no more.
6. Write the bounded conclusion and concrete limitations.
7. Connect the steps through one command and a deterministic manifest.
8. Delete the output directory, rebuild, rerun, and ask a peer to reproduce it
   without verbal help.

### Minimum checks

Adapt these checks to your question rather than copying names blindly:

- required fields and allowed values fail with useful messages;
- row keys match the declared grain;
- raw input bytes do not change;
- exclusions and conversion failures reconcile to source counts;
- every reported rate or probability is in `[0, 1]`;
- group totals reconcile to the intended unit;
- any train/test indices are disjoint and preprocessing fits on training only;
- figure values agree with their supporting table;
- every public artifact exists, is non-empty, and is in the manifest;
- a second identical run produces identical bytes or documented exceptions.

## Explain

Write the final learner-owned explanation in this order:

1. **Question:** decision, row unit, timing, outcome/statistic, and comparison.
2. **Data:** provenance, schema, missingness, coverage, and exclusions.
3. **Transformation:** named steps, policies, seed, and any model or interval.
4. **Validation:** tests, independent checks, comparison, and uncertainty.
5. **Insight:** the strongest supported pattern in plain language.
6. **Limitations:** sampling, measurement, subgroup size, drift, and causal
   boundary.

A useful conclusion can be “the evidence does not improve enough over the
baseline” or “this subgroup is too small for a stable comparison.” Honest
stopping is part of the result.

## Review rubric

Score each card 0 (missing), 1 (partial), or 2 (convincing):

- **Question:** unit, timing, statistic/outcome, comparison, and practical
  consequence; error cost when the project supports a prediction decision.
- **Data:** provenance, grain, coverage, missingness, and unchanged raw input.
- **Transformation:** small named steps with explicit policy and no hidden state.
- **Validation:** boundaries, an independent check, and an honest comparison.
- **Insight:** a bounded claim tied directly to visible evidence.
- **Reproducibility:** locked environment, one command, stable outputs, manifest.
- **Independence:** at least two material choices owned by the learner.
- **Limitations:** concrete uncertainty, subgroup, drift, and causal bounds.

Aim for no zero and at least 12 of 16 points. Extra models, dashboards, and
decorative plots do not compensate for an invalid question or split.

## Guided practice journey

[Work through Try → Hint 1 → Hint 2 → rubric → worked reasoning](../practice/13-capstone.md).
The studio turns Track A inspection into a deliberately different Track B project.

## Keep going

Carry the course sequence into unfamiliar work:

```text
question → data → transformation → validation → insight
```

Predict before running, preserve row meaning, reserve independent evidence,
compare with a simple reference, make errors visible, and say where the claim
must stop.
