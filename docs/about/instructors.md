# Instructor guide

This course is for learners who are new to Python and want to make trustworthy decisions with data. Its central classroom habit is simple: learners state expected values, types, shapes, or behavior before they run code.

## Teaching stance

Teach mechanisms before shortcuts. A learner should be able to explain what one row means, which values cross a function boundary, which axis is reduced, and which evidence could invalidate a result.

Use these norms throughout:

- ask for a prediction before execution;
- treat errors and failed checks as evidence;
- separate structural correctness from substantive meaning;
- require plain-language explanations beside code;
- invite adversarial examples that challenge a claim;
- open solutions after a genuine attempt, then compare reasoning rather than keystrokes.

The goal is not to cover every method. It is to build judgment that transfers to unfamiliar data.

## One-day quick format

The quick format is a guided survey for learners who need a coherent first workflow. Keep examples small and provide starter code.

| Time | Focus | Learner output |
| --- | --- | --- |
| 09:00–09:30 | Question contract | unit, target, cutoff, baseline, failure mode |
| 09:30–10:30 | Python values and functions | predicted types plus tested helper function |
| 10:45–11:45 | NumPy and pandas structure | annotated shapes, axes, grain, schema checks |
| 11:45–12:15 | Retrieval practice | explain one mechanism without notes |
| 13:00–14:15 | Cleaning and exploration | transformation ledger and two honest charts |
| 14:30–15:30 | Evaluation | baseline, split rationale, leakage challenge |
| 15:30–16:30 | Mini-capstone | reproducible answer to one bounded question |
| 16:30–17:00 | Peer audit | evidence, limitation, and next decision |

Skip optional extensions before skipping prediction, checks, or explanation. A smaller complete workflow teaches more than a rushed catalogue.

## Multi-session full format

Use six to eight sessions of 90–150 minutes. Leave time between meetings for short practice and retrieval.

1. **Questions and Python values:** decision framing, row unit, target timing, names, types, expressions.
2. **Functions and collections:** contracts, pure functions, conditions, loops, comprehensions, boundary tests.
3. **Arrays and tables:** shape, axis, dtype, grain, selection, grouping, joining, missingness.
4. **Cleaning and exploration:** transformation ledgers, distributions, rates, visual choices, uncertainty.
5. **Evaluation:** baselines, splits, leakage, metrics, thresholds, subgroup behavior.
6. **Reproducibility and communication:** environments, tests, version control, claim-first writing.
7. **Capstone studio:** small-group build with instructor checkpoints.
8. **Capstone review:** reproduction, presentation, adversarial audit, revision.

Begin each session with a five-minute retrieval prompt from the previous one. End with an exit ticket: one mechanism the learner can explain and one assumption they still need to test.

## The predict–run–explain loop

For every important snippet:

1. **Frame:** name the question and inputs.
2. **Predict:** learners write the expected output and type or shape.
3. **Run:** execute once without editing the prediction.
4. **Compare:** mark agreement or the exact mismatch.
5. **Explain:** trace the mechanism in plain language.
6. **Check:** add a boundary or adversarial case.

Cold-calling predictions can punish uncertainty. Prefer silent writing, a quick vote, then discussion. This gives every learner a committed idea to inspect.

## Pair explanation

Pairs alternate roles:

- the **driver** runs or edits code but must first describe the next operation;
- the **auditor** tracks grain, types, shapes, timing, and possible failure;
- both agree on an expected result before execution;
- roles switch every 10–15 minutes.

Ask auditors to use questions rather than take over the keyboard: “What does axis 0 represent?” or “Could this column exist at decision time?”

## Adversarial checks

After a result works, assign a deliberate attempt to break it:

- use an empty collection or boundary value;
- introduce a duplicate key or missing category;
- change the time split;
- remove the strongest feature;
- compare with a simpler baseline;
- inspect a subgroup or period where the claim may fail;
- reverse a chart or metric choice and explain what changes.

Reward a well-explained failure as strongly as a passing result. The question is whether the learner discovers the limit before a reader does.

## Open solutions

Publish solutions with the course materials or reveal them after the attempt window. A solution should include:

- an expected output before code;
- one clear implementation, not every clever alternative;
- checks for the main contract and boundary;
- a short explanation of mechanism and judgment;
- at least one plausible wrong approach and why it fails.

Have learners annotate differences between their approach and the solution. Matching output alone is insufficient if grain, timing, or assumptions differ.

## Auditing AI-assisted work

AI tools may help explain an error, propose a test, or draft repetitive code, but generated output is an untrusted contribution. Require learners to keep a short audit note:

1. What was requested from the tool?
2. Which code or claim was accepted, changed, or rejected?
3. Which types, shapes, sources, and time boundaries were verified?
4. Which test could distinguish a convincing answer from a correct one?
5. Can the learner explain every submitted line without the tool?

An effective exercise is to provide a plausible generated analysis containing one leakage feature, one grain mistake, and one misleading metric. Pairs find the defects, add checks, and rewrite the conclusion.

Do not grade prompt style. Grade ownership of evidence, verification, and explanation.

## Capstone rubric

Score each dimension from 0 to 3: **0 absent**, **1 attempted**, **2 sound**, **3 unusually clear and well challenged**.

| Dimension | Evidence expected |
| --- | --- |
| Question and decision | unit, target, timing, baseline, success criterion |
| Data contract | schema, grain, joins, missingness, coverage checks |
| Method judgment | justified cleaning, exploration, statistic or model |
| Evaluation | leakage controls, suitable split and metric, uncertainty |
| Reproducibility | declared environment, runnable workflow, focused tests |
| Communication | answer-first claim, honest visual, limitation, next action |
| Explanation | learner can trace mechanisms and defend choices |
| Adversarial audit | meaningful attempt to disprove the result |

A project should not pass on aggregate score alone if it exposes private data, uses known leakage, cannot be reproduced, or makes an unsupported causal claim. Allow revision after feedback; the revision is part of the learning outcome.

## Before teaching

- Run every example in a clean environment.
- Confirm datasets and site links are available without private credentials.
- Prepare one expected mistake for each mechanism.
- Decide when solutions open and how pairs will rotate.
- Make accessibility and installation alternatives visible in advance.
- Reserve time for explanation, not only execution.
