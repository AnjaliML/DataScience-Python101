# Pre-share analysis checklist

Use this audit before sending an analysis, notebook, model, or report to another person. It is a set of questions, not a promise that the work is correct. Mark an item only when you can point to evidence.

## 1. Question and decision

- [ ] The decision this work supports is stated in one sentence.
- [ ] The audience and decision owner are named.
- [ ] The unit of observation is explicit: “Each row represents … at …”.
- [ ] The target or outcome has an observable definition and time window.
- [ ] The prediction or analysis date is separate from the date the outcome becomes known.
- [ ] Allowed features are limited to information available at decision time.
- [ ] A baseline describes what happens without this analysis or model.
- [ ] The success criterion connects to the decision, capacity, and error costs.
- [ ] Important failure modes and groups who could be harmed by errors are listed.
- [ ] The conclusion does not silently change a descriptive question into a causal claim.

Write the smallest defensible claim:

> For [unit and population] during [period], we estimate [quantity] using [evidence], to support [decision], subject to [main limitation].

## 2. Grain, schema, and coverage

- [ ] Row and column counts are recorded before transformations.
- [ ] Every column used in the result has a definition, unit, and expected type.
- [ ] The proposed key is tested for missing values and duplicates.
- [ ] Duplicate rows are explained rather than automatically removed.
- [ ] Category values, including capitalization and whitespace variants, are inspected.
- [ ] Numeric ranges are checked against plausible domain limits.
- [ ] Dates parse successfully and fall within the intended observation period.
- [ ] Join keys are checked on both sides before joining.
- [ ] Join cardinality is predicted and checked after the join.
- [ ] Coverage gaps by time, source, region, channel, or customer group are reported.
- [ ] A sample of raw rows has been compared with source definitions or records.

Useful structural checks include:

```python
assert not data[key_columns].isna().any(axis=None)
assert not data.duplicated(key_columns).any()
assert set(required_columns).issubset(data.columns)
```

## 3. Cleaning and transformation

- [ ] Missing values are counted by column and relevant subgroup.
- [ ] Missingness is not treated as zero unless the meanings are equivalent.
- [ ] Every row filter has a stated reason and before/after row count.
- [ ] Type conversions are explicit; failed conversions are surfaced.
- [ ] Units and time zones are consistent before comparison.
- [ ] Category mappings preserve unknown or newly observed values.
- [ ] Outliers are investigated before removal, capping, or transformation.
- [ ] Derived features have plain-language formulas and valid time cutoffs.
- [ ] Aggregations state their grouping keys and the meaning of one output row.
- [ ] The cleaned result still satisfies its key, range, and allowed-value checks.
- [ ] Cleaning code is repeatable rather than dependent on manual spreadsheet edits.

Keep a small transformation ledger: input rows, output rows, columns added or removed, and the reason for each material change.

## 4. Exploration and statistics

- [ ] Distributions are inspected, not represented only by averages.
- [ ] Counts accompany percentages and rates.
- [ ] Denominators are named and comparable across groups.
- [ ] Missing and “unknown” categories remain visible where relevant.
- [ ] Time trends are checked for seasonality, outages, and definition changes.
- [ ] Group comparisons use the same period and population or explain why not.
- [ ] Charts have titles, labeled axes, units, and honest scales.
- [ ] Visual encodings remain readable without relying only on color.
- [ ] Statistical assumptions match the data-generating process and sampling design.
- [ ] Uncertainty is shown with intervals, sensitivity analysis, or explicit bounds.
- [ ] Multiple comparisons and post-hoc subgroup searches are disclosed.
- [ ] Correlation is not described as an intervention effect without a causal design.

Ask an adversarial question: what alternative data-generating process could create the same pattern?

## 5. Leakage and evaluation

- [ ] Every feature can be reconstructed using only information available at prediction time.
- [ ] Labels and post-outcome fields cannot leak through joins, aggregates, or preprocessing.
- [ ] Repeated entities do not cross train and test boundaries when that would leak identity or history.
- [ ] A time-based split is used when future performance is the real question.
- [ ] Preprocessing is fitted on training data and then applied to validation or test data.
- [ ] The untouched test set is used once for the final estimate, not for iteration.
- [ ] Metrics match class balance, ranking needs, capacity, and error costs.
- [ ] Performance is compared with a simple, named baseline.
- [ ] Thresholds are chosen on validation data and connected to operating capacity.
- [ ] Results include uncertainty and subgroup or time-slice performance.
- [ ] The evaluation population matches the population that will receive decisions.
- [ ] Known distribution shifts, feedback loops, and monitoring needs are documented.

For any impressive result, try to make it disappear by removing suspicious columns, changing the split, and testing a simpler baseline.

## 6. Reproducibility

- [ ] A new environment can be created from declared dependencies.
- [ ] Exact commands to run tests, analysis, and site build are documented.
- [ ] Random processes use recorded seeds where reproducibility is expected.
- [ ] Raw inputs are read-only; generated outputs have clear locations.
- [ ] Paths are project-relative and secrets are not stored in code or data files.
- [ ] Data versions, extraction dates, and external sources are recorded.
- [ ] The analysis runs from a clean session in the intended order.
- [ ] Automated tests cover key transformations and boundary conditions.
- [ ] Assertions test row grain, ranges, shapes, and allowed values.
- [ ] Temporary files, caches, and private data are excluded from version control.
- [ ] The final commit contains only intentional files and passes all checks.

## 7. Communication and release

- [ ] The answer appears before implementation detail.
- [ ] Each headline number includes population, period, unit, and denominator.
- [ ] Every table and chart can be understood from its title, labels, and note.
- [ ] Claims distinguish observation, prediction, and causation.
- [ ] Limitations describe likely direction or consequence, not only a disclaimer.
- [ ] Sensitive examples and small groups are protected from identification.
- [ ] Accessibility, readable contrast, and useful alternative text are checked.
- [ ] Links work and exported artifacts render correctly.
- [ ] Another person has challenged one assumption and reproduced one result.
- [ ] The recommended action, owner, monitoring signal, and revisit date are clear.

## Final stop test

Do not share yet if you cannot answer any of these:

1. What exactly is one row?
2. Which evidence could reveal the answer too early?
3. What baseline does the result beat?
4. Which check would most likely overturn the conclusion?
5. Can another person reproduce the result from the documented starting point?
6. What decision should change, and what harm could a wrong answer cause?
