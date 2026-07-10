# 06 — Cleaning data with explicit rules

Cleaning means converting observations into a form that satisfies a declared contract while preserving evidence about what changed.

By the end, you will be able to diagnose missing values and duplicates, convert types safely, validate categories and ranges, and keep raw data separate from cleaned output.

## Frame

A file can load successfully while containing a blank score, repeated customer, or `"twelve"` in a numeric column. Loading answers “can pandas parse this?” Validation answers “does this table meet our rules?”

Use a visible boundary: **raw file → inspect → clean by policy → validate → analysis-ready table**.

The raw file is evidence, so never overwrite it. A cleaned table is a derived artifact with a known source, rules, exclusions, and checks.

## Predict

What happens to `"unknown"` here?

~~~python
pd.to_numeric(pd.Series(["12", "unknown"]), errors="coerce")
~~~

It becomes missing. Coercion is useful only when you count newly invalid values; otherwise a new data-entry problem disappears.

A missing optional score and missing target have different meanings. Likewise, repeated identifiers may be errors or real repeated events. A blanket `dropna` or `drop_duplicates` is not a policy.

## Build

Load raw bytes, identify them, and work on a copy:

~~~python
from pathlib import Path
import hashlib
import pandas as pd
DATA_PATH = Path("data/customer_renewals.csv")
raw = pd.read_csv(DATA_PATH)
cleaned = raw.copy(deep=True)
source_sha256 = hashlib.sha256(DATA_PATH.read_bytes()).hexdigest()
rows_at_start = len(raw)
~~~

Inspect missingness before changing values:

~~~python
missing_report = raw.isna().sum().rename("missing").to_frame()
missing_report["percent"] = 100 * missing_report["missing"] / len(raw)
print(missing_report.sort_values("missing", ascending=False))
cleaned["satisfaction_score_was_missing"] = cleaned["satisfaction_score"].isna()
~~~

Ask whether each blank means not collected, not applicable, or lost. Preserve a flag before a justified imputation.

Normalize text without turning missing values into the string `"nan"`:

~~~python
for column in ["customer_id", "plan", "signup_channel"]:
    cleaned[column] = cleaned[column].astype("string").str.strip()
    cleaned[column] = cleaned[column].mask(cleaned[column].eq(""))
~~~

Convert numeric fields and count conversion failures:

~~~python
numeric_columns = ["tenure_months", "monthly_usage_hours",
                   "support_tickets", "satisfaction_score"]
conversion_failures = {}
for column in numeric_columns:
    was_missing = cleaned[column].isna()
    converted = pd.to_numeric(cleaned[column], errors="coerce")
    conversion_failures[column] = int((converted.isna() & ~was_missing).sum())
    cleaned[column] = converted
print(conversion_failures)
~~~

Normalize renewal from an explicit vocabulary:

~~~python
renewal_map = {"true": 1, "false": 0, "yes": 1, "no": 0,
               "1": 1, "0": 0, "1.0": 1, "0.0": 0}
renewal_text = cleaned["renewed"].astype("string").str.strip().str.lower()
unexpected = sorted(set(renewal_text.dropna().unique()) - set(renewal_map))
if unexpected:
    raise ValueError(f"Unexpected renewed values: {unexpected}")
cleaned["renewed"] = renewal_text.map(renewal_map).astype("Int64")
~~~

This rejects typos instead of guessing. Missing outcomes stay missing and fail the boundary below.

Treat exact duplicates and duplicate keys differently:

~~~python
exact_duplicate_count = int(cleaned.duplicated().sum())
cleaned = cleaned.drop_duplicates().copy()
duplicate_ids = cleaned[cleaned.duplicated("customer_id", keep=False)]
if not duplicate_ids.empty:
    raise ValueError(f"Conflicting customer rows:\n{duplicate_ids}")
~~~

Removing an exact row can be documented; choosing the first conflicting row makes file order decide truth.

Create a validation boundary for identity, outcome, and ranges:

~~~python
REQUIRED = {"customer_id", "plan", "signup_channel", "tenure_months",
            "monthly_usage_hours", "support_tickets",
            "satisfaction_score", "renewed"}
COMPLETE = ("customer_id", "plan", "signup_channel", "tenure_months",
            "monthly_usage_hours", "support_tickets", "renewed")
ALLOWED = {"plan": {"basic", "plus", "pro"}, "signup_channel": {"organic", "referral", "paid", "partner"}}
def validate_customer_data(frame):
    problems = []
    missing = sorted(REQUIRED - set(frame.columns))
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    for column in COMPLETE:
        if frame[column].isna().any():
            problems.append(f"{column} is missing")
    if frame["customer_id"].duplicated().any():
        problems.append("customer_id is not unique")
    if not frame["renewed"].dropna().isin([0, 1]).all():
        problems.append("renewed is not 0 or 1")
    for column, allowed in ALLOWED.items():
        if not set(frame[column].dropna()).issubset(allowed):
            problems.append(f"{column} has unexpected values")
    if not frame["tenure_months"].dropna().between(1, 48).all():
        problems.append("tenure_months is outside 1 to 48")
    for column in ["monthly_usage_hours", "support_tickets"]:
        if frame[column].dropna().lt(0).any():
            problems.append(f"{column} is negative")
    if not frame["satisfaction_score"].dropna().between(1, 10).all():
        problems.append("satisfaction_score is outside 1 to 10")
    for column in ["tenure_months", "support_tickets"]:
        if not frame[column].dropna().mod(1).eq(0).all():
            problems.append(f"{column} contains fractions")
    if problems:
        raise ValueError("Validation failed:\n- " + "\n- ".join(problems))
validate_customer_data(cleaned)
cleaned[["plan", "signup_channel"]] = cleaned[
    ["plan", "signup_channel"]
].astype("category")
~~~

This boundary permits missing optional satisfaction scores but rejects missing required fields. Change that policy only when the question contract changes.

~~~python
analysis_ready = cleaned.dropna(subset=["monthly_usage_hours", "satisfaction_score"]).copy()
excluded_rows = len(cleaned) - len(analysis_ready)
print(f"Excluded {excluded_rows} rows for this analysis")
~~~

Do not fill every number with its mean. That narrows variation and makes invented values look observed.

## Check

Confirm that cleaning preserved the unit and source:

~~~python
assert len(raw) == rows_at_start
assert cleaned["customer_id"].is_unique
assert len(cleaned) == rows_at_start - exact_duplicate_count

cleaning_log = {
    "source": str(DATA_PATH), "source_sha256": source_sha256,
    "rows_read": rows_at_start, "rows_cleaned": len(cleaned),
    "duplicates_removed": exact_duplicate_count,
    "conversion_failures": conversion_failures,
}
print(cleaning_log)
~~~

Write processed output to a new path and save this log beside it. The raw file remains unchanged.

## Explain

The mechanism is to preserve and identify the source; profile missingness, duplicates, and labels; normalize with explicit conversions; investigate conflicting keys; validate types, categories, ranges, and identity; make task-specific exclusions or imputations; and record every material change.

Passing validation means “fits this contract,” not “unbiased” or “true.”

## Practice

In an in-memory copy, set tenure to `-1`, satisfaction to `11`, renewal to `"maybe"`, and repeat an identifier with a different plan. Confirm which check catches each problem. Then propose separate policies for missing usage, satisfaction, and renewal; state why each is defensible and how many rows it affects.

## Guided practice journey

[Work through Try → Hint 1 → Hint 2 → tests → worked reasoning](../practice/06-cleaning.md).
You will first measure five failures, then defend task-specific repair policies.

## Keep going

Before moving on, explain why raw and cleaned data need different paths, why coercion needs a failure count, why duplicate keys cannot be solved by habit, which missing values the boundary permits, and which provenance would reproduce the result.

The next lesson turns checked tables into honest visual claims.
