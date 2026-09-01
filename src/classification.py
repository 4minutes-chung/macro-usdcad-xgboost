"""Expanding-window USD/CAD direction classification."""

from __future__ import annotations

import json

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

from src.evaluation import classifier_confusion, evaluate_classifier
from src.features import DIRECTION_FEATURE_COLS, DIRECTION_FEATURE_SETS


TARGET_CONFIG = {
    "1w": {"target": "direction_1w", "gap": 1},
    "4w": {"target": "direction_4w", "gap": 4},
}

ONE_WEEK_VALIDATION_START = "2016-12-31"
ONE_WEEK_VALIDATION_END = "2019-12-31"
ONE_WEEK_TEST_START = "2019-12-31"

LOGISTIC_C_GRID = (0.001, 0.01, 0.1, 1.0)
ELASTIC_NET_C_GRID = (0.003, 0.01, 0.03, 0.1, 0.3, 1.0)
ELASTIC_NET_L1_GRID = (0.25, 0.5, 0.75)
THRESHOLD_GRID = tuple(np.round(np.arange(0.45, 0.5501, 0.005), 3))

XGBOOST_GRID = (
    tuple(
        {
            "max_depth": depth,
            "n_estimators": estimators,
            "learning_rate": learning_rate,
            "min_child_weight": 20,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
            "reg_alpha": 0.1,
            "reg_lambda": 20.0,
        }
        for depth in (1, 2)
        for estimators, learning_rate in ((40, 0.03), (80, 0.03), (80, 0.05))
    )
    + (
        {
            "max_depth": 2,
            "n_estimators": 80,
            "learning_rate": 0.05,
            "min_child_weight": 10,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
            "reg_alpha": 0.1,
            "reg_lambda": 10.0,
        },
    )
)


def make_classifier(name: str, params: dict | None = None):
    params = params or {}
    if name == "Logistic":
        defaults = {"C": 1.0, "max_iter": 5000, "random_state": 0}
        defaults.update(params)
        return make_pipeline(
            StandardScaler(),
            LogisticRegression(**defaults),
        )
    if name == "ElasticNet":
        defaults = {
            "C": 1.0,
            "penalty": "elasticnet",
            "solver": "saga",
            "l1_ratio": 0.5,
            "max_iter": 5000,
            "random_state": 0,
        }
        defaults.update(params)
        return make_pipeline(
            StandardScaler(),
            LogisticRegression(**defaults),
        )
    if name == "XGBoost":
        defaults = {
            "n_estimators": 80,
            "max_depth": 2,
            "learning_rate": 0.05,
            "min_child_weight": 10,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
            "reg_alpha": 0.1,
            "reg_lambda": 10.0,
            "objective": "binary:logistic",
            "eval_metric": "logloss",
            "random_state": 0,
            "n_jobs": 1,
        }
        defaults.update(params)
        return XGBClassifier(**defaults)
    raise ValueError(f"unknown classifier: {name}")


def classification_models() -> dict:
    return {
        name: make_classifier(name) for name in ("Logistic", "ElasticNet", "XGBoost")
    }


def default_model_specs() -> dict:
    return {
        name: {
            "feature_set": "core",
            "feature_cols": DIRECTION_FEATURE_COLS,
            "params": {},
            "threshold": 0.5,
            "tuned": False,
        }
        for name in ("Logistic", "ElasticNet", "XGBoost")
    }


def purged_training_frame(df: pd.DataFrame, origin: pd.Timestamp, gap: int) -> pd.DataFrame:
    """Return rows before origin after removing the immediately preceding gap rows."""
    origin_position = df.index.get_loc(origin)
    train_stop = origin_position - gap
    if train_stop <= 0:
        raise ValueError("not enough history before forecast origin and gap")
    return df.iloc[:train_stop]


def expanding_window_predictions(
    df: pd.DataFrame,
    target_col: str,
    horizon: str,
    gap: int,
    test_start: str = "2019-12-31",
    model_specs: dict | None = None,
) -> pd.DataFrame:
    model_specs = model_specs or default_model_specs()
    frame = df.dropna(subset=[target_col])
    records = []
    for origin in frame.index[frame.index > pd.Timestamp(test_start)]:
        train = purged_training_frame(frame, origin, gap)
        y_train = train[target_col]
        actual = int(frame.at[origin, target_col])

        if y_train.nunique() != 2:
            raise ValueError(f"training labels at {origin.date()} do not contain both classes")

        base_probability = float(y_train.mean())
        records.append(
            {
                "date": origin,
                "horizon": horizon,
                "model": "HistoricalBaseRate",
                "actual": actual,
                "probability_up": base_probability,
                "threshold": 0.5,
                "feature_set": "benchmark",
                "tuned": False,
                "n_train": len(train),
                "train_end": train.index.max(),
                "gap": gap,
            }
        )

        for name, spec in model_specs.items():
            feature_cols = spec["feature_cols"]
            model_frame = frame.dropna(subset=feature_cols)
            model_train = purged_training_frame(model_frame, origin, gap)
            model = make_classifier(name, spec.get("params"))
            X_train = model_train[feature_cols]
            X_origin = model_frame.loc[[origin], feature_cols]
            model.fit(X_train, model_train[target_col])
            probability = float(model.predict_proba(X_origin)[0, 1])
            records.append(
                {
                    "date": origin,
                    "horizon": horizon,
                    "model": name,
                    "actual": actual,
                    "probability_up": probability,
                    "threshold": float(spec.get("threshold", 0.5)),
                    "feature_set": spec.get("feature_set", "core"),
                    "tuned": bool(spec.get("tuned", False)),
                    "n_train": len(model_train),
                    "train_end": model_train.index.max(),
                    "gap": gap,
                }
            )

    return pd.DataFrame(records)


def one_week_search_space() -> list[dict]:
    candidates = []
    for feature_set in DIRECTION_FEATURE_SETS:
        for C in LOGISTIC_C_GRID:
            candidates.append(
                {"model": "Logistic", "feature_set": feature_set, "params": {"C": C}}
            )
        for C in ELASTIC_NET_C_GRID:
            for l1_ratio in ELASTIC_NET_L1_GRID:
                candidates.append(
                    {
                        "model": "ElasticNet",
                        "feature_set": feature_set,
                        "params": {"C": C, "l1_ratio": l1_ratio},
                    }
                )
        for params in XGBOOST_GRID:
            candidates.append(
                {"model": "XGBoost", "feature_set": feature_set, "params": params}
            )
    return candidates


def validation_probabilities(
    df: pd.DataFrame,
    model_name: str,
    feature_cols: list[str],
    params: dict,
    validation_start: str = ONE_WEEK_VALIDATION_START,
    validation_end: str = ONE_WEEK_VALIDATION_END,
    gap: int = 1,
) -> pd.DataFrame:
    frame = df.dropna(subset=feature_cols + ["direction_1w"])
    origins = frame.index[
        (frame.index > pd.Timestamp(validation_start))
        & (frame.index <= pd.Timestamp(validation_end))
    ]
    records = []
    for origin in origins:
        train = purged_training_frame(frame, origin, gap)
        model = make_classifier(model_name, params)
        model.fit(train[feature_cols], train["direction_1w"])
        probability = float(model.predict_proba(frame.loc[[origin], feature_cols])[0, 1])
        records.append(
            {
                "date": origin,
                "actual": int(frame.at[origin, "direction_1w"]),
                "probability_up": probability,
                "n_train": len(train),
                "train_end": train.index.max(),
                "gap": gap,
            }
        )
    if not records:
        raise ValueError("validation window contains no forecast origins")
    return pd.DataFrame(records)


def select_threshold(y_true: np.ndarray, probability: np.ndarray) -> float:
    scored = []
    for threshold in THRESHOLD_GRID:
        metric = evaluate_classifier(
            y_true,
            probability,
            label="threshold_search",
            horizon="1w",
            threshold=threshold,
        )
        scored.append((metric["balanced_accuracy"], abs(threshold - 0.5), threshold))
    return float(sorted(scored, key=lambda row: (-row[0], row[1], row[2]))[0][2])


def tune_one_week_models(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    records = []
    for candidate_id, candidate in enumerate(one_week_search_space(), start=1):
        feature_set = candidate["feature_set"]
        predictions = validation_probabilities(
            df,
            model_name=candidate["model"],
            feature_cols=DIRECTION_FEATURE_SETS[feature_set],
            params=candidate["params"],
        )
        y_true = predictions["actual"].to_numpy(dtype=int)
        probability = predictions["probability_up"].to_numpy(dtype=float)
        threshold = select_threshold(y_true, probability)
        metrics = evaluate_classifier(
            y_true,
            probability,
            label=candidate["model"],
            horizon="1w_validation",
            threshold=threshold,
        )
        records.append(
            {
                "candidate_id": candidate_id,
                "model": candidate["model"],
                "feature_set": feature_set,
                "params": json.dumps(candidate["params"], sort_keys=True),
                "validation_start": predictions["date"].min(),
                "validation_end": predictions["date"].max(),
                "n_validation": len(predictions),
                "threshold": threshold,
                "balanced_accuracy": metrics["balanced_accuracy"],
                "brier_score": metrics["brier_score"],
                "log_loss": metrics["log_loss"],
                "probability_std": float(np.std(probability, ddof=1)),
            }
        )

    search = pd.DataFrame(records)
    selected = (
        search.sort_values(["model", "brier_score", "log_loss", "candidate_id"])
        .groupby("model", sort=False)
        .head(1)
    )
    search["selected"] = search["candidate_id"].isin(selected["candidate_id"])

    specs = {}
    for row in selected.itertuples(index=False):
        specs[row.model] = {
            "feature_set": row.feature_set,
            "feature_cols": DIRECTION_FEATURE_SETS[row.feature_set],
            "params": json.loads(row.params),
            "threshold": float(row.threshold),
            "tuned": True,
        }
    return search.sort_values(["model", "brier_score"]).reset_index(drop=True), specs


def summarize_predictions(predictions: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    metrics = []
    confusion_tables = []
    for (horizon, model), group in predictions.groupby(["horizon", "model"], sort=False):
        y_true = group["actual"].to_numpy(dtype=int)
        probability = group["probability_up"].to_numpy(dtype=float)
        threshold = float(group["threshold"].iloc[0]) if "threshold" in group else 0.5
        metrics.append(
            evaluate_classifier(y_true, probability, model, horizon, threshold=threshold)
        )
        confusion_tables.append(
            classifier_confusion(y_true, probability, model, horizon, threshold=threshold)
        )

    return pd.DataFrame(metrics), pd.concat(confusion_tables, ignore_index=True)


def summarize_predictions_by_year(predictions: pd.DataFrame) -> pd.DataFrame:
    annual = predictions.copy()
    annual["year"] = pd.to_datetime(annual["date"]).dt.year
    records = []
    for (year, model), group in annual.groupby(["year", "model"], sort=True):
        threshold = float(group["threshold"].iloc[0])
        metrics = evaluate_classifier(
            group["actual"].to_numpy(dtype=int),
            group["probability_up"].to_numpy(dtype=float),
            model,
            horizon="1w",
            threshold=threshold,
        )
        records.append({"year": year, **metrics})
    return pd.DataFrame(records)
