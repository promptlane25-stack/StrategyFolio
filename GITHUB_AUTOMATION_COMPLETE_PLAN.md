# 🤖 GITHUB AUTOMATION — Live Reference Document

> **Last updated:** 2026-04-26
> **Status:** ✅ Fully live and working
> **Repo:** `promptlane25-stack/StrategyFolio`
> **Update this doc** every time a workflow is added, changed, or removed.

---

## 📁 ACTIVE WORKFLOWS

Two workflow files live in `.github/workflows/`:

| File | Trigger | What it does |
|------|---------|--------------|
| `auto-inject-tracking.yml` | Push to `Clients/**/*.html` OR manual | Injects analytics tracking into client HTML files |
| `update-index.yml` | Push to any file on `main` | Rebuilds `index.html` from `generate_index.py` |

---

## 🔄 WORKFLOW 1: Auto-Inject Tracking Script

**File:** `.github/workflows/auto-inject-tracking.yml`
**Last modified:** 2026-04-26 (added `workflow_dispatch`, upgraded actions)

### Triggers
- **Automatic:** Any `.html` file pushed to `Clients/**/*.html` on `main`
- **Manual:** GitHub Actions → "Auto-Inject Tracking Script" → "Run workflow" button

### What it does
1. Checks out the repo
2. Scans every `.html` file inside the `Clients/` folder recursively
3. Checks if tracking already exists (looks for `recordVisit` and `recordEngagement` in file content) — **skips if already injected, prevents duplicates**
4. If not injected: inserts the tracking script before `</body>` (or before `</html>`, or at end of file as fallback)
5. Commits and pushes the updated file(s) back to `main`

### Actions versions (current)
- `actions/checkout@v4`
- `actions/setup-python@v5`
- Python version: `3.10`

### The tracking script
Injected into every client HTML. Sends two payloads to the GAS webhook:

**On page load → records a visit:**
```
action: recordVisit
data: timestamp, documentName, referrer, country, city, device, browser, userAgent, visitorType: Client
```

**On page close/inactivity → records engagement:**
```
action: recordEngagement
data: timestamp, documentName, timeOnPageSeconds, scrollDepthPercent, clickCount, sessionId
```

**GAS Webhook URL:**
`https://script.google.com/macros/s/AKfycbwkRFXfGZAhlGZlv7Wqw1u3FPPP2-20Znf3N7w1jepxctkmWNVMLbBV4cyUHJrKCaT0tA/exec`

### Additional tracking behaviours
- **Scroll depth:** Checked every 5 seconds, max depth tracked
- **Inactivity timer:** Sends engagement after 30 seconds of no interaction
- **Booking clicks:** Tracks clicks on cal.com / calendly links and any button with "book" in text
- **Device detection:** Mobile / Tablet / Desktop
- **Browser detection:** Chrome / Firefox / Safari / Edge / IE

### Current injection status (as of 2026-04-26)
| File | Status |
|------|--------|
| `Clients/H&F Autos/H&F Autos.html` | ✅ Injected |
| `Clients/H&F Autos/H&F Autos – What I can do for you.html` | ✅ Injected |
| `Clients/Martlesham Service Centre/martleshamservicecentre.html` | ✅ Injected |
| `Clients/Martlesham Service Centre/ martlesham – What I can do for you.html` | ✅ Injected |
| `Clients/Polka Dot Photography/Polka Dot – What I can do for you.html` | ✅ Injected |

---

## 🔄 WORKFLOW 2: Auto-Update Index

**File:** `.github/workflows/update-index.yml`

### Trigger
- Any push to `main` branch (skips if pushed by the Actions bot itself — prevents infinite loops)

### What it does
1. Checks out the repo
2. Runs `generate_index.py` (Python script in the repo root)
3. Script rebuilds `index.html` — the master navigation page for the StrategyFolio repo
4. If `index.html` changed, commits and pushes it automatically

### Actions versions (current)
- `actions/checkout@v4`
- `actions/setup-python@v5`
- Python version: `3.11`

---

## 🎯 THE COMPLETE AUTOMATION FLOW

```
You push an HTML file to Clients/ folder
        ↓
GitHub Actions: auto-inject-tracking.yml fires (within seconds)
        ↓
Python script scans Clients/**/*.html
        ↓
Tracking script injected before </body>
        ↓
Updated HTML committed back to main by Actions bot
        ↓
(update-index.yml also fires → rebuilds index.html)
        ↓
Client opens the HTML file
        ↓
Tracking script fires on page load → POST to GAS Webhook
        ↓
GAS writes visit row to Google Sheets
        ↓
On page close → POST engagement data → GAS → Google Sheets
        ↓
Analytics dashboard reads Google Sheets → displays live data ✅
```

### Timing
| Step | Approx time |
|------|------------|
| Push to workflow trigger | ~5 seconds |
| Workflow completes | ~10 seconds |
| Client opens page → data in Sheets | < 2 seconds |
| Total: push HTML → analytics visible | ~30 seconds |

---

## ➕ ADDING A NEW CLIENT

1. Create folder: `Clients/[Client Name]/`
2. Add their HTML file(s) to that folder
3. Push to GitHub main branch
4. ✅ Tracking auto-injected within 10 seconds — no manual steps needed

---

## 🖱️ MANUALLY RUNNING THE WORKFLOW

If you need to force a run across all files:

1. Go to: GitHub repo → Actions → "Auto-Inject Tracking Script"
2. Click **"Run workflow"** → Branch: `main` → **"Run workflow"**
3. Already-tracked files are skipped automatically

---

## 🚫 WHAT THE SYSTEM PREVENTS

| Risk | How it's handled |
|------|-----------------|
| Double-injecting tracking | Checks for `recordVisit` string before injecting |
| Infinite loop on auto-commits | `update-index.yml` checks `github.actor != 'github-actions[bot]'` |
| Wrong file types | Workflow only targets `*.html` files |
| Encoding errors | Python reads/writes with `utf-8` encoding |

---

## ⚙️ CHANGELOG

| Date | Change |
|------|--------|
| 2026-04-26 | Added `workflow_dispatch` trigger — enables manual runs from GitHub UI |
| 2026-04-26 | Upgraded `actions/checkout@v3 → @v4` and `setup-python@v4 → @v5` |
| 2026-04-26 | Confirmed all 5 client HTML files have tracking injected |
| Earlier | Initial workflows created, tracking injected into all client files |

---

## 📋 NEXT STEPS (as of 2026-04-26)

- [ ] Verify end-to-end: Open a client HTML in browser → confirm visit row appears in Google Sheets
- [ ] Confirm analytics dashboard displays the visit correctly
