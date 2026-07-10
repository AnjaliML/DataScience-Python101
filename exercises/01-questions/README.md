# Exercise 01 — Make the question answerable

## Frame

A product manager asks: “Which customers are happy?” You receive a table with
one row per account, recent usage, support tickets, a sometimes-missing survey
score, and whether the account renewed.

## Predict

Before writing Python, predict one way that each definition below could change
the answer:

- “customer”;
- “happy”;
- “recent”;
- “renewed”.

## Build

Write an analysis contract containing:

1. the decision the result will inform;
2. the population and unit of observation;
3. one outcome and the time at which it becomes known;
4. three candidate features and when they become known;
5. one comparison or baseline;
6. a success metric and an unacceptable failure;
7. two limitations the available table cannot resolve.

Then sketch the pipeline as boxes and arrows. Mark every step that can change a
row count.

## Check

Challenge the contract with these cases:

- the same account appears twice;
- only dissatisfied customers answer the survey;
- one feature was recorded after the renewal decision;
- the positive class is much more common than the negative class.

Revise the contract where necessary.

## Explain

In three sentences, state what your proposed analysis could support, what it
could not prove, and what additional data would most improve it.
