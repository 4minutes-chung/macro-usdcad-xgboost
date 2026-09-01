# Macro-Finance Note

## Question

How do oil prices, Canada-US rate spreads, VIX, and U.S. equity-risk conditions relate to USD/CAD over the weekly 2005-2026 sample?

The exchange-rate convention is FRED `DEXCAUS`: Canadian dollars per one U.S. dollar. Higher USD/CAD means USD strength or CAD weakness. FRED documents this unit directly on the `DEXCAUS` page. WTI is FRED `DCOILWTICO`, in dollars per barrel. VIX is FRED `VIXCLS`. Canadian rates come from Bank of Canada Valet.

Sources: [FRED DEXCAUS](https://fred.stlouisfed.org/series/DEXCAUS), [FRED DCOILWTICO](https://fred.stlouisfed.org/series/DCOILWTICO), [FRED VIXCLS](https://fred.stlouisfed.org/series/VIXCLS), [BoC Valet](https://www.bankofcanada.ca/valet/docs).

## Data and transformations

Daily raw series are pulled from FRED and Bank of Canada Valet, capped at 2026-04-30, then resampled to weekly Friday close. The last weekly observation is 2026-04-24 because that is the last Friday on or before the cap. Feature rows run from 2005-03-04 to 2026-04-17 after rolling windows and the 1-week target shift.

The target is:

```text
y_1w(t) = log(USD/CAD at t+1) - log(USD/CAD at t)
```

The structural check passed:

```text
feature count: 12
target alignment max abs error: 0
```

## Descriptive facts

The strongest contemporaneous relationships are sensible:

| Relationship | Correlation |
|---|---:|
| `r_usdcad` vs `r_wti` | -0.377 |
| `r_usdcad` vs `r_equity` | -0.453 |
| `r_usdcad` vs `d_vix` | 0.413 |
| `r_usdcad` vs `d_spread_2y` | -0.323 |

Interpretation:

Oil up tends to coincide with lower USD/CAD, consistent with CAD strength. Equity-risk-on weeks also coincide with lower USD/CAD. VIX increases line up with higher USD/CAD, consistent with USD safe-haven pressure. These are contemporaneous relationships, not forecasts.

## Forecasting warning from EDA

The target correlations are weak:

| Feature vs `y_1w` | Correlation |
|---|---:|
| `spread_2y` | 0.049 |
| `d_vix` | 0.047 |
| `r_equity` | -0.034 |
| `r_wti` | -0.014 |
| `r_usdcad` | -0.017 |

That means Stage 2 and Stage 3 should expect small or zero forecasting gains. This matches the FX literature and the final results.

## Required figures

| Figure | File | Purpose |
|---|---|---|
| USD/CAD level | `outputs/figures/01_usdcad.png` | Exchange-rate history |
| WTI level | `outputs/figures/02_wti.png` | Oil-price history |
| USD/CAD vs WTI normalized | `outputs/figures/03_usdcad_vs_wti.png` | Commodity-currency channel |
| Rolling oil-FX correlation | `outputs/figures/04_rolling_corr_usdcad_wti.png` | Instability of oil relationship |
| CA-US 2Y spread | `outputs/figures/05_spread_2y.png` | Rates/carry block |
| VIX | `outputs/figures/06_vix.png` | Risk-stress block |
| Feature correlation heatmap | `outputs/figures/07_corr_heatmap.png` | Collinearity and target correlations |

## Economic read

The descriptive stage supports the macro-finance framing. Oil, risk sentiment, and equity-risk conditions matter for same-week USD/CAD moves. The evidence does not imply reliable 1-week-ahead predictability. The right story is exchange-rate disconnect at short horizons, not model failure.

## Stage 1 gate

Passed:

1. Data dictionary updated.
2. Data cap enforced.
3. Target alignment check passed.
4. Seven figures saved.
5. Summary stats and correlation table saved.
6. This note exists.
