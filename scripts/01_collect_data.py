"""Phase 2: collect raw data from FRED, BoC Valet, and Statistics Canada."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


from src.data import DATA_END, DATA_START, fetch_all, to_weekly


def main() -> None:
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    daily = fetch_all(start=DATA_START, end=DATA_END)
    weekly = to_weekly(daily).loc[:DATA_END]
    daily.to_parquet("data/raw/daily.parquet")
    weekly.to_parquet("data/raw/weekly.parquet")
    print(f"daily shape: {daily.shape}")
    print(f"weekly shape: {weekly.shape}")
    print(f"data cap: {DATA_END}")
    print(f"weekly date range: {weekly.index.min().date()} to {weekly.index.max().date()}")
    print("\nLast 5 weekly observations:")
    print(weekly.tail())
    print("\nMissing per column:")
    print(weekly.isna().sum())


if __name__ == "__main__":
    main()
