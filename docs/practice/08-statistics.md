# Practice 08 — Report effect, uncertainty, and limits

This on-site exercise pairs with [lesson 08](../lessons/08-statistics.md).

## Worked warm-up

“Renewers used 4.2 more hours per month” is an estimate, not a complete claim.
A useful report also gives group sizes and spread, an uncertainty interval, a
predeclared practically meaningful difference, and the assumptions that make
the comparison interpretable.

## Try

### Completion — bootstrap one rate

Use this incomplete `scratch.py` scaffold. Replace all five `___` placeholders:

```python
values = customers["renewed"].dropna().to_numpy()
rng = np.random.default_rng(101)
bootstrap_rates = np.empty(2_000)

for index in range(len(bootstrap_rates)):
    sample = rng.choice(values, size=___, replace=___)
    bootstrap_rates[index] = sample.___()

point_estimate = values.mean()
interval = np.percentile(bootstrap_rates, [___, ___])
```

Before running, predict the point estimate, the shape of resampled estimates,
and whether a 95% interval must contain exactly 95% of future observations.
Report the estimate, interval, sample size, seed, and one sampling limitation.

### Transfer — compare ticket counts

Compare support-ticket counts between renewal groups. Choose and justify a
difference measure, compute an interval, set a practically meaningful
threshold **before** seeing the interval, and name two plausible confounders.
Repeat with another seed and explain why the result moves slightly.

## Hint 1

??? tip "Reveal Hint 1"
    For each bootstrap repeat, sample row positions with replacement and
    compute the statistic once. The distribution is over estimates, not a new
    enlarged customer dataset.

## Hint 2

??? tip "Reveal Hint 2"
    Keep these questions separate: “Is zero compatible with the interval?” and
    “Is the point estimate large enough to matter?” They can have different
    answers.

## Tests or rubric

Check finite bootstrap estimates, interval order, bounds within `[0, 1]`, an
overall point estimate equal to the source mean, explicit missing-row counts, a
fixed seed, and a statistic in its original unit. Inspect whether this run's
point estimate lies between its percentile endpoints, but do not treat that as
a general bootstrap invariant. A conclusion passes only if it distinguishes
association from causation and does not describe a p-value as the probability
that a hypothesis is true.

## Worked reasoning

??? success "Reveal worked reasoning"
    Resampling rows approximates how an estimate might vary under repeated
    samples from a similar data-generating process. The interval does not
    contain 95% of individual customers and cannot repair biased coverage.
    Changing the seed changes finite Monte Carlo draws, so endpoints move a
    little; a large movement suggests too few resamples or an unstable sample.

    Ticket-count differences can reflect plan, tenure, support policy, or
    selection as well as renewal status. Report the observed difference and
    uncertainty, compare it with the predeclared operational threshold, and
    stop at association.

    The completion values are `len(values)`, `True`, `mean`, `2.5`, and `97.5`.
    Sampling with replacement keeps every bootstrap sample at the observed
    row count while allowing some rows to appear more than once.

Next: [lesson 09](../lessons/09-modeling.md) or [practice 09](09-modeling.md).
