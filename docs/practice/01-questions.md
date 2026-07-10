# Practice 01 — Make the question answerable

Return to [lesson 01](../lessons/01-questions.md) if unit, target, timing, or
baseline is still unfamiliar.

## Worked warm-up

Weak request: “Which customers need help?”

One defensible first draft is:

> Before each renewal decision, rank subscription accounts by the chance of
> non-renewal using information recorded before that decision, so a team that
> can contact 100 accounts can find more eventual non-renewals than a
> current priority rule that also selects 100 accounts.

The draft names a decision, unit, decision time, outcome, information cutoff,
capacity, and capacity-matched comparison. A majority-outcome classifier would
not be a usable ranking baseline because it does not choose which 100 accounts
to contact. The draft does **not** claim that contact will cause renewal.

## Try

### Completion — finish the renewal contract

Copy and complete this worksheet in plain language. No Python is required.

```text
decision:
one row represents:
row key:
decision time:
target and allowed outcomes:
features must be recorded before:
baseline:
success rule and capacity:
costly false positive:
costly false negative:
stop-the-analysis failure:
```

Then classify each candidate feature as **available**, **too late**, or
**uncertain**: current plan, last month's usage, cancellation reason, renewal
confirmation, unresolved tickets, and a survey with no recorded date.

### Transfer — frame a different decision

Choose one: restock a product, review an application, schedule maintenance, or
prioritise support. Write a one-sentence question and the same contract. Make
the unit more precise than “item”, “person”, or “machine”.

## Hint 1

??? tip "Reveal Hint 1"
    Start with the action and clock: “At ___, decide which ___ will ___.” The
    row unit should be something that can actually receive that action.

## Hint 2

??? tip "Reveal Hint 2"
    If a field changes because the outcome happened, it is too late. If you
    cannot prove when it was recorded, mark it uncertain rather than quietly
    treating it as available.

## Tests or rubric

Score one point for each statement you can support:

- [ ] A stranger could tell exactly what one row represents.
- [ ] The target has observable allowed outcomes and a time window.
- [ ] The feature cutoff is earlier than the outcome.
- [ ] The baseline and capacity make “better” measurable.
- [ ] Both error types have a consequence, not just a name.
- [ ] At least one failure would make you stop rather than publish.
- [ ] The final claim is predictive unless an intervention design supports causation.

Revise before continuing if the first four boxes are not checked.

## Worked reasoning

??? success "Reveal one defensible reasoning path"
    The cancellation reason and renewal confirmation are too late because they
    are created with or after the outcome. Last month's usage and unresolved
    tickets are usable only if their timestamps precede the decision. An
    undated survey is uncertain. A useful stop rule is “decision timestamps are
    missing, so feature availability cannot be verified.” That failure attacks
    the question's timing, not merely the code.

    For maintenance, a transfer question might be: “At Monday planning time,
    which operating machine-week records are most likely to include an
    unplanned stoppage in the next seven days, using sensor readings frozen by
    Sunday midnight?” The key could be `(machine_id, week_start)`, not just
    `machine_id`, because the same machine appears in many weeks.

Next: [lesson 02](../lessons/02-python-basics.md) or
[practice 02](02-python-basics.md).
