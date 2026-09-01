# XGBoost Notes

## Gradient boosting intuition

Gradient boosting builds an additive model one tree at a time. Each new tree is chosen to reduce the current loss, so the ensemble updates predictions in the direction that lowers error. In this project the loss is squared error on 1-week-ahead USD/CAD log returns.

Chen and Guestrin (2016) describe XGBoost as a scalable tree-boosting system with regularization and efficient split search. The official XGBoost docs separate parameters into general parameters, booster parameters, and learning-task parameters.

Sources: [Chen and Guestrin 2016](https://arxiv.org/abs/1603.02754), [XGBoost parameter docs](https://xgboost.readthedocs.io/en/stable/parameter.html).

## Objective

The conceptual objective is:

```text
loss over observations + penalty over trees
```

In notation:

```text
L = sum_i l(y_i, yhat_i) + sum_k Omega(f_k)
```

For this project, the important part is not the algebra. The important part is that XGBoost is allowed to say: no split is worth it. That is what happened. The final model has one terminal node and no feature splits.

## Hyperparameters used

| Parameter | What it controls | Effect of increasing |
|---|---|---|
| `max_depth` | maximum tree depth | more interaction capacity, more overfit risk |
| `eta` | learning-rate shrinkage | smaller values are more conservative |
| `subsample` | row fraction per tree | lower values add randomness and regularization |
| `colsample_bytree` | feature fraction per tree | lower values reduce reliance on any one predictor |
| `min_child_weight` | minimum child-node hessian/weight | higher values make splits harder |
| `gamma` | minimum loss reduction for a split | higher values make the tree more conservative |
| `reg_lambda` | L2 penalty on leaf weights | higher values shrink leaf scores |

The final Optuna parameters were:

```text
max_depth=5
eta=0.15886862017758807
subsample=0.9978285954459796
colsample_bytree=0.7542674629502206
reg_lambda=2.8864523836452007
min_child_weight=7
gamma=0.46965238775400736
```

## Validation design

The code uses `TimeSeriesSplit` inside the training window for tuning. scikit-learn documents this as a time-series version of k-fold where successive training sets are supersets of earlier ones. That is the right direction for time series because future rows cannot train past forecasts.

Source: [scikit-learn Time Series Split docs](https://scikit-learn.org/stable/modules/cross_validation.html#time-series-split).

Final training uses train 2005-2016 and validation 2017-2019 for early stopping. XGBoost documents `early_stopping_rounds` as requiring validation improvement within the specified number of rounds.

Source: [XGBoost Python API docs](https://xgboost.readthedocs.io/en/stable/python/python_api.html#xgboost.train).

## Three-pass tuning

| Pass | Output | Best observed CV RMSE |
|---|---|---:|
| Manual grid | `outputs/tables/xgb_pass1_manual.csv` | 0.01403 |
| Random search | `outputs/tables/xgb_pass2_random.csv` | 0.01382 |
| Optuna | `outputs/tables/xgb_pass3_optuna.csv` | 0.01383 |

The random and Optuna passes both preferred conservative models. The final trained model had no splits.

## Importance methods

The repo reports:

1. Native gain.
2. Native weight.
3. Native cover.
4. Permutation importance.
5. SHAP TreeExplainer.

SHAP TreeExplainer is designed for tree models and returns per-feature contribution values for each observation. In this project, those contributions are zero because the final booster does not split on any feature.

Source: [SHAP TreeExplainer docs](https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html).

## Self-check answers

1. Gradient boosting adds trees sequentially to reduce the current loss.
2. `max_depth`, `eta`, `subsample`, `colsample_bytree`, `min_child_weight`, `gamma`, and `reg_lambda` control capacity and regularization.
3. Early stopping needs validation data because stopping on test data would leak final evaluation information.
4. Gain measures split loss reduction inside the trained trees. SHAP measures per-observation feature contributions. Here both are zero because there are no splits.
5. Random k-fold is wrong for FX time series because it lets future observations influence training folds for earlier observations.

## Stage 3 readout

The final XGBoost result is economically useful because it refuses to manufacture nonlinear structure. It gets a tiny RMSE improvement over random walk, but it does so as an intercept-only model. The correct interpretation is weak conditional mean signal at the 1-week horizon.
