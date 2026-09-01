"""Phase 4: benchmark models. Random walk, AR(1), Ridge."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.ar_model import AutoReg

from src.evaluation import benchmark_table, evaluate
from src.features import train_val_test_split
from src.interpretation import ridge_coefficient_report


def random_walk_predict(y_test: pd.Series) -> np.ndarray:
    """Random walk in the exchange-rate level implies zero expected return."""
    return np.zeros(len(y_test))


def ar1_walk_forward(df: pd.DataFrame, test_index: pd.Index) -> np.ndarray:
    """Forecast r_usdcad_{t+1} from returns observed through date t."""
    preds = []
    for origin in test_index:
        history = df.loc[df.index <= origin, "r_usdcad"].dropna().values
        model = AutoReg(history, lags=1, old_names=False).fit()
        preds.append(model.predict(start=len(history), end=len(history)).item())
    return np.array(preds)


def ridge_walk_forward(
    df: pd.DataFrame, test_index: pd.Index, feature_cols: list[str], alpha: float = 1.0
) -> np.ndarray:
    """Expanding-window Ridge forecast. At origin t, train only on rows before t."""
    preds = []
    for origin in test_index:
        train_df = df.loc[df.index < origin]
        X_train, y_train = train_df[feature_cols], train_df["y_1w"]
        X_origin = df.loc[[origin], feature_cols]
        scaler = StandardScaler().fit(X_train)
        model = Ridge(alpha=alpha).fit(scaler.transform(X_train), y_train)
        preds.append(model.predict(scaler.transform(X_origin)).item())
    return np.array(preds)


def fit_ridge_for_coefficients(
    df: pd.DataFrame, feature_cols: list[str], alpha: float = 1.0
) -> tuple[Ridge, StandardScaler]:
    scaler = StandardScaler().fit(df[feature_cols])
    model = Ridge(alpha=alpha).fit(scaler.transform(df[feature_cols]), df["y_1w"])
    return model, scaler


def main() -> None:
    Path("outputs/tables").mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet("data/processed/features.parquet")
    train, val, test = train_val_test_split(df)
    train_val = pd.concat([train, val])
    feature_cols = [c for c in df.columns if c != "y_1w"]

    y_test = test["y_1w"]

    print(f"train rows: {len(train)} | validation rows: {len(val)} | test rows: {len(test)}")
    print(f"first test origin: {test.index.min().date()} | last test origin: {test.index.max().date()}")

    preds_rw = random_walk_predict(y_test)
    preds_ar1 = ar1_walk_forward(df, test.index)
    preds_ridge = ridge_walk_forward(df, test.index, feature_cols)

    results = [
        evaluate(y_test.values, preds_rw, "RandomWalk"),
        evaluate(y_test.values, preds_ar1, "AR(1)"),
        evaluate(y_test.values, preds_ridge, "Ridge"),
    ]

    table = benchmark_table(results)
    print(table)
    table.to_csv("outputs/tables/benchmark_table.csv")

    prediction_table = pd.DataFrame(
        {
            "y_1w": y_test,
            "RandomWalk": preds_rw,
            "AR(1)": preds_ar1,
            "Ridge": preds_ridge,
        },
        index=test.index,
    )
    prediction_table.to_csv("outputs/tables/benchmark_predictions.csv")

    ridge_model, _ = fit_ridge_for_coefficients(train_val, feature_cols)
    ridge_coefs = ridge_coefficient_report(ridge_model, feature_cols)
    ridge_coefs.to_csv("outputs/tables/ridge_coefficients.csv")
    print("\nRidge coefficients estimated on train+validation window:")
    print(ridge_coefs)


if __name__ == "__main__":
    main()
