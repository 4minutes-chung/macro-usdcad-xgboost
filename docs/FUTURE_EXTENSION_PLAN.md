# Future Extension Plan

Status: adopted future research direction; implementation deferred. This document authorizes no implementation inside the current archived project.

## Decision

The weekly USD/CAD direction study is frozen as a disciplined negative forecasting result. Logistic and Elastic Net show small numerical gains, but the gains are statistically unresolved and unstable. XGBoost tuning does not solve the weak-signal problem.

The adopted future economics paper is the monetary-policy announcement event study below. Its paper identity, estimand and feasibility gate are approved as the future direction, but no data collection or implementation is active.

The methodological lesson is not that gradient boosting is bad. The lesson is that next-week FX direction, using a small weekly public-information dataset, is a poor setting for learning the advantages of gradient boosting.

Future work is split into two separate possible projects:

1. A monetary-policy announcement event study for the economics question.
2. A new gradient-boosting project with a better-suited tabular prediction problem.

Neither project is an extension of the current test set. Do not add either to this repository without an explicit decision to reopen the project.

## Paper Identity

The future monetary-policy paper must not become a model-comparison paper.

Its organizing question is economic:

> How does USD/CAD respond when unexpected BoC or Fed policy information arrives?

Non-negotiable rules:

1. Use one primary estimand and one primary event-study estimator.
2. Treat alternative windows and inference methods as robustness checks, not competing models.
3. Do not organize the title, abstract or main results around Logistic, Elastic Net or XGBoost.
4. Use the current weekly forecasting null only as motivation for studying information arrival, or place it in an appendix.
5. Do not add XGBoost to the event study merely to create a machine-learning section.
6. Keep the separate gradient-boosting methodology project in another repository and another paper.

The paper contribution should be a measured economic response to identified policy news, not an algorithm ranking.

## A. Monetary-Policy Event Study

### Research question

How does USD/CAD respond when the Bank of Canada or Federal Reserve delivers unexpected monetary-policy news?

This replaces stale weekly predictors with new information arriving at a known announcement time.

### Estimand

Estimate BoC and Fed events separately:

```text
FX return over event window
    = intercept
    + beta_CA * unexpected BoC policy news
    + beta_US * unexpected Fed policy news
    + error
```

USD/CAD is Canadian dollars per US dollar. A hawkish BoC surprise should lower USD/CAD, while a hawkish Fed surprise should raise USD/CAD.

The target parameter is the event-window change in log USD/CAD per one-basis-point unexpected policy shock. It is not a forecast hit rate.

### Required data

1. Exact BoC and Fed announcement dates, times and time zones.
2. A defensible pre-announcement market expectation from OIS or interest-rate futures.
3. Timestamped intraday USD/CAD bid and ask prices, or a reliable midpoint series.
4. A calendar of overlapping CPI, employment and other major announcements.
5. Documentation of licensing and redistribution limits.

Do not define a surprise as the announced rate minus the previous rate. That measures the policy change, not the unexpected component.

### Feasibility gate

Allow one 5-8 hour feasibility block only after higher-priority portfolio work is complete.

Proceed only if all conditions pass:

1. Surprise data are public, reproducible and legally usable.
2. Intraday FX timestamps can be synchronized with announcement times.
3. Clean events remain after removing overlapping releases and data failures.
4. A prospective precision calculation shows that the sample can identify an economically meaningful response.
5. Target-rate and forward-guidance surprises can be separated, or the limitation can be stated without a causal overclaim.

If any condition fails, stop. Do not replace missing surprise data with realized rate changes.

### Design

1. Pre-specify a primary event window, such as 10 minutes before to 30 minutes after the announcement.
2. Estimate BoC and Fed responses separately before considering a pooled model.
3. Use event-level OLS with HC3 standard errors.
4. Add small-sample wild-bootstrap or randomization inference.
5. Test a wider event window only as a declared robustness check.
6. Run pre-event placebo windows to detect anticipation or timestamp errors.
7. Report crisis and overlapping-news exclusions transparently.

### Identification assumptions

1. The market-based surprise captures information not known immediately before the announcement.
2. No other major news systematically arrives inside the event window.
3. FX prices and announcement timestamps are correctly synchronized.
4. Anticipatory trading does not fully absorb the surprise before the event.
5. Central-bank information effects and forward guidance are separated or explicitly included as limitations.

### Main threats

1. Noisy or unavailable public expectation data.
2. Too few independent events for precise inference.
3. Simultaneous macroeconomic releases.
4. Multiple dimensions of policy communication.
5. Intraday bid-ask noise and timezone mistakes.
6. Post-selection from trying several windows or surprise definitions.

### Deliverables

1. Event and exclusion ledger.
2. Data-feasibility memo.
3. Pre-analysis specification with one primary window and estimand.
4. Event-level regression table with effect sizes and confidence intervals.
5. Event-time response figure and placebo diagnostics.
6. Limitations section separating association from causal identification.

## B. Future Gradient-Boosting Methodology Project

### Purpose

Learn gradient boosting on a problem where nonlinear splits and interactions have a credible role. Do not force XGBoost onto another weak financial-return direction target.

This is a separate methodology project. It must not be merged into the monetary-policy event-study paper.

### Topic-selection gate

A candidate topic must satisfy all conditions:

1. Tabular data contain thousands of observations or meaningful cross-sectional variation.
2. The target has a plausible and measurable signal.
3. Economic reasoning supports thresholds, interactions or nonlinear marginal effects.
4. Observations can be separated with a credible time, group or entity holdout.
5. Logistic, Elastic Net or another simple model provides a serious benchmark.
6. The target, split and primary metric are fixed before tuning.
7. Probability calibration and decision costs matter, not accuracy alone.

Preferred topic families are loan-level credit risk, delinquency or default prediction, large-move or volatility risk as a separate project, and other high-observation tabular economic datasets. Topic choice requires a separate data audit.

### Methodology-learning objectives

1. Build a leakage-safe time or group validation design.
2. Compare Logistic, Elastic Net and gradient boosting on identical folds.
3. Tune tree depth, learning rate, minimum child weight and regularization inside training data only.
4. Evaluate calibration, Brier score, log loss and decision-relevant errors.
5. Use learning curves to determine whether model performance is sample-limited.
6. Compare gain, permutation importance and SHAP without treating importance as causality.
7. Test stability across time, entities and economically meaningful regimes.

### Kill rules

Stop if any condition holds:

1. The dataset is too small to estimate stable nonlinear structure.
2. The target is changed after seeing weak results.
3. Validation requires random splitting of dependent observations.
4. Gradient boosting wins only under one unstable threshold or sample period.
5. The project duplicates an existing portfolio project without adding a new question or skill.

## Sequence

1. Keep the current USD/CAD project frozen.
2. Complete higher-priority active portfolio work.
3. If monetary-policy transmission remains important, run only the event-study feasibility gate.
4. If the goal is gradient-boosting methodology, select a separate high-observation tabular dataset instead.
5. Do not run both future projects simultaneously.

## Current Project Claim

Public weekly macro-financial information did not deliver statistically reliable or specification-stable improvements over base-rate USD/CAD direction forecasts. This is evidence about the tested forecasting design, not evidence that monetary policy has no exchange-rate effect.
