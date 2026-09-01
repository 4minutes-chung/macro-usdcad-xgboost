# AGENTS.md

Bootstrap file for any Codex (or other AI) agent working on this project. Read in order:

1. `AGENT_GUARDRAILS.md` (hard rules, non-negotiable)
2. `MASTER_PLAN.md` (stage-gated 4+1 plan)
3. `RESEARCH_PLAN.md` (hypotheses per stage)
4. `READING_LIST.md` (verified citations)
5. `STRATEGIC_RATIONALE.md` (time cap, kill criteria)
6. `BACKLOG.md` (deferred ideas; no active implementation)
7. `docs/FUTURE_EXTENSION_PLAN.md` (future event-study and gradient-boosting gates)
8. `data/DATA_DICTIONARY.md` (every series and feature)
9. This file (project context and current state)

## Project identity

- **Title:** USD/CAD Macro-Financial Forecasting and Interpretation
- **Owner:** Steven Chung, MA Economics, University of Toronto
- **Slot:** P12B portfolio, stage-gated (quick-win at 8-10h, full flagship at 36-45h)
- **Audience:** Macro / FX research, applied econ, model validation, data science (lane depends on stop point)
- **Status:** CLOSED-ARCHIVED (hard wrap 2026-07-31). Stages 1-4, the focused direction extension and the primary one-week tuning pass are built and documented; the forecasting specification is frozen; the oil-news continuation draft is DEFERRED-NO-BUILD; the separate monetary-policy event study remains the adopted but deferred future paper direction.

## What this project is

A macro-financial forecasting and interpretation study with four stages:

1. Descriptive macro-finance (standalone deliverable)
2. Benchmark forecasting (RW, AR(1), Ridge)
3. XGBoost depth (tuning + interpretation)
4. Local Projection / IRF (optional dynamic shock response)

This is **not** "ML on FX" or "trading model." It is hypothesis testing on macro-financial drivers of USD/CAD, with XGBoost as one of several tools and LP as optional dynamic extension.

## Steven's communication style

- Terse and direct. Match the energy.
- Cantonese profanity = cognitive overload signal. Simplify the next message.
- One concrete next step at a time.
- Never em dashes. Never Simplified Chinese.
- Never fabricate. Cite non-obvious facts. "I cannot confirm this" when needed.

## Stage tracking

| Stage | Status | Gate |
|---|---|---|
| 1. Descriptive | shipped | 7 figures + macro_finance_note.md |
| 2. Benchmarks | shipped | RW + AR(1) + Ridge table locked, Ridge coefficients interpreted |
| 3. XGBoost | shipped with null result | xgboost_notes.md + 3 importance methods + SHAP + regime tables |
| 4. LP/IRF (optional) | shipped with weak-identification caveat | 3 IRF charts + lp_irf_notes.md |
| Focused direction extension | shipped with weak 1-week signal | original linear models remain best; tuning improves XGBoost but HAC uncertainty includes no gain; 4-week remains mixed |
| Hard wrap | CLOSED-ARCHIVED 2026-07-31 | continuation DEFERRED-NO-BUILD; OPEN_QUESTIONS locked; POSITIONING pitch filled |

_No active stage. Do not reopen without Steven's explicit scope decision._

## Decision gates

After each stage, decide: ship-and-stop, or continue.

## How to start a session

1. Read this file and the current stage status.
2. Read `AGENT_GUARDRAILS.md` (every session, not just the first).
3. Pick up at the current stage's next substage.
4. If unclear, ask Steven.

## How to end a session

1. Update the stage status table above.
2. Save artifacts to `outputs/` or `docs/`.
3. Commit with a clear message naming the stage and substage.
4. Write open questions to `OPEN_QUESTIONS.md`.

## Hard "no" list

1. No neural networks.
2. No PCA in v1.
3. More than 15 features in v1.
4. Random train/test split.
5. "The model can be used for trading" framing.
6. SHAP before Stage 3c.
7. Optuna before manual grid in Stage 3b.
8. Stage 4 before Stages 1-3 ship.
9. Silent assumption-making.

When in doubt, ask Steven. Better than a mistake.
