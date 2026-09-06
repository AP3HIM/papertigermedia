from django.urls import path

from .views import GuessView, TodayPuzzleView

# Included from your central api/urls.py as:
#   path("games/", include("games.urls"))
# which puts these at /api/games/23-guesses/...
urlpatterns = [
    path("23-guesses/today/", TodayPuzzleView.as_view(), name="23guesses-today"),
    path("23-guesses/guess/", GuessView.as_view(), name="23guesses-guess"),
]
