"""Local Projection for impulse response functions (Stage 4, optional).

Jorda (2005). At each horizon h, regress y_{t+h} on shock_t (plus controls).
Newey-West HAC standard errors. Plot IRF with confidence bands.

This is a simple internal-instrument implementation: shocks are AR(1)
innovations from each driver. Identification is descriptive, not causal.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm


def ar1_innovations(s: pd.Series) -> pd.Series:
    """Residuals from AR(1) regression. Treated as shock proxy."""
    s = s.dropna()
    y = s.iloc[1:]
    x = sm.add_constant(s.iloc[:-1].values)
    model = sm.OLS(y.values, x).fit()
    resid = pd.Series(model.resid, index=y.index, name=f"{s.name}_shock")
    return resid


def lp_irf(
    y: pd.Series,
    shock: pd.Series,
    horizons: int = 12,
    controls: pd.DataFrame | None = None,
    nw_lags: int = 4,
) -> pd.DataFrame:
    """Local projection IRF.

    For h in [0, horizons]:
        y_{t+h} = alpha_h + beta_h * shock_t + gamma * controls_t + eps

    Returns DataFrame with columns: horizon, beta, se, ci_lo, ci_hi.
    Newey-West HAC SEs with `nw_lags` lags to handle serial correlation.
    """
    y, shock = y.align(shock, join="inner")
    if controls is not None:
        shock_controls = pd.concat([shock, controls.loc[shock.index]], axis=1).dropna()
    else:
        shock_controls = shock.to_frame()
    out = []
    for h in range(horizons + 1):
        y_future = y.shift(-h)
        df = pd.concat([y_future.rename("y"), shock_controls], axis=1).dropna()
        if len(df) < 30:
            break
        X = sm.add_constant(df.drop(columns=["y"]))
        model = sm.OLS(df["y"], X).fit(cov_type="HAC", cov_kwds={"maxlags": nw_lags})
        # Beta on the shock variable (first non-const column)
        shock_col = shock_controls.columns[0]
        beta = model.params[shock_col]
        se = model.bse[shock_col]
        out.append({
            "horizon": h,
            "beta": beta,
            "se": se,
            "ci_lo": beta - 1.96 * se,
            "ci_hi": beta + 1.96 * se,
        })
    return pd.DataFrame(out)


def plot_irf(irf: pd.DataFrame, title: str, ylabel: str = "Cumulative response"):
    """Plot IRF with 95% confidence band. Returns matplotlib figure."""
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(irf["horizon"], irf["beta"], lw=2, label="IRF")
    ax.fill_between(irf["horizon"], irf["ci_lo"], irf["ci_hi"], alpha=0.2, label="95% CI (Newey-West)")
    ax.axhline(0, color="k", lw=0.8)
    ax.set_xlabel("Horizon (weeks)")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    return fig
