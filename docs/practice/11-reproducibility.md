# Practice 11 — Rebuild without hidden state

This on-site lab pairs with [lesson 11](../lessons/11-reproducibility.md).

## Worked warm-up

A result is reproducible when a reviewer can identify the input bytes, code
revision, environment, command, seed, and outputs. A random seed alone is not a
reproducibility plan, and a checksum alone does not make data representative or
lawful.

## Try

### Completion — finish a provenance record

For one lesson output, complete:

```text
question and row unit:
input path and SHA-256:
code revision:
Python and package environment:
exact command:
random seed and where it is used:
output paths:
tests run:
known limitations:
```

Restart from a clean Python process and rebuild the artifact.

### Transfer — reproduce from elsewhere

Ask another learner, or use a fresh clone/directory, to rebuild using only the
README and locked environment. Do not give verbal corrections. Record the
first ambiguity they encounter and repair the instructions or interface.

## Hint 1

??? tip "Reveal Hint 1"
    Capture commands as executed from the repository root. Replace local
    absolute paths in durable instructions with project-relative paths.

## Hint 2

??? tip "Reveal Hint 2"
    Separate exploratory notebooks from source-of-truth functions. Restarting
    and running all cells is a useful check, but another artifact should import
    durable logic rather than copy it.

## Tests or rubric

- [ ] Raw input is unchanged and identified by checksum.
- [ ] The environment is installable from the lock file.
- [ ] One documented command rebuilds named outputs from a clean process.
- [ ] Seeds control every stochastic step that affects the result.
- [ ] Tests protect contracts, not a preferred scientific conclusion.
- [ ] Git diff contains no secrets, caches, environments, or accidental outputs.
- [ ] A second person can follow the instructions without an oral patch.

## Worked reasoning

??? success "Reveal worked reasoning"
    Reproduction failures are evidence about hidden assumptions. If a command
    works only from one directory, path handling is part of the bug. If a
    notebook needs an old cell state, execution order is part of the bug. If
    package versions drift, the environment claim was incomplete. Record the
    first divergence rather than manually nudging the process past it.

Next: [lesson 12](../lessons/12-tools.md) or [practice 12](12-tools.md).
