import numpy as np
import pandas as pd

from src.classification import (
    one_week_search_space,
    purged_training_frame,
    validation_probabilities,
)
from src.evaluation import evaluate_classifier, paired_classifier_loss_tests
from src.features import (
    DIRECTION_EXTENDED_FEATURE_COLS,
    DIRECTION_FEATURE_COLS,
    USD_FACTOR_QUOTES,
    build_direction_features,
    leave_cad_out_usd_factor,
)


def synthetic_weekly(rows: int = 16) -> pd.DataFrame:
    index = pd.date_range("2020-01-03", periods=rows, freq="W-FRI")
    time = np.arange(rows, dtype=float)
    data = {
        "usdcad": np.exp(0.01 * time),
        "wti": np.exp(0.005 * time),
        "vix": 20.0 + time,
        "ca_1y": 2.0 + 0.01 * time,
        "us_1y": 1.5 + 0.005 * time,
    }
    for pair, quote_sign in USD_FACTOR_QUOTES.items():
        data[pair] = np.exp(quote_sign * 0.01 * time)
    return pd.DataFrame(data, index=index)


def test_direction_targets_are_forward_aligned() -> None:
    weekly = synthetic_weekly()
    features = build_direction_features(weekly)

    np.testing.assert_allclose(features["y_1w"], 0.01)
    np.testing.assert_allclose(features["y_4w"].dropna(), 0.04)
    assert features["direction_1w"].eq(1).all()
    assert features["direction_4w"].dropna().eq(1).all()
    assert features["y_1w"].notna().all()
    assert features["y_4w"].isna().sum() == 3
    assert [column for column in features if column in DIRECTION_FEATURE_COLS] == DIRECTION_FEATURE_COLS


def test_usd_factor_is_positive_when_usd_appreciates() -> None:
    factor = leave_cad_out_usd_factor(synthetic_weekly()).dropna()
    np.testing.assert_allclose(factor, 0.01)


def test_extended_direction_features_use_only_trailing_information() -> None:
    features = build_direction_features(synthetic_weekly())

    np.testing.assert_allclose(features["d_policy_spread_4w"].dropna(), 0.02)
    np.testing.assert_allclose(features["r_usd_factor_4w"].dropna(), 0.04)
    np.testing.assert_allclose(features["r_wti_4w"].dropna(), 0.02)
    np.testing.assert_allclose(features["d_vix_4w"].dropna(), 4.0)
    np.testing.assert_allclose(features["r_usdcad_1w"], 0.01)
    np.testing.assert_allclose(features["r_usdcad_4w"].dropna(), 0.04)
    assert [column for column in features if column in DIRECTION_EXTENDED_FEATURE_COLS] == (
        DIRECTION_EXTENDED_FEATURE_COLS
    )


def test_purged_training_frame_removes_full_gap() -> None:
    df = pd.DataFrame(
        {"value": np.arange(12)},
        index=pd.date_range("2020-01-03", periods=12, freq="W-FRI"),
    )
    origin = df.index[10]
    train = purged_training_frame(df, origin, gap=4)

    assert train.index[-1] == df.index[5]
    assert list(df.index[6:10]) == list(df.index[df.index > train.index[-1]][:4])


def test_validation_predictions_never_train_through_origin() -> None:
    index = pd.date_range("2016-01-01", periods=40, freq="W-FRI")
    time = np.arange(len(index), dtype=float)
    df = pd.DataFrame(index=index)
    for offset, column in enumerate(DIRECTION_FEATURE_COLS, start=1):
        df[column] = np.sin(time / offset)
    df["direction_1w"] = (time.astype(int) % 2).astype("int8")

    predictions = validation_probabilities(
        df,
        model_name="Logistic",
        feature_cols=DIRECTION_FEATURE_COLS,
        params={"C": 0.1},
        validation_start=str(index[15].date()),
        validation_end=str(index[25].date()),
        gap=1,
    )

    assert predictions["date"].max() <= index[25]
    for row in predictions.itertuples(index=False):
        origin_position = df.index.get_loc(row.date)
        assert row.train_end == df.index[origin_position - 2]


def test_classifier_metrics_apply_locked_threshold() -> None:
    y_true = np.array([0, 1, 0, 1])
    probability = np.array([0.46, 0.48, 0.52, 0.54])

    default = evaluate_classifier(y_true, probability, "model", "1w")
    lowered = evaluate_classifier(
        y_true, probability, "model", "1w", threshold=0.47
    )

    assert default["balanced_accuracy"] == 0.5
    assert lowered["balanced_accuracy"] == 0.75
    assert lowered["threshold"] == 0.47


def test_paired_loss_test_uses_date_matched_probabilities() -> None:
    dates = pd.date_range("2020-01-03", periods=20, freq="W-FRI")
    actual = np.tile([0, 1], 10)
    records = []
    for date, label in zip(dates, actual, strict=True):
        records.append(
            {
                "date": date,
                "model": "HistoricalBaseRate",
                "actual": label,
                "probability_up": 0.5,
            }
        )
        model_probability = 0.6 if label else 0.4
        records.append(
            {
                "date": date,
                "model": "Model",
                "actual": label,
                "probability_up": model_probability,
            }
        )

    tests = paired_classifier_loss_tests(pd.DataFrame(records), hac_lags=1)

    assert set(tests["loss"]) == {"brier", "log_loss"}
    assert tests["n"].eq(20).all()
    assert tests["mean_loss_difference"].lt(0).all()


def test_tuning_grid_contains_original_model_settings() -> None:
    candidates = one_week_search_space()

    assert len(candidates) == 58
    assert any(
        candidate["model"] == "ElasticNet"
        and candidate["feature_set"] == "core"
        and candidate["params"] == {"C": 1.0, "l1_ratio": 0.5}
        for candidate in candidates
    )
    assert any(
        candidate["model"] == "XGBoost"
        and candidate["feature_set"] == "core"
        and candidate["params"]["min_child_weight"] == 10
        and candidate["params"]["reg_lambda"] == 10.0
        for candidate in candidates
    )
