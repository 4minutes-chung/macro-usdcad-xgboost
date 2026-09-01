# Research Plan

Pre-registered hypotheses, expected results, and robustness checks. Organized by stage. Each stage stands alone with its own gates.

---

## Stage 1: Descriptive macro-finance

**Question.** What are the empirical relationships between USD/CAD and (a) WTI returns, (b) Canada-US 2Y and 10Y yield spreads, (c) VIX, (d) a U.S. equity-risk proxy, over 2005-2026?

**Data-source note.** FRED's `SP500` daily history is source-limited to roughly 10 years under current licensing notes. The primary full-sample equity-risk feature is therefore `NASDAQCOM` (`r_equity`). `SP500` remains in raw data only as a recent-sample reference.

**Pre-registered observations (sign expectations):**

- D1: WTI returns and USD/CAD returns negatively correlated (oil up → CAD up → USD/CAD down). Expected ρ in [-0.4, -0.1].
- D2: CA-US 2Y spread negatively correlated with USD/CAD (wider spread → CAD demand → USD/CAD down). Sign expectation weak (UIP failures).
- D3: VIX and USD/CAD positively correlated (risk-off → USD up). Expected ρ in [0.1, 0.4].
- D4: Rolling 26-week correlation between oil returns and USD/CAD returns will be unstable, weakening post-2015.

**Stage 1 success criterion:** Charts, summary statistics, and a 4-page write-up identifying where each relationship holds and where it breaks. Not contingent on any model winning.

---

## Stage 2: Benchmark forecasting

**Hypotheses for the linear forecasting layer:**

- H2.1: Ridge with all 12 features achieves OOS R² > 0 against random walk on the test period (2020-2026). Expected magnitude: -1% to +2% per Rossi (2013).
- H2.2: AR(1) does not meaningfully outperform random walk on RMSE. Expected: AR(1) OOS R² ≈ 0.
- H2.3: Ridge coefficient signs align with macro priors for at least 2 of 3 key factors (oil, 2Y spread, VIX).

**Null hypothesis (Meese-Rogoff):** No model beats random walk on RMSE or directional accuracy at 1-week horizon.

**Stage 2 success criterion:** Benchmark table saved, Ridge coefficient signs interpreted economically, null result reported honestly if observed. Stage 2 is NOT contingent on Ridge winning; a clean null is a real contribution.

---

## Stage 3: XGBoost depth

**Hypotheses for the nonlinear forecasting and interpretation layer:**

- H3.1: XGBoost OOS R² ≥ Ridge OOS R² on the full test period.
- H3.2: XGBoost gain-based feature importance puts at least one factor block (oil, rates, risk) in top-3.
- H3.3: Three importance methods (gain, weight, cover) will partially disagree. Disagreement is informative, not a bug.
- H3.4: Permutation importance and SHAP will broadly agree on the top-2 features but may disagree on rank.
- H3.5: XGBoost beats Ridge by larger margin in high-VIX subperiods than low-VIX subperiods (regime nonlinearity hypothesis).
- H3.6: Pre-2020 vs post-2020 test subperiod will show different dominant features.

**Pre-registered expected results:**

| Quantity | Expected range | Suspicious if |
|---|---|---|
| XGBoost OOS R² | -1% to +3% | > 5% (re-check look-ahead) |
| Directional accuracy | 50% to 55% | > 56% (re-check leakage) |
| Top feature (gain) | rate spread, VIX change, or lagged FX | oil only (post-2015 weakness in BoC SAN 2024-20) |
| Regime difference | high-VIX dir-acc 2-4pp higher than low-VIX | reverse direction |

**Stage 3 success criterion:** XGBoost performance reported honestly. Three importance methods reported jointly. Permutation importance added (was missing in v1 plan). SHAP plot saved. Regime tables saved. `findings.md` written.

---

## Stage 4 (optional): Local Projection / IRF

**Hypotheses for the dynamic-response layer:**

- H4.1: A unit positive WTI return shock predicts a negative USD/CAD response that peaks at 1-2 weeks and decays by 8 weeks. Expected magnitude small (5-15 bp).
- H4.2: A unit positive Canada-US 2Y spread shock predicts a negative USD/CAD response, peak at 0-2 weeks. Sign expectation weaker than H4.1 (UIP failures).
- H4.3: A unit positive VIX shock predicts a positive USD/CAD response (USD strength in risk-off), peak at 0-1 weeks. Expected magnitude small but precisely estimated.
- H4.4: At least one IRF confidence band will exclude zero at some horizon, or none will (null result acceptable).

**Identification strategy:** Shocks defined as innovations from AR(1) on each driver in v1 (simple internal instrument). Acknowledge identification weakness in writeup. External instruments (Killian 2009 oil supply shocks, Romer-Romer monetary surprises) noted as v2 extension if data accessible.

**Stage 4 success criterion:** Three IRF plots with Newey-West confidence bands. Horizon 0-12 weeks. Economic interpretation per IRF. Identification weakness explicitly declared.

---

## Cross-stage methodology

**Validation discipline (applies to Stages 2, 3, 4):**

- Train: 2005-2016. Validation: 2017-2019. Test: 2020-2026.
- Walk-forward expanding window for hyperparameter tuning in Stage 3.
- Test set is sacred: touched once at the end of each stage.
- LP estimation uses full available sample, but acknowledges in-sample nature distinct from forecast-evaluation framing.

**Look-ahead bias:** All features observable at time t. Target shifted forward by 1 week. Alignment test in code.

**Robustness checks (run if primary results hold):**

1. Alternative start date (2010 instead of 2005).
2. Alternative train/val/test split (train through 2018, test 2019-2026).
3. Drop-one-feature ablation in Stage 3.
4. Pre-COVID-only test subsample (2020 omitted).
5. Equal-weighted Ridge + XGBoost ensemble.

**Limitations declared upfront:**

1. 1-week horizon is among the hardest in FX.
2. Sample size limited by weekly resampling (~1,100 obs).
3. No transaction costs modelled. Not a trading strategy.
4. Single currency pair, no cross-validation against AUD/USD or NOK/USD.
5. Test period covers COVID + inflation shock, which may be atypical.
6. LP identification in Stage 4 is weak (internal instrument); contribution is descriptive dynamic association, not causal claim.
7. No Diebold-Mariano or Clark-West test of forecast accuracy in v1.

**Decision rules at each stage gate:**

- **Strong result at Stage N:** continue to Stage N+1 if marginal hour pays.
- **Null result at Stage N:** ship the null honestly; the methodology is the contribution.
- **Suspicious result (OOS R² > 5%, dir-acc > 56%):** halt, re-check data leakage, do not advance.

---

## Falsifiability

The entire study is falsifiable. If random walk dominates across every stage, the paper-equivalent contribution is:

> A staged, properly-validated empirical test that the canonical three-factor framework for CAD does not generate exploitable 1-week-ahead forecasts after benchmark discipline. Linear and nonlinear models agree with the Meese-Rogoff baseline at this horizon. LP shock responses, if estimated, are economically small and statistically borderline.

That is a real contribution.
