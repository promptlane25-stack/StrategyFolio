# Client Analytics Dashboard

A real-time analytics dashboard for tracking StrategyFolio client engagement — built as a single HTML file that pulls data from Google Sheets via a Google Apps Script backend.

## Features

### Top Stats Cards
- **Client Opens** — total visits from clients (excludes self/personal visits)
- **Unique Clients** — distinct client fingerprints (country|city|device|browser)
- **Avg Time on Page** — mean seconds clients spent reading, filterable by Client / Self / All
- **Avg Scroll Depth** — mean scroll percentage per client session, filterable by Client / Self / All
- Filter dropdown on stats cards lets you switch between Client-only, Self-only, or All data

### Visits Table
- Full visit log with columns: timestamp, document, referrer, country, city, device, browser, type
- **Returning Visitor Tags** — ↺ Returning (orange) or New (green) badge per row, based on fingerprint recurrence across client visits
- **Row Selection** — click any row or use checkboxes to select multiple visits
- **Mark as Self / Mark as Client** — buttons to reclassify selected rows; persisted to localStorage and matched by fingerprint going forward
- **Filters** — filter by type (Client / Self / All) and by document

### Scroll Depth Panel
- Breakdown of average scroll depth per document, client visits only

### Time of Day Panel
- Visit distribution across time slots (Morning / Afternoon / Evening / Night), client visits only

## How the Fingerprint System Works

Each visit is fingerprinted as `country|city|device|browser`. When you mark a row as "Self" or "Client", that fingerprint is saved to localStorage and all past and future matching visits are automatically reclassified.

To make a fingerprint permanent across all browsers, add it to the hardcoded arrays near the top of `analytics-dashboard.html`:

```js
var HARDCODED_SELF_FP = ['United Kingdom|Shadwell|Mobile|Safari'];
var HARDCODED_CLIENT_FP = [];
```

## Technical Notes

- **CSP Compatible** — no inline event handlers; all interactions use `addEventListener` (required for GitHub Pages)
- **Data Source** — JSONP requests to a Google Apps Script deployment; no CORS issues
- **localStorage Keys** — `sf_selfFP` (self fingerprints), `sf_clientFP` (client fingerprints)
- **Engagement Cross-referencing** — engagement rows (scroll, time) are matched to visit rows by timestamp (rounded to nearest minute) to infer Client/Self classification

## Files

- `analytics-dashboard.html` — the full dashboard (self-contained, upload to GitHub Pages to deploy)
- `README.md` — this file

## Tracked Pages

All pages under the StrategyFolio domain are tracked, including proposal documents, case studies, and the main landing page.
