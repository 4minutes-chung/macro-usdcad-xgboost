# NotebookLM Source Pack

How to ingest this project's reading list into NotebookLM, plus query starters that exploit NotebookLM's ability to synthesize across sources.

NotebookLM works best when you upload 5-10 high-quality sources and then ask cross-source questions. Resist the urge to dump 50 papers; signal-to-noise drops fast.

---

## Setup

Create two separate notebooks. Keep the FX domain and the XGBoost depth materials apart so cross-source synthesis is sharper.

### Notebook 1: "FX Domain Foundations"

Upload these as sources:

| # | Source | Type | URL / Location |
|---|---|---|---|
| 1 | Rossi (2013) "Exchange Rate Predictability" | PDF | Download from Rossi's website at Duke / ICREA, or JEL via institutional access |
| 2 | BoC Staff Analytical Note 2024-20 "Foreign exchange risk premiums and global currency factors" | URL | https://www.bankofcanada.ca/2024/07/staff-analytical-note-2024-20/ |
| 3 | BoC Staff Analytical Note 2025-2 "Monetary policy, interest rates and the Canadian dollar" | URL | https://www.bankofcanada.ca/2025/02/staff-analytical-note-2025-2/ |
| 4 | Meese & Rogoff (1983) "Empirical exchange rate models of the seventies" | PDF | Find via institutional access; abstract free |
| 5 | Engel (2014) "Exchange Rates and Interest Parity" | PDF | NBER WP 19336, free at https://www.nber.org/papers/w19336 |
| 6 (optional) | Fontaine & Nolin (2016, 2017) BoC SAN 2016-15 + 2017-1 (Systematic Variations in CAD, Parts I + II) | URL | Search bankofcanada.ca |

### Notebook 2: "XGBoost Depth"

Upload these:

| # | Source | Type | URL / Location |
|---|---|---|---|
| 1 | Chen & Guestrin (2016) "XGBoost: A Scalable Tree Boosting System" | PDF | arXiv 1603.02754 |
| 2 | XGBoost Parameters page | URL | https://xgboost.readthedocs.io/en/stable/parameter.html |
| 3 | XGBoost "Notes on Parameter Tuning" | URL | https://xgboost.readthedocs.io/en/stable/tutorials/param_tuning.html |
| 4 | scikit-learn cross-validation chapter | URL | https://scikit-learn.org/stable/modules/cross_validation.html |
| 5 | Optuna basic tutorial | URL | https://optuna.readthedocs.io/en/stable/tutorial/index.html |
| 6 | Gu, Kelly, Xiu (2020) "Empirical Asset Pricing via Machine Learning" | PDF | NBER or Chicago Booth WP version free |
| 7 (optional) | SHAP TreeExplainer documentation | URL | https://shap.readthedocs.io/en/latest/example_notebooks/api_examples/explainers/Tree.html |

---

## Query starters (Notebook 1: FX Domain)

Use these in order. Each one synthesizes across sources.

### Foundation pass

1. "Across all sources, summarize the empirical record on exchange-rate predictability at horizons under 1 month. Distinguish what is settled from what is contested."
2. "What does Meese and Rogoff (1983) establish as the benchmark for FX forecasting, and how does Rossi (2013) update this view?"
3. "Compare the BoC 2024-20 three-factor framework (dollar, carry, oil) with Engel's UIP framework. Where do they agree? Where do they emphasize different mechanisms?"

### Mechanism pass

4. "What does the FX literature say about why oil prices predict CAD movements, and has this relationship weakened over time?"
5. "Explain the forward premium puzzle in one paragraph. Why does it matter that higher-interest-rate currencies tend to appreciate rather than depreciate?"
6. "What is the foreign exchange risk premium, and how does the BoC 2025-2 paper estimate it for CAD?"

### Predictability pass

7. "Across all sources, what factors are claimed to have non-trivial predictive content for short-horizon (1-week to 1-month) FX returns? Rank by evidence strength."
8. "What econometric pitfalls does Rossi (2013) identify in claims of FX predictability? Make a checklist I can apply to my own analysis."
9. "How does sample period choice affect FX predictability results? Identify three regimes where the literature finds different predictability."

### Personal-application pass

10. "I am building a 1-week-ahead USD/CAD forecasting model with oil, rate differentials, and VIX as features. Based on all the sources, what is the most likely outcome of this exercise, and what limitations should I declare upfront?"
11. "If my XGBoost model achieves 5% out-of-sample R² against random walk on USD/CAD at 1-week horizon, is that plausible or suspicious? Cite specific sources."
12. "What benchmarks beyond random walk does the literature use for FX forecasting? List them with citations."

---

## Query starters (Notebook 2: XGBoost Depth)

### Theory pass

1. "Across all sources, explain the regularized objective function in XGBoost, including the role of the Ω(f) term."
2. "What is the difference between gradient boosting and Newton boosting? Where does XGBoost sit?"
3. "Explain the exact split-finding algorithm used by XGBoost. How does it differ from standard CART?"

### Hyperparameter pass

4. "For each XGBoost hyperparameter (max_depth, eta, n_estimators, gamma, min_child_weight, subsample, colsample_bytree, reg_lambda, reg_alpha), write a one-sentence summary, the typical range, and what increasing it does to bias-variance trade-off."
5. "Which hyperparameters matter most for time-series data with small samples and noisy targets? Cite the XGBoost docs and Gu-Kelly-Xiu."
6. "What is early stopping, and why does it require a validation set distinct from the test set?"

### Validation pass

7. "Why is random k-fold cross-validation invalid for time-series data? Explain look-ahead bias with a concrete example."
8. "What is the difference between TimeSeriesSplit, walk-forward CV, and purged k-fold? When is each appropriate?"
9. "Across the sources, what is the consensus on how to validate a financial ML model? Build a checklist."

### Feature importance pass

10. "Compare gain, weight, and cover for tree-based feature importance. When do they disagree, and what does the disagreement mean?"
11. "How does SHAP differ from these three traditional importance measures? What is a SHAP value's exact interpretation?"
12. "What are the failure modes of feature importance in correlated-feature settings?"

### ML-in-finance pass

13. "What does Gu, Kelly, Xiu (2020) conclude about the relative performance of OLS, Lasso, Ridge, Random Forest, GBM, and Neural Networks for asset return prediction? Which one wins, and by what metric?"
14. "How do Gu, Kelly, Xiu handle sample size and overfitting in their ML application to finance?"
15. "What does the literature say about applying tree ensembles to time-series financial data, including the look-ahead-bias risks specific to walk-forward CV?"

---

## Generation prompts (for writing your learning artifacts)

After you've asked NotebookLM enough questions, use it to draft sections:

### For `fx_primer.md`:

> Based on all sources in this notebook, draft a 1-page note for an economics student covering: (1) why short-horizon FX forecasting is hard, (2) the commodity-currency hypothesis and its modern limits, (3) UIP and its empirical failure, (4) risk-on/risk-off and the USD safe-haven, (5) the BoC three-factor framework. Use accessible language. Cite sources inline with author-year.

### For `xgboost_notes.md`:

> Based on all sources in this notebook, draft a study note covering: (1) the regularized boosting objective, (2) every hyperparameter and its role, (3) early stopping mechanics, (4) feature importance methods compared, (5) time-series CV strategies, (6) monotonic constraints. Use accessible language. Cite the XGBoost docs and Chen-Guestrin inline.

Edit the drafts heavily. Do not ship NotebookLM output verbatim. The point of writing the notes is to learn, not to delegate.

---

## Sanity rules for NotebookLM

1. **Verify before trusting.** NotebookLM can hallucinate even from real sources. Check any quoted claim against the original.
2. **Cross-source claims are highest-value.** Single-source summaries you could write yourself.
3. **One question at a time.** Multi-part questions get garbled answers.
4. **Ask for citations.** "Which source says this?" forces NotebookLM to ground its claim.
5. **Iterate.** First answer is rarely the best. Refine with "go deeper on point 2" or "give a counter-example."
6. **No NotebookLM output goes into the project repo verbatim.** Always rewrite in your own words.

---

## (Stage 4 optional) Notebook 3: "Local Projection / IRF"

Only set up this notebook if you commit to Stage 4.

### Sources

| # | Source | Type | URL |
|---|---|---|---|
| 1 | Jordà (2005) "Estimation and Inference of Impulse Responses by Local Projections" | PDF | Working paper version on Jordà's UC Davis page |
| 2 | Plagborg-Møller & Wolf (2021) "Local Projections and VARs Estimate the Same Impulse Responses" | PDF | https://scholar.princeton.edu/mikkelpm/ |
| 3 | Kilian (2009) "Not All Oil Price Shocks Are Alike" | PDF | Working paper version free |
| 4 | (Optional) Your own LP-IV notes from the Lucas neutrality project | text | Paste from your archive |

### Query starters

1. "Explain in one paragraph what Local Projection estimates that a VAR does not, or vice versa."
2. "What does it mean to say LP and VAR estimate the same impulse response in population, per Plagborg-Møller and Wolf?"
3. "What identification assumption is required for LP when the shock is an AR(1) innovation? Is this credible for oil prices?"
4. "Compare the identification strategies Kilian uses for oil shocks. Which would be feasible for a student project with weekly data?"
5. "If I find an IRF whose confidence band excludes zero at horizon 2 but not at horizon 0, what is the economic interpretation?"
6. "What Newey-West lag length would you recommend for LP with weekly data and 12-week maximum horizon? Cite a rule of thumb if one exists."
