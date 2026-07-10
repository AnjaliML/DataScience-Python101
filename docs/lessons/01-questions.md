# 01 — From a decision to a data question

Data science starts before code. A useful analysis connects a real decision to a table whose rows, columns, and timing are unambiguous.

By the end of this lesson, you will be able to write a small **question contract**: what one row represents, what must be predicted, what information is available, how success is judged, and how the work could fail.

## Frame

Imagine a subscription team asking, “Which customers should we contact?” A computer cannot answer yet: contact them about what, at what time, based on which evidence, and with what result?

First name the decision: before a renewal decision, prioritise customers for a
helpful check-in. Then ask an answerable question:

> Using pre-decision account information, which customers are at greater risk
> of not renewing at the current decision?

Five parts make this question testable:

| Part | Meaning | Renewal example |
| --- | --- | --- |
| Unit of observation | What exactly one row describes | one customer at one renewal decision |
| Target | The outcome to learn or estimate | renewed at this decision: `1` or `0` |
| Features | Information allowed at prediction time | plan, channel, tenure, usage, support, satisfaction |
| Success criterion | A measurable improvement tied to the decision | find more likely non-renewers than the current rule |
| Failure modes | Ways a plausible answer could mislead | late data, leakage, duplicate customers, unequal errors |

The unit is not automatically “a customer.” A real customer might hold two
subscriptions or encounter several decision dates. In this teaching table,
`customer_id` is unique and each fictional customer contributes one row.

The raw target remains `renewed`: `1` means renewed and `0` means not
renewed. Later, evaluation treats **not renewed** as the positive class because
that is the event the prioritisation decision tries to find.

## Predict

Before opening `data/customer_renewals.csv`, write down what you expect.

1. What should one row represent?
2. Which column should contain the eventual outcome?
3. Which columns must exist before the renewal outcome becomes known?
4. Which values would be impossible or suspicious?
5. Which column should uniquely identify a row?

Then predict the behavior of this small question specification before running it:

```python
question = {
    "unit": "customer at one renewal decision",
    "key": "customer_id",
    "target": "renewed",
    "target_values": {0, 1},
    "later_positive_evaluation_class": "not renewed",
}

print(type(question))
print(question["target"] == "renewed")
```

State both expected outputs and their types. Prediction is a habit: it makes misunderstandings visible before they become results.

## Build

Start with the unit of observation. Complete this sentence without using the word “data”:

> Each row represents ______ observed at ______.

“One customer at one renewal decision” tells us what must be unique and when
features must be frozen. In this table, `customer_id` should not repeat. A
future event table might instead need a compound key such as
`(customer_id, decision_date)`.

Next define the target as an observable rule, not a vague business word:

```python
target_rule = {
    "name": "renewed",
    "one_when": "the customer renewed at the observed decision",
    "zero_when": "the customer did not renew",
    "known_after": "the renewal decision",
}
```

A good target rule says which event counts, what time window applies, and when the answer becomes known. “Customer loyalty” does none of these.

Now divide possible columns by time:

```python
feature_timing = {
    "tenure_months": "available",
    "plan": "available",
    "monthly_usage_hours": "available",
    "support_tickets": "available",
    "satisfaction_score": "available when the survey was answered",
    "renewal_confirmation_sent": "future outcome",
}
```

Only features available at the decision moment may be used. A future payment date would reveal the answer. That is **target leakage**: excellent-looking performance produced by information the real decision cannot have.

Write a success criterion with a baseline and a constraint:

```python
success = {
    "baseline": "predict the most common outcome",
    "primary_measure": "non-renewers found among prioritised customers",
    "constraint": "review a fixed number of customers per week",
}
```

This is more useful than “achieve high accuracy.” If 90% of customers renew, always predicting renewal is 90% accurate and finds no one who needs help.

Finally, list failure modes before analysis. Include at least one from each group:

- **Definition:** renewals and later reactivations are mixed together.
- **Timing:** a feature was updated after the renewal decision.
- **Structure:** duplicate rows make some customers count twice.
- **Coverage:** new customers or a sales channel are missing.
- **Decision cost:** too many people are flagged for the team to contact.
- **Human impact:** errors are concentrated in a particular customer group.

## Check

Use questions as checks, not as decoration.

```python
required_parts = {
    "unit",
    "key",
    "target",
    "target_values",
    "later_positive_evaluation_class",
}

assert required_parts.issubset(question)
assert question["target_values"] == {0, 1}
assert question["key"] != question["target"]
```

Before running, predict whether each assertion passes. If an assertion fails, Python is telling you which assumption is not encoded as expected; it is not proving the business definition is correct.

When you later inspect the table, check claims implied by the contract:

```python
# These checks become possible after the dataset is loaded as `customers`.
assert customers["customer_id"].notna().all()
assert customers["customer_id"].is_unique
assert customers["renewed"].isin([0, 1]).all()
assert customers["tenure_months"].between(1, 48).all()
```

Predict the result of every check first. A failed uniqueness check may mean bad data, or it may mean your proposed unit was wrong.

## Explain

A dataset does not contain a question by itself. People choose the rows, labels, time windows, and measures. Those choices determine what an analysis can honestly claim.

The mechanism is:

1. A decision fixes **who or what** can receive an action.
2. Its timing fixes **when** information must be available.
3. The desired consequence fixes a measurable **target**.
4. Capacity and error costs fix the **success criterion**.
5. Assumptions imply **checks** and predictable failure modes.

Notice that prediction quality and decision quality are related but different. A model may estimate renewal accurately while the reminder has no effect. Prediction asks what is likely; an intervention question asks what will change because we act.

## Practice

Choose one decision: send a reminder, review an application, restock an item, or schedule support. Write a question contract with all five parts.

Then revise these weak questions:

1. “Why do customers leave?”
2. “Can we predict sales?”
3. “Which users are valuable?”

For each revision, specify a unit, target, decision time, feature cutoff, and success criterion.

For the renewal scenario, decide whether each item is a valid feature and explain why:

- current plan recorded before the decision
- monthly usage measured before the decision
- a cancellation reason entered after non-renewal
- renewal confirmation status
- support tickets recorded before the decision

Finally, invent two checks that could disprove your assumptions. Strong checks have a clear expected result, such as a unique key or an allowed set of target values.

## Keep going

Keep your question contract beside the analysis and update it when definitions change. In the next lesson, you will encode small, readable claims with Python names, values, types, and expressions.

Before moving on, you should be able to state what one row represents, when prediction happens, when its outcome becomes known, which information is permitted, what would beat the baseline, and which failure would make you stop rather than publish.
