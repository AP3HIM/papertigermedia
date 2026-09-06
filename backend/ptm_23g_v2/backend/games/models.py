from django.db import models


class DailyPuzzle(models.Model):
    """A single day's '23 Guesses' mystery.

    Clues are individual fields (clue_1..clue_8) rather than one JSON blob —
    this is 100% an admin-usability call: editing 8 plain text boxes in the
    Django admin is much easier than hand-editing JSON. Order clue_1 (most
    obscure) through clue_8 (most obvious/giveaway). Leave trailing ones
    blank if a puzzle needs fewer than 8 — `clues` below skips blanks.
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
        help_text="Scheduled date for this puzzle. You don't have to schedule "
        "every date — services.get_daily_puzzle deterministically picks an "
        "active puzzle from the pool for any day that has nothing scheduled.",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to pull this puzzle out of rotation without deleting it.",
    )
    sport = models.CharField(max_length=16, choices=Sport.choices, default=Sport.NBA)
    category = models.CharField(max_length=16, choices=Category.choices, default=Category.PLAYER)
    difficulty = models.CharField(max_length=16, choices=Difficulty.choices, default=Difficulty.MEDIUM)

    answer = models.CharField(max_length=200, help_text="The canonical, display-ready answer.")
    accepted_answers_extra = models.CharField(
        max_length=500,
        blank=True,
        help_text='Comma-separated alternate answers/aliases, e.g. "LeBron, Bron, King James". '
        "The canonical answer above is always accepted automatically — don't repeat it here.",
    )

    clue_1 = models.CharField(max_length=280, help_text="Shown first. Start obscure.")
    clue_2 = models.CharField(max_length=280, blank=True)
    clue_3 = models.CharField(max_length=280, blank=True)
    clue_4 = models.CharField(max_length=280, blank=True)
    clue_5 = models.CharField(max_length=280, blank=True)
    clue_6 = models.CharField(max_length=280, blank=True)
    clue_7 = models.CharField(max_length=280, blank=True)
    clue_8 = models.CharField(max_length=280, blank=True, help_text="Last resort. Most obvious.")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.date} — {self.get_category_display()}: {self.answer}"

    @property
    def clues(self):
        raw = [
            self.clue_1, self.clue_2, self.clue_3, self.clue_4,
            self.clue_5, self.clue_6, self.clue_7, self.clue_8,
        ]
        return [c for c in raw if c and c.strip()]

    def normalized_accepted(self):
        variants = {self.answer}
        variants.update(v.strip() for v in self.accepted_answers_extra.split(",") if v.strip())
        return {v.lower() for v in variants if v}
