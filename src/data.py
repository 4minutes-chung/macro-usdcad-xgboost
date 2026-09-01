"""Data ingestion: FRED, BoC Valet, and Statistics Canada.

All sources use direct HTTP. No API keys required.

Note on series codes:
- FRED DEXCAUS = Canadian dollars per 1 USD (higher = USD stronger).
- BoC Valet uses BD.CDN.*YR.DQ.YLD format for benchmark bond yields (modern API).
"""

from __future__ import annotations

import io
import zipfile

import pandas as pd
import requests

DATA_START = "2005-01-01"
DATA_END = "2026-04-30"

FRED_SERIES = {
    "usdcad": "DEXCAUS",
    "wti": "DCOILWTICO",
    "vix": "VIXCLS",
    "us_1y": "DGS1",
    "us_2y": "DGS2",
    "us_10y": "DGS10",
    "spx": "SP500",
    "nasdaq": "NASDAQCOM",
    "eurusd": "DEXUSEU",
    "gbpusd": "DEXUSUK",
    "usdjpy": "DEXJPUS",
    "usdchf": "DEXSZUS",
    "audusd": "DEXUSAL",
    "usdnok": "DEXNOUS",
    "usdsek": "DEXSDUS",
    "nzdusd": "DEXUSNZ",
}

BOC_SERIES = {
    "ca_2y": "BD.CDN.2YR.DQ.YLD",
    "ca_10y": "BD.CDN.10YR.DQ.YLD",
}

STATCAN_TABLE_URL = "https://www150.statcan.gc.ca/n1/en/tbl/csv/10100139-eng.zip"
STATCAN_TABLE_FILE = "10100139.csv"
STATCAN_SERIES = {
    "ca_1y": "v39067",
}


def fetch_fred_series(code: str) -> pd.Series:
    """Fetch a single FRED series as CSV. No API key needed."""
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={code}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text), na_values=".")
    date_col = df.columns[0]  # "observation_date" or "DATE" depending on version
    df[date_col] = pd.to_datetime(df[date_col])
    return df.set_index(date_col)[code]


def fetch_fred(start: str = DATA_START, end: str = DATA_END) -> pd.DataFrame:
    end_ts = pd.Timestamp(end)
    df = pd.concat(
        [fetch_fred_series(code).rename(name) for name, code in FRED_SERIES.items()],
        axis=1,
    ).rename_axis("date")
    return df.loc[pd.Timestamp(start):end_ts]


def fetch_boc(series_code: str, start: str = DATA_START, end: str = DATA_END) -> pd.Series:
    url = f"https://www.bankofcanada.ca/valet/observations/{series_code}/json"
    r = requests.get(url, params={"start_date": start, "end_date": end}, timeout=30)
    r.raise_for_status()
    obs = r.json()["observations"]
    s = pd.Series(
        {pd.Timestamp(o["d"]): float(o[series_code]["v"]) for o in obs if o[series_code]["v"]}
    )
    s.index.name = "date"
    return s


def fetch_boc_all(start: str = DATA_START, end: str = DATA_END) -> pd.DataFrame:
    return pd.concat(
        [fetch_boc(code, start=start, end=end).rename(name) for name, code in BOC_SERIES.items()],
        axis=1,
    )


def fetch_statcan_series(
    vector: str, start: str = DATA_START, end: str = DATA_END
) -> pd.Series:
    """Fetch one vector from Statistics Canada daily table 10-10-0139-01."""
    r = requests.get(STATCAN_TABLE_URL, timeout=60)
    r.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(r.content)) as archive:
        table = pd.read_csv(
            archive.open(STATCAN_TABLE_FILE),
            usecols=["REF_DATE", "VECTOR", "VALUE"],
            low_memory=False,
        )

    rows = table.loc[table["VECTOR"].eq(vector), ["REF_DATE", "VALUE"]].dropna()
    if rows.empty:
        raise ValueError(f"Statistics Canada vector {vector} returned no observations")
    rows["REF_DATE"] = pd.to_datetime(rows["REF_DATE"])
    series = rows.set_index("REF_DATE")["VALUE"].astype(float).sort_index()
    series.index.name = "date"
    return series.loc[pd.Timestamp(start):pd.Timestamp(end)]


def fetch_statcan_all(start: str = DATA_START, end: str = DATA_END) -> pd.DataFrame:
    return pd.concat(
        [
            fetch_statcan_series(vector, start=start, end=end).rename(name)
            for name, vector in STATCAN_SERIES.items()
        ],
        axis=1,
    )


def fetch_all(start: str = DATA_START, end: str = DATA_END) -> pd.DataFrame:
    """Combined daily dataset from FRED, BoC, and Statistics Canada."""
    daily = pd.concat(
        [
            fetch_fred(start=start, end=end),
            fetch_boc_all(start=start, end=end),
            fetch_statcan_all(start=start, end=end),
        ],
        axis=1,
    ).sort_index()
    return daily.loc[pd.Timestamp(start):pd.Timestamp(end)]


def to_weekly(df: pd.DataFrame, rule: str = "W-FRI") -> pd.DataFrame:
    """Resample daily to weekly Friday close, forward-fill within week."""
    return df.resample(rule).last().dropna(how="all")


if __name__ == "__main__":
    daily = fetch_all()
    weekly = to_weekly(daily).loc[:DATA_END]
    daily.to_parquet("data/raw/daily.parquet")
    weekly.to_parquet("data/raw/weekly.parquet")
    print(f"daily: {daily.shape}, weekly: {weekly.shape}")
    print(weekly.tail())
