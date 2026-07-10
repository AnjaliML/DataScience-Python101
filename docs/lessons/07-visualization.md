# 07 — Visualization: make one honest claim

A useful chart answers a named question and makes its evidence inspectable. Decoration comes later.

By the end of this lesson, you will be able to choose plots for distributions, relationships, and groups; use honest scales and accessible encodings; and save reproducible figures.

## Frame

Exploratory data analysis usually asks three kinds of questions:

1. **Distribution:** What values are common, unusual, or missing?
2. **Relationship:** How do two measurements vary together?
3. **Group comparison:** How does a measure differ across categories?

Begin with a sentence, not a chart type:

> How does renewal rate vary by plan, and how many customers support each rate?

A plot is a claim because position, length, colour, and scale direct attention. The code, summary table, and missing-data count are part of that claim.

## Predict

Predict which view better shows individual values:

~~~python
customers.groupby("plan")["monthly_usage_hours"].mean()
customers.plot.scatter(x="tenure_months", y="monthly_usage_hours")
~~~

The grouped mean compresses every plan to one number. The scatter plot preserves rows but may hide overlapping points. Neither is automatically better; each answers a different question.

Before drawing a renewal-rate bar chart, predict its valid y-axis range. A proportion must be between zero and one, and bars should start at zero because their lengths encode magnitude.

## Build

Load the table and create one numeric outcome:

~~~python
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
customers = pd.read_csv("data/customer_renewals.csv")
customers["renewed_num"] = pd.to_numeric(customers["renewed"], errors="coerce")
assert customers["renewed_num"].notna().all()
assert customers["renewed_num"].isin([0, 1]).all()
~~~

Set stable visual defaults and one save function:

~~~python
plt.rcParams.update({"axes.spines.top": False, "axes.spines.right": False})
FIGURE_DIR = Path("docs/assets/figures")
def save_figure(fig, filename):
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURE_DIR / filename, dpi=160, facecolor="white",
                bbox_inches="tight",
                metadata={"Creator": "Data Science Python 101"})
    plt.close(fig)
~~~

Fixed inputs, dimensions, bins, ordering, and library versions make figures repeatable. Use a random seed whenever sampling or jitter is involved.

### Distribution

Inspect counts before plotting:

~~~python
usage = customers["monthly_usage_hours"].dropna()
assert not usage.empty
upper = max(5.0, float(np.ceil(usage.max() / 5) * 5))
bins = np.arange(0, upper + 5, 5)
fig, ax = plt.subplots(figsize=(7, 4), constrained_layout=True)
ax.hist(usage, bins=bins, color="#0072B2", edgecolor="white")
ax.set(title="Distribution of monthly usage", xlabel="Monthly usage (hours)",
       ylabel="Customers", xlim=(0, upper))
save_figure(fig, "monthly-usage-distribution.png")
~~~

Explicit bins make comparisons stable. Starting at zero is sensible because negative usage is impossible. Report how many missing values the chart excluded.

### Relationship

Encode renewal with both colour and marker style:

~~~python
relationship = customers.dropna(
    subset=["tenure_months", "monthly_usage_hours", "renewed_num"]
).assign(
    renewal=lambda x: x["renewed_num"].map({0.0: "No", 1.0: "Yes"})
).sort_values("customer_id", kind="stable")
fig, ax = plt.subplots(figsize=(7, 4), constrained_layout=True)
for label, marker, colour in [("No", "o", "#D55E00"),
                              ("Yes", "^", "#0072B2")]:
    group = relationship.loc[relationship["renewal"].eq(label)]
    ax.scatter(group["tenure_months"], group["monthly_usage_hours"],
               label=label, marker=marker, color=colour, alpha=0.7)
ax.legend(title="Renewed")
ax.set(title="Usage and tenure among observed customers",
       xlabel="Tenure (months)", ylabel="Monthly usage (hours)")
save_figure(fig, "usage-by-tenure.png")
~~~

Transparency reveals dense regions. Redundant marker shapes help when colour is unavailable. The title says “among observed customers” because a scatter plot does not show a causal effect.

### Groups

Build the supporting table before the bars:

~~~python
plan_summary = customers.groupby(
    "plan", as_index=False, dropna=False, observed=True
).agg(
    renewal_rate=("renewed_num", "mean"),
    customers=("customer_id", "nunique"),
).sort_values("renewal_rate", ascending=False, kind="stable")
fig, ax = plt.subplots(figsize=(7, 4), constrained_layout=True)
bars = ax.bar(
    plan_summary["plan"].astype("string"), plan_summary["renewal_rate"],
    color="#0072B2"
)
ax.set(title="Observed renewal rate by plan", xlabel="Plan",
       ylabel="Renewal rate", ylim=(0, 1))
ax.bar_label(
    bars,
    labels=[
        f"{rate:.0%}\n(n={count})"
        for rate, count in zip(plan_summary["renewal_rate"],
                               plan_summary["customers"])
    ],
    padding=3
)
save_figure(fig, "renewal-rate-by-plan.png")
~~~

The zero baseline makes bar length honest. Counts prevent a tiny group with an extreme rate from looking as certain as a large group.

## Check

Audit the rows behind every plot:

~~~python
plot_checks = pd.DataFrame({
    "column": customers.columns,
    "missing": customers.isna().sum().to_numpy(),
})
print(plot_checks)

assert plan_summary["renewal_rate"].between(0, 1).all()
assert plan_summary["customers"].gt(0).all()
assert len(relationship) <= len(customers)
assert bins[0] == 0
assert np.all(np.diff(bins) > 0)
~~~

Also inspect the saved image at its intended display size. Labels can overlap even when code succeeds, and colour contrast can fail even when values are correct.

## Explain

Use this plot-as-claim sequence: state the question and unit; compute a supporting table; match the encoding to a distribution, relationship, or group; label units, sizes, exclusions, and scales; describe the pattern without causal language; and name a limitation.

For example: “Renewal rate is higher in plan A than plan B in this file. Plan membership may differ with tenure or signup channel, so this comparison does not show that changing plans would cause renewal.”

## Practice

1. Plot the distribution of `support_tickets` with integer-aligned bins.
2. Compare satisfaction across plans with a box plot plus visible observations.
3. Plot renewal rate by signup channel and annotate group sizes.
4. Make one misleading version by truncating a bar axis, then repair it.
5. Write alt text that states the chart type, axes, main pattern, and important exception.

For each figure, save a deterministic file and write the summary table that produced it.

## Keep going

Before moving on, explain why the question comes before the chart type, different questions need different encodings, bars need an honest baseline, colour should not carry meaning alone, exclusions and group sizes belong beside plots, and association is not causation.

The next lesson adds uncertainty, effect sizes, and appropriately limited statistical evidence.
