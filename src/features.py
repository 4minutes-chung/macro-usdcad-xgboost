"""Feature engineering. All features built from data available at time t.

Target: 1-week-ahead log return of USD/CAD.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


DIRECTION_FEATURE_COLS = [
    "policy_spread_1y",
    "d_policy_spread_1y",
    "r_usd_factor",
    "r_wti",
    "d_vix",
]

DIRECTION_EXTENDED_FEATURE_COLS = DIRECTION_FEATURE_COLS + [
    "d_policy_spread_4w",
    "r_usd_factor_4w",
    "r_wti_4w",
    "d_vix_4w",
    "r_usdcad_1w",
    "r_usdcad_4w",
]

DIRECTION_FEATURE_SETS = {
    "core": DIRECTION_FEATURE_COLS,
    "extended": DIRECTION_EXTENDED_FEATURE_COLS,
}

USD_FACTOR_QUOTES = {
    "eurusd": -1.0,
    "gbpusd": -1.0,
    "usdjpy": 1.0,
    "usdchf": 1.0,
    "audusd": -1.0,
    "usdnok": 1.0,
    "usdsek": 1.0,
    "nzdusd": -1.0,
}


def log_return(s: pd.Series) -> pd.Series:
    return np.log(s).diff()


def rolling_vol(r: pd.Series, window: int) -> pd.Series:
    return r.rolling(window).std()


def forward_log_return(s: pd.Series, horizon: int) -> pd.Series:
    log_level = np.log(s)
    return log_level.shift(-horizon) - log_level


def leave_cad_out_usd_factor(weekly: pd.DataFrame, periods: int = 1) -> pd.Series:
    """Equal-weighted USD return against eight currencies, excluding CAD.

    Positive values mean broad USD appreciation.
    """
    usd_returns = pd.DataFrame(
        {
            pair: quote_sign * np.log(weekly[pair]).diff(periods)
            for pair, quote_sign in USD_FACTOR_QUOTES.items()
        }
    )
    factor = usd_returns.mean(axis=1).where(usd_returns.notna().sum(axis=1) >= 6)
    return factor.rename("r_usd_factor")


def build_features(weekly: pd.DataFrame) -> pd.DataFrame:
    """Construct feature matrix and target from weekly raw data.

    All predictors observable at t. Target is the 1-week-ahead USD/CAD return.
    """
    df = weekly.copy()

    df["r_usdcad"] = log_return(df["usdcad"])
    df["r_wti"] = log_return(df["wti"])
    df["r_equity"] = log_return(df["nasdaq"])

    df["vol_usdcad_4w"] = rolling_vol(df["r_usdcad"], 4)
    df["vol_usdcad_8w"] = rolling_vol(df["r_usdcad"], 8)
    df["vol_wti_4w"] = rolling_vol(df["r_wti"], 4)
    df["vol_wti_8w"] = rolling_vol(df["r_wti"], 8)

    df["spread_2y"] = df["ca_2y"] - df["us_2y"]
    df["spread_10y"] = df["ca_10y"] - df["us_10y"]
    df["d_spread_2y"] = df["spread_2y"].diff()

    df["d_vix"] = df["vix"].diff()

    feature_cols = [
        "r_usdcad",
        "vol_usdcad_4w",
        "vol_usdcad_8w",
        "r_wti",
        "vol_wti_4w",
        "vol_wti_8w",
        "spread_2y",
        "spread_10y",
        "d_spread_2y",
        "vix",
        "d_vix",
        "r_equity",
    ]

    df["y_1w"] = df["r_usdcad"].shift(-1)  # forward-looking target

    out = df[feature_cols + ["y_1w"]].dropna()
    return out


def build_direction_features(weekly: pd.DataFrame) -> pd.DataFrame:
    """Build core and extended features with aligned direction targets."""
    df = weekly.copy()
    df["policy_spread_1y"] = df["ca_1y"] - df["us_1y"]
    df["d_policy_spread_1y"] = df["policy_spread_1y"].diff()
    df["r_usd_factor"] = leave_cad_out_usd_factor(df)
    df["r_wti"] = log_return(df["wti"])
    df["d_vix"] = df["vix"].diff()

    df["d_policy_spread_4w"] = df["policy_spread_1y"].diff(4)
    df["r_usd_factor_4w"] = leave_cad_out_usd_factor(df, periods=4)
    df["r_wti_4w"] = np.log(df["wti"]).diff(4)
    df["d_vix_4w"] = df["vix"].diff(4)
    df["r_usdcad_1w"] = log_return(df["usdcad"])
    df["r_usdcad_4w"] = np.log(df["usdcad"]).diff(4)

    df["y_1w"] = forward_log_return(df["usdcad"], 1)
    df["y_4w"] = forward_log_return(df["usdcad"], 4)
    df["direction_1w"] = (df["y_1w"] > 0).astype("Int8")
    df["direction_4w"] = (df["y_4w"] > 0).astype("Int8")
    df.loc[df["y_1w"].isna(), "direction_1w"] = pd.NA
    df.loc[df["y_4w"].isna(), "direction_4w"] = pd.NA

    target_cols = ["y_1w", "y_4w", "direction_1w", "direction_4w"]
    out = df[DIRECTION_EXTENDED_FEATURE_COLS + target_cols]
    out = out.dropna(subset=DIRECTION_FEATURE_COLS)
    return out.dropna(subset=["y_1w", "y_4w"], how="all")


def train_val_test_split(
    df: pd.DataFrame,
    train_end: str = "2016-12-31",
    val_end: str = "2019-12-31",
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Strict-comparison split avoids ambiguity when boundary dates may or may not be in index."""
    train_end_ts = pd.Timestamp(train_end)
    val_end_ts = pd.Timestamp(val_end)
    train = df.loc[df.index <= train_end_ts]
    val = df.loc[(df.index > train_end_ts) & (df.index <= val_end_ts)]
    test = df.loc[df.index > val_end_ts]
    return train, val, test


if __name__ == "__main__":
    weekly = pd.read_parquet("data/raw/weekly.parquet")
    feats = build_features(weekly)
    feats.to_parquet("data/processed/features.parquet")
    print(f"features: {feats.shape}")
    print(feats.describe().T[["count", "mean", "std", "min", "max"]])
