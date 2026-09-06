# Wiring up 23 Guesses

## Backend (Django)

1. Copy `backend/games/` into your Django project root (next to `sports/`,
   `simulations/`, `articles/`).

2. In `config/settings.py`, add to `INSTALLED_APPS`:
   ```python
   INSTALLED_APPS = [
       ...
       "rest_framework",
       "games",
   ]
   ```
   (add `djangorestframework` to your requirements if it isn't already there —
   it's the only new dependency this needs)

3. In whichever file aggregates your API routes (e.g. `api/urls.py`), add:
   ```python
   path("games/", include("games.urls")),
   ```
   That puts the two endpoints at:
   - `GET  /api/games/23-guesses/today/`
   - `POST /api/games/23-guesses/guess/`

4. Run migrations and seed sample puzzles:
   ```bash
   python manage.py makemigrations games
   python manage.py migrate
   python manage.py seed_23guesses
   ```

5. (Optional but recommended) add puzzles for real from now on via
   `/admin/games/dailypuzzle/` instead of the seed command — the seed data
   is just launch-week filler.

## Frontend (React/Vite)

1. Copy `frontend/src/games/twentyThreeGuesses/`, `frontend/src/pages/TwentyThreeGuessesPage.jsx`,
   and `frontend/src/lib/api.js` into your existing `src/` tree (merge `lib/`
   if you already have one).

2. Import `styles/tokens.css` once, globally (e.g. in `main.jsx` or `App.jsx`):
   ```js
   import "./styles/tokens.css";
   ```

3. Add the route in `App.jsx`:
   ```jsx
   import TwentyThreeGuessesPage from "./pages/TwentyThreeGuessesPage";
   // ...
   <Route path="/games/23-guesses" element={<TwentyThreeGuessesPage />} />
   ```

4. In dev, proxy `/api` to Django so you don't need CORS headers. In
   `vite.config.js`:
   ```js
   export default defineConfig({
     plugins: [react()],
     server: {
       proxy: { "/api": "http://localhost:8000" },
     },
   });
   ```
   In production, if the frontend and API end up on different domains,
   you'll need `django-cors-headers` — not needed yet.

That's it — `/games/23-guesses` should be playable end to end.

## Notes / things I made judgment calls on

- **Scoring**: solving on clue 1 = 1000 pts, decreasing per clue used, 0 if
  you run out. Easy to retune in `backend/games/services.py` (`SCORE_STEPS`).
- **6 clues per puzzle** in the seed data — not literal to the "23" in the
  name, which (per your brief) is about the guessing feel, not a literal
  count. Change per-puzzle by just adding/removing clue strings.
- **Streak/progress** live in `localStorage` only — no accounts yet, matches
  your MVP scope. Once you build user accounts this should move server-side.
- **Anti-peeking**: the guess endpoint only accepts guesses against whatever
  puzzle is actually scheduled for *today* — you can't pass an arbitrary
  `puzzle_id` to see a future puzzle's clues early.
- The 6 seed puzzles are placeholder trivia so the game isn't empty on day
  one — swap them for whatever you actually want to run via the admin.
