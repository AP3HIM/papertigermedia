# Wiring up the UI shell

This is the whole app shell for a currently-empty Vite React app: routing,
layout, nav/footer, a small component kit, and the homepage.

## 1. Install the one new dependency

```bash
npm install react-router-dom
```

## 2. Copy files in

Copy everything under `frontend/src/` into your existing `src/` folder,
merging with anything already there (you should already have
`games/twentyThreeGuesses/`, `pages/TwentyThreeGuessesPage.jsx`, and
`lib/api.js` from the last drop — if `styles/tokens.css` already exists,
these two copies are identical, so either one is fine).

This **replaces** `main.jsx` and `App.jsx` — if you've already put anything
in those, merge by hand rather than overwriting blind.

## 3. Run it

```bash
npm run dev
```

You should get:
- `/` — homepage (hero, today's 23 Guesses, honest "in development"/"planned"
  badges for Dynasty, Stat Challenge, Lab, Archive)
- `/games` — games hub
- `/games/23-guesses` — the live game from last time
- `/games/dynasty`, `/games/stat-challenge`, `/lab`, `/articles` — plain,
  honest placeholder pages (not styled as broken links, not spammed with
  "Coming Soon" — one clear sentence on what's coming)

## What's in the component kit so far

`Button`, `Nav`, `Footer`, `PageHeader`, `SectionHeader`, `Stat`, `Badge`.

That's deliberately a small set — just what the homepage and games hub
actually need right now. I didn't build `DataTable`, `GameCard`, `Tabs`,
`Score`, `Progress`, etc. yet because nothing uses them yet — building them
speculatively is exactly the overbuilding your brief told me to fight.
They'll come out of Dynasty's actual UI needs when we get there, not before.

## Judgment calls

- **Nav has 3 links** (PLAY / LAB / ARCHIVE), matching your brief's core
  pillars. LAB and ARCHIVE go to honest one-line placeholder pages rather
  than 404ing or being hidden — your brief explicitly allows either
  approach, and I'd rather show the shape of the site than hide it.
- **Footer social links** are the real ones pulled from your existing
  `public/index.html` (X, YouTube, Instagram) — not invented.
- Homepage skips "EXPLORE" as its own nav destination for now and points
  that hero button at `/lab` — the brief's mockup has both, but I didn't
  want a third placeholder page duplicating what Lab already says. Easy to
  split later once there's an actual data-explorer page to send it to.
