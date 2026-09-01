# Learning Guide: Tuning and Interpretation

The pedagogical walkthrough for Stage 3. What you actually learn, in what order, and where each piece lives in this repo. Read this alongside `docs/xgboost_notes.md`. This file is the "why and in what order"; the notes are the write-up.

---

## 1. What hyperparameter tuning teaches you here

You are not pressing "optimize." You are answering: which XGBoost settings give the best out-of-sample USD/CAD forecast without overfitting?

The learning targets are not the best parameters. They are:

1. How model complexity affects performance.
2. How overfitting shows up (train improves, validation degrades).
3. Why validation method matters (time-series, not random).
4. Why time-series tuning differs from random cross-validation.
5. How to compare models honestly against benchmarks.

The single sentence you should be able to say at the end:

> I understand why a more complex model can look better in training but fail out of sample.

That sentence is the deliverable. The tuned model is secondary.

## 2. The six hyperparameters that matter (start here only)

| Parameter | Controls | Try | Increasing it does |
|---|---|---|---|
| `max_depth` | tree complexity | 2, 3 | more flexible, more overfit risk. Depth 5+ likely overfits this small dataset. |
| `learning_rate` (`eta`) | how slowly it learns | 0.03, 0.05, 0.1 | faster fit, more overfit risk. Lower is more conservative. |
| `n_estimators` (`num_boost_round`) | number of trees | 100, 300, 500 | more fitting power; too many overfits unless early-stopped. |
| `subsample` | fraction of rows per tree | 0.7, 1.0 | 0.7 adds randomness, can reduce overfitting. |
| `colsample_bytree` | fraction of features per tree | 0.7, 1.0 | useful when predictors are correlated; can reduce overfitting. |
| `reg_lambda` | L2 regularization | 1, 5, 10 | higher is more conservative, lower is more flexible. |

Do not tune more than these six in v1. The grid in `scripts/05_xgboost_tuning.py` uses exactly this set.

## 3. How to tune properly

The rule: **the test set is sacred. Do not keep tuning after seeing test results.**

Validation structure (lives in `src/features.py` `train_val_test_split`):

```
Train:      2005-2016
Validation: 2017-2019   (pick best settings here)
Test:       2020-2026   (touch once, report)
```

Process:
1. Fit many settings on train, score on validation.
2. Pick best by validation RMSE/MAE.
3. Refit, test once on the final test set.
4. Compare against random walk, AR(1), and Ridge.

Why time-series and not random k-fold: random folds let the model train on future data to predict the past. That is look-ahead bias. `TimeSeriesSplit` and walk-forward respect the arrow of time. This is the single most common interview question about the project.

## 4. The untuned-vs-tuned comparison (do not skip)

To show that tuning actually did something, report an **untuned XGBoost** (default parameters) alongside the **tuned** one. If they are nearly identical, that itself is a finding: tuning bought little, and the benchmark discipline matters more than the knobs.

Target table for your README:

| Model | RMSE | MAE | OOS R² vs RW | Directional Accuracy |
|---|---|---|---|---|
| Random Walk | x | x | 0.000 | x |
| AR(1) | x | x | x | x |
| Ridge | x | x | x | x |
| XGBoost untuned | x | x | x | x |
| XGBoost tuned | x | x | x | x |

Then write one sentence:

> Tuning improved validation performance by [amount], but the final test result shows whether the improvement survives out of sample.

`scripts/05_xgboost_tuning.py` writes only the tuned final row. There is no untuned XGBoost row in `outputs/tables/xgb_final_eval.csv` or `outputs/tables/benchmark_table.csv`. Treat the missing untuned comparison as a locked documentation gap, not a to-do.

## 5. The interpretation ladder (use in this exact order)

Interpretation is not one step. Climb these five rungs in order. Each is harder and more informative than the last.

### Rung 1: Correlation and rolling correlation (before any ML)
Lives in: `scripts/03_eda.py`, `src/plots.py` `rolling_corr`.
Ask: Is the oil-CAD relationship stable? Does correlation change over time?

### Rung 2: Ridge coefficients
Lives in: `src/interpretation.py` `ridge_coefficient_report`.
Ask: Directionally, do oil, rates, and risk variables behave as theory expects? The report checks each coefficient's sign against a prior-sign expectation.

### Rung 3: XGBoost feature importance (gain, weight, cover)
Lives in: `scripts/06_interpretation.py` `importance_table`.
Ask: Which variables reduce forecast error most often? Report all three; they often disagree.

### Rung 4: Permutation importance
Lives in: `src/interpretation.py` `permutation_importance_table`.
Ask: If I shuffle this variable, how much does performance get worse? This is the most honest measure: it tests real predictive contribution, robust to correlation. Run on the test set.

### Rung 5: SHAP (only after the model works)
Lives in: `scripts/06_interpretation.py` (TreeExplainer).
Ask: For each prediction, did this variable push the USD/CAD forecast up or down? Per-observation, directional.

Do not jump to SHAP. Climb the ladder. If you skip rungs you cannot explain in an interview why each tool tells you something different.

## 6. Two levels of interpretation

### Level 1: Model interpretation (what did it use?)
"The model relied most on VIX changes and the Canada-US 2Y spread, while WTI mattered mainly during high-oil-volatility periods."

### Level 2: Economic interpretation (does it make macro sense?)

Pre-written readouts to adapt based on your actual results:

- **If VIX is important:** USD/CAD is strongly affected by global risk-off conditions, consistent with USD strength during stress periods.
- **If oil is important:** CAD appears commodity-sensitive, but the relationship may be unstable across regimes.
- **If CA-US 2Y spread is important:** short-rate differentials may capture monetary-policy expectations affecting FX.
- **If lagged USD/CAD dominates:** the model may be using recent FX momentum or reversal rather than macro fundamentals. This is the result to watch for: it would mean the macro factors add little.

The Level 2 readout is what separates an economist from someone who ran a model.

## 7. Interview framing: good vs bad

**Good (sounds serious):**

> I used XGBoost as the flagship model because it handles nonlinear tabular relationships well. I tuned only a small set of hyperparameters using time-series validation, not random cross-validation, because this is forecasting data. I compared the tuned model against random-walk and Ridge benchmarks, then interpreted it using feature importance, permutation importance, and regime analysis.

**Bad (sounds shallow):**

> I used GridSearchCV and got the best parameters.

The difference is that the good version names the validation choice, the benchmark discipline, and the interpretation ladder. The bad version names a function.

## 8. What this guide maps to in the repo

| Learning item | Lives in |
|---|---|
| Hyperparameter table + theory | `docs/xgboost_notes.md` |
| Three-pass tuning (manual, random, Optuna). Untuned baseline was planned and is not in the shipped tables | `scripts/05_xgboost_tuning.py` |
| Time-series split | `src/features.py` |
| Rolling correlation (Rung 1) | `scripts/03_eda.py`, `src/plots.py` |
| Ridge coefficient report (Rung 2) | `src/interpretation.py` |
| Gain/weight/cover importance (Rung 3) | `scripts/06_interpretation.py` |
| Permutation importance (Rung 4) | `src/interpretation.py` |
| SHAP (Rung 5) | `scripts/06_interpretation.py` |
| Regime analysis | `scripts/06_interpretation.py` |
| Interview framing | `POSITIONING.md` |

## 9. The one rule

Tune XGBoost only after the benchmarks work, and interpret the results economically, not just technically.
