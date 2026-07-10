# Practice 07 — Build a chart as a claim

This on-site studio pairs with
[lesson 07](../lessons/07-visualization.md). The lesson shows real rendered
outputs as well as code.

## Worked warm-up

Question: “How is monthly usage distributed among observed customers?”

A histogram is appropriate because the target is one numeric distribution.
Its contract includes five-hour bins beginning at zero, customer count on the
y-axis, the number of non-missing rows, and a note about excluded missing
values. Changing the bins changes the visual claim, so bins belong in code.

## Try

### Completion — repair a renewal-rate chart

After running the loading and style setup from lesson 07, copy this incomplete
scaffold into `scratch.py`. Replace the four `___` placeholders before adding
anything else:

```python
channel_summary = customers.groupby(
    "signup_channel", as_index=False, dropna=False
).agg(
    renewal_rate=("renewed_num", "___"),
    customers=("customer_id", "___"),
).sort_values(["renewal_rate", "signup_channel"], kind="stable")

fig, ax = plt.subplots(figsize=(7.2, 4.4), layout="constrained")
bars = ax.bar(channel_summary["signup_channel"],
              channel_summary["renewal_rate"], color=BLUE)
ax.set(title="Observed renewal rate by signup channel",
       xlabel="Signup channel", ylabel="Renewal rate", ylim=(___, ___))
ax.bar_label(
    bars,
    labels=[
        f"{rate:.0%} · n={count}"
        for rate, count in zip(channel_summary["renewal_rate"],
                               channel_summary["customers"])
    ],
)
```

Complete the supporting table first, then ensure:

- the rate axis starts at zero and ends at one;
- every bar label includes a unique-customer count;
- categories have a deterministic order;
- the title says the rates are observed;
- the caption says the comparison is not causal.

Write alt text with chart type, axes, broad pattern, and group-size warning.

### Transfer — show satisfaction without hiding rows

Compare satisfaction across plans. Combine a box plot with visible individual
observations, use a fixed seed for any jitter, state how many scores are
missing, and use more than colour to distinguish groups when needed. Write the
summary table that supports the figure.

## Hint 1

??? tip "Reveal Hint 1"
    Build `groupby(...).agg(rate=(...), customers=("customer_id", "nunique"))`
    before plotting. If the table is wrong, the bars will be wrong more neatly.

## Hint 2

??? tip "Reveal Hint 2"
    Inspect the saved file at the size used on the website. Code cannot detect
    clipped labels, illegible annotations, or a legend that covers data.

## Tests or rubric

- [ ] The first sentence names the question and row unit.
- [ ] The supporting table and plotted values agree.
- [ ] Axis labels include units; bars use an honest zero baseline.
- [ ] Counts and missing-value exclusions are visible near the figure.
- [ ] Colour is not the only encoding of a critical distinction.
- [ ] Output is deterministic and readable at final size.
- [ ] Alt text gives the evidence without claiming causation.

## Worked reasoning

??? success "Reveal worked reasoning"
    A rate alone hides whether it came from five customers or five hundred.
    Unique-customer counts preserve the question's unit and put apparent
    differences in context. A zero-to-one rate axis makes bar length
    interpretable. “Observed rate” and an association caption keep the figure
    from implying that changing channel or plan would change renewal.

    For satisfaction, a box plot supplies a compact distribution summary while
    points reveal sample size, gaps, clusters, and outliers. Reporting excluded
    missing scores prevents the visible subset from masquerading as the whole
    table.

    The four completion values are `"mean"`, `"nunique"`, `0`, and `1`.
    Those choices make the rate and its customer denominator explicit and give
    bar length an honest zero-to-one scale.

Next: [lesson 08](../lessons/08-statistics.md) or [practice 08](08-statistics.md).
