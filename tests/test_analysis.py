import pandas as pd

from ds_python101.analysis import FEATURES, renewal_summary, train_and_evaluate


def test_summary_is_json_safe_and_keeps_group_rates(customers: pd.DataFrame) -> None:
    summary = renewal_summary(customers)

    assert summary["rows"] == 240
    assert 0 < summary["renewal_rate"] < 1
    assert summary["missing_satisfaction"] == 18
    assert set(summary["renewal_rate_by_plan"]) == {"basic", "plus", "pro"}


def test_model_uses_declared_features_and_holdout(customers: pd.DataFrame) -> None:
    result = train_and_evaluate(customers, random_state=42)

    assert list(result.x_test.columns) == list(FEATURES)
    assert len(result.x_test) == 60
    assert len(result.predictions) == 60
    assert set(result.metrics) == {"accuracy", "precision", "recall", "f1", "roc_auc"}
    assert result.metrics["roc_auc"] > result.baseline_metrics["roc_auc"]
    assert sum(map(sum, result.confusion)) == 60
    assert result.y_test.name == "not_renewed"
    assert 0.2 <= result.decision_threshold <= 0.8
    assert set(result.cross_validation) == {
        "accuracy",
        "precision",
        "recall",
        "f1",
        "roc_auc",
    }
    assert all(
        set(values) == {"mean", "std"} for values in result.cross_validation.values()
    )
    assert {row["plan"] for row in result.subgroup_metrics} == {"basic", "plus", "pro"}


def test_training_is_deterministic_for_a_fixed_seed(customers: pd.DataFrame) -> None:
    first = train_and_evaluate(customers, random_state=17)
    second = train_and_evaluate(customers, random_state=17)

    assert first.metrics == second.metrics
    assert first.confusion == second.confusion
    assert first.decision_threshold == second.decision_threshold
    assert first.threshold_rule == second.threshold_rule
    assert first.cross_validation == second.cross_validation
    assert first.subgroup_metrics == second.subgroup_metrics
    assert first.x_test.index.tolist() == second.x_test.index.tolist()
