# CSS/Homepage redesign — v2

## Fix the 404 first (separate from this pass)

In `backend/config/urls.py`, change:
```python
path("games/", include("games.urls")),
```
to:
```python
path("api/games/", include("games.urls")),
```
That's the whole fix — your frontend was calling `/api/games/...`, Django was
only serving `/games/...`.

## What changed visually

- **Bigger everywhere**: hero wordmark now scales up to ~7rem, page titles
  ~3rem+, more line-height room.
- **Wider layout**: container max-width went from 960px → 1180px, so grids
  actually use the screen.
- **Orange accent** (`--ptm-orange: #C1440E`, a burnt/tiger orange, not
  neon): "TIGERS" in the wordmark, LIVE badges, hover states, active nav
  links, eyebrow labels on featured content.
- **Paper grain**: a subtle two-layer dotted texture on `body` (tiny radial
  gradients, not a big flashy gradient) instead of flat off-white.
- **Less repetition**: the homepage was 5 near-identical stacked
  eyebrow+title+badge+button blocks — that repetition was almost certainly
  what read as "cluttered." Replaced with: hero → one large featured card
  for whatever's live today → a single 2×2 grid for everything else. The
  games hub (`/games`) got the same treatment — 3 cards in a real grid
  instead of stacked bordered sections.
- Added a proper **`GameCard`** component, shared by the homepage and the
  games hub — this is the first component I built ahead of a second use
  case, but it immediately had two (home + hub), so it earned its place
  rather than being speculative.

## How to apply

Copy `frontend/src/` on top of what you have — this overwrites
`tokens.css`, `global.css`, `Nav.css`, `Nav.jsx`, `Button.css`, `Badge.css`,
`HomePage.jsx/css`, `GamesIndexPage.jsx/css`, `PageHeader.css`, and adds the
new `GameCard.jsx/css`. Nothing else (23 Guesses, App.jsx routing, Layout,
Footer) needed to change.
