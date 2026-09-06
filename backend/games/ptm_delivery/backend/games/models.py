from django.db import models


class DailyPuzzle(models.Model):
    """A single day's '23 Guesses' mystery.

    One row = one day's puzzle. `clues` is an ordered list revealed one at a
    time as the player guesses wrong. The canonical `answer` plus any
    `accepted_answers` aliases are never sent to the client until the puzzle
    is solved or the player runs out of clues (see games/services.py).
    """

    class Sport(models.TextChoices):
        NBA = "NBA", "NBA"
        NFL = "NFL", "NFL"
        MLB = "MLB", "MLB"
        NHL = "NHL", "NHL"
        GENERAL = "GENERAL", "General"

    class Category(models.TextChoices):
        PLAYER = "PLAYER", "Player"
        TEAM = "TEAM", "Team"
        SEASON = "SEASON", "Season"
        GAME = "GAME", "Game"
        RECORD = "RECORD", "Record"

    class Difficulty(models.TextChoices):
        EASY = "EASY", "Easy"
        MEDIUM = "MEDIUM", "Medium"
        HARD = "HARD", "Hard"

    date = models.DateField(
        unique=True,
        db_index=True,
        help_text="Scheduled date for this puzzle. Leave puzzles unscheduled "
        "(don't set every date) and the deterministic fallback in "
        "services.get_daily_puzzle will still pick one for any given day.",
    )
    sport = models.CharField(max_length=16, choices=Sport.choices, default=Sport.NBA)
    category = models.CharField(max_length=16, choices=Category.choices, default=Category.PLAYER)
    difficulty = models.CharField(max_length=16, choices=Difficulty.choices, default=Difficulty.MEDIUM)

    answer = models.CharField(max_length=200, help_text="The canonical, display-ready answer.")
    accepted_answers = models.JSONField(
        default=list,
        blank=True,
        help_text='Alternate spellings/nicknames that also count, e.g. ["LeBron", "Bron"].',
    )
    clues = models.JSONField(
        default=list,
        help_text="Ordered list of clue strings, easiest-to-hardest is NOT required — "
        "order them from most-obscure to most-obvious, revealed one at a time.",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.date} — {self.get_category_display()}: {self.answer}"

    def normalized_accepted(self):
        variants = {self.answer, *self.accepted_answers}
        return {v.strip().lower() for v in variants if v and v.strip()}
