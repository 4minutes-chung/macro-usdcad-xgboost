# Local Projection / IRF Notes

## What was estimated

Stage 4 estimates descriptive local projections for USD/CAD weekly log returns. For each horizon `h`:

```text
r_usdcad(t+h) = alpha_h + beta_h * shock(t) + controls(t-1) + error(t,h)
```

Controls are lagged USD/CAD return and lagged 4-week USD/CAD volatility. Standard errors use Newey-West/HAC with 4 lags.

Jorda (2005) motivates local projections as horizon-by-horizon regressions for impulse responses. The AEA abstract emphasizes that LPs can be estimated with simple regressions and are more robust to misspecification than iterating a full dynamic system.

Source: [Jorda 2005, AEA](https://www.aeaweb.org/articles?id=10.1257/0002828053828518).

## Identification warning

This is weak identification. Shocks are AR(1) innovations in the driver:

| Shock | Series |
|---|---|
| Oil shock | `r_wti` innovation |
| Rate-spread shock | `spread_2y` innovation |
| VIX shock | `d_vix` innovation |

These are internal statistical shocks, not external instruments. Results are dynamic associations, not causal effects.

## Scale

The regression coefficient is the USD/CAD log-return response to a one-unit shock. One-unit shocks are too large for oil and VIX, so read signs first. One-standard-deviation shock sizes are:

| Shock | Std. dev. |
|---|---:|
| `r_wti` innovation | 0.0591 |
| `spread_2y` innovation | 0.0768 |
| `d_vix` innovation | 3.4428 |

## Results

### WTI shock

At horizon 0, the response is negative and the 95% band excludes zero:

```text
beta = -0.07563
95% CI = [-0.10562, -0.04564]
```

A one-standard-deviation oil shock implies roughly `-0.07563 * 0.0591 = -0.00447`, or about -45 bp in weekly USD/CAD log return. This is consistent with the commodity-currency prior: oil up, CAD up, USD/CAD down.

After horizon 0, confidence intervals mostly include zero. The dynamic persistence is weak.

### CA-US 2Y spread shock

At horizon 0, the response is negative and the 95% band excludes zero:

```text
beta = -0.04949
95% CI = [-0.06128, -0.03769]
```

A one-standard-deviation spread shock implies roughly `-0.04949 * 0.0768 = -0.00380`, or about -38 bp. This matches the capital-flow sign prior: a wider Canada-US 2Y spread supports CAD and lowers USD/CAD.

Later horizons are not precisely estimated.

### VIX shock

At horizon 0, the response is positive and the 95% band excludes zero:

```text
beta = 0.001466
95% CI = [0.001004, 0.001927]
```

A one-standard-deviation VIX shock implies roughly `0.001466 * 3.4428 = 0.00505`, or about +51 bp. This matches the risk-off prior: higher VIX, stronger USD, higher USD/CAD.

There are additional significant points at horizons 8 and 10, but the alternating signs suggest caution rather than a clean dynamic pattern.

## Charts and tables

| Output | File |
|---|---|
| WTI IRF chart | `outputs/figures/09_irf_wti.png` |
| 2Y spread IRF chart | `outputs/figures/10_irf_spread2y.png` |
| VIX IRF chart | `outputs/figures/11_irf_vix.png` |
| WTI IRF table | `outputs/tables/irf_wti.csv` |
| 2Y spread IRF table | `outputs/tables/irf_spread2y.csv` |
| VIX IRF table | `outputs/tables/irf_vix.csv` |

## Connection to forecasting

LP finds sensible contemporaneous shock responses, but forecasting models still struggle. That is not contradictory. Same-week reactions can be economically clear while next-week conditional mean predictability remains weak.

## Stage 4 gate

Passed with caveat:

1. Three IRF charts saved.
2. Three IRF tables saved.
3. Newey-West/HAC standard errors used.
4. Identification weakness explicitly documented.

Do not describe these as causal IRFs without stronger identification.
