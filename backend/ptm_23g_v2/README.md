# Applying this update

## 1. Copy files in

Copy `backend/games/models.py`, `admin.py`, `services.py`, `tests.py`, and
`management/commands/seed_23guesses.py` over your existing ones.

## 2. Reset the schema (only safe because it's all placeholder data)

The `DailyPuzzle` model changed shape (per-clue fields instead of one JSON
blob), so old migrations won't line up. Since everything in the DB right
now is seed/placeholder content anyway, easiest path is to wipe and
regenerate rather than write a data migration for throwaway data:

```powershell
cd C:\Dev\papertigermedia\backend
del db.sqlite3
del games\migrations\0*.py
python manage.py makemigrations games
python manage.py migrate
python manage.py seed_23guesses
python manage.py createsuperuser
```

(`del games\migrations\0*.py` removes the numbered migration files but
leaves `__init__.py` alone — that one should stay.)

That gives you 21 puzzles scheduled starting today, one per day.

## 3. What changed

- **8 clues instead of 6**, ordered obscure → obvious on purpose — the
  LeBron puzzle you tried gave too much away in clue 1 ("10 NBA Finals"
  basically only fits him). These new ones open with genuinely obscure
  facts and only become obvious by clue 6-8.
- **Admin now edits clue_1 through clue_8 as plain text fields** instead of
  raw JSON — much easier to write/tweak puzzles without JSON syntax.
- **`is_active` checkbox**, toggleable right from the admin list view —
  pull a puzzle out of rotation without deleting it.
- **Aliases are now a plain comma-separated field** (`accepted_answers_extra`)
  instead of JSON, e.g. `LeBron, Bron, King James`.
- Scoring steps adjusted for 8 clues: `1000, 900, 800, 700, 600, 500, 350, 200`.

No frontend changes needed — it already reads `total_clues` dynamically.

## Going live today — the parts that actually block you

**CORS is the one you'll hit first.** Locally, Vite's dev proxy hides the
fact that your frontend and backend are different origins. On Netlify +
Render they're different domains for real, so you need
`django-cors-headers`:

```bash
pip install django-cors-headers gunicorn
```

In `config/settings.py`:
```python
INSTALLED_APPS = [
    ...,
    "corsheaders",
    "games",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",   # near the top, before CommonMiddleware
    ...,
]

import os
DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")
CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",")
```

On Render, set env vars:
- `DJANGO_ALLOWED_HOSTS` = your Render domain (e.g. `papertigermedia.onrender.com`)
- `CORS_ALLOWED_ORIGINS` = your Netlify URL (e.g. `https://papertigermedia.netlify.app`)
- `DJANGO_DEBUG` = `False`

Start command on Render: `gunicorn config.wsgi`

**The bigger one: SQLite will not survive on Render.** Render's free web
service filesystem is ephemeral — it resets on every deploy/restart, which
means your puzzles (and any admin edits) vanish the next time you push or
the service spins down. Before you rely on this being "live," add Render's
free Postgres and point `DATABASE_URL` at it:

```bash
pip install dj-database-url psycopg2-binary
```
```python
import dj_database_url
if os.environ.get("DATABASE_URL"):
    DATABASES["default"] = dj_database_url.parse(os.environ["DATABASE_URL"])
```

On Netlify: build command `npm run build`, publish directory `dist`, and
set env var `VITE_API_BASE_URL` to your Render URL + `/api`
(e.g. `https://papertigermedia.onrender.com/api`) — locally this defaults
to `/api` and relies on the Vite proxy, which doesn't exist in production.

Say the word when you hit any of these and I'll help you debug the actual
error — Render/Netlify logs are usually pretty clear once you know what
you're looking for.
