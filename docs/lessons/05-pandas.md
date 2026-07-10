# 05 — Pandas: questions into table operations

A pandas table is a collection of labelled columns, not a spreadsheet with prettier syntax. Every operation should express a claim about rows, columns, or keys.

By the end, you will be able to inspect, select, filter, sort, assign, group, and merge without letting an accidental index decide which customer is which.

## Frame

We will use `data/customer_renewals.csv`. One row should describe one customer and one renewal outcome. The columns describe identity, plan, signup channel, tenure, usage, support, satisfaction, and renewal.

A **DataFrame** is a two-dimensional table. A **Series** is one labelled column. Both have an index, but that index is not automatically a customer identifier.

Our working question is:

> Which plans have many customers, high usage, and low satisfaction?

That question requires inspection, selection, calculation, grouping, and checks. Before each step, name what one output row will represent.

## Predict

Predict the type and shape of these results:

~~~python
customers["monthly_usage_hours"]
customers[["monthly_usage_hours"]]
~~~

Single brackets select a Series. A list inside brackets selects a DataFrame, even when the list contains one column.

Now predict which rows this Boolean mask selects:

~~~python
mask = (customers["support_tickets"] >= 3) & (
    customers["satisfaction_score"] < 3
)
~~~

Each comparison creates a Boolean Series. The `&` combines values with matching index labels. Parentheses make the intended precedence explicit.

## Build

Load the file and check its schema before analysing values:

~~~python
from pathlib import Path
import pandas as pd

DATA_PATH = Path("data/customer_renewals.csv")
customers = pd.read_csv(DATA_PATH)

expected = {
    "customer_id", "plan", "signup_channel", "tenure_months",
    "monthly_usage_hours", "support_tickets", "satisfaction_score", "renewed",
}
missing = sorted(expected - set(customers.columns))
assert not missing, f"Missing columns: {missing}"

print(customers.shape)
print(customers.head(3))
customers.info()
~~~

`head` shows examples, not guarantees. Build a full schema summary:

~~~python
schema = customers.dtypes.rename("dtype").to_frame()
schema["missing"] = customers.isna().sum()
schema["unique"] = customers.nunique(dropna=False)
print(schema)
~~~

Use `.loc[rows, columns]` to make both dimensions visible:

~~~python
attention_needed = customers.loc[
    (customers["support_tickets"] >= 3)
    & (customers["satisfaction_score"] < 3),
    ["customer_id", "plan", "support_tickets", "satisfaction_score"],
].copy()
~~~

The copy is safe to modify. Without it, chained selection can leave unclear whether an assignment changes the original table.

Create derived columns and a reproducible order:

~~~python
assert customers["tenure_months"].between(1, 48).all()

priority = customers.assign(
    tickets_per_month=lambda x: (
        x["support_tickets"] / x["tenure_months"]
    ),
    needs_attention=lambda x: (
        (x["support_tickets"] >= 3) & (x["satisfaction_score"] < 3)
    ),
).sort_values(
    ["needs_attention", "satisfaction_score", "customer_id"],
    ascending=[False, True, True], kind="stable",
).reset_index(drop=True)
~~~

The range check enforces the dataset contract before division instead of hiding an invalid zero. A stable sort preserves input order among ties. Resetting the index simplifies display; it does not create a durable key.

Summarize one row per plan:

~~~python
plan_summary = customers.groupby(
    "plan", as_index=False, dropna=False, observed=True
).agg(
    customers=("customer_id", "nunique"),
    average_usage=("monthly_usage_hours", "mean"),
    median_tickets=("support_tickets", "median"),
    average_satisfaction=("satisfaction_score", "mean"),
).sort_values("customers", ascending=False, kind="stable")
~~~

`as_index=False` keeps the group key as a column. `dropna=False` exposes missing plans instead of silently excluding them.

Merge on named keys with a declared relationship:

~~~python
channel_lookup = customers[["signup_channel"]].drop_duplicates().assign(
    channel_label=lambda x: x["signup_channel"].astype("string")
    .str.replace("_", " ", regex=False).str.title()
)
assert channel_lookup["signup_channel"].is_unique

enriched = customers.merge(
    channel_lookup,
    how="left",
    on="signup_channel",
    validate="many_to_one",
    indicator=True,
)
~~~

`many_to_one` permits many customers per channel but rejects repeated lookup keys. The indicator reveals unmatched rows.

Avoid `.join` until you intentionally want index-based alignment. Pandas also aligns a Series by index during assignment, not by visible row position. Keep real identifiers in columns; reset an index only for presentation.

## Check

Turn structural assumptions into executable checks:

~~~python
assert customers["customer_id"].notna().all()
assert customers["customer_id"].is_unique
assert len(enriched) == len(customers)
assert enriched["_merge"].eq("both").all()
assert plan_summary["customers"].sum() == customers["customer_id"].nunique()

assert attention_needed["support_tickets"].ge(3).all()
assert attention_needed["satisfaction_score"].lt(3).all()
~~~

The group-total check is valid because each customer has one row and one plan. With repeated customer events, use the event key or compare the correct unit instead.

Do not remove a failed assertion merely to continue. Decide whether the table, the question, or the assumption is wrong.

## Explain

The mechanism is to inspect the schema, select explicitly, derive from named columns, group only after naming the output unit, merge with cardinality validation, and check keys, counts, matches, and values.

An index is useful for alignment, but accidental alignment is dangerous. A customer identifier belongs in a column and should be validated directly.

## Practice

1. Select customers with at least 12 months of tenure and fewer than two tickets.
2. Sort by usage descending, breaking ties by `customer_id`.
3. Define `usage_per_ticket`, first deciding what zero tickets means.
4. Summarize count and median usage by signup channel.
5. Merge a one-row-per-plan lookup with `validate="many_to_one"`.

Before each operation, predict the output unit, row count, and columns. Then write an assertion that could fail.

## Keep going

Before moving on, explain why one bracket returns a Series, why `.loc` aids review, what a row means after `groupby`, why merges need cardinality checks, and why an index must not silently become customer identity.

The next lesson treats cleaning as a documented validation boundary, not a pile of convenient replacements.
