"""Phase 2: build features and target."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


import pandas as pd

from src.features import build_direction_features, build_features


def main() -> None:
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    weekly = pd.read_parquet("data/raw/weekly.parquet")
    feats = build_features(weekly)
    direction_feats = build_direction_features(weekly)
    feats.to_parquet("data/processed/features.parquet")
    direction_feats.to_parquet("data/processed/direction_features.parquet")
    print(f"features shape: {feats.shape}")
    print(f"date range: {feats.index.min().date()} to {feats.index.max().date()}")
    print("\nDescribe:")
    print(feats.describe().T[["count", "mean", "std", "min", "max"]].round(4))
    print(f"\ndirection features shape: {direction_feats.shape}")
    print(
        f"direction date range: {direction_feats.index.min().date()} "
        f"to {direction_feats.index.max().date()}"
    )


if __name__ == "__main__":
    main()
