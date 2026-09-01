"""Phase 3: EDA and required figures."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


import pandas as pd

from src.plots import corr_heatmap, line_series, normalized_overlay, rolling_corr, save


def main() -> None:
    Path("outputs/figures").mkdir(parents=True, exist_ok=True)
    Path("outputs/tables").mkdir(parents=True, exist_ok=True)

    weekly = pd.read_parquet("data/raw/weekly.parquet")
    feats = pd.read_parquet("data/processed/features.parquet")

    save(line_series(weekly[["usdcad"]], "USD/CAD weekly", "CAD per USD"), "01_usdcad")
    save(line_series(weekly[["wti"]], "WTI weekly", "USD/barrel"), "02_wti")
    save(normalized_overlay(weekly["usdcad"], weekly["wti"], "USD/CAD vs WTI (normalized to 100)"),
         "03_usdcad_vs_wti")
    save(rolling_corr(feats["r_usdcad"], feats["r_wti"], 26,
                      "Rolling correlation: USD/CAD return vs WTI return"),
         "04_rolling_corr_usdcad_wti")
    save(line_series(feats[["spread_2y"]], "CA-US 2Y yield spread", "percentage points"),
         "05_spread_2y")
    save(line_series(feats[["vix"]], "VIX weekly", "VIX level"), "06_vix")
    save(corr_heatmap(feats.drop(columns=["y_1w"]), "Feature correlation matrix"),
         "07_corr_heatmap")

    summary = feats.describe().T.round(4)
    summary.to_csv("outputs/tables/summary_stats.csv")
    feats.corr().round(3).to_csv("outputs/tables/correlation_table.csv")

    print("All Phase 3 figures and tables saved.")


if __name__ == "__main__":
    main()
