# Run Log

Date: 2026-05-30.

Environment: conda base.

## Commands run

```bash
conda run -n base python -m py_compile src/data.py src/features.py src/evaluation.py src/interpretation.py src/lp.py src/plots.py scripts/00_project_checks.py scripts/01_collect_data.py scripts/02_features.py scripts/03_eda.py scripts/04_benchmarks.py scripts/05_xgboost_tuning.py scripts/06_interpretation.py scripts/07_lp_irf.py
conda run -n base python scripts/01_collect_data.py
conda run -n base python scripts/02_features.py
conda run -n base python scripts/00_project_checks.py
conda run -n base python scripts/03_eda.py
conda run -n base python scripts/04_benchmarks.py
conda run -n base python -m pip install -r requirements.txt
conda run -n base python scripts/05_xgboost_tuning.py
conda run -n base python scripts/06_interpretation.py
conda run -n base python scripts/07_lp_irf.py
```

## Diagnostics

```text
daily shape: (5564, 9)
weekly shape: (1112, 9)
data cap: 2026-04-30
weekly date range: 2005-01-07 to 2026-04-24
features shape: (1103, 13)
feature date range: 2005-03-04 to 2026-04-17
feature count: 12
target alignment max abs error: 0
```

## Important implementation decisions

1. Enforced `DATA_END = 2026-04-30` in `src/data.py`.
2. Dropped weekly rows after the cap, so the final weekly date is 2026-04-24.
3. Added `NASDAQCOM` as `nasdaq` because FRED `SP500` is source-limited to about 10 years of daily history.
4. Replaced the full-sample equity feature with `r_equity = weekly log return of NASDAQCOM`.
5. Fixed AR(1) to forecast next week's USD/CAD return from returns observable through the current week.
6. Fixed directional accuracy so a zero random-walk forecast is not treated as an up/down call.
7. Treated pre-2020 XGBoost regime evaluation as validation-window diagnostic because the final test window begins in 2020.

## Output files created

Figures:

```text
outputs/figures/01_usdcad.png
outputs/figures/02_wti.png
outputs/figures/03_usdcad_vs_wti.png
outputs/figures/04_rolling_corr_usdcad_wti.png
outputs/figures/05_spread_2y.png
outputs/figures/06_vix.png
outputs/figures/07_corr_heatmap.png
outputs/figures/08_shap_summary.png
outputs/figures/09_irf_wti.png
outputs/figures/10_irf_spread2y.png
outputs/figures/11_irf_vix.png
```

Tables and model:

```text
outputs/tables/summary_stats.csv
outputs/tables/correlation_table.csv
outputs/tables/benchmark_table.csv
outputs/tables/benchmark_predictions.csv
outputs/tables/ridge_coefficients.csv
outputs/tables/xgb_pass1_manual.csv
outputs/tables/xgb_pass2_random.csv
outputs/tables/xgb_pass3_optuna.csv
outputs/tables/xgb_final_eval.csv
outputs/tables/feature_importance_native.csv
outputs/tables/feature_importance_permutation.csv
outputs/tables/regime_table.csv
outputs/tables/irf_wti.csv
outputs/tables/irf_spread2y.csv
outputs/tables/irf_vix.csv
outputs/xgb_final.json
```

Docs:

```text
docs/STEVEN_PICKUP.md
docs/fx_primer.md
docs/macro_finance_note.md
docs/xgboost_notes.md
docs/lp_irf_notes.md
docs/findings.md
docs/RUN_LOG.md
```

## 2026-07-15 one-week direction tuning

Environment: conda base.

Implemented a validation-only tuning pass for Logistic, Elastic Net and XGBoost direction classifiers. Hyperparameters and feature sets use 2017-2019 expanding-window forecasts; post-2019 evaluation remains separate in code. The one-week and four-week samples are filtered independently.

Verification:

```text
pytest: 8 passed
validation candidates: 58, including every original fixed specification
direction feature count: 11
target alignment max absolute error: 0 at 1 week and 4 weeks
one-week test forecasts: 329
four-week test forecasts: 326
```

One-week model ranking:

```text
Original Elastic Net balanced accuracy: 0.54428
Original Logistic Brier score:          0.24898
Original Logistic log loss:             0.69102
Tuned XGBoost balanced accuracy:         0.53463
Tuned XGBoost Brier score:               0.24940
Tuned XGBoost log loss:                  0.69195
Original Logistic Brier HAC p-value:     0.629
XGBoost Brier loss HAC p-value:          0.375
```

Tuning improves XGBoost relative to its fixed version but does not beat the original linear models. The loss-difference confidence interval includes zero.
