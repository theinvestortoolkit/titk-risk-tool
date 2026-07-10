"""
Fetches 20 years of trailing daily price history for the four Risk Analysis
Tool bucket proxies (SHY, SPXX, VNQ, SPY) and writes a normalized growth
index to data/historical.json for the frontend to fetch and blend client-side.

Run monthly via .github/workflows/fetch_historical.yml.
"""
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import yfinance as yf

TICKERS = ["SHY", "SPXX", "VNQ", "SPY"]
LOOKBACK_YEARS = 20
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "historical.json"


def fetch_prices(ticker: str, start: datetime, end: datetime) -> pd.Series:
    history = yf.Ticker(ticker).history(start=start, end=end, auto_adjust=True)
    if history.empty:
        raise RuntimeError(f"No price history returned for {ticker}")
    series = history["Close"]
    series.index = series.index.tz_localize(None)
    return series


def main() -> None:
    end = datetime.now(timezone.utc).replace(tzinfo=None)
    start = end - timedelta(days=LOOKBACK_YEARS * 365 + 5)

    per_ticker = {}
    for ticker in TICKERS:
        per_ticker[ticker] = fetch_prices(ticker, start, end)

    df = pd.concat(per_ticker, axis=1, join="inner").sort_index().ffill().dropna()

    if len(df) < LOOKBACK_YEARS * 200:
        raise RuntimeError(
            f"Aligned history too short ({len(df)} rows) — check ticker data availability"
        )

    normalized = df / df.iloc[0]

    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "start_date": df.index[0].strftime("%Y-%m-%d"),
        "end_date": df.index[-1].strftime("%Y-%m-%d"),
        "tickers": TICKERS,
        "dates": [d.strftime("%Y-%m-%d") for d in df.index],
        "index": {ticker: normalized[ticker].round(6).tolist() for ticker in TICKERS},
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, separators=(",", ":")))
    print(f"Wrote {len(df)} trading days ({payload['start_date']} to {payload['end_date']}) to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
