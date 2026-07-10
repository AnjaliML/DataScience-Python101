# Practice 13 — Audit first, then own the analysis

This studio pairs with [lesson 13](../lessons/13-capstone.md). The two tracks
have different purposes: auditing the supplied reference teaches inspection;
building your own capstone demonstrates independent choices.

## Worked warm-up

Run the reference workflow into a temporary directory. Pick one claim in
`metrics.json` and trace it backward through the threshold rule, held-out rows,
pipeline, cleaned table, raw fields, and question contract. Record one design
choice you agree with and one you would challenge. Reproduction is the start of
an audit, not completion of a capstone.

## Try

### Completion — reference audit

Use the supplied command and audit checklist from lesson 13. Change exactly one
safe condition—such as the seed or a training-fold threshold constraint—and
predict which artifacts and checksums should change. Rebuild, compare, and
explain the mechanism. Do not edit the result after generation.

### Transfer — learner-owned capstone

Choose a question that the reference capsule does not answer. Options include:

- describe which subscription accounts at one renewal decision have missing
  satisfaction and how coverage differs by plan;
- estimate uncertainty around plan-level renewal rates without ranking people;
- compare a simple usage-based review rule with a capacity-matched baseline;
- use another public or synthetic dataset whose provenance you can document.

Write your own question contract, output contract, small functions, tests, and
one-command interface. At least two material choices—question, target or
statistic, feature/field policy, comparison, or artifact—must be yours. Calling
the supplied capsule builder unchanged does not satisfy this track.

## Hint 1

??? tip "Reveal Hint 1"
    Start with one table and one figure before adding a model. A descriptive or
    uncertainty-focused capstone can be rigorous without classification.

## Hint 2

??? tip "Reveal Hint 2"
    Define public artifact names and the command before implementation. Build
    vertically: one validated input → one correct result → one saved artifact →
    one test, then add the next slice.

## Tests or rubric

Score each criterion 0 (missing), 1 (partial), or 2 (convincing):

| Criterion | What earns 2 |
| --- | --- |
| Question | unit, timing, outcome/statistic, comparison, and practical consequence; error cost when predicting decisions |
| Data | provenance, grain, coverage, missingness, and unchanged raw input |
| Transformation | small named steps with explicit policies and no hidden state |
| Validation | boundary tests, independent checks, and an honest comparison |
| Insight | a bounded claim tied directly to visible evidence |
| Reproducibility | locked environment, one command, stable outputs, manifest |
| Independence | at least two material choices differ from the reference workflow |
| Limitations | concrete uncertainty, coverage, subgroup, drift, and causal bounds |

Aim for no zero and at least 12 of 16 points. Ask a peer to reproduce the work
without verbal help.

## Worked reasoning

??? success "Reveal a strong project strategy"
    A strong learner-owned project starts smaller than the reference package.
    For the missing-satisfaction question, the unit remains one subscription
    account at one renewal decision; the outcome is whether satisfaction is
    observed, not renewal. First validate IDs and plan labels. Then build one
    plan-level table with unique-customer
    counts, observed-score counts, and missing rates. Plot zero-based missing
    rates with denominators. Add a seeded interval only after the descriptive
    result is correct. Tests should catch duplicate IDs, unknown plans, rates
    outside `[0, 1]`, totals that do not reconcile, and raw-file mutation.

    This project reuses course habits but owns the analytical question,
    statistic, evidence, and limitations. That is the distinction between
    inspecting expert work and producing a capstone.

Return to [the capstone lesson](../lessons/13-capstone.md) or the
[practice index](index.md).
