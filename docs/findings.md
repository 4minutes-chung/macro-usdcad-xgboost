# Findings

## Bottom line

Random walk remains the serious benchmark for 1-week-ahead USD/CAD. The macro-financial variables have sensible contemporaneous relationships, but they do not produce strong out-of-sample forecast gains at this horizon.

This is a clean null result, not a failed project.

## Stage 1 findings

The descriptive macro-finance story works:

| Object | Finding |
|---|---|
| Oil | Same-week WTI returns are negatively correlated with USD/CAD returns. |
| Risk sentiment | Same-week VIX changes are positively correlated with USD/CAD returns. |
| Equity-risk proxy | Same-week NASDAQ returns are negatively correlated with USD/CAD returns. |
| Forecast target | Correlations with next-week USD/CAD returns are small. |

Interpretation: the factor blocks are economically relevant for explaining market movement, but not enough for simple short-horizon forecasting.

## Stage 2 benchmark results

| Model | RMSE | MAE | OOS R2 vs RW | Directional accuracy |
|---|---:|---:|---:|---:|
| Random walk | 0.00866 | 0.00657 | 0.00000 | n/a |
| AR(1) | 0.00867 | 0.00659 | -0.00256 | 0.48318 |
| Ridge | 0.00886 | 0.00666 | -0.04783 | 0.55352 |

Random walk wins RMSE. AR(1) is barely worse. Ridge gets directional signs right more often than chance in this sample, but its squared-error forecast is worse than random walk.

The random-walk directional metric is `n/a` because a zero-return forecast makes no up/down call.

## Ridge coefficient interpretation

| Feature | Coefficient sign | Prior match |
|---|---:|---|
| `r_wti` | negative | yes |
| `r_equity` | negative | yes |
| `d_vix` | positive | yes |
| `vix` | negative | no |
| `spread_2y` | positive | mixed prior |
| `spread_10y` | negative | mixed prior |

The signs are not crazy, but they are not enough to beat random walk on RMSE.

## Stage 3 XGBoost results

| Model | RMSE | MAE | OOS R2 vs RW | Directional accuracy |
|---|---:|---:|---:|---:|
| XGBoost | 0.00866 | 0.00657 | 0.00031 | 0.49847 |

XGBoost barely improves RMSE relative to random walk, but the gain is economically tiny. Directional accuracy is essentially 50%.

The most important Stage 3 result is structural: the final XGBoost model made no splits. Therefore:

| Importance method | Result |
|---|---|
| Gain | all zero |
| Weight | all zero |
| Cover | all zero |
| Permutation importance | all zero |
| SHAP | zero contributions |

Interpretation: under the chosen validation discipline and conservative tuning, the model finds no stable feature-level signal worth splitting on.

## Regime readout

| Regime | OOS R2 vs RW | Directional accuracy |
|---|---:|---:|
| High VIX | -0.00103 | 0.45399 |
| Low VIX | 0.00251 | 0.54268 |
| High oil vol | 0.00042 | 0.52147 |
| Low oil vol | 0.00016 | 0.47561 |
| Post-2020 test | 0.00031 | 0.49847 |

The high-VIX hypothesis does not hold in this run. Low VIX has better direction, but the model has no feature splits, so this should not be over-interpreted.

## Stage 4 LP/IRF results

Stage 4 is descriptive dynamic association, not causal identification. Shocks are AR(1) innovations.

| Shock | Horizon 0 beta | 95% CI | Sign read |
|---|---:|---|---|
| WTI return shock | -0.07563 | [-0.10562, -0.04564] | oil up, USD/CAD down |
| CA-US 2Y spread shock | -0.04949 | [-0.06128, -0.03769] | wider Canadian spread, USD/CAD down |
| VIX change shock | 0.001466 | [0.001004, 0.001927] | risk-off, USD/CAD up |

The signs match the macro priors at horizon 0. Later horizons mostly lose precision, so the dynamic story is short-lived.

## Project contribution

The contribution is benchmark discipline:

1. The data are capped and target alignment is checked.
2. The macro priors are stated before modeling.
3. Random walk is treated as the benchmark.
4. Linear and nonlinear models are reported honestly.
5. The null is not buried.

## Ship decision

Recommended decision: ship the full version now. The coherent story is: macro-financial relationships are visible in contemporaneous data and LP shock responses, but disciplined 1-week-ahead forecasting remains close to random walk.

## Focused direction-classification extension

The compact Logistic, Elastic Net and XGBoost comparison improves the original one-week direction question without changing the shipped V1 regression results.

- One week: Elastic Net reaches `0.54428` balanced accuracy. Logistic has the best learned-model Brier score (`0.24898`) and log loss (`0.69102`), both slightly better than the historical base rate.
- Four weeks: Elastic Net reaches `0.52841` balanced accuracy, but the historical base rate retains better Brier score and log loss than every learned model.
- One-week tuning: a strongly regularized, depth-1 XGBoost reaches `0.53463` balanced accuracy, `0.24940` Brier score and `0.69195` log loss. This improves its fixed specification but does not beat the original linear models.
- Uncertainty: the original Logistic and tuned XGBoost Brier improvements over the historical base rate have four-lag HAC `p = 0.629` and `p = 0.375`; both 95% intervals include zero.

Conclusion: the one-week classification framing contains a small, unstable predictive signal. Shallow XGBoost tuning improves probability scoring but does not establish a statistically resolved edge, and tuning weakens the linear models. Moving to four weeks still does not produce a better calibrated probability forecast. Further broad search is not justified without a new confirmation sample.
