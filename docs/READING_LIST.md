# Reading List

Reading order matches project phases. Tier 1 is mandatory before the corresponding phase; Tier 2 is read during or after model runs.

---

## Stage 1 Prerequisite: FX Domain (Tier 1, must read first)

### 1. Rossi (2013), "Exchange Rate Predictability"
- **Citation:** Rossi, B. (2013). Exchange Rate Predictability. *Journal of Economic Literature*, 51(4), 1063-1119.
- **Why:** The comprehensive survey. Establishes that FX predictability depends on predictor, horizon, sample, model, and evaluation method. This is the humility frame you must internalize before building anything.
- **Open access:** Working paper version on Rossi's website at Duke / ICREA. Also available via JEL (institutional access).
- **Read order:** Abstract, Introduction, Section 2 (predictors), Section 6 (conclusion). Full paper if time allows.
- **Time budget:** 1.5-2h
- **Take-away you must write down:** Why is the random walk such a tough benchmark? What does "predictability" actually mean in FX?

### 2. Bank of Canada Staff Analytical Note 2024-20: "Foreign exchange risk premiums and global currency factors"
- **Citation:** Bank of Canada Staff Analytical Note No. 2024-20 (July 2024).
- **URL:** https://www.bankofcanada.ca/2024/07/staff-analytical-note-2024-20/
- **Why:** This is the canonical recent BoC paper that constructs the three-factor framework for currency dynamics: (1) US dollar factor (broad USD exposure), (2) carry factor (cross-country interest-rate differentials), (3) oil factor (commodity-currency channel). This directly justifies your factor block design.
- **Open access:** Yes, free on bankofcanada.ca.
- **Read order:** Full note. Pay attention to the three-factor construction and the time-varying coefficient charts (rolling 252-day windows).
- **Time budget:** 1h
- **Take-away:** Write each of the three factors in your own words and note which has the largest coefficient on CAD historically.

### 2b. Bank of Canada Staff Analytical Note 2025-2: "Monetary policy, interest rates and the Canadian dollar"
- **Citation:** Fontaine, J.-S., Krohn, I., Kyeong, J., Vala, R., and Zmitrowicz, K. (February 2025). Bank of Canada Staff Analytical Note No. 2025-2.
- **URL:** https://www.bankofcanada.ca/2025/02/staff-analytical-note-2025-2/
- **Why:** Most recent BoC piece focused specifically on how interest-rate differentials and FX risk premium affect CAD. Useful pairing with SAN 2024-20.
- **Open access:** Yes.
- **Read order:** Skim. Focus on the regression tables showing CAD return sensitivity to rate differential and risk premium.
- **Time budget:** 30min
- **Take-away:** What share of recent CAD depreciation does the rate differential explain vs the risk premium?

### 3. Meese & Rogoff (1983), "Empirical exchange rate models of the seventies"
- **Citation:** Meese, R. A., & Rogoff, K. (1983). Empirical exchange rate models of the seventies: Do they fit out of sample? *Journal of International Economics*, 14(1-2), 3-24.
- **Why:** Foundational result that structural FX models fail to beat the random walk out of sample. The reason every FX paper since 1983 cites Meese-Rogoff.
- **Open access:** Available via institutional access; abstract is free.
- **Read order:** Abstract + Introduction only. The methodology is dated; you only need the headline result.
- **Time budget:** 30min
- **Take-away:** One sentence on why this paper matters.

### 4. Engel (2014), "Exchange Rates and Interest Parity"
- **Citation:** Engel, C. (2014). Exchange Rates and Interest Parity. *Handbook of International Economics*, Vol. 4, Ch. 8. NBER WP 19336.
- **Why:** Survey of UIP and carry trade. Covers why interest-rate differentials matter for FX and why UIP fails empirically (which is exactly the puzzle your rate-spread features sit inside).
- **Open access:** NBER WP 19336 free on nber.org.
- **Read order:** Section on UIP failures + carry trade. Skip the heavy theory.
- **Time budget:** 1.5h
- **Take-away:** Why does the CA-US rate spread potentially predict USD/CAD? What does the failure of UIP imply about predictability?

---

## Stage 3 Prerequisite: XGBoost Depth (Tier 1, must read before tuning)

### 5. Chen & Guestrin (2016), "XGBoost: A Scalable Tree Boosting System"
- **Citation:** Chen, T., & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. *Proceedings of the 22nd ACM SIGKDD*, 785-794.
- **Why:** The original paper. Gives the actual mathematics of regularized gradient boosting. You cannot understand XGBoost without this.
- **Open access:** Yes, on arXiv (1603.02754).
- **Read order:** Section 2 (Tree Boosting In a Nutshell) and Section 3 (Split Finding Algorithms) in full. Skip system implementation (Section 4-5) unless interested.
- **Time budget:** 2h
- **Take-away:** Write the regularized objective function in your own notation. Explain in one paragraph why XGBoost penalizes tree complexity directly.

### 6. XGBoost Official Documentation
- **URL:** https://xgboost.readthedocs.io/
- **Why:** Definitive reference for parameters and API. The parameters page in particular is mandatory.
- **Read order:**
  1. "Get Started with XGBoost"
  2. "Python API Reference" (skim)
  3. **"XGBoost Parameters" page in full** (this is the critical one)
  4. "Notes on Parameter Tuning"
- **Time budget:** 1.5h
- **Take-away:** Every hyperparameter listed in your `xgboost_notes.md` template with a one-line description.

### 7. scikit-learn Cross-Validation Documentation
- **URL:** https://scikit-learn.org/stable/modules/cross_validation.html
- **Why:** Foundational time-series CV. The single most common interview question about your project will be "how did you validate?"
- **Read order:** Cross-validation overview + the time-series section specifically. Look at `TimeSeriesSplit` and the diagram showing train/test folds advancing.
- **Time budget:** 30min
- **Take-away:** Explain in one paragraph why random k-fold is wrong for time series.

### 8. Optuna Tutorial
- **URL:** https://optuna.org/ → Tutorial
- **Why:** Bayesian hyperparameter search. Used in Stage 3b (tuning) pass 3.
- **Read order:** Basic tutorial + the XGBoost example + the visualization tutorial.
- **Time budget:** 1h
- **Take-away:** Difference between TPE sampler and random search, and when each is appropriate.

---

## Tier 2: After Stage 3 model runs

### 9. Gu, Kelly, Xiu (2020), "Empirical Asset Pricing via Machine Learning"
- **Citation:** Gu, S., Kelly, B., & Xiu, D. (2020). Empirical Asset Pricing via Machine Learning. *Review of Financial Studies*, 33(5), 2223-2273.
- **Why:** Gold-standard ML-in-finance benchmark. Compares OLS, Ridge, Lasso, Elastic Net, GBM, Random Forest, Neural Nets on US equity returns. You want to know how serious researchers compare these methods.
- **Open access:** Yes, NBER and Chicago Booth working paper versions free.
- **Read order:** Section 2 (methodology), Section 4 (results), tables comparing methods. Skip the deep stat learning theory unless curious.
- **Time budget:** 2h
- **Take-away:** How do they choose which model "wins"? What metric do they trust?

### 10. SHAP TreeExplainer Documentation
- **URL:** https://shap.readthedocs.io/
- **Why:** Explainability for tree models. Used in Stage 3c (interpretation).
- **Read order:** Basic intro + TreeExplainer tutorial.
- **Time budget:** 45min
- **Take-away:** What does a SHAP value actually represent? How is it different from feature importance by gain?

---

## Reference (consult as needed)

### 11. FRED Series Documentation
For each series used in this project:
- **DEXCAUS:** USD/CAD daily noon rate (Canadian dollars per 1 USD).
- **DCOILWTICO:** WTI crude oil spot price, USD per barrel, daily.
- **VIXCLS:** CBOE VIX daily close, not seasonally adjusted.
- **DGS2:** US 2-year Treasury constant maturity yield, daily.
- **DGS10:** US 10-year Treasury constant maturity yield, daily.
- **SP500:** S&P 500 daily close.

Each FRED series page has a description and source notes. Cite these in your data dictionary.

### 12. Bank of Canada Valet API
- **URL:** https://www.bankofcanada.ca/valet/docs
- **Why:** Source for Canadian rates. Free, no key needed.
- **Series (modern API format):**
  - **BD.CDN.2YR.DQ.YLD:** Canada benchmark 2-year bond yield, daily.
  - **BD.CDN.10YR.DQ.YLD:** Canada benchmark 10-year bond yield, daily.
  - **FXUSDCAD / FXCADUSD:** USD/CAD daily noon rate (BoC's own version, alternative to FRED's DEXCAUS).

---

## Tier 3: Optional, only if you go deeper

### 13. Lopez de Prado (2018), "Advances in Financial Machine Learning"
- **Citation:** Lopez de Prado, M. (2018). *Advances in Financial Machine Learning*. Wiley.
- **Why:** Covers walk-forward CV, purged k-fold, embargo periods, info leakage. The "right" way to do CV in finance.
- **Open access:** No, paid book. Some chapters discussed in his papers.
- **Worth it?** Only if you continue doing finance ML beyond this project. For v1, sklearn's TimeSeriesSplit is enough.

### 14. Hyndman & Athanasopoulos, "Forecasting: Principles and Practice"
- **URL:** https://otexts.com/fpp3/ (free online)
- **Why:** General forecasting textbook. The cross-validation chapter is excellent.
- **Read order:** Skim only the time-series cross-validation chapter if you want a second source on the topic.

---

## Total reading time budget

| Tier | Hours |
|---|---|
| Tier 1 FX (before Stage 1) | 5-8 |
| Tier 1 XGBoost (before Stage 3) | 4-6 |
| Tier 2 (after Stage 3) | 2-3 |
| Tier 3 | optional |

**Reading is a deliverable, not overhead.** The notes you write while reading (`fx_primer.md`, `xgboost_notes.md`) are graded artifacts of the project, not throwaway scratch work.

---

## Stage 4 (optional) Local Projection / IRF references

### 15. Jordà (2005), "Estimation and Inference of Impulse Responses by Local Projections"
- **Citation:** Jordà, Ò. (2005). Estimation and Inference of Impulse Responses by Local Projections. *American Economic Review*, 95(1), 161-182.
- **Why:** The foundational paper for the LP approach. Distinguishes from VAR-based IRFs.
- **Open access:** Working paper version free on Jordà's UC Davis website.
- **Read order:** Sections on motivation, single-equation LP, comparison to VAR.
- **Time budget:** 1.5h
- **Take-away:** Why does estimating one OLS per horizon (rather than iterating a VAR) give more robust IRFs?

### 16. Plagborg-Møller & Wolf (2021), "Local Projections and VARs Estimate the Same Impulse Responses"
- **Citation:** Plagborg-Møller, M., & Wolf, C. K. (2021). Local Projections and VARs Estimate the Same Impulse Responses. *Econometrica*, 89(2), 955-980.
- **Why:** Modern result showing that LP and VAR identify the same population object. Important context for interpreting your LP results.
- **Open access:** Working paper version free at https://scholar.princeton.edu/mikkelpm/
- **Read order:** Abstract + introduction + Section 2.
- **Time budget:** 1h
- **Take-away:** What does it mean to say LP and VAR are "equivalent in population"? What changes in finite samples?

### 17. (Optional) Kilian (2009), "Not All Oil Price Shocks Are Alike"
- **Citation:** Kilian, L. (2009). Not All Oil Price Shocks Are Alike. *American Economic Review*, 99(3), 1053-1069.
- **Why:** Classic shock-decomposition paper for oil. If you ever upgrade Stage 4 to external instruments, this is the starting point.
- **Open access:** Working paper version free.
- **Time budget:** 1h (optional)
