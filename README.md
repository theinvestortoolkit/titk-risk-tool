# titk-risk-tool

Risk Profile Calculator for members.theinvestortoolkit.com — 13-question questionnaire,
1–10 blended tolerance/capacity score, four-bucket ("Infinity" framework) portfolio
allocation, and a 20-year synthetic backtest vs. the S&P 500.

## Structure

- `frontend/index.html` — standalone HTML/CSS/JS fragment (no doctype/html/head/body),
  embedded directly in an Elementor HTML widget on a PMPro-protected page. Fetches
  `data/historical.json` from this repo's `main` branch (raw.githubusercontent.com) and
  blends the four bucket proxies client-side per the user's score.
- `scripts/fetch_historical.py` — pulls 20 years of trailing daily price history for the
  bucket proxies (SHY, SPXX, VNQ, SPY) via yfinance, normalizes to a growth-of-$1 index,
  writes `data/historical.json`.
- `.github/workflows/fetch_historical.yml` — runs the fetch script monthly and commits
  the refreshed JSON.
- `data/historical.json` — generated output, committed by the workflow (not hand-edited).

## Bucket proxies

| Bucket | Ticker |
|---|---|
| Cash | SHY |
| Income | SPXX |
| Real Estate | VNQ |
| Growth | SPY |

## Notes

- This repo is public intentionally — it only contains historical ETF price data and
  the allocation math, both already fully visible in the shipped frontend JS to any
  logged-in member. No auth, no user data, nothing sensitive.
- Auth/paywall is handled entirely by PMPro on the WordPress site — this tool has no
  login of its own.
