# CommunityOne — Pitch Deck (Defying Gravity)

> **How to use:** each `## Slide N` block is one slide. Copy the title, body, and speaker notes into Google Slides / Keynote / PowerPoint. 14 slides total. Designed to land the 3-minute video narrative and back it up with the receipts judges need (Impact 40 / Video 30 / Tech Depth 30 = 100).
>
> **Recommended deck theme:** dark navy background, white serif title, Gemma 4 accent green (#16a34a) for callouts, the *Defying Gravity* lyric as a footer on the title and closing slides.

---

## Slide 1 — Title

**CommunityOne**
*Defying Gravity for Local Democracy*

**Sub-title:** Gemma 4 Good Hackathon · Digital Equity & Inclusivity Track

**Visual:** Wordmark on dark navy. Small footnote: *"You and I — defying gravity."*

**Speaker notes:** Hold for 2 seconds. Let the title breathe. The audience hears the word "Gravity" — they already feel the stakes.

---

## Slide 2 — Act 1 · The "Impossible" Reality

**Headline:** Google told me it was *"technically impossible."*

**Body (one line each, large type):**
- A complete list of every city, county, and school-district website in my state.
- *Technically impossible.*
- Renee's favorite song says: *"through with playing by the rules of someone else's game."*

**Visual:** Side-by-side — a stock "404 Not Found" screenshot and a still from *Defying Gravity*. Or just the Elphaba lyric on the right half, the failed Google query on the left.

**Speaker notes:** This is the emotional hook. Don't explain the technology yet. Let the audience feel that "impossible" is a *choice* somebody else made.

---

## Slide 3 — The Receipt

**Headline:** It wasn't impossible. It was unprofitable.

**Body:**
- CommunityOne is **now the only place** where you can find a free, complete list of local-government websites for every U.S. state.
- 18,000 jurisdictions. Tuscaloosa County. Big Timber, MT. Both in the index.
- **Size shouldn't dictate your importance.**

**Visual:** A live screenshot of the CommunityOne web UX — the jurisdiction directory, with a count badge ("50 states · 18,000+ jurisdictions").

**Speaker notes:** This is the slide that proves Act 1 isn't a complaint, it's a *victory*. The next two acts explain how we make it useful.

---

## Slide 4 — Why this matters

**Headline:** We're running the country on emotions.

**Body:**
- More than half of U.S. counties are now **news deserts** (Northwestern, 2024).
- Our kids are on track for a worse financial future than we had.
- Without facts, we vote on feelings.
- **We believe in an AI revolution powerful enough to map a better path — one we've never tried before.**

**Visual:** Map of the U.S. with news-desert counties shaded red, CommunityOne-indexed jurisdictions overlaid green.

**Speaker notes:** Tie the personal story to a national consequence. The judges' rubric weights *Impact & Vision* at 40 points — this slide is for those 40 points.

---

## Slide 5 — Act 2 · The $500,000 "Public" Paywall

**Headline:** Information is a luxury good.

**Body (three stacked stats):**
- Federal "public" health data: **fees exceeding $500,000**.
- Nonprofit registry aggregators: **thousands of dollars a year** just to *see* a registry.
- Academic gatekeeping: *frame analysis*, *normative tradeoffs*, *dissenting diagnosis* — the **jargon moat**.

**Visual:** Three giant dollar signs on the left. On the right, a redacted academic abstract with red boxes around the jargon.

**Speaker notes:** This is where the audience realizes the problem isn't *availability* — it's *access*. Two moats: financial and linguistic.

---

## Slide 6 — Who gets locked out

**Headline:** If you can't pay the toll or speak the jargon, you stay in the dark.

**Body:**
- A reporter at a five-person paper.
- A Spanish-speaking resident in a rural county.
- A volunteer fire commissioner reading her own minutes.
- A high-school civics student writing a paper.

**Visual:** Four small photographs (or stock illustrations) in a 2x2 grid, each labeled with the persona.

**Speaker notes:** Make the moat concrete. These are not abstractions — they are the people whose decisions we live with.

---

## Slide 7 — Act 3 · The Truly Free Equalizer

**Headline:** CommunityOne is the equalizer.

**Body:**
- Using **Gemma 4**, we built a shared language.
- We map Southern *"fixin' to"* ↔ Northern *"about to."*
- We map *frame analysis* ↔ small-town common sense.
- **One clear view we can all understand.**

**Visual:** A "translation matrix" graphic — three columns labeled "Academic," "Regional," "Plain English" — with five rows of paired terms.

**Speaker notes:** This is the *product* slide. The audience now wants to know how it works.

---

## Slide 8 — The receipts (live web UX)

**Headline:** The receipts.

**Body:**
- Search any jurisdiction.
- Read every decision, in plain English.
- See the **drift map** — what changed between the agenda and the vote.
- Trace the money — donors → legislation → meeting minutes.

**Visual:** Two screenshots of the React UX, side-by-side: (1) jurisdiction search page; (2) policy-drift Mermaid diagram for a real meeting.

**Speaker notes:** This is the second proof-of-life moment (the first was Slide 3). The web UX is the *equalizer in a browser*.

---

## Slide 9 — How Gemma 4 makes it possible

**Headline:** Eight Gemma 4 capabilities, one pipeline.

**Body (table, two columns):**

| Capability                            | What it does for the community               |
| ------------------------------------- | -------------------------------------------- |
| Native multimodality                  | Reads 1990s scanned PDFs no one else can     |
| Adjustable token budget               | Pays attention to budget tables, skims body  |
| Built-in thinking mode                | Publishes the AI's reasoning beside the answer |
| Long-context sliding-window attention | 3-hour meetings fit in one pipeline          |
| Strict JSON / response schema         | Outputs every reporter, journalist, clerk can search |
| Mixed-size deployment (E2B → 31B)     | Runs on a $300 laptop *and* a data center    |
| Local open-weights fallback           | Zero bytes leave the courthouse              |
| ShieldGemma post-hoc review           | Every output reviewed for bias before publish |

**Visual:** The ARCHITECTURE diagram (from ARCHITECTURE.md §1) as the background.

**Speaker notes:** This is the *Technical Depth* slide. The 30 rubric points for "is the technology real, functional, well-engineered" live here.

---

## Slide 10 — Money, meetings, legislation — together

**Headline:** Not just summarizing. **Mapping.**

**Body:**
- We are the only truly free public platform combining:
  - **Meeting notes** (Gemma 4 deconstruction prompt)
  - **Donor dollars** (campaign-finance joins by jurisdiction_id)
  - **Legislation** (cross-jurisdiction EmbeddingGemma clusters)
- *Measure what's actually working.*

**Visual:** A three-circle Venn diagram with CommunityOne in the center.

**Speaker notes:** This is the differentiator vs. Documenters / Granicus / OpenStates. They each do one circle. We do all three, on Gemma 4.

---

## Slide 11 — Trust & safety (Digital Equity is not just "more")

**Headline:** Free doesn't mean reckless.

**Body:**
- Every LLM output reviewed by **ShieldGemma** before publish.
- Demographic enrichment is **opt-in, capped, model-perceived** — explicitly labeled.
- **Offline mode** — flip one env var and zero bytes leave the building.
- All outputs **citable back to a timestamped audio frame or PDF page**.

**Visual:** A "guardrails" graphic — four checkmarks on a navy background.

**Speaker notes:** Pre-empts the obvious judge question: *how do you stop this from harming the communities you claim to serve?*

---

## Slide 12 — Who it's for, Monday morning

**Headline:** What changes Monday morning.

**Body (table):**

| Persona                              | Before                              | With CommunityOne                                |
| ------------------------------------ | ----------------------------------- | ------------------------------------------------ |
| Resident in a news desert            | "I don't know what they did"        | One-page Markdown brief per meeting              |
| Reporter at a five-person paper      | Scrubs 3-hour videos manually       | Drift map shows agenda-vs-vote divergence        |
| Bilingual resident                   | English-only minutes                | `transcript.es.txt` per audio file                |
| State auditor                        | Spot-checks PDFs                    | Cluster identical ordinance language by jurisdiction |
| You                                  | Vote on emotion                     | Vote on evidence                                  |

**Visual:** Five small persona portraits on the left, the table on the right.

**Speaker notes:** Concrete. Five people. Five wins. The judges go home thinking about whose life this changes.

---

## Slide 13 — Ask & call to action

**Headline:** Help us defy gravity for local democracy.

**Body:**
- **Live web UX:** **getcommunityone.github.io/c1_gemma_4_good** (no login, no paywall)
- **GitHub:** github.com/getcommunityone/c1_gemma_4_good (CC-BY-4.0)
- **Run the pipeline:** one Colab notebook, one free `GEMINI_API_KEY`, 45 minutes
- **Track:** Digital Equity & Inclusivity · also eligible Main Track

**Visual:** QR code (top-left) to the live web UX. QR code (top-right) to the GitHub repo. Centered: the Kaggle writeup URL.

**Speaker notes:** Make every link a single tap. Judges will scan with their phone.

---

## Slide 14 — Close

**Headline:** *"You and I — defying gravity."*

**Sub-title:** CommunityOne · Built on Gemma 4 · For the next generation.

**Visual:** Black background. White serif title. Tiny credits line at the bottom — *Built with Gemma 4 · ShieldGemma · EmbeddingGemma. Submitted to the Gemma 4 Good Hackathon, 2026.*

**Speaker notes:** Hold for three seconds of silence. Then black slide. End.

---

## Build notes (for the deck author)

- **Aspect ratio:** 16:9 (Kaggle Media Gallery and YouTube both expect it).
- **Font:** the lyric and titles in a clean serif (Georgia / Source Serif / Lora). Body in a clean sans (Inter / Source Sans).
- **Slide builds:** keep them minimal — one animation per slide max. Judges watch the *video*; the deck supports the video.
- **Brand colors:**
  - Background: `#0b1220` (deep navy)
  - Accent: `#16a34a` (Gemma green)
  - Highlight: `#facc15` (warning yellow, for the $500K paywall stat)
  - Text: `#f8fafc` (warm white)
- **Where the deck shows up:** in the *Media Gallery* of the Kaggle writeup (as a series of slide images) **and** as the visual base for the YouTube video. The pitch deck *is* the storyboard.
