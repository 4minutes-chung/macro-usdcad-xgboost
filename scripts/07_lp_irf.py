"""Stage 4 (optional): Local Projection IRF for USD/CAD response to shocks."""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt
import pandas as pd

from src.lp import ar1_innovations, lp_irf, plot_irf
from src.plots import save


def main() -> None:
    Path("outputs/figures").mkdir(parents=True, exist_ok=True)
    Path("outputs/tables").mkdir(parents=True, exist_ok=True)

    feats = pd.read_parquet("data/processed/features.parquet")

    # Construct shocks as AR(1) innovations on each driver
    shock_wti = ar1_innovations(feats["r_wti"])
    shock_spread = ar1_innovations(feats["spread_2y"])
    shock_vix = ar1_innovations(feats["d_vix"])

    # Controls: lagged dependent variable and contemporaneous other drivers
    target = feats["r_usdcad"]
    controls = feats[["r_usdcad", "vol_usdcad_4w"]].shift(1)

    irf_wti = lp_irf(target, shock_wti, horizons=12, controls=controls)
    irf_spread = lp_irf(target, shock_spread, horizons=12, controls=controls)
    irf_vix = lp_irf(target, shock_vix, horizons=12, controls=controls)

    save(plot_irf(irf_wti, "USD/CAD response to WTI return shock"), "09_irf_wti")
    save(plot_irf(irf_spread, "USD/CAD response to CA-US 2Y spread shock"), "10_irf_spread2y")
    save(plot_irf(irf_vix, "USD/CAD response to VIX change shock"), "11_irf_vix")

    irf_wti.to_csv("outputs/tables/irf_wti.csv", index=False)
    irf_spread.to_csv("outputs/tables/irf_spread2y.csv", index=False)
    irf_vix.to_csv("outputs/tables/irf_vix.csv", index=False)

    print("Stage 4 IRFs saved.")


if __name__ == "__main__":
    main()
