from datetime import date, timedelta

from django.test import TestCase

from .models import DailyPuzzle
from .services import check_guess, get_daily_puzzle, score_for_clue_index


class DailyPuzzleDeterminismTests(TestCase):
    def setUp(self):
        self.puzzles = [
            DailyPuzzle.objects.create(
                date=date(2026, 1, 1) + timedelta(days=i),
                answer=f"Player {i}",
                clue_1="clue a", clue_2="clue b", clue_3="clue c",
            )
            for i in range(5)
        ]

    def test_scheduled_date_returns_exact_match(self):
        target = self.puzzles[2]
        self.assertEqual(get_daily_puzzle(target.date), target)

    def test_unscheduled_date_is_deterministic(self):
        unscheduled = date(2030, 6, 1)
        first = get_daily_puzzle(unscheduled)
        second = get_daily_puzzle(unscheduled)
        self.assertEqual(first.id, second.id)

    def test_unscheduled_date_picks_from_active_pool(self):
        unscheduled = date(2030, 6, 1)
        result = get_daily_puzzle(unscheduled)
        self.assertIn(result, self.puzzles)

    def test_inactive_puzzles_are_excluded(self):
        for p in self.puzzles:
            p.is_active = False
            p.save()
        self.assertIsNone(get_daily_puzzle(date(2030, 6, 1)))

    def test_empty_pool_returns_none(self):
        DailyPuzzle.objects.all().delete()
        self.assertIsNone(get_daily_puzzle(date(2030, 6, 1)))


class GuessScoringTests(TestCase):
    def setUp(self):
        self.puzzle = DailyPuzzle.objects.create(
            date=date(2026, 1, 1),
            answer="LeBron James",
            accepted_answers_extra="lebron, bron",
            clue_1="clue 1", clue_2="clue 2", clue_3="clue 3",
        )

    def test_correct_guess_on_first_clue_scores_max(self):
        result = check_guess(self.puzzle, "LeBron James", clue_index=0)
        self.assertTrue(result["correct"])
        self.assertEqual(result["score"], score_for_clue_index(0))

    def test_accepted_alias_counts_as_correct(self):
        result = check_guess(self.puzzle, "  bron ", clue_index=0)
        self.assertTrue(result["correct"])

    def test_wrong_guess_advances_clue_without_revealing_answer(self):
        result = check_guess(self.puzzle, "wrong answer", clue_index=0)
        self.assertFalse(result["correct"])
        self.assertEqual(result["next_clue"], "clue 2")
        self.assertFalse(result["out_of_clues"])
        self.assertIsNone(result["answer"])

    def test_running_out_of_clues_reveals_answer(self):
        result = check_guess(self.puzzle, "wrong", clue_index=2)
        self.assertTrue(result["out_of_clues"])
        self.assertEqual(result["answer"], "LeBron James")
        self.assertEqual(result["score"], 0)
