import pandas as pd

from ds_python101.plotting import (
    close_all,
    plot_confusion,
    plot_renewal_by_plan,
)


def test_plan_plot_states_rate_and_group(customers: pd.DataFrame) -> None:
    figure = plot_renewal_by_plan(customers)
    axis = figure.axes[0]

    assert axis.get_xlabel() == "Observed renewal rate"
    assert axis.get_ylabel() == "Plan"
    assert len(axis.patches) == 3
    assert all("n=" in label.get_text() for label in axis.texts)
    close_all()


def test_confusion_plot_labels_observed_and_predicted() -> None:
    figure = plot_confusion([[12, 3], [4, 21]])
    axis = figure.axes[0]

    assert axis.get_xlabel() == "Predicted outcome"
    assert axis.get_ylabel() == "Observed outcome"
    assert {label.get_text() for label in axis.texts} == {"12", "3", "4", "21"}
    close_all()
