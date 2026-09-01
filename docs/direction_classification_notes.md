# Focused Direction Classification

## Question

Can a compact macro-financial information set forecast whether USD/CAD will rise or fall over the next week?

One week is the primary model horizon. Four weeks remains a secondary robustness extension and does not replace the shipped regression results.

## Economic motivation

Devereux and Smith, "Commodity Currencies and Monetary Policy" (Queen's Economics Department Working Paper 1408), argue that commodity prices may affect commodity currencies through expected future relative monetary policy. After accounting for that policy channel, commodity prices have no significant remaining role in their exchange-rate model.

Reference: https://www.econ.queensu.ca/sites/econ.queensu.ca/files/wpaper/qed_wp_1408.pdf

This extension uses that mechanism only as forecasting motivation. It makes no causal claim.

## Design

The original feature set is deliberately limited to five variables:

1. Canada-US 1-year yield spread.
2. Weekly change in that spread.
3. Leave-CAD-out global USD factor.
4. WTI return.
5. VIX change.

The 1-year spread is a public policy-path proxy, not an OIS or high-frequency monetary-policy surprise. The global USD factor is an equal-weighted USD return against eight currencies and excludes CAD.

The tuning pass compares that core with one controlled 11-variable extension. The extension adds 4-week changes in the policy spread, USD factor, WTI and VIX, plus trailing 1-week and 4-week USD/CAD returns. Every added variable is observable at the forecast origin and the total remains below the 15-feature cap.

The three learned classifiers remain:

1. Logistic regression.
2. Elastic-net logistic regression.
3. XGBoost classifier.

The forecast estimand is

`P(log(USD/CAD[t+1]) - log(USD/CAD[t]) > 0 | information available at t)`.

This is a predictive probability, not a causal monetary-policy coefficient. A historical expanding-window up-rate is included only as the probability benchmark.

The tuning search is intentionally small: four Logistic `C` values, six Elastic Net `C` values crossed with three `l1_ratio` values, and seven XGBoost configurations. The original fixed settings are included explicitly. Each model may select the core or extended feature set. No random search or Optuna is used.

## Validation

- Tuning period: weekly expanding-window forecasts from 2017 through 2019.
- Locked evaluation period: 2020 through April 2026 for one week and March 2026 for four weeks.
- Forecast origins advance one week at a time.
- Models are refit on an expanding window at every origin.
- The 1-week target uses a 1-week purge; the 4-week target uses a 4-week purge.
- Four-week targets overlap, so the purge prevents target-window overlap between training and forecast origin.
- Hyperparameters and feature sets minimize validation Brier score. A decision threshold between `0.45` and `0.55` is then selected using validation balanced accuracy.
- A 2010-start sensitivity check is run before applying the selected specification to the evaluation period.

The post-2019 period had already been inspected in the original fixed-model extension before this tuning pass. The code keeps tuning mechanically isolated from it, but the new scores are model-development evidence rather than a fresh untouched confirmation sample.

## Results

| Horizon | Model | Balanced accuracy | Brier score | Log loss |
|---|---|---:|---:|---:|
| 1 week | Historical base rate | 0.50000 | 0.25032 | 0.69379 |
| 1 week | Logistic | 0.54126 | 0.24898 | 0.69102 |
| 1 week | Elastic Net | 0.54428 | 0.24903 | 0.69112 |
| 1 week | XGBoost | 0.52731 | 0.25049 | 0.69420 |
| 4 weeks | Historical base rate | 0.47769 | 0.25083 | 0.69480 |
| 4 weeks | Logistic | 0.52542 | 0.25153 | 0.69625 |
| 4 weeks | Elastic Net | 0.52841 | 0.25154 | 0.69628 |
| 4 weeks | XGBoost | 0.52000 | 0.25398 | 0.70134 |

There are 329 one-week test forecasts through 2026-04-17 and 326 four-week forecasts through 2026-03-27. Full prediction probabilities and confusion counts are saved in `outputs/tables/direction_predictions.csv` and `outputs/tables/direction_confusion_matrix.csv`.

### One-week tuning pass

| Run | Model | Threshold | Balanced accuracy | Brier score | Log loss |
|---|---|---:|---:|---:|---:|
| Original fixed | Logistic | 0.500 | 0.54126 | 0.24898 | 0.69102 |
| Original fixed | Elastic Net | 0.500 | 0.54428 | 0.24903 | 0.69112 |
| Original fixed | XGBoost | 0.500 | 0.52731 | 0.25049 | 0.69420 |
| Validation tuned | Logistic | 0.500 | 0.50044 | 0.24964 | 0.69243 |
| Validation tuned | Elastic Net | 0.490 | 0.48219 | 0.25021 | 0.69356 |
| Validation tuned | XGBoost | 0.510 | 0.53463 | 0.24940 | 0.69195 |
| Benchmark | Historical base rate | 0.500 | 0.50000 | 0.25032 | 0.69379 |

The selected XGBoost uses the extended feature set, 40 depth-1 trees, learning rate `0.03`, minimum child weight `20` and `reg_lambda=20`. This is a deliberately low-capacity nonlinear model.

The original Logistic model improves mean Brier loss over the historical base rate by `0.00134`, but its four-lag HAC interval is `[-0.00679, 0.00410]` with `p = 0.629`. The original Elastic Net probability gain is similarly unresolved (`p = 0.632`).

The tuned XGBoost improves mean Brier loss relative to the historical base rate by `0.00092`, but the four-lag HAC 95% interval for that loss difference is `[-0.00296, 0.00112]` with `p = 0.375`. The interval includes zero. The result is therefore not statistically resolved.

## Interpretation

The original one-week linear models still provide the highest threshold accuracy. Validation tuning over-regularizes Logistic and Elastic Net, so their tuned versions are not improvements.

Tuning improves XGBoost relative to its original fixed specification, but it does not beat the original linear models. The gain is small, varies by year, and is not statistically distinguishable from the historical probability benchmark with the available sample.

The four-week result is mixed. All learned models improve threshold-based balanced accuracy relative to the historical base-rate rule, but all have worse Brier scores and log loss. Therefore, the extension does not establish better calibrated four-week probability forecasts.

The 2010-start sensitivity keeps the shallow XGBoost capacity settings but switches its selected feature set from extended to core and moves the threshold from `0.510` to `0.545`. That instability is a warning against further threshold mining.

The practical one-week conclusion is model-dependent: the original Elastic Net leads threshold direction, and the original Logistic model leads probability scoring. Tuned XGBoost is a useful low-capacity robustness result, not the main model. None of the results is strong enough for a trading or causal claim.

## Limitations

1. The 1-year yield spread is not a clean monetary-policy surprise.
2. Four-week labels overlap, although the expanding-window purge prevents training leakage.
3. The evaluation period includes COVID-19 and the subsequent inflation cycle.
4. The experiment is forecasting, not causal identification and not a trading strategy.
5. The original evaluation period was observed before tuning, so an entirely new future sample is still required for clean confirmation.
6. Hyperparameter, feature-set and threshold comparisons create selection uncertainty beyond the reported HAC loss test.
