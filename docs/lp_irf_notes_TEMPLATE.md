# Local Projection / IRF Notes (Stage 4 Deliverable)

Fill in after reading Jorda (2005) plus your prior LP-IV notes from the Lucas neutrality project.

This is the learning artifact for Stage 4. Optional. Only start after Stages 1-3 are shipped.

---

## 1. What is Local Projection?

(In your own words. How does Jorda (2005) define LP? What is the key insight that distinguishes it from VAR-based IRFs?)

## 2. The LP regression at horizon h

Write the regression in your own notation:

$$ y_{t+h} = \alpha_h + \beta_h \cdot shock_t + \gamma_h' x_t + \varepsilon_{t,h} $$

What does $\beta_h$ represent? Why does estimating one regression per horizon (rather than iterating a VAR) make the impulse response more robust to misspecification?

## 3. Identification

What is a "shock" in this study? Options ranked by identification strength:

1. (Weakest) AR(1) innovations as internal instrument. Used in v1.
2. (Medium) Cholesky ordering in a small VAR, extract the orthogonalized shock.
3. (Stronger) External instrument (Killian 2009 oil supply shocks, Romer-Romer monetary surprises, FOMC announcement surprises).
4. (Strongest) Natural experiment.

What identification does this study use? What is the cost of that choice?

## 4. Newey-West standard errors

Why use HAC standard errors instead of OLS standard errors in LP? What lag length is appropriate? (Rule of thumb: 4 * (T/100)^(2/9).)

## 5. Reading the IRF plot

Each chart shows:
- x-axis: horizon in weeks (0 to 12)
- y-axis: cumulative response of USD/CAD log return per unit shock
- shaded band: 95% Newey-West confidence interval
- horizontal line at zero: null of no response

What does it mean if the band excludes zero at horizon h?

## 6. Three IRFs in this study

### 6.1 Response to WTI return shock
- Sign expectation: negative (oil up -> CAD up -> USD/CAD down).
- Peak expected at horizon 1-2 weeks.
- Decay expected by horizon 8 weeks.
- Magnitude expected small (5-15 bp per unit oil shock).

(Fill in actual results after running.)

### 6.2 Response to CA-US 2Y spread shock
- Sign expectation: negative under capital-flow story, positive under UIP.
- Empirical literature: mixed; UIP failures common.

(Fill in actual results.)

### 6.3 Response to VIX change shock
- Sign expectation: positive (risk-off -> USD strength -> USD/CAD up).
- Peak expected at horizon 0-1 weeks (fast response).

(Fill in actual results.)

## 7. Connection to forecasting results (Stage 3)

If XGBoost found feature X important for forecasting, does the LP IRF for shock to X show a precisely-estimated dynamic response? If yes: consistent story. If no: features matter for prediction but not for dynamic interpretation, which is an interesting discrepancy.

## 8. Limitations declared

1. Internal-instrument shocks have weak identification. Results are descriptive associations, not causal impulse responses.
2. Sample size limits how far horizons can extend.
3. Regime instability: pre-2020 and post-2020 may show different IRFs. Consider sub-sample LPs.
4. Single-equation LP cannot capture full system dynamics. A VAR would, at the cost of more assumptions.

## 9. Self-check before Stage 4 ship

Answer without notes:

1. Why does LP estimate one regression per horizon rather than iterating?
2. What identification strategy did you use? Why is it weak?
3. What is Newey-West correcting for, and what lag length did you pick?
4. Which IRF (if any) showed a confidence band excluding zero at any horizon?
5. Are the IRF signs consistent with the Ridge coefficient signs from Stage 2c?

If you cannot answer all five, the Stage 4 writeup is not done.

---

## Reading log

| Item | Date | Time | Take-away |
|---|---|---|---|
| Jorda (2005) | | | |
| Prior LP-IV notes (Lucas project) | | | |
