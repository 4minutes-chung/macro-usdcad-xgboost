# USD/CAD Research Continuation Plan

Status: **DEFERRED-NO-BUILD** (hard wrap 2026-07-31). Steven closed the
archived forecasting project without approving Phase 0. This draft is retained
as a cold design note only. No identification gate, data collection, or
estimation is authorized until an explicit reopen decision with its own time
budget. The weekly forecasting null remains the shipped result.

## 1. Decision and scope

Continue with an economics-led study of the mechanism connecting oil news,
expected relative monetary policy and USD/CAD.

The continuation is not another forecasting-model comparison. The existing
weekly results remain the empirical starting point:

- Tuned XGBoost OOS R2 versus random walk is `0.00031`, with direction
  accuracy `0.49847` and no tree splits.
- The best one-week balanced accuracy is `0.54428` from Elastic Net.
- Logistic has Brier score `0.24898` and log loss `0.69102`.
- Logistic and tuned XGBoost Brier improvements over the historical base rate
  are statistically unresolved, with HAC `p = 0.629` and `p = 0.375`.
- Four-week learned probability forecasts lose to the historical base rate.

These results motivate a better economic question. They are not to be
re-litigated through additional model, feature, threshold or horizon searches.

## 2. Research question

> When defensibly identified oil news moves oil prices, do USD/CAD and the
> expected Canada-US policy-rate differential move jointly in the direction
> predicted by the commodity-currency mechanism?

A secondary descriptive question is whether oil retains incremental
explanatory content for USD/CAD after the expected policy-path revision is
observed.

The secondary result is not a causal mediation estimate.

## 3. Contribution and novelty

[Devereux and Smith, QED Working Paper 1408](https://www.econ.queensu.ca/research/working-papers/1408)
study a present-value mechanism in which commodity prices affect commodity
currencies through expected future relative monetary policy. Their exact
monthly specification must be extracted from the paper before this project
claims to reproduce it.

A generic monetary-policy announcement event study would overlap with recent
Bank of Canada research:

- [Bank of Canada Staff Working Paper 2025-33](https://www.bankofcanada.ca/2025/11/staff-working-paper-2025-33/)
  studies high-frequency BoC and Fed communications and Canadian financial
  markets, including CAD/USD.
- [Bank of Canada Staff Analytical Note 2025-10](https://www.bankofcanada.ca/2025/03/staff-analytical-note-2025-10/)
  studies Canadian asset-price responses to Canadian and US macroeconomic
  announcements.

The proposed contribution is narrower and different:

1. Measure one identified oil-news shock.
2. Measure its response in a matched 12-month-ahead Canada-minus-US
   market-implied policy-rate differential.
3. Measure its response in USD/CAD over one pre-specified horizon.
4. Test the joint signs and restrictions implied by the commodity-currency
   mechanism.

A sample update alone is not novelty. Novelty must come from direct measurement
of the expected-policy-path mechanism and a defensible oil-news design.

## 4. Primary estimands

Let `z_t` be one pre-selected oil-news instrument. Scale it so a positive value
corresponds to oil-price-increasing news.

### Instrument relevance

Estimate the response of WTI futures to `z_t` over the pre-specified price
window:

```text
Delta WTI_t = pi * z_t + controls_t + error_t
```

The relevance diagnostic concerns `pi`. It does not concern the policy-path
equation.

### Reduced-form policy-path response

```text
Delta ExpectedPolicyDifferential_t
    = rho_policy * z_t + controls_t + error_t
```

The expected sign is `rho_policy > 0`: oil-price-increasing supply news should
raise the expected Canadian policy path relative to the US path.

### Reduced-form FX response

```text
CumulativeDeltaLogUSDCAD_t
    = rho_fx * z_t + controls_t + error_t
```

USD/CAD is Canadian dollars per US dollar. The expected sign is `rho_fx < 0`,
meaning CAD appreciation.

If the oil instrument passes its exclusion and relevance gates, responses may
also be scaled per unit of instrumented WTI change using weak-IV-robust
inference. The primary result remains the joint reduced-form response vector.

Do not report `rho_fx / rho_policy`, or the difference between unconditional
and conditional oil coefficients, as a causal mediated share.

## 5. Causal structure and boundaries

```text
Oil-news instrument z
        |
        v
Oil-price innovation ----------------------> USD/CAD
        |                                      ^
        v                                      |
Expected Canada-US policy path ---------------+

Global demand, risk, macro news and policy news may affect all three objects.
```

The proposed instrument can identify reduced-form responses only if its
exclusion argument is credible. It does not independently identify the causal
effect of policy expectations on USD/CAD.

The following boundaries are mandatory:

1. An OPEC or OPEC+ announcement is not automatically an exogenous supply
   shock. Anticipation, leakage, demand information and concurrent news must be
   considered.
2. Conditioning on policy-path revisions creates a descriptive conditional
   regression unless a separate mediator instrument or justified structural
   restriction exists.
3. Market-implied rates contain risk premia, liquidity effects and measurement
   error. The primary object is the market-implied differential, not a pure
   mathematical expectation.
4. `2019-2026` is an extension sample, not proof of a 2018 structural break.

## 6. Phase 0: identification-and-data gate

Time cap: `5-8 hours`. Estimate no USD/CAD equation during this phase.

Create `docs/phase0_identification_data_gate.md` containing:

### 6.1 Exact benchmark target

- Read the Devereux-Smith paper at source.
- Extract its equations, variables, frequency, sample, instruments, estimator,
  restrictions and inference method.
- Separate what can be reproduced exactly from what requires unavailable data.

### 6.2 Novelty matrix

Compare the proposed estimand at the specification level against:

- Devereux and Smith.
- Bank of Canada Staff Working Paper 2025-33.
- Bank of Canada Staff Analytical Note 2025-10.
- The high-frequency target/path and exchange-rate identification literature.

Pass only if the proposed oil-news and expected-policy-path test is genuinely
distinct.

### 6.3 Oil-instrument audit

For each candidate instrument, record:

- Economic shock being measured.
- Construction and original source.
- Frequency and timestamp.
- Sample coverage.
- Exclusion argument.
- Known anticipation, leakage and contamination risks.
- Reproducibility and licensing.

Select exactly one primary candidate before looking at USD/CAD outcomes.

### 6.4 Policy-expectations data audit

Audit Canadian and US contracts needed to construct one matched
12-month-ahead policy differential:

| Requirement | Audit question |
|---|---|
| Canada leg | Can BAX/CDOR and CORRA-based contracts be mapped consistently? |
| US leg | Can Fed funds and SOFR contracts be mapped consistently? |
| Maturity | Can both legs represent the same 12-month-ahead object? |
| Timing | Are settlement or quote timestamps synchronized? |
| Coverage | Are at least 90% of eligible observations available? |
| Rights | Are use, storage and redistribution legally permitted? |
| Premia | How will term, risk and liquidity premia be described? |

The existing guardrail permits only FRED and BoC Valet data. Any named source
outside that boundary requires Steven's explicit approval before ingestion.
Do not replace unavailable market expectations with government bond yields and
pretend the same estimand has been preserved.

### 6.5 Power and timing audit

- Count eligible shock observations after pre-specified exclusions.
- Define one candidate outcome window consistent with the instrument timing.
- Calculate the minimum detectable policy-path and USD/CAD responses.
- Define the smallest economically meaningful effects before estimation.

### 6.6 Phase 0 verdict

Return `GO` only if novelty, identification, data, licensing, coverage and power
all pass. Otherwise return `NO-GO` with the failed gate recorded.

## 7. Phase 1: Devereux-Smith benchmark

Time cap: `8-12 hours`, conditional on Phase 0 passing.

1. Create `docs/ds1408_specification.md` from the source paper.
2. Reproduce the original monthly estimand using its stated objects and
   estimator as closely as available data permit.
3. Report `match`, `partial match` or `non-match`.
4. Quantify and explain every discrepancy.
5. Do not label the later expectations-curve design a replication.

Failure to reproduce the benchmark is not automatically fatal, but unexplained
failure is a stop condition.

## 8. Phase 2: fixed extension

Time cap: `12-18 hours`, conditional on Phases 0 and 1.

Use the fixed extension sample `2019-01-01` through the project's current data
cap, `2026-04-30`.

Before opening the USD/CAD outcome:

1. Pre-specify one oil instrument.
2. Pre-specify one matched 12-month policy-path measure.
3. Pre-specify one FX response horizon.
4. Pre-specify contamination and missing-data exclusions.
5. Pre-specify controls and the HAC lag rule.

Estimate:

1. Instrument relevance: `z_t -> WTI futures change`.
2. Reduced form: `z_t -> expected policy differential`.
3. Reduced form: `z_t -> cumulative log USD/CAD`.
4. The joint sign restriction `rho_policy > 0` and `rho_fx < 0`.

Use HAC inference, small-sample wild bootstrap where appropriate, and
weak-IV-robust confidence sets for any response scaled by instrumented WTI.
If the instrument is event-based, run pre-event placebo windows.

Robustness checks are limited to predeclared timing, contract-splice,
risk-premium and crisis-exclusion variants. Do not search across maturities,
horizons, regimes or algorithms.

## 9. Pass, fail and kill criteria

Stop this specification if any condition holds:

1. No specification-level novelty remains after comparison with the closest
   papers.
2. No reproducible and legally usable policy-expectations data exist.
3. Eligible-observation coverage is below `90%`.
4. No oil instrument has a defensible exclusion argument.
5. The instrument is weak, approximately effective first-stage `F < 10`, and
   weak-IV intervals are uninformative.
6. Prospective power cannot detect the smallest economically meaningful
   response.
7. The original benchmark cannot be reproduced and the discrepancy cannot be
   explained.
8. The result changes sign across the limited, predeclared timing or contract
   mappings.
9. Placebo windows reveal anticipation or timestamp contamination.

Possible valid conclusions include:

- Mechanism-consistent responses.
- Precise near-zero responses.
- An underpowered and unresolved result.
- A data or identification `NO-GO`.

Do not convert a failed gate into a new feature, horizon or model search.

## 10. Planned outputs

1. `docs/phase0_identification_data_gate.md`
2. `docs/ds1408_specification.md`
3. A timestamped pre-analysis specification
4. An instrument/event and exclusion ledger
5. A contract-transition and licensing table
6. Instrument-relevance diagnostics
7. Two primary reduced-form tables
8. Policy-path and USD/CAD response figures with placebo panels
9. A limitations section separating reduced forms from causal mediation

## 11. Future implementation map

No code is authorized by this draft. If Phase 0 returns `GO`, use:

| Path | Responsibility |
|---|---|
| `src/policy_curve.py` | Construct matched Canadian and US policy paths |
| `src/oil_news.py` | Load and validate the selected oil-news instrument |
| `src/event_align.py` | Align timestamps and apply exclusion rules |
| `src/reduced_form.py` | Estimate responses and robust inference |
| `scripts/10_phase0_gate.py` | Produce Phase 0 audit tables |
| `scripts/11_ds1408_benchmark.py` | Run the benchmark reproduction |
| `scripts/12_policy_mechanism.py` | Run the fixed extension |
| `tests/test_event_alignment.py` | Test timing, overlap and look-ahead rules |

Every new series and transformation must be added to
`data/DATA_DICTIONARY.md`.

## 12. Hard prohibitions

1. No model-comparison framing.
2. No causal mediation claim without separate identification.
3. No assumption that OPEC announcements are exogenous.
4. No arbitrary 2018 break claim.
5. No substitution of realized oil returns for a failed instrument.
6. No multiple primary horizons, maturities or windows.
7. No premium or licensed data without explicit approval.
8. No outcome estimation before Phase 0 passes.
9. No trading claim.
10. No assertion of Devereux-Smith details before source extraction.

## 13. Single first action

Read the Devereux-Smith paper at source and create the exact specification
extraction table in `docs/ds1408_specification.md`.

Do not collect new market data or estimate a USD/CAD equation until that table
and the Phase 0 gate dossier exist.
