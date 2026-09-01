"""Focused 1-week and 4-week USD/CAD direction classification."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd

from src.classification import (
    TARGET_CONFIG,
    expanding_window_predictions,
    summarize_predictions,
)


def main() -> None:
    Path("outputs/tables").mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet("data/processed/direction_features.parquet")

    prediction_tables = []
    for horizon, config in TARGET_CONFIG.items():
        print(f"Running {horizon} direction classification with gap={config['gap']}...")
        prediction_tables.append(
            expanding_window_predictions(
                df,
                target_col=config["target"],
                horizon=horizon,
                gap=config["gap"],
            )
        )

    predictions = pd.concat(prediction_tables, ignore_index=True)
    metrics, confusion = summarize_predictions(predictions)
    metrics = metrics.sort_values(["horizon", "log_loss"]).reset_index(drop=True)

    predictions.to_csv("outputs/tables/direction_predictions.csv", index=False)
    metrics.to_csv("outputs/tables/direction_metrics.csv", index=False)
    confusion.to_csv("outputs/tables/direction_confusion_matrix.csv", index=False)

    print("\nClassification metrics:")
    print(metrics.round(5).to_string(index=False))


if __name__ == "__main__":
    main()
