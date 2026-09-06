"""Reusable game logic for '23 Guesses', kept separate from views/serializers.

Two responsibilities live here:
  1. get_daily_puzzle(date)  — deterministic puzzle selection for any date
  2. check_guess(...)        — guess validation + scoring, never leaks the
                                answer early
"""

import hashlib

from .models import DailyPuzzle

# Score awarded based on which clue (0-indexed) was showing when the player
# solved it. Solving on the very first clue is worth the most. 8 steps to
# match the 8-clue puzzle format.
SCORE_STEPS = [1000, 900, 800, 700, 600, 500, 350, 200]


def score_for_clue_index(clue_index: int) -> int:
    if clue_index < 0:
        return 0
    if clue_index >= len(SCORE_STEPS):
        return SCORE_STEPS[-1]
    return SCORE_STEPS[clue_index]


def get_daily_puzzle(for_date):
    """Return the puzzle for `for_date`.

    If an active puzzle has been explicitly scheduled for that date, use it.
    Otherwise deterministically pick one from the active pool by hashing the
    date — every player who visits on the same day gets the same puzzle.
    """
    scheduled = DailyPuzzle.objects.filter(date=for_date, is_active=True).first()
    if scheduled is not None:
        return scheduled

    pool = list(DailyPuzzle.objects.filter(is_active=True).order_by("id"))
    if not pool:
        return None

    digest = hashlib.sha256(for_date.isoformat().encode()).hexdigest()
    index = int(digest, 16) % len(pool)
    return pool[index]


def _normalize(guess: str) -> str:
    return (guess or "").strip().lower()


def check_guess(puzzle: DailyPuzzle, guess: str, clue_index: int) -> dict:
    """Validate a guess against `puzzle`.

    `clue_index` is the 0-based index of the clue the player was looking at
    when they submitted this guess. The answer is only included in the
    response when the puzzle is solved or the player has run out of clues.
    """
    total_clues = len(puzzle.clues)
    is_correct = _normalize(guess) in puzzle.normalized_accepted()

    if is_correct:
        return {
            "correct": True,
            "solved": True,
            "out_of_clues": False,
            "answer": puzzle.answer,
            "score": score_for_clue_index(clue_index),
            "clue_index": clue_index,
            "total_clues": total_clues,
        }

    next_index = clue_index + 1
    out_of_clues = next_index >= total_clues

    return {
        "correct": False,
        "solved": False,
        "out_of_clues": out_of_clues,
        "answer": puzzle.answer if out_of_clues else None,
        "score": 0 if out_of_clues else None,
        "next_clue": None if out_of_clues else puzzle.clues[next_index],
        "clue_index": next_index,
        "total_clues": total_clues,
    }
