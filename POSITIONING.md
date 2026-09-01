# Positioning

How this project is marketed across lanes, with the stage-gated structure in mind. The same work, told differently for different audiences, with stop points that match each audience's expectations.

Hard wrap 2026-07-31: CLOSED-ARCHIVED. Numbers below are locked.

## P11A claim bullets (paste-ready)

1. Built a walk-forward USD/CAD study (FRED + BoC, 2005-2026) testing oil, Canada-US spreads, and risk sentiment against random walk, AR(1), Ridge, and tuned XGBoost; random walk wins on RMSE and XGBoost collapses to intercept-only (`OOS R² ≈ 0.00031`, no tree splits).
2. Reported four importance methods plus SHAP; all zero because the selected model made no splits; direction-classification gains remain HAC-unresolved, so no edge claim.
3. Optional local projections show prior-consistent horizon-0 signs with weak AR(1)-innovation identification; framed as descriptive association, not causal IRFs. Not a trading model.

If you cannot defend the current state in 90 seconds, the project is incomplete regardless of what's in the repo.

---

## The honest one-liner (full version)

> A staged study of how oil prices, Canada-US interest-rate differentials, and global risk sentiment relate to USD/CAD over 2005-2026, with random-walk and Ridge benchmarks, XGBoost forecasting, and optional local-projection shock analysis.

That sentence is true at every stop point, just with progressively more of it.

## Per-stage one-liners

- **After Stage 1:** "An empirical descriptive study of macro-financial drivers of USD/CAD across 2005-2026."
- **After Stage 2:** "An empirical study of macro-financial drivers of USD/CAD, with a benchmark forecasting evaluation under walk-forward validation."
- **After Stage 3:** "A macro-financial forecasting and interpretation study of USD/CAD using disciplined benchmarks and a deeply-tuned XGBoost."
- **After Stage 4:** "A macro-financial forecasting, interpretation, and dynamic-response study of USD/CAD combining XGBoost with local-projection shock analysis."

---

## Resume bullet (calibrated to stop point)

**After Stage 1:**

> USD/CAD Macro-Finance Study (Python): Empirical analysis of oil, Canada-US yield spreads, and risk sentiment as drivers of USD/CAD across 2005-2026; produced rolling-correlation figures, regime-conditional charts, and a written interpretation note.

**After Stage 3:**

> USD/CAD Macro-Financial Forecasting Study (Python, XGBoost, BoC + FRED data): Tested whether oil, Canada-US yield spreads, and risk sentiment improve 1-week forecasts beyond random-walk and Ridge benchmarks; ran three-pass hyperparameter tuning under walk-forward CV; reported gain, weight, cover, permutation importance, and SHAP; analyzed pre/post-2020 and high/low-VIX regimes.

**After Stage 4:**

> Add a second line: ... and estimated local-projection impulse responses of USD/CAD to shocks in oil, yield spreads, and VIX, with Newey-West confidence bands across 12-week horizons.

---

## LinkedIn project description (Stage 3 ship)

> Empirical FX forecasting study: tested the explanatory power of oil prices, Canada-US 2Y and 10Y yield spreads, and risk sentiment (VIX) for 1-week-ahead USD/CAD returns. Benchmarks: random walk, AR(1), Ridge. Flagship model: XGBoost with manual grid → random search → Optuna Bayesian tuning under walk-forward expanding-window CV. Interpretation via gain/weight/cover, permutation importance, and SHAP TreeExplainer, with regime-conditional analysis across pre/post-2020 and high/low-VIX subperiods. Framework grounded in Rossi (2013) on FX predictability and Bank of Canada Staff Analytical Note 2024-20 on currency factors.

After Stage 4, append:

> Extended with local-projection impulse-response analysis (Jordà 2005) of USD/CAD response to oil, yield-spread, and VIX shocks across 12-week horizons.

---

## The 90-second interview version (Stage 3 ship)

> I built a forecasting study on USD/CAD, motivated by the Bank of Canada's recent staff analytical note on the three global currency factors. The hypothesis was that oil prices, Canada-US rate differentials, and global risk sentiment should add forecasting value beyond a simple random walk at one-week horizon.

> I built the pipeline in Python with FRED and BoC Valet data, validated everything with walk-forward expanding-window cross-validation to avoid look-ahead bias, and benchmarked against random walk, AR(1), and Ridge before bringing in XGBoost. The XGBoost stage I deliberately structured in three passes: manual grid first to build intuition, random search next, Optuna Bayesian last. I report feature importance four ways: gain, weight, cover, permutation importance, and SHAP. Permutation importance matters because it's the only one that directly measures predictive contribution rather than how often a feature was used.

> The honest result is that random walk still wins on RMSE. Tuned XGBoost posts only OOS R² of about 0.00031 versus random walk, directional accuracy is essentially 50%, and the final tree makes no splits, so gain, weight, cover, permutation importance, and SHAP are all zero. A focused direction-classification extension shows small one-week numerical gains that are statistically unresolved under HAC, so I do not claim an edge. I interpret this as Meese-Rogoff still binding at the one-week horizon: the macro factors are sensible contemporaneously, but they do not deliver stable short-horizon forecast value under walk-forward discipline. The contribution is the empirical discipline and the honest null, not a forecasting win.

If Stage 4 shipped, add 20 seconds:

> I extended this with a local-projection analysis. At horizon 0 the signs match priors: a WTI shock and a wider CA-US 2Y spread lower USD/CAD, and a VIX shock raises it. LP identification is weak because I use AR(1) innovations as the internal shock, so I frame the results as descriptive dynamic associations, not causal IRFs.

Practice with a stopwatch.

---

## The 30-second coffee chat version (any stage)

> I shipped a staged USD/CAD study testing whether oil, rate differentials, and risk sentiment beat random-walk and Ridge benchmarks one week ahead. Motivation is the BoC three-factor framework. Under walk-forward CV, the honest result is a null: XGBoost collapses to intercept-only. The point is disciplined validation in a low-signal FX setting, not a trading edge.

---

## Lane-specific framing

Same project, different emphasis depending on audience.

### For FX research / macro research roles

Lead with the **research design** and **factor framework**.

- The three-factor framework (USD, carry, oil) maps directly to BoC SAN 2024-20.
- Rossi 2013 humility frame is built in.
- Walk-forward CV is the right validation for any FX forecasting claim.
- Regime analysis is the right way to read FX in 2020-2026.
- If Stage 4 shipped: LP shock-response is genuine econometric depth.

**Signal:** you read the FX literature, you respect Meese-Rogoff, you don't oversell.

### For credit risk / model validation roles (Fitch)

Lead with the **modeling discipline** and **interpretation rigor**.

- Three-pass hyperparameter tuning shows you tune deliberately.
- Walk-forward CV is standard for time-series credit models.
- Four feature importance methods reported jointly (gain, weight, cover, permutation) plus SHAP is what model validators want.
- Regime analysis is stress-testing.
- Honest negative-or-mixed result shows you don't overfit your story.

**Signal:** you can validate, not just build. You understand ML failure modes in finance.

### For data science / ML engineering roles

Lead with the **technical depth**.

- Direct CSV pull from FRED, no premium data dependencies.
- Reusable `src/` modules.
- Look-ahead bias check baked into tests.
- Optuna with TPE sampler.
- SHAP TreeExplainer for explainability.
- Permutation importance for honest feature ranking.
- Clean repo, reproducible.

**Signal:** you ship clean code, you know modern tooling.

### For applied economist / economic consulting roles

Lead with the **empirical economics framing**, especially if Stage 4 is shipped.

- Research question is economic, not technical.
- Factor blocks correspond to identifiable theoretical channels.
- Validation discipline (walk-forward, OOS R²) is the same standard causal-inference economists use for forecasting.
- LP/IRF (Stage 4) is the modern econometric tool for dynamic response.
- Limitations are part of the contribution.

**Signal:** you think like an economist who uses ML, not an ML practitioner who touches macro data.

---

## What NOT to claim

1. **Do not say the model can be used for trading.**
2. **Do not say "my model beats the benchmark"** without the specific OOS R² and confidence statement.
3. **Do not overstate ML novelty.** XGBoost is a 2016 tool. The novelty is disciplined application to a noisy small-sample domain.
4. **Do not say "AI helped me build this."** Say what you decided, validated, and verified.
5. **Do not hide the negative result.** A clean null is more credible.
6. **Do not claim causal interpretation** of Stage 4 IRFs. Use "dynamic association" or "descriptive response" if identification is weak.

---

## Defensive answers (interview)

> **Q: Did the model beat the benchmark?**
> A: No. Random walk wins RMSE. Tuned XGBoost OOS R² versus random walk is 0.00031, directional accuracy is 0.49847, and the final tree made no splits. That is consistent with FX predictability literature at this horizon (Rossi 2013). Regime tables do not rescue it: high VIX has worse direction than low VIX, and both oil-vol splits have tiny OOS R².

> **Q: Why XGBoost over neural networks?**
> A: Sample size. ~1,000 weekly observations is the regime where tree ensembles beat neural networks, per Gu, Kelly, Xiu (2020). Tree-based methods also give interpretable feature importance, which matters for a macro story.

> **Q: How did you validate?**
> A: Walk-forward expanding-window CV inside training for hyperparameter tuning. Held-out validation set for early stopping. Test set touched once at the end. Never random k-fold.

> **Q: How did you handle feature importance?**
> A: Reported four ways plus SHAP: gain, weight, cover, and permutation. In this project they all returned zero because the selected model made no splits. Permutation importance is the method I would trust when trees actually split; here the agreement at zero is the result.

> **Q: Why did the model make no splits?**
> A: XGBoost is allowed to say no split is worth it. That is what happened. The final model has one terminal node and no feature splits. Conservative tuning preferred intercept-only, so all importance methods are zero. That is a finding about weak 1-week signal, not a coding bug.

> **Q: How did you avoid look-ahead bias?**
> A: Every feature constructed from data observable at time t. Target shifted forward by one week. Explicit alignment test confirming y[t] equals next-period return.

> **Q (Stage 4): What's the identification in the LP?**
> A: Weak in this version. Shocks are AR(1) innovations as internal instruments, not external. I frame the IRFs as descriptive dynamic associations, not causal impulse responses. Stronger identification would be a separate project, not a v2 of this archive.

> **Q: What did you learn?**
> A: Three things. Disciplined benchmarks change the story: random walk still wins. Conservative XGBoost can refuse to split, and that is a valid result. Regime tables did not rescue the 1-week null.

> **Q: What would you do differently?**
> A: I already ran 4-week direction. The historical base rate beat every learned model on Brier and log loss, so longer weekly horizons did not help. I would not keep horse-racing weekly forecasts. If I continued, it would be a separate identified-news paper with new data rights, not another model in this archive. Stage 4 identification stays weak (AR(1) innovations) and stays descriptive.

---

## The "single best signal" rule

If you could highlight only ONE thing in any conversation, it is:

> I built the three-pass tuning structure so I would learn what each hyperparameter does, not just optimize blindly. On the manual grid, learning rate moved CV RMSE about five to six times more than max_depth, and depth was non-monotonic. The selected model is intercept-only: no splits, so the later Optuna depth and subsample values did not bind. The honest headline is the null, not the knobs.

That sentence signals: you tune thoughtfully, you can verbalize what you did, you understand the model.

If Stage 4 shipped, the second-best signal is:

> I report four feature importance methods plus SHAP because they often disagree. Here they all agree at zero, which is the informative part: the tree never split.
