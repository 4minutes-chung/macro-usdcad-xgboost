"""Evaluation metrics for FX return forecasts."""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.metrics import (
    balanced_accuracy_score,
    brier_score_loss,
    confusion_matrix,
    log_loss,
    mean_absolute_error,
    mean_squared_error,
)


def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))


def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(mean_absolute_error(y_true, y_pred))


def oos_r2_vs_rw(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Out-of-sample R^2 against random-walk benchmark (zero forecast).

    Formula: 1 - SSE_model / SSE_rw, where SSE_rw uses y_pred = 0.
    Positive means model beats RW.
    """
    sse_model = np.sum((y_true - y_pred) ** 2)
    sse_rw = np.sum(y_true ** 2)
    return float(1 - sse_model / sse_rw)


def directional_accuracy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    true_sign = np.sign(y_true)
    pred_sign = np.sign(y_pred)
    directional_call = (true_sign != 0) & (pred_sign != 0)
    if not np.any(directional_call):
        return float("nan")
    return float(np.mean(true_sign[directional_call] == pred_sign[directional_call]))


def balanced_directional_accuracy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    true_sign = np.sign(y_true)
    pred_sign = np.sign(y_pred)
    directional_call = (true_sign != 0) & (pred_sign != 0)
    if not np.any(directional_call):
        return float("nan")
    return float(balanced_accuracy_score(true_sign[directional_call], pred_sign[directional_call]))


def evaluate(y_true: np.ndarray, y_pred: np.ndarray, label: str) -> dict:
    return {
        "model": label,
        "rmse": rmse(y_true, y_pred),
        "mae": mae(y_true, y_pred),
        "oos_r2_vs_rw": oos_r2_vs_rw(y_true, y_pred),
        "dir_acc": directional_accuracy(y_true, y_pred),
        "bal_dir_acc": balanced_directional_accuracy(y_true, y_pred),
    }


def benchmark_table(results: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(results).set_index("model").round(5)


def confusion(y_true: np.ndarray, y_pred: np.ndarray) -> pd.DataFrame:
    cm = confusion_matrix(np.sign(y_true), np.sign(y_pred))
    return pd.DataFrame(cm, index=["true_down", "true_up"], columns=["pred_down", "pred_up"])


def evaluate_classifier(
    y_true: np.ndarray,
    probability: np.ndarray,
    label: str,
    horizon: str,
    threshold: float = 0.5,
) -> dict:
    prediction = (probability >= threshold).astype(int)
    return {
        "horizon": horizon,
        "model": label,
        "n": len(y_true),
        "actual_up_rate": float(np.mean(y_true)),
        "threshold": threshold,
        "balanced_accuracy": float(balanced_accuracy_score(y_true, prediction)),
        "brier_score": float(brier_score_loss(y_true, probability)),
        "log_loss": float(log_loss(y_true, probability, labels=[0, 1])),
    }


def classifier_confusion(
    y_true: np.ndarray,
    probability: np.ndarray,
    label: str,
    horizon: str,
    threshold: float = 0.5,
) -> pd.DataFrame:
    prediction = (probability >= threshold).astype(int)
    matrix = confusion_matrix(y_true, prediction, labels=[0, 1])
    records = []
    for true_label in (0, 1):
        for pred_label in (0, 1):
            records.append(
                {
                    "horizon": horizon,
                    "model": label,
                    "threshold": threshold,
                    "true_direction": "up" if true_label else "down",
                    "predicted_direction": "up" if pred_label else "down",
                    "count": int(matrix[true_label, pred_label]),
                }
            )
    return pd.DataFrame(records)


def paired_classifier_loss_tests(
    predictions: pd.DataFrame,
    benchmark: str = "HistoricalBaseRate",
    hac_lags: int = 4,
) -> pd.DataFrame:
    """Compare paired probability losses using a HAC intercept test.

    A negative mean loss difference favors the learned model.
    """
    wide_probability = predictions.pivot(
        index="date", columns="model", values="probability_up"
    )
    wide_actual = predictions.pivot(index="date", columns="model", values="actual")
    if benchmark not in wide_probability:
        raise ValueError(f"benchmark model not found: {benchmark}")

    y_true = wide_actual[benchmark].to_numpy(dtype=float)
    benchmark_probability = wide_probability[benchmark].to_numpy(dtype=float)
    records = []
    for model in wide_probability.columns:
        if model == benchmark:
            continue
        model_probability = wide_probability[model].to_numpy(dtype=float)
        losses = {
            "brier": (
                (y_true - model_probability) ** 2,
                (y_true - benchmark_probability) ** 2,
            ),
            "log_loss": (
                -(
                    y_true * np.log(np.clip(model_probability, 1e-15, 1 - 1e-15))
                    + (1 - y_true)
                    * np.log(np.clip(1 - model_probability, 1e-15, 1 - 1e-15))
                ),
                -(
                    y_true
                    * np.log(np.clip(benchmark_probability, 1e-15, 1 - 1e-15))
                    + (1 - y_true)
                    * np.log(
                        np.clip(1 - benchmark_probability, 1e-15, 1 - 1e-15)
                    )
                ),
            ),
        }
        for loss_name, (model_loss, benchmark_loss) in losses.items():
            difference = model_loss - benchmark_loss
            fit = sm.OLS(difference, np.ones(len(difference))).fit(
                cov_type="HAC", cov_kwds={"maxlags": hac_lags}
            )
            confidence_interval = fit.conf_int()[0]
            records.append(
                {
                    "model": model,
                    "benchmark": benchmark,
                    "loss": loss_name,
                    "n": len(difference),
                    "model_mean_loss": float(np.mean(model_loss)),
                    "benchmark_mean_loss": float(np.mean(benchmark_loss)),
                    "mean_loss_difference": float(np.mean(difference)),
                    "hac_standard_error": float(fit.bse[0]),
                    "test_statistic": float(fit.tvalues[0]),
                    "p_value": float(fit.pvalues[0]),
                    "ci_95_lower": float(confidence_interval[0]),
                    "ci_95_upper": float(confidence_interval[1]),
                    "hac_lags": hac_lags,
                }
            )
    return pd.DataFrame(records)
