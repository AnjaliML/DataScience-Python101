"""Deterministic, claim-led figures for the reference workflow."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure

COLORS = {"ink": "#14213d", "blue": "#2457d6", "teal": "#0f766e"}


def plot_renewal_by_plan(customers: pd.DataFrame) -> Figure:
    """Plot renewal rate and sample size for each plan."""

    summary = (
        customers.groupby("plan", observed=True)["renewed"]
        .agg(rate="mean", customers="size")
        .sort_values("rate")
    )
    figure, axis = plt.subplots(figsize=(7.2, 4.4), layout="constrained")
    bars = axis.barh(summary.index, summary["rate"], color=COLORS["blue"])
    axis.bar_label(
        bars,
        labels=[f"{rate:.0%} · n={count}" for rate, count in summary.to_numpy()],
        padding=5,
        color=COLORS["ink"],
    )
    axis.set(xlim=(0, 1), xlabel="Observed renewal rate", ylabel="Plan")
    axis.set_title("Renewal differs by plan in the synthetic sample", loc="left")
    axis.spines[["top", "right", "left"]].set_visible(False)
    axis.grid(axis="x", alpha=0.2)
    return figure


def plot_confusion(values: list[list[int]]) -> Figure:
    """Plot a two-class confusion matrix with explicit counts."""

    figure, axis = plt.subplots(figsize=(5.2, 4.5), layout="constrained")
    image = axis.imshow(values, cmap="Blues")
    for row in range(2):
        for column in range(2):
            axis.text(
                column,
                row,
                str(values[row][column]),
                ha="center",
                va="center",
                color="white"
                if values[row][column] > max(map(max, values)) / 2
                else "black",
                fontweight="bold",
            )
    axis.set(
        xticks=[0, 1],
        yticks=[0, 1],
        xticklabels=["Renewed", "Did not renew"],
        yticklabels=["Renewed", "Did not renew"],
        xlabel="Predicted outcome",
        ylabel="Observed outcome",
        title="Holdout errors · positive class is non-renewal",
    )
    figure.colorbar(image, ax=axis, shrink=0.8, label="Customers")
    return figure


def save_figure(figure: Figure, path: str | Path) -> None:
    """Save and close a figure using stable course defaults."""

    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(destination, dpi=160, bbox_inches="tight", metadata={"Date": None})
    plt.close(figure)


def close_all() -> None:
    """Close figures created in examples or tests."""

    plt.close("all")
