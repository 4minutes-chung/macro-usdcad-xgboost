"""Project sanity checks before modeling.

These are economics checks, not software ceremony:
- sample must respect the 2026-04-30 data cap;
- features must stay inside the v1 feature budget;
- the target must be exactly next week's USD/CAD log return.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import pandas as pd

from src.data import DATA_END
from src.features import (
    DIRECTION_EXTENDED_FEATURE_COLS,
    DIRECTION_FEATURE_COLS,
    forward_log_return,
    log_return,
)


def main() -> None:
    weekly = pd.read_parquet("data/raw/weekly.parquet")
    features = pd.read_parquet("data/processed/features.parquet")
    direction_features = pd.read_parquet("data/processed/direction_features.parquet")

    max_weekly_date = weekly.index.max()
    max_feature_date = features.index.max()
    cap = pd.Timestamp(DATA_END)
    max_direction_date = direction_features.index.max()
    if max_weekly_date > cap or max_feature_date > cap or max_direction_date > cap:
        raise AssertionError(
            "data cap violated: "
            f"weekly max={max_weekly_date}, feature max={max_feature_date}, "
            f"direction max={max_direction_date}, cap={cap}"
        )

    feature_cols = [c for c in features.columns if c != "y_1w"]
    if len(feature_cols) > 15:
        raise AssertionError(f"feature budget violated: {len(feature_cols)} features > 15")

    r_usdcad = log_return(weekly["usdcad"])
    expected_target = r_usdcad.shift(-1).reindex(features.index)
    max_error = float(np.nanmax(np.abs(features["y_1w"] - expected_target)))
    if max_error > 1e-12:
        raise AssertionError(f"target alignment failed: max abs error={max_error}")

    observed_direction_features = [
        column
        for column in direction_features.columns
        if column in DIRECTION_EXTENDED_FEATURE_COLS
    ]
    if observed_direction_features != DIRECTION_EXTENDED_FEATURE_COLS:
        raise AssertionError(
            f"direction feature set mismatch: {observed_direction_features}"
        )
    if len(DIRECTION_EXTENDED_FEATURE_COLS) > 15:
        raise AssertionError(
            "direction feature budget violated: "
            f"{len(DIRECTION_EXTENDED_FEATURE_COLS)} features > 15"
        )

    direction_errors = {}
    for horizon in (1, 4):
        target_col = f"y_{horizon}w"
        direction_col = f"direction_{horizon}w"
        horizon_features = direction_features.dropna(
            subset=[target_col, direction_col]
        )
        expected_return = forward_log_return(weekly["usdcad"], horizon).reindex(
            horizon_features.index
        )
        target_error = float(
            np.nanmax(np.abs(horizon_features[target_col] - expected_return))
        )
        expected_direction = (expected_return > 0).astype("int8")
        observed_direction = horizon_features[direction_col].astype("int8")
        direction_matches = observed_direction.eq(expected_direction).all()
        if target_error > 1e-12 or not direction_matches:
            raise AssertionError(
                f"{horizon}-week direction alignment failed: "
                f"target error={target_error}, direction matches={direction_matches}"
            )
        direction_errors[horizon] = target_error

    print("Project checks passed.")
    print(f"weekly date range: {weekly.index.min().date()} to {weekly.index.max().date()}")
    print(f"feature date range: {features.index.min().date()} to {features.index.max().date()}")
    print(f"feature count: {len(feature_cols)}")
    print(f"target alignment max abs error: {max_error:.3g}")
    print(f"direction core feature count: {len(DIRECTION_FEATURE_COLS)}")
    print(f"direction extended feature count: {len(DIRECTION_EXTENDED_FEATURE_COLS)}")
    for horizon, error in direction_errors.items():
        print(f"{horizon}-week direction target max abs error: {error:.3g}")


if __name__ == "__main__":
    main()
