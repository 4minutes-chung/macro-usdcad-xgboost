"""Phase 6: XGBoost three-pass tuning.

Pass 1: Manual exploratory grid. Understand parameter sensitivity.
Pass 2: Random search. Broader.
Pass 3: Optuna Bayesian search. Final.

Do not skip to Pass 3. The point is to learn what each parameter does.
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))



import numpy as np
import optuna
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import TimeSeriesSplit

from src.evaluation import benchmark_table, evaluate
from src.features import train_val_test_split


def cv_score(params: dict, X: pd.DataFrame, y: pd.Series, n_splits: int = 5) -> float:
    tscv = TimeSeriesSplit(n_splits=n_splits)
    rmses = []
    for tr, va in tscv.split(X):
        dtrain = xgb.DMatrix(X.iloc[tr], label=y.iloc[tr])
        dval = xgb.DMatrix(X.iloc[va], label=y.iloc[va])
        booster = xgb.train(
            params, dtrain, num_boost_round=2000,
            evals=[(dval, "val")], early_stopping_rounds=50, verbose_eval=False,
        )
        pred = booster.predict(dval)
        rmses.append(np.sqrt(np.mean((y.iloc[va].values - pred) ** 2)))
    return float(np.mean(rmses))


# Pass 1: manual grid
def pass1_manual(X: pd.DataFrame, y: pd.Series) -> list[dict]:
    grid = [
        {"max_depth": d, "eta": lr, "subsample": 0.8, "colsample_bytree": 0.8,
         "reg_lambda": 1.0, "objective": "reg:squarederror", "verbosity": 0}
        for d in (2, 3, 4) for lr in (0.03, 0.05, 0.1)
    ]
    records = [{**p, "cv_rmse": cv_score(p, X, y)} for p in grid]
    return records


# Pass 2: random search
def pass2_random(X: pd.DataFrame, y: pd.Series, n_iter: int = 30, seed: int = 0) -> list[dict]:
    rng = np.random.default_rng(seed)
    records = []
    for _ in range(n_iter):
        p = {
            "max_depth": int(rng.integers(2, 6)),
            "eta": float(10 ** rng.uniform(-2, -0.7)),
            "subsample": float(rng.uniform(0.6, 1.0)),
            "colsample_bytree": float(rng.uniform(0.6, 1.0)),
            "reg_lambda": float(10 ** rng.uniform(-1, 1)),
            "min_child_weight": int(rng.integers(1, 10)),
            "gamma": float(rng.uniform(0, 1)),
            "objective": "reg:squarederror",
            "verbosity": 0,
        }
        records.append({**p, "cv_rmse": cv_score(p, X, y)})
    return records


# Pass 3: Optuna
def pass3_optuna(X: pd.DataFrame, y: pd.Series, n_trials: int = 50) -> tuple[dict, optuna.Study]:
    def objective(trial: optuna.Trial) -> float:
        p = {
            "max_depth": trial.suggest_int("max_depth", 2, 6),
            "eta": trial.suggest_float("eta", 0.01, 0.2, log=True),
            "subsample": trial.suggest_float("subsample", 0.6, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
            "reg_lambda": trial.suggest_float("reg_lambda", 0.1, 10.0, log=True),
            "min_child_weight": trial.suggest_int("min_child_weight", 1, 10),
            "gamma": trial.suggest_float("gamma", 0.0, 1.0),
            "objective": "reg:squarederror",
            "verbosity": 0,
        }
        return cv_score(p, X, y)

    study = optuna.create_study(direction="minimize", sampler=optuna.samplers.TPESampler(seed=0))
    study.optimize(objective, n_trials=n_trials, show_progress_bar=False)
    return study.best_params, study


def train_final(params: dict, X_train: pd.DataFrame, y_train: pd.Series,
                X_val: pd.DataFrame, y_val: pd.Series,
                X_test: pd.DataFrame) -> tuple[xgb.Booster, np.ndarray]:
    """Train on train set with early stopping on val. Predict on test. No leakage."""
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dval = xgb.DMatrix(X_val, label=y_val)
    dtest = xgb.DMatrix(X_test)
    booster = xgb.train(
        {**params, "objective": "reg:squarederror", "verbosity": 0},
        dtrain, num_boost_round=2000,
        evals=[(dval, "val")], early_stopping_rounds=50, verbose_eval=False,
    )
    return booster, booster.predict(dtest)


def main() -> None:
    Path("outputs/tables").mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet("data/processed/features.parquet")
    train, val, test = train_val_test_split(df)
    X_train, y_train = train.drop(columns=["y_1w"]), train["y_1w"]
    X_val, y_val = val.drop(columns=["y_1w"]), val["y_1w"]
    X_test, y_test = test.drop(columns=["y_1w"]), test["y_1w"]

    print("Pass 1: manual grid")
    p1 = pass1_manual(X_train, y_train)
    pd.DataFrame(p1).to_csv("outputs/tables/xgb_pass1_manual.csv", index=False)

    print("Pass 2: random search")
    p2 = pass2_random(X_train, y_train, n_iter=30)
    pd.DataFrame(p2).sort_values("cv_rmse").to_csv("outputs/tables/xgb_pass2_random.csv", index=False)

    print("Pass 3: Optuna")
    best_params, study = pass3_optuna(X_train, y_train, n_trials=50)
    print(f"Best Optuna params: {best_params}")
    pd.DataFrame([{**t.params, "cv_rmse": t.value} for t in study.trials]).to_csv(
        "outputs/tables/xgb_pass3_optuna.csv", index=False
    )

    booster, preds = train_final(best_params, X_train, y_train, X_val, y_val, X_test)
    booster.save_model("outputs/xgb_final.json")
    final_eval = evaluate(y_test.values, preds, "XGBoost")
    benchmark_table([final_eval]).to_csv("outputs/tables/xgb_final_eval.csv")
    print(benchmark_table([final_eval]))


if __name__ == "__main__":
    main()
