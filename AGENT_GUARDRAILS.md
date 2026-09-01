# Agent Guardrails

Hard rules any AI agent (or me, future-session) must follow when working on this project. These close the common failure modes for forecasting projects in noisy financial domains.

---

## Communication (Steven's preferences)

1. Terse, blunt, minimal. One concrete next step at a time.
2. No em dashes. No Simplified Chinese.
3. Mix English and Cantonese OK.
4. Cantonese profanity is a cognitive overload signal, not hostility. Slow down, simplify the next message.
5. Never fabricate. Never invent citations, metrics, or methods.
6. Say "I cannot confirm this" when uncertain rather than guessing.
7. Cite non-obvious facts.
8. Ask if unclear before mistakes.

## Scope discipline

1. This is **stage-gated**, not flagship-committed. Default stop point: end of Stage 3. Stage 4 is optional.
2. Do not add neural networks (RNN, LSTM, Transformer) in v1.
3. Do not add PCA in v1.
4. Do not exceed 15 features in v1.
5. Do not add a second target variable (4-week-ahead) before 1-week is shipped.
6. Do not introduce alternative data (sentiment, news, macro indicators outside the four factor blocks) in v1.
7. New ideas go in `BACKLOG.md` (create if needed), not into the code.
8. Do not start Stage N+1 before Stage N's ship gate is passed.

## Data discipline

1. All features must be observable at time t. No look-ahead.
2. After any change to `src/features.py` or `src/data.py`, re-run the look-ahead bias check (target alignment test).
3. Use FRED + BoC Valet only. No premium data sources.
4. Cap data at 2026-04-30 to respect knowledge-cutoff hygiene for downstream training.
5. Document every transformation in `data/DATA_DICTIONARY.md`.

## Validation discipline

1. Walk-forward expanding-window CV only. Never random k-fold.
2. The test set is sacred. Touch it once, at the end, for final reporting per stage.
3. Early stopping uses the validation set, never the test set.
4. Hyperparameter tuning uses CV inside the training window.
5. If a result looks too good (OOS R² > 5%, dir-acc > 56%), suspect a bug. Re-check look-ahead bias and data leakage first.

## Stage gates

Each stage has a ship gate. Do not advance until passed. After each gate, decide explicitly: ship-and-stop, or continue.

### Stage 1: Descriptive macro-finance (8-10h)
- Gate 1a: `data/DATA_DICTIONARY.md` complete; look-ahead bias structural check passes.
- Gate 1b: 7 required figures saved; summary stats and correlation table saved.
- Gate 1 ship: `docs/macro_finance_note.md` (4-page write-up) exists.

### Stage 2: Benchmark forecasting (6-8h)
- Gate 2a: `src/features.py` produces feature matrix with proper target shift.
- Gate 2b: Random Walk, AR(1), Ridge all evaluated on test set; benchmark table saved.
- Gate 2 ship: Ridge coefficients reported with prior-sign expectation matching.

### Stage 3: XGBoost depth (12-15h)
- Gate 3a: `docs/xgboost_notes.md` exists; self-check passed without notes.
- Gate 3b: Three tuning passes complete (manual grid, random search, Optuna).
- Gate 3c: Four importance methods reported (gain, weight, cover, permutation) plus SHAP. Regime tables saved.
- Gate 3 ship: `docs/findings.md` written with one-paragraph regime conclusion.

### Stage 4 (optional): LP/IRF (8-12h)
- Gate 4a: `docs/lp_irf_notes.md` covers identification choice and Newey-West rationale.
- Gate 4b: Three IRFs estimated (oil shock, 2Y spread shock, VIX shock).
- Gate 4 ship: Three IRF charts saved with 95% confidence bands and economic interpretation.

## Reporting discipline

1. If RW wins, report it. Do not bury or reframe.
2. Report all benchmark metrics, not just favorable ones.
3. Negative results are valuable. The story is "what we learned about FX predictability," not "my model wins."
4. Four feature importance methods (gain, weight, cover, permutation) reported, not one. They often disagree.
5. SHAP required, but only after Stage 3 main tuning completes.
6. Limitations section is mandatory in README.

## Code discipline

1. Use the highest-leverage package. No manual matrix algebra. No nested loops where vectorization works.
2. No unnecessary comments. Code should be self-explanatory from names.
3. One responsibility per script. Scripts call into `src/`, not the other way.
4. New plotting functions live in `src/plots.py`. New metrics live in `src/evaluation.py`. New interpretation helpers in `src/interpretation.py`. New LP helpers in `src/lp.py`.
5. Format the codebase before any commit if a linter is set up.

## What not to do

1. Do not claim the model can be used for trading.
2. Do not write "AI did this." Write what was decided and validated.
3. Do not skip Stage 3a (theory) to get to Stage 3b (tuning) faster.
4. Do not skip the manual grid in Stage 3b to get to Optuna faster.
5. Do not import `pandas_datareader` (incompatible with current pandas, replaced by direct FRED CSV fetch).
6. Do not silently change a hyperparameter range or a feature definition. Document it.
7. Do not claim causal interpretation of Stage 4 IRFs unless identification is strong.

## If unsure

If the next step is unclear, ask in the conversation. Do not invent.
