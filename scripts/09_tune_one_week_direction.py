"""Tune and evaluate the primary 1-week USD/CAD direction models."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd

from src.classification import (
    ONE_WEEK_TEST_START,
    ONE_WEEK_VALIDATION_END,
    expanding_window_predictions,
    summarize_predictions,
    summarize_predictions_by_year,
    tune_one_week_models,
)
from src.evaluation import paired_classifier_loss_tests


def main() -> None:
    output_dir = Path("outputs/tables")
    output_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet("data/processed/direction_features.parquet")

    print("Tuning on 2017-2019 expanding-window validation forecasts...")
    search, model_specs = tune_one_week_models(df)
    selected = search.loc[search["selected"]].copy()
    if selected["validation_end"].max() > pd.Timestamp(ONE_WEEK_VALIDATION_END):
        raise AssertionError("tuning used observations after the validation period")

    print("Checking 2010-start validation sensitivity...")
    sensitivity_search, _ = tune_one_week_models(df.loc["2010-01-01":])
    sensitivity_selected = sensitivity_search.loc[sensitivity_search["selected"]].copy()

    print("Running locked 2020-2026 test forecasts...")
    predictions = expanding_window_predictions(
        df,
        target_col="direction_1w",
        horizon="1w",
        gap=1,
        test_start=ONE_WEEK_TEST_START,
        model_specs=model_specs,
    )
    metrics, confusion = summarize_predictions(predictions)
    annual = summarize_predictions_by_year(predictions)
    loss_tests = paired_classifier_loss_tests(predictions, hac_lags=4)
    metrics = metrics.sort_values("log_loss").reset_index(drop=True)
    conventional_predictions = predictions.copy()
    conventional_predictions["threshold"] = 0.5
    conventional_metrics, _ = summarize_predictions(conventional_predictions)
    conventional_metrics = conventional_metrics.sort_values("log_loss").reset_index(
        drop=True
    )

    search.to_csv(output_dir / "direction_1w_tuning_search.csv", index=False)
    selected.to_csv(output_dir / "direction_1w_tuned_specs.csv", index=False)
    sensitivity_selected.to_csv(
        output_dir / "direction_1w_tuned_specs_start_2010.csv", index=False
    )
    predictions.to_csv(output_dir / "direction_1w_tuned_predictions.csv", index=False)
    metrics.to_csv(output_dir / "direction_1w_tuned_metrics.csv", index=False)
    locked_thresholds = metrics.copy()
    locked_thresholds["evaluation"] = "validation_locked_threshold"
    conventional_metrics["evaluation"] = "conventional_0.50_threshold"
    pd.concat([locked_thresholds, conventional_metrics], ignore_index=True).to_csv(
        output_dir / "direction_1w_threshold_sensitivity.csv", index=False
    )
    confusion.to_csv(output_dir / "direction_1w_tuned_confusion_matrix.csv", index=False)
    annual.to_csv(output_dir / "direction_1w_tuned_annual_metrics.csv", index=False)
    loss_tests.to_csv(output_dir / "direction_1w_tuned_loss_tests.csv", index=False)

    original_path = output_dir / "direction_metrics.csv"
    if original_path.exists():
        original = pd.read_csv(original_path)
        original = original.loc[original["horizon"].eq("1w")].copy()
        if "threshold" not in original:
            original["threshold"] = 0.5
        original["run"] = "original_fixed"
        tuned = metrics.copy()
        tuned["run"] = "tuned"
        pd.concat([original, tuned], ignore_index=True).to_csv(
            output_dir / "direction_1w_model_comparison.csv", index=False
        )

    original_predictions_path = output_dir / "direction_predictions.csv"
    if original_predictions_path.exists():
        original_predictions = pd.read_csv(original_predictions_path)
        original_predictions = original_predictions.loc[
            original_predictions["horizon"].eq("1w")
        ]
        paired_classifier_loss_tests(original_predictions, hac_lags=4).to_csv(
            output_dir / "direction_1w_fixed_loss_tests.csv", index=False
        )

    print("\nSelected validation configurations:")
    print(
        selected[
            [
                "model",
                "feature_set",
                "params",
                "threshold",
                "balanced_accuracy",
                "brier_score",
                "log_loss",
            ]
        ].to_string(index=False)
    )
    print("\nLocked test metrics:")
    print(metrics.round(5).to_string(index=False))


if __name__ == "__main__":
    main()
