# Data Dictionary

## Raw series

| Variable | Source | Code | Frequency | Units | Notes |
|---|---|---|---|---|---|
| `usdcad` | FRED | DEXCAUS | Daily | CAD per USD | Daily noon rate. Higher = USD stronger. |
| `wti` | FRED | DCOILWTICO | Daily | USD per barrel | Spot WTI crude. |
| `vix` | FRED | VIXCLS | Daily | Index level | CBOE VIX, close. |
| `us_1y` | FRED | DGS1 | Daily | Percent | US 1-year Treasury constant maturity yield. |
| `us_2y` | FRED | DGS2 | Daily | Percent | US 2Y Treasury constant maturity yield. |
| `us_10y` | FRED | DGS10 | Daily | Percent | US 10Y Treasury constant maturity yield. |
| `spx` | FRED | SP500 | Daily | Index level | S&P 500 close. Source-limited to roughly 10 years of daily history in FRED, so not used as the primary full-sample feature. |
| `nasdaq` | FRED | NASDAQCOM | Daily | Index level | NASDAQ Composite close. Used as the full-sample equity risk proxy because FRED provides daily history back before 2005. |
| `eurusd`, `gbpusd`, `audusd`, `nzdusd` | FRED | DEXUSEU, DEXUSUK, DEXUSAL, DEXUSNZ | Daily | USD per foreign currency | Inputs to the leave-CAD-out global USD factor. |
| `usdjpy`, `usdchf`, `usdnok`, `usdsek` | FRED | DEXJPUS, DEXSZUS, DEXNOUS, DEXSDUS | Daily | Foreign currency per USD | Inputs to the leave-CAD-out global USD factor. |
| `ca_2y` | BoC Valet | BD.CDN.2YR.DQ.YLD | Daily | Percent | Canada benchmark 2Y bond yield. |
| `ca_10y` | BoC Valet | BD.CDN.10YR.DQ.YLD | Daily | Percent | Canada benchmark 10Y bond yield. |
| `ca_1y` | Statistics Canada | Table 10-10-0139-01, vector v39067 | Daily | Percent | Canada 1-year Treasury-bill yield. |

## Engineered features

| Feature | Definition | Observable at t? |
|---|---|---|
| `r_usdcad` | `log(usdcad_t) - log(usdcad_{t-1})` | Yes |
| `vol_usdcad_4w` | rolling 4-week std of `r_usdcad` | Yes |
| `vol_usdcad_8w` | rolling 8-week std of `r_usdcad` | Yes |
| `r_wti` | weekly log return of WTI | Yes |
| `vol_wti_4w` | rolling 4-week std of `r_wti` | Yes |
| `vol_wti_8w` | rolling 8-week std of `r_wti` | Yes |
| `spread_2y` | `ca_2y - us_2y` | Yes |
| `spread_10y` | `ca_10y - us_10y` | Yes |
| `d_spread_2y` | weekly change in `spread_2y` | Yes |
| `vix` | VIX level | Yes |
| `d_vix` | weekly change in VIX | Yes |
| `r_equity` | weekly log return of NASDAQ Composite | Yes |

## Focused direction-classification features

| Feature | Definition | Interpretation |
|---|---|---|
| `policy_spread_1y` | Canada 1-year Treasury-bill yield minus US 1-year Treasury yield | Public proxy for the relative expected policy path; includes term-premium and other yield components. |
| `d_policy_spread_1y` | Weekly change in `policy_spread_1y` | Revision in the relative short-end path proxy. |
| `r_usd_factor` | Equal-weighted, sign-normalized USD return against EUR, GBP, JPY, CHF, AUD, NOK, SEK and NZD | Positive means broad USD appreciation; CAD is excluded to prevent mechanical overlap with the target. |
| `r_wti` | Weekly WTI log return | Oil block. |
| `d_vix` | Weekly VIX change | Global risk block. |
| `d_policy_spread_4w` | Trailing 4-week change in `policy_spread_1y` | Medium-horizon revision in the relative short-end path proxy. |
| `r_usd_factor_4w` | Trailing 4-week leave-CAD-out global USD log return | Medium-horizon broad USD movement. |
| `r_wti_4w` | Trailing 4-week WTI log return | Medium-horizon oil block. |
| `d_vix_4w` | Trailing 4-week VIX change | Medium-horizon global risk movement. |
| `r_usdcad_1w` | Trailing 1-week USD/CAD log return | Own-pair short-run reversal or momentum information. |
| `r_usdcad_4w` | Trailing 4-week USD/CAD log return | Own-pair medium-run reversal or momentum information. |

The primary `core` set is the first five variables. The controlled `extended` tuning set contains all 11 variables. Model selection between the two sets uses only 2017-2019 expanding-window validation forecasts.

## Target

| Variable | Definition | Observable at t? |
|---|---|---|
| `y_1w` | `r_usdcad` shifted forward by one week (`r_usdcad_{t+1}`) | No (only at t+1) |
| `y_4w` | `log(usdcad_{t+4}) - log(usdcad_t)` | No (only at t+4) |
| `direction_1w` | 1 when `y_1w > 0`, otherwise 0 | No |
| `direction_4w` | 1 when `y_4w > 0`, otherwise 0 | No |

## Weekly resampling

Daily series resampled to weekly Friday close using `.resample("W-FRI").last()`. Holidays handled by forward-fill within the week. The weekly sample is then capped at the last Friday on or before 2026-04-30.

## Sample window

Start: 2005-01-01.
End: latest available, capped at 2026-04-30 to respect knowledge-cutoff hygiene.

## Look-ahead bias check

All engineered features use only information available at time t. The one-week target is shifted forward using `.shift(-1)`, and the four-week target uses a four-period forward log difference. Rows without the core features are removed; each model then removes only rows missing its selected feature set or horizon target. This preserves the full core-model history and lets the one-week sample extend three observations beyond the four-week sample.
