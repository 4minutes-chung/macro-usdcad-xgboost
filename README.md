# USD/CAD one week ahead

Do oil prices, Canada-US interest differentials, and risk sentiment forecast next-week USD/CAD, or does a random walk still win?

Weekly Friday closes, 2005-2026. FRED, Bank of Canada, and Statistics Canada. Expanding-window evaluation: train 2005-2016, validate 2017-2019, evaluate 2020-2026.

## Results

| Model | RMSE | MAE | OOS R² vs RW | Direction |
|---|---:|---:|---:|---|
| Random walk | 0.00866 | 0.00657 | 0.000 | n/a |
| AR(1) | 0.00867 | 0.00659 | -0.003 | 0.483 |
| Ridge | 0.00886 | 0.00666 | -0.048 | 0.554 |
| XGBoost | 0.00866 | 0.00657 | 0.000 | 0.498 |

Same-week WTI, NASDAQ, and VIX move with USD/CAD in the expected direction. Next-week returns do not. Random walk has the lowest RMSE. Ridge is worse on squared error even though its sign calls are above one half.

The selected XGBoost model never splits, so gain, cover, permutation importance, and SHAP are all zero. The 0.00031 OOS R² versus random walk is an intercept, not a feature effect.

On one-week direction, Elastic Net balanced accuracy is 0.544 and Logistic Brier score is 0.249. Those Brier gains versus the historical base rate are not distinguishable from zero (HAC \(p = 0.629\) and \(0.375\)). At four weeks the base rate still has the better Brier score and log loss.

Local projections at horizon 0 have the expected signs: a WTI shock and a wider Canadian 2-year spread lower USD/CAD; a VIX shock raises it. The shocks are AR(1) residuals, so the IRFs are reduced-form associations.

Write-up: [`docs/findings.md`](docs/findings.md). Sources: [`docs/READING_LIST.md`](docs/READING_LIST.md).

## Reproduce

```bash
conda run -n base python -m pip install -r requirements.txt
conda run -n base python scripts/01_collect_data.py
conda run -n base python scripts/02_features.py
conda run -n base python scripts/00_project_checks.py
conda run -n base python scripts/03_eda.py
conda run -n base python scripts/04_benchmarks.py
conda run -n base python scripts/05_xgboost_tuning.py
conda run -n base python scripts/06_interpretation.py
conda run -n base python scripts/07_lp_irf.py
conda run -n base python scripts/08_direction_classification.py
conda run -n base python scripts/09_tune_one_week_direction.py
conda run -n base python -m pytest tests/ -q
```

Data end on 2026-04-30. Equity risk uses `NASDAQCOM` because FRED's daily `SP500` history is short.

## Layout

```
src/      data, features, evaluation, interpretation, plots, local projections
scripts/  01-09
docs/     findings and notes
data/     parquet and dictionary
outputs/  figures and tables
```

Steven Chung, MA Economics, University of Toronto.
