"""Generate the deterministic synthetic dataset used throughout the course."""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

SEED = 20260710
ROWS = 240


def sigmoid(values: np.ndarray) -> np.ndarray:
    """Map real-valued scores to probabilities."""

    return 1.0 / (1.0 + np.exp(-values))


def main() -> None:
    """Write a stable, fictional customer-renewal table."""

    rng = np.random.default_rng(SEED)
    plan = rng.choice(["basic", "plus", "pro"], ROWS, p=[0.46, 0.35, 0.19])
    channel = rng.choice(
        ["organic", "referral", "paid", "partner"],
        ROWS,
        p=[0.38, 0.27, 0.24, 0.11],
    )
    tenure = rng.integers(1, 49, ROWS)

    plan_usage = np.select(
        [plan == "plus", plan == "pro"],
        [3.0, 6.5],
        default=0.0,
    )
    usage = np.clip(
        rng.normal(8.0 + 0.34 * tenure + plan_usage, 6.0, ROWS),
        0.5,
        60.0,
    )
    tickets = rng.poisson(1.25 + 0.8 * (usage < 8), ROWS)
    satisfaction_complete = np.clip(
        rng.normal(6.8 + 0.075 * usage - 0.52 * tickets, 1.25, ROWS),
        1.0,
        10.0,
    )

    plan_effect = np.select(
        [plan == "plus", plan == "pro"],
        [0.20, 0.42],
        default=0.0,
    )
    channel_effect = np.select(
        [channel == "referral", channel == "partner", channel == "paid"],
        [0.30, 0.15, -0.18],
        default=0.0,
    )
    renewal_score = (
        -3.7
        + 0.065 * tenure
        + 0.065 * usage
        + 0.38 * (satisfaction_complete - 5.0)
        - 0.45 * tickets
        + plan_effect
        + channel_effect
    )
    renewed = rng.binomial(1, sigmoid(renewal_score))

    satisfaction = np.round(satisfaction_complete, 1).astype(object)
    missing = rng.choice(ROWS, size=18, replace=False)
    satisfaction[missing] = ""

    destination = Path(__file__).resolve().parents[1] / "data" / "customer_renewals.csv"
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(
            [
                "customer_id",
                "plan",
                "signup_channel",
                "tenure_months",
                "monthly_usage_hours",
                "support_tickets",
                "satisfaction_score",
                "renewed",
            ]
        )
        for index in range(ROWS):
            writer.writerow(
                [
                    f"C{index + 1:04d}",
                    plan[index],
                    channel[index],
                    int(tenure[index]),
                    f"{usage[index]:.1f}",
                    int(tickets[index]),
                    satisfaction[index],
                    int(renewed[index]),
                ]
            )

    print(f"wrote {ROWS} rows to {destination}")


if __name__ == "__main__":
    main()
