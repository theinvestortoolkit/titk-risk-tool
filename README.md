# titk-risk-tool

Bucket Allocation Profiler for members.theinvestortoolkit.com — 13-question questionnaire,
1–10 blended tolerance/capacity score, four-bucket ("Infinity" framework) portfolio
allocation, and a 20-year synthetic backtest vs. the S&P 500.

## Structure

- `frontend/index.html` — standalone HTML document (has its own doctype/head/body).
  Deploy as `index.html` in a new Bluehost subfolder (e.g. `/calculators/bucket-allocation-profiler/`,
  matching the CC/CSP calculator convention: always a new folder, never overwrite) and
  embed via `<iframe>` on a PMPro-protected WordPress page — required for any tool using
  Chart.js per the site's established embedding rules. Fetches `data/historical.json`
  from this repo's `main` branch (raw.githubusercontent.com) and blends the four bucket
  proxies client-side per the user's score.
- `scripts/fetch_historical.py` — pulls 20 years of trailing daily price history for the
  bucket proxies (SHY, SPXX, VNQ, SPY) via yfinance, normalizes to a growth-of-$1 index,
  writes `data/historical.json`.
- `.github/workflows/fetch_historical.yml` — runs the fetch script monthly and commits
  the refreshed JSON.
- `data/historical.json` — generated output, committed by the workflow (not hand-edited).

## Iframe embedding on the WordPress page

The tool's height changes a lot between the questionnaire and the results view, so it
posts a `titk-risk-tool-resize` message with its current height whenever framed. Add the
iframe plus this small listener in the page's Elementor HTML widget (or a WPCode snippet):

```html
<iframe id="titk-risk-tool-frame" src="https://members.theinvestortoolkit.com/calculators/bucket-allocation-profiler/"
        style="width:100%; border:none; display:block;" title="Bucket Allocation Profiler"></iframe>
<script>
window.addEventListener('message', function (e) {
  if (e.data && e.data.type === 'titk-risk-tool-resize') {
    var frame = document.getElementById('titk-risk-tool-frame');
    if (frame) frame.style.height = e.data.height + 'px';
  }
});
</script>
```

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
