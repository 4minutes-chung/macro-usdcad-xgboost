# Steven Pickup Note

Last updated: 2026-09-01.

## Wrap status

**CLOSED-ARCHIVED (hard wrap 2026-07-31; interview Q&A locked 2026-09-01).** Forecasting work is finished. No active next step in this repository. `docs/USD_CAD_RESEARCH_CONTINUATION_PLAN.md` is DEFERRED-NO-BUILD. Future papers (monetary-policy event study; separate GB methodology) stay cold and, if ever started, belong in separate repos with explicit reopen authorization.

**Reopen floor:** this archive does not reopen. Any continuation must name a dataset, an hour count, and a new repo. Oil-news / expected-policy-path work is not a next step here.

## Current state

Stages 1-4, the focused direction-classification extension and the one-week tuning pass are built and runnable in conda base. The forecasting specification is frozen. The separate monetary-policy event study is the adopted but deferred future economics-paper direction. Gradient boosting remains a separate future methodology project with no selected dataset. Neither is active work in this repository.

Core result: the project is an honest FX predictability null. The macro factors explain contemporaneous USD/CAD movement better than they forecast 1-week-ahead USD/CAD. Random walk is still the benchmark to beat.

## Run order

```bash
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
```

Run `scripts/07_lp_irf.py` only if you want to refresh the optional LP/IRF outputs.

## What each script does

| Script | Role | Main output |
|---|---|---|
| `01_collect_data.py` | Pull FRED + BoC daily data, cap at 2026-04-30, resample weekly Friday | `data/raw/daily.parquet`, `data/raw/weekly.parquet` |
| `02_features.py` | Build 12 observable-at-t features and `y_1w` target | `data/processed/features.parquet` |
| `00_project_checks.py` | Check date cap, feature count, target alignment | printed pass/fail diagnostics |
| `03_eda.py` | Make Stage 1 charts and tables | `outputs/figures/01_*.png` to `07_*.png`, summary/correlation CSVs |
| `04_benchmarks.py` | Evaluate random walk, AR(1), Ridge | `benchmark_table.csv`, `ridge_coefficients.csv` |
| `05_xgboost_tuning.py` | Manual grid, random search, Optuna | `xgb_pass*.csv`, `xgb_final.json`, `xgb_final_eval.csv` |
| `06_interpretation.py` | XGBoost importance, permutation, SHAP, regimes | importance CSVs, `08_shap_summary.png`, `regime_table.csv` |
| `07_lp_irf.py` | Optional local projections for oil, spread, VIX shocks | `09_*.png` to `11_*.png`, `irf_*.csv` |
| `08_direction_classification.py` | Expanding-window 1-week and 4-week direction comparison | `direction_metrics.csv`, predictions and confusion matrix |
| `09_tune_one_week_direction.py` | Validation-only tuning for the primary one-week classifiers | tuning search, locked metrics, annual stability and HAC loss tests |

## Main findings

1. Contemporaneous oil and equity moves line up with USD/CAD in the expected direction. In the full feature sample, `corr(r_usdcad, r_wti) = -0.377` and `corr(r_usdcad, r_equity) = -0.453`.
2. The 1-week-ahead target is close to unforecastable with these features. The largest simple target correlations are small: `d_vix` at `0.047`, `spread_2y` at `0.049`, and `r_equity` at `-0.034`.
3. Random walk wins Stage 2 on RMSE. AR(1) is barely worse. Ridge is worse on RMSE but has directional accuracy around 55%.
4. Ridge signs partly match macro priors: oil return, equity return, and VIX change have expected signs. VIX level has the wrong sign in this sample.
5. Tuned XGBoost barely beats random walk on RMSE (`OOS R2 = 0.00031`) but gives no directional edge (`dir_acc = 0.49847`).
6. The final XGBoost model is effectively intercept-only. Native importance, permutation importance, and SHAP are all zero because the model made no splits.
7. Regime tables do not rescue the story. High VIX has worse direction than low VIX; high oil-vol and low oil-vol both have tiny OOS R2.
8. LP/IRF signs are sensible at horizon 0: WTI shock negative, 2Y spread shock negative, VIX shock positive. Identification is weak and later-horizon persistence is limited.
9. The original one-week Elastic Net has the highest balanced accuracy at `0.54428`; original Logistic has the best probability scores (`Brier = 0.24898`, `log loss = 0.69102`).
10. Tuned shallow XGBoost improves its fixed version but does not beat the original linear models. Neither the original Logistic nor tuned XGBoost Brier gain is statistically resolved (`p = 0.629` and `p = 0.375`, four-lag HAC). Four-week probability forecasting remains a null.

## Key caveats

FRED `SP500` daily history is source-limited to about 10 years. The full-sample equity-risk feature uses FRED `NASDAQCOM` instead, documented in `data/DATA_DICTIONARY.md` and `RESEARCH_PLAN.md`.

The random-walk row has blank directional accuracy because a zero-return forecast has no up/down direction.

The pre/post-2020 regime split is not a pure test-set split because the test window starts in 2020. The pre-2020 row is a validation diagnostic, not a final test metric.

## What Steven should read first

1. `docs/findings.md`
2. `docs/macro_finance_note.md`
3. `outputs/tables/benchmark_table.csv`
4. `outputs/tables/feature_importance_native.csv`
5. `docs/xgboost_notes.md`
6. `docs/lp_irf_notes.md`
7. `docs/direction_classification_notes.md`

## Pitch version

This project tests whether oil, Canada-US rate spreads, VIX, and a U.S. equity-risk proxy forecast USD/CAD one week ahead. The descriptive relationships and same-week LP shock responses are economically sensible, but they do not translate into strong 1-week-ahead predictive power. Random walk remains hard to beat in return regression. The regression XGBoost collapses to an intercept-only model; a separate shallow direction classifier shows a small but unconfirmed probability-score gain. The contribution is benchmark discipline and transparent interpretation, not a winning trading model.
