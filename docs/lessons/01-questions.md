# 01 — From a decision to a data question

Data science starts before code. A useful analysis connects a real decision to
rows, fields, and timing that another person can challenge.

**No programming is required in this lesson.** The main artifact is a
plain-language question contract. An optional code preview appears near the end
for learners who are curious about how the same claims later become checks.

By the end, you will be able to state what one row represents, what outcome is
measured, which information is available in time, how success is judged, and
what failure should stop the work.

## Frame

Imagine a subscription team asking, “Which customers should we contact?” It is
not answerable yet. Contact them about what? At what moment? Using which
evidence? What result would make the effort useful?

First name the decision: **before a renewal decision, prioritise accounts for a
helpful check-in**. Then write an answerable question:

> Using account information recorded before the renewal decision, which
> accounts are at greater risk of not renewing at that decision?

Five parts make the question testable:

| Part | Plain-language meaning | Renewal example |
| --- | --- | --- |
| Unit | What exactly one row describes | one subscription account at one renewal decision |
| Outcome | What later event is measured | renewed: yes or no |
| Available evidence | What is known before acting | plan, tenure, earlier usage, earlier support history |
| Success rule | What must improve, under what constraint | find more eventual non-renewals than the current priority rule when both review 100 accounts |
| Failure modes | What could make the answer misleading | late data, repeated accounts, missing groups, unequal error costs |

The unit is not automatically “a customer.” One person might have two
subscriptions or several renewal dates. In this teaching table, each fictional
`customer_id` represents one account at one observed renewal decision.

## Predict

Before opening the table, write your expectations in ordinary sentences:

1. One row should represent…
2. The later outcome should be recorded as…
3. These fields must already exist when the decision is made…
4. These values would be impossible or suspicious…
5. This field, or combination of fields, should identify one row…

Do not look for the “right” wording yet. A prediction gives the table something
specific to disagree with.

## Build

Copy this worksheet into your reasoning log:

```text
decision:
population covered:
one row represents:
row key:
decision time:
outcome and allowed values:
when the outcome becomes known:
permitted evidence and its cutoff:
baseline:
success rule and capacity:
cost of a false alarm:
cost of a missed case:
failure that would stop the analysis:
```

### 1. Make the row visible

Complete this sentence without using the word “data”:

> Each row represents ______ observed at ______.

For this course: “Each row represents one subscription account observed at one
renewal decision.” That statement implies a key and a clock. In a table with
many decisions per account, the key might need both account ID and decision
date.

### 2. Define an observable outcome

Avoid a vague label such as “loyal”. State what event counts, its allowed
outcomes, and when it becomes known:

| Question | Renewal contract |
| --- | --- |
| What is measured? | whether the account renewed at this decision |
| Which outcomes are allowed? | renewed or did not renew |
| When is the answer known? | after the renewal decision |

Later lessons store those outcomes as `1` and `0`, but the words come first.

### 3. Draw the time boundary

Classify possible evidence as **available**, **too late**, or **uncertain**:

| Field | Classification | Reason |
| --- | --- | --- |
| plan recorded before the decision | available | exists when prioritisation happens |
| earlier monthly usage | available | measured before the cutoff |
| cancellation reason | too late | created because non-renewal happened |
| renewal confirmation | too late | directly reveals the outcome |
| survey without a timestamp | uncertain | availability cannot be verified |

Using information created with or after the outcome is **target leakage**. It
can make a model look excellent while making the real decision impossible.

### 4. Make “better” measurable

“Achieve high accuracy” is not enough. If most accounts renew, always saying
“renew” can have high accuracy while finding none of the accounts the team
wants to review. It is also not a capacity-matched ranking baseline: it does
not say which 100 accounts should be contacted.

A stronger success rule names:

- a capacity-matched baseline, such as the current priority rule or a seeded
  random selection of the same 100 accounts;
- a scarce resource, such as 100 reviews per week;
- the useful event, such as eventual non-renewals found;
- error consequences for unnecessary contacts and missed accounts.

### 5. Name failure before analysis

Include at least one threat from each group:

- **Definition:** later reactivations are mixed with on-time renewals.
- **Timing:** a field was updated after the decision.
- **Structure:** repeated rows give some accounts extra weight.
- **Coverage:** a channel or newly arrived account group is absent.
- **Decision cost:** the rule flags more accounts than the team can review.
- **Human impact:** errors concentrate in a particular group.

## Check

Challenge the contract without writing code:

- If one account appears twice, does the proposed key expose it?
- If only dissatisfied people answer the survey, what population does that
  score describe?
- If a field has no timestamp, can its pre-decision status be defended?
- If 90% of rows share one outcome, what does the baseline achieve?
- If the team can review only 100 cases, can the success rule be acted on?
- Which failure would make you stop rather than simply add a caveat?

Ask another learner to read only your contract. If they cannot answer “who,
when, what outcome, compared with what, and where the claim stops,” revise it.

## Explain

A dataset does not contain a question by itself. People choose the rows,
labels, windows, and measures; those choices determine what the analysis can
honestly claim.

The mechanism is:

1. A decision fixes who or what can receive an action.
2. Its timing fixes which information is available.
3. The desired consequence fixes an observable outcome.
4. Capacity and error costs fix the success rule.
5. Assumptions imply checks and predictable failure modes.

Prediction and intervention remain different. Estimating who may not renew
does not show that contacting them will change renewal. That causal question
requires evidence about what happens because of the action.

??? note "Optional code preview — safe to skip"
    Later, the plain-language contract can become a small Python dictionary:

    ```python
    question = {
        "unit": "account at one renewal decision",
        "key": "customer_id",
        "target": "renewed",
        "target_values": {0, 1},
        "positive_evaluation_class": "not renewed",
    }
    ```

    Checks can then ask whether the structure matches the stated contract:

    ```python
    required = {"unit", "key", "target", "target_values"}
    assert required.issubset(question)
    assert question["target_values"] == {0, 1}
    assert question["key"] != question["target"]
    ```

    These checks confirm that the specification has the expected pieces. They
    cannot prove that the business definition, timing, or human impact is right.

## Practice

Revise one weak request—“Why do customers leave?”, “Can we predict sales?”, or
“Which users are valuable?”—using the worksheet. Specify unit, outcome,
decision time, evidence cutoff, baseline, capacity, error costs, and a stop
rule.

## Guided practice journey

[Work through Try → Hint 1 → Hint 2 → rubric → worked reasoning](../practice/01-questions.md).
It starts in plain language and then transfers the contract to a new decision.

## Keep going

Before moving on, you should be able to state what one row represents, when the
decision happens, when its outcome becomes known, which information is
permitted, what would beat the baseline, and which failure would make you stop.

Next, [lesson 02](02-python-basics.md) turns small claims into Python names,
values, types, and expressions.
