from django.urls import path

from .views import AdvanceView, NewGameView, ResolveSituationView

# Included from config/urls.py as:
#   path("api/dynasty/", include("dynasty.urls"))
urlpatterns = [
    path("new-game/", NewGameView.as_view(), name="dynasty-new-game"),
    path("advance/", AdvanceView.as_view(), name="dynasty-advance"),
    path("resolve-situation/", ResolveSituationView.as_view(), name="dynasty-resolve-situation"),
]
