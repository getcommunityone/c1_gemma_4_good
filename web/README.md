# Hackathon web UI (static)

Runs **without a backend** — suitable for GitHub Pages.

| Route | Feature |
|-------|---------|
| `/` | Home — links to search & data explorer |
| `/search` | Client-side search over `public/data/search-index.json` |
| `/data-explorer` | ACS map + scorecard + jurisdiction quality + Gemma meetings |

## Develop

From **repo root** (recommended):

```bash
npm run install:web
npm run dev
```

Or from this folder:

```bash
cd web
npm install
npm run dev
```

Open http://localhost:5173/c1_gemma_4_good/ (Vite `base` matches GitHub Pages).

## Deploy

Push to `main` — workflow `.github/workflows/gh-pages.yml` publishes `web/dist`.

Enable **Settings → Pages → GitHub Actions** on the repo.

## Data

- **Census map:** `public/data/census-map/` (national + AL county trends; ~10MB)
- **Search:** edit `public/data/search-index.json` or run `../scripts/export_web_demo_index.py`
- **Meetings:** `public/data/gemma-demo/index.json`

Copied from [open-navigator](https://github.com/getcommunityone/open-navigator) `frontend/` — trimmed to explorer + static search only.
