# USD/CAD Macro-Financial Forecasting

Public archive: https://github.com/4minutes-chung/macro-usdcad-xgboost

**Status: CLOSED-ARCHIVED (2026-07-31).** Frozen forecasting specification. Not a trading model.

Stage-gated test of whether oil, Canada-US rate differentials, and risk sentiment forecast USD/CAD one week ahead. Walk-forward validation. Random walk, AR(1), Ridge, then tuned XGBoost. Optional local projections.

## Result

Random walk wins. Macro factors explain same-week USD/CAD better than they forecast next week.

| Model | RMSE | MAE | OOS R² vs RW | Dir acc |
|---|---:|---:|---:|---|
| Random walk | 0.00866 | 0.00657 | 0.00000 | n/a |
| AR(1) | 0.00867 | 0.00659 | -0.00256 | 0.483 |
| Ridge | 0.00886 | 0.00666 | -0.04783 | 0.554 |
| Tuned XGBoost | 0.00866 | 0.00657 | 0.00031 | 0.498 |

- Tuned XGBoost is intercept-only: no tree splits, so gain, weight, cover, permutation, and SHAP are all zero.
- 1-week direction: Elastic Net balanced accuracy 0.544; Logistic Brier 0.249. HAC tests of Brier gains vs the historical base rate are unresolved (`p = 0.629` and `0.375`).
- 4-week: historical base rate still has the best Brier and log loss.
- LP horizon-0 signs match priors (WTI and CA-US 2Y spread lower USD/CAD; VIX raises it). Identification is weak AR(1) innovations. Descriptive, not causal.

Full write-up: `docs/findings.md`. Interview claims: `POSITIONING.md`.

## Design

- Weekly Friday close, 2005-2026, data capped at 2026-04-30. FRED + BoC Valet + Statistics Canada. Dictionary: `data/DATA_DICTIONARY.md`.
- Train 2005-2016 / val 2017-2019 / test 2020-2026. Test set touched once. Expanding-window CV. No random k-fold.
- At most 12 features. No neural nets. No PCA.

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

Raw and processed parquet files are in `data/`. Re-running collection overwrites them under the same date cap.

## Limits

- 1-week FX is a hard horizon (Meese-Rogoff / Rossi 2013).
- About 1,100 weekly observations.
- Full-sample equity risk uses `NASDAQCOM` because FRED `SP500` daily history is short.
- Direction extension uses a 1-year yield spread as a policy-path proxy, not a surprise series.
- This archive does not reopen. Continuation would need a new repo, a named dataset, and an hour count.

## Layout

```
src/        data, features, evaluation, interpretation, plots, LP
scripts/    stage entry points 01-09
docs/       findings, notes, run log
data/       raw + processed parquet + dictionary
outputs/    figures, tables, xgb_final.json
tests/      direction-classification checks
```

## Author

Steven Chung, MA Economics, University of Toronto.
