# Hackathon web UI (static)

Runs **without a backend** — suitable for GitHub Pages.

| Route | Feature |
|-------|---------|
| `/` | Home — links to search & data explorer |
| `/search` | Client-side search over `public/data/search-index.json` |
| `/data-explorer` | ACS map + scorecard + jurisdiction quality + Gemma meetings |

**Live site:** https://getcommunityone.github.io/c1_gemma_4_good/

---

## Develop locally

From **repo root**:

```bash
npm run install:web
npm run dev
```

Open http://localhost:5173/c1_gemma_4_good/

---

## Deploy automatically (recommended)

A GitHub Action builds and publishes on **every push to `main`**:

- Workflow: [`.github/workflows/deploy-github-pages.yml`](../.github/workflows/deploy-github-pages.yml)

**One-time setup:**

1. Push this repo to GitHub (`getcommunityone/c1_gemma_4_good`).
2. Open **Settings → Pages → Build and deployment**
3. **Source:** **GitHub Actions** (not “Deploy from a branch” and not “main / root”).
4. Re-run the failed workflow: **Actions → Deploy to GitHub Pages → Re-run all jobs**

**If deploy fails with `404` / `Failed to create deployment`:** Pages was still on legacy branch deploy. Fix: Settings → Pages → set source to **GitHub Actions**, or run:

```bash
gh api -X PUT repos/getcommunityone/c1_gemma_4_good/pages -f build_type=workflow
```

No `npm run deploy` needed for routine updates.

---

## Deploy manually (`gh-pages` branch)

Optional — pushes `web/dist` to the **`gh-pages`** branch:

```bash
cd web
npm install gh-pages --save-dev   # once
npm run deploy                    # from repo root: npm run deploy
```

If you use this, set **Settings → Pages → Deploy from branch → `gh-pages`**.  
Do **not** mix branch deploy and GitHub Actions unless you pick one source under Settings → Pages.

---

## Data files

- **Census map:** `public/data/census-map/` (~10MB) — must be **in git** (root `.gitignore` uses `/data/` so this folder is not ignored)  
- **Search:** `public/data/search-index.json`  
- **Meetings:** `public/data/gemma-demo/index.json` — `python scripts/export_web_demo_index.py` after §6  

Based on [open-navigator](https://github.com/getcommunityone/open-navigator) `frontend/`.
