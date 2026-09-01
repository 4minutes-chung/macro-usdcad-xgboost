# FX Primer

## Why FX forecasting is hard

Rossi (2013) frames exchange-rate predictability as conditional on predictor, horizon, sample period, and evaluation method, not as a stable yes/no fact. Meese and Rogoff (1983) set the benchmark: structural exchange-rate models have historically struggled to beat a random walk out of sample. This project therefore treats random walk as the benchmark, not as a strawman.

Sources: [Rossi 2013, AEA](https://www.aeaweb.org/articles?id=10.1257/jel.51.4.1063), [Meese and Rogoff 1983, Rogoff page](https://rogoff.scholars.harvard.edu/publications/empirical-exchange-rate-models-seventies-do-they-fit-out-sample), [ScienceDirect abstract](https://www.sciencedirect.com/science/article/pii/002219968390017X).

## Commodity-currency channel

Canada is a commodity-linked economy, so oil can matter for CAD through terms of trade, current-account expectations, and investor demand for Canadian assets. The sign prior in this repo is: oil return up, CAD up, USD/CAD down. That means `r_wti` should have a negative coefficient when predicting `y_1w`, if the channel carries short-horizon signal.

The Bank of Canada 2024 note motivates three currency risk factors relevant here: broad U.S. dollar exposure, cross-country interest-rate differences, and oil price movements. It also reports that the dollar factor explains more of FX risk-premium variation than carry or oil in their G9 setup, so this repo should not expect oil alone to dominate.

Source: [Bank of Canada SAN 2024-20](https://www.bankofcanada.ca/2024/07/staff-analytical-note-2024-20/).

## Interest-rate channel

The Canada-US spread can matter through capital flows and uncovered interest parity logic. The sign is not clean. A higher Canadian rate relative to the U.S. can support CAD, implying lower USD/CAD. Under UIP-style logic, high-interest-rate currencies can instead be expected to depreciate. Engel (2014) is the survey anchor for why interest parity is central but empirically fragile.

Source: [Engel 2014, NBER WP 19336](https://www.nber.org/papers/w19336).

## Risk-on and risk-off

VIX proxies global risk stress. The prior is: higher VIX, stronger USD safe-haven demand, higher USD/CAD. FRED identifies VIX as an index of near-term volatility expectations from stock-index option prices. In this project, `d_vix` has the expected positive Ridge sign, while the VIX level does not.

Source: [FRED VIXCLS](https://fred.stlouisfed.org/series/VIXCLS).

## Equity-risk proxy decision

The original plan used S&P 500 returns, but FRED now documents that S&P/Dow daily history in FRED includes only 10 years because of the data agreement. That would shrink the feature sample to 2016-2026. To keep the intended 2005 start while staying inside the FRED-only guardrail, the primary full-sample equity feature is `r_equity`, the weekly log return of `NASDAQCOM`.

Sources: [FRED SP500 notes](https://fred.stlouisfed.org/series/SP500), [FRED NASDAQCOM](https://fred.stlouisfed.org/series/NASDAQCOM).

## Implication for this project

The correct expectation is not that XGBoost wins. The correct expectation is a strict benchmark test:

1. Descriptive relationships should look economically sensible.
2. Forecasting gains at 1-week horizon should be small or absent.
3. If model results look too good, suspect leakage before celebrating.

That is exactly what happened: contemporaneous correlations are meaningful, but 1-week-ahead forecast gains are tiny.

## Reading log

| Item | Status | Take-away |
|---|---|---|
| Rossi 2013 | summarized from AEA listing and project reading list | FX predictability is unstable across sample, horizon, predictor, and evaluation method. |
| BoC SAN 2024-20 | summarized from BoC page | CAD exposure is framed around broad USD, carry/rates, and oil factors. |
| BoC SAN 2025-2 | summarized from BoC page | Recent CAD depreciation discussion separates rate differentials from a broader FX risk premium. |
| Meese and Rogoff 1983 | summarized from author/publisher pages | Random walk remains the benchmark because structural models historically fail out of sample. |
| Engel 2014 | summarized from NBER page | UIP is theoretically central but empirically unreliable, so rate-spread signs are not mechanical. |
