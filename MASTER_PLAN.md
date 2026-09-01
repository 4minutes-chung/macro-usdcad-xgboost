# Master Plan: USD/CAD Macro-Financial Forecasting and Interpretation

## 0. Identity

**Title:** USD/CAD Macro-Financial Forecasting and Interpretation
**Subtitle:** A staged study of oil, rates, and risk-sentiment drivers, with XGBoost forecasting and optional local-projection shock analysis.
**Owner:** Steven Chung
**Audience:** Macro / FX research, applied econ, model validation, data science (lane depends on which stages ship).
**Sizing:** Stage-gated. Quick-win (8-10h) to full flagship (34-45h) depending on stop point.
**Status:** Stages 1-4 built and documented; Stage 4 is weak-identification descriptive LP/IRF.

## 1. Why stage-gated

Earlier framing committed to 30-40h upfront. After integrating ChatGPT input and your slow-down signal, the project is restructured into four stages plus one optional extension. Each stage has a real ship gate. You stop where the marginal hour stops paying.

## 2. Research question

**Layer 1 (macro-finance):** How do oil prices, Canada-US interest-rate differentials, and global risk sentiment relate to USD/CAD over 2005-2026?

**Layer 2 (forecasting):** Do these factors improve 1-week-ahead USD/CAD forecasts beyond random-walk and Ridge benchmarks, when modelled with a tuned XGBoost?

**Layer 3 (interpretation):** When the model finds signal, which factor carries it, and under what regimes?

**Layer 4 (dynamics, optional):** How does USD/CAD respond dynamically to shocks in oil, rate differentials, and VIX?

This is not "ML on FX." It is **macro-financial forecasting and interpretation**, with optional dynamic extension.

## 3. Positioning vs other P12B work

| Project | Lane | Distinguishing feature |
|---|---|---|
| HKMFE | HK macro-finance engineering | Multi-module engine (HW, BVAR, BLP) |
| GARCH-EVT gold | Univariate tail risk | Volatility + POT |
| IFRS9 group | Credit risk | Regulatory + group |
| **USD/CAD (this)** | **Cross-asset macro-finance + ML + LP** | **Hypothesis testing + tuning depth + optional shock dynamics** |

If completed through Stage 4, this becomes a second flagship in the FX/macro lane, distinct from HKMFE's engineering focus.

## 4. The four stages

### Stage 1: Descriptive macro-finance analysis (8-10h)

**Goal:** Show that you can do empirical macro work cleanly. This is a standalone deliverable.

Substages:
- 1a. Data + dictionary (3-4h). FRED + BoC Valet pulls. Weekly resampling. Document everything.
- 1b. EDA + required figures (3-4h). 7 figures (USD/CAD vs WTI normalized, rolling correlations, 2Y spread overlay, VIX overlay, correlation heatmap, plus base series plots).
- 1c. Macro-finance interpretation note (2h). 4-page write-up: what the charts say, where the relationships are stable, where they break.

**Stage 1 ship gate:** Figures + summary stats + correlation table + 4-page note in `docs/macro_finance_note.md`. Repo and README polished enough that this alone could go on your portfolio.

**Decision:** Ship-and-stop (quick-win, ~10h total), or continue to Stage 2.

### Stage 2: Benchmark forecasting study (6-8h)

**Goal:** Establish honest benchmark discipline before any ML.

Substages:
- 2a. Feature engineering and look-ahead-bias check (2h).
- 2b. Random Walk, AR(1), and Ridge with walk-forward CV (3h).
- 2c. Benchmark table + Ridge coefficient interpretation (2h). Ridge coefficients are interpretation tool, not just metric. Their signs tell you direction.

**Stage 2 ship gate:** Benchmark table saved. Ridge coefficient signs interpreted economically (do they match theoretical priors from Stage 1?). Lock the benchmark before XGBoost.

**Decision:** Ship-and-stop (quick-win-plus, ~16h total - a clean Meese-Rogoff-style empirical test), or continue to Stage 3.

### Stage 3: XGBoost depth (12-15h)

**Goal:** Deep XGBoost learning, not just fit-and-go.

Substages:
- 3a. XGBoost theory (3-4h). Read Chen & Guestrin 2016 plus parameter docs. Write `docs/xgboost_notes.md` with self-check before tuning.
- 3b. Three-pass tuning (4-5h). Manual grid first (build intuition), random search second (broaden), Optuna last (refine).
- 3c. Final model + interpretation (4-5h). Feature importance (gain/weight/cover all reported), permutation importance, SHAP TreeExplainer. Regime tables: high/low VIX, pre/post-2020, high/low oil vol.
- 3d. Economic interpretation (1-2h). Tie ML findings back to macro mechanisms. Write `docs/findings.md`.

**Stage 3 ship gate:** XGBoost beat or lost to benchmarks honestly. Three importance methods reported. SHAP plot saved. Regime tables saved. `xgboost_notes.md` + `findings.md` exist as standalone learning artifacts.

**Decision:** Ship-and-stop (flagship-adjacent, ~28-33h total), or continue to Stage 4.

### Stage 4 (optional): Local Projection / IRF extension (8-12h)

**Goal:** Add econometric dynamic-response rigor. Builds on your existing LP-IV experience.

Substages:
- 4a. LP theory recap (1h). Jordà (2005) plus your prior LP-IV notes from Lucas project.
- 4b. Shock construction (2-3h). Innovations from AR(1) on each driver, OR external instruments (oil supply shocks if accessible, Romer-Romer monetary surprises).
- 4c. LP estimation (3-4h). Horizon-by-horizon OLS with Newey-West SEs. Horizons 0-12 weeks.
- 4d. IRF plots and interpretation (2-3h). Three IRFs: USD/CAD response to oil shock, 2Y spread shock, VIX shock. Confidence bands.

**Stage 4 ship gate:** Three IRF charts saved. Economic interpretation of each. `docs/lp_irf_notes.md` written.

**Decision:** Done. Full-flagship version shipped (~36-45h total).

## 5. Decision gates - explicit triggers to stop early

You should stop and ship at the current stage's gate (rather than continuing) if any of these are true:

- Applications or interviews demand more than 4h/week of recovered time.
- A Fitch advance requires prep.
- You hit your weekly project cap (8h) and want to redirect.
- The current stage's deliverable already tells a strong portfolio story.
- You realize the next stage has lost interest or interview value for your current pipeline.

## 6. Sizing summary

| Stop point | Total hours | Slot | Story |
|---|---|---|---|
| End of Stage 1 | 8-10h | Quick-win | "Clean empirical macro-finance descriptive study" |
| End of Stage 2 | 14-18h | Quick-win-plus | "Benchmark-disciplined FX forecasting honesty" |
| End of Stage 3 | 26-33h | Flagship-adjacent | "Macro-financial forecasting and interpretation with deep ML" |
| End of Stage 4 | 36-45h | Full flagship | "Macro-financial forecasting, interpretation, and dynamic shock response" |

Pick your stop based on weekly cap, interview pipeline, and marginal value of the next stage.

## 7. What NOT to do (unchanged from AGENT_GUARDRAILS)

1. No neural networks
2. No PCA in v1
3. No more than 15 features in v1
4. No random train/test split
5. No claims of trading profitability
6. No SHAP before Stage 3c
7. No Optuna before manual grid in Stage 3b
8. No data after 2026-04-30
9. No Stage 4 before Stages 1-3 ship
10. No silent feature definition changes

## 8. File map

```
usdcad-macro-xgboost/
├── README.md
├── CLAUDE.md                       (agent bootstrap)
├── AGENT_GUARDRAILS.md             (hard rules)
├── MASTER_PLAN.md                  (this file)
├── RESEARCH_PLAN.md                (hypotheses per stage)
├── POSITIONING.md                  (marketing across lanes)
├── STRATEGIC_RATIONALE.md          (passion vs prospects, time cap)
├── READING_LIST.md                 (verified citations)
├── NOTEBOOKLM_PACK.md              (NotebookLM setup)
├── requirements.txt
├── .gitignore
├── docs/
│   ├── fx_primer_TEMPLATE.md
│   ├── xgboost_notes_TEMPLATE.md
│   ├── lp_irf_notes_TEMPLATE.md    (Stage 4)
│   ├── macro_finance_note.md       (Stage 1 deliverable, write yourself)
│   └── findings.md                 (Stage 3 deliverable, write yourself)
├── src/
│   ├── __init__.py
│   ├── data.py                     (Stage 1)
│   ├── features.py                 (Stage 2)
│   ├── evaluation.py               (Stage 2)
│   ├── interpretation.py           (Stage 3 - permutation, ridge coefs)
│   ├── plots.py                    (all stages)
│   └── lp.py                       (Stage 4)
├── scripts/
│   ├── 01_collect_data.py          (Stage 1a)
│   ├── 02_features.py              (Stage 2a, runs before EDA)
│   ├── 03_eda.py                   (Stage 1b)
│   ├── 04_benchmarks.py            (Stage 2b)
│   ├── 05_xgboost_tuning.py        (Stage 3b)
│   ├── 06_interpretation.py        (Stage 3c)
│   └── 07_lp_irf.py                (Stage 4)
├── data/
│   ├── raw/                        (gitignored)
│   ├── processed/                  (gitignored)
│   └── DATA_DICTIONARY.md
└── outputs/
    ├── figures/
    └── tables/
```
