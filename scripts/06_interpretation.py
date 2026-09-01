"""Stage 3c: Interpretation. Feature importance (gain/weight/cover),
permutation importance, SHAP, regime tables, and economic readout.

Adds permutation importance after ChatGPT critique.
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
import xgboost as xgb
from sklearn.base import BaseEstimator, RegressorMixin

from src.evaluation import benchmark_table, evaluate
from src.features import train_val_test_split
from src.interpretation import permutation_importance_table, regime_split
from src.plots import save


class _BoosterWrapper(BaseEstimator, RegressorMixin):
    """Wrap xgb.Booster as a sklearn-style estimator so permutation_importance works."""

    def __init__(self, booster: xgb.Booster):
        self.booster = booster
        self.feature_names_in_ = booster.feature_names

    def fit(self, X, y):
        return self

    def predict(self, X):
        if isinstance(X, pd.DataFrame):
            return self.booster.predict(xgb.DMatrix(X))
        return self.booster.predict(xgb.DMatrix(pd.DataFrame(X, columns=self.feature_names_in_)))


def importance_table(booster: xgb.Booster, feature_names: list[str]) -> pd.DataFrame:
    scores = {
        kind: booster.get_score(importance_type=kind)
        for kind in ("gain", "weight", "cover")
    }
    return (
        pd.DataFrame(index=feature_names)
        .assign(
            gain=lambda x: [scores["gain"].get(f, 0.0) for f in x.index],
            weight=lambda x: [scores["weight"].get(f, 0.0) for f in x.index],
            cover=lambda x: [scores["cover"].get(f, 0.0) for f in x.index],
        )
        .sort_values("gain", ascending=False)
    )


def regime_eval(y_true: pd.Series, y_pred: np.ndarray, mask: pd.Series, label: str) -> dict:
    if int(mask.sum()) == 0:
        return {
            "model": label,
            "rmse": np.nan,
            "mae": np.nan,
            "oos_r2_vs_rw": np.nan,
            "dir_acc": np.nan,
            "bal_dir_acc": np.nan,
        }
    return evaluate(y_true[mask].values, y_pred[mask.values], label)


def main() -> None:
    Path("outputs/tables").mkdir(parents=True, exist_ok=True)
    Path("outputs/figures").mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet("data/processed/features.parquet")
    train, val, test = train_val_test_split(df)
    X_val, y_val = val.drop(columns=["y_1w"]), val["y_1w"]
    X_test, y_test = test.drop(columns=["y_1w"]), test["y_1w"]

    booster = xgb.Booster()
    booster.load_model("outputs/xgb_final.json")
    val_preds = booster.predict(xgb.DMatrix(X_val))
    preds = booster.predict(xgb.DMatrix(X_test))

    # Feature importance: gain, weight, cover (XGBoost native)
    imp = importance_table(booster, list(X_test.columns))
    imp.to_csv("outputs/tables/feature_importance_native.csv")
    print("Native feature importance (gain/weight/cover):")
    print(imp)

    # Permutation importance on test set
    wrapped = _BoosterWrapper(booster)
    perm = permutation_importance_table(wrapped, X_test, y_test, n_repeats=30, random_state=0)
    perm.to_csv("outputs/tables/feature_importance_permutation.csv")
    print("\nPermutation importance:")
    print(perm)

    # SHAP
    explainer = shap.TreeExplainer(booster)
    shap_values = explainer.shap_values(X_test)
    shap.summary_plot(shap_values, X_test, show=False)
    save(plt.gcf(), "08_shap_summary")
    plt.close()

    # Regime tables: high vs low VIX, pre/post-2020 diagnostic, high vs low oil vol.
    # Test starts in 2020, so pre-2020 can only be shown as validation-window diagnostic.
    high_vix, low_vix = regime_split(X_test, "vix")
    high_oilvol, low_oilvol = regime_split(X_test, "vol_wti_4w")
    val_pre_2020 = X_val.index < "2020-01-01"
    test_post_2020 = X_test.index >= "2020-01-01"

    regimes = [
        regime_eval(y_test, preds, high_vix, "XGB | high VIX"),
        regime_eval(y_test, preds, low_vix, "XGB | low VIX"),
        regime_eval(y_val, val_preds, pd.Series(val_pre_2020, index=X_val.index),
                    "XGB | pre-2020 validation diagnostic"),
        regime_eval(y_test, preds, pd.Series(test_post_2020, index=X_test.index),
                    "XGB | post-2020 test"),
        regime_eval(y_test, preds, high_oilvol, "XGB | high oil vol"),
        regime_eval(y_test, preds, low_oilvol, "XGB | low oil vol"),
    ]
    regime_table = benchmark_table(regimes)
    print("\nRegime-conditional evaluation:")
    print(regime_table)
    regime_table.to_csv("outputs/tables/regime_table.csv")


if __name__ == "__main__":
    main()
