"""Interpretation tooling: permutation importance, Ridge coefficient reporting,
regime-conditional evaluation.

Added in v2 after ChatGPT noted permutation importance was missing.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance


def permutation_importance_table(
    model,
    X: pd.DataFrame,
    y: pd.Series,
    n_repeats: int = 30,
    random_state: int = 0,
    scoring: str = "neg_root_mean_squared_error",
) -> pd.DataFrame:
    """Permutation importance: shuffle each feature, measure performance drop.

    Strictly better than gain-based importance because it accounts for the
    real predictive contribution rather than how often a feature was used.
    """
    r = permutation_importance(
        model, X, y, n_repeats=n_repeats, random_state=random_state, scoring=scoring
    )
    return (
        pd.DataFrame(
            {
                "feature": X.columns,
                "importance_mean": r.importances_mean,
                "importance_std": r.importances_std,
            }
        )
        .set_index("feature")
        .sort_values("importance_mean", ascending=False)
    )


def ridge_coefficient_report(ridge_model, feature_names: list[str], scaler=None) -> pd.DataFrame:
    """Report Ridge coefficients with prior-sign expectations.

    Use this as interpretation tool, not just metric. The sign of each coefficient
    tells you which direction each factor pushes USD/CAD.

    Theoretical priors (sign of expected coefficient on 1-week-ahead USD/CAD return):
    - r_usdcad lag: ambiguous (momentum vs reversal)
    - r_wti: negative (oil up -> CAD up -> USD/CAD down)
    - vol_wti: ambiguous
    - spread_2y (CA - US): negative under capital-flow story, positive under UIP
    - spread_10y: same as 2y
    - d_spread_2y: same direction as level
    - vix: positive (risk-off -> USD strength)
    - d_vix: positive
    - r_equity: ambiguous (typically risk-on -> CAD up -> USD/CAD down, so negative)
    """
    coefs = ridge_model.coef_
    priors = {
        "r_usdcad": "ambiguous (momentum vs reversal)",
        "r_wti": "negative",
        "vol_usdcad_4w": "ambiguous",
        "vol_usdcad_8w": "ambiguous",
        "vol_wti_4w": "ambiguous",
        "vol_wti_8w": "ambiguous",
        "spread_2y": "negative under capital flow; positive under UIP",
        "spread_10y": "negative under capital flow; positive under UIP",
        "d_spread_2y": "same direction as level",
        "vix": "positive (risk-off -> USD)",
        "d_vix": "positive",
        "r_equity": "negative (risk-on -> CAD up)",
    }
    df = pd.DataFrame({
        "feature": feature_names,
        "coefficient": coefs,
        "prior_sign": [priors.get(f, "unknown") for f in feature_names],
    }).set_index("feature")
    df["sign_matches_prior"] = df.apply(_check_sign_match, axis=1)
    return df.sort_values("coefficient", key=abs, ascending=False)


def _check_sign_match(row) -> str:
    coef = row["coefficient"]
    prior = row["prior_sign"]
    if "ambiguous" in prior or "unknown" in prior:
        return "n/a"
    if "negative" in prior and "positive" not in prior:
        return "yes" if coef < 0 else "no"
    if "positive" in prior and "negative" not in prior:
        return "yes" if coef > 0 else "no"
    return "mixed prior"


def regime_split(df: pd.DataFrame, column: str, quantile: float = 0.5) -> tuple[pd.Series, pd.Series]:
    """Return boolean masks for high vs low regimes based on a quantile cut."""
    cutoff = df[column].quantile(quantile)
    return df[column] > cutoff, df[column] <= cutoff
