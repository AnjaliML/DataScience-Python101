# 08 — Statistics: effects, uncertainty, and limits

Statistics helps separate a pattern in one table from what the underlying process might produce again. It does not turn observational data into certainty.

By the end of this lesson, you will be able to summarize a distribution, estimate sampling variability, build a confidence interval, interpret a hypothesis test narrowly, and distinguish association from causation.

## Frame

Consider this question:

> Do customers who renew use the product more each month?

It asks about typical usage, the size of a difference, how that estimate varies across samples, and whether another variable could explain the association.

The row is a customer. The outcome is renewal. Usage is measured, not assigned by an experiment, so causal claims are out of scope.

## Predict

Two samples can have the same mean and different spread:

~~~python
a = pd.Series([9, 10, 10, 10, 11])
b = pd.Series([0, 5, 10, 15, 20])
print(a.mean(), b.mean())
print(a.std(), b.std())
~~~

Predict the results qualitatively. The means match, but sample `b` is much more variable. A center without a spread is an incomplete description.

Also predict what happens to uncertainty when a representative sample grows. Standard errors usually shrink because averages fluctuate less across larger samples.

## Build

Load the table and normalize the binary outcome:

~~~python
import numpy as np
import pandas as pd
customers = pd.read_csv("data/customer_renewals.csv")
customers["renewed_num"] = pd.to_numeric(customers["renewed"], errors="coerce")
assert customers["renewed_num"].notna().all()
assert customers["renewed_num"].isin([0, 1]).all()
~~~

### Describe before inferring

Summarize monthly usage with measures that answer different questions:

~~~python
usage = customers["monthly_usage_hours"].dropna()
q1, q3 = usage.quantile([0.25, 0.75])
usage_summary = usage.describe()
usage_summary["median"] = usage.median()
usage_summary["iqr"] = q3 - q1
print(usage_summary)
~~~

The mean uses every value and is sensitive to extremes. The median is the middle ordered value. Standard deviation measures spread around the mean; the interquartile range describes the middle half. Compute these by renewal group before comparing them.

### See sampling variability

A bootstrap resamples observed rows with replacement. A fixed seed makes the demonstration repeatable:

~~~python
rng = np.random.default_rng(101)
bootstrap_means = np.array([
    rng.choice(usage.to_numpy(), size=len(usage), replace=True).mean()
    for _ in range(5_000)
])
bootstrap_interval = np.quantile(bootstrap_means, [0.025, 0.975])
print(bootstrap_interval)
~~~

This approximate interval assumes representative, appropriately independent rows. A frequentist 95% procedure captures the parameter in about 95% of repeated samples when assumptions hold. Once computed, its endpoints are fixed; it does not give a 95% probability about a fixed parameter.

### Estimate a difference and effect size

~~~python
complete = customers.dropna(subset=["monthly_usage_hours", "renewed_num"])
renewed_usage = complete.loc[complete["renewed_num"].eq(1),
                             "monthly_usage_hours"].to_numpy()
not_renewed_usage = complete.loc[complete["renewed_num"].eq(0),
                                 "monthly_usage_hours"].to_numpy()
assert len(renewed_usage) >= 2
assert len(not_renewed_usage) >= 2
mean_difference = renewed_usage.mean() - not_renewed_usage.mean()
~~~

Bootstrap the difference by resampling independently within each group:

~~~python
rng = np.random.default_rng(101)
bootstrap_differences = np.array([
    rng.choice(renewed_usage, len(renewed_usage), replace=True).mean()
    - rng.choice(not_renewed_usage, len(not_renewed_usage),
                 replace=True).mean()
    for _ in range(5_000)
])
difference_interval = np.quantile(bootstrap_differences, [0.025, 0.975])
~~~

Report the difference in hours because its unit is understandable. A standardized effect can help compare across measures:

~~~python
n1, n0 = len(renewed_usage), len(not_renewed_usage)
pooled_variance = (
    (n1 - 1) * renewed_usage.var(ddof=1)
    + (n0 - 1) * not_renewed_usage.var(ddof=1)
) / (n1 + n0 - 2)
cohens_d = mean_difference / np.sqrt(pooled_variance)
print("Mean difference:", mean_difference)
print("95% bootstrap interval:", difference_interval)
print("Cohen's d:", cohens_d)
~~~

`Cohen's d` expresses the mean difference in pooled standard-deviation units. It is not automatically “small” or “large”; domain consequences decide whether the effect matters.

### Use a hypothesis test narrowly

A permutation test asks what differences appear when group labels are exchangeable under a null model:

~~~python
rng = np.random.default_rng(101)
combined = np.concatenate([renewed_usage, not_renewed_usage])
null_differences = np.empty(5_000)
for index in range(len(null_differences)):
    shuffled = rng.permutation(combined)
    null_differences[index] = shuffled[:n1].mean() - shuffled[n1:].mean()
extreme = np.count_nonzero(abs(null_differences) >= abs(mean_difference))
p_value = (extreme + 1) / (len(null_differences) + 1)
print("Permutation p-value:", p_value)
~~~

Under the null and exchangeability assumptions, this p-value estimates how often a shuffled difference is at least this extreme. It is not the probability that the null is true or the effect size. Choose the analysis first: repeated testing makes one unusual result more likely.

### Separate correlation from causation

~~~python
measurements = ["tenure_months", "monthly_usage_hours",
                "support_tickets", "satisfaction_score"]
correlations = customers[measurements].corr(method="spearman")
print(correlations.round(2))
~~~

Correlation can arise because one variable influences another, because the direction is reversed, because a third variable influences both, through selection, or by chance. Here, plan and tenure could affect both usage and renewal.

## Check

Connect statistical evidence to a practical threshold:

~~~python
MIN_MEANINGFUL_DIFFERENCE = 5.0  # hours per month
interval_excludes_zero = (
    difference_interval[0] > 0 or difference_interval[1] < 0
)
practically_large = abs(mean_difference) >= MIN_MEANINGFUL_DIFFERENCE
assert np.isfinite(mean_difference)
assert difference_interval[0] <= mean_difference <= difference_interval[1]
assert -1 <= correlations.loc["tenure_months", "monthly_usage_hours"] <= 1
~~~

The two Boolean results answer different questions. A precise tiny effect can be statistically clear but practically unimportant. A valuable-looking effect can remain too uncertain to guide a decision.

Before publishing, check the unit, missing-row exclusions, independence assumptions, group sizes, outliers, test choice, effect units, interval, and number of analyses attempted.

## Explain

A disciplined explanation describes the sample, reports the effect in its original unit, gives uncertainty, states any test and assumptions, compares with a predeclared practical threshold, and limits the claim to association unless the design supports causation.

A small p-value is limited evidence against one null model. It does not repair biased sampling, measurement errors, leakage, uncontrolled confounding, or an irrelevant question.

## Practice

Summarize satisfaction with center and spread; bootstrap renewal rate; compare support tickets between renewal groups with an effect and interval; change the bootstrap seed and explain the movement; choose a meaningful threshold before calculating; and name two plausible confounders. Write each conclusion as an estimate, uncertainty statement, and limitation.

## Guided practice journey

[Work through Try → Hint 1 → Hint 2 → rubric → worked reasoning](../practice/08-statistics.md).
You will complete one interval estimate before transferring the reasoning to a group effect.

## Keep going

You should now be able to explain why center and spread belong together, how resampling reveals sampling variability, what confidence intervals promise, why p-values are not verdicts or effect sizes, why practical and statistical significance differ, and why correlation is not causation. The goal is a calibrated claim: what was observed, how it may vary, its assumptions, and where it must stop.
