# XGBoost Notes (Stage 3 Prerequisite Reading Deliverable)

Fill in after reading Chen & Guestrin 2016, the XGBoost parameter docs, and the sklearn CV docs.

This is the learning artifact. If you can answer every prompt below without re-reading, you have actually learned XGBoost. If not, re-read.

---

## 1. Gradient boosting intuition

(In your own words: how does boosting build an ensemble of trees? What is being minimized at each step? Why is each new tree fit to residuals or pseudo-residuals?)

## 2. The regularized objective (Chen & Guestrin 2016, Section 2)

Write the objective:

$$ \mathcal{L} = \sum_i l(y_i, \hat{y}_i) + \sum_k \Omega(f_k) $$

What does Ω(f) include? Why is the regularization term innovative compared to traditional gradient boosting?

## 3. Hyperparameter table

| Parameter | What it controls | Typical range | Effect of increasing |
|---|---|---|---|
| `max_depth` | tree depth | 2-10 | more capacity, more overfit risk |
| `eta` (learning_rate) | shrinkage per tree | 0.01-0.3 | slower learning, often better generalization at low values |
| `n_estimators` / `num_boost_round` | | | |
| `subsample` | | | |
| `colsample_bytree` | | | |
| `min_child_weight` | | | |
| `gamma` | | | |
| `reg_lambda` (L2) | | | |
| `reg_alpha` (L1) | | | |

(Fill in the gaps from the XGBoost parameter docs.)

## 4. Early stopping

What is it? How does it work in XGBoost? Why do you need a validation set distinct from the test set?

## 5. Feature importance methods

| Method | What it measures | When to use |
|---|---|---|
| `gain` | Average improvement in loss from splits using this feature | Default report. Misleading if features are correlated. |
| `weight` | Number of times feature is used as a split | Low-information; cardinality-biased. |
| `cover` | Number of observations affected by splits on this feature | Useful as cross-check. |
| **Permutation importance** | Drop in performance when feature values are shuffled | Best objective measure of predictive contribution. Run on held-out data. |
| SHAP | Per-prediction marginal contribution | Per-observation insight. Best for interpretation, not ranking. |

Why is `gain` the most commonly reported but also potentially misleading? (Answer: it rewards features used in many trees regardless of whether they actually help out-of-sample. Correlated features can split the gain artificially.)

Why is permutation importance preferred for honest reporting? (Answer: it directly measures the performance cost of removing a feature's information. Robust to correlation. Run on the validation or test set after the model is fit.)

When does SHAP add value beyond permutation importance? (Answer: when you need to explain individual predictions, see direction of effect, or check whether the model uses features in economically sensible ways.)

## 6. Time-series cross-validation

Why is random k-fold wrong for time series? Explain in one paragraph using the look-ahead-bias framing.

What does `TimeSeriesSplit` do? Draw the train/test split diagram.

What is walk-forward CV? How is it different from `TimeSeriesSplit`?

## 7. Monotonic constraints

What are they? When would you use them in a finance context? (Hint: when you have strong prior beliefs about the sign of a relationship.)

## 8. Three-pass tuning rationale

Why do all three passes (manual, random, Optuna) instead of skipping to Optuna?

- Manual: ___
- Random: ___
- Optuna: ___

---

## Self-check before Stage 3b (tuning)

Answer without notes:

1. Explain gradient boosting in 2 minutes.
2. Name 5 hyperparameters and what each does.
3. Why does early stopping require a validation set?
4. What is the difference between `gain` and SHAP for feature importance?
5. Why is `TimeSeriesSplit` necessary instead of random k-fold for FX data?

If you cannot answer all five, do not start Stage 3b (tuning).
