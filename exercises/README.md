# Exercises

The exercises are small enough to inspect completely. Each one asks for a
prediction, a focused implementation, an adversarial check, and a short
explanation.

Run an exercise from its directory so `starter.py` is importable:

```bash
cd exercises/02-functions
uv run pytest -q
```

The first run should fail for exercises with unfinished starter code. Make the
smallest change that satisfies the stated contract. Open the matching file in
`solutions/` only after a genuine attempt.

| Exercise | Main decision |
| --- | --- |
| 01 Questions | define row, target, comparison, and failure modes |
| 02 Functions | encode a metric contract and invalid-input policy |
| 03 NumPy | preserve shape while standardising columns |
| 04 DataFrames | group without losing counts or mutating the input |
| 05 Cleaning | measure quality failures before choosing a repair |
| 06 Modelling | separate features and target before fitting a baseline |
